"""Passe de compactage deterministe (bottom-left-fill), appliquee APRES le recuit simule
pour GARANTIR 0 chevauchement et 0 hors-contour par construction, plutot que de compter sur
le recuit + la legalisation (qui ne font que pousser localement et peuvent laisser des
chevauchements residuels ou de grands vides, cf. retour utilisateur du 2026-11-05).

Principe repris de l'essai precedent `kicad_tetris_placement.py` (script d'essai du projet Boomrone) (tasseur generique a
points d'ancrage = coins des rectangles deja places) : ici integre au modele Board/Component
du moteur (pas un script a part sur un JSON), et tient compte du contour de carte fixe
(Board.outline) en plus des ancres fixes."""
from __future__ import annotations

import random

import numpy as np
from typing import Dict, List, Optional, Tuple

from . import live
from .model import Board


class _Packer:
    """Empile des rectangles (boites englobantes de composants) sans chevauchement ni sortie
    du contour, en minimisant la boite englobante totale a chaque etape. `fixed` = rectangles
    deja occupes (ancres mecaniques), jamais deplaces."""

    def __init__(self, margin: float, rng: random.Random,
                 outline: Optional[Tuple[float, float, float, float]], fixed: List[dict]):
        self.margin = margin
        self.rng = rng
        self.outline = outline
        self.placed: List[dict] = list(fixed)
        self._refresh_candidates()

    def _refresh_candidates(self) -> None:
        x0 = self.outline[0] if self.outline else min((r["x0"] for r in self.placed), default=0.0)
        y0 = self.outline[1] if self.outline else min((r["y0"] for r in self.placed), default=0.0)
        xs = {x0}
        ys = {y0}
        for r in self.placed:
            xs.add(r["x0"]); xs.add(r["x1"])
            ys.add(r["y0"]); ys.add(r["y1"])
        self.candidates = sorted((x, y) for x in xs for y in ys)

    def _overlaps(self, x0: float, y0: float, x1: float, y1: float) -> bool:
        m = self.margin
        for r in self.placed:
            if x0 < r["x1"] + m and x1 + m > r["x0"] and y0 < r["y1"] + m and y1 + m > r["y0"]:
                return True
        return False

    def _out_of_bounds(self, x0: float, y0: float, x1: float, y1: float) -> bool:
        if self.outline is None:
            return False
        ox0, oy0, ox1, oy1 = self.outline
        return x0 < ox0 - 1e-6 or y0 < oy0 - 1e-6 or x1 > ox1 + 1e-6 or y1 > oy1 + 1e-6

    def _bbox_area_with(self, x0: float, y0: float, x1: float, y1: float) -> float:
        xs = [x0, x1] + [r["x0"] for r in self.placed] + [r["x1"] for r in self.placed]
        ys = [y0, y1] + [r["y0"] for r in self.placed] + [r["y1"] for r in self.placed]
        return (max(xs) - min(xs)) * (max(ys) - min(ys))

    def _scan_free_spot(self, w: float, h: float, near: Optional[Tuple[float, float]],
                        step: float = 0.2) -> Optional[Tuple[float, float]]:
        """Balayage fin du contour (pas `step` mm, vectorise) : position LIBRE la plus proche
        de `near` (centre actuel du composant), pour garder le regroupement obtenu par le
        recuit (condensateurs de decouplage pres de leur circuit, blocs groupes). Sans contour
        impose, pas de balayage (zone illimitee : les candidats suffisent)."""
        if self.outline is None:
            return None
        ox0, oy0, ox1, oy1 = self.outline
        if w > ox1 - ox0 + 1e-6 or h > oy1 - oy0 + 1e-6:
            return None
        xs = np.arange(ox0, ox1 - w + 1e-6, step)
        ys = np.arange(oy0, oy1 - h + 1e-6, step)
        if len(xs) == 0 or len(ys) == 0:
            xs, ys = np.array([ox0]), np.array([oy0])
        X, Y = np.meshgrid(xs, ys)
        free = np.ones(X.shape, dtype=bool)
        m = self.margin
        for r in self.placed:
            free &= ~((X < r["x1"] + m) & (X + w + m > r["x0"]) & (Y < r["y1"] + m) & (Y + h + m > r["y0"]))
        if not free.any():
            return None
        if near is None:
            idx = int(np.argmax(free))
        else:
            d = np.where(free, (X + w / 2 - near[0]) ** 2 + (Y + h / 2 - near[1]) ** 2, np.inf)
            idx = int(np.argmin(d))
        return float(X.flat[idx]), float(Y.flat[idx])

    def place(self, item_id: str, w: float, h: float, top_k: int = 3,
              near: Optional[Tuple[float, float]] = None) -> Optional[Tuple[float, float]]:
        options = []
        for cx, cy in self.candidates:
            x0, y0, x1, y1 = cx, cy, cx + w, cy + h
            if self._overlaps(x0, y0, x1, y1) or self._out_of_bounds(x0, y0, x1, y1):
                continue
            options.append((self._bbox_area_with(x0, y0, x1, y1), x0, y0))
        if not options:
            spot = self._scan_free_spot(w, h, near)
            if spot is None:
                return None
            x0, y0 = spot
            self.placed.append({"id": item_id, "x0": x0, "y0": y0, "x1": x0 + w, "y1": y0 + h})
            self._refresh_candidates()
            return x0, y0
        options.sort(key=lambda o: o[0])
        _, x0, y0 = self.rng.choice(options[:max(1, top_k)])
        self.placed.append({"id": item_id, "x0": x0, "y0": y0, "x1": x0 + w, "y1": y0 + h})
        self._refresh_candidates()
        return x0, y0


