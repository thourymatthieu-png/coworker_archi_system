"""Boucle d'optimisation complete (section 6) et strategies en parallele (section 10) :
genere une solution initiale, optimise (hierarchy.optimize_board), evalue, compare a la
meilleure solution connue, recommence jusqu'au critere d'arret - plusieurs fois en parallele
avec des graines differentes, puis garde la meilleure solution FAISABLE (sans recouvrement)
toutes strategies confondues."""
from __future__ import annotations

import dataclasses
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .config import EngineConfig
from .cost import CostBreakdown, is_better
from .hierarchy import optimize_board
from .io_data import load_board
from .model import Board


@dataclass
class CycleResult:
    cycle: int
    cost: CostBreakdown


@dataclass
class StrategyResult:
    seed: int
    best_cost: CostBreakdown
    positions: Dict[str, Tuple[float, float, int]]
    history: List[CycleResult]
    elapsed_s: float


def run_strategy(extract_json_path: str, config: EngineConfig, seed: int, progress_prefix: str = "") -> StrategyResult:
    board = load_board(extract_json_path)
    weights = config.to_cost_weights()

    best_cost: Optional[CostBreakdown] = None
    best_snapshot = None
    no_improve = 0
    history: List[CycleResult] = []
    t_start = time.time()

    for cycle in range(config.stopping.max_cycles):
        hcfg = config.to_hierarchy_config(seed=seed * 10_000 + cycle)
        cost = optimize_board(board, weights, hcfg)
        history.append(CycleResult(cycle=cycle, cost=cost))
        print(f"{progress_prefix}graine {seed} cycle {cycle}: cout={cost.total:.1f} "
              f"(aire={cost.area_mm2:.0f}mm2, cablage={cost.wirelength_mm:.0f}mm, "
              f"croisements={cost.crossings}, vias~={cost.vias_estimate}, "
              f"recouvrement={cost.overlap_mm2:.2f}mm2, faisable={cost.feasible})")

        improved = best_cost is None or is_better(cost, best_cost)
        if improved:
            best_cost = cost
            best_snapshot = board.clone_positions()
            no_improve = 0
        else:
            no_improve += 1

        if no_improve >= config.stopping.no_improve_cycles:
            break
        if config.stopping.time_budget_s and (time.time() - t_start) > config.stopping.time_budget_s:
            break

    if best_snapshot is None:
        # Aucun cycle n'a ete faisable (carte trop dense pour la config donnee) : on garde
        # tout de meme le dernier essai pour diagnostic plutot que de ne rien retourner.
        best_cost = history[-1].cost
        best_snapshot = board.clone_positions()

    board.restore_positions(best_snapshot)
    return StrategyResult(seed=seed, best_cost=best_cost, positions=best_snapshot, history=history, elapsed_s=time.time() - t_start)


def _run_strategy_worker(extract_json_path: str, config_dict: dict, seed: int) -> StrategyResult:
    config = _config_from_dict(config_dict)
    return run_strategy(extract_json_path, config, seed, progress_prefix=f"[strategie {seed}] ")


def _config_from_dict(config_dict: dict) -> EngineConfig:
    from .config import StoppingCriteria
    data = dict(config_dict)
    stopping_data = data.pop("stopping", None)
    cfg = EngineConfig(**data)
    if stopping_data:
        cfg.stopping = StoppingCriteria(**stopping_data)
    return cfg


def run_parallel_strategies(extract_json_path: str, config: EngineConfig, parallel: bool = True) -> List[StrategyResult]:
    seeds = [config.random_seed + i for i in range(config.n_parallel_strategies)]
    config_dict = dataclasses.asdict(config)

    if not parallel or config.n_parallel_strategies <= 1:
        return [run_strategy(extract_json_path, config, s) for s in seeds]

    results: List[StrategyResult] = []
    with ProcessPoolExecutor(max_workers=config.n_parallel_strategies) as pool:
        futures = {pool.submit(_run_strategy_worker, extract_json_path, config_dict, s): s for s in seeds}
        for fut in as_completed(futures):
            results.append(fut.result())
    results.sort(key=lambda r: r.seed)
    return results


def best_of(results: List[StrategyResult]) -> StrategyResult:
    feasible = [r for r in results if r.best_cost.feasible]
    pool = feasible if feasible else results
    return min(pool, key=lambda r: r.best_cost.total)
