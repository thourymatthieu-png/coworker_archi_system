"""Placement par forces dirigees (attraction par reseau, repulsion anti-recouvrement) et
legalisation (resorption des chevauchements residuels par poussee geometrique). Opere
directement sur les Component d'un Board (mutation des positions en place) pour un
sous-ensemble de references donne ; le reste de la carte (autres composants non inclus dans
`refs`) reste fixe et sert d'obstacle pour la repulsion/legalisation si `obstacles` est passe."""
from __future__ import annotations

import math
import random
from typing import Dict, List, Optional

from . import live
from .model import ALLOWED_ROTATIONS, Board
from .partition import build_weight_matrix


def force_directed_layout(
    board: Board,
    refs: List[str],
    iterations: int = 200,
    area_hint: Optional[float] = None,
    seed: int = 0,
    try_rotations: bool = True,
) -> None:
    """Dispose `refs` par forces dirigees (style Fruchterman-Reingold adapte) : attraction
    le long des reseaux partages (poids = expansion en clique, cf. partition.build_weight_matrix),
    repulsion proportionnelle a l'encombrement reel (demi-extensions + marge) pour que le
    refroidissement separe deja grossierement les boitiers avant la legalisation stricte."""
    rng = random.Random(seed)
    movable = [r for r in refs if not board.components[r].fixed]
    if not movable:
        return
    w = build_weight_matrix(refs, board.nets)
    idx = {r: i for i, r in enumerate(refs)}

    # Rayon caracteristique : aire visee (ou somme des aires composants * 2 par defaut),
    # sert a calibrer les constantes d'attraction/repulsion comme pour FR classique.
    if area_hint is None:
        # Aire des SEULS composants places par cet appel (jamais celle de toute la carte :
        # un petit groupe ne doit pas heriter d'une echelle calculee sur les 100+ composants
        # du PCB entier, sinon le rayon de depart explose - bug constate le 2026-11-05).
        area_hint = sum(board.components[r].courtyard_w * board.components[r].courtyard_h for r in refs) * 2.5
    k = math.sqrt(max(area_hint, 1.0) / max(len(refs), 1))

    # Position initiale : cercle (eviter la degenerescence toutes-positions-egales de FR).
    for i, r in enumerate(refs):
        if r in movable:
            angle = 2 * math.pi * i / len(refs)
            jitter = rng.uniform(-0.5, 0.5)
            board.components[r].x = k * len(refs) ** 0.5 * math.cos(angle) + jitter
            board.components[r].y = k * len(refs) ** 0.5 * math.sin(angle) + jitter

    temp = k * 2.0
    cooling = temp / iterations
    gravity = 0.03  # rappel doux vers le centre : sans lui, un composant peu connecte
    # (poids d'attraction faible) derive indefiniment car la repulsion (~1/dist) decroit
    # plus lentement que l'attraction ne peut le retenir a grande distance - defaut classique
    # du placement par forces dirigees, constate le 2026-11-05 (composants pousses a des
    # dizaines de mm des ancres alors que la carte fait quelques cm).

    for it in range(iterations):
        live.tick(board)
        disp: Dict[str, List[float]] = {r: [0.0, 0.0] for r in movable}
        center_x = sum(board.components[r].x for r in refs) / len(refs)
        center_y = sum(board.components[r].y for r in refs) / len(refs)
        for r in movable:
            disp[r][0] -= gravity * (board.components[r].x - center_x)
            disp[r][1] -= gravity * (board.components[r].y - center_y)
        # Repulsion (toutes paires de refs, y compris fixes comme obstacles immobiles).
        for a_idx, ra in enumerate(refs):
            ca = board.components[ra]
            for rb in refs[a_idx + 1:]:
                cb = board.components[rb]
                dx = ca.x - cb.x
                dy = ca.y - cb.y
                dist = math.hypot(dx, dy) or 0.01
                hw_a, hh_a = ca.world_half_extents()
                hw_b, hh_b = cb.world_half_extents()
                min_sep = (hw_a + hw_b + hh_a + hh_b) / 2.0 + 0.3
                # Repulsion a PORTEE LIMITEE (coupee au-dela de quelques fois min_sep) : deux
                # composants non/peu connectes n'ont aucune raison de se repousser a grande
                # distance (un champ a decroissance en 1/dist reste non negligeable sur toute
                # la carte) - seule la gravite (vers le centre du groupe) et l'attraction par
                # reseau doivent gouverner l'espacement au-dela du contact. Defaut constate le
                # 2026-11-05 : composants pousses a des dizaines de mm sans raison avec une
                # repulsion a portee illimitee.
                if dist < min_sep * 4.0:
                    force = (k * k) / dist * max(min_sep / dist, 1.0)
                    fx, fy = dx / dist * force, dy / dist * force
                    if ra in disp:
                        disp[ra][0] += fx
                        disp[ra][1] += fy
                    if rb in disp:
                        disp[rb][0] -= fx
                        disp[rb][1] -= fy

        # Attraction (ressort le long des reseaux partages, pondere par le poids de clique).
        for a_idx, ra in enumerate(refs):
            ca = board.components[ra]
            ia = idx[ra]
            row = w[ia]
            for b_idx in range(a_idx + 1, len(refs)):
                # float(...) : sortir du type numpy.float64 des maintenant, sinon il
                # contamine ensuite Component.x/y (numpy.bool_ refuse par json.dump plus loin).
                weight = float(row[b_idx])
                if weight <= 0:
                    continue
                rb = refs[b_idx]
                cb = board.components[rb]
                dx = ca.x - cb.x
                dy = ca.y - cb.y
                dist = math.hypot(dx, dy) or 0.01
                force = weight * (dist * dist) / k
                fx, fy = dx / dist * force, dy / dist * force
                if ra in disp:
                    disp[ra][0] -= fx
                    disp[ra][1] -= fy
                if rb in disp:
                    disp[rb][0] += fx
                    disp[rb][1] += fy

        for r in movable:
            dx, dy = disp[r]
            dist = math.hypot(dx, dy) or 0.01
            capped = min(dist, temp)
            board.components[r].x = float(board.components[r].x + dx / dist * capped)
            board.components[r].y = float(board.components[r].y + dy / dist * capped)

        if try_rotations and it % 20 == 19:
            for r in movable:
                _try_best_rotation(board, r)

        temp = max(temp - cooling, 0.01)


