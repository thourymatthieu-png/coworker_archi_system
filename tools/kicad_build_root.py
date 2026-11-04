#!/usr/bin/env python3
"""Reconstruit la page racine d'un projet KiCad hiérarchique : une case par
feuille, ses broches de feuille déduites des étiquettes hiérarchiques de la
sous-feuille, et une étiquette locale au bout de chaque broche. Les broches de
même nom se retrouvent reliées par leur nom, sans fil entre les cases.

Usage :
    python tools/kicad_build_root.py <dossier_projet_kicad> [--title "Titre"]

À relancer après toute modification des étiquettes hiérarchiques d'une feuille.
Conserve les UUID et les chemins d'instance des feuilles existantes (les
feuilles doivent d'abord avoir été créées par `create_hierarchical_subsheet`).
La disposition est dans LAYOUT (colonne, ligne) ; une feuille inconnue est
placée à la suite.
"""
import argparse
import glob
import os
import re
import uuid

PAPER = "A3"
COL_X = [38.1, 139.7, 241.3, 342.9]
ROW_Y = [45.72, 106.68, 167.64]
# nom de fichier -> (colonne, ligne)
LAYOUT = {
    "des-008-batterie-xt30.kicad_sch": (0, 0), "des-009-regulateur-pont.kicad_sch": (1, 0),
    "des-010-bouton.kicad_sch": (2, 0), "des-011-voyant-buzzer.kicad_sch": (3, 0),
    "des-003-centrale-inertielle.kicad_sch": (0, 1), "des-005-flux-optique.kicad_sch": (1, 1),
    "des-004-capteur-hauteur.kicad_sch": (2, 1), "des-012-module-bluetooth.kicad_sch": (3, 1),
    "des-007-puissance-moteurs.kicad_sch": (0, 2), "des-002-microcontroleur.kicad_sch": (1, 2),
}
BOX_W = 38.1
STUB = 15.24   # le texte de la broche est dessiné hors de la case : la bague doit le dépasser


def uid():
    return str(uuid.uuid4())


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


