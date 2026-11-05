"""Cout INCREMENTAL du placement : meme fonction de cout que `cost.total_cost`, mais mise a
jour en ne recalculant que ce qu'un deplacement change (au lieu de tout recalculer a chaque
pas du recuit simule).

Usage (boucle de recuit) :
    ic = IncrementalCost(board, refs, nets, weights)
    ... modifier la position de quelques composants dans `board` ...
    new_cost = ic.propose(["R1", "R2"])      # cout apres deplacement (n'ecrit rien)
    if accepte: ic.commit()                   # fige l'etat
    else:       restaurer `board`, ic.discard()

Ce qui est incremental :
- recouvrement et hors-contour : seules les paires/boites des composants deplaces ;
- HPWL et arbre couvrant : seuls les reseaux touchant un composant deplace ;
- croisements : seules les paires dont un segment appartient a un reseau touche ;
- congestion : grille a origine FIXE (differe un peu de `cost.congestion_grid`, dont la grille
  suit la boite englobante : meme proxy, valeurs absolues legerement differentes) mise a jour
  sur les seules cellules touchees ;
- accessibilite : seules les pastilles du composant deplace et celles dont une sonde
  rencontre l'ancienne ou la nouvelle boite.
L'aire de la carte est recalculee entierement (un min/max numpy, negligeable).

Tout le reste (poids, faisabilite, formule du total) est identique a `cost.total_cost`.
Une resynchronisation complete est faite periodiquement pour eliminer la derive des flottants.
"""
from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .cost import CostBreakdown, CostWeights, decoupling_excess
from .model import Board, Net

_RESYNC_EVERY = 1500   # commits entre deux recalculs complets (derive des flottants)
_CELL_MM = 2.0
_PROBE_MM = 1.5
_AREA_MARGIN_MM = 1.0


def _cross_matrix(a: np.ndarray, b: np.ndarray, nid_a: np.ndarray, nid_b: np.ndarray) -> np.ndarray:
    """Booleens (|a|, |b|) : le segment i de `a` croise strictement le segment j de `b` et ils
    appartiennent a des reseaux DIFFERENTS (meme critere que cost._segments_intersect)."""
    p1x, p1y, p2x, p2y = (a[:, i][:, None] for i in range(4))
    p3x, p3y, p4x, p4y = (b[:, i][None, :] for i in range(4))
    d1 = (p4x - p3x) * (p1y - p3y) - (p4y - p3y) * (p1x - p3x)
    d2 = (p4x - p3x) * (p2y - p3y) - (p4y - p3y) * (p2x - p3x)
    d3 = (p2x - p1x) * (p3y - p1y) - (p2y - p1y) * (p3x - p1x)
    d4 = (p2x - p1x) * (p4y - p1y) - (p2y - p1y) * (p4x - p1x)
    inter = (((d1 > 0) & (d2 < 0)) | ((d1 < 0) & (d2 > 0))) & (((d3 > 0) & (d4 < 0)) | ((d3 < 0) & (d4 > 0)))
    return inter & (nid_a[:, None] != nid_b[None, :])


