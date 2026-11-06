"""Script d'EXPLORATION (pas le moteur de placement) pour construire `regle_decouplage.md` avec
l'utilisateur, cas par cas. Ne fait PAS partie du pipeline de production (`hierarchy.py`,
`place_active_and_decoupling`) : sert a generer des images de scenarios candidats, discutes puis
actes dans la regle. A CORRIGER directement ici au fil de la discussion plutot que de regenerer
du code ailleurs (demande utilisateur du 2026-11-06).

Usage :
    python tools/pcb_placement/exploration_decouplage.py

Sortie : images dans <TEMP>/resultats_placement/exploration/ (hors depot).

Etat actuel (2026-11-06) : cas 2 (C28+C34 sur la broche 36 de U1), etape "C34 colle a C28" -
genere les 12 combinaisons (2 positions de C28 [cas 1] x 3 bords libres x 2 styles). La derniere
version validee par l'utilisateur est la fonction `scenario_c34_contre_c28`.
"""
from __future__ import annotations

import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from pcb_placement.io_data import apply_active_rules, apply_decoupling, load_board
from pcb_placement.placement import _rotate_xy, _snap_cardinal
from pcb_placement.model import ALLOWED_ROTATIONS

OUT_DIR = os.path.join(os.environ.get("TEMP", "/tmp"), "resultats_placement", "exploration")
EXTRACT_JSON = os.path.join(os.environ.get("TEMP", "/tmp"), "resultats_placement", "extract.json")
DECOUPLING_FILE = os.path.join(REPO, "projets", "boomrone", "hardware", "kicad", "proj_boomrone", "decouplage.json")
RULES_FILE = os.path.join(REPO, "projets", "boomrone", "hardware", "kicad", "proj_boomrone", "regles_actives.json")
MARGIN_MM = 0.3


class Frame:
    """Repere dir/lateral autour d'une broche d'un composant actif (cf. regle_decouplage.md,
    principes generaux) : `dir` = de l'IC vers la broche, ramene a un axe cardinal ; `lat` =
    perpendiculaire. Tout le reste du script raisonne dans ce repere."""

    def __init__(self, ic, pin: str):
        self.ic = ic
        self.pin = pin
        self.ic_cx, self.ic_cy = ic.world_center()
        self.ic_hw, self.ic_hh = ic.world_half_extents()
        pad = next(p for p in ic.pads if p.name == pin)
        self.px, self.py = ic.pad_world_pos(pad)
        self.dirx, self.diry = _snap_cardinal(self.px - self.ic_cx, self.py - self.ic_cy)
        self.latx, self.laty = -self.diry, self.dirx
        self.ic_half_dir = self.ic_hw if abs(self.dirx) >= abs(self.diry) else self.ic_hh
        self.pin_depth = (self.px - self.ic_cx) * self.dirx + (self.py - self.ic_cy) * self.diry
        self.pin_lateral = (self.px - self.ic_cx) * self.latx + (self.py - self.ic_cy) * self.laty


def _power_pad(cap):
    return next(p for p in cap.pads if p.net == "+3V0")


def _other_pad(cap, power_pad):
    return next(p for p in cap.pads if p is not power_pad)


def place_cap1_on_pin(cap, frame: Frame, mode: int) -> None:
    """Cas 1 (regle_decouplage.md) : pose `cap` seul sur la broche de `frame`.
    mode=1 : position 1 (petit cote colle). mode=2 : position 2a (grand cote colle)."""
    pp = _power_pad(cap)
    op = _other_pad(cap, pp)
    dirx, diry, latx, laty = frame.dirx, frame.diry, frame.latx, frame.laty
    if mode == 1:
        def sc(rot):
            pox, poy = _rotate_xy(pp.local_x, pp.local_y, rot)
            oox, ooy = _rotate_xy(op.local_x, op.local_y, rot)
            return (oox - pox) * dirx + (ooy - poy) * diry
    else:
        def sc(rot):
            pox, poy = _rotate_xy(pp.local_x, pp.local_y, rot)
            oox, ooy = _rotate_xy(op.local_x, op.local_y, rot)
            return abs((oox - pox) * latx + (ooy - poy) * laty)
    rot = max(ALLOWED_ROTATIONS, key=sc)
    cap.rotation = rot
    pox, poy = _rotate_xy(pp.local_x, pp.local_y, rot)
    cox, coy = _rotate_xy(cap.courtyard_offset_x, cap.courtyard_offset_y, rot)
    pad_off_x, pad_off_y = pox - cox, poy - coy
    pad_depth_offset = pad_off_x * dirx + pad_off_y * diry
    pad_lateral_offset = pad_off_x * latx + pad_off_y * laty
    hw, hh = cap.world_half_extents()
    half_depth = hw if abs(dirx) >= abs(diry) else hh
    center_depth_min = frame.ic_half_dir + half_depth + MARGIN_MM
    if mode == 1:
        center_depth = max(center_depth_min, frame.pin_depth - pad_depth_offset)
    else:
        center_depth = center_depth_min
    center_lateral = frame.pin_lateral - pad_lateral_offset
    cap.x = frame.ic_cx + dirx * center_depth + latx * center_lateral - cox
    cap.y = frame.ic_cy + diry * center_depth + laty * center_lateral - coy


