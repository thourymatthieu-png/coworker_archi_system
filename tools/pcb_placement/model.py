"""Modele de donnees interne du moteur de placement (independant de KiCad)."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# Rotations supportees : multiples de 90 degres seulement. Simplification volontaire : les
# rectangles d'encombrement (courtyard) restent alors toujours alignes aux axes (on echange
# juste largeur/hauteur a 90/270), ce qui rend les tests de recouvrement triviaux et rapides.
# Une rotation quelconque degraderait la detection de collision (SAT necessaire) pour un gain
# de compacite marginal sur une carte a composants majoritairement rectangulaires/CMS.
ALLOWED_ROTATIONS: Tuple[int, ...] = (0, 90, 180, 270)


@dataclass
class Pad:
    name: str
    net: str
    local_x: float  # mm, repere local non tourne du footprint
    local_y: float


@dataclass
class Component:
    ref: str
    value: str
    block: str
    is_anchor: bool
    courtyard_w: float  # mm, repere local (rotation 0)
    courtyard_h: float
    courtyard_offset_x: float  # offset du centre du rectangle / centre du footprint
    courtyard_offset_y: float
    pads: List[Pad]
    # Etat de placement courant (mm, degres) ; (0, 0) / 0 par defaut, a initialiser.
    x: float = 0.0
    y: float = 0.0
    rotation: int = 0
    fixed: bool = False  # ancre mecanique dure : jamais deplace/tourne par le moteur

    def world_half_extents(self) -> Tuple[float, float]:
        """Demi-largeur/demi-hauteur du rectangle d'encombrement en orientation courante."""
        w, h = self.courtyard_w, self.courtyard_h
        if self.rotation in (90, 270):
            w, h = h, w
        return w / 2.0, h / 2.0

    def world_center(self) -> Tuple[float, float]:
        """Centre reel du rectangle d'encombrement (le centre du footprint n'est pas toujours
        le centre du courtyard, cf. courtyard_offset_*)."""
        ox, oy = self.courtyard_offset_x, self.courtyard_offset_y
        if self.rotation == 90:
            ox, oy = -oy, ox
        elif self.rotation == 180:
            ox, oy = -ox, -oy
        elif self.rotation == 270:
            ox, oy = oy, -ox
        return self.x + ox, self.y + oy

    def world_bbox(self) -> Tuple[float, float, float, float]:
        """(xmin, ymin, xmax, ymax) du rectangle d'encombrement en coordonnees carte."""
        cx, cy = self.world_center()
        hw, hh = self.world_half_extents()
        return cx - hw, cy - hh, cx + hw, cy + hh

    def pad_world_pos(self, pad: Pad) -> Tuple[float, float]:
        a = math.radians(self.rotation)
        cos_a, sin_a = math.cos(a), math.sin(a)
        lx, ly = pad.local_x, pad.local_y
        wx = lx * cos_a - ly * sin_a
        wy = lx * sin_a + ly * cos_a
        return self.x + wx, self.y + wy


@dataclass
class Net:
    name: str
    # liste de (ref, pad) - la position se recalcule via Board.pad_positions
    pins: List[Tuple[str, str]] = field(default_factory=list)

    @property
    def degree(self) -> int:
        return len(self.pins)


@dataclass
class Board:
    components: Dict[str, Component]
    nets: Dict[str, Net]
    source_pcb: str = ""
    outline_w: float = 0.0
    outline_h: float = 0.0

    def pad_world_pos(self, ref: str, pad_name: str) -> Optional[Tuple[float, float]]:
        comp = self.components.get(ref)
        if comp is None:
            return None
        for p in comp.pads:
            if p.name == pad_name:
                return comp.pad_world_pos(p)
        return None

    def movable_refs(self) -> List[str]:
        return [r for r, c in self.components.items() if not c.fixed]

    def refs_in_block(self, block: str) -> List[str]:
        return [r for r, c in self.components.items() if c.block == block]

    def blocks(self) -> List[str]:
        seen = []
        for c in self.components.values():
            if c.block not in seen:
                seen.append(c.block)
        return seen

    def clone_positions(self) -> Dict[str, Tuple[float, float, int]]:
        return {r: (c.x, c.y, c.rotation) for r, c in self.components.items()}

    def restore_positions(self, snapshot: Dict[str, Tuple[float, float, int]]) -> None:
        for r, (x, y, rot) in snapshot.items():
            c = self.components[r]
            c.x, c.y, c.rotation = x, y, rot

    def global_bbox(self, refs: Optional[List[str]] = None) -> Tuple[float, float, float, float]:
        refs = refs if refs is not None else list(self.components.keys())
        xs_min, ys_min, xs_max, ys_max = [], [], [], []
        for r in refs:
            x0, y0, x1, y1 = self.components[r].world_bbox()
            xs_min.append(x0)
            ys_min.append(y0)
            xs_max.append(x1)
            ys_max.append(y1)
        if not refs:
            return (0.0, 0.0, 0.0, 0.0)
        return (min(xs_min), min(ys_min), max(xs_max), max(ys_max))