def _mst_edges(pts: np.ndarray) -> List[Tuple[int, int]]:
    """Arbre couvrant minimal (Prim, depart au point 0, egalites a l'indice le plus bas comme
    cost._net_mst_edges). Chemins rapides pour les petits reseaux (la grande majorite)."""
    k = len(pts)
    if k < 2:
        return []
    if k == 2:
        return [(0, 1)]
    if k <= 6:
        p = pts.tolist()
        hyp = math.hypot
        in_tree = [False] * k
        in_tree[0] = True
        dist = [hyp(p[0][0] - q[0], p[0][1] - q[1]) for q in p]
        parent = [0] * k
        edges = []
        for _ in range(k - 1):
            best, bd = -1, math.inf
            for i in range(k):
                if not in_tree[i] and dist[i] < bd:
                    best, bd = i, dist[i]
            if best == -1:
                break
            in_tree[best] = True
            edges.append((parent[best], best))
            bx, by = p[best]
            for i in range(k):
                if not in_tree[i]:
                    d = hyp(bx - p[i][0], by - p[i][1])
                    if d < dist[i]:
                        dist[i] = d
                        parent[i] = best
        return edges
    D = np.hypot(pts[:, None, 0] - pts[None, :, 0], pts[:, None, 1] - pts[None, :, 1])
    inf = np.inf
    dist = D[0].copy()
    dist[0] = inf
    D[:, 0] = inf           # un point deja dans l'arbre n'est plus jamais mis a jour
    parent = np.zeros(k, dtype=np.int64)
    edges = []
    for _ in range(k - 1):
        best = int(dist.argmin())
        if dist[best] == inf:
            break
        edges.append((int(parent[best]), best))
        dist[best] = inf
        D[:, best] = inf
        d = D[best]
        upd = d < dist
        dist[upd] = d[upd]
        parent[upd] = best
    return edges


def _overlap_rows(box: np.ndarray, others: np.ndarray) -> np.ndarray:
    """Aire de recouvrement entre `box` (4,) ou (m,4) et chaque ligne de `others` (n,4)."""
    box = np.atleast_2d(box)
    dx = np.minimum(box[:, None, 2], others[None, :, 2]) - np.maximum(box[:, None, 0], others[None, :, 0])
    dy = np.minimum(box[:, None, 3], others[None, :, 3]) - np.maximum(box[:, None, 1], others[None, :, 1])
    return np.where((dx > 0) & (dy > 0), dx * dy, 0.0)


