"""Placeur « regles simples » (banc de placement Boomrone) : pas d'optimiseur global.

Flux industriel : 1) pieces fixes (verrouillees) ; 2) pieces principales posees une a une, par
ordre de connectivite, sur une grille grossiere (score = distance pastille -> pastille voisine +
penalites des regles d'isolement) avec un « halo » libre autour pour les futurs satellites ;
3) condensateurs de decouplage : pastille d'alimentation au plus pres de la broche ; 4) passifs
et points de test : pres de la pastille voisine du reseau ; 5) reste pose pres de son bloc.
Toute position est cherchee en spirale sur une grille fine, sans recouvrement (marge 0,3 mm),
dans le contour, 4 rotations.

Usage : python place.py <extract.json> <decouplage.json> <regles_actives.json> <solution.json>
Le .kicad_pcb final s'obtient avec kicad_apply_placement.py (Python KiCad, pcbnew).
"""
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "moteur"))
from pcb_placement import cost, io_data  # noqa: E402

RES, MARGIN, EDGE = 0.05, 0.3, 0.3          # grille d'occupation, ecart courtyard, ecart au contour (mm)
HALO = {"U": 2.2, "J": 1.0, "Q": 0.9, "D": 0.6}   # espace libre laisse aux satellites (phase principale)
HSCALE = float(os.environ.get("HALO_SCALE", "1.0"))        # variante : echelle des halos
W_PEN = 30.0                                # poids (par mm) du manque d isolement (regles > longueur)
ROTS = (0, 90, 180, 270)


class Grid:
    """Occupation du plan, resolution RES. mark() gonfle d'une marge ; free() teste une boite."""
    def __init__(self, outline):
        self.x0, self.y0, self.x1, self.y1 = outline
        self.occ = np.zeros((int((self.y1 - self.y0) / RES) + 2, int((self.x1 - self.x0) / RES) + 2), bool)

    def _cells(self, b, m):
        f = lambda v, o: int(math.floor((v - o) / RES))
        return (max(f(b[1] - m, self.y0), 0), max(f(b[3] + m, self.y0) + 1, 0),
                max(f(b[0] - m, self.x0), 0), max(f(b[2] + m, self.x0) + 1, 0))

    def mark(self, b, m=MARGIN):
        a, c, d, e = self._cells(b, m)
        self.occ[a:c + 1, d:e + 1] = True

    def free(self, b):
        if b[0] < self.x0 + EDGE or b[1] < self.y0 + EDGE or b[2] > self.x1 - EDGE or b[3] > self.y1 - EDGE:
            return False
        a, c, d, e = self._cells(b, 0.0)
        return not self.occ[a:c + 1, d:e + 1].any()


def offsets(step, rmax):
    n = int(rmax / step)
    g = np.arange(-n, n + 1) * step
    dx, dy = np.meshgrid(g, g)
    r = np.hypot(dx, dy).ravel()
    o = np.argsort(r, kind="stable")
    return [(dx.ravel()[i], dy.ravel()[i], r[i]) for i in o if r[i] <= rmax]


