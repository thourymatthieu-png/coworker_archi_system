"""Phase 1 seule du placement hierarchique : les « petits tas » par bloc.

Pour chaque bloc, partitionne en petits groupes (`partition_refs`) et optimise chaque groupe
(forces dirigees, legalisation, recuit - `hierarchy.optimize_group`), puis s'ARRETE : pas
d'assemblage des groupes, des blocs, ni de recuit global. Produit une image par bloc (un
panneau par groupe : composants, references, chevelu interne) et un rapport texte, pour
critiquer les groupes avant d'aller plus loin. Les groupes ne sont pas poses sur la carte :
chaque panneau est a sa propre echelle, hors contour."""
from __future__ import annotations

import os
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from .cost import hpwl, net_segments, total_cost
from .hierarchy import decoupling_links, optimize_group
from .io_data import apply_active_rules, apply_decoupling, load_board
from .model import Board, Net
from .partition import partition_refs
from .visualize import block_colors, block_label

_GROUP_COLORS = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#8B4513", "#6A3D9A"]


def _sub_nets(board: Board, refs: List[str]) -> Dict[str, Net]:
    s = set(refs)
    out = {}
    for name, net in board.nets.items():
        pins = [(r, p) for r, p in net.pins if r in s]
        if len(pins) >= 2:
            out[name] = Net(name, pins)
    return out


def _draw_group(ax, board: Board, refs: List[str], title: str, color: str) -> None:
    nets = _sub_nets(board, refs)
    for p1, p2, _n in net_segments(board, nets):
        ax.add_line(Line2D([p1[0], p2[0]], [p1[1], p2[1]], color="#777777", linewidth=0.5, zorder=1))
    xs, ys = [], []
    for r in refs:
        c = board.components[r]
        x0, y0, x1, y1 = c.world_bbox()
        xs += [x0, x1]
        ys += [y0, y1]
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="#bbbbbb" if c.fixed else color,
                               edgecolor="black", linewidth=0.7, alpha=0.75, zorder=2,
                               hatch="//" if c.fixed else None))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, r, ha="center", va="center", fontsize=7, zorder=3)
        for p in c.pads:
            px, py = c.pad_world_pos(p)
            ax.plot(px, py, ".", color="black", markersize=1.5, zorder=3)
    m = 1.0
    ax.set_xlim(min(xs) - m, max(xs) + m)
    ax.set_ylim(max(ys) + m, min(ys) - m)   # y vers le bas, comme KiCad
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=8)
    ax.tick_params(labelsize=6)