class IncrementalCost:
    def __init__(self, board: Board, refs: Sequence[str], nets: Dict[str, Net], weights: CostWeights):
        self.board = board
        self.refs = list(refs)
        self.nets_in = nets
        self.w = weights
        self.base_w = weights
        self.ridx = {r: i for i, r in enumerate(self.refs)}
        self._commits = 0
        self._pending: Optional[dict] = None
        self._build()

    # ------------------------------------------------------------------ construction
    def _boxes(self) -> np.ndarray:
        return np.array([self.board.components[r].world_bbox() for r in self.refs], dtype=float).reshape(-1, 4)

    def _oob_one(self, ref: str, box) -> float:
        b = self.board
        if b.outline is None or ref in b.overhang_refs:
            return 0.0
        x0, y0, x1, y1 = box
        area = max(x1 - x0, 0.0) * max(y1 - y0, 0.0)
        ox0, oy0, ox1, oy1 = b.outline
        dx = min(x1, ox1) - max(x0, ox0)
        dy = min(y1, oy1) - max(y0, oy0)
        inside = dx * dy if dx > 0 and dy > 0 else 0.0
        return max(area - inside, 0.0)

    def _build(self) -> None:
        board, refs = self.board, self.refs
        n = len(refs)
        clr2 = self.w.min_clearance_mm / 2.0
        self.B = self._boxes()
        # recouvrement
        Bi = self.B + np.array([-clr2, -clr2, clr2, clr2])
        if n:
            m = _overlap_rows(Bi, Bi)
            np.fill_diagonal(m, 0.0)
            self.overlap = float(m.sum() / 2.0)
        else:
            self.overlap = 0.0
        self.oob_i = np.array([self._oob_one(r, self.B[i]) for i, r in enumerate(refs)])
        self.oob = float(self.oob_i.sum())

        # pastilles (accessibilite) : tous les pads des composants de refs
        apx, apy, aown, self.aslice = [], [], [], []
        for i, r in enumerate(refs):
            comp = board.components[r]
            a = len(apx)
            for p in comp.pads:
                x, y = comp.pad_world_pos(p)
                apx.append(x); apy.append(y); aown.append(i)
            self.aslice.append((a, len(apx)))
        self.APX = np.array(apx, dtype=float)
        self.APY = np.array(apy, dtype=float)
        self.AOWN = np.array(aown, dtype=int)
        self.acc_i = self._access_for(np.arange(len(self.APX)), self.B, self.APX, self.APY)
        self.access = float(self.acc_i.sum())

        # reseaux : pins valides, positions, HPWL, segments (emplacements fixes)
        self.net_names: List[str] = []
        self.net_pins: List[List[Tuple[str, object, int]]] = []   # (ref, pad, ridx ou -1)
        self.net_pos: List[np.ndarray] = []
        self.ref_pins: Dict[int, List[Tuple[int, int]]] = {}      # ridx -> [(net, pin)]
        for name, net in self.nets_in.items():
            pins = []
            for ref, pad_name in net.pins:
                comp = board.components.get(ref)
                if comp is None:
                    continue
                pad = next((p for p in comp.pads if p.name == pad_name), None)
                if pad is None:
                    continue
                pins.append((ref, pad, self.ridx.get(ref, -1)))
            if len(pins) < 2:
                continue
            ni = len(self.net_names)
            self.net_names.append(name)
            self.net_pins.append(pins)
            for pi, (ref, pad, ri) in enumerate(pins):
                if ri >= 0:
                    self.ref_pins.setdefault(ri, []).append((ni, pi))
            self.net_pos.append(np.array([board.components[r].pad_world_pos(p) for r, p, _ in pins], dtype=float))
        nn = len(self.net_names)
        self.hp = np.array([self._hp(p) for p in self.net_pos]) if nn else np.zeros(0)
        self.wl = float(self.hp.sum())
        # emplacements de segments : k-1 par reseau de k pins
        self.seg_slice: List[Tuple[int, int]] = []
        total = 0
        nid = []
        for ni, pins in enumerate(self.net_pins):
            k = len(pins) - 1
            self.seg_slice.append((total, total + k))
            nid.extend([ni] * k)
            total += k
        self.SEG = np.zeros((total, 4))
        self.NID = np.array(nid, dtype=int)
        for ni in range(nn):
            a, b = self.seg_slice[ni]
            self.SEG[a:b] = self._segs_of(self.net_pos[ni])
        if total:
            cm = _cross_matrix(self.SEG, self.SEG, self.NID, self.NID)
            self.crossings = int(cm.sum() // 2)
        else:
            self.crossings = 0

        # congestion : grille a origine fixe
        if n:
            x0, y0 = self.B[:, 0].min(), self.B[:, 1].min()
            x1, y1 = self.B[:, 2].max(), self.B[:, 3].max()
        else:
            x0 = y0 = x1 = y1 = 0.0
        pad = max(25.0, x1 - x0, y1 - y0)
        self.gx0, self.gy0 = x0 - pad, y0 - pad
        self.nx = max(1, int(math.ceil((x1 - x0 + 2 * pad) / _CELL_MM)))
        self.ny = max(1, int(math.ceil((y1 - y0 + 2 * pad) / _CELL_MM)))
        self.grid = np.zeros(self.nx * self.ny)
        if total:
            idx, wt = self._cong_of(self.SEG)
            np.add.at(self.grid, idx, wt)
        self.comp_cong: List[Tuple[np.ndarray, np.ndarray]] = []
        for i in range(n):
            c = self._comp_cells(self.B[i])
            self.comp_cong.append(c)
            np.add.at(self.grid, c[0], c[1])
        self.cong = float(np.sum(self.grid ** 2))
        self.area = self._area(self.B)
        # regles de decouplage : valeur par regle, index ref -> regles
        self.rules = list(board.decoupling_rules)
        self.rule_val = np.array([decoupling_excess(board, r) for r in self.rules], dtype=float)
        self.dec = float(self.rule_val.sum())
        self.ref_rules: Dict[str, List[int]] = {}
        for k, r in enumerate(self.rules):
            self.ref_rules.setdefault(r["cap"], []).append(k)
            self.ref_rules.setdefault(r["ic"], []).append(k)
        self.current = self._breakdown(self.overlap, self.oob, self.area, self.wl, self.cong,
                                       self.crossings, self.access, self.dec)

    # ------------------------------------------------------------------ helpers de calcul
    @staticmethod
    def _hp(pos: np.ndarray) -> float:
        return float((pos[:, 0].max() - pos[:, 0].min()) + (pos[:, 1].max() - pos[:, 1].min()))

    @staticmethod
    def _segs_of(pos: np.ndarray) -> np.ndarray:
        e = _mst_edges(pos)
        out = np.zeros((len(e), 4))
        for k, (i, j) in enumerate(e):
            out[k] = (pos[i, 0], pos[i, 1], pos[j, 0], pos[j, 1])
        return out

    @staticmethod
    def _match_slots(old: np.ndarray, new: np.ndarray) -> Tuple[np.ndarray, List[int]]:
        """Replace les segments du nouvel arbre dans les emplacements de l'ancien : un segment
        identique (memes extremites) garde son emplacement et sa ligne ; les autres occupent
        les emplacements liberes. Renvoie (lignes, emplacements modifies)."""
        def key(r):
            p, q = (r[0], r[1]), (r[2], r[3])
            return (p, q) if p <= q else (q, p)
        slots: Dict[tuple, List[int]] = {}
        for i in range(len(old)):
            slots.setdefault(key(old[i]), []).append(i)
        rows = old.copy()
        free_new = []
        for r in new:
            lst = slots.get(key(r))
            if lst:
                lst.pop()
            else:
                free_new.append(r)
        free_slots = sorted(i for lst in slots.values() for i in lst)
        for i, r in zip(free_slots, free_new):
            rows[i] = r
        return rows, free_slots

    def _area(self, B: np.ndarray) -> float:
        if len(B) == 0:
            return 0.0
        w = max(B[:, 2].max() - B[:, 0].min() + 2 * _AREA_MARGIN_MM, 0.0)
        h = max(B[:, 3].max() - B[:, 1].min() + 2 * _AREA_MARGIN_MM, 0.0)
        return float(w * h)

    def _cong_of(self, segs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        k = len(segs)
        if k == 0:
            return np.zeros(0, dtype=int), np.zeros(0)
        dx = segs[:, 2] - segs[:, 0]
        dy = segs[:, 3] - segs[:, 1]
        length = np.hypot(dx, dy)
        steps = np.maximum(1, (length / (_CELL_MM / 2.0)).astype(int))
        cnt = steps + 1
        rep = np.repeat(np.arange(k), cnt)
        offs = np.arange(int(cnt.sum())) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        t = offs / steps[rep]
        x = segs[rep, 0] + t * dx[rep]
        y = segs[rep, 1] + t * dy[rep]
        cx = np.floor((x - self.gx0) / _CELL_MM).astype(int)
        cy = np.floor((y - self.gy0) / _CELL_MM).astype(int)
        ok = (cx >= 0) & (cx < self.nx) & (cy >= 0) & (cy < self.ny)
        return (cy[ok] * self.nx + cx[ok]), (1.0 / cnt[rep])[ok]

    def _comp_cells(self, box) -> Tuple[np.ndarray, np.ndarray]:
        bx0, by0, bx1, by1 = box
        cx0 = max(0, int(math.floor((bx0 - self.gx0) / _CELL_MM)))
        cx1 = min(self.nx - 1, int(math.floor((bx1 - self.gx0) / _CELL_MM)))
        cy0 = max(0, int(math.floor((by0 - self.gy0) / _CELL_MM)))
        cy1 = min(self.ny - 1, int(math.floor((by1 - self.gy0) / _CELL_MM)))
        if cx1 < cx0 or cy1 < cy0:
            return np.zeros(0, dtype=int), np.zeros(0)
        xs = np.arange(cx0, cx1 + 1)
        ys = np.arange(cy0, cy1 + 1)
        idx = (ys[:, None] * self.nx + xs[None, :]).ravel()
        return idx, np.full(len(idx), 0.3)

    def _access_for(self, q: np.ndarray, B: np.ndarray, APX: np.ndarray, APY: np.ndarray) -> np.ndarray:
        """Penalite (0/1) des pastilles d'indices `q` : aucune des 4 directions n'est libre."""
        if len(q) == 0:
            return np.zeros(0)
        d = _PROBE_MM
        dirs = np.array([(d, 0), (-d, 0), (0, d), (0, -d)], dtype=float)
        px = APX[q][:, None] + dirs[None, :, 0]          # (Q,4)
        py = APY[q][:, None] + dirs[None, :, 1]
        pr = np.stack([px - 0.2, py - 0.2, px + 0.2, py + 0.2], axis=-1)   # (Q,4,4)
        dx = np.minimum(pr[:, :, None, 2], B[None, None, :, 2]) - np.maximum(pr[:, :, None, 0], B[None, None, :, 0])
        dy = np.minimum(pr[:, :, None, 3], B[None, None, :, 3]) - np.maximum(pr[:, :, None, 1], B[None, None, :, 1])
        blocked = (dx > 0) & (dy > 0)                                     # (Q,4,n)
        own = self.AOWN[q]
        blocked[np.arange(len(q)), :, own] = False                        # on ignore son propre composant
        free = ~blocked.any(axis=2)                                       # (Q,4)
        return np.where(free.any(axis=1), 0.0, 1.0)

    def _breakdown(self, overlap, oob, area, wl, cong, crossings, access, dec=0.0) -> CostBreakdown:
        w = self.w
        vias = round(crossings / 2.0)
        feasible = overlap <= 1e-6 and oob <= 1e-6
        total = (w.area * area + w.wirelength * wl + w.congestion * cong + w.crossings * crossings
                 + w.vias * vias + w.accessibility * access + w.decoupling * dec
                 + w.overlap_penalty_weight * (overlap + oob))
        return CostBreakdown(area_mm2=area, wirelength_mm=wl, congestion=cong, crossings=int(crossings),
                             vias_estimate=int(vias), accessibility_penalty=access,
                             overlap_mm2=overlap, out_of_bounds_mm2=oob, total=total, feasible=feasible,
                             decoupling_mm=dec)

    # ------------------------------------------------------------------ proposition
    def propose(self, moved: Sequence[str]) -> CostBreakdown:
        """Cout si les composants `moved` ont ete deplaces (`board` deja modifie). Ne change
        pas l'etat tant que `commit()` n'est pas appele."""
        board = self.board
        M = sorted({self.ridx[r] for r in moved if r in self.ridx})
        if not M:
            self._pending = None
            return self.current
        Marr = np.array(M, dtype=int)
        clr2 = self.w.min_clearance_mm / 2.0
        infl = np.array([-clr2, -clr2, clr2, clr2])

        # --- boites, recouvrement, hors-contour
        newB = self.B.copy()
        for i in M:
            newB[i] = board.components[self.refs[i]].world_bbox()

        def touch(Bm: np.ndarray) -> float:
            Bi = Bm + infl
            rows = _overlap_rows(Bi[Marr], Bi)          # (m, n)
            rows[np.arange(len(M)), Marr] = 0.0
            return float(rows.sum() - rows[:, Marr].sum() / 2.0)

        overlap = self.overlap - touch(self.B) + touch(newB)
        if abs(overlap) < 1e-9:
            overlap = 0.0
        new_oob_vals = {i: self._oob_one(self.refs[i], newB[i]) for i in M}
        oob = self.oob + sum(new_oob_vals[i] - self.oob_i[i] for i in M)
        if abs(oob) < 1e-9:
            oob = 0.0
        area = self._area(newB)

        # --- positions des pastilles (accessibilite) et des pins de reseaux
        newAPX, newAPY = self.APX.copy(), self.APY.copy()
        for i in M:
            comp = board.components[self.refs[i]]
            a, b = self.aslice[i]
            for k, p in enumerate(comp.pads):
                newAPX[a + k], newAPY[a + k] = comp.pad_world_pos(p)
        touched_nets: Dict[int, np.ndarray] = {}
        for i in M:
            for ni, pi in self.ref_pins.get(i, ()):
                if ni not in touched_nets:
                    touched_nets[ni] = self.net_pos[ni].copy()
                touched_nets[ni][pi] = board.components[self.refs[i]].pad_world_pos(self.net_pins[ni][pi][1])

        # --- reseaux touches : HPWL, segments. Un deplacement ne change que quelques segments
        # d'un reseau (meme d'un gros reseau) : on apparie les segments identiques entre
        # l'ancien et le nouvel arbre et on ne traite que ceux qui different.
        wl = self.wl
        new_hp: Dict[int, float] = {}
        new_rows: Dict[int, np.ndarray] = {}
        changed: List[int] = []
        for ni, pos in touched_nets.items():
            new_hp[ni] = self._hp(pos)
            wl += new_hp[ni] - self.hp[ni]
            a, b = self.seg_slice[ni]
            rows, ch = self._match_slots(self.SEG[a:b], self._segs_of(pos))
            new_rows[ni] = rows
            changed.extend(a + c for c in ch)

        # --- croisements (seulement les segments modifies)
        crossings = self.crossings
        newSEG = None
        idx_parts, w_parts = [], []
        if changed:
            carr = np.array(changed, dtype=int)
            newSEG = self.SEG.copy()
            for ni, rows in new_rows.items():
                a, b = self.seg_slice[ni]
                newSEG[a:b] = rows
            tmask = np.zeros(len(self.SEG), dtype=bool)
            tmask[carr] = True

            def cross_touch(S: np.ndarray) -> int:
                cm = _cross_matrix(S[carr], S, self.NID[carr], self.NID)
                return int(cm.sum() - cm[:, tmask].sum() // 2)

            crossings = self.crossings - cross_touch(self.SEG) + cross_touch(newSEG)
            # congestion : retrait des segments modifies (anciens), ajout des nouveaux
            oi, ow = self._cong_of(self.SEG[carr])
            idx_parts.append(oi); w_parts.append(-ow)
            ci, cw = self._cong_of(newSEG[carr])
            idx_parts.append(ci); w_parts.append(cw)

        # --- congestion : occupation des composants deplaces
        new_cong_comp: Dict[int, Tuple[np.ndarray, np.ndarray]] = {}
        for i in M:
            oi, ow = self.comp_cong[i]
            idx_parts.append(oi); w_parts.append(-ow)
            ci, cw = self._comp_cells(newB[i])
            new_cong_comp[i] = (ci, cw)
            idx_parts.append(ci); w_parts.append(cw)
        idx_all = np.concatenate(idx_parts) if idx_parts else np.zeros(0, dtype=int)
        w_all = np.concatenate(w_parts) if w_parts else np.zeros(0)
        if len(idx_all):
            uniq, inv = np.unique(idx_all, return_inverse=True)
            delta = np.bincount(inv, weights=w_all, minlength=len(uniq))
            g0 = self.grid[uniq]
            cong = self.cong + float(((g0 + delta) ** 2).sum() - (g0 ** 2).sum())
        else:
            uniq = delta = None
            cong = self.cong

        # --- accessibilite : pastilles du composant deplace + pastilles dont une sonde rencontre
        # l'ancienne ou la nouvelle boite
        if len(self.APX):
            d = _PROBE_MM
            dirs = np.array([(d, 0), (-d, 0), (0, d), (0, -d)], dtype=float)
            moved_boxes = np.concatenate([self.B[Marr], newB[Marr]], axis=0)        # (2m,4)
            hit = np.zeros(len(self.APX), dtype=bool)
            for oldAPX, oldAPY in ((self.APX, self.APY), (newAPX, newAPY)):
                px = oldAPX[:, None] + dirs[None, :, 0]
                py = oldAPY[:, None] + dirs[None, :, 1]
                dx = (np.minimum(px[:, :, None] + 0.2, moved_boxes[None, None, :, 2])
                      - np.maximum(px[:, :, None] - 0.2, moved_boxes[None, None, :, 0]))
                dy = (np.minimum(py[:, :, None] + 0.2, moved_boxes[None, None, :, 3])
                      - np.maximum(py[:, :, None] - 0.2, moved_boxes[None, None, :, 1]))
                hit |= ((dx > 0) & (dy > 0)).any(axis=(1, 2))
            hit |= np.isin(self.AOWN, Marr)
            q = np.nonzero(hit)[0]
            new_acc = self._access_for(q, newB, newAPX, newAPY)
            access = self.access - float(self.acc_i[q].sum()) + float(new_acc.sum())
        else:
            q = new_acc = None
            access = self.access

        # --- decouplage : regles dont le condensateur ou le circuit integre a bouge
        dec = self.dec
        new_rule_val: Dict[int, float] = {}
        if self.rules:
            for i in M:
                for k in self.ref_rules.get(self.refs[i], ()):
                    if k not in new_rule_val:
                        new_rule_val[k] = decoupling_excess(board, self.rules[k])
                        dec += new_rule_val[k] - self.rule_val[k]

        bd = self._breakdown(overlap, oob, area, wl, cong, crossings, access, dec)
        self._pending = dict(
            M=M, newB=newB, new_oob_vals=new_oob_vals, newAPX=newAPX, newAPY=newAPY,
            touched_nets=touched_nets, new_hp=new_hp, newSEG=newSEG,
            new_cong_comp=new_cong_comp, uniq=uniq, delta=delta,
            q=q, new_acc=new_acc, totals=(overlap, oob, area, wl, cong, crossings, access),
            new_rule_val=new_rule_val, dec=dec, bd=bd)
        return bd

    def commit(self) -> None:
        p = self._pending
        if p is None:
            return
        self.B = p["newB"]
        for i, v in p["new_oob_vals"].items():
            self.oob_i[i] = v
        self.APX, self.APY = p["newAPX"], p["newAPY"]
        for ni, pos in p["touched_nets"].items():
            self.net_pos[ni] = pos
            self.hp[ni] = p["new_hp"][ni]
        if p["newSEG"] is not None:
            self.SEG = p["newSEG"]
        for i, c in p["new_cong_comp"].items():
            self.comp_cong[i] = c
        if p["uniq"] is not None:
            self.grid[p["uniq"]] += p["delta"]
        if p["q"] is not None and len(p["q"]):
            self.acc_i[p["q"]] = p["new_acc"]
        (self.overlap, self.oob, self.area, self.wl, self.cong, self.crossings, self.access) = p["totals"]
        for k, v in p["new_rule_val"].items():
            self.rule_val[k] = v
        self.dec = p["dec"]
        self.current = p["bd"]
        self._pending = None
        self._commits += 1
        if self._commits % _RESYNC_EVERY == 0:
            self._build()

    def set_penalty_scale(self, f: float) -> CostBreakdown:
        """Multiplie le poids des contraintes dures (recouvrement, hors-contour) par `f` par
        rapport au poids de base, et recalcule le cout courant. A appeler entre deux pas (hors
        proposition en cours). Sert a la penalite progressive du recuit global."""
        import dataclasses
        self._pending = None
        self.w = dataclasses.replace(self.base_w, overlap_penalty_weight=self.base_w.overlap_penalty_weight * f)
        self.current = self._breakdown(self.overlap, self.oob, self.area, self.wl, self.cong,
                                       self.crossings, self.access, self.dec)
        return self.current

    def discard(self) -> None:
        self._pending = None

    def resync(self) -> CostBreakdown:
        """Recalcul complet depuis l'etat courant de `board` (apres un changement non suivi)."""
        self._pending = None
        self._build()
        return self.current