def _local_wirelength(board: Board, ref: str) -> float:
    comp = board.components[ref]
    total = 0.0
    for pad in comp.pads:
        net = board.nets.get(pad.net)
        if net is None or len(net.pins) < 2:
            continue
        px, py = comp.pad_world_pos(pad)
        for other_ref, other_pad in net.pins:
            if other_ref == ref:
                continue
            pos = board.pad_world_pos(other_ref, other_pad)
            if pos is None:
                continue
            total += math.hypot(px - pos[0], py - pos[1])
    return total


def _try_best_rotation(board: Board, ref: str) -> None:
    comp = board.components[ref]
    if comp.fixed:
        return
    best_rot = comp.rotation
    best_cost = _local_wirelength(board, ref)
    for rot in ALLOWED_ROTATIONS:
        if rot == comp.rotation:
            continue
        comp.rotation = rot
        cost = _local_wirelength(board, ref)
        if cost < best_cost - 1e-6:
            best_cost = cost
            best_rot = rot
    comp.rotation = best_rot


def legalize(board: Board, refs: List[str], min_clearance_mm: float = 0.3, max_iters: int = 800) -> int:
    """Resorbe les chevauchements residuels en poussant chaque paire en recouvrement le long
    de l'axe de moindre penetration (algorithme de separation iteratif, cf. "legalisation +
    spread" de suggest_placement cote MCP KiCad, reimplemente ici pour tourner hors KiCad).
    Retourne le nombre d'iterations effectuees (utile pour diagnostiquer une carte trop
    dense pour converger)."""
    movable = [r for r in refs if not board.components[r].fixed]
    for it in range(max_iters):
        moved = False
        for a_idx, ra in enumerate(refs):
            ca = board.components[ra]
            ax0, ay0, ax1, ay1 = ca.world_bbox()
            for rb in refs[a_idx + 1:]:
                cb = board.components[rb]
                bx0, by0, bx1, by1 = cb.world_bbox()
                ox0, oy0 = max(ax0, bx0) - min_clearance_mm / 2.0, max(ay0, by0) - min_clearance_mm / 2.0
                ox1, oy1 = min(ax1, bx1) + min_clearance_mm / 2.0, min(ay1, by1) + min_clearance_mm / 2.0
                overlap_x = ox1 - ox0
                overlap_y = oy1 - oy0
                if overlap_x <= 0 or overlap_y <= 0:
                    continue
                moved = True
                a_can_move = ra in movable
                b_can_move = rb in movable
                if not a_can_move and not b_can_move:
                    continue
                if overlap_x < overlap_y:
                    push = overlap_x / 2.0 + 0.01
                    direction = 1.0 if ca.x <= cb.x else -1.0
                    if a_can_move and b_can_move:
                        ca.x -= direction * push
                        cb.x += direction * push
                    elif a_can_move:
                        ca.x -= direction * 2 * push
                    else:
                        cb.x += direction * 2 * push
                else:
                    push = overlap_y / 2.0 + 0.01
                    direction = 1.0 if ca.y <= cb.y else -1.0
                    if a_can_move and b_can_move:
                        ca.y -= direction * push
                        cb.y += direction * push
                    elif a_can_move:
                        ca.y -= direction * 2 * push
                    else:
                        cb.y += direction * 2 * push
        if not moved:
            return it
    return max_iters