def run_groups_phase(extract_json: str, out_dir: str, max_group_size: int = 10, seed: int = 0,
                     decoupling_file: str | None = None, rules_file: str | None = None,
                     config=None, group_restarts: int = 6) -> str:
    from .config import EngineConfig
    config = config or EngineConfig()
    config.max_group_size = max_group_size
    board = load_board(extract_json)
    if decoupling_file:
        apply_decoupling(board, decoupling_file, config.decoupling_max_mm)
    if rules_file:
        apply_active_rules(board, rules_file)
    weights = config.to_cost_weights()
    hcfg = config.to_hierarchy_config(seed=seed)
    hcfg.group_restarts = group_restarts
    os.makedirs(out_dir, exist_ok=True)

    colors = block_colors(board)
    lines = ["# Phase 1 : petits groupes par bloc (rien d'assemble)", "",
             f"Taille max d'un groupe : {max_group_size} ; graine {seed}. Chaque groupe est place seul "
             "(hors carte) : seule sa forme interne est a juger.", ""]
    for bi, block in enumerate(board.blocks()):
        refs = board.refs_in_block(block)
        groups = partition_refs(refs, board.nets, max_group_size, decoupling_links(board, hcfg.decoupling_link_weight))
        lines += [f"## {block_label(block)} ({len(refs)} composants, {len(groups)} groupe(s))", ""]
        n = len(groups)
        cols = min(3, n)
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(5.2 * cols, 5.0 * rows), squeeze=False)
        for gi, g in enumerate(groups):
            optimize_group(board, g, weights, hcfg, seed=seed * 1000 + bi * 50 + gi)
            sub = _sub_nets(board, g)
            wl = hpwl(board, sub)
            xs0 = min(board.components[r].world_bbox()[0] for r in g)
            xs1 = max(board.components[r].world_bbox()[2] for r in g)
            ys0 = min(board.components[r].world_bbox()[1] for r in g)
            ys1 = max(board.components[r].world_bbox()[3] for r in g)
            surface_comp = sum((lambda b: (b[2] - b[0]) * (b[3] - b[1]))(board.components[r].world_bbox()) for r in g)
            ax = axes[gi // cols][gi % cols]
            title = f"groupe {gi + 1} : {len(g)} comp., {xs1 - xs0:.1f} x {ys1 - ys0:.1f} mm, cablage {wl:.0f} mm"
            _draw_group(ax, board, g, title, _GROUP_COLORS[gi % len(_GROUP_COLORS)])
            lines.append(f"- Groupe {gi + 1} : {', '.join(sorted(g))} - {xs1 - xs0:.1f} x {ys1 - ys0:.1f} mm "
                         f"(emprise {(xs1 - xs0) * (ys1 - ys0):.0f} mm2 pour {surface_comp:.0f} mm2 de composants), "
                         f"cablage interne {wl:.0f} mm")
        for k in range(n, rows * cols):
            axes[k // cols][k % cols].axis("off")
        fig.suptitle(block_label(block), color=colors[block], fontsize=11)
        fig.tight_layout()
        fname = f"groupes_{block}.png"
        fig.savefig(os.path.join(out_dir, fname), dpi=110)
        plt.close(fig)
        lines += ["", f"Image : `{fname}`", ""]
    report = os.path.join(out_dir, "groupes_rapport.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return report


def free_rectangles(board: Board, obstacles: List[tuple], k: int = 8, step: float = 0.5, margin: float = 0.3) -> List[tuple]:
    """Plus grands rectangles LIBRES du contour de carte, disjoints (glouton : on prend le plus
    grand, on le marque occupe, on recommence). `obstacles` : boites (x0, y0, x1, y1) deja
    posees (gonflees de `margin`). Renvoie [(x0, y0, largeur, hauteur)] par aire decroissante."""
    import numpy as np
    ox0, oy0, ox1, oy1 = board.outline
    nx, ny = int((ox1 - ox0) / step), int((oy1 - oy0) / step)
    occ = np.zeros((ny, nx), dtype=bool)
    for (x0, y0, x1, y1) in obstacles:
        cx0 = max(0, int((x0 - margin - ox0) / step)); cx1 = min(nx, int(np.ceil((x1 + margin - ox0) / step)))
        cy0 = max(0, int((y0 - margin - oy0) / step)); cy1 = min(ny, int(np.ceil((y1 + margin - oy0) / step)))
        if cx1 > cx0 and cy1 > cy0:
            occ[cy0:cy1, cx0:cx1] = True
    out = []
    for _ in range(k):
        heights = np.zeros(nx, dtype=int)
        best = (0, 0, 0, 0, 0)    # aire, x, y, w, h (en cellules)
        for y in range(ny):
            heights = np.where(occ[y], 0, heights + 1)
            stack = []
            for x in range(nx + 1):
                h = heights[x] if x < nx else 0
                start = x
                while stack and stack[-1][1] >= h:
                    sx, sh = stack.pop()
                    area = sh * (x - sx)
                    if area > best[0]:
                        best = (area, sx, y - sh + 1, x - sx, sh)
                    start = sx
                stack.append((start, h))
        if best[0] < 4:
            break
        _a, bx, by, bw, bh = best
        occ[by:by + bh, bx:bx + bw] = True
        out.append((ox0 + bx * step, oy0 + by * step, bw * step, bh * step))
    return out


def optimize_group_in_box(board: Board, refs: List[str], box_w: float, box_h: float, weights, hcfg,
                          seed: int, restarts: int = 10):
    """Refait la phase 1 d'un groupe avec un BUT DE FORME : le groupe doit tenir dans un
    rectangle box_w x box_h (le contour de la carte est remplace le temps du calcul, la
    penalite hors-contour s'applique donc a tous ses composants). Positions rendues dans le
    repere de la boite, coin haut-gauche en (0, 0). Renvoie (faisable, cout)."""
    saved_outline, saved_over = board.outline, board.overhang_refs
    board.outline, board.overhang_refs = (0.0, 0.0, box_w, box_h), frozenset()
    hcfg2 = hcfg.__class__(**{**hcfg.__dict__, "group_restarts": restarts})
    for r in refs:
        c = board.components[r]
        c.x, c.y = box_w / 2.0, box_h / 2.0
    try:
        cost = optimize_group(board, refs, weights, hcfg2, seed=seed)
    finally:
        board.outline, board.overhang_refs = saved_outline, saved_over
    return cost.feasible, cost


def run_rectangles_phase(extract_json: str, out_dir: str, max_group_size: int = 10, seed: int = 0,
                         decoupling_file: str | None = None, rules_file: str | None = None,
                         config=None, group_restarts: int = 6, n_orders: int = 20) -> str:
    """Phase 2 : chaque petit groupe (phase 1) est entoure d'un rectangle rigide, et les
    rectangles sont poses sur la carte (`hierarchy.assemble_blocks`, un « bloc » = un groupe) :
    autour des pieces verrouillees, sans recouvrement, avec la rotation d'ensemble qui minimise
    le cablage vers ce qui est deja pose. Un groupe qui contient une piece verrouillee reste
    autour de son ancre. S'ARRETE la : ni recuit de bloc ni recuit global (ajustement a venir)."""
    from .config import EngineConfig
    from .hierarchy import assemble_blocks
    config = config or EngineConfig()
    config.max_group_size = max_group_size
    board = load_board(extract_json)
    if decoupling_file:
        apply_decoupling(board, decoupling_file, config.decoupling_max_mm)
    if rules_file:
        apply_active_rules(board, rules_file)
    weights = config.to_cost_weights()
    hcfg = config.to_hierarchy_config(seed=seed)
    hcfg.group_restarts = group_restarts
    os.makedirs(out_dir, exist_ok=True)

    groups_map: Dict[str, List[str]] = {}
    group_block: Dict[str, str] = {}
    for bi, block in enumerate(board.blocks()):
        refs = board.refs_in_block(block)
        groups = partition_refs(refs, board.nets, max_group_size, decoupling_links(board, hcfg.decoupling_link_weight))
        for gi, g in enumerate(groups):
            optimize_group(board, g, weights, hcfg, seed=seed * 1000 + bi * 50 + gi)
            gid = f"{block_label(block).split(' ')[0]} g{gi + 1}" if len(groups) > 1 else block_label(block).split(' ')[0]
            if gid in groups_map:
                gid += f" ({block.split('-')[-1]})"
            groups_map[gid] = g
            group_block[gid] = block

    # Plusieurs ordres de pose : on garde celui qui laisse le moins de groupes sans place.
    snap1 = board.clone_positions()
    def _area(gid):
        b = board.global_bbox([r for r in groups_map[gid] if not board.components[r].fixed] or groups_map[gid])
        return (b[2] - b[0]) * (b[3] - b[1])
    best = None
    tried = []
    for k in range(n_orders):
        board.restore_positions(snap1)
        unfit_k = assemble_blocks(board, groups_map, weights, hcfg, seed=seed + k, order_noise=0.0 if k == 0 else 0.35)
        score = (len(unfit_k), sum(_area(g) for g in unfit_k), hpwl(board, board.nets))
        tried.append((k, len(unfit_k)))
        if best is None or score < best[0]:
            best = (score, k, board.clone_positions(), list(unfit_k))
    board.restore_positions(best[2])
    unfit = best[3]
    log = [f"Ordres essayes : {n_orders} ; groupes sans place par essai : {[n for _k, n in tried]} ; retenu : essai {best[1]} "
           f"({len(unfit)} groupe(s) sans place : {unfit})."]

    # Refaire la phase 1 des groupes sans place avec un but de forme (un trou restant de la carte).
    redone, failed = [], []
    for gid in sorted(unfit, key=_area, reverse=True):
        refs = groups_map[gid]
        need = sum((lambda b: (b[2] - b[0]) * (b[3] - b[1]))(board.components[r].world_bbox()) for r in refs)
        obstacles = []
        for g2, refs2 in groups_map.items():
            if g2 in unfit and g2 not in redone:
                continue
            free2 = [r for r in refs2 if not board.components[r].fixed]
            if any(board.components[r].fixed for r in refs2):
                obstacles += [board.components[r].world_bbox() for r in refs2]
            elif free2:
                obstacles.append(board.global_bbox(free2))
        obstacles += [c.world_bbox() for c in board.components.values() if c.fixed]
        holes = [h for h in free_rectangles(board, obstacles, k=12) if h[2] * h[3] >= need * 1.0]
        holes.sort(key=lambda h: h[2] * h[3])          # le plus petit trou qui convient
        done = False
        snap_g = {r: (board.components[r].x, board.components[r].y, board.components[r].rotation) for r in refs}
        for (hx, hy, hw, hh) in holes:
            ok, cst = optimize_group_in_box(board, refs, hw - 0.2, hh - 0.2, weights, hcfg, seed=seed * 7 + len(redone), restarts=30)
            if ok:
                for r in refs:
                    c = board.components[r]
                    c.x += hx + 0.1
                    c.y += hy + 0.1
                redone.append(gid)
                log.append(f"{gid} : phase 1 refaite pour un trou de {hw:.1f} x {hh:.1f} mm en ({hx:.1f} ; {hy:.1f}) : OK.")
                done = True
                break
        if not done:
            for r, (x, y, rot) in snap_g.items():
                c = board.components[r]
                c.x, c.y, c.rotation = x, y, rot
            failed.append(gid)
            log.append(f"{gid} : aucun trou ne convient ({len(holes)} trou(s) assez grand(s) essaye(s)) ; laisse en place.")

    all_refs = [r for g in groups_map.values() for r in g]
    cost = total_cost(board, all_refs, board.nets, weights)
    colors = block_colors(board)
    fig, ax = plt.subplots(figsize=(11, 11))
    if board.outline:
        ox0, oy0, ox1, oy1 = board.outline
        ax.add_patch(Rectangle((ox0, oy0), ox1 - ox0, oy1 - oy0, fill=False, edgecolor="black", linewidth=2.0, zorder=0))
    for p1, p2, _n in net_segments(board):
        ax.add_line(Line2D([p1[0], p2[0]], [p1[1], p2[1]], color="#999999", linewidth=0.3, alpha=0.6, zorder=1))
    for gid, refs in groups_map.items():
        col = colors[group_block[gid]]
        free = [r for r in refs if not board.components[r].fixed]
        boxes = [board.components[r].world_bbox() for r in (free or refs)]
        x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
        ax.add_patch(Rectangle((x0 - 0.3, y0 - 0.3), x1 - x0 + 0.6, y1 - y0 + 0.6, fill=True, facecolor=col, alpha=0.12,
                               edgecolor=col, linewidth=2.2, linestyle="--", zorder=1.5))
        for r in refs:
            c = board.components[r]
            bx0, by0, bx1, by1 = c.world_bbox()
            ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, facecolor="#bbbbbb" if c.fixed else col,
                                   edgecolor="black", linewidth=0.5, alpha=0.8, zorder=2, hatch="//" if c.fixed else None))
            if min(bx1 - bx0, by1 - by0) >= 1.6:
                ax.text((bx0 + bx1) / 2, (by0 + by1) / 2, r, ha="center", va="center", fontsize=5.5, zorder=3)
        ax.text(x0 - 0.2, y0 - 0.5, gid, fontsize=7, color=col, fontweight="bold", zorder=4)
    allb = [board.components[r].world_bbox() for r in all_refs]
    pad = 3.0
    ax.set_xlim(min(min(b[0] for b in allb), board.outline[0]) - pad, max(max(b[2] for b in allb), board.outline[2]) + pad)
    ax.set_ylim(max(max(b[3] for b in allb), board.outline[3]) + pad, min(min(b[1] for b in allb), board.outline[1]) - pad)
    ax.set_aspect("equal")
    ax.set_title(f"Phase 2 : rectangles de groupes poses sur la carte (contour noir ; pieces verrouillees hachurees)\n"
                 f"recouvrement {cost.overlap_mm2:.1f} mm2, hors contour {cost.out_of_bounds_mm2:.1f} mm2, "
                 f"cablage {cost.wirelength_mm:.0f} mm, croisements {cost.crossings}, "
                 f"depassement des regles {cost.decoupling_mm:.0f} mm", fontsize=9)
    fig.tight_layout()
    img = os.path.join(out_dir, "phase2_rectangles.png")
    fig.savefig(img, dpi=120)
    plt.close(fig)
    with open(os.path.join(out_dir, "phase2_rapport.md"), "w", encoding="utf-8") as f:
        f.write("# Phase 2 : rectangles de groupes sur la carte\n\n")
        f.write(chr(10).join(log) + chr(10) + chr(10))
        f.write(f"Recouvrement {cost.overlap_mm2:.2f} mm2, hors contour {cost.out_of_bounds_mm2:.2f} mm2, "
                f"cablage {cost.wirelength_mm:.0f} mm, croisements {cost.crossings}, regles {cost.decoupling_mm:.1f} mm.\n\n")
        for gid, refs in groups_map.items():
            f.write(f"- {gid} : {', '.join(sorted(refs))}\n")
    return img
