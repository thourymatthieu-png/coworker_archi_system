"""Extraction unique de la geometrie du PCB pour le placement "tetris" (essai, lecture seule).

A lancer avec le Python embarque de KiCad (celui declare dans KICAD_PYTHON de .claude.json),
car il a besoin du module pcbnew. Ne modifie JAMAIS le fichier .kicad_pcb (LoadBoard seul,
pas de Save).

Usage:
    <venv_kicad>/python.exe modules/kicad/tools/kicad_tetris_extract.py <proj.kicad_pcb> <sortie.json>
      [--sheet-map <fichier_json_optionnel>]

Sortie JSON: liste de composants avec reference, valeur, bloc fonctionnel, position/rotation
actuelles (lecture seule, pour les ancres), rectangle d'encombrement (courtyard) en repere
LOCAL non tourne (w, h, offset du centre du rectangle par rapport a l'origine du footprint -
en general (0,0) mais garde par securite), liste des pastilles (nom, reseau, offset local
x/y par rapport au centre du footprint, dans le repere non tourne).

Le bloc fonctionnel (une feuille hierarchique du schema) n'est pas porte par les proprietes
Sheetfile des empreintes est lu d'abord (rempli par la mise a jour du PCB depuis l'interface de
KiCad, mais vide apres la synchronisation du serveur MCP, constate le 2026-11-05). A defaut, le bloc
est deduit des feuilles .kicad_sch du dossier du PCB et de ses sous-dossiers : toute reference
annotee d'une feuille appartient au bloc qui porte le nom du fichier (sans extension).
--sheet-map (JSON {"reference": "bloc"}) a le dernier mot.
"""
import argparse
import json
import os
import re

import pcbnew

REF_PROP_RE = re.compile(r'\(property\s+"Reference"\s+"([A-Za-z]+[0-9]+)"')
REF_INST_RE = re.compile(r'\(reference\s+"([A-Za-z]+[0-9]+)"\)')


def ref_to_block_from_schematics(sch_dir):
    """Reference -> bloc, d'apres les feuilles .kicad_sch du dossier et de ses sous-dossiers
    (proprietes Reference et references d'instance des feuilles utilisees plusieurs fois)."""
    mapping, duplicates = {}, []
    for root, _dirs, files in os.walk(sch_dir):
        for name in sorted(files):
            if not name.endswith(".kicad_sch"):
                continue
            block = name[:-len(".kicad_sch")]
            with open(os.path.join(root, name), encoding="utf-8") as f:
                text = f.read()
            for ref in set(REF_PROP_RE.findall(text)) | set(REF_INST_RE.findall(text)):
                if ref in mapping and mapping[ref] != block:
                    duplicates.append(ref)
                mapping.setdefault(ref, block)
    return mapping, sorted(set(duplicates))


def sheetfile_block(fp):
    """Bloc porte par l'empreinte (champ Sheetfile, rempli par la mise a jour du PCB depuis
    l'interface de KiCad), ou None s'il est vide ou absent."""
    getter = getattr(fp, "GetSheetfile", None)
    value = getter() if getter else ""
    if not value:
        return None
    return os.path.splitext(os.path.basename(value))[0]


def mm(iu):
    return pcbnew.ToMM(iu)


def rotate_point(x, y, angle_deg):
    """Tourne (x, y) de angle_deg autour de l'origine (degres, sens horaire KiCad)."""
    import math
    a = math.radians(angle_deg)
    cos_a, sin_a = math.cos(a), math.sin(a)
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)


def unrotate_point(x, y, angle_deg):
    return rotate_point(x, y, -angle_deg)


def get_local_courtyard_bbox(fp):
    """Boite englobante du courtyard (F.CrtYd ou B.CrtYd) dans le repere LOCAL non tourne du
    footprint (centre = position actuelle du footprint, axes alignes a la rotation actuelle
    retiree). Retourne (w_mm, h_mm, cx_mm, cy_mm) avec cx/cy = offset du centre du rectangle
    par rapport au centre du footprint (en general ~0,0)."""
    pos = fp.GetPosition()
    cx_board, cy_board = mm(pos.x), mm(pos.y)
    rot = fp.GetOrientationDegrees()

    pts_local = []
    for item in fp.GraphicalItems():
        layer = item.GetLayer()
        if layer not in (pcbnew.F_CrtYd, pcbnew.B_CrtYd):
            continue
        shape = item
        # PCB_SHAPE : recuperer les points via GetStart/GetEnd/GetCenter/GetArcMid, et pour
        # les polygones GetPolyShape si dispo.
        try:
            poly = shape.GetPolyShape()
            if poly is not None and poly.OutlineCount() > 0:
                outline = poly.Outline(0)
                for i in range(outline.PointCount()):
                    p = outline.CPoint(i)
                    pts_local.append((mm(p.x), mm(p.y)))
                continue
        except Exception:
            pass
        for getter in ("GetStart", "GetEnd", "GetCenter"):
            try:
                p = getattr(shape, getter)()
                pts_local.append((mm(p.x), mm(p.y)))
            except Exception:
                pass

    if not pts_local:
        # Repli : bounding box pcbnew standard (moins precis, mais evite un bloc sans taille).
        bbox = fp.GetBoundingBox()
        w = mm(bbox.GetWidth())
        h = mm(bbox.GetHeight())
        return (w, h, 0.0, 0.0)

    # pts_local sont en coordonnees absolues de la carte -> ramener au centre du footprint,
    # puis retirer la rotation actuelle pour obtenir un repere canonique (0 deg).
    rel = [(x - cx_board, y - cy_board) for (x, y) in pts_local]
    unrot = [unrotate_point(x, y, rot) for (x, y) in rel]
    xs = [p[0] for p in unrot]
    ys = [p[1] for p in unrot]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    w = xmax - xmin
    h = ymax - ymin
    ctr_x = (xmin + xmax) / 2.0
    ctr_y = (ymin + ymax) / 2.0
    return (w, h, ctr_x, ctr_y)


