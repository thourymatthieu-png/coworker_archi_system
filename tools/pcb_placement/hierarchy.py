"""Optimisation hierarchique en 5 niveaux (cf. mission) :
1. composants individuels (geres par placement.force_directed_layout + annealing a chaque niveau)
2. petits groupes a l'interieur d'un bloc (partition.partition_refs)
3. bloc fonctionnel entier (assemblage rigide des groupes puis recuit fin du bloc)
4. assemblage des blocs entre eux (chaque bloc traite comme un noeud macro, peut etre
   reoriente/reordonne)
5. optimisation globale : recuit sur TOUTE la carte, avec un type de mouvement
   supplementaire qui deplace/tourne un bloc entier en bloc rigide (un bloc n'est donc
   jamais definitivement figer apres son placement local, conformement a la mission).
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np

from .annealing import AnnealingConfig, relevant_nets, run_annealing
from .cost import CostBreakdown, CostWeights, is_better, total_cost
from .model import ALLOWED_ROTATIONS, Board
from .partition import build_weight_matrix, partition_refs
from .placement import force_directed_layout, legalize


@dataclass
class HierarchyConfig:
    max_group_size: int = 10
    fd_iterations_group: int = 250
    fd_iterations_assembly: int = 120
    sa_group: AnnealingConfig = field(default_factory=lambda: AnnealingConfig(iterations=1500, t0=8.0))
    sa_block: AnnealingConfig = field(default_factory=lambda: AnnealingConfig(iterations=2500, t0=10.0))
    sa_global: AnnealingConfig = field(default_factory=lambda: AnnealingConfig(iterations=4000, t0=6.0))
    block_move_prob: float = 0.15
    rotation_probe_every: int = 15
    seed: int = 0


def _group_centroid(board: Board, refs: List[str]) -> tuple:
    xs = [board.components[r].x for r in refs]
    ys = [board.components[r].y for r in refs]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def rigid_transform(board: Board, refs: List[str], dx: float, dy: float, rotate_deg: int, pivot: tuple) -> None:
    """Deplace et/ou tourne `refs` en bloc rigide autour de `pivot` (translation `dx,dy`
    appliquee APRES rotation). N'affecte pas les composants fixes (ancres) : s'ils sont dans
    `refs` ils sont ignores (une ancre ne doit jamais etre deplacee par le moteur)."""
    rotate_deg = rotate_deg % 360
    a = math.radians(rotate_deg)
    cos_a, sin_a = math.cos(a), math.sin(a)
    px, py = pivot
    for r in refs:
        comp = board.components[r]
        if comp.fixed:
            continue
        rx, ry = comp.x - px, comp.y - py
        nx = rx * cos_a - ry * sin_a
        ny = rx * sin_a + ry * cos_a
        comp.x = px + nx + dx
        comp.y = py + ny + dy
        if rotate_deg:
            comp.rotation = (comp.rotation + rotate_deg) % 360


def optimize_group(board: Board, refs: List[str], weights: CostWeights, cfg: HierarchyConfig, seed: int) -> CostBreakdown:
    """Niveau 1+2 : place et polit un petit groupe de composants fortement connectes."""
    force_directed_layout(board, refs, iterations=cfg.fd_iterations_group, seed=seed)
    legalize(board, refs, min_clearance_mm=weights.min_clearance_mm)
    sa_cfg = AnnealingConfig(**{**cfg.sa_group.__dict__, "seed": seed})
    cost = run_annealing(board, refs, weights, sa_cfg)
    legalize(board, refs, min_clearance_mm=weights.min_clearance_mm)
    return cost


def assemble_rigid_groups(board: Board, groups: List[List[str]], weights: CostWeights, cfg: HierarchyConfig, seed: int) -> None:
    """Niveau 3 (partie assemblage) : dispose plusieurs groupes DEJA optimises en interne les
    uns par rapport aux autres, par forces dirigees sur des noeuds macro (un noeud = un
    groupe), puis translation/rotation RIGIDE du contenu reel du groupe - le placement
    interne obtenu au niveau 2 n'est jamais deforme ici, seulement deplace en bloc."""
    if len(groups) <= 1:
        return
    rng = random.Random(seed)
    # Poids inter-groupes = somme des poids (expansion en clique) entre membres de deux
    # groupes differents - reutilise le meme graphe que le partitionnement.
    all_refs = [r for g in groups for r in g]
    w_full = build_weight_matrix(all_refs, board.nets)
    idx = {r: i for i, r in enumerate(all_refs)}
    n = len(groups)
    macro_w = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            idx_i = [idx[r] for r in groups[i]]
            idx_j = [idx[r] for r in groups[j]]
            macro_w[i, j] = macro_w[j, i] = float(w_full[np.ix_(idx_i, idx_j)].sum())

    half_extents = []
    for g in groups:
        x0, y0, x1, y1 = board.global_bbox(g)
        half_extents.append(((x1 - x0) / 2.0, (y1 - y0) / 2.0))
    centroids = [list(_group_centroid(board, g)) for g in groups]
    # Un groupe qui contient au moins une ancre mecanique dure (composant "fixed") ne peut
    # pas etre deplace en rigide : rigid_transform ignore deja les composants fixes en son
    # sein, donc le "deplacer en bloc" ne deplacerait QUE les membres libres et romprait la
    # rigidite silencieusement - sur plusieurs dizaines d'iterations, le suivi du centroide
    # (qui suppose tout le groupe deplace) derive alors sans jamais revenir, et les membres
    # libres finissent a des dizaines de mm de l'ancre (constate le 2026-11-05 sur
    # DES-012-module-bluetooth : U7 fixe, TP7-10/C36/C37 pousses a plus de 100 mm). Un tel
    # groupe reste donc immobile a ce niveau : ses membres libres restent ceux deja places
    # pres de l'ancre par le recuit fin de niveau 2/3 (qui, lui, respecte correctement
    # `fixed` composant par composant).
    group_is_anchored = [any(board.components[r].fixed for r in g) for g in groups]

    k = max((sum(h[0] + h[1] for h in half_extents) / n) * 2.0, 5.0)
    temp = k * 2.0
    cooling = temp / cfg.fd_iterations_assembly
    gravity = 0.03  # meme raison que placement.force_directed_layout : sans rappel vers le
    # centre, un groupe/bloc faiblement connecte aux autres derive indefiniment.

    for it in range(cfg.fd_iterations_assembly):
        disp = [[0.0, 0.0] for _ in range(n)]
        overall_cx = sum(c[0] for c in centroids) / n
        overall_cy = sum(c[1] for c in centroids) / n
        for i in range(n):
            disp[i][0] -= gravity * (centroids[i][0] - overall_cx)
            disp[i][1] -= gravity * (centroids[i][1] - overall_cy)
        for i in range(n):
            for j in range(i + 1, n):
                dx = centroids[i][0] - centroids[j][0]
                dy = centroids[i][1] - centroids[j][1]
                dist = math.hypot(dx, dy) or 0.01
                min_sep = half_extents[i][0] + half_extents[j][0] + half_extents[i][1] + half_extents[j][1]
                # Meme correction qu'en placement.force_directed_layout : repulsion coupee
                # au-dela de quelques fois min_sep, sinon deux blocs non connectes s'eloignent
                # indefiniment au lieu de se stabiliser sous l'effet de la gravite.
                if dist < min_sep * 4.0:
                    force = (k * k) / dist * max(min_sep / dist, 1.0)
                    fx, fy = dx / dist * force, dy / dist * force
                    disp[i][0] += fx
                    disp[i][1] += fy
                    disp[j][0] -= fx
                    disp[j][1] -= fy
                weight = float(macro_w[i, j])
                if weight > 0:
                    att = weight * (dist * dist) / k
                    afx, afy = dx / dist * att, dy / dist * att
                    disp[i][0] -= afx
                    disp[i][1] -= afy
                    disp[j][0] += afx
                    disp[j][1] += afy
        for i in range(n):
            if group_is_anchored[i]:
                continue  # immobile (cf. commentaire plus haut) ; exerce quand meme une force sur les autres ci-dessus
            dx, dy = disp[i]
            dist = math.hypot(dx, dy) or 0.01
            capped = min(dist, temp)
            step_x, step_y = dx / dist * capped, dy / dist * capped
            rigid_transform(board, groups[i], step_x, step_y, 0, tuple(centroids[i]))
            centroids[i][0] += step_x
            centroids[i][1] += step_y
        temp = max(temp - cooling, 0.01)

    # Essai d'orientation globale de chaque groupe (0/90/180/270) : garde celle qui minimise
    # le cout de cablage inter-groupes (le groupe garde sa structure interne, seul l'angle
    # d'ensemble et sa position changent) - c'est ce qui permet a un bloc d'etre "retourne"
    # plutot que figer apres son optimisation locale (exigence de la mission).
    for i, g in enumerate(groups):
        if group_is_anchored[i]:
            continue  # memes raisons : une rotation rigide deplacerait aussi les membres libres loin de l'ancre fixe
        pivot = tuple(centroids[i])
        relevant = relevant_nets(board, g)
        best_rot, best_cost = 0, _inter_group_wirelength(board, g, relevant)
        for rot in (90, 180, 270):
            rigid_transform(board, g, 0.0, 0.0, 90, pivot)
            cost = _inter_group_wirelength(board, g, relevant)
            cumulative_rot = (rot) % 360
            if cost < best_cost - 1e-6:
                best_cost = cost
                best_rot = cumulative_rot
        # best_rot est l'angle cumule depuis l'etat initial (0 si rien de mieux trouve) :
        # revenir a 0 (on a fini a +270 apres les 3 essais) puis appliquer best_rot.
        rigid_transform(board, g, 0.0, 0.0, 90, pivot)  # +360 degre -> retour a l'etat initial
        if best_rot:
            rigid_transform(board, g, 0.0, 0.0, best_rot, pivot)


