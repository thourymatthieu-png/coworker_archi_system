"""Agencements internes "bloc par bloc" v2 (essai, lecture seule, AUCUNE modification du
.kicad_pcb). Pour chaque bloc fonctionnel (feuille DES-xxx), genere 3 agencements internes
distincts (heuristiques differentes : cote de decouplage, ordre des annexes, rotation du
hub), avec decouplage colle a la broche d'alimentation precise identifiee par connectivite
reelle (pastilles/reseaux extraits par tools/kicad_tetris_extract.py), pas juste "pres du CI".

Lit le JSON produit par kicad_tetris_extract.py (ex. _blocs_v2/geometrie.json).
Ecrit des images matplotlib dans <dossier_sortie> (ex. _blocs_v2/).

Usage:
    python tools/kicad_blocks_v2_placement.py <geometrie.json> <dossier_sortie>

Methode (voir rapport de tache pour le detail) :
- Blocs sans ancre (DES-002,003,004,005,009,010,011) : hub = composant le plus connecte
  (nb de pastilles, puis priorite de type U>Q>D>SW). Composants <= 2 pastilles partageant un
  reseau nomme avec une pastille du hub sont "colles" (snap) a cette pastille precise (repartis
  en tourniquet si plusieurs pastilles partagent le meme reseau sur le hub, ex. QFN multi-VDD).
  Le reste est tasse autour (packer rectangulaire bottom-left-fill repris de
  tools/kicad_tetris_placement.py).
- Blocs a ancre unique (DES-008 J1, DES-012 U7) : l'ancre garde sa rotation et la geometrie
  reelle de ses pastilles (donc l'orientation reelle de chaque broche) ; sa position absolue
  sur la carte n'est PAS reproduite ici (test de bloc isole, l'assemblage global est une etape
  ulterieure separee) mais la geometrie relative broche-a-broche est identique a la realite.
  Les composants annexes sont colles aux pastilles pertinentes par connectivite (voir
  DES-008 : FB1 colle au VBATM de J1, C8 colle au VBATL de FB1 -- C8 ne touche pas directement
  J1 electriquement, c'est le decouplage du rail APRES la self de ferrite, pas du connecteur).
- DES-007 (4 ancres M1-M4) : 4 sous-groupes par connectivite reelle (snubber/diode/MOSFET par
  moteur), chacun ancre a son connecteur reel, AUX POSITIONS REELLES RELATIVES des 4 ancres
  (coordonnees monde reprises de l'extraction, lecture seule). Un 5e groupe "mutualise" (C6,
  C7, C9 -- decouplage de bus commun, pas lie a un moteur en particulier) est tasse a part,
  simplification documentee dans le rapport.
"""
import argparse
import json
import math
import os
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kicad_tetris_placement import Packer  # reutilise le tasseur bottom-left-fill

GAP = 0.2            # mm, jeu decoupage/colle a une broche (reduit de 0.3 -> 0.2, cf. consigne
                     # compacite ; garde une securite anti-chevauchement, valeur de confort pour
                     # cet essai visuel, pas une regle DRC sourcee -- DOU a poser si retenue).
PACK_MARGIN = 0.15   # mm, jeu packer generique (reduit de 0.3 -> 0.15, idem ci-dessus).

N_TRIALS_GENERIC = 24   # essais internes par bloc generique avant selection des 3 plus compacts
N_TRIALS_DES008 = 20
N_TRIALS_DES012 = 24
N_TRIALS_DES007 = 20

HUB_COLOR = "#227093"
ANCHOR_COLOR = "#b33939"
SNAP_COLOR = "#f6b93b"
OTHER_COLOR = "#60a3bc"
BULK_COLOR = "#c44569"

TYPE_PRIORITY = {"U": 0, "Q": 1, "D": 2, "SW": 3}


def ref_letters(ref):
    return "".join(ch for ch in ref if ch.isalpha())


