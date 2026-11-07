"""Placement PCB "tetris" (essai hors-ligne, aucune modification du .kicad_pcb).

Lit le JSON produit par `modules/kicad/tools/kicad_tetris_extract.py` (geometrie reelle des 107 composants
de proj_boomrone, lecture seule du .kicad_pcb) et calcule, en un seul passage Python, plusieurs
propositions de placement par tassement rectangulaire deterministe ("tetris"/skyline packing),
sans aucun appel au serveur MCP KiCad ni au board reel.

Principe (demande explicite de l'utilisateur, voir rapport) :
1. 4 ancres fixes (J1, M1-M4, U7) gardent leurs positions/rotations reelles actuelles - jamais
   deplacees, mais leur encombrement (boite englobante tournee) bloque de l'espace pour le reste.
2. Pour chaque bloc fonctionnel (feuille de schema DES-xxx), tassement local : le composant "hub"
   (le plus connecte du bloc, hors ancre) est place en premier, puis les decouplages identifies par
   connectivite reelle (passif 2 broches partageant un reseau non-GND avec une broche du hub)
   colles contre lui, puis les autres composants du bloc tasses autour. Resultat : une boite
   englobante par bloc.
3. Assemblage : les boites de bloc sont a leur tour tassees entre elles ET autour des ancres fixes
   (qui occupent reellement de l'espace), par le meme algorithme "bottom-left-fill" (points
   d'ancrage = coins des rectangles deja places, on choisit a chaque etape le point/l'orientation
   qui minimise la boite englobante totale).
4. Score = aire de la boite englobante totale de l'assemblage (plus petit = mieux). Zero
   chevauchement garanti par construction (verifie quand meme par securite, voir
   `check_no_overlap`).
5. Plusieurs essais (ordre de tassement et choix d'orientation varies par graine aleatoire),
   classement par score, Top 10 rapporte.

Rendu: matplotlib (pas de kicad-cli ni de MCP dans la boucle), PNG dans
`<dossier_projet_kicad>/_tetris_essais/`.

Usage:
    python projets/boomrone/tools/kicad_tetris_placement.py <geometrie.json> <dossier_sortie> [--essais N] [--seed S]

Limites connues (a verifier/ameliorer si cette methode est retenue au-dela d'un essai) :
- L'orientation choisie par l'algorithme (rotation 0/90 d'un rectangle d'encombrement) est une
  variable de calcul interne au tasseur, elle n'est PAS appliquee a un composant reel ni ecrite
  nulle part : une vraie rotation devrait ensuite respecter les regles de brochage (voir
  `modules/kicad/kicad-mcp-notes.md`, rotation des composants).
- Les decouplages d'un bloc dont le "hub" est lui-meme une ancre (ex. DES-012, hub = U7) ne
  peuvent pas etre colles a cette ancre pendant le tassement LOCAL du bloc (les ancres sont
  retirees du tetris) ; ils sont tasses entre eux puis leur mini-groupe est positionne par
  l'assemblage global, qui peut ou non finir pres de l'ancre.
- Marges de tassement (0,3 mm entre composants d'un bloc, 1,0 mm entre boites de bloc à l'assemblage)
  sont des valeurs de confort pour cet essai visuel, pas des regles de conception (DRC) sourcees.
"""
import argparse
import itertools
import json
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

INTRA_BLOCK_MARGIN_MM = 0.3
INTER_BLOCK_MARGIN_MM = 1.0

ANCHOR_COLOR = "#b33939"
HUB_COLOR = "#227093"
DECAP_COLOR = "#f6b93b"
OTHER_COLOR = "#60a3bc"
BLOCK_COLORS = [
    "#60a3bc", "#78e08f", "#f8c291", "#b8e994", "#82ccdd",
    "#f3a683", "#f7d794", "#c44569", "#786fa6", "#e77f67",
]


# ---------------------------------------------------------------------------
# Geometrie
# ---------------------------------------------------------------------------

def rotate_pt(x, y, deg):
    import math
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return (x * c - y * s, x * s + y * c)


