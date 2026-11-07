#!/usr/bin/env python3
"""Place les champs Référence / Valeur des symboles d'un schéma KiCad (.kicad_sch)
à l'endroit le plus probablement lisible, selon le type de symbole.

Pourquoi : les serveurs MCP posent les champs au centre du symbole, ce qui
oblige à les replacer à la main page après page. Ce script applique des règles
fixes (voir RULES plus bas), vérifie les collisions avec les fils, les autres
symboles, les étiquettes et les textes déjà placés, et choisit le premier
emplacement candidat libre. Idempotent : on peut le relancer.

Usage :
    python modules/kicad/tools/kicad_place_fields.py <schema.kicad_sch> [--refs R1,R2,...] [--dry-run]

Sans --refs, traite tous les symboles de la feuille. Les repères commençant par
« # » (symboles de puissance) voient leur Référence masquée.

Règles (distances en mm, modifiables dans RULES) :
- résistance, condensateur, diode, ferrite... (2 broches)
    horizontale : Référence et Valeur AU-DESSUS, centrées (repli : en dessous)
    verticale   : Référence et Valeur À GAUCHE, alignées à droite (repli : à droite)
- symbole de puissance : GND -> Valeur centrée SOUS le triangle ; autres (+3V0...) -> au-dessus
- transistor (Q) : à droite, Référence au-dessus de la Valeur (repli : à gauche)
- autres (U, J, SW, BZ...) : Référence au-dessus, Valeur en dessous, centrées
  (repli : à droite)
- angle du champ : (360 - rotation du symbole) % 360 pour 90/270, sinon 0
  (le texte reste horizontal à l'écran).

À améliorer à chaque fois qu'un placement manuel a été nécessaire : ajouter la
règle ici plutôt que de corriger à la main.
"""
import argparse
import math
import re
import sys

RULES = {
    "margin": 1.3,        # écart texte / corps du symbole
    "line": 2.54,         # écart entre Référence et Valeur
    "char_w": 1.05,       # largeur estimée d'un caractère (police 1,27)
    "char_h": 1.4,        # hauteur estimée d'une ligne de texte
    "pad": 0.5,           # marge de sécurité autour d'un texte pour le test de collision
}


