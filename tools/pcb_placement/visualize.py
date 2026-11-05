"""Visualisation du placement (avant/apres) et rapport texte des metriques (section 9)."""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

from .cost import CostBreakdown, net_segments
from .model import Board

_PALETTE = [
    "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
    "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac",
]


def draw_board(board: Board, ax, title: str, show_nets: bool = True) -> None:
    blocks = board.blocks()
    color_by_block = {b: _PALETTE[i % len(_PALETTE)] for i, b in enumerate(blocks)}

    if show_nets:
        for p1, p2, _net in net_segments(board):
            ax.add_line(Line2D([p1[0], p2[0]], [p1[1], p2[1]], color="#999999", linewidth=0.4, alpha=0.7, zorder=1))

    for ref, comp in board.components.items():
        x0, y0, x1, y1 = comp.world_bbox()
        color = color_by_block.get(comp.block, "#cccccc")
        edge = "black" if comp.fixed else color
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=color, edgecolor=edge,
                                linewidth=0.8 if comp.fixed else 0.4, alpha=0.75, zorder=2))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, ref, ha="center", va="center", fontsize=3.5, zorder=3)

    x0, y0, x1, y1 = board.global_bbox()
    margin = 3
    ax.set_xlim(x0 - margin, x1 + margin)
    ax.set_ylim(y1 + margin, y0 - margin)  # Y vers le bas comme dans KiCad
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("x (mm)", fontsize=7)
    ax.set_ylabel("y (mm)", fontsize=7)
    ax.tick_params(labelsize=6)


def save_comparison(board_before: Board, board_after: Board, cost_before: Optional[CostBreakdown],
                     cost_after: CostBreakdown, out_path: str) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    title_before = "Placement initial"
    if cost_before is not None:
        title_before += f" (cout={cost_before.total:.0f})"
    draw_board(board_before, axes[0], title_before)
    draw_board(board_after, axes[1], f"Placement optimise (cout={cost_after.total:.0f})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def format_report(cost_before: Optional[CostBreakdown], cost_after: CostBreakdown, elapsed_s: float,
                   strategy_history: Optional[List[Tuple[int, CostBreakdown]]] = None) -> str:
    lines = ["# Rapport d'optimisation du placement PCB", ""]
    if cost_before is not None:
        lines.append("## Avant")
        lines.append(_format_cost(cost_before))
        lines.append("")
    lines.append("## Apres (meilleure solution retenue)")
    lines.append(_format_cost(cost_after))
    lines.append("")
    if cost_before is not None and cost_before.area_mm2 > 0:
        gain_area = 100.0 * (1 - cost_after.area_mm2 / cost_before.area_mm2)
        lines.append(f"Gain de surface : {gain_area:.1f} %")
    lines.append(f"Temps de calcul : {elapsed_s:.1f} s")
    if strategy_history:
        lines.append("")
        lines.append("## Historique par cycle")
        for seed, c in strategy_history:
            lines.append(f"- graine {seed} : cout={c.total:.1f}, faisable={c.feasible}")
    return "\n".join(lines)


def _format_cost(c: CostBreakdown) -> str:
    return (
        f"- Surface occupee : {c.area_mm2:.1f} mm2\n"
        f"- Longueur de cablage estimee (HPWL) : {c.wirelength_mm:.1f} mm\n"
        f"- Congestion (indice) : {c.congestion:.1f}\n"
        f"- Croisements de pistes probables : {c.crossings}\n"
        f"- Vias estimes : {c.vias_estimate}\n"
        f"- Penalite d'accessibilite des pastilles : {c.accessibility_penalty:.1f}\n"
        f"- Recouvrement residuel : {c.overlap_mm2:.4f} mm2 ({'OK' if c.feasible else 'VIOLATION'})\n"
        f"- Cout total pondere : {c.total:.1f}"
    )