def anchor_world_bbox(comp):
    """Boite englobante (axis-aligned) de l'ancre dans le repere monde, en tenant compte de sa
    rotation reelle actuelle (lecture seule, la position/rotation ne sont jamais changees)."""
    w, h = comp["courtyard_w_mm"], comp["courtyard_h_mm"]
    cox, coy = comp["courtyard_center_offset_x_mm"], comp["courtyard_center_offset_y_mm"]
    rot = comp["current_rotation_deg"]
    corners_local = [
        (cox - w / 2, coy - h / 2), (cox + w / 2, coy - h / 2),
        (cox - w / 2, coy + h / 2), (cox + w / 2, coy + h / 2),
    ]
    wx, wy = comp["current_x_mm"], comp["current_y_mm"]
    world_pts = []
    for (lx, ly) in corners_local:
        rx, ry = rotate_pt(lx, ly, rot)
        world_pts.append((wx + rx, wy + ry))
    xs = [p[0] for p in world_pts]
    ys = [p[1] for p in world_pts]
    return (min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))


# ---------------------------------------------------------------------------
# Tasseur generique "bottom-left-fill" avec points d'ancrage = coins des rectangles places.
# ---------------------------------------------------------------------------

class Packer:
    """Empile des rectangles sans chevauchement, en minimisant la boite englobante au fur et a
    mesure. `placed` est une liste de dict {id, x, y, w, h} (x, y = coin superieur-gauche)."""

    def __init__(self, margin, rng, fixed=None):
        self.margin = margin
        self.rng = rng
        self.placed = list(fixed) if fixed else []
        self._refresh_candidates()

    def _refresh_candidates(self):
        """Points d'ancrage = intersections de la grille formee par les bords (gauche/droite,
        haut/bas) de tous les rectangles deja places, plus l'origine. Plus riche que les seuls
        coins (bas-gauche/haut-droite) d'un simple "shelf packing" : permet de loger un
        rectangle dans un creux interieur (entre deux ancres, par exemple), pas seulement en
        bout de ligne/colonne. Nombre de rectangles par instance de Packer reste petit (<=~20
        pour un bloc, <=~16 pour l'assemblage), donc ce O(n^2) reste rapide."""
        xs = {0.0}
        ys = {0.0}
        for r in self.placed:
            xs.add(r["x"]); xs.add(r["x"] + r["w"])
            ys.add(r["y"]); ys.add(r["y"] + r["h"])
        self.candidates = sorted((x, y) for x in xs for y in ys)

    def _overlaps(self, x, y, w, h):
        m = self.margin
        for r in self.placed:
            if (x < r["x"] + r["w"] + m and x + w + m > r["x"] and
                    y < r["y"] + r["h"] + m and y + h + m > r["y"]):
                return True
        return False

    def _bbox_area_with(self, x, y, w, h):
        xs = [x, x + w] + [r["x"] for r in self.placed] + [r["x"] + r["w"] for r in self.placed]
        ys = [y, y + h] + [r["y"] for r in self.placed] + [r["y"] + r["h"] for r in self.placed]
        if not self.placed:
            return w * h
        return (max(xs) - min(xs)) * (max(ys) - min(ys))

    def place(self, item_id, w, h, allow_rotate=True, top_k=3):
        """Essaie toutes les orientations/points d'ancrage valides, garde les `top_k` meilleurs
        (plus petite boite englobante resultante) et en tire un au hasard (diversite entre essais).
        Retourne (x, y, w_final, h_final)."""
        orientations = [(w, h)]
        if allow_rotate and abs(w - h) > 1e-6:
            orientations.append((h, w))

        options = []
        for (ow, oh) in orientations:
            for (cx, cy) in self.candidates:
                if self._overlaps(cx, cy, ow, oh):
                    continue
                area = self._bbox_area_with(cx, cy, ow, oh)
                options.append((area, cx, cy, ow, oh))

        if not options:
            # Repli : poser plus loin a droite du dernier point (ne devrait pas arriver avec un
            # canevas suffisamment grand de candidats, garde-fou).
            far_x = max([r["x"] + r["w"] for r in self.placed], default=0.0) + self.margin
            options = [(far_x * far_x, far_x, 0.0, w, h)]

        options.sort(key=lambda o: o[0])
        top = options[:max(1, top_k)]
        _, x, y, ow, oh = self.rng.choice(top)

        self.placed.append({"id": item_id, "x": x, "y": y, "w": ow, "h": oh})
        self._refresh_candidates()
        return x, y, ow, oh

    def bbox(self):
        if not self.placed:
            return (0.0, 0.0, 0.0, 0.0)
        xs0 = [r["x"] for r in self.placed]
        xs1 = [r["x"] + r["w"] for r in self.placed]
        ys0 = [r["y"] for r in self.placed]
        ys1 = [r["y"] + r["h"] for r in self.placed]
        return (min(xs0), min(ys0), max(xs1) - min(xs0), max(ys1) - min(ys0))


