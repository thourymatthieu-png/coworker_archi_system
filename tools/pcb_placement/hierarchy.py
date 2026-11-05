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
from .compaction import _Packer, compact
from .cost import CostBreakdown, CostWeights, block_dispersion, is_better, total_cost
from . import live
from .incremental import IncrementalCost
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
    # Passe de compactage deterministe (0 chevauchement/hors-contour garanti) en fin de
    # pipeline plutot que la legalisation seule - cf. optimize_board. Desactiver seulement
    # pour comparer au comportement historique (recuit + legalisation seules).
    use_compaction: bool = True
    # Penalite progressive du recuit global : le poids des contraintes de recouvrement et de
    # contour demarre a `penalty_start` x sa valeur pleine et monte (geometriquement) jusqu'a
    # 1 apres `penalty_ramp_frac` des pas. Evite de forcer un etat faisable avant le recuit
    # (qui deplace des composants a l'aveugle) et laisse le recuit resoudre les recouvrements
    # en douceur. False : ancien comportement (remise en etat faisable puis poids plein).
    penalty_ramp: bool = False
    penalty_start: float = 0.03
    penalty_ramp_frac: float = 0.7
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
        live.tick(board)
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


def _attached_wirelength(board: Board, cluster: List[str], placed: set, nets) -> float:
    """Demi-perimetre cumule des reseaux (<= 8 pastilles) qui relient `cluster` a des
    composants DEJA poses (`placed`), en ne regardant que ces pastilles-la : mesure le cout de
    cablage d'un emplacement de bloc vis-a-vis de ce qui est deja en place (les blocs pas encore
    poses sont dans un repere arbitraire et fausseraient le calcul)."""
    cl = set(cluster)
    total = 0.0
    for net in nets.values():
        if len(net.pins) > 8:
            continue
        xs, ys, mine, other = [], [], False, False
        for ref, pad in net.pins:
            if ref in cl:
                mine = True
            elif ref in placed:
                other = True
            else:
                continue
            pos = board.pad_world_pos(ref, pad)
            if pos is None:
                continue
            xs.append(pos[0])
            ys.append(pos[1])
        if mine and other and len(xs) >= 2:
            total += (max(xs) - min(xs)) + (max(ys) - min(ys))
    return total


