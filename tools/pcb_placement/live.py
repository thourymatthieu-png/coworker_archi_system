"""Suivi en direct du placement : le moteur ecrit des instantanes JSON, une page web locale
(`viewer/index.html`) les relit et anime les composants.

Fichiers ecrits dans le dossier `live_dir` :
- `static.json`        : une fois, avant le calcul (composants, pastilles, reseaux, regles de
                         decouplage, contour, couleurs par bloc) ;
- `state_<graine>.json`: un par strategie, reecrit toutes les ~0,25 s (positions, phase,
                         bloc en cours, blocs termines, metriques).

Aucun effet si `configure()` n'a pas ete appele (`live_dir` absent) : les appels `tick` /
`set_phase` sortent immediatement. Chaque processus de strategie a son propre etat module.
Ecriture atomique (fichier temporaire puis remplacement) pour que la page ne lise jamais un
fichier a moitie ecrit."""
from __future__ import annotations

import json
import os
import time
from typing import Dict, List, Optional

_MIN_INTERVAL_S = 0.25

_dir: Optional[str] = None
_seed = 0
_cycle = 0
_phase = ""
_block: Optional[str] = None
_done: List[str] = []
_show_cost = False
_cost: Optional[dict] = None
_last = 0.0
_t0 = 0.0


def configure(live_dir: Optional[str], seed: int = 0) -> None:
    global _dir, _seed, _cycle, _phase, _block, _done, _show_cost, _cost, _last, _t0
    _dir = live_dir
    _seed = seed
    _cycle = 0
    _phase = "demarrage"
    _block = None
    _done = []
    _show_cost = False
    _cost = None
    _last = 0.0
    _t0 = time.time()


def enabled() -> bool:
    return _dir is not None


def set_cycle(cycle: int) -> None:
    global _cycle, _done, _block
    _cycle = cycle
    _done = []
    _block = None


def set_phase(label: str, block: Optional[str] = None, show_cost: Optional[bool] = None) -> None:
    global _phase, _block, _show_cost
    _phase = label
    _block = block
    if show_cost is not None:
        _show_cost = show_cost


def mark_done(block: str) -> None:
    if block not in _done:
        _done.append(block)


def _cost_dict(c) -> dict:
    return {
        "total": round(c.total, 1), "area": round(c.area_mm2, 1), "hpwl": round(c.wirelength_mm, 1),
        "crossings": int(c.crossings), "vias": int(c.vias_estimate),
        "overlap": round(c.overlap_mm2, 3), "oob": round(c.out_of_bounds_mm2, 3),
        "decoupling": round(getattr(c, "decoupling_mm", 0.0), 1), "feasible": bool(c.feasible),
    }


def _write(name: str, data: dict) -> None:
    path = os.path.join(_dir, name)
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"))
        os.replace(tmp, path)
    except OSError:
        pass  # la page relira au prochain instantane (fichier momentanement verrouille)


def tick(board, cost=None, force: bool = False, finished: bool = False) -> None:
    """Ecrit un instantane si le dernier date de plus de _MIN_INTERVAL_S (ou si `force`)."""
    global _last, _cost
    if _dir is None:
        return
    now = time.monotonic()
    if not force and now - _last < _MIN_INTERVAL_S:
        return
    _last = now
    if cost is not None and _show_cost:
        _cost = _cost_dict(cost)
    snap = {
        "seed": _seed, "cycle": _cycle, "phase": _phase, "block": _block, "done": list(_done),
        "elapsed_s": round(time.time() - _t0, 1), "finished": finished,
        "cost": _cost if _show_cost else None,
        "pos": {r: [round(c.x, 3), round(c.y, 3), round(float(c.rotation), 1)]
                for r, c in board.components.items()},
    }
    _write(f"state_{_seed}.json", snap)


def write_static(live_dir: str, board, n_strategies: int, block_colors: Dict[str, str],
                 block_labels: Dict[str, str]) -> None:
    """Description fixe de la carte, ecrite une fois par le processus principal."""
    comps = []
    for ref, c in board.components.items():
        comps.append({
            "ref": ref, "value": c.value, "block": c.block, "fixed": bool(c.fixed),
            "w": round(c.courtyard_w, 3), "h": round(c.courtyard_h, 3),
            "ox": round(c.courtyard_offset_x, 3), "oy": round(c.courtyard_offset_y, 3),
            "pads": [{"n": p.name, "net": p.net, "x": round(p.local_x, 3), "y": round(p.local_y, 3)}
                     for p in c.pads],
        })
    nets = {name: [[r, p] for r, p in net.pins] for name, net in board.nets.items() if len(net.pins) >= 2}
    data = {
        "outline": list(board.outline) if board.outline else None,
        "n_strategies": n_strategies,
        "components": comps, "nets": nets,
        "decoupling": board.decoupling_rules,
        "blocks": sorted(board.blocks()),
        "block_colors": block_colors, "block_labels": block_labels,
    }
    os.makedirs(live_dir, exist_ok=True)
    path = os.path.join(live_dir, "static.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))