# ---------------------------------------------------------------------------
# Tassement local d'un bloc
# ---------------------------------------------------------------------------

def choose_hub_and_decaps(members):
    """members: liste de composants (non-ancres) d'un bloc. Retourne (hub, decaps, others)."""
    if not members:
        return None, [], []
    type_priority = {"U": 0, "Q": 1, "D": 2, "SW": 3}

    def priority(c):
        ref = c["ref"]
        letters = "".join(ch for ch in ref if ch.isalpha())
        return type_priority.get(letters, 9)

    hub = max(members, key=lambda c: (len(c["pads"]), -priority(c)))
    if len(hub["pads"]) < 2:
        # Pas de vrai "hub" multi-broches (ex. bloc de 2 passifs) : pas de decouplage dedie.
        return None, [], members

    hub_nets_non_gnd = {p["net"] for p in hub["pads"]
                         if p["net"] and "GND" not in p["net"].upper()}

    decaps, others = [], []
    for c in members:
        if c is hub:
            continue
        ref = c["ref"]
        is_cap = ref.startswith("C")
        two_pin = len(c["pads"]) == 2
        shares_power = any(p["net"] in hub_nets_non_gnd for p in c["pads"])
        if is_cap and two_pin and shares_power:
            decaps.append(c)
        else:
            others.append(c)
    return hub, decaps, others


def pack_block(block_name, members, rng, snapshot_cb=None):
    """Tasse les composants d'un bloc (hors ancres). Retourne (bbox_w, bbox_h, placements)
    avec placements = liste de dict {ref, x, y, w, h, role} en coordonnees LOCALES au bloc
    (origine = coin superieur-gauche de la boite du bloc)."""
    hub, decaps, others = choose_hub_and_decaps(members)
    packer = Packer(margin=INTRA_BLOCK_MARGIN_MM, rng=rng)
    roles = {}

    order = []
    if hub is not None:
        order.append(hub)
        roles[hub["ref"]] = "hub"
    decaps_shuffled = decaps[:]
    rng.shuffle(decaps_shuffled)
    for c in decaps_shuffled:
        order.append(c)
        roles[c["ref"]] = "decap"
    others_shuffled = others[:]
    rng.shuffle(others_shuffled)
    for c in others_shuffled:
        order.append(c)
        roles.setdefault(c["ref"], "autre")

    placements = []
    for c in order:
        x, y, w, h = packer.place(c["ref"], c["courtyard_w_mm"], c["courtyard_h_mm"])
        placements.append({"ref": c["ref"], "x": x, "y": y, "w": w, "h": h,
                            "role": roles[c["ref"]], "value": c["value"]})
        if snapshot_cb:
            snapshot_cb(block_name, placements, packer.bbox())

    bx0, by0, bw, bh = packer.bbox()
    # Ramener a une origine (0,0) pour ce bloc.
    for p in placements:
        p["x"] -= bx0
        p["y"] -= by0
    return bw, bh, placements


# ---------------------------------------------------------------------------
# Assemblage global
# ---------------------------------------------------------------------------

