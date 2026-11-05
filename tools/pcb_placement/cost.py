"""Fonction de cout orientee routage : surface, longueur de cablage, congestion, croisements,
accessibilite des pastilles, estimation de vias ; plus les contraintes dures (recouvrement,
distance minimale) qui rejettent une solution plutot que d'etre simplement ponderees.

Toutes les fonctions prennent `board` deja place (positions/rotations a jour sur les
Component) et sont pensees pour etre rappelees a chaque iteration du recuit simule : pas
d'appel a pcbnew ni a KiCad ici (exigence d'independance du moteur pendant les calculs).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from .model import Board

Rect = Tuple[float, float, float, float]  # xmin, ymin, xmax, ymax


def rect_overlap_area(a: Rect, b: Rect) -> float:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    dx = min(ax1, bx1) - max(ax0, bx0)
    dy = min(ay1, by1) - max(ay0, by0)
    if dx <= 0 or dy <= 0:
        return 0.0
    return dx * dy


def inflate(r: Rect, margin: float) -> Rect:
    x0, y0, x1, y1 = r
    return (x0 - margin, y0 - margin, x1 + margin, y1 + margin)


def overlap_penalty(board: Board, refs: List[str], min_clearance_mm: float) -> float:
    """Somme des surfaces de recouvrement (mm^2) entre tous les rectangles d'encombrement
    des composants de `refs`, chacun gonfle de min_clearance_mm/2 (clearance partagee entre
    les deux composants). Contrainte dure : doit tendre vers 0, jamais simplement compensee
    par un meilleur score ailleurs (cf. total_cost)."""
    boxes = [inflate(board.components[r].world_bbox(), min_clearance_mm / 2.0) for r in refs]
    n = len(boxes)
    total = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            total += rect_overlap_area(boxes[i], boxes[j])
    return total


def out_of_bounds_penalty(board: Board, refs: List[str]) -> float:
    """Somme des surfaces (mm^2) de chaque composant qui tombent EN DEHORS du contour de
    carte fixe (board.outline), hors references exemptees (board.overhang_refs - debord
    mecanique deja decide, ex. connecteur batterie, antenne). Contrainte dure, meme principe
    que overlap_penalty : doit tendre vers 0. Retourne 0 si aucun contour n'est impose
    (board.outline is None, comportement d'origine : le moteur choisit la taille de carte)."""
    if board.outline is None:
        return 0.0
    total = 0.0
    for r in refs:
        if r in board.overhang_refs:
            continue
        comp = board.components[r]
        x0, y0, x1, y1 = comp.world_bbox()
        comp_area = max(x1 - x0, 0.0) * max(y1 - y0, 0.0)
        inside_area = rect_overlap_area((x0, y0, x1, y1), board.outline)
        total += max(comp_area - inside_area, 0.0)
    return total


def board_area(board: Board, refs: List[str], margin_mm: float = 1.0) -> float:
    x0, y0, x1, y1 = board.global_bbox(refs)
    w = max(x1 - x0 + 2 * margin_mm, 0.0)
    h = max(y1 - y0 + 2 * margin_mm, 0.0)
    return w * h


def hpwl(board: Board, nets: Dict[str, "Net"] | None = None) -> float:
    """Half-Perimeter Wire Length : pour chaque reseau de >= 2 pastilles, demi-perimetre de
    la boite englobante de ses pastilles. Proxy standard, rapide, independant du routage
    reel - utilise pour guider le placement, pas pour estimer la longueur finale des pistes."""
    nets = nets if nets is not None else board.nets
    total = 0.0
    for net in nets.values():
        if len(net.pins) < 2:
            continue
        xs, ys = [], []
        for ref, pad in net.pins:
            pos = board.pad_world_pos(ref, pad)
            if pos is None:
                continue
            xs.append(pos[0])
            ys.append(pos[1])
        if len(xs) < 2:
            continue
        total += (max(xs) - min(xs)) + (max(ys) - min(ys))
    return total


def _net_mst_edges(points: List[Tuple[float, float]]) -> List[Tuple[int, int]]:
    """Arbre couvrant minimal (Prim) sur une petite liste de points - approxime le trajet
    probable des pistes d'un reseau (mieux qu'une clique complete, moins cher a calculer que
    le vrai routage)."""
    n = len(points)
    if n < 2:
        return []
    in_tree = [False] * n
    in_tree[0] = True
    dist = [math.hypot(points[0][0] - p[0], points[0][1] - p[1]) for p in points]
    parent = [0] * n
    edges = []
    for _ in range(n - 1):
        best, best_d = -1, math.inf
        for i in range(n):
            if not in_tree[i] and dist[i] < best_d:
                best, best_d = i, dist[i]
        if best == -1:
            break
        in_tree[best] = True
        edges.append((parent[best], best))
        for i in range(n):
            if not in_tree[i]:
                d = math.hypot(points[best][0] - points[i][0], points[best][1] - points[i][1])
                if d < dist[i]:
                    dist[i] = d
                    parent[i] = best
    return edges


def net_segments(board: Board, nets: Dict[str, "Net"] | None = None) -> List[Tuple[Tuple[float, float], Tuple[float, float], str]]:
    """Segments (arbre couvrant minimal) approximant le trajet de chaque reseau. Utilise par
    la congestion et l'estimation de croisements."""
    nets = nets if nets is not None else board.nets
    segments = []
    for name, net in nets.items():
        pts, refs = [], []
        for ref, pad in net.pins:
            pos = board.pad_world_pos(ref, pad)
            if pos is None:
                continue
            pts.append(pos)
            refs.append(ref)
        if len(pts) < 2:
            continue
        for i, j in _net_mst_edges(pts):
            segments.append((pts[i], pts[j], name))
    return segments


def _segments_intersect(p1, p2, p3, p4) -> bool:
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return False


def crossing_count(segments) -> int:
    """Nombre de paires de segments (de reseaux DIFFERENTS) qui se croisent - proxy rapide
    des connexions difficiles / detours probables (un vrai routeur eviterait certains
    croisements par un via, d'ou le lien avec via_estimate)."""
    n = len(segments)
    count = 0
    for i in range(n):
        p1, p2, net_i = segments[i]
        for j in range(i + 1, n):
            p3, p4, net_j = segments[j]
            if net_i == net_j:
                continue
            if _segments_intersect(p1, p2, p3, p4):
                count += 1
    return count


def via_estimate(segments) -> int:
    """Estimation grossiere du nombre de vias necessaires : une piste qui croise une autre
    piste doit souvent descendre sur l'autre couche a un bout - on compte un via pour moitie
    des croisements detectes (une seule des deux pistes change de couche en general)."""
    return round(crossing_count(segments) / 2.0)


@dataclass
class CongestionGrid:
    grid: np.ndarray  # densite par cellule
    cell_mm: float
    x0: float
    y0: float

    def hot_cells(self, threshold: float) -> int:
        return int(np.sum(self.grid > threshold))

    def score(self) -> float:
        # Penalise les cellules tres chargees plus que lineairement (congestion reelle =
        # non-routable localement au-dela d'un seuil, pas juste "un peu plus lent").
        return float(np.sum(self.grid ** 2))


def congestion_grid(board: Board, refs: List[str], segments, cell_mm: float = 2.0) -> CongestionGrid:
    x0, y0, x1, y1 = board.global_bbox(refs)
    x0 -= cell_mm
    y0 -= cell_mm
    w = max(x1 - x0 + cell_mm, cell_mm)
    h = max(y1 - y0 + cell_mm, cell_mm)
    nx = max(1, int(math.ceil(w / cell_mm)))
    ny = max(1, int(math.ceil(h / cell_mm)))
    grid = np.zeros((ny, nx), dtype=float)

    def add_segment(p1, p2):
        length = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        steps = max(1, int(length / (cell_mm / 2.0)))
        for s in range(steps + 1):
            t = s / steps
            x = p1[0] + t * (p2[0] - p1[0])
            y = p1[1] + t * (p2[1] - p1[1])
            cx = int((x - x0) / cell_mm)
            cy = int((y - y0) / cell_mm)
            if 0 <= cx < nx and 0 <= cy < ny:
                grid[cy, cx] += 1.0 / (steps + 1)

    for p1, p2, _net in segments:
        add_segment(p1, p2)

    # Densite de composants (occupation physique, reduit l'espace de routage disponible).
    for r in refs:
        bx0, by0, bx1, by1 = board.components[r].world_bbox()
        cx0 = max(0, int((bx0 - x0) / cell_mm))
        cx1 = min(nx - 1, int((bx1 - x0) / cell_mm))
        cy0 = max(0, int((by0 - y0) / cell_mm))
        cy1 = min(ny - 1, int((by1 - y0) / cell_mm))
        if cx1 >= cx0 and cy1 >= cy0:
            grid[cy0:cy1 + 1, cx0:cx1 + 1] += 0.3

    return CongestionGrid(grid=grid, cell_mm=cell_mm, x0=x0, y0=y0)


def accessibility_penalty(board: Board, refs: List[str], probe_mm: float = 1.5) -> float:
    """Pour chaque pastille, verifie qu'il existe au moins une direction (haut/bas/gauche/
    droite) ou aucun AUTRE composant n'empiete sur une petite zone sonde autour de la
    pastille a `probe_mm` - sinon la pastille est consideree difficile d'acces (entouree)."""
    boxes = {r: board.components[r].world_bbox() for r in refs}
    penalty = 0.0
    directions = [(probe_mm, 0), (-probe_mm, 0), (0, probe_mm), (0, -probe_mm)]
    for r in refs:
        comp = board.components[r]
        for pad in comp.pads:
            px, py = comp.pad_world_pos(pad)
            free_dir = False
            for dx, dy in directions:
                probe = (px + dx - 0.2, py + dy - 0.2, px + dx + 0.2, py + dy + 0.2)
                blocked = False
                for other, box in boxes.items():
                    if other == r:
                        continue
                    if rect_overlap_area(probe, box) > 0:
                        blocked = True
                        break
                if not blocked:
                    free_dir = True
                    break
            if not free_dir:
                penalty += 1.0
    return penalty


def decoupling_excess(board: Board, rule: dict) -> float:
    """Depassement (mm) de la distance max entre un condensateur de decouplage et la broche
    d'alimentation de son circuit integre : centre du condensateur -> broche la plus proche
    parmi `rule["pins"]` (plusieurs broches candidates pour un groupe de condensateurs
    equivalents). 0 si le condensateur est assez proche, ou si la regle ne s'applique pas."""
    cap = board.components.get(rule["cap"])
    ic = board.components.get(rule["ic"])
    if cap is None or ic is None:
        return 0.0
    cx, cy = cap.world_center()
    best = None
    for p in ic.pads:
        if p.name in rule["pins"]:
            px, py = ic.pad_world_pos(p)
            d = math.hypot(px - cx, py - cy)
            if best is None or d < best:
                best = d
    if best is None:
        return 0.0
    return max(0.0, best - rule["dmax"])


def block_dispersion(board: Board, merge_split: bool = True):
    """Compacite des blocs : pour chaque bloc, distance RMS (mm) des centres de ses composants
    LIBRES a leur centre de gravite ; moyenne ponderee par le nombre de composants. Plus c'est
    petit, plus les blocs sont groupes. `merge_split=True` regroupe les sous-blocs d'un bloc
    decoupe par ancre (ex. DES-007 en -M1..-M4) sous le bloc d'origine (feuille DES) ; False les
    garde separes. Renvoie (dispersion moyenne, {bloc: dispersion})."""
    groups = {}
    for ref, c in board.components.items():
        if c.fixed:
            continue
        key = board.block_parent.get(c.block, c.block) if merge_split else c.block
        groups.setdefault(key, []).append(c.world_center())
    total, n, per = 0.0, 0, {}
    for key, pts in groups.items():
        if len(pts) < 2:
            continue
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        rms = math.sqrt(sum((p[0] - cx) ** 2 + (p[1] - cy) ** 2 for p in pts) / len(pts))
        per[key] = rms
        total += rms * len(pts)
        n += len(pts)
    return (total / n if n else 0.0), per


def decoupling_total(board: Board) -> float:
    return sum(decoupling_excess(board, r) for r in board.decoupling_rules)


@dataclass
class CostWeights:
    area: float = 1.0
    wirelength: float = 0.5
    congestion: float = 0.3
    crossings: float = 0.4
    accessibility: float = 0.2
    vias: float = 0.6
    min_clearance_mm: float = 0.3
    overlap_penalty_weight: float = 1000.0  # contrainte dure : poids ecrasant, pas un critere parmi d'autres
    decoupling: float = 0.0  # poids du depassement de distance de decouplage (mm), 0 = sans effet


@dataclass
class CostBreakdown:
    area_mm2: float
    wirelength_mm: float
    congestion: float
    crossings: int
    vias_estimate: int
    accessibility_penalty: float
    overlap_mm2: float
    out_of_bounds_mm2: float
    total: float
    feasible: bool
    decoupling_mm: float = 0.0  # depassement cumule des distances de decouplage (mm)
    dispersion_mm: float = 0.0  # dispersion moyenne des blocs (mm), cf. block_dispersion (information)


def is_better(candidate: "CostBreakdown", current_best: "CostBreakdown") -> bool:
    """Une solution FAISABLE (sans recouvrement) bat toujours une infaisable, quel que soit
    son cout total ; entre deux solutions de meme faisabilite, le cout total pondere
    tranche. Utilise partout ou on compare une nouvelle solution a la meilleure connue
    (annealing.run_annealing, hierarchy.run_global_annealing_with_block_moves,
    optimizer.run_strategy) pour ne jamais perdre le progres fait vers la faisabilite tant
    qu'aucune solution pleinement faisable n'a encore ete trouvee."""
    if candidate.feasible != current_best.feasible:
        return candidate.feasible
    return candidate.total < current_best.total


def total_cost(board: Board, refs: List[str], nets: Dict[str, "Net"], weights: CostWeights) -> CostBreakdown:
    overlap = overlap_penalty(board, refs, weights.min_clearance_mm)
    area = board_area(board, refs)
    wl = hpwl(board, nets)
    segs = net_segments(board, nets)
    crossings = crossing_count(segs)
    vias = via_estimate(segs)
    grid = congestion_grid(board, refs, segs)
    cong = grid.score()
    access = accessibility_penalty(board, refs)

    oob = out_of_bounds_penalty(board, refs)
    dec = decoupling_total(board)
    feasible = overlap <= 1e-6 and oob <= 1e-6
    total = (
        weights.area * area
        + weights.wirelength * wl
        + weights.congestion * cong
        + weights.crossings * crossings
        + weights.vias * vias
        + weights.accessibility * access
        + weights.decoupling * dec
        + weights.overlap_penalty_weight * (overlap + oob)
    )
    return CostBreakdown(
        area_mm2=area,
        wirelength_mm=wl,
        congestion=cong,
        crossings=crossings,
        vias_estimate=vias,
        accessibility_penalty=access,
        overlap_mm2=overlap,
        out_of_bounds_mm2=oob,
        total=total,
        feasible=feasible,
        decoupling_mm=dec,
    )
