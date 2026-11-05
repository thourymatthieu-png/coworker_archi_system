"""Recuit simule : explore translations, rotations et echanges de position sur un
sous-ensemble de composants (un groupe, un bloc, ou la carte entiere), evalue par la
fonction de cout complete (tools.pcb_placement.cost). Independant de KiCad : ne touche que
le modele interne (Board)."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional

from .cost import CostBreakdown, CostWeights, is_better, total_cost
from . import live
from .incremental import IncrementalCost
from .model import ALLOWED_ROTATIONS, Board, Net


@dataclass
class AnnealingConfig:
    t0: float = 15.0           # temperature initiale (mm, ordre de grandeur des deplacements acceptes au depart)
    t_end: float = 0.05        # temperature finale
    iterations: int = 2000
    move_translate_prob: float = 0.55
    move_rotate_prob: float = 0.2
    move_swap_prob: float = 0.25  # le reste
    translate_step_frac: float = 1.0  # fraction de la temperature utilisee comme ecart-type du deplacement gaussien
    seed: int = 0


def relevant_nets(board: Board, refs: List[str]) -> Dict[str, Net]:
    ref_set = set(refs)
    return {name: net for name, net in board.nets.items() if any(r in ref_set for r, _p in net.pins)}


def run_annealing(
    board: Board,
    refs: List[str],
    weights: CostWeights,
    config: AnnealingConfig,
    nets: Optional[Dict[str, Net]] = None,
) -> CostBreakdown:
    """Optimise les positions/rotations des composants MOBILES de `refs` (les autres restent
    fixes et servent d'obstacles). Modifie `board` en place et renvoie le detail du cout de
    la MEILLEURE solution trouvee (deja re-appliquee sur `board` avant de retourner)."""
    movable = [r for r in refs if not board.components[r].fixed]
    nets = nets if nets is not None else relevant_nets(board, refs)
    if not movable:
        return total_cost(board, refs, nets, weights)

    rng = random.Random(config.seed)
    ic = IncrementalCost(board, refs, nets, weights)   # cout incremental (cf. incremental.py)
    current_cost = ic.current
    best_cost = current_cost
    best_snapshot = board.clone_positions()

    n_steps = max(config.iterations, 1)
    log_ratio = math.log(max(config.t_end, 1e-6) / max(config.t0, 1e-6))

    for step in range(n_steps):
        t = config.t0 * math.exp(log_ratio * step / n_steps)
        before = {r: (board.components[r].x, board.components[r].y, board.components[r].rotation) for r in movable}

        move_kind = rng.random()
        r = rng.choice(movable)
        comp = board.components[r]
        moved = [r]
        if move_kind < config.move_translate_prob:
            std = max(t * config.translate_step_frac, 0.05)
            comp.x += rng.gauss(0, std)
            comp.y += rng.gauss(0, std)
        elif move_kind < config.move_translate_prob + config.move_rotate_prob:
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
        delta = new_cost.total - current_cost.total
        accept = delta < 0
        if not accept and t > 1e-9:
            accept = rng.random() < math.exp(-delta / max(t, 1e-9))

        if accept:
            ic.commit()
            current_cost = new_cost
            if is_better(new_cost, best_cost):
                best_cost = new_cost
                best_snapshot = board.clone_positions()
        else:
            ic.discard()
            for ref, (x, y, rot) in before.items():
                c = board.components[ref]
                c.x, c.y, c.rotation = x, y, rot
        live.tick(board, current_cost)

    board.restore_positions(best_snapshot)
    # cout final exact (la grille de congestion incrementale differe legerement de la reference)
    return total_cost(board, refs, nets, weights)