def run_one_trial(components, seed, representative=False, out_dir=None, trial_idx=0):
    rng = random.Random(seed)

    anchors = [c for c in components if c["is_anchor"]]
    non_anchor = [c for c in components if not c["is_anchor"]]
    blocks = {}
    for c in non_anchor:
        blocks.setdefault(c["block"], []).append(c)

    fixed_rects = []
    for a in anchors:
        x0, y0, w, h = anchor_world_bbox(a)
        fixed_rects.append({"id": a["ref"], "x": x0, "y": y0, "w": w, "h": h})

    block_names = list(blocks.keys())
    rng.shuffle(block_names)

    block_results = {}
    progression_images = []
    step_no = 0
    if representative and out_dir:
        step_no += 1
        img = os.path.join(out_dir, f"essai_{trial_idx:02d}_etape_{step_no:02d}_ancres.png")
        render_assembly(f"Essai {trial_idx} - etape {step_no} - ancres fixes",
                         fixed_rects, {}, img)
        progression_images.append(img)

    for bname in block_names:
        members = blocks[bname]
        local_snaps = []

        def snap_cb(block_name, placements, bbox, _store=local_snaps):
            _store.append((list(placements), bbox))

        bw, bh, placements = pack_block(bname, members, rng,
                                         snapshot_cb=(snap_cb if representative else None))
        block_results[bname] = {"w": bw, "h": bh, "placements": placements}

        if representative and out_dir:
            img = os.path.join(out_dir, f"essai_{trial_idx:02d}_bloc_local_{bname}.png")
            render_block_local(bname, placements, bw, bh, img)
            progression_images.append(img)

    # Assemblage : place les boites de bloc (triees par aire decroissante en tete pour un
    # tassement plus compact, le reste de l'ordre reste aleatoire) autour des ancres fixes.
    block_order = sorted(block_names, key=lambda n: -(block_results[n]["w"] * block_results[n]["h"]))
    if rng.random() < 0.5:
        # Variante : ordre partiellement aleatoire plutot que purement par aire decroissante.
        rng.shuffle(block_order)

    packer = Packer(margin=INTER_BLOCK_MARGIN_MM, rng=rng, fixed=fixed_rects)
    block_offsets = {}
    for bname in block_order:
        bw, bh = block_results[bname]["w"], block_results[bname]["h"]
        x, y, w, h = packer.place(bname, bw, bh, allow_rotate=True)
        block_offsets[bname] = (x, y, w, h, bw, bh)

        if representative and out_dir:
            step_no += 1
            img = os.path.join(out_dir, f"essai_{trial_idx:02d}_etape_{step_no:02d}_{bname}.png")
            all_rects_so_far = build_full_component_rects(
                components, {k: v for k, v in block_offsets.items()}, block_results)
            render_assembly(f"Essai {trial_idx} - etape {step_no} - apres {bname}",
                             fixed_rects, all_rects_so_far, img)
            progression_images.append(img)

    full_rects = build_full_component_rects(components, block_offsets, block_results)
    bbox = compute_global_bbox(fixed_rects, full_rects)
    score = bbox[2] * bbox[3]
    overlap_ok = check_no_overlap(fixed_rects, full_rects)

    final_img = None
    if out_dir:
        final_img = os.path.join(out_dir, f"essai_{trial_idx:02d}_assemblage_final.png")
        render_assembly(f"Essai {trial_idx} - assemblage final (score={score:.0f} mm2)",
                         fixed_rects, full_rects, final_img, bbox=bbox)

    return {
        "seed": seed,
        "trial": trial_idx,
        "score_mm2": round(score, 1),
        "overlap_ok": overlap_ok,
        "bbox": bbox,
        "final_image": final_img,
        "progression_images": progression_images,
    }


def build_full_component_rects(components, block_offsets, block_results):
    """Place chaque composant non-ancre dans le repere global, a partir de l'offset de son bloc."""
    rects = {}
    for bname, (x, y, w, h, bw, bh) in block_offsets.items():
        placements = block_results[bname]["placements"]
        # Le bloc a pu etre tourne (w != bw) lors de l'assemblage : si tourne, on echange les
        # coordonnees locales x/y pour rester coherent (rotation 90 deg approximee).
        rotated = abs(w - bw) > 1e-6
        for p in placements:
            if not rotated:
                gx = x + p["x"]
                gy = y + p["y"]
                gw, gh = p["w"], p["h"]
            else:
                gx = x + p["y"]
                gy = y + p["x"]
                gw, gh = p["h"], p["w"]
            rects[p["ref"]] = {"x": gx, "y": gy, "w": gw, "h": gh,
                                "role": p["role"], "block": bname, "value": p["value"]}
    return rects


def compute_global_bbox(fixed_rects, full_rects):
    xs0, ys0, xs1, ys1 = [], [], [], []
    for r in fixed_rects:
        xs0.append(r["x"]); ys0.append(r["y"])
        xs1.append(r["x"] + r["w"]); ys1.append(r["y"] + r["h"])
    for r in full_rects.values():
        xs0.append(r["x"]); ys0.append(r["y"])
        xs1.append(r["x"] + r["w"]); ys1.append(r["y"] + r["h"])
    x0, y0 = min(xs0), min(ys0)
    return (x0, y0, max(xs1) - x0, max(ys1) - y0)