def assemble_blocks(board: Board, blocks_map: Dict[str, List[str]], weights: CostWeights,
                    cfg: HierarchyConfig, seed: int) -> None:
    """Niveau 4 (avec contour impose) : pose chaque bloc comme un RECTANGLE RIGIDE dans le
    contour, autour des pieces verrouillees, sans recouvrement. Remplace l'assemblage par
    forces dirigees (`assemble_rigid_groups`) qui empile les blocs les uns sur les autres puis
    laisse `legalize` repousser les composants un par un, ce qui defait les grappes construites
    aux niveaux inferieurs.

    Les blocs sont poses du plus grand au plus petit ; chacun va a l'emplacement libre le plus
    proche de la position qui le rapproche de ce qui est deja pose (reseaux de <= 8 pastilles,
    pieces verrouillees comprises), avec la rotation d'ensemble (0/90/180/270) qui minimise le
    cablage vers l'existant. Seuls les composants LIBRES d'un bloc bougent (les verrouilles
    restent, ils servent d'obstacles). Un bloc qui ne tient nulle part est laisse a sa place et
    signale ; `legalize` et le recuit global s'en occupent alors comme avant."""
    if board.outline is None:
        assemble_rigid_groups(board, list(blocks_map.values()), weights, cfg, seed)
        return
    rng = random.Random(seed)
    fixed_rects = []
    placed = set()
    for r, c in board.components.items():
        if c.fixed:
            x0, y0, x1, y1 = c.world_bbox()
            fixed_rects.append({"id": r, "x0": x0, "y0": y0, "x1": x1, "y1": y1})
            placed.add(r)
    packer = _Packer(margin=weights.min_clearance_mm, rng=rng, outline=board.outline, fixed=fixed_rects)
    ox0, oy0, ox1, oy1 = board.outline
    board_c = ((ox0 + ox1) / 2.0, (oy0 + oy1) / 2.0)

    # Un bloc qui contient une piece verrouillee (pilotes des moteurs M1-M4 aux quatre coins,
    # composants du module radio U7) a deja ses composants tires vers ses ancres : ils sont
    # a peu pres a leur place dans le repere de la carte, repartis entre les ancres (constate :
    # 4 a 7 composants sur 37 a 44 mm). Un rectangle rigide n'aurait pas de sens : le bloc
    # reste en place (comme avant pour les groupes ancres) et ses composants servent d'obstacles
    # et de points d'attraction pour les autres blocs ; `legalize` et le compactage reglent les
    # recouvrements restants.
    clusters = []
    for b, refs in blocks_map.items():
        free = [r for r in refs if not board.components[r].fixed]
        if not free:
            continue
        if any(board.components[r].fixed for r in refs):
            for r in free:
                x0, y0, x1, y1 = board.components[r].world_bbox()
                packer.placed.append({"id": r, "x0": x0, "y0": y0, "x1": x1, "y1": y1})
                placed.add(r)
            continue
        x0, y0, x1, y1 = board.global_bbox(free)
        clusters.append((b, free, (x1 - x0) * (y1 - y0)))
    clusters.sort(key=lambda t: t[2], reverse=True)

    unfit = []
    for b, free, _a in clusters:
        live.tick(board)
        pivot = _group_centroid(board, free)
        # cible : centre de gravite des composants deja poses relies a ce bloc
        cl = set(free)
        sx = sy = sw = 0.0
        for net in board.nets.values():
            if len(net.pins) > 8:
                continue
            mine = [r for r, _p in net.pins if r in cl]
            other = [r for r, _p in net.pins if r in placed]
            if mine and other:
                w = 1.0 / (len(net.pins) - 1)
                for r in other:
                    cx, cy = board.components[r].world_center()
                    sx += w * cx
                    sy += w * cy
                    sw += w
        target = (sx / sw, sy / sw) if sw > 0 else board_c

        best = None
        for k in range(4):
            if k > 0:
                rigid_transform(board, free, 0.0, 0.0, 90, pivot)
            x0, y0, x1, y1 = board.global_bbox(free)
            w, h = x1 - x0, y1 - y0
            spot = packer._scan_free_spot(w, h, target, step=0.5)
            if spot is None:
                continue
            dx, dy = spot[0] - x0, spot[1] - y0
            rigid_transform(board, free, dx, dy, 0, pivot)
            wl = _attached_wirelength(board, free, placed, board.nets)
            dist = math.hypot(spot[0] + w / 2.0 - target[0], spot[1] + h / 2.0 - target[1])
            rigid_transform(board, free, -dx, -dy, 0, pivot)
            score = wl + 0.2 * dist
            if best is None or score < best[0]:
                best = (score, k, dx, dy, spot, w, h)
        # revenir a la rotation retenue (on est a 270 apres la boucle)
        if best is None:
            rigid_transform(board, free, 0.0, 0.0, 90, pivot)  # retour a 0
            unfit.append(b)
            placed.update(free)
            continue
        rigid_transform(board, free, 0.0, 0.0, 90 * ((best[1] + 1) % 4), pivot)
        rigid_transform(board, free, best[2], best[3], 0, pivot)
        spot, w, h = best[4], best[5], best[6]
        packer.placed.append({"id": b, "x0": spot[0], "y0": spot[1], "x1": spot[0] + w, "y1": spot[1] + h})
        placed.update(free)
    if unfit:
        print(f"ATTENTION : {len(unfit)} bloc(s) ne tiennent pas comme rectangle rigide dans le "
              f"contour : {unfit} (laisses a legalize et au recuit global)")


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
    live.set_phase("groupes : forces dirigees puis recuit", block=block, show_cost=False)
    for gi, g in enumerate(groups):
        optimize_group(board, g, weights, cfg, seed=seed * 1000 + gi)
    live.set_phase("assemblage des groupes du bloc", block=block, show_cost=False)
    assemble_rigid_groups(board, groups, weights, cfg, seed=seed)
    legalize(board, refs, min_clearance_mm=weights.min_clearance_mm)
    live.set_phase("recuit du bloc", block=block, show_cost=False)
    sa_cfg = AnnealingConfig(**{**cfg.sa_block.__dict__, "seed": seed})
    cost = run_annealing(board, refs, weights, sa_cfg)
    legalize(board, refs, min_clearance_mm=weights.min_clearance_mm)
    live.mark_done(block)
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

    ic = IncrementalCost(board, all_refs, nets, weights)   # cout incremental
    current = ic.current
    best = current
    best_snapshot = board.clone_positions()

    n_steps = max(sa_cfg.iterations, 1)
    log_ratio = math.log(max(sa_cfg.t_end, 1e-6) / max(sa_cfg.t0, 1e-6))

    for step in range(n_steps):
        if cfg.penalty_ramp and step % 25 == 0:
            frac = min(step / max(cfg.penalty_ramp_frac * n_steps, 1.0), 1.0)
            current = ic.set_penalty_scale(cfg.penalty_start ** (1.0 - frac))
            if not best.feasible:  # les couts a des poids differents ne se comparent pas
                best = current
                best_snapshot = board.clone_positions()
        t = sa_cfg.t0 * math.exp(log_ratio * step / n_steps)
        before = board.clone_positions()
        moved = []

        if movable_blocks and rng.random() < cfg.block_move_prob:
            b = rng.choice(movable_blocks)
            refs = blocks_map[b]
            pivot = _group_centroid(board, refs)
            dx = rng.gauss(0, max(t, 0.1))
            dy = rng.gauss(0, max(t, 0.1))
            rotate = rng.choice(ALLOWED_ROTATIONS) if rng.random() < 0.3 else 0
            rigid_transform(board, refs, dx, dy, rotate, pivot)
            moved = list(refs)
        else:
            movable = [r for r in all_refs if not board.components[r].fixed]
            if not movable:
                break
            move_kind = rng.random()
            r = rng.choice(movable)
            comp = board.components[r]
            moved = [r]
            if move_kind < sa_cfg.move_translate_prob:
                std = max(t * sa_cfg.translate_step_frac, 0.05)
                comp.x += rng.gauss(0, std)
                comp.y += rng.gauss(0, std)
            elif move_kind < sa_cfg.move_translate_prob + sa_cfg.move_rotate_prob:
                comp.rotation = rng.choice(ALLOWED_ROTATIONS)
            else:
                other = rng.choice(movable)
                if other != r:
                    moved.append(other)
                    oc = board.components[other]
                    comp.x, oc.x = oc.x, comp.x
                    comp.y, oc.y = oc.y, comp.y
                    comp.rotation, oc.rotation = oc.rotation, comp.rotation

        new_cost = ic.propose(moved)
        delta = new_cost.total - current.total
        accept = delta < 0 or (t > 1e-9 and rng.random() < math.exp(-delta / max(t, 1e-9)))

        if accept:
            ic.commit()
            current = new_cost
            if is_better(new_cost, best):
                best = new_cost
                best_snapshot = board.clone_positions()
        else:
            ic.discard()
            board.restore_positions(before)
        live.tick(board, current)

    board.restore_positions(best_snapshot)
    return total_cost(board, all_refs, nets, weights)


