"""Passe de compactage deterministe (bottom-left-fill), appliquee APRES le recuit simule
pour GARANTIR 0 chevauchement et 0 hors-contour par construction, plutot que de compter sur
le recuit + la legalisation (qui ne font que pousser localement et peuvent laisser des
chevauchements residuels ou de grands vides, cf. retour utilisateur du 2026-11-05).

Principe repris de l'essai precedent `tools/kicad_tetris_placement.py` (tasseur generique a
points d'ancrage = coins des rectangles deja places) : ici integre au modele Board/Component
du moteur (pas un script a part sur un JSON), et tient compte du contour de carte fixe
(Board.outline) en plus des ancres fixes."""
from __future__ import annotations

import random
from typing import Dict, List, Optional, Tuple

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

    def place(self, item_id: str, w: float, h: float, top_k: int = 3) -> Optional[Tuple[float, float]]:
        options = []
        for cx, cy in self.candidates:
            x0, y0, x1, y1 = cx, cy, cx + w, cy + h
            if self._overlaps(x0, y0, x1, y1) or self._out_of_bounds(x0, y0, x1, y1):
                continue
            options.append((self._bbox_area_with(x0, y0, x1, y1), x0, y0))
        if not options:
            return None
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
        result = packer.place(r, w, h)
        if result is None:
            unplaced.append(r)
            continue
        x0, y0 = result
        bx0, by0, bx1, by1 = comp.world_bbox()
        old_cx, old_cy = (bx0 + bx1) / 2.0, (by0 + by1) / 2.0
        dx, dy = (x0 + w / 2.0) - old_cx, (y0 + h / 2.0) - old_cy
        comp.x += dx
        comp.y += dy
    return unplaced