def place_touching(cap_fixed, cap_new, frame: Frame, edge_name: str, style: str) -> None:
    """Pose `cap_new` EN CONTACT (marge minimale, jamais plus loin) avec le bord `edge_name`
    ('E' = loin de l'IC, 'N'/'S' = lateral - 'O'/vers l'IC n'est jamais teste, deja occupe) de
    `cap_fixed`, vise la PASTILLE de `cap_fixed` (jamais son centre) le long du bord. `style` :
    'petit_cote' (axe des pastilles de `cap_new` perpendiculaire au bord) ou 'grand_cote'
    (parallele au bord)."""
    dirx, diry, latx, laty = frame.dirx, frame.diry, frame.latx, frame.laty
    if edge_name == "E":
        ndx, ndy = dirx, diry
    elif edge_name == "N":
        ndx, ndy = -latx, -laty
    elif edge_name == "S":
        ndx, ndy = latx, laty
    else:
        raise ValueError(f"bord non teste : {edge_name}")
    tdx, tdy = -ndy, ndx

    fixed_box = cap_fixed.world_bbox()
    corners = [(fixed_box[0], fixed_box[1]), (fixed_box[2], fixed_box[1]),
               (fixed_box[2], fixed_box[3]), (fixed_box[0], fixed_box[3])]
    edge_n = max(cx * ndx + cy * ndy for cx, cy in corners)

    pp_fixed = _power_pad(cap_fixed)
    target = cap_fixed.pad_world_pos(pp_fixed)
    target_t = target[0] * tdx + target[1] * tdy

    pp_new = _power_pad(cap_new)
    op_new = _other_pad(cap_new, pp_new)
    if style == "petit_cote":
        def sc(rot):
            pox, poy = _rotate_xy(pp_new.local_x, pp_new.local_y, rot)
            oox, ooy = _rotate_xy(op_new.local_x, op_new.local_y, rot)
            return (oox - pox) * ndx + (ooy - poy) * ndy
    elif style == "grand_cote":
        def sc(rot):
            pox, poy = _rotate_xy(pp_new.local_x, pp_new.local_y, rot)
            oox, ooy = _rotate_xy(op_new.local_x, op_new.local_y, rot)
            return abs((oox - pox) * tdx + (ooy - poy) * tdy)
    else:
        raise ValueError(f"style non reconnu : {style}")
    rot = max(ALLOWED_ROTATIONS, key=sc)
    cap_new.rotation = rot
    pox, poy = _rotate_xy(pp_new.local_x, pp_new.local_y, rot)
    cox, coy = _rotate_xy(cap_new.courtyard_offset_x, cap_new.courtyard_offset_y, rot)
    pad_off_n = (pox - cox) * ndx + (poy - coy) * ndy
    pad_off_t = (pox - cox) * tdx + (poy - coy) * tdy
    hw, hh = cap_new.world_half_extents()
    half_n = hw if abs(ndx) >= abs(ndy) else hh

    center_n = edge_n + MARGIN_MM + half_n
    center_t = target_t - pad_off_t
    center_x = center_n * ndx + center_t * tdx
    center_y = center_n * ndy + center_t * tdy
    cap_new.x, cap_new.y = center_x - cox, center_y - coy


def overlaps(a, b, m=0.0) -> bool:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    return ax0 - m < bx1 and bx0 - m < ax1 and ay0 - m < by1 and by0 - m < ay1


def pin_distance(cap, pin_xy) -> float:
    pw = cap.pad_world_pos(_power_pad(cap))
    return ((pw[0] - pin_xy[0]) ** 2 + (pw[1] - pin_xy[1]) ** 2) ** 0.5


def cap_distance(cap_a, cap_b) -> float:
    pa = cap_a.pad_world_pos(_power_pad(cap_a))
    pb = cap_b.pad_world_pos(_power_pad(cap_b))
    return ((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2) ** 0.5


def scenario_c34_contre_c28(board, out_name: str = "c34_vs_c28.png") -> None:
    """Etat actuel (2026-11-06), valide par l'utilisateur comme bon balayage pour cette etape :
    C34 colle a C28, pour les 2 positions de C28 (cas 1) x 3 bords libres x 2 styles."""
    u1 = board.components["U1"]
    c28 = board.components["C28"]
    c34 = board.components["C34"]
    frame = Frame(u1, "36")

    c28_modes = [("C28 position 1 (petit cote)", 1), ("C28 position 2a (grand cote)", 2)]
    edges = [("nord", "N"), ("sud", "S"), ("est", "E")]
    styles = ["petit_cote", "grand_cote"]

    results = []
    for c28_label, c28_mode in c28_modes:
        place_cap1_on_pin(c28, frame, c28_mode)
        c28_box = c28.world_bbox()
        for edge_label, edge in edges:
            for style in styles:
                place_touching(c28, c34, frame, edge, style)
                bad = (overlaps(c34.world_bbox(), c28_box, MARGIN_MM - 0.01)
                       or overlaps(c34.world_bbox(), u1.world_bbox(), -0.01))
                d_cap = cap_distance(c28, c34)
                d_pin = pin_distance(c34, (frame.px, frame.py))
                results.append({
                    "label": f"{c28_label} / {edge_label}, {style}",
                    "d_cap": d_cap, "d_pin": d_pin, "bad": bad,
                    "snap28": (c28.x, c28.y, c28.rotation),
                    "snap34": (c34.x, c34.y, c34.rotation),
                })

    for r in results:
        flag = " [RECOUVREMENT]" if r["bad"] else ""
        print(f"{r['label']:45s} C28-C34={r['d_cap']:.2f} mm  C34-broche={r['d_pin']:.2f} mm{flag}")

    n = len(results)
    cols = 4
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4.6 * cols, 4.6 * rows), squeeze=False)
    for i, r in enumerate(results):
        ax = axes[i // cols][i % cols]
        c28.x, c28.y, c28.rotation = r["snap28"]
        c34.x, c34.y, c34.rotation = r["snap34"]
        ux0, uy0, ux1, uy1 = u1.world_bbox()
        ax.add_patch(Rectangle((ux0, uy0), ux1 - ux0, uy1 - uy0, facecolor="#0072B2", edgecolor="black", alpha=0.6, zorder=1))
        ax.plot(frame.px, frame.py, "o", color="red", markersize=6, zorder=5)
        for c in (c28, c34):
            pp = _power_pad(c)
            bx0, by0, bx1, by1 = c.world_bbox()
            ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, facecolor="#E69F00", edgecolor="black", linewidth=1.0, zorder=3))
            for p in c.pads:
                wx, wy = c.pad_world_pos(p)
                col = "red" if p is pp else "black"
                ax.plot(wx, wy, ".", color=col, markersize=10, zorder=4)
            ax.annotate(c.ref, c.world_center(), ha="center", va="center", fontsize=6.5, zorder=6)
        col_title = "red" if r["bad"] else "black"
        ax.set_title(f"{r['label']}\nC28-C34 {r['d_cap']:.2f}, broche {r['d_pin']:.2f} mm", fontsize=7.5, color=col_title)
        ax.set_xlim(frame.px - 6, frame.px + 6)
        ax.set_ylim(frame.py + 6, frame.py - 6)
        ax.set_aspect("equal")
        ax.tick_params(labelsize=6)
    for k in range(n, rows * cols):
        axes[k // cols][k % cols].axis("off")
    fig.suptitle("C34 colle a C28 (3 bords x 2 styles), pour les 2 positions de C28", fontsize=11)
    fig.tight_layout()
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, out_name)
    fig.savefig(out, dpi=110)
    plt.close(fig)
    print("saved", out)