class Placer:
    def __init__(self, board):
        self.b, self.placed = board, set()
        self.grid, self.halo = Grid(board.outline), Grid(board.outline)
        self.shapes = {}
        self.rules = [r for r in board.decoupling_rules if r.get("kind") == "eloigner"]
        self.net_small = {n: (len(v.pins) <= 8) for n, v in board.nets.items()}

    # ---- geometrie --------------------------------------------------------------------------
    def shape(self, ref, rot):
        k = (ref, rot)
        if k not in self.shapes:
            c = self.b.components[ref]
            sv = (c.x, c.y, c.rotation)
            c.x = c.y = 0.0
            c.rotation = rot
            self.shapes[k] = (c.world_bbox(), {p.name: c.pad_world_pos(p) for p in c.pads})
            c.x, c.y, c.rotation = sv
        return self.shapes[k]

    def put(self, ref, x, y, rot, halo=0.0):
        c = self.b.components[ref]
        c.x, c.y, c.rotation = x, y, rot
        bb = c.world_bbox()
        self.grid.mark(bb)
        self.halo.mark(bb, MARGIN + halo)
        self.placed.add(ref)

    def fixed_pos(self, ref, pad):
        return self.b.pad_world_pos(ref, pad)

    # ---- score ------------------------------------------------------------------------------
    def targets(self, ref):
        """[(nom_pastille, [positions des pastilles voisines deja posees], poids)] par reseau."""
        out = []
        for p in self.b.components[ref].pads:
            net = self.b.nets.get(p.net)
            if not p.net or "GND" in p.net or net is None:
                continue
            tg = [self.fixed_pos(r, n) for r, n in net.pins if r != ref and r in self.placed]
            if tg:
                out.append((p.name, tg, 1.0 if self.net_small[p.net] else 0.25))
        return out

    def isolement(self, ref, bb):
        """Manque d'isolement (mm) cumule des regles `eloigner` vis-a-vis des pieces deja posees.
        Une piece principale herite des groupes de ses satellites (self.member, marge `extra`)."""
        pen = 0.0
        for i, side, extra in self.member.get(ref, ()):
            r = self.rules[i]
            for o in r["b" if side == "a" else "a"]:
                if o in self.placed and o != ref:
                    pen += max(0.0, r["dmin"] + extra - cost._bbox_gap(bb, self.b.components[o].world_bbox()))
        return W_PEN * pen

    def init_membres(self, main_refs, extra=1.5):
        self.member = {}
        for i, r in enumerate(self.rules):
            for side in ("a", "b"):
                for ref in r[side]:
                    self.member.setdefault(ref, []).append((i, side, 0.0))
        for s, lst in list(self.member.items()):       # heritage : piece principale <- satellites
            if s in main_refs or s not in self.b.components:
                continue
            for n in {p.net for p in self.b.components[s].pads if p.net and "GND" not in p.net}:
                if self.net_small[n]:
                    for m, _ in self.b.nets[n].pins:
                        if m in main_refs and m != s:
                            self.member.setdefault(m, []).extend((i, sd, extra) for i, sd, _ in lst)

    def search(self, ref, hint, step, rmax, score, extra=None, grid=None, rots=ROTS):
        """Cherche (x, y, rot) de score minimal, en spirale autour de `hint` ; s'arrete `extra` mm
        apres le premier candidat libre ET sans manque d'isolement (None = exploration complete)."""
        grid = grid or self.grid
        hx, hy = round(hint[0] / step) * step, round(hint[1] / step) * step
        best, r_ok = None, None
        for dx, dy, r in offsets(step, rmax):
            if r_ok is not None and extra is not None and r > r_ok + extra:
                break
            for rot in rots:
                bb0, pads = self.shape(ref, rot)
                x, y = hx + dx, hy + dy
                bb = (bb0[0] + x, bb0[1] + y, bb0[2] + x, bb0[3] + y)
                if not grid.free(bb):
                    continue
                pen = self.isolement(ref, bb)
                s = score(x, y, rot, bb, pads) + pen
                if best is None or s < best[0]:
                    best = (s, x, y, rot)
                    if pen == 0.0:
                        r_ok = r
        return best

    def nearest_score(self, ref, T, hint):
        def score(x, y, rot, bb, pads):
            if not T:
                return 0.2 * math.hypot((bb[0] + bb[2]) / 2 - hint[0], (bb[1] + bb[3]) / 2 - hint[1])
            return sum(w * min(math.hypot(x + pads[n][0] - tx, y + pads[n][1] - ty) for tx, ty in tg)
                       for n, tg, w in T)
        return score


def is_main(c):
    return (not c.fixed) and (c.ref.startswith(("U", "J", "Q", "D", "SW", "BZ", "LED", "FB", "C6", "C7", "C8"))
                             )


def block_hint(P, ref):
    c = P.b.components[ref]
    pts = [o.world_center() for r, o in P.b.components.items() if r in P.placed and o.block == c.block]
    if not pts:
        pts = [o.world_center() for r, o in P.b.components.items() if r in P.placed]
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def hint_of(T, bb_fallback):
    pts = [t for _, tg, _ in T for t in tg]
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)) if pts else bb_fallback


