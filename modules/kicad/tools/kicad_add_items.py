#!/usr/bin/env python3
"""Ajoute en une fois des fils, étiquettes hiérarchiques, étiquettes locales,
croix de non-connexion et jonctions à une feuille KiCad (.kicad_sch).

Pourquoi : le serveur MCP ne sait poser qu'un élément par appel ; une feuille
de microcontrôleur en demande une centaine. Ce script écrit les mêmes objets
directement dans le fichier (même format que ceux écrits par le serveur).

Usage :
    python modules/kicad/tools/kicad_add_items.py <feuille.kicad_sch> <spec.json>

spec.json :
{
  "wires":      [ [[x1,y1],[x2,y2],[x3,y3]], ... ],     # polylignes (un segment par couple de points)
  "hlabels":    [ ["NOM", "input|output|bidirectional", x, y, angle], ... ],   # angle 0 ou 180
  "labels":     [ ["NOM", x, y, angle], ... ],           # étiquettes locales, angle 0 ou 180
  "noconnects": [ [x, y], ... ],
  "junctions":  [ [x, y], ... ]
}
Coordonnées en mm, telles que données par get_schematic_pin_locations.
"""
import json
import re
import sys
import uuid


def uid():
    return str(uuid.uuid4())


def fmt(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def wire(a, b):
    return ("\t(wire\n\t\t(pts\n\t\t\t(xy %s %s) (xy %s %s)\n\t\t)\n\t\t(stroke\n\t\t\t(width 0)\n"
            "\t\t\t(type default)\n\t\t)\n\t\t(uuid \"%s\")\n\t)\n" % (fmt(a[0]), fmt(a[1]), fmt(b[0]), fmt(b[1]), uid()))


def effects(angle, extra=""):
    j = "right" if int(angle) == 180 else "left"
    return ("\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify %s%s)\n\t\t)\n" % (j, extra))


def hlabel(name, shape, x, y, angle):
    return ("\t(hierarchical_label \"%s\"\n\t\t(shape %s)\n\t\t(at %s %s %d)\n%s\t\t(uuid \"%s\")\n\t)\n"
            % (name, shape, fmt(x), fmt(y), angle, effects(angle), uid()))


def label(name, x, y, angle):
    return ("\t(label \"%s\"\n\t\t(at %s %s %d)\n%s\t\t(uuid \"%s\")\n\t)\n"
            % (name, fmt(x), fmt(y), angle, effects(angle, " bottom"), uid()))


def noconnect(x, y):
    return "\t(no_connect\n\t\t(at %s %s)\n\t\t(uuid \"%s\")\n\t)\n" % (fmt(x), fmt(y), uid())


def junction(x, y):
    return ("\t(junction\n\t\t(at %s %s)\n\t\t(diameter 0)\n\t\t(color 0 0 0 0)\n\t\t(uuid \"%s\")\n\t)\n"
            % (fmt(x), fmt(y), uid()))


def main():
    path, specpath = sys.argv[1], sys.argv[2]
    spec = json.load(open(specpath, encoding="utf8"))
    out = ""
    for poly in spec.get("wires", []):
        for a, b in zip(poly, poly[1:]):
            out += wire(a, b)
    for n, s, x, y, ang in spec.get("hlabels", []):
        out += hlabel(n, s, x, y, ang)
    for n, x, y, ang in spec.get("labels", []):
        out += label(n, x, y, ang)
    for x, y in spec.get("noconnects", []):
        out += noconnect(x, y)
    for x, y in spec.get("junctions", []):
        out += junction(x, y)
    text = open(path, encoding="utf8").read()
    k = re.search(r"\n[ \t]*\(sheet_instances", text).start() + 1
    open(path, "w", encoding="utf8").write(text[:k] + out + text[k:])
    print("ajoutés : %d fils, %d étiq. hiérarchiques, %d étiq. locales, %d NC, %d jonctions" % (
        sum(len(p) - 1 for p in spec.get("wires", [])), len(spec.get("hlabels", [])),
        len(spec.get("labels", [])), len(spec.get("noconnects", [])), len(spec.get("junctions", []))))


if __name__ == "__main__":
    main()
