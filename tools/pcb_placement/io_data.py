"""Chargement du JSON d'extraction (tools/kicad_tetris_extract.py) vers le modele interne,
et sauvegarde/relecture des solutions de placement (positions/rotations)."""
from __future__ import annotations

import json
from typing import Dict

from .model import Board, Component, Net, Pad


def load_board(extract_json_path: str) -> Board:
    with open(extract_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    components: Dict[str, Component] = {}
    nets: Dict[str, Net] = {}

    for c in data["components"]:
        pads = [Pad(name=p["name"], net=p["net"], local_x=p["x"], local_y=p["y"]) for p in c["pads"]]
        comp = Component(
            ref=c["ref"],
            value=c["value"],
            block=c["block"],
            is_anchor=c["is_anchor"],
            courtyard_w=c["courtyard_w_mm"],
            courtyard_h=c["courtyard_h_mm"],
            courtyard_offset_x=c["courtyard_center_offset_x_mm"],
            courtyard_offset_y=c["courtyard_center_offset_y_mm"],
            pads=pads,
            x=c["current_x_mm"],
            y=c["current_y_mm"],
            rotation=_snap_rotation(c["current_rotation_deg"]),
            fixed=c["is_anchor"],
        )
        components[comp.ref] = comp
        for p in pads:
            if not p.net:
                continue
            net = nets.setdefault(p.net, Net(name=p.net))
            net.pins.append((comp.ref, p.name))

    # Les reseaux a une seule pastille ne contraignent rien (pas de paire a relier) : on les
    # garde dans Board.nets pour la tracabilite mais le cout les ignore (cf. cost.py).
    board = Board(
        components=components,
        nets=nets,
        source_pcb=data.get("source_pcb", ""),
        outline_w=data["board_outline_bbox_mm"]["w_mm"],
        outline_h=data["board_outline_bbox_mm"]["h_mm"],
    )
    return board


def _snap_rotation(angle_deg: float) -> int:
    a = round(angle_deg / 90.0) * 90 % 360
    return int(a)


def save_solution(board: Board, path: str, extra: dict | None = None) -> None:
    sol = {
        "source_pcb": board.source_pcb,
        "positions": {
            r: {"x_mm": round(c.x, 4), "y_mm": round(c.y, 4), "rotation_deg": c.rotation}
            for r, c in board.components.items()
        },
    }
    if extra:
        sol["metrics"] = extra
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sol, f, indent=2)


def load_solution_into(board: Board, path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        sol = json.load(f)
    for ref, pos in sol["positions"].items():
        if ref not in board.components:
            continue
        c = board.components[ref]
        c.x = pos["x_mm"]
        c.y = pos["y_mm"]
        c.rotation = int(pos["rotation_deg"])