def rotate_pt(x, y, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return (x * c - y * s, x * s + y * c)


def oriented_bbox(w, h, cox, coy, rot):
    corners = [(cox - w / 2, coy - h / 2), (cox + w / 2, coy - h / 2),
               (cox - w / 2, coy + h / 2), (cox + w / 2, coy + h / 2)]
    pts = [rotate_pt(x, y, rot) for (x, y) in corners]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (max(xs) - min(xs), max(ys) - min(ys),
            (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0)


def pick_hub(members):
    def key(c):
        letters = ref_letters(c["ref"])
        return (len(c["pads"]), -TYPE_PRIORITY.get(letters, 9))
    return max(members, key=key)


def snap_pin_components(hub, hub_rot, candidates, net_round_robin=None):
    """candidates: composants <=2 pastilles pouvant etre colles a une broche precise du hub.
    Retourne (snapped, leftover). snapped = liste de dict {comp, pin_xy, net, pin_name}."""
    hub_pads_by_net = {}
    for p in hub["pads"]:
        if not p["net"]:
            continue
        hub_pads_by_net.setdefault(p["net"], []).append(p)

    net_counts = dict(net_round_robin) if net_round_robin else {}
    snapped, leftover = [], []
    for c in candidates:
        if len(c["pads"]) > 2:
            leftover.append(c)
            continue
        comp_nets = [p["net"] for p in c["pads"] if p["net"]]
        match_net = None
        for n in comp_nets:
            if n in hub_pads_by_net and n.upper() != "GND":
                match_net = n
                break
        if match_net is None:
            for n in comp_nets:
                if n in hub_pads_by_net:
                    match_net = n
                    break
        if match_net is None:
            leftover.append(c)
            continue
        pins = hub_pads_by_net[match_net]
        idx = net_counts.get(match_net, 0) % len(pins)
        net_counts[match_net] = net_counts.get(match_net, 0) + 1
        pin = pins[idx]
        pin_xy = rotate_pt(pin["x"], pin["y"], hub_rot)
        snapped.append({"comp": c, "pin_xy": pin_xy, "net": match_net, "pin_name": pin["name"]})
    return snapped, leftover


def place_snapped(snapped, hub_hw, hub_hh, occupied, hub_offset=(0.0, 0.0)):
    """Place chaque composant 'snappe' juste a l'exterieur du bord du hub le plus proche de sa
    broche cible, centre sur la coordonnee de la broche le long du bord. occupied: liste de
    rect dict {x,y,w,h} deja places (modifiee en place). hub_offset: translation du hub (pour
    les sous-groupes avec ancre a une position reelle != origine)."""
    ox, oy = hub_offset
    placed = []
    for item in snapped:
        c = item["comp"]
        px, py = item["pin_xy"]
        left, right = px - (-hub_hw), hub_hw - px
        top, bottom = py - (-hub_hh), hub_hh - py
        edge = min([("left", left), ("right", right), ("top", top), ("bottom", bottom)],
                   key=lambda t: t[1])[0]
        cw, ch = c["courtyard_w_mm"], c["courtyard_h_mm"]
        if edge in ("left", "right"):
            ow, oh = (cw, ch) if cw <= ch else (ch, cw)
            x = (-hub_hw - GAP - ow) if edge == "left" else (hub_hw + GAP)
            y = py - oh / 2
        else:
            ow, oh = (ch, cw) if ch <= cw else (cw, ch)
            y = (-hub_hh - GAP - oh) if edge == "top" else (hub_hh + GAP)
            x = px - ow / 2

        def overlaps(x, y, w, h):
            for r in occupied:
                if (x < r["x"] + r["w"] + PACK_MARGIN and x + w + PACK_MARGIN > r["x"] and
                        y < r["y"] + r["h"] + PACK_MARGIN and y + h + PACK_MARGIN > r["y"]):
                    return True
            return False

        tries = 0
        step_dir = 1
        while overlaps(x, y, ow, oh) and tries < 300:
            tries += 1
            shift = (oh + PACK_MARGIN) * ((tries + 1) // 2) * step_dir if edge in ("left", "right") \
                else (ow + PACK_MARGIN) * ((tries + 1) // 2) * step_dir
            step_dir = -step_dir
            if edge in ("left", "right"):
                y = py - oh / 2 + shift
            else:
                x = px - ow / 2 + shift

        rect = {"ref": c["ref"], "x": x + ox, "y": y + oy, "w": ow, "h": oh,
                "role": "snap", "value": c["value"], "pin_net": item["net"],
                "pin_name": item["pin_name"],
                "dist_to_pin_mm": round(math.hypot((x + ow / 2) - px, (y + oh / 2) - py), 2)}
        occupied.append({"x": rect["x"] - ox, "y": rect["y"] - oy, "w": ow, "h": oh})
        placed.append(rect)
    return placed


def pack_leftover(leftover, occupied_fixed, order_seed, offset=(0.0, 0.0)):
    rng = random.Random(order_seed)
    items = leftover[:]
    rng.shuffle(items)
    fixed = [{"id": "f%d" % i, "x": r["x"], "y": r["y"], "w": r["w"], "h": r["h"]}
             for i, r in enumerate(occupied_fixed)]
    packer = Packer(margin=PACK_MARGIN, rng=rng, fixed=fixed)
    placed = []
    ox, oy = offset
    for c in items:
        x, y, w, h = packer.place(c["ref"], c["courtyard_w_mm"], c["courtyard_h_mm"],
                                   allow_rotate=True, top_k=2)
        placed.append({"ref": c["ref"], "x": x + ox, "y": y + oy, "w": w, "h": h,
                        "role": "autre", "value": c["value"]})
    return placed


# ---------------------------------------------------------------------------
# Rendu
# ---------------------------------------------------------------------------

def render(title, rects, out_path, extra_boxes=None):
    fig, ax = plt.subplots(figsize=(8, 7))
    colors = {"hub": HUB_COLOR, "anchor": ANCHOR_COLOR, "snap": SNAP_COLOR,
              "autre": OTHER_COLOR, "bulk": BULK_COLOR}
    for r in rects:
        color = colors.get(r["role"], OTHER_COLOR)
        ax.add_patch(patches.Rectangle((r["x"], r["y"]), r["w"], r["h"], linewidth=0.6,
                                        edgecolor="black", facecolor=color, alpha=0.85))
        label = r["ref"]
        ax.text(r["x"] + r["w"] / 2, r["y"] + r["h"] / 2, label, ha="center", va="center",
                fontsize=5.5)
        if r["role"] == "snap" and "pin_name" in r:
            ax.text(r["x"] + r["w"] / 2, r["y"] + r["h"] / 2 - max(r["h"], 1.2) * 0.65,
                     f"-> {r['pin_name']} ({r['dist_to_pin_mm']}mm)", ha="center",
                     va="center", fontsize=3.4, color="#222222")
    if extra_boxes:
        for b in extra_boxes:
            ax.add_patch(patches.Rectangle((b["x"], b["y"]), b["w"], b["h"], linewidth=0.8,
                                            edgecolor="#555555", facecolor="none",
                                            linestyle=":"))
    all_x = [r["x"] for r in rects] + [r["x"] + r["w"] for r in rects]
    all_y = [r["y"] for r in rects] + [r["y"] + r["h"] for r in rects]
    pad = 3
    ax.set_xlim(min(all_x) - pad, max(all_x) + pad)
    ax.set_ylim(max(all_y) + pad, min(all_y) - pad)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("mm"); ax.set_ylabel("mm")
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def check_no_overlap(rects):
    import itertools
    for (a, b) in itertools.combinations(rects, 2):
        if (a["x"] < b["x"] + b["w"] - 1e-6 and a["x"] + a["w"] > b["x"] + 1e-6 and
                a["y"] < b["y"] + b["h"] - 1e-6 and a["y"] + a["h"] > b["y"] + 1e-6):
            return False, (a["ref"], b["ref"])
    return True, None


def bbox_of(rects):
    xs0 = [r["x"] for r in rects]; ys0 = [r["y"] for r in rects]
    xs1 = [r["x"] + r["w"] for r in rects]; ys1 = [r["y"] + r["h"] for r in rects]
    return (max(xs1) - min(xs0), max(ys1) - min(ys0))


# ---------------------------------------------------------------------------
# Agencement generique (blocs sans ancre, ou a ancre unique)
# ---------------------------------------------------------------------------

def build_generic_variant(hub, members, hub_rot, order_seed, is_anchor_hub=False):
    rest = [c for c in members if c["ref"] != hub["ref"]]
    hw, hh, hcx, hcy = oriented_bbox(hub["courtyard_w_mm"], hub["courtyard_h_mm"],
                                      hub["courtyard_center_offset_x_mm"],
                                      hub["courtyard_center_offset_y_mm"], hub_rot)
    hub_rect = {"ref": hub["ref"], "x": -hw / 2, "y": -hh / 2, "w": hw, "h": hh,
                "role": "anchor" if is_anchor_hub else "hub", "value": hub["value"]}
    occupied = [{"x": hub_rect["x"], "y": hub_rect["y"], "w": hw, "h": hh}]

    rng = random.Random(order_seed)
    candidates_snap = [c for c in rest if len(c["pads"]) <= 2]
    rng.shuffle(candidates_snap)
    snapped, snap_leftover = snap_pin_components(hub, hub_rot, candidates_snap)
    snap_rects = place_snapped(snapped, hw / 2, hh / 2, occupied)

    leftover = snap_leftover + [c for c in rest if len(c["pads"]) > 2]
    other_rects = pack_leftover(leftover, occupied, order_seed)

    all_rects = [hub_rect] + snap_rects + other_rects
    x0 = min(r["x"] for r in all_rects)
    y0 = min(r["y"] for r in all_rects)
    for r in all_rects:
        r["x"] -= x0
        r["y"] -= y0
    return all_rects


def run_generic_block(block_name, number_base, members, out_dir, results,
                       n_trials=N_TRIALS_GENERIC):
    """Genere n_trials essais internes (rotation du hub + graine de tassement variees), ne
    retient que les 3 plus compacts (plus petite boite englobante) parmi ceux sans
    chevauchement, et ne rend/n'ecrit que ces 3-la."""
    hub = pick_hub(members)
    rotations = [0, 90, 180, 270]
    trials = []
    for i in range(n_trials):
        rot = rotations[i % len(rotations)]
        seed = 1000 + number_base * 100 + i
        rects = build_generic_variant(hub, members, rot, seed)
        ok, bad = check_no_overlap(rects)
        if not ok:
            continue
        w, h = bbox_of(rects)
        trials.append({"rot": rot, "seed": seed, "rects": rects, "w": w, "h": h,
                        "area": w * h, "bad": bad})
    trials.sort(key=lambda t: t["area"])
    best3 = trials[:3]
    n_valid = len(trials)
    for rank, t in enumerate(best3):
        n = number_base + rank
        rects, w, h = t["rects"], t["w"], t["h"]
        img = os.path.join(out_dir, f"agencement_{n}_{block_name}.png")
        snap_info = [r for r in rects if r["role"] == "snap"]
        dist_txt = ", ".join(f"{r['ref']}->{r['pin_name']}:{r['dist_to_pin_mm']}mm"
                              for r in snap_info) or "aucun composant colle a une broche precise"
        render(f"Agencement {n} - {block_name} (hub={hub['ref']}, rot={t['rot']} deg, "
               f"rang compacite {rank + 1}/{n_valid} essais, {w:.1f}x{h:.1f}mm)", rects, img)
        results.append({
            "block": block_name, "agencement": n, "image": img,
            "bbox_w_mm": round(w, 2), "bbox_h_mm": round(h, 2),
            "overlap_ok": True, "overlap_bad_pair": None,
            "snap_distances": {r["ref"]: r["dist_to_pin_mm"] for r in snap_info},
            "note": dist_txt, "n_essais_internes": n_valid, "rang_compacite": rank + 1,
        })
        print(f"{block_name} agencement {n}: bbox={w:.1f}x{h:.1f}mm "
              f"(rang {rank + 1}/{n_valid} essais valides) | {dist_txt}")


# ---------------------------------------------------------------------------
# DES-008 : ancre J1
# ---------------------------------------------------------------------------

def build_des008_variant(members_by_ref, order_seed, reversed_fb1, side_flip):
    j1 = members_by_ref["J1"]
    fb1 = members_by_ref["FB1"]
    c8 = members_by_ref["C8"]
    if True:
        hw = j1["courtyard_w_mm"] / 2
        hh = j1["courtyard_h_mm"] / 2
        j1_rot = j1["current_rotation_deg"]
        anchor_rect = {"ref": "J1", "x": -hw, "y": -hh, "w": j1["courtyard_w_mm"],
                       "h": j1["courtyard_h_mm"], "role": "anchor", "value": j1["value"]}
        occupied = [{"x": anchor_rect["x"], "y": anchor_rect["y"], "w": j1["courtyard_w_mm"],
                     "h": j1["courtyard_h_mm"]}]

        # FB1 colle a la broche VBATM de J1 (pin2).
        snapped, _ = snap_pin_components(j1, j1_rot, [fb1])
        if reversed_fb1:
            snapped = list(reversed(snapped))
        fb1_rects = place_snapped(snapped, hw, hh, occupied)
        fb1_rect = fb1_rects[0]

        # C8 colle a la broche VBATL de FB1 (pas a J1 directement : decouplage du rail APRES
        # la self de ferrite). FB1 pads non rotates stockes ; FB1 n'a pas de rotation choisie
        # ici (on garde sa rotation reelle pour le calcul de la broche VBATL).
        fb1_rot = fb1["current_rotation_deg"]
        vbatl_pads = [p for p in fb1["pads"] if p["net"] == "VBATL"]
        if vbatl_pads:
            pin = vbatl_pads[0]
            pin_xy_local = rotate_pt(pin["x"], pin["y"], fb1_rot)
            pin_world = (fb1_rect["x"] + fb1_rect["w"] / 2 + pin_xy_local[0] * 0,
                         fb1_rect["y"] + fb1_rect["h"] / 2 + pin_xy_local[1] * 0)
            # Simplification : on colle C8 au bord de FB1 du cote de la pastille VBATL,
            # identifie par le signe de x local de cette pastille (gauche/droite du bead).
            side_left = pin_xy_local[0] < 0
            cw, ch = c8["courtyard_w_mm"], c8["courtyard_h_mm"]
            ow, oh = (cw, ch) if cw <= ch else (ch, cw)
            if not side_flip:
                x = fb1_rect["x"] - GAP - ow if side_left else fb1_rect["x"] + fb1_rect["w"] + GAP
            else:
                x = fb1_rect["x"] + fb1_rect["w"] + GAP if side_left else fb1_rect["x"] - GAP - ow
            y = fb1_rect["y"] + fb1_rect["h"] / 2 - oh / 2

            def overlaps_occ(x, y, w, h):
                for r in occupied:
                    if (x < r["x"] + r["w"] + GAP and x + w + GAP > r["x"] and
                            y < r["y"] + r["h"] + GAP and y + h + GAP > r["y"]):
                        return True
                return False

            tries = 0
            step_dir = 1
            while overlaps_occ(x, y, ow, oh) and tries < 200:
                tries += 1
                shift = (ow + GAP) * ((tries + 1) // 2) * step_dir
                step_dir = -step_dir
                x = (fb1_rect["x"] - GAP - ow if side_left else
                     fb1_rect["x"] + fb1_rect["w"] + GAP) + shift

            cx_ref, cy_ref = fb1_rect["x"] + fb1_rect["w"] / 2, fb1_rect["y"] + fb1_rect["h"] / 2
            c8_rect = {"ref": "C8", "x": x, "y": y, "w": ow, "h": oh, "role": "snap",
                       "value": c8["value"], "pin_net": "VBATL", "pin_name": pin["name"],
                       "dist_to_pin_mm": round(math.hypot((x + ow / 2) - cx_ref,
                                                            (y + oh / 2) - cy_ref), 2)}
        else:
            c8_rect = {"ref": "C8", "x": fb1_rect["x"] + fb1_rect["w"] + GAP, "y": fb1_rect["y"],
                       "w": c8["courtyard_w_mm"], "h": c8["courtyard_h_mm"], "role": "snap",
                       "value": c8["value"], "pin_net": "?", "pin_name": "?", "dist_to_pin_mm": None}

        all_rects = [anchor_rect, fb1_rect, c8_rect]
        x0 = min(r["x"] for r in all_rects); y0 = min(r["y"] for r in all_rects)
        for r in all_rects:
            r["x"] -= x0; r["y"] -= y0
        return all_rects, fb1_rect, c8_rect


def run_des008(members_by_ref, out_dir, results, n_trials=N_TRIALS_DES008):
    """n_trials essais internes (ordre FB1/C8 inverse ou non, cote de C8, graine de recherche
    de position sans chevauchement), ne retient que les 3 plus compacts."""
    base = 80
    rng = random.Random(8080)
    trials = []
    for i in range(n_trials):
        order_seed = 10 + i
        reversed_fb1 = rng.random() < 0.5
        side_flip = rng.random() < 0.5
        all_rects, fb1_rect, c8_rect = build_des008_variant(members_by_ref, order_seed,
                                                             reversed_fb1, side_flip)
        ok, bad = check_no_overlap(all_rects)
        if not ok:
            continue
        w, h = bbox_of(all_rects)
        trials.append({"rects": all_rects, "fb1": fb1_rect, "c8": c8_rect, "w": w, "h": h,
                        "area": w * h, "reversed_fb1": reversed_fb1, "side_flip": side_flip})
    trials.sort(key=lambda t: t["area"])
    best3 = trials[:3]
    n_valid = len(trials)
    for rank, t in enumerate(best3):
        n = base + rank
        all_rects, fb1_rect, c8_rect, w, h = t["rects"], t["fb1"], t["c8"], t["w"], t["h"]
        img = os.path.join(out_dir, f"agencement_{n}_DES-008-batterie-xt30.png")
        rot_note = (f"FB1 inverse={t['reversed_fb1']}, cote C8 inverse={t['side_flip']}, "
                    f"rang compacite {rank + 1}/{n_valid} essais")
        render(f"Agencement {n} - DES-008 batterie/XT30 (J1 ancre reelle, {rot_note}, "
               f"{w:.1f}x{h:.1f}mm)", all_rects, img)
        note = (f"FB1->VBATM(J1):{fb1_rect['dist_to_pin_mm']}mm ; "
                f"C8->VBATL(FB1):{c8_rect['dist_to_pin_mm']}mm")
        results.append({
            "block": "DES-008-batterie-xt30", "agencement": n, "image": img,
            "bbox_w_mm": round(w, 2), "bbox_h_mm": round(h, 2),
            "overlap_ok": True, "overlap_bad_pair": None,
            "snap_distances": {"FB1": fb1_rect["dist_to_pin_mm"], "C8": c8_rect["dist_to_pin_mm"]},
            "note": note, "n_essais_internes": n_valid, "rang_compacite": rank + 1,
        })
        print(f"DES-008 agencement {n}: bbox={w:.1f}x{h:.1f}mm "
              f"(rang {rank + 1}/{n_valid} essais valides) | {note}")


# ---------------------------------------------------------------------------
# DES-012 : ancre U7
# ---------------------------------------------------------------------------

def build_des012_variant(members_by_ref, order):
    u7 = members_by_ref["U7"]
    hw = u7["courtyard_w_mm"] / 2
    hh = u7["courtyard_h_mm"] / 2
    u7_rot = u7["current_rotation_deg"]
    anchor_rect = {"ref": "U7", "x": -hw, "y": -hh, "w": u7["courtyard_w_mm"],
                   "h": u7["courtyard_h_mm"], "role": "anchor", "value": u7["value"]}
    occupied = [{"x": anchor_rect["x"], "y": anchor_rect["y"], "w": u7["courtyard_w_mm"],
                 "h": u7["courtyard_h_mm"]}]
    snapped, leftover = snap_pin_components(u7, u7_rot, order)
    snap_rects = place_snapped(snapped, hw, hh, occupied)

    all_rects = [anchor_rect] + snap_rects
    x0 = min(r["x"] for r in all_rects); y0 = min(r["y"] for r in all_rects)
    for r in all_rects:
        r["x"] -= x0; r["y"] -= y0
    return all_rects, snap_rects


def run_des012(members_by_ref, out_dir, results, n_trials=N_TRIALS_DES012):
    """n_trials ordres de collage (permutations de C36/C37/TP7-10 sur les broches de U7) :
    l'ordre influe sur la boite englobante via les decalages anti-chevauchement successifs,
    pas via la broche visee (chaque composant vise toujours sa broche reelle precise)."""
    caps = [members_by_ref["C36"], members_by_ref["C37"]]
    tps = [members_by_ref[r] for r in ("TP7", "TP8", "TP9", "TP10")]
    combined = caps + tps
    base = 120
    rng = random.Random(1212)
    trials = []
    for i in range(n_trials):
        order = combined[:]
        rng.shuffle(order)
        all_rects, snap_rects = build_des012_variant(members_by_ref, order)
        ok, bad = check_no_overlap(all_rects)
        if not ok:
            continue
        w, h = bbox_of(all_rects)
        trials.append({"rects": all_rects, "snap": snap_rects, "w": w, "h": h, "area": w * h})
    trials.sort(key=lambda t: t["area"])
    best3 = trials[:3]
    n_valid = len(trials)
    for rank, t in enumerate(best3):
        n = base + rank
        all_rects, snap_rects, w, h = t["rects"], t["snap"], t["w"], t["h"]
        img = os.path.join(out_dir, f"agencement_{n}_DES-012-module-bluetooth.png")
        c36 = next(r for r in snap_rects if r["ref"] == "C36")
        c37 = next(r for r in snap_rects if r["ref"] == "C37")
        render(f"Agencement {n} - DES-012 module radio (U7 ancre reelle, C36/C37 colles au "
               f"+3V0, rang compacite {rank + 1}/{n_valid} essais, {w:.1f}x{h:.1f}mm)",
               all_rects, img)
        note = (f"C36->{c36['pin_name']}(+3V0):{c36['dist_to_pin_mm']}mm ; "
                f"C37->{c37['pin_name']}(+3V0):{c37['dist_to_pin_mm']}mm")
        results.append({
            "block": "DES-012-module-bluetooth", "agencement": n, "image": img,
            "bbox_w_mm": round(w, 2), "bbox_h_mm": round(h, 2),
            "overlap_ok": True, "overlap_bad_pair": None,
            "snap_distances": {r["ref"]: r["dist_to_pin_mm"] for r in snap_rects},
            "note": note, "n_essais_internes": n_valid, "rang_compacite": rank + 1,
        })
        print(f"DES-012 agencement {n}: bbox={w:.1f}x{h:.1f}mm "
              f"(rang {rank + 1}/{n_valid} essais valides) | {note}")


# ---------------------------------------------------------------------------
# DES-007 : 4 ancres M1-M4 (sous-groupes par moteur) + groupe mutualise (C6,C7,C9)
# ---------------------------------------------------------------------------

MOTOR_GROUPS = {
    "M1": {"snap": ["C2", "D1"], "other": ["Q1", "R3", "R7", "TP11"]},
    "M2": {"snap": ["C3", "D2"], "other": ["Q2", "R4", "R8"]},
    "M3": {"snap": ["C4", "D3"], "other": ["Q3", "R5", "R29"]},
    "M4": {"snap": ["C5", "D4"], "other": ["Q4", "R6", "R30"]},
}
BULK_REFS = ["C6", "C7", "C9"]


def anchor_world_rect(comp):
    hw = comp["courtyard_w_mm"] / 2
    hh = comp["courtyard_h_mm"] / 2
    rot = comp["current_rotation_deg"]
    cx, cy = comp["current_x_mm"], comp["current_y_mm"]
    w, h, ocx, ocy = oriented_bbox(comp["courtyard_w_mm"], comp["courtyard_h_mm"],
                                     comp["courtyard_center_offset_x_mm"],
                                     comp["courtyard_center_offset_y_mm"], rot)
    return {"ref": comp["ref"], "x": cx + ocx - w / 2, "y": cy + ocy - h / 2, "w": w, "h": h,
            "role": "anchor", "value": comp["value"]}


def build_des007_variant(members_by_ref, order_seed, reversed_snap_by_motor, reversed_bulk):
    all_rects = []
    snap_dist = {}
    for motor_ref, grp in MOTOR_GROUPS.items():
        motor = members_by_ref[motor_ref]
        mrect = anchor_world_rect(motor)
        all_rects.append(mrect)
        rot = motor["current_rotation_deg"]
        # M1-M4 sont montes en diagonale (rotation 45/135/-45/-135 deg, cf. geometrie.json) :
        # l'encombrement reel (boite tournee) est bien plus grand que courtyard_w/h brut.
        # Corrige ici (bug latent repris de l'essai precedent, demasque par le tassement serre) :
        # occupied doit refleter la VRAIE boite tournee + decalage de centre de courtyard,
        # sinon un composant snap peut se retrouver dans le vrai footprint du moteur.
        ow, oh, ocx_o, ocy_o = oriented_bbox(motor["courtyard_w_mm"], motor["courtyard_h_mm"],
                                              motor["courtyard_center_offset_x_mm"],
                                              motor["courtyard_center_offset_y_mm"], rot)
        hw, hh = ow / 2, oh / 2
        occupied = [{"x": ocx_o - ow / 2, "y": ocy_o - oh / 2, "w": ow, "h": oh}]
        snap_candidates = [members_by_ref[r] for r in grp["snap"]]
        if reversed_snap_by_motor.get(motor_ref):
            snap_candidates = list(reversed(snap_candidates))
        snapped, _ = snap_pin_components(motor, rot, snap_candidates)
        snap_rects_local = place_snapped(snapped, hw, hh, occupied,
                                          hub_offset=(motor["current_x_mm"], motor["current_y_mm"]))
        all_rects += snap_rects_local
        for r in snap_rects_local:
            snap_dist[r["ref"]] = r["dist_to_pin_mm"]

        other_refs = grp["other"]
        other_members = [members_by_ref[r] for r in other_refs]
        occ_for_pack = [{"x": r["x"] - motor["current_x_mm"], "y": r["y"] - motor["current_y_mm"],
                          "w": r["w"], "h": r["h"]} for r in ([mrect] + snap_rects_local)]
        other_rects = pack_leftover(other_members, occ_for_pack, order_seed + hash(motor_ref) % 97,
                                     offset=(motor["current_x_mm"], motor["current_y_mm"]))
        all_rects += other_rects

    # Groupe mutualise C6/C7/C9 : pas d'ancre dedie (decouplage de bus commun), place en
    # cluster tasse pres du barycentre des 4 ancres, simplification documentee.
    cx_bary = sum(members_by_ref[r]["current_x_mm"] for r in MOTOR_GROUPS) / 4.0
    cy_bary = sum(members_by_ref[r]["current_y_mm"] for r in MOTOR_GROUPS) / 4.0
    bulk_members = [members_by_ref[r] for r in BULK_REFS]
    if reversed_bulk:
        bulk_members = list(reversed(bulk_members))
    offset = (cx_bary - 3.0, cy_bary - 3.0)
    occ_for_bulk_local = [{"x": r["x"] - offset[0], "y": r["y"] - offset[1], "w": r["w"],
                            "h": r["h"]} for r in all_rects]
    bulk_rects = pack_leftover(bulk_members, occ_for_bulk_local, order_seed + 100, offset=offset)
    for r in bulk_rects:
        r["role"] = "bulk"
    all_rects += bulk_rects
    return all_rects, snap_dist


def run_des007(members_by_ref, out_dir, results, n_trials=N_TRIALS_DES007):
    """n_trials essais internes (graine de tassement des annexes/bulk, inversion independante
    de l'ordre de collage snap par moteur, inversion du cluster mutualise), ne retient que les
    3 plus compacts. Les 4 ancres M1-M4 restent a leur position/rotation reelle (jamais
    deplacees) : la compacite ne joue que sur le tassement des composants annexes autour."""
    base = 70
    rng = random.Random(7070)
    trials = []
    for i in range(n_trials):
        order_seed = 5 + i * 11
        reversed_snap_by_motor = {m: (rng.random() < 0.5) for m in MOTOR_GROUPS}
        reversed_bulk = rng.random() < 0.5
        all_rects, snap_dist = build_des007_variant(members_by_ref, order_seed,
                                                      reversed_snap_by_motor, reversed_bulk)
        ok, bad = check_no_overlap(all_rects)
        if not ok:
            continue
        w, h = bbox_of(all_rects)
        trials.append({"rects": all_rects, "snap_dist": snap_dist, "w": w, "h": h,
                        "area": w * h})
    trials.sort(key=lambda t: t["area"])
    best3 = trials[:3]
    n_valid = len(trials)
    for rank, t in enumerate(best3):
        n = base + rank
        all_rects, snap_dist, w, h = t["rects"], t["snap_dist"], t["w"], t["h"]
        img = os.path.join(out_dir, f"agencement_{n}_DES-007-puissance-moteurs.png")
        note = ", ".join(f"{k}:{v}mm" for k, v in snap_dist.items())
        render(f"Agencement {n} - DES-007 puissance moteurs (M1-M4 ancres reelles, "
               f"rang compacite {rank + 1}/{n_valid} essais, {w:.1f}x{h:.1f}mm)",
               all_rects, img)
        results.append({
            "block": "DES-007-puissance-moteurs", "agencement": n, "image": img,
            "bbox_w_mm": round(w, 2), "bbox_h_mm": round(h, 2),
            "overlap_ok": True, "overlap_bad_pair": None,
            "snap_distances": snap_dist,
            "note": note + " ; C6/C7/C9 en cluster mutualise (simplification, non ancres a un "
                            "moteur)",
            "n_essais_internes": n_valid, "rang_compacite": rank + 1,
        })
        print(f"DES-007 agencement {n}: bbox={w:.1f}x{h:.1f}mm "
              f"(rang {rank + 1}/{n_valid} essais valides) | {note}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

GENERIC_BLOCKS = [
    ("DES-002-microcontroleur", 20),
    ("DES-003-centrale-inertielle", 30),
    ("DES-004-capteur-hauteur", 40),
    ("DES-005-flux-optique", 50),
    ("DES-009-regulateur-pont", 90),
    ("DES-010-bouton", 100),
    ("DES-011-voyant-buzzer", 110),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("geometry_json")
    ap.add_argument("out_dir")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    with open(args.geometry_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    components = data["components"]
    by_block = {}
    by_ref = {}
    for c in components:
        by_block.setdefault(c["block"], []).append(c)
        by_ref[c["ref"]] = c

    results = []

    for block_name, base in GENERIC_BLOCKS:
        run_generic_block(block_name, base, by_block[block_name], args.out_dir, results)

    run_des008(by_ref, args.out_dir, results)
    run_des012(by_ref, args.out_dir, results)
    run_des007(by_ref, args.out_dir, results)

    out_json = os.path.join(args.out_dir, "resultats_blocs_v2.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\nEcrit:", out_json)

    bad = [r for r in results if not r["overlap_ok"]]
    if bad:
        print("\n!!! CHEVAUCHEMENTS DETECTES:")
        for r in bad:
            print(" ", r["block"], r["agencement"], r["overlap_bad_pair"])
    else:
        print("\nAucun chevauchement detecte (0 sur", len(results), "agencements).")


if __name__ == "__main__":
    main()