def _inter_group_wirelength(board: Board, refs: List[str], nets) -> float:
    from .cost import hpwl
    return hpwl(board, nets)


def optimize_block(board: Board, block: str, weights: CostWeights, cfg: HierarchyConfig, seed: int) -> CostBreakdown:
    """Niveau 2+3 complet pour un bloc fonctionnel : partitionnement en petits groupes,
    optimisation interne de chaque groupe, assemblage rigide, puis recuit fin libre sur tout
    le bloc (les composants peuvent de nouveau bouger individuellement pour polir les
    jonctions entre groupes)."""
    refs = board.refs_in_block(block)
    groups = partition_refs(refs, board.nets, cfg.max_group_size)
    for gi, g in enumerate(groups):
        optimize_group(board, g, weights, cfg, seed=seed * 1000 + gi)
    assemble_rigid_groups(board, groups, weights, cfg, seed=seed)
    legalize(board, refs, min_clearance_mm=weights.min_clearance_mm)
    sa_cfg = AnnealingConfig(**{**cfg.sa_block.__dict__, "seed": seed})
    cost = run_annealing(board, refs, weights, sa_cfg)
    legalize(board, refs, min_clearance_mm=weights.min_clearance_mm)
    return cost


def run_global_annealing_with_block_moves(
    board: Board,
    blocks_map: Dict[str, List[str]],
    weights: CostWeights,
    cfg: HierarchyConfig,
) -> CostBreakdown:
    """Niveau 5 : recuit sur l'ensemble de la carte avec, en plus des mouvements habituels
    (translation/rotation/echange d'UN composant), un mouvement de bloc entier (translation +
    rotation rigide de tous ses composants a la fois) - un bloc peut donc encore changer de
    position/orientation et etre reoptimise ici, il n'est jamais verrouille."""
    all_refs = [r for refs in blocks_map.values() for r in refs]
    # Un bloc contenant une ancre fixe ne peut pas etre deplace en rigide (meme raison que
    # dans assemble_rigid_groups : rigid_transform ignore les composants fixes, un bloc
    # "mixte" perdrait donc sa rigidite a chaque mouvement accepte). Ses membres libres
    # restent individuellement mobiles via les mouvements composant-par-composant ci-dessous.
    movable_blocks = [b for b, refs in blocks_map.items() if all(not board.components[r].fixed for r in refs)]
    sa_cfg = cfg.sa_global
    rng = random.Random(sa_cfg.seed)
    nets = board.nets

    current = total_cost(board, all_refs, nets, weights)
    best = current
    best_snapshot = board.clone_positions()

    n_steps = max(sa_cfg.iterations, 1)
    log_ratio = math.log(max(sa_cfg.t_end, 1e-6) / max(sa_cfg.t0, 1e-6))

    for step in range(n_steps):
        t = sa_cfg.t0 * math.exp(log_ratio * step / n_steps)
        before = board.clone_positions()

        if movable_blocks and rng.random() < cfg.block_move_prob:
            b = rng.choice(movable_blocks)
            refs = blocks_map[b]
            pivot = _group_centroid(board, refs)
            dx = rng.gauss(0, max(t, 0.1))
            dy = rng.gauss(0, max(t, 0.1))
            rotate = rng.choice(ALLOWED_ROTATIONS) if rng.random() < 0.3 else 0
            rigid_transform(board, refs, dx, dy, rotate, pivot)
        else:
            movable = [r for r in all_refs if not board.components[r].fixed]
            if not movable:
                break
            move_kind = rng.random()
            r = rng.choice(movable)
            comp = board.components[r]
            if move_kind < sa_cfg.move_translate_prob:
                std = max(t * sa_cfg.translate_step_frac, 0.05)
                comp.x += rng.gauss(0, std)
                comp.y += rng.gauss(0, std)
            elif move_kind < sa_cfg.move_translate_prob + sa_cfg.move_rotate_prob:
                comp.rotation = rng.choice(ALLOWED_ROTATIONS)
            else:
                other = rng.choice(movable)
                if other != r:
                    oc = board.components[other]
                    comp.x, oc.x = oc.x, comp.x
                    comp.y, oc.y = oc.y, comp.y
                    comp.rotation, oc.rotation = oc.rotation, comp.rotation

        new_cost = total_cost(board, all_refs, nets, weights)
        delta = new_cost.total - current.total
        accept = delta < 0 or (t > 1e-9 and rng.random() < math.exp(-delta / max(t, 1e-9)))

        if accept:
            current = new_cost
            if is_better(new_cost, best):
                best = new_cost
                best_snapshot = board.clone_positions()
        else:
            board.restore_positions(before)

    board.restore_positions(best_snapshot)
    return best