def default_compaction_order(board: Board, refs: List[str]) -> List[str]:
    """Ordre de pose par defaut : regroupe par bloc fonctionnel (prefere au placement
    `refs` brut pour garder le regroupement obtenu par le recuit simule), et a l'interieur
    d'un bloc pose d'abord les composants les plus connectes (nombre de pastilles, comme
    "hub" dans l'ancien essai tetris) - un ordre arbitraire donnerait un tassement tout aussi
    valide (0 chevauchement garanti dans tous les cas) mais moins fidele au regroupement
    fonctionnel du recuit."""
    def degree(ref: str) -> int:
        return len(board.components[ref].pads)

    by_block: Dict[str, List[str]] = {}
    for r in refs:
        by_block.setdefault(board.components[r].block, []).append(r)
    order: List[str] = []
    for block in by_block:
        order.extend(sorted(by_block[block], key=degree, reverse=True))
    return order


def compact(board: Board, refs: List[str], margin_mm: float = 0.3, seed: int = 0,
            order: Optional[List[str]] = None) -> List[str]:
    """Remise en etat faisable (0 recouvrement, 0 hors-contour), en gardant au mieux ce que le
    recuit a obtenu (blocs groupes, condensateurs de decouplage pres de leur circuit) :
    1. `spread_resolve` : RELAXATION LOCALE - les composants qui se recouvrent ou depassent du
       contour sont ecartes, et leurs voisins s'ecartent un peu pour leur faire de la place ;
    2. repli `compact_minimal` : les rares restants vont a la place libre la plus proche ;
    3. repli `_compact_repack` : repavage complet."""
    if order is None:
        if spread_resolve(board, refs, margin_mm=margin_mm, seed=seed):
            return []
        if board.outline is not None and not compact_minimal(board, refs, margin_mm=margin_mm, seed=seed):
            return []
    return _compact_repack(board, refs, margin_mm=margin_mm, seed=seed, order=order)