def fmt(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def labels_of(path):
    t = open(path, encoding="utf8").read()
    out = []
    for m in re.finditer(r'\(hierarchical_label "([^"]+)"\s*\(shape (\w+)\)\s*\(at ([\d.\-]+) ([\d.\-]+)', t):
        out.append((m.group(1), m.group(2), float(m.group(4)), float(m.group(3))))
    out.sort(key=lambda r: (r[2], r[3]))
    return [(n, s) for n, s, _, _ in out]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("projet")
    ap.add_argument("--title", default="Schema racine - index des feuilles")
    a = ap.parse_args()
    root_path = glob.glob(os.path.join(a.projet, "*.kicad_sch"))
    pro = glob.glob(os.path.join(a.projet, "*.kicad_pro"))[0]
    root_path = os.path.join(a.projet, os.path.splitext(os.path.basename(pro))[0] + ".kicad_sch")
    t = open(root_path, encoding="utf8").read()

    # 1) relever puis retirer les blocs (sheet ...)
    sheets, out, i = [], [], 0
    while True:
        m = re.search(r"\n\s*\(sheet\s*\(at", t[i:])
        if not m:
            out.append(t[i:])
            break
        s = i + m.start() + 1
        s0 = s + (len(t[s:]) - len(t[s:].lstrip()))
        e = block_end(t, s0)
        blk = t[s0:e]
        out.append(t[i:s0])
        sheets.append({
            "uuid": re.search(r'\(uuid "([^"]+)"\)', blk).group(1),
            "name": re.search(r'\(property "Sheetname" "([^"]*)"', blk).group(1),
            "file": re.search(r'\(property "Sheetfile" "([^"]*)"', blk).group(1),
            "instances": re.search(r"\(instances.*\)\s*(?=\(pin|\)\s*$)", blk, re.S).group(0).strip()
            if "(instances" in blk else "",
        })
        # instances : récupérer le bloc complet par appariement
        k = blk.index("(instances")
        sheets[-1]["instances"] = blk[k:block_end(blk, k)]
        i = e
    t = "".join(out)

    # 1bis) purger les fils, étiquettes, jonctions et textes d'un passage précédent
    out, i = [], 0
    while True:
        m = re.search(r"\n\s*\((wire|label|junction|text)\b", t[i:])
        if not m:
            out.append(t[i:])
            break
        s = i + m.start() + 1
        s0 = s + (len(t[s:]) - len(t[s:].lstrip()))
        out.append(t[i:s0])
        i = block_end(t, s0)
    t = "".join(out)

    # 2) générer les nouveaux blocs
    free = [(c, r) for r in range(len(ROW_Y)) for c in range(len(COL_X))
            if (c, r) not in LAYOUT.values()]
    new = []
    for sh in sheets:
        c, r = LAYOUT.get(sh["file"]) or free.pop(0)
        labs = labels_of(os.path.join(a.projet, sh["file"]))
        left = [(n, s) for n, s in labs if s == "input"]
        right = [(n, s) for n, s in labs if s != "input"]
        h = max(15.24, round((max(len(left), len(right)) * 2.54 + 7.62) / 2.54 + 0.4) * 2.54)
        x, y = COL_X[c], ROW_Y[r]
        b = ["  (sheet (at %s %s) (size %s %s) (fields_autoplaced yes)" % (fmt(x), fmt(y), fmt(BOX_W), fmt(h)),
             "    (stroke (width 0.0006) (type default))",
             "    (fill (color 0 0 0 0.0000))",
             '    (uuid "%s")' % sh["uuid"],
             '    (property "Sheetname" "%s" (at %s %s 0)' % (sh["name"], fmt(x + 2.54), fmt(y - 1.27)),
             "      (effects (font (size 1.27 1.27)) (justify left bottom))", "    )",
             '    (property "Sheetfile" "%s" (at %s %s 0)' % (sh["file"], fmt(x + 2.54), fmt(y + h + 1.27)),
             "      (effects (font (size 1.27 1.27)) (justify left top))", "    )",
             "    " + sh["instances"].replace("\n", "\n    ")]
        wires = []
        for side, items in (("L", left), ("R", right)):
            for k, (n, s) in enumerate(items):
                py = y + 5.08 + 2.54 * k
                px = x if side == "L" else x + BOX_W
                rot = 180 if side == "L" else 0
                just = "right" if side == "L" else "left"
                b += ['    (pin "%s" %s (at %s %s %d)' % (n, s, fmt(px), fmt(py), rot),
                      '      (uuid "%s")' % uid(),
                      "      (effects (font (size 1.27 1.27)) (justify %s))" % just, "    )"]
                ex = px - STUB if side == "L" else px + STUB
                wires.append((px, py, ex, n, rot))
        b.append("  )")
        new.append("\n".join(b))
        for px, py, ex, n, rot in wires:
            new.append("  (wire (pts (xy %s %s) (xy %s %s)) (stroke (width 0) (type default)) (uuid \"%s\"))"
                       % (fmt(px), fmt(py), fmt(ex), fmt(py), uid()))
            new.append('  (label "%s" (at %s %s %d) (effects (font (size 1.27 1.27)) (justify %s bottom)) (uuid "%s"))'
                       % (n, fmt(ex), fmt(py), rot, "right" if rot == 180 else "left", uid()))
    new.append('  (text "%s" (exclude_from_sim no) (at 38.1 25.4 0) '
               '(effects (font (size 2.5 2.5) (bold yes)) (justify left)) (uuid "%s"))' % (a.title, uid()))

    k = re.search(r"\n\s*\(sheet_instances", t).start() + 1
    t = t[:k] + "\n".join(new) + "\n" + t[k:]
    t = re.sub(r'\(paper "[^"]*"\)', '(paper "%s")' % PAPER, t, count=1)
    open(root_path, "w", encoding="utf8").write(t)
    print("%d feuilles reconstruites dans %s" % (len(sheets), os.path.basename(root_path)))


if __name__ == "__main__":
    main()