def scenario_cap_seul(board, ic_ref: str, cap_ref: str, pin: str, out_name: str | None = None) -> None:
    """Cas 1 (regle_decouplage.md) : un condensateur seul, les 3 positions candidates (position 1,
    2a, 2b), departagees par la distance pastille -> broche. Generalise ce qui a ete valide a la
    main sur C32/U1 et C28/U1 (2026-11-06)."""
    ic = board.components[ic_ref]
    cap = board.components[cap_ref]
    frame = Frame(ic, pin)
    pp, op = _power_pad(cap), _other_pad(cap, _power_pad(cap))

    def score2(rot):
        pox, poy = _rotate_xy(pp.local_x, pp.local_y, rot)
        oox, ooy = _rotate_xy(op.local_x, op.local_y, rot)
        return abs((oox - pox) * frame.latx + (ooy - poy) * frame.laty)
    best2 = max(ALLOWED_ROTATIONS, key=score2)

    scenarios = [("Position 1 : petit cote colle", 1, None),
                 ("Position 2a : grand cote colle, allonge d un cote", 2, best2),
                 ("Position 2b : grand cote colle, allonge de l autre cote", 2, (best2 + 180) % 360)]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (title, mode, forced_rot) in zip(axes, scenarios):
        if forced_rot is None:
            place_cap1_on_pin(cap, frame, mode)
        else:
            # position 2b : meme construction que 2a, rotation imposee (symetrique).
            place_cap1_on_pin(cap, frame, mode)
            cap.rotation = forced_rot
            pox, poy = _rotate_xy(pp.local_x, pp.local_y, forced_rot)
            cox, coy = _rotate_xy(cap.courtyard_offset_x, cap.courtyard_offset_y, forced_rot)
            pad_lateral_offset = (pox - cox) * frame.latx + (poy - coy) * frame.laty
            hw, hh = cap.world_half_extents()
            half_depth = hw if abs(frame.dirx) >= abs(frame.diry) else hh
            center_depth = frame.ic_half_dir + half_depth + MARGIN_MM
            center_lateral = frame.pin_lateral - pad_lateral_offset
            cap.x = frame.ic_cx + frame.dirx * center_depth + frame.latx * center_lateral - cox
            cap.y = frame.ic_cy + frame.diry * center_depth + frame.laty * center_lateral - coy

        ux0, uy0, ux1, uy1 = ic.world_bbox()
        ax.add_patch(Rectangle((ux0, uy0), ux1 - ux0, uy1 - uy0, facecolor="#0072B2", edgecolor="black", alpha=0.6, zorder=1))
        ax.plot(frame.px, frame.py, "o", color="red", markersize=7, zorder=5)
        ax.annotate(f"broche {pin}", (frame.px, frame.py), textcoords="offset points", xytext=(6, -10), fontsize=8, color="red")
        bx0, by0, bx1, by1 = cap.world_bbox()
        ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, facecolor="#E69F00", edgecolor="black", linewidth=1.2, zorder=3))
        for p in cap.pads:
            wx, wy = cap.pad_world_pos(p)
            col = "red" if p is pp else "black"
            ax.plot(wx, wy, ".", color=col, markersize=14, zorder=4)
        dist = pin_distance(cap, (frame.px, frame.py))
        ax.set_title(f"{title}\n(distance : {dist:.2f} mm)", fontsize=9)
        ax.set_xlim(frame.px - 5, frame.px + 5)
        ax.set_ylim(frame.py + 5, frame.py - 5)
        ax.set_aspect("equal")
        ax.tick_params(labelsize=7)
    fig.suptitle(f"{cap_ref} seul ({ic_ref}, broche {pin}) : 3 positions candidates", fontsize=11)
    fig.tight_layout()
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, out_name or f"{cap_ref.lower()}_seul_3positions.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print("saved", out)