def optimize_board(board: Board, weights: CostWeights, cfg: HierarchyConfig) -> CostBreakdown:
    """Pipeline complet, niveaux 1 a 5."""
    blocks = board.blocks()
    for bi, block in enumerate(blocks):
        optimize_block(board, block, weights, cfg, seed=cfg.seed * 100 + bi)

    blocks_map = {b: board.refs_in_block(b) for b in blocks}
    # Niveau 4 : assemblage des blocs entre eux (memes outils que l'assemblage de groupes).
    live.set_phase("assemblage des blocs sur la carte", block=None, show_cost=False)
    assemble_blocks(board, blocks_map, weights, cfg, seed=cfg.seed)

    all_refs = [r for refs in blocks_map.values() for r in refs]
    legalize(board, all_refs, min_clearance_mm=weights.min_clearance_mm)
    if cfg.use_compaction and board.outline is not None and not cfg.penalty_ramp:
        # Etat FAISABLE avant le recuit global : sinon la penalite de recouvrement/contour
        # (poids 1000) domine le cout et le recuit passe son temps a repousser les composants
        # au hasard, ce qui eclate les grappes construites aux niveaux inferieurs. Deplacement
        # minimal : seuls les composants en defaut bougent.
        compact(board, all_refs, margin_mm=weights.min_clearance_mm, seed=cfg.seed)

    # Niveau 5 : recuit global avec mouvements de bloc.
    live.set_phase("recuit global (mouvements de blocs et de composants)", block=None, show_cost=True)
    cost = run_global_annealing_with_block_moves(board, blocks_map, weights, cfg)

    if cfg.use_compaction:
        # Passe de compactage deterministe : GARANTIT 0 chevauchement et 0 hors-contour par
        # construction (le recuit + la legalisation seuls peuvent laisser des residus ou de
        # grands vides, cf. retour utilisateur du 2026-11-05) - remplace la legalisation en
        # fin de pipeline. Garde approximativement le regroupement par bloc du recuit
        # (default_compaction_order), au prix d'un resultat un peu moins affine cote cablage
        # qu'un recuit seul.
        live.set_phase("compactage final (zero recouvrement)", block=None, show_cost=False)
        unplaced = compact(board, all_refs, margin_mm=weights.min_clearance_mm, seed=cfg.seed)
        if unplaced:
            print(f"ATTENTION : {len(unplaced)} composant(s) n'ont trouve aucune place dans "
                  f"le contour impose (carte trop petite/dense pour cette config) : {unplaced}")
    else:
        # Repli historique (pas de contour fixe, ou compactage explicitement desactive) :
        # deux passes de legalisation seulement (poussee locale, peut laisser un residu).
        legalize(board, all_refs, min_clearance_mm=weights.min_clearance_mm)
        legalize(board, all_refs, min_clearance_mm=weights.min_clearance_mm)

    cost = total_cost(board, all_refs, board.nets, weights)
    cost.dispersion_mm = block_dispersion(board)[0]
    live.set_phase("cycle termine", block=None, show_cost=True)
    live.tick(board, cost, force=True)
    return cost