def spread_resolve(board: Board, refs: List[str], margin_mm: float = 0.3, seed: int = 0,
                   max_iters: int = 4000, max_step_mm: float = 1.5) -> bool:
    """Relaxation locale : a chaque iteration, pour chaque paire de boites qui se recouvrent
    (marge comprise), on les ecarte selon l'axe de plus faible penetration ; le deplacement est
    PARTAGE entre les deux composants, au prorata de leur mobilite (les petits composants
    cedent plus que les gros ; une piece verrouillee ne bouge pas). Les composants depassant du
    contour sont ramenes a l'interieur et poussent leurs voisins a leur tour : la poussee se
    propage de proche en proche, chaque composant reste proche de sa place d'origine.
    Translation seulement. Renvoie True si l'etat final est sans recouvrement ni hors-contour."""
    rng = np.random.default_rng(seed)
    names = list(refs)
    n = len(names)
    if n == 0:
        return True
    comps = [board.components[r] for r in names]
    fixed = np.array([c.fixed for c in comps])
    exempt = np.array([c.fixed or (r in board.overhang_refs) for c, r in zip(comps, names)])
    area = np.array([max((lambda b: (b[2] - b[0]) * (b[3] - b[1]))(c.world_bbox()), 0.01) for c in comps])
    mob = np.where(fixed, 0.0, 1.0 / (np.sqrt(area) + 1.0))
    iu, ju = np.triu_indices(n, k=1)
    keep = ~(fixed[iu] & fixed[ju])          # deux pieces verrouillees : rien a faire
    iu, ju = iu[keep], ju[keep]
    m = margin_mm / 2.0
    outline = board.outline

    def boxes() -> np.ndarray:
        return np.array([c.world_bbox() for c in comps], dtype=float)

    ok = False
    for it in range(max_iters):
        B = boxes()
        ox = np.minimum(B[iu, 2], B[ju, 2]) - np.maximum(B[iu, 0], B[ju, 0]) + 2 * m
        oy = np.minimum(B[iu, 3], B[ju, 3]) - np.maximum(B[iu, 1], B[ju, 1]) + 2 * m
        hit = (ox > 1e-6) & (oy > 1e-6)
        disp = np.zeros((n, 2))
        if hit.any():
            I, J, X, Y = iu[hit], ju[hit], ox[hit], oy[hit]
            use_x = X <= Y
            pen = np.where(use_x, X, Y) + 1e-3
            cx = (B[:, 0] + B[:, 2]) / 2.0
            cy = (B[:, 1] + B[:, 3]) / 2.0
            d = np.where(use_x, cx[I] - cx[J], cy[I] - cy[J])
            sgn = np.where(d > 0, 1.0, -1.0)
            ties = np.abs(d) < 1e-9
            if ties.any():
                sgn[ties] = rng.choice([-1.0, 1.0], size=int(ties.sum()))
            wi, wj = mob[I], mob[J]
            tot = wi + wj
            fi = np.where(tot > 0, wi / np.where(tot > 0, tot, 1.0), 0.0)
            fj = np.where(tot > 0, wj / np.where(tot > 0, tot, 1.0), 0.0)
            axis = np.where(use_x, 0, 1)
            np.add.at(disp, (I, axis), sgn * pen * fi)
            np.add.at(disp, (J, axis), -sgn * pen * fj)
            disp *= 0.8                                   # amortissement (evite les oscillations)
            np.clip(disp, -max_step_mm, max_step_mm, out=disp)
        # contour : ramener a l'interieur (sauf pieces verrouillees et debords decides)
        if outline is not None:
            ox0, oy0, ox1, oy1 = outline
            nb = B + np.concatenate([disp, disp], axis=1)
            dxw = np.maximum(ox0 - nb[:, 0], 0.0) - np.maximum(nb[:, 2] - ox1, 0.0)
            dyw = np.maximum(oy0 - nb[:, 1], 0.0) - np.maximum(nb[:, 3] - oy1, 0.0)
            wall = np.stack([dxw, dyw], axis=1)
            wall[exempt] = 0.0
            disp = disp + wall
            outside = (np.abs(wall) > 1e-9).any()
        else:
            outside = False
        if not hit.any() and not outside:
            ok = True
            break
        for k in range(n):
            if not fixed[k] and (disp[k, 0] != 0.0 or disp[k, 1] != 0.0):
                comps[k].x += float(disp[k, 0])
                comps[k].y += float(disp[k, 1])
        if it % 20 == 0:
            live.tick(board)
    return ok