def get_pads(fp):
    pos = fp.GetPosition()
    cx_board, cy_board = mm(pos.x), mm(pos.y)
    rot = fp.GetOrientationDegrees()
    pads = []
    for pad in fp.Pads():
        ppos = pad.GetPosition()
        px, py = mm(ppos.x), mm(ppos.y)
        rel = (px - cx_board, py - cy_board)
        unrot = unrotate_point(rel[0], rel[1], rot)
        net = pad.GetNetname()
        pads.append({
            "name": pad.GetPadName(),
            "net": net,
            "x": round(unrot[0], 4),
            "y": round(unrot[1], 4),
        })
    return pads


def main():
    ap = argparse.ArgumentParser(description="Extraction de la geometrie d'un PCB KiCad (lecture seule).")
    ap.add_argument("pcb", help="fichier .kicad_pcb")
    ap.add_argument("sortie", help="fichier JSON a ecrire")
    ap.add_argument("--sheet-map", help='JSON {"reference": "bloc"} prioritaire sur Sheetfile et sur la deduction depuis les feuilles')
    args = ap.parse_args()
    pcb_path, out_path = args.pcb, args.sortie

    ref_to_block, duplicates = ref_to_block_from_schematics(os.path.dirname(os.path.abspath(pcb_path)))
    if duplicates:
        print("References presentes dans plusieurs feuilles (premiere feuille retenue):", duplicates)
    override = {}
    if args.sheet_map:
        with open(args.sheet_map, encoding="utf-8") as f:
            override = json.load(f)

    board = pcbnew.LoadBoard(pcb_path)  # lecture seule, aucun Save.

    components = []
    missing_block = []
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        val = fp.GetValue()
        pos = fp.GetPosition()
        x_mm, y_mm = mm(pos.x), mm(pos.y)
        rot = fp.GetOrientationDegrees()
        w, h, ctr_x, ctr_y = get_local_courtyard_bbox(fp)
        pads = get_pads(fp)
        block = override.get(ref) or sheetfile_block(fp) or ref_to_block.get(ref)
        if block is None:
            missing_block.append(ref)
            block = "INCONNU"
        components.append({
            "ref": ref,
            "value": val,
            "block": block,
            "is_anchor": bool(fp.IsLocked()),  # fixe = empreinte verrouillee dans KiCad
            "current_x_mm": round(x_mm, 4),
            "current_y_mm": round(y_mm, 4),
            "current_rotation_deg": rot,
            "courtyard_w_mm": round(w, 4),
            "courtyard_h_mm": round(h, 4),
            "courtyard_center_offset_x_mm": round(ctr_x, 4),
            "courtyard_center_offset_y_mm": round(ctr_y, 4),
            "pads": pads,
        })

    board_extents = board.GetBoardEdgesBoundingBox()
    # Contour = rectangle(s) Edge.Cuts dessine(s) dans KiCad (contrainte dure si trouve).
    edge = [d for d in board.GetDrawings() if d.GetLayerName() == "Edge.Cuts"]
    outline = None
    if edge:
        bb = edge[0].GetBoundingBox()
        for d in edge[1:]:
            bb.Merge(d.GetBoundingBox())
        outline = [round(mm(bb.GetX()), 4), round(mm(bb.GetY()), 4),
                   round(mm(bb.GetX() + bb.GetWidth()), 4), round(mm(bb.GetY() + bb.GetHeight()), 4)]
    data = {
        "source_pcb": os.path.abspath(pcb_path),
        "note": "Extraction en lecture seule, aucune modification du .kicad_pcb.",
        "board_outline_bbox_mm": {
            "x_mm": mm(board_extents.GetX()),
            "y_mm": mm(board_extents.GetY()),
            "w_mm": mm(board_extents.GetWidth()),
            "h_mm": mm(board_extents.GetHeight()),
        },
        "outline_mm": outline,
        "components": components,
        "missing_block_refs": missing_block,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("Composants extraits:", len(components))
    print("Sans bloc identifie:", missing_block)
    print("Ecrit:", out_path)


if __name__ == "__main__":
    main()