def scenario_c34_au_plus_pres(board, out_name: str = "c34_au_plus_pres.png") -> None:
    """C34 pose contre C28 deja fixe (position 1, cf. `scenario_une_capa_seule`) : toutes les
    combinaisons (3 bords libres x 2 styles, cf. `place_touching`) sont essayees, celles qui
    provoquent un recouvrement sont ecartees, et C34 est POSE a la combinaison qui minimise sa
    distance pastille -> broche ("au plus pres", demande utilisateur du 2026-11-06). Une seule
    image produite (le resultat retenu), pas la grille des 12 (rejetee precedemment) - le detail
    de chaque combinaison essayee est imprime sur la console pour tracabilite."""
    u1 = board.components["U1"]
    c28 = board.components["C28"]
    c34 = board.components["C34"]
    frame = Frame(u1, "36")
    place_cap1_on_pin(c28, frame, 1)
    c28_box = c28.world_bbox()

    edges = [("nord", "N"), ("sud", "S"), ("est", "E")]
    styles = ["petit_cote", "grand_cote"]
    candidates = []
    for edge_label, edge in edges:
        for style in styles:
            place_touching(c28, c34, frame, edge, style)
            bad = (overlaps(c34.world_bbox(), c28_box, MARGIN_MM - 0.01)
                   or overlaps(c34.world_bbox(), u1.world_bbox(), -0.01))
            d_pin = pin_distance(c34, (frame.px, frame.py))
            candidates.append({
                "label": f"{edge_label}, {style}", "d_pin": d_pin, "bad": bad,
                "snap34": (c34.x, c34.y, c34.rotation),
            })

    for c in candidates:
        flag = " [RECOUVREMENT]" if c["bad"] else ""
        print(f"{c['label']:25s} C34-broche={c['d_pin']:.2f} mm{flag}")

    valid = [c for c in candidates if not c["bad"]]
    if not valid:
        raise RuntimeError("aucune combinaison sans recouvrement pour C34 contre C28")
    best = min(valid, key=lambda c: c["d_pin"])
    c34.x, c34.y, c34.rotation = best["snap34"]
    print(f"retenu : {best['label']} (C34-broche={best['d_pin']:.2f} mm)")

    fig, ax = plt.subplots(figsize=(6, 6))
    ux0, uy0, ux1, uy1 = u1.world_bbox()
    ax.add_patch(Rectangle((ux0, uy0), ux1 - ux0, uy1 - uy0, facecolor="#0072B2", edgecolor="black", alpha=0.6, zorder=1))
    ax.plot(frame.px, frame.py, "o", color="red", markersize=8, zorder=5)
    ax.annotate("broche 36", (frame.px, frame.py), textcoords="offset points", xytext=(6, -10), fontsize=9, color="red")
    for c in (c28, c34):
        pp = _power_pad(c)
        bx0, by0, bx1, by1 = c.world_bbox()
        ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, facecolor="#E69F00", edgecolor="black", linewidth=1.2, zorder=3))
        for p in c.pads:
            wx, wy = c.pad_world_pos(p)
            col = "red" if p is pp else "black"
            ax.plot(wx, wy, ".", color=col, markersize=14, zorder=4)
        ax.annotate(c.ref, c.world_center(), ha="center", va="center", fontsize=10, zorder=6)
    ax.set_title(f"C28 (position 1) + C34 au plus pres ({best['label']}, {best['d_pin']:.2f} mm)", fontsize=9.5)
    ax.set_xlim(frame.px - 6, frame.px + 6)
    ax.set_ylim(frame.py + 6, frame.py - 6)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, out_name)
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print("saved", out)