def main(argv):
    extract, decoup, regles, out = argv[1:5]
    t0 = time.time()
    board = io_data.load_board(extract)
    io_data.apply_decoupling(board, decoup, default_mm=5.0)
    n_dec = len(board.decoupling_rules)
    io_data.apply_active_rules(board, regles)
    dec_rules = board.decoupling_rules[:n_dec]
    P = Placer(board)
    cx, cy = (board.outline[0] + board.outline[2]) / 2, (board.outline[1] + board.outline[3]) / 2

    # 1) pieces fixes
    for r, c in board.components.items():
        if c.fixed:
            P.put(r, c.x, c.y, c.rotation, (HALO.get(r[0], 0.5) if r.startswith("U") else 0.4) * HSCALE)
    # 2) pieces principales : la plus liee aux pieces deja posees d'abord (puis la plus grande)
    main_refs = [r for r, c in board.components.items() if is_main(c)]
    P.init_membres(set(main_refs))
    while main_refs:
        def prio(r):
            T = P.targets(r)
            c = board.components[r]
            return (-sum(w * len(tg) for _, tg, w in T if w == 1.0), -c.courtyard_w * c.courtyard_h, r)
        main_refs.sort(key=prio)
        r = main_refs.pop(0)
        T = P.targets(r)
        hint = hint_of(T, block_hint(P, r))
        h = (HALO.get(r[0], 0.0) if r != "FB1" else 0.0) * HSCALE
        sc = P.nearest_score(r, T, hint)
        best = None
        for grid in (P.halo, P.grid):           # d'abord avec halo, sinon sans (carte saturee)
            best = P.search(r, (cx, cy), 1.0, 40.0, sc, grid=grid)
            if best:
                break
        _, x, y, rot = best
        fine = P.search(r, (x, y), 0.25, 1.0, sc, grid=grid)   # affinage local
        _, x, y, rot = fine or best
        P.put(r, x, y, rot, h)
        print(f"  principale {r:5s} -> ({x:6.2f},{y:6.2f}) {rot:3d} deg")
    # 3) condensateurs de decouplage : pastille d'alimentation au plus pres d'une broche candidate
    used = {}
    for rule in sorted(dec_rules, key=lambda q: (len(q["pins"]), q["cap"])):
        cap, ic = rule["cap"], board.components[rule["ic"]]
        pw = [p.name for p in board.components[cap].pads if p.net == rule.get("net")] or \
             [p.name for p in board.components[cap].pads if "GND" not in p.net]
        best = None
        for pin in [p for p in ic.pads if p.name in rule["pins"]]:
            tgt = ic.pad_world_pos(pin)
            nuse = used.get((rule["ic"], pin.name), 0)

            def sc(x, y, rot, bb, pads, tgt=tgt, nuse=nuse):
                return min(math.hypot(x + pads[n][0] - tgt[0], y + pads[n][1] - tgt[1]) for n in pw) + 1.2 * nuse
            cand = P.search(cap, tgt, 0.25, 12.0, sc, extra=2.5)
            if cand and (best is None or cand[0] < best[0][0]):
                best = (cand, pin.name)
        if best is None:
            print(f"  ECHEC decouplage {cap}")
            continue
        (_, x, y, rot), pn = best
        used[(rule["ic"], pn)] = used.get((rule["ic"], pn), 0) + 1
        P.put(cap, x, y, rot)
        print(f"  decouplage {cap:4s} -> broche {rule['ic']}.{pn} ({x:6.2f},{y:6.2f}) {rot:3d}")
    # 4) et 5) satellites restants : le plus lie en premier ; sans lien, pres de son bloc
    rest = [r for r, c in board.components.items() if r not in P.placed]
    while rest:
        rest.sort(key=lambda r: (r not in P.member, -sum(w * len(tg) for _, tg, w in P.targets(r) if w == 1.0), r))
        r = rest.pop(0)
        T = P.targets(r)
        hint = hint_of(T, block_hint(P, r))
        cand = None
        for rmax in (8.0, 20.0, 60.0):
            cand = P.search(r, hint, 0.25 if rmax < 10 else 0.5, rmax, P.nearest_score(r, T, hint), extra=2.0)
            if cand:
                break
        if cand is None:
            print(f"  ECHEC {r}")
            continue
        _, x, y, rot = cand
        P.put(r, x, y, rot)
    # sortie
    # Le moteur tourne dans le sens horaire a l'ecran (x' = x cos - y sin, y vers le bas) alors que
    # KiCad compte l'angle anti-horaire : on ecrit l'angle oppose pour les pieces mobiles (toutes a
    # 0 deg au depart). Sans cela, une rotation de 90 deg dans le modele donne 270 deg dans KiCad.
    sol = {"source_pcb": board.source_pcb,
           "positions": {r: {"x_mm": round(c.x, 3), "y_mm": round(c.y, 3),
                             "rotation_deg": c.rotation if c.fixed else (-c.rotation) % 360}
                         for r, c in board.components.items()}}
    json.dump(sol, open(out, "w"), indent=1)
    br = cost.total_cost(board, list(board.components), board.nets, cost.CostWeights())
    manque = [r for r in board.components if r not in P.placed]
    print(f"temps {time.time() - t0:.1f} s | non places {manque} | recouvr. {br.overlap_mm2:.2f} | hors contour "
          f"{br.out_of_bounds_mm2:.2f} | HPWL {br.wirelength_mm:.0f} | croisements {br.crossings} | "
          f"exces decouplage {sum(cost.decoupling_excess(board, q) for q in dec_rules):.1f} mm")


if __name__ == "__main__":
    main(sys.argv)
