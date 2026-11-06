"""Visualisation du placement (avant/apres) et rapport texte des metriques (section 9)."""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from matplotlib.lines import Line2D

from .cost import CostBreakdown, net_segments
from .model import Board

# 12 couleurs franches et bien distinctes (palette Okabe-Ito completee), une par bloc.
_PALETTE = [
    "#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9",
    "#F0E442", "#8B4513", "#6A3D9A", "#2F4F4F", "#FF1493", "#7FBF00",
    "#A6CEE3", "#B15928",
]


_DARK = {"#0072B2", "#D55E00", "#8B4513", "#6A3D9A", "#2F4F4F", "#009E73", "#FF1493", "#B15928"}


def block_colors(board: Board) -> Dict[str, str]:
    """Couleur par bloc fonctionnel, stable (ordre alphabetique) d'une carte a l'autre."""
    return {b: _PALETTE[i % len(_PALETTE)] for i, b in enumerate(sorted(board.blocks()))}


def block_label(block: str) -> str:
    """'DES-007-puissance-moteurs' -> 'DES-007 puissance moteurs'."""
    parts = block.split("-")
    if len(parts) >= 3 and parts[0] == "DES":
        return f"{parts[0]}-{parts[1]} {' '.join(parts[2:])}"
    return block


def draw_board(board: Board, ax, title: str, show_nets: bool = True) -> None:
    color_by_block = block_colors(board)

    if show_nets:
        for p1, p2, _net in net_segments(board):
            ax.add_line(Line2D([p1[0], p2[0]], [p1[1], p2[1]], color="#999999", linewidth=0.4, alpha=0.7, zorder=1))

    for ref, comp in board.components.items():
        x0, y0, x1, y1 = comp.world_bbox()
        color = color_by_block.get(comp.block, "#cccccc")
        edge = "black" if comp.fixed else "#222222"
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=color, edgecolor=edge,
                                linewidth=1.2 if comp.fixed else 0.35, alpha=0.9, zorder=2,
                                hatch="//" if comp.fixed else None))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, ref, ha="center", va="center", fontsize=3.5,
                color="white" if color in _DARK else "black", zorder=3)

    if board.outline is not None:
        ox0, oy0, ox1, oy1 = board.outline
        ax.add_patch(Rectangle((ox0, oy0), ox1 - ox0, oy1 - oy0, fill=False, edgecolor="red",
                                linewidth=1.3, linestyle="--", zorder=4))

    x0, y0, x1, y1 = board.global_bbox()
    if board.outline is not None:
        ox0, oy0, ox1, oy1 = board.outline
        x0, y0, x1, y1 = min(x0, ox0), min(y0, oy0), max(x1, ox1), max(y1, oy1)
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
    fig, axes = plt.subplots(1, 2, figsize=(14, 7.5))
    title_before = "Placement initial"
    if cost_before is not None:
        title_before += f" (cout={cost_before.total:.0f})"
    draw_board(board_before, axes[0], title_before)
    draw_board(board_after, axes[1], f"Placement optimise (cout={cost_after.total:.0f})")
    colors = block_colors(board_after)
    handles = [Patch(facecolor=c, edgecolor="#222222", label=block_label(b)) for b, c in colors.items()]
    handles.append(Patch(facecolor="white", edgecolor="black", hatch="//", label="fixe (verrouille)"))
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=7, frameon=False)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
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
        f"- Recouvrement residuel : {c.overlap_mm2:.4f} mm2\n"
        f"- Hors du contour de carte : {c.out_of_bounds_mm2:.4f} mm2\n"
        f"- Depassement des regles de proximite (decouplage, J1, centrale) : {c.decoupling_mm:.2f} mm\n"
        f"- Dispersion moyenne des blocs : {c.dispersion_mm:.1f} mm\n"
        f"- Faisable : {'OK' if c.feasible else 'VIOLATION'}\n"
        f"- Cout total pondere : {c.total:.1f}"
    )