# ----------------------------------------------------------------- S-expression
TOKEN = re.compile(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+')


def parse(text):
    stack = [[]]
    for tok in TOKEN.findall(text):
        if tok == "(":
            stack.append([])
        elif tok == ")":
            node = stack.pop()
            stack[-1].append(node)
        elif tok.startswith('"'):
            stack[-1].append(("s", tok[1:-1]))
        else:
            stack[-1].append(tok)
    return stack[0][0]


def head(n):
    return n[0] if isinstance(n, list) and n and isinstance(n[0], str) else None


def kids(n, name):
    return [c for c in n if head(c) == name]


def kid(n, name):
    k = kids(n, name)
    return k[0] if k else None


def num(x):
    return float(x)


def sval(n):
    return n[1][1] if isinstance(n[1], tuple) else n[1]


# ------------------------------------------------------------------ geometry
def lib_points(sym, unit, style):
    """Points (x, y) en coordonnées de symbole : corps + broches visibles."""
    pts, pinpts = [], []

    def walk(n):
        for c in n:
            h = head(c)
            if h == "symbol":
                m = re.search(r"_(\d+)_(\d+)$", c[1][1])
                if m:
                    u, s = int(m.group(1)), int(m.group(2))
                    if u not in (0, unit) or s not in (0, style):
                        continue
                walk(c)
            elif h == "rectangle":
                for k in ("start", "end"):
                    p = kid(c, k)
                    pts.append((num(p[1]), num(p[2])))
            elif h == "polyline":
                for xy in kids(kid(c, "pts"), "xy"):
                    pts.append((num(xy[1]), num(xy[2])))
            elif h == "circle":
                ce, r = kid(c, "center"), num(kid(c, "radius")[1])
                cx, cy = num(ce[1]), num(ce[2])
                pts.extend([(cx - r, cy - r), (cx + r, cy + r)])
            elif h == "arc":
                for k in ("start", "mid", "end"):
                    p = kid(c, k)
                    pts.append((num(p[1]), num(p[2])))
            elif h == "pin":
                hid = kid(c, "hide")
                if hid and len(hid) > 1 and hid[1] == "yes":
                    continue
                at, ln = kid(c, "at"), num(kid(c, "length")[1])
                x, y, a = num(at[1]), num(at[2]), num(at[3])
                ex = x + ln * math.cos(math.radians(a))
                ey = y + ln * math.sin(math.radians(a))
                pinpts.append((x, y))
                pts.extend([(x, y), (ex, ey)])

    walk(sym)
    return pts, pinpts


def to_sheet(p, at, mirror):
    x, y = p
    if mirror == "x":
        y = -y
    elif mirror == "y":
        x = -x
    r = math.radians(at[2])
    rx = x * math.cos(r) - y * math.sin(r)
    ry = x * math.sin(r) + y * math.cos(r)
    return (round(at[0] + rx, 3), round(at[1] - ry, 3))


def bbox(points):
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return (min(xs), min(ys), max(xs), max(ys))


def inter(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def text_box(x, y, s, just):
    w, h = len(s) * RULES["char_w"], RULES["char_h"]
    if just == "left":
        x0 = x
    elif just == "right":
        x0 = x - w
    else:
        x0 = x - w / 2
    return (x0, y - h / 2, x0 + w, y + h / 2)


# ------------------------------------------------------------------- analysis
def load(path):
    text = open(path, encoding="utf8").read()
    root = parse(text)
    libs = {}
    for ls in kids(root, "lib_symbols"):
        for s in kids(ls, "symbol"):
            libs[s[1][1]] = s
    insts = []
    for s in kids(root, "symbol"):
        lid = kid(s, "lib_id")
        if not lid:
            continue
        at = kid(s, "at")
        mir = kid(s, "mirror")
        ref = None
        for p in kids(s, "property"):
            if p[1][1] == "Reference":
                ref = p[2][1]
            if p[1][1] == "Value":
                val = p[2][1]
        unit = kid(s, "unit")
        style = kid(s, "body_style")
        insts.append({
            "lib_id": lid[1][1], "ref": ref, "value": val,
            "at": (num(at[1]), num(at[2]), num(at[3]) if len(at) > 3 else 0.0),
            "mirror": mir[1] if mir else None,
            "unit": int(unit[1]) if unit else 1,
            "style": int(style[1]) if style else 1,
        })
    wires = []
    for w in kids(root, "wire"):
        xy = kids(kid(w, "pts"), "xy")
        a, b = (num(xy[0][1]), num(xy[0][2])), (num(xy[1][1]), num(xy[1][2]))
        wires.append((min(a[0], b[0]) - 0.15, min(a[1], b[1]) - 0.15,
                      max(a[0], b[0]) + 0.15, max(a[1], b[1]) + 0.15))
    labels = []
    for h in ("label", "hierarchical_label", "global_label"):
        for l in kids(root, h):
            at, txt = kid(l, "at"), l[1][1]
            x, y, a = num(at[1]), num(at[2]), num(at[3]) if len(at) > 3 else 0
            wd = len(txt) * RULES["char_w"] + 2.0
            if a == 180:
                labels.append((x - wd, y - 0.9, x, y + 0.9))
            elif a == 0:
                labels.append((x, y - 0.9, x + wd, y + 0.9))
    for t in kids(root, "text"):
        at, txt = kid(t, "at"), t[1][1]
        x, y = num(at[1]), num(at[2])
        labels.append((x, y - 1.5, x + len(txt) * 2.0, y + 1.5))
    return text, libs, insts, wires, labels


def analyse(inst, libs):
    sym = libs.get(inst["lib_id"])
    if sym is None:
        return None
    pts, pins = lib_points(sym, inst["unit"], inst["style"])
    if not pts:
        return None
    sp = [to_sheet(p, inst["at"], inst["mirror"]) for p in pts]
    pp = [to_sheet(p, inst["at"], inst["mirror"]) for p in pins]
    return {"bbox": bbox(sp), "pins": pp}


def category(inst, info):
    lid, ref = inst["lib_id"], inst["ref"] or ""
    if lid.startswith("power:") or ref.startswith("#"):
        return "gnd" if "GND" in lid.upper() or "GND" in inst["value"].upper() else "power"
    pins = {(round(x, 2), round(y, 2)) for x, y in info["pins"]}
    prefix = re.match(r"[A-Za-z]+", ref).group(0) if re.match(r"[A-Za-z]+", ref) else ""
    if len(pins) == 2 and prefix not in ("J", "SW", "BZ", "LS"):
        (x1, y1), (x2, y2) = list(pins)
        return "passive_h" if abs(y1 - y2) < 0.01 else "passive_v"
    if prefix == "Q":
        return "transistor"
    return "other"


def candidates(cat, bb, ref, val, pin_y=None):
    m, ln = RULES["margin"], RULES["line"]
    cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    if cat in ("gnd", "power"):
        below = ((cx, bb[3] + m + 0.8), "center")
        above = ((cx, bb[1] - m - 0.8), "center")
        left = ((bb[0] - m, cy), "right")
        right = ((bb[2] + m, cy), "left")
        # le symbole « pend » sous sa broche (GND, ou +3V0 tourné) -> texte dessous ; sinon dessus
        hangs_down = pin_y is not None and pin_y < cy - 0.01
        order = [below, left, right, above] if hangs_down else [above, left, right, below]
        return [(None, v) for v in order]
    if cat == "passive_h":
        up = (((cx, bb[1] - m - ln), "center"), ((cx, bb[1] - m), "center"))
        dn = (((cx, bb[3] + m), "center"), ((cx, bb[3] + m + ln), "center"))
        inline_up = (((cx - 0.6, bb[1] - m), "right"), ((cx + 0.6, bb[1] - m), "left"))
        inline_dn = (((cx - 0.6, bb[3] + m), "right"), ((cx + 0.6, bb[3] + m), "left"))
        return [up, dn, inline_up, inline_dn]
    if cat in ("passive_v", "transistor"):
        lf = (((bb[0] - m, cy - ln / 2), "right"), ((bb[0] - m, cy + ln / 2), "right"))
        rt = (((bb[2] + m, cy - ln / 2), "left"), ((bb[2] + m, cy + ln / 2), "left"))
        return [lf, rt] if cat == "passive_v" else [rt, lf]
    full = (((cx, bb[1] - m - 0.8), "center"), ((cx, bb[3] + m + 0.8), "center"))
    above2 = (((cx, bb[1] - m - ln), "center"), ((cx, bb[1] - m), "center"))
    below2 = (((cx, bb[3] + m), "center"), ((cx, bb[3] + m + ln), "center"))
    rt = (((bb[2] + m, cy - ln / 2), "left"), ((bb[2] + m, cy + ln / 2), "left"))
    lf = (((bb[0] - m, cy - ln / 2), "right"), ((bb[0] - m, cy + ln / 2), "right"))
    # coins : à gauche / à droite en bas du corps (hors broches), utile quand le haut et les côtés sont encombrés
    lb = (((bb[0] - m, bb[3] - 0.8 - ln), "right"), ((bb[0] - m, bb[3] - 0.8), "right"))
    rb = (((bb[2] + m, bb[3] - 0.8 - ln), "left"), ((bb[2] + m, bb[3] - 0.8), "left"))
    return [full, above2, below2, rb, lb, rt, lf]


def field_angle(rot):
    r = int(round(rot)) % 360
    return (360 - r) % 360 if r in (90, 270) else 0


# --------------------------------------------------------------------- edits
def block_end(t, i):
    d = 0
    for k in range(i, len(t)):
        if t[k] == "(":
            d += 1
        elif t[k] == ")":
            d -= 1
            if d == 0:
                return k + 1
    raise ValueError("parenthèses déséquilibrées")


def set_prop(t, ref, prop, x, y, ang, just, hide):
    m = re.search(r'\(property "Reference" "%s"' % re.escape(ref), t)
    if not m:
        return t
    p = m.start()
    if prop != "Reference":
        p = t.index('(property "%s"' % prop, p)
    e = block_end(t, p)
    val = re.match(r'\(property "[^"]+" "([^"]*)"', t[p:e]).group(1)
    eff = "\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n"
    if just != "center":
        eff += "\t\t\t\t(justify %s)\n" % just
    if hide:
        eff += "\t\t\t\t(hide yes)\n"
    eff += "\t\t\t)\n"
    new = ('(property "%s" "%s"\n\t\t\t(at %s %s %s)\n\t\t\t(show_name no)\n'
           '\t\t\t(do_not_autoplace no)\n%s\t\t)' % (prop, val, round(x, 2), round(y, 2), ang, eff))
    return t[:p] + new + t[e:]


def check_spacing(insts, infos):
    """Avertit quand deux passifs voisins sont trop serrés pour que leurs textes tiennent.

    Passifs verticaux alignés sur une même ligne (même y) : pas minimal =
    demi-largeurs des corps + largeur du plus long texte + 2 marges.
    Passifs horizontaux alignés dans une même colonne (même x) : pas minimal =
    demi-hauteurs des corps + 2 lignes de texte + 1 marge.
    Le pas conseillé est arrondi au multiple de 2,54 mm supérieur.
    """
    m, ln = RULES["margin"], RULES["line"]
    rows = {}
    for i in insts:
        info = infos.get(i["ref"])
        if info is None or i["ref"].startswith("#"):
            continue
        cat = category(i, info)
        if cat not in ("passive_h", "passive_v"):
            continue
        bb = info["bbox"]
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        key = (cat, round(cy) if cat == "passive_v" else round(cx))
        rows.setdefault(key, []).append((cx if cat == "passive_v" else cy, bb, i))
    warns = []
    for (cat, _), items in rows.items():
        items.sort(key=lambda t: t[0])
        for (pa, ba, ia), (pb, bb_, ib) in zip(items, items[1:]):
            tw = max(len(ia["ref"]), len(ia["value"]), len(ib["ref"]), len(ib["value"])) * RULES["char_w"]
            if cat == "passive_v":
                need = (ba[2] - ba[0]) / 2 + (bb_[2] - bb_[0]) / 2 + tw + 2 * m
            else:
                need = (ba[3] - ba[1]) / 2 + (bb_[3] - bb_[1]) / 2 + 2 * ln + m
            if pb - pa < need - 0.01:
                rec = math.ceil(need / 2.54) * 2.54
                warns.append("ESPACEMENT %s et %s : pas %.2f mm < %.2f mm nécessaires, conseillé %.2f mm"
                             % (ia["ref"], ib["ref"], pb - pa, need, rec))
    return warns


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("schema")
    ap.add_argument("--refs", help="repères à traiter, séparés par des virgules")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    text, libs, insts, wires, labels = load(a.schema)
    only = set(a.refs.split(",")) if a.refs else None
    infos = {}
    for i in insts:
        infos[i["ref"]] = analyse(i, libs)
    placed = []  # boîtes de texte déjà placées
    report = []
    for i in insts:
        info = infos[i["ref"]]
        if info is None or (only and i["ref"] not in only):
            continue
        cat = category(i, info)
        bb = info["bbox"]
        obstacles = list(wires) + list(labels) + placed
        for j in insts:
            if j is not i and infos[j["ref"]] is not None:
                obstacles.append(infos[j["ref"]]["bbox"])
        ang = field_angle(i["at"][2])
        best, bestn = None, None
        pin_y = info["pins"][0][1] if info["pins"] else None
        for cand in candidates(cat, bb, i["ref"], i["value"], pin_y):
            if cat in ("gnd", "power"):
                refp, valp = None, cand[1]
                boxes = [text_box(*valp[0], i["value"], valp[1])]
                choice = (None, valp)
            else:
                refp, valp = cand
                boxes = [text_box(*refp[0], i["ref"], refp[1])]
                if valp:
                    boxes.append(text_box(*valp[0], i["value"], valp[1]))
                choice = (refp, valp)
            pd = RULES["pad"]
            n = sum(1 for b in boxes for o in obstacles
                    if inter((b[0] - pd, b[1] - pd, b[2] + pd, b[3] + pd), o))
            if best is None or n < bestn:
                best, bestn = (choice, boxes), n
            if n == 0:
                break
        (refp, valp), boxes = best
        placed += boxes
        if i["ref"].startswith("#"):
            text = set_prop(text, i["ref"], "Reference", i["at"][0], i["at"][1], 0, "center", True)
        elif refp:
            text = set_prop(text, i["ref"], "Reference", refp[0][0], refp[0][1], ang, refp[1], False)
        if valp:
            text = set_prop(text, i["ref"], "Value", valp[0][0], valp[0][1],
                            0 if cat in ("gnd", "power") else ang, valp[1], False)
        report.append("%-8s %-11s collisions=%d" % (i["ref"], cat, bestn))
    print("\n".join(report))
    for w in check_spacing(insts, infos):
        print(w)
    if not a.dry_run:
        open(a.schema, "w", encoding="utf8").write(text)


if __name__ == "__main__":
    sys.exit(main())