def check_no_overlap(fixed_rects, full_rects):
    all_r = [(r["id"], r["x"], r["y"], r["w"], r["h"]) for r in fixed_rects]
    all_r += [(ref, r["x"], r["y"], r["w"], r["h"]) for ref, r in full_rects.items()]
    for (id1, x1, y1, w1, h1), (id2, x2, y2, w2, h2) in itertools.combinations(all_r, 2):
        if (x1 < x2 + w2 - 1e-6 and x1 + w1 > x2 + 1e-6 and
                y1 < y2 + h2 - 1e-6 and y1 + h1 > y2 + 1e-6):
            return False
    return True


# ---------------------------------------------------------------------------
# Rendu matplotlib
# ---------------------------------------------------------------------------

def _draw_rect(ax, x, y, w, h, color, label, fontsize=4):
    ax.add_patch(patches.Rectangle((x, y), w, h, linewidth=0.5,
                                    edgecolor="black", facecolor=color, alpha=0.85))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fontsize)


def render_block_local(block_name, placements, bw, bh, out_path):
    fig, ax = plt.subplots(figsize=(6, 6))
    for p in placements:
        color = {"hub": HUB_COLOR, "decap": DECAP_COLOR, "autre": OTHER_COLOR}.get(p["role"], OTHER_COLOR)
        _draw_rect(ax, p["x"], p["y"], p["w"], p["h"], color, p["ref"])
    ax.set_xlim(-1, bw + 1)
    ax.set_ylim(bh + 1, -1)
    ax.set_aspect("equal")
    ax.set_title(f"Bloc {block_name} - tasse localement ({bw:.1f} x {bh:.1f} mm)")
    ax.set_xlabel("mm"); ax.set_ylabel("mm")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def render_assembly(title, fixed_rects, full_rects, out_path, bbox=None):
    fig, ax = plt.subplots(figsize=(9, 9))
    for r in fixed_rects:
        _draw_rect(ax, r["x"], r["y"], r["w"], r["h"], ANCHOR_COLOR, r["id"], fontsize=5)

    block_color_map = {}
    for ref, r in full_rects.items():
        bname = r["block"]
        if bname not in block_color_map:
            block_color_map[bname] = BLOCK_COLORS[len(block_color_map) % len(BLOCK_COLORS)]
        _draw_rect(ax, r["x"], r["y"], r["w"], r["h"], block_color_map[bname], ref, fontsize=3.2)

    all_x = [r["x"] for r in fixed_rects] + [r["x"] + r["w"] for r in fixed_rects]
    all_y = [r["y"] for r in fixed_rects] + [r["y"] + r["h"] for r in fixed_rects]
    all_x += [r["x"] for r in full_rects.values()] + [r["x"] + r["w"] for r in full_rects.values()]
    all_y += [r["y"] for r in full_rects.values()] + [r["y"] + r["h"] for r in full_rects.values()]
    if all_x:
        pad = 5
        ax.set_xlim(min(all_x) - pad, max(all_x) + pad)
        ax.set_ylim(max(all_y) + pad, min(all_y) - pad)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("mm"); ax.set_ylabel("mm")
    if bbox:
        x0, y0, w, h = bbox
        ax.add_patch(patches.Rectangle((x0, y0), w, h, linewidth=1.2,
                                        edgecolor="red", facecolor="none", linestyle="--"))
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("geometry_json")
    ap.add_argument("out_dir")
    ap.add_argument("--essais", type=int, default=20)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    with open(args.geometry_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    components = data["components"]

    results = []
    for i in range(args.essais):
        seed = args.seed + i
        representative = (i == 0)
        res = run_one_trial(components, seed, representative=representative,
                             out_dir=args.out_dir, trial_idx=i)
        results.append(res)
        print(f"Essai {i:02d} (seed={seed}): score={res['score_mm2']} mm2, "
              f"overlap_ok={res['overlap_ok']}, bbox={res['bbox']}")

    results.sort(key=lambda r: r["score_mm2"])
    top10 = results[:10]

    print("\n=== Top 10 ===")
    for rank, r in enumerate(top10, 1):
        print(f"{rank}. essai {r['trial']:02d} (seed={r['seed']}): "
              f"score={r['score_mm2']} mm2, overlap_ok={r['overlap_ok']}, "
              f"image={r['final_image']}")

    summary_path = os.path.join(args.out_dir, "resultats.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({"all_trials": results, "top10": top10}, f, indent=2)
    print("\nResume ecrit:", summary_path)


if __name__ == "__main__":
    main()