def scenario_c34_toutes_options(board, out_name: str = "c34_toutes_options.png") -> None:
    """C34 contre C28 deja fixe (position 1) : calcule TOUTES les combinaisons valables (3 bords
    libres x 2 styles, cf. `place_touching`) puis NE GARDE POUR L'IMAGE que celles dont la
    distance pastille C28 -> pastille C34 (`cap_distance`, pas la distance a la broche) est la
    plus courte (demande utilisateur du 2026-11-06 : "on ne garde que les cas qui donne les
    distance entre pin de capa les plus courte"). Toutes les combinaisons restent imprimees sur
    la console (gardees ou non) pour tracabilite ; la liste jamais reduite a un seul resultat
    auto-choisi (demande precedente du 2026-11-06 : "montre moi toutes les possibilites
    TOUJOURS") - ici "toutes" = toutes celles qui partagent le minimum, pas une seule."""
    u1 = board.components["U1"]
    c28 = board.components["C28"]
    c34 = board.components["C34"]
    frame = Frame(u1, "36")
    place_cap1_on_pin(c28, frame, 1)
    c28_box = c28.world_bbox()

    edges = [("nord", "N"), ("sud", "S"), ("est", "E")]
    styles = ["petit_cote", "grand_cote"]
    results = []
    for edge_label, edge in edges:
        for style in styles:
            place_touching(c28, c34, frame, edge, style)
            bad = (overlaps(c34.world_bbox(), c28_box, MARGIN_MM - 0.01)
                   or overlaps(c34.world_bbox(), u1.world_bbox(), -0.01))
            d_pin = pin_distance(c34, (frame.px, frame.py))
            d_cap = cap_distance(c28, c34)
            results.append({
                "label": f"{edge_label}, {style}", "d_pin": d_pin, "d_cap": d_cap, "bad": bad,
                "snap34": (c34.x, c34.y, c34.rotation),
            })

    valid = [r for r in results if not r["bad"]]
    d_cap_min = min(r["d_cap"] for r in valid)
    # Seuil de tolerance (pas un minimum strict) : garde tout cas "sensiblement" aussi proche du
    # minimum, pas seulement l'egalite exacte - demande utilisateur du 2026-11-06 ("le script
    # devrait retourner 4 cas alors pas 2") : nord/sud x petit_cote/grand_cote sont tous proches
    # (1,73 a 1,76 mm) et doivent rester, seuls les cas cote est (3,26/3,28 mm, nettement plus
    # loin) doivent etre ecartes. 20 % du minimum separe nettement les deux groupes ici ; valeur
    # provisoire, a ajuster si un futur cas la met en defaut.
    REL_MARGIN = 0.20
    for r in results:
        r["kept"] = (not r["bad"]) and r["d_cap"] <= d_cap_min * (1 + REL_MARGIN)

    for r in results:
        flag = " [RECOUVREMENT]" if r["bad"] else (" [retenu]" if r["kept"] else " [ecarte]")
        print(f"{r['label']:25s} C28-C34={r['d_cap']:.2f} mm  C34-broche={r['d_pin']:.2f} mm{flag}")

    kept = [r for r in results if r["kept"]]
    n = len(kept)
    cols = min(3, n)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4.8 * cols, 4.8 * rows), squeeze=False)
    for i, r in enumerate(kept):
        ax = axes[i // cols][i % cols]
        c34.x, c34.y, c34.rotation = r["snap34"]
        ux0, uy0, ux1, uy1 = u1.world_bbox()
        ax.add_patch(Rectangle((ux0, uy0), ux1 - ux0, uy1 - uy0, facecolor="#0072B2", edgecolor="black", alpha=0.6, zorder=1))
        ax.plot(frame.px, frame.py, "o", color="red", markersize=6, zorder=5)
        for c in (c28, c34):
            pp = _power_pad(c)
            bx0, by0, bx1, by1 = c.world_bbox()
            ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, facecolor="#E69F00", edgecolor="black", linewidth=1.0, zorder=3))
            for p in c.pads:
                wx, wy = c.pad_world_pos(p)
                col = "red" if p is pp else "black"
                ax.plot(wx, wy, ".", color=col, markersize=10, zorder=4)
            ax.annotate(c.ref, c.world_center(), ha="center", va="center", fontsize=7, zorder=6)
        col_title = "red" if r["bad"] else "black"
        ax.set_title(f"{r['label']}\nC34-broche {r['d_pin']:.2f} mm", fontsize=9, color=col_title)
        ax.set_xlim(frame.px - 6, frame.px + 6)
        ax.set_ylim(frame.py + 6, frame.py - 6)
        ax.set_aspect("equal")
        ax.tick_params(labelsize=7)
    for k in range(n, rows * cols):
        axes[k // cols][k % cols].axis("off")
    fig.suptitle(f"C28 (position 1, fixe) + C34 : combinaisons a distance C28-C34 minimale ({d_cap_min:.2f} mm)", fontsize=11.5)
    fig.tight_layout()
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, out_name)
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print("saved", out)


def _draw_panel(ax, ic, px, py, pin_label, caps, title) -> None:
    """Dessine un panneau (IC, broche ciblee, un ou plusieurs condensateurs DEJA positionnes -
    cap.x/y/rotation doivent etre regles avant l'appel) - factorise pour que tous les cas tiennent
    sur une seule image cote a cote (demande utilisateur du 2026-11-06 : "je veux tous les cas sur
    la meme page")."""
    ux0, uy0, ux1, uy1 = ic.world_bbox()
    ax.add_patch(Rectangle((ux0, uy0), ux1 - ux0, uy1 - uy0, facecolor="#0072B2", edgecolor="black", alpha=0.6, zorder=1))
    ax.plot(px, py, "o", color="red", markersize=7, zorder=5)
    ax.annotate(pin_label, (px, py), textcoords="offset points", xytext=(5, -9), fontsize=7.5, color="red")
    for cap in caps:
        pp = _power_pad(cap)
        bx0, by0, bx1, by1 = cap.world_bbox()
        ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, facecolor="#E69F00", edgecolor="black", linewidth=1.1, zorder=3))
        for p in cap.pads:
            wx, wy = cap.pad_world_pos(p)
            col = "red" if p is pp else "black"
            ax.plot(wx, wy, ".", color=col, markersize=11, zorder=4)
        ax.annotate(cap.ref, cap.world_center(), ha="center", va="center", fontsize=7.5, zorder=6)
    ax.set_title(title, fontsize=8.5)
    ax.set_xlim(px - 5.5, px + 5.5)
    ax.set_ylim(py + 5.5, py - 5.5)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=6.5)