def compact_minimal(board: Board, refs: List[str], margin_mm: float = 0.3, seed: int = 0) -> List[str]:
    """Garde en place chaque composant mobile valide (dans le contour, sans recouvrement avec
    ceux deja retenus : on retient d'abord les plus gros), puis deplace les autres, du plus
    gros au plus petit, vers la position libre la plus proche de leur position actuelle.
    Translation seulement. Retourne les references sans place (a repaver)."""
    rng = random.Random(seed)
    fixed_rects = []
    for r, c in board.components.items():
        if c.fixed:
            x0, y0, x1, y1 = c.world_bbox()
            fixed_rects.append({"id": r, "x0": x0, "y0": y0, "x1": x1, "y1": y1})
    packer = _Packer(margin=margin_mm, rng=rng, outline=board.outline, fixed=fixed_rects)

    def area(ref: str) -> float:
        hw, hh = board.components[ref].world_half_extents()
        return hw * hh

    mobile = sorted((r for r in refs if not board.components[r].fixed), key=area, reverse=True)
    conflict: List[str] = []
    for r in mobile:
        x0, y0, x1, y1 = board.components[r].world_bbox()
        if packer._overlaps(x0, y0, x1, y1) or packer._out_of_bounds(x0, y0, x1, y1):
            conflict.append(r)
        else:
            packer.placed.append({"id": r, "x0": x0, "y0": y0, "x1": x1, "y1": y1})

    unplaced: List[str] = []
    for r in conflict:
        comp = board.components[r]
        bx0, by0, bx1, by1 = comp.world_bbox()
        w, h = bx1 - bx0, by1 - by0
        cx, cy = (bx0 + bx1) / 2.0, (by0 + by1) / 2.0
        spot = packer._scan_free_spot(w, h, (cx, cy))
        if spot is None:
            unplaced.append(r)
            continue
        packer.placed.append({"id": r, "x0": spot[0], "y0": spot[1], "x1": spot[0] + w, "y1": spot[1] + h})
        comp.x += (spot[0] + w / 2.0) - cx
        comp.y += (spot[1] + h / 2.0) - cy
        live.tick(board)
    return unplaced


def _compact_repack(board: Board, refs: List[str], margin_mm: float = 0.3, seed: int = 0,
                    order: Optional[List[str]] = None) -> List[str]:
    """Replace chaque composant MOBILE de `refs` par tassement compact deterministe autour
    des ancres fixes et les uns des autres, en respectant `board.outline` si impose. Les
    composants fixes ne bougent pas (ils servent d'obstacles, comme pour la legalisation).
    Modifie `board` en place (translation seulement, aucune rotation changee). Retourne la
    liste des references qui n'ont trouve aucune place (carte trop petite/dense pour y faire
    tenir tout le monde avec cette config) - a SIGNALER explicitement, jamais a passer sous
    silence (cf. consigne du projet : pas de trou comble par une supposition silencieuse)."""
    rng = random.Random(seed)
    fixed_rects = []
    for r, c in board.components.items():
        if c.fixed:
            x0, y0, x1, y1 = c.world_bbox()
            fixed_rects.append({"id": r, "x0": x0, "y0": y0, "x1": x1, "y1": y1})

    packer = _Packer(margin=margin_mm, rng=rng, outline=board.outline, fixed=fixed_rects)
    sequence = order if order is not None else default_compaction_order(board, refs)

    unplaced: List[str] = []
    for r in sequence:
        comp = board.components[r]
        if comp.fixed:
            continue
        hw, hh = comp.world_half_extents()
        w, h = hw * 2.0, hh * 2.0
        bx0, by0, bx1, by1 = comp.world_bbox()
        old_cx, old_cy = (bx0 + bx1) / 2.0, (by0 + by1) / 2.0
        result = packer.place(r, w, h, near=(old_cx, old_cy))
        if result is None:
            unplaced.append(r)
            continue
        x0, y0 = result
        dx, dy = (x0 + w / 2.0) - old_cx, (y0 + h / 2.0) - old_cy
        comp.x += dx
        comp.y += dy
        live.tick(board)
    if unplaced and order is None:
        # Dernier recours : tout reposer en commencant par les plus gros composants (les
        # gros sont les plus difficiles a caser une fois la carte remplie).
        def area(ref: str) -> float:
            hw, hh = board.components[ref].world_half_extents()
            return hw * hh
        biggest_first = sorted(refs, key=area, reverse=True)
        return _compact_repack(board, refs, margin_mm=margin_mm, seed=seed, order=biggest_first)
    return unplaced