def optimize_board(board: Board, weights: CostWeights, cfg: HierarchyConfig) -> CostBreakdown:
    """Pipeline complet, niveaux 1 a 5."""
    blocks = board.blocks()
    for bi, block in enumerate(blocks):
        optimize_block(board, block, weights, cfg, seed=cfg.seed * 100 + bi)

    blocks_map = {b: board.refs_in_block(b) for b in blocks}
    # Niveau 4 : assemblage des blocs entre eux (memes outils que l'assemblage de groupes).
    assemble_rigid_groups(board, list(blocks_map.values()), weights, cfg, seed=cfg.seed)

    all_refs = [r for refs in blocks_map.values() for r in refs]
    legalize(board, all_refs, min_clearance_mm=weights.min_clearance_mm)

    # Niveau 5 : recuit global avec mouvements de bloc.
    cost = run_global_annealing_with_block_moves(board, blocks_map, weights, cfg)
    # Deux passes de legalisation : une chaine de poussees (A pousse B qui pousse C...) peut
    # laisser un residu apres la premiere passe si elle s'arrete a max_iters ; relancer sur
    # l'etat deja presque legal converge generalement en quelques iterations de plus.
    legalize(board, all_refs, min_clearance_mm=weights.min_clearance_mm)
    legalize(board, all_refs, min_clearance_mm=weights.min_clearance_mm)
    cost = total_cost(board, all_refs, board.nets, weights)
    return cost