def _single_cap_cases(ic, cap, pin: str):
    """Cas 1 generalise (cf. `scenario_cap_seul`) : calcule les 3 positions candidates d'UN
    condensateur seul sur une broche, SANS dessiner - retourne (frame, [(title, snap, dist), ...])
    pour composition dans une page a plusieurs broches."""
    frame = Frame(ic, pin)
    pp, op = _power_pad(cap), _other_pad(cap, _power_pad(cap))

    def score2(rot):
        pox, poy = _rotate_xy(pp.local_x, pp.local_y, rot)
        oox, ooy = _rotate_xy(op.local_x, op.local_y, rot)
        return abs((oox - pox) * frame.latx + (ooy - poy) * frame.laty)
    best2 = max(ALLOWED_ROTATIONS, key=score2)

    scenarios = [(f"{cap.ref} position 1", 1, None),
                 (f"{cap.ref} position 2a", 2, best2),
                 (f"{cap.ref} position 2b", 2, (best2 + 180) % 360)]
    cases = []
    for title, mode, forced_rot in scenarios:
        place_cap1_on_pin(cap, frame, mode)
        if forced_rot is not None:
            cap.rotation = forced_rot
            pox, poy = _rotate_xy(pp.local_x, pp.local_y, forced_rot)
            cox, coy = _rotate_xy(cap.courtyard_offset_x, cap.courtyard_offset_y, forced_rot)
            pad_lateral_offset = (pox - cox) * frame.latx + (poy - coy) * frame.laty
            hw, hh = cap.world_half_extents()
            half_depth = hw if abs(frame.dirx) >= abs(frame.diry) else hh
            center_depth = frame.ic_half_dir + half_depth + MARGIN_MM
            center_lateral = frame.pin_lateral - pad_lateral_offset
            cap.x = frame.ic_cx + frame.dirx * center_depth + frame.latx * center_lateral - cox
            cap.y = frame.ic_cy + frame.diry * center_depth + frame.laty * center_lateral - coy
        dist = pin_distance(cap, (frame.px, frame.py))
        cases.append((title, (cap.x, cap.y, cap.rotation), dist))
    return frame, cases


def _filter_largest_gap(items, key):
    """Ne garde que le groupe de valeurs le plus proche : trie par `key`, trouve le plus grand
    "saut" entre deux valeurs consecutives, et ecarte tout ce qui est apres ce saut (demande
    utilisateur du 2026-11-06 : "il y a des cas en trop... quand il y a un gros saut entre les
    solutions il faut ignorer les lointaines"). Avec 1 seul item, rien a filtrer."""
    if len(items) <= 1:
        return items
    ordered = sorted(items, key=key)
    keys = [key(it) for it in ordered]
    gaps = [keys[i + 1] - keys[i] for i in range(len(keys) - 1)]
    cut = max(range(len(gaps)), key=lambda i: gaps[i]) + 1
    return ordered[:cut]


def _pair_cap_cases(ic, cap_fixed, cap_new, pin: str):
    """Cas 2 generalise (cf. `scenario_c34_toutes_options`) : `cap_fixed` essaie SES 3 positions
    du cas 1 (position 1, 2a, 2b - pas seulement la position 1, demande utilisateur du
    2026-11-06 : "C28 et C34 a aussi plusieurs position. je devrai avoir plus que 9 possibilite"),
    et pour CHACUNE, `cap_new` colle contre lui (3 bords x 2 styles) : 3 x 6 = 18 combinaisons
    essayees. Dans chaque groupe (une position fixe de `cap_fixed`), ne garde que le sous-groupe
    de distances le plus proche, coupe au plus grand saut (`_filter_largest_gap` - demande
    utilisateur du 2026-11-06, qui annule le "toutes les combinaisons sans filtrage" essaye juste
    avant : la encore trop de cas, mais cette fois le critere est le saut de distance, pas un seuil
    fixe). Retourne (frame, [(label, snap_fixed, snap_new, d_cap), ...])."""
    frame, fixed_cases = _single_cap_cases(ic, cap_fixed, pin)
    edges = [("nord", "N"), ("sud", "S"), ("est", "E")]
    styles = ["petit_cote", "grand_cote"]
    all_valid = []
    for fixed_title, fixed_snap, _fixed_dist in fixed_cases:
        cap_fixed.x, cap_fixed.y, cap_fixed.rotation = fixed_snap
        fixed_box = cap_fixed.world_bbox()
        group = []
        for edge_label, edge in edges:
            for style in styles:
                place_touching(cap_fixed, cap_new, frame, edge, style)
                bad = (overlaps(cap_new.world_bbox(), fixed_box, MARGIN_MM - 0.01)
                       or overlaps(cap_new.world_bbox(), ic.world_bbox(), -0.01))
                d_cap = cap_distance(cap_fixed, cap_new)
                if not bad:
                    group.append({"label": f"{edge_label}, {style}", "d_cap": d_cap,
                                   "snap_new": (cap_new.x, cap_new.y, cap_new.rotation)})
        kept = _filter_largest_gap(group, key=lambda g: g["d_cap"])
        for g in kept:
            all_valid.append((f"{fixed_title} / {g['label']}", fixed_snap, g["snap_new"], g["d_cap"]))
    return frame, all_valid


