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
    # int pour un composant mobile (grille ALLOWED_ROTATIONS) ; peut etre un angle quelconque
    # (float) pour une ancre FIXE, jamais touchee par le moteur (cf. io_data.load_board).
    rotation: float = 0
    fixed: bool = False  # ancre mecanique dure : jamais deplace/tourne par le moteur

    def _local_corners(self) -> Tuple[Tuple[float, float], ...]:
        ox, oy = self.courtyard_offset_x, self.courtyard_offset_y
        hw, hh = self.courtyard_w / 2.0, self.courtyard_h / 2.0
        return ((ox - hw, oy - hh), (ox + hw, oy - hh), (ox + hw, oy + hh), (ox - hw, oy + hh))

    def world_bbox(self) -> Tuple[float, float, float, float]:
        """(xmin, ymin, xmax, ymax) du rectangle d'encombrement en coordonnees carte.

        Calcule par rotation exacte des 4 coins locaux : couvre aussi bien les rotations
        multiples de 90 (le cas courant, ou le resultat est exact) que les rotations
        quelconques d'une ancre fixe (ex. moteurs a 45 degres sur Boomrone, orientes en
        diagonale vers les bras du chassis) - dans ce dernier cas la boite retournee est la
        boite ENGLOBANTE (conservative) du rectangle tourne, pas le rectangle tourne
        lui-meme (cf. limite documentee : la detection de recouvrement reste un test de
        boites alignees aux axes, cf. ALLOWED_ROTATIONS)."""
        a = math.radians(self.rotation)
        cos_a, sin_a = math.cos(a), math.sin(a)
        xs, ys = [], []
        for lx, ly in self._local_corners():
            xs.append(self.x + lx * cos_a - ly * sin_a)
            ys.append(self.y + lx * sin_a + ly * cos_a)
        return min(xs), min(ys), max(xs), max(ys)

    def world_center(self) -> Tuple[float, float]:
        """Centre du rectangle d'encombrement (le centre du footprint n'est pas toujours le
        centre du courtyard, cf. courtyard_offset_*) ; pour une rotation non multiple de 90,
        c'est le centre de la boite ENGLOBANTE (cf. world_bbox)."""
        x0, y0, x1, y1 = self.world_bbox()
        return (x0 + x1) / 2.0, (y0 + y1) / 2.0

    def world_half_extents(self) -> Tuple[float, float]:
        """Demi-largeur/demi-hauteur de la boite ENGLOBANTE (cf. world_bbox)."""
        x0, y0, x1, y1 = self.world_bbox()
        return (x1 - x0) / 2.0, (y1 - y0) / 2.0

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
    outline_w: float = 0.0  # dimensions de la boite englobante au moment de l'extraction (info, pas une contrainte)
    outline_h: float = 0.0
    # Contour de carte FIXE (xmin, ymin, xmax, ymax, mm) impose par la mecanique (chassis,
    # bras moteur...) - a la difference de outline_w/h ci-dessus, c'est une contrainte dure :
    # tout composant hors de ce rectangle (et pas dans overhang_refs) penalise le cout comme
    # un recouvrement (cf. cost.out_of_bounds_penalty). None = pas de contour impose, le
    # moteur est alors libre de choisir la taille de la carte (comportement d'origine).
    outline: Optional[Tuple[float, float, float, float]] = None
    # References autorisees a deborder du contour (ex. connecteur batterie, antenne radio) -
    # exemptees de la contrainte ci-dessus. Prevu pour des ancres FIXES dont le debord est une
    # decision mecanique deja prise (cf. tools/pcb_placement/README.md) ; le moteur ne decide
    # jamais lui-meme qu'un composant peut deborder.
    overhang_refs: frozenset = frozenset()
    # Regles de decouplage (cf. io_data.apply_decoupling) : liste de dicts
    # {"cap": ref, "ic": ref, "pins": [numeros de broche], "dmax": mm}. Vide = pas de regle.
    decoupling_rules: list = field(default_factory=list)

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