def _draw_panel_full(ax, ic, caps, title, pins=(), links=(), margin: float = 1.0) -> None:
    """Comme `_draw_panel`, mais dessine TOUS les condensateurs passes (pas seulement ceux de la
    broche en cours) et cadre la vue sur l'ensemble IC + condensateurs - demande utilisateur du
    2026-11-06 ("je veux voir toutes les capa a chaque vignette") : chaque vignette doit montrer
    le placement complet des 8 condensateurs du MCU, pas juste ceux de la broche variee dans cette
    vignette. `pins` : liste de (px, py, label) - point rouge sur CHAQUE broche ciblee du composant
    actif, retire par erreur en generalisant la vue (demande utilisateur du 2026-11-06 : "il manque
    les points rouge pour le composant actif"). `links` : liste de ((x1,y1), (x2,y2)) - trait rouge
    fin entre chaque broche et le point d'interet (pastille d'alimentation) du condensateur associe
    (demande utilisateur du 2026-11-06 : "il faut tracer un leger trait rouge entre les broches et
    pins qui montre quelle distance et le point d'interet" ; la valeur chiffree sur le trait a
    ensuite ete retiree - "il ne faut pas ecrire la valeur, juste le trait rouge")."""
    ux0, uy0, ux1, uy1 = ic.world_bbox()
    x0, y0, x1, y1 = ux0, uy0, ux1, uy1
    ax.add_patch(Rectangle((ux0, uy0), ux1 - ux0, uy1 - uy0, facecolor="#0072B2", edgecolor="black", alpha=0.6, zorder=1))
    for (x1l, y1l), (x2l, y2l) in links:
        ax.plot([x1l, x2l], [y1l, y2l], "-", color="red", linewidth=0.7, alpha=0.55, zorder=2)
    for px, py, pin_label in pins:
        ax.plot(px, py, "o", color="red", markersize=6, zorder=5)
        ax.annotate(pin_label, (px, py), textcoords="offset points", xytext=(5, -8), fontsize=6.5, color="red", zorder=6)
    for cap in caps:
        pp = _power_pad(cap)
        bx0, by0, bx1, by1 = cap.world_bbox()
        x0, y0, x1, y1 = min(x0, bx0), min(y0, by0), max(x1, bx1), max(y1, by1)
        ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, facecolor="#E69F00", edgecolor="black", linewidth=0.9, zorder=3))
        for p in cap.pads:
            wx, wy = cap.pad_world_pos(p)
            col = "red" if p is pp else "black"
            ax.plot(wx, wy, ".", color=col, markersize=7, zorder=4)
        ax.annotate(cap.ref, cap.world_center(), ha="center", va="center", fontsize=6, zorder=6)
    ax.set_title(title, fontsize=8)
    ax.set_xlim(x0 - margin, x1 + margin)
    ax.set_ylim(y1 + margin, y0 - margin)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=6)


def _chain_cap_cases(ic, pin: str, caps_chain: list):
    """Methode en CHAINE (demande utilisateur du 2026-11-06, en reaction a des chevauchements
    constates avec l'approche precedente "groupes independants + defauts") : "on pose la 1ere
    capa (x combinaison), on pose la 2eme capa a cote des x combinaison ce qui donne Y nouvelle
    combinaison, on pose la x eme capa a cote ... etc, toujours en minimisant les distances des
    pin actives et en ignorant dans le nouveau lot de combinaison les 'saut' de distance."

    `caps_chain` : condensateurs dans l'ordre de pose. Le premier utilise le cas 1 (3 positions,
    cf. `_single_cap_cases`). Chaque suivant est colle contre N'IMPORTE LEQUEL des condensateurs
    deja poses dans CETTE branche (jamais contre un condensateur d'une autre branche - c'est ce
    qui garantit l'absence de chevauchement, contrairement a l'ancienne methode qui combinait des
    groupes calcules independamment), teste sur 3 bords x 2 styles par reference, filtre par
    recouvrement (IC + TOUS les condensateurs deja poses dans la branche) puis par le plus grand
    saut de distance (`_filter_largest_gap`, distance = la plus courte vers un condensateur deja
    pose dans la branche). Retourne (frame, [{"snaps": [(cap, snap), ...], "label": str,
    "links": [(a, b), ...]}, ...]) - une entree par combinaison finale, chacune complete et
    coherente (prete a etre dessinee telle quelle, sans superposition possible)."""
    frame = Frame(ic, pin)
    first = caps_chain[0]
    _, first_cases = _single_cap_cases(ic, first, pin)
    results = [{"snaps": [(first, snap)], "label": title, "links": [("broche", first.ref)]}
               for title, snap, _dist in first_cases]

    edges = [("nord", "N"), ("sud", "S"), ("est", "E")]
    styles = ["petit_cote", "grand_cote"]
    for nxt in caps_chain[1:]:
        new_results = []
        for r in results:
            for cap, snap in r["snaps"]:
                cap.x, cap.y, cap.rotation = snap
            placed = [(cap, cap.world_bbox()) for cap, _snap in r["snaps"]]
            candidates = []
            for ref_cap, _ref_box in placed:
                for edge_label, edge in edges:
                    for style in styles:
                        place_touching(ref_cap, nxt, frame, edge, style)
                        bad = overlaps(nxt.world_bbox(), ic.world_bbox(), -0.01)
                        if not bad:
                            for _placed_cap, box in placed:
                                if overlaps(nxt.world_bbox(), box, MARGIN_MM - 0.01):
                                    bad = True
                                    break
                        if not bad:
                            d = min(cap_distance(nxt, c) for c, _b in placed)
                            candidates.append({"ref": ref_cap.ref,
                                                "label": f"{ref_cap.ref} {edge_label} {style}",
                                                "snap": (nxt.x, nxt.y, nxt.rotation), "d": d})
            kept = _filter_largest_gap(candidates, key=lambda c: c["d"])
            for k in kept:
                new_results.append({
                    "snaps": r["snaps"] + [(nxt, k["snap"])],
                    "label": r["label"] + f" | +{nxt.ref} ({k['label']})",
                    "links": r["links"] + [(k["ref"], nxt.ref)],
                })
        results = new_results
    return frame, results


def scenario_page_complete(board, out_name: str = "page_complete.png",
                            json_name: str = "page_complete_cas.json") -> None:
    """Genere et CATALOGUE tous les cas candidats (demande utilisateur du 2026-11-06 : "on
    choisira jamais une position, je veux generer tous les cas pour les avoir a disposition plus
    tard dans le process") par la methode EN CHAINE (cf. `_chain_cap_cases`) - chaque combinaison
    finale est auto-coherente, donc jamais de chevauchement entre condensateurs affiches ensemble.

    Perimetre actuel (demande utilisateur du 2026-11-06, retreci puis reetendu pas a pas : "on
    fait cela que pour C33 C34 et C28", puis "je ne veux que C34 et C28", puis reintroduction de
    C33 comme 3e capacite d'exemple pour la methode en chaine, puis "ajoute une 4eme capa... avec
    le meme jeu de regles") : U1 (STM32G431C6), broche 36, chaine C28 -> C34 -> C33 -> C27 (C27
    pris dans le groupe des 100nF interchangeables de U1, cf. decouplage.json, comme 4e capacite
    d'exemple - choix arbitraire, exercice de methode uniquement)."""
    u1 = board.components["U1"]
    pin, pin_label = "36", "broche 36"
    caps_chain = [board.components[r] for r in ("C28", "C34", "C33", "C27")]
    frame, results = _chain_cap_cases(u1, pin, caps_chain)

    panels = []  # (caps_snap, title, links)
    for r in results:
        panels.append((r["snaps"], f"[{pin_label}] {r['label']}", r["links"]))

    n = len(panels)
    cols = 4
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4.2 * cols, 4.2 * rows), squeeze=False)
    pins_xy = [(frame.px, frame.py, pin_label)]
    for i, (caps_snap, title, links_spec) in enumerate(panels):
        ax = axes[i // cols][i % cols]
        caps = []
        cap_by_ref = {}
        for cap, snap in caps_snap:
            cap.x, cap.y, cap.rotation = snap
            cap_by_ref[cap.ref] = cap
            caps.append(cap)
        links = []
        broche_xy = (frame.px, frame.py)
        for a, b in links_spec:
            pt_a = broche_xy if a == "broche" else cap_by_ref[a].pad_world_pos(_power_pad(cap_by_ref[a]))
            pt_b = cap_by_ref[b].pad_world_pos(_power_pad(cap_by_ref[b]))
            links.append((pt_a, pt_b))
        _draw_panel_full(ax, u1, caps, title, pins=pins_xy, links=links)
    for k in range(n, rows * cols):
        axes[k // cols][k % cols].axis("off")
    fig.suptitle(f"U1 (MCU), {pin_label} : chaine {' -> '.join(c.ref for c in caps_chain)} (chaque vignette auto-coherente)",
                  fontsize=11)
    fig.tight_layout()
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, out_name)
    fig.savefig(out, dpi=105)
    plt.close(fig)
    print(f"{n} panneaux, saved", out)

    # Catalogue JSON : chaque combinaison finale (deja coherente - pas de recomposition a faire).
    catalogue = {
        pin: {
            "broche_label": pin_label,
            "chaine": [c.ref for c in caps_chain],
            "cas": [
                {
                    "titre": r["label"],
                    "condensateurs": [
                        {"ref": cap.ref, "x": snap[0], "y": snap[1], "rotation_deg": snap[2]}
                        for cap, snap in r["snaps"]
                    ],
                }
                for r in results
            ],
        }
    }
    json_out = os.path.join(OUT_DIR, json_name)
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(catalogue, f, ensure_ascii=False, indent=2)
    print("catalogue json saved", json_out)


def scenario_une_capa_seule(board, ic_ref: str, cap_ref: str, pin: str, mode: int = 1,
                             out_name: str | None = None) -> None:
    """Pose UN SEUL condensateur (pas de combinaisons) dans la position choisie (mode, cf.
    `place_cap1_on_pin`) et s'arrete la - etape manuelle, le reste (ou mettre le condensateur
    suivant) vient de l'utilisateur, pas de ce script (demande utilisateur du 2026-11-06 :
    "c'est le script qui place, jamais toi [l'assistant directement]")."""
    ic = board.components[ic_ref]
    cap = board.components[cap_ref]
    frame = Frame(ic, pin)
    place_cap1_on_pin(cap, frame, mode)
    dist = pin_distance(cap, (frame.px, frame.py))
    print(f"{cap_ref} seul, position {mode}, distance={dist:.3f} mm")

    fig, ax = plt.subplots(figsize=(6, 6))
    ux0, uy0, ux1, uy1 = ic.world_bbox()
    ax.add_patch(Rectangle((ux0, uy0), ux1 - ux0, uy1 - uy0, facecolor="#0072B2", edgecolor="black", alpha=0.6, zorder=1))
    ax.plot(frame.px, frame.py, "o", color="red", markersize=8, zorder=5)
    ax.annotate(f"broche {pin}", (frame.px, frame.py), textcoords="offset points", xytext=(6, -10), fontsize=9, color="red")
    bx0, by0, bx1, by1 = cap.world_bbox()
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, facecolor="#E69F00", edgecolor="black", linewidth=1.2, zorder=3))
    pp = _power_pad(cap)
    for p in cap.pads:
        wx, wy = cap.pad_world_pos(p)
        col = "red" if p is pp else "black"
        ax.plot(wx, wy, ".", color=col, markersize=16, zorder=4)
    ax.annotate(cap_ref, cap.world_center(), ha="center", va="center", fontsize=10, zorder=6)
    ax.set_title(f"{cap_ref} seul, position {mode} (distance {dist:.2f} mm)", fontsize=10)
    ax.set_xlim(frame.px - 5, frame.px + 5)
    ax.set_ylim(frame.py + 5, frame.py - 5)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, out_name or f"{cap_ref.lower()}_seul_etape.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print("saved", out)


def main() -> None:
    board = load_board(EXTRACT_JSON)
    apply_decoupling(board, DECOUPLING_FILE)
    apply_active_rules(board, RULES_FILE)
    scenario_page_complete(board)


if __name__ == "__main__":
    main()
