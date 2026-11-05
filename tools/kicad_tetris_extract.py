"""Extraction unique de la geometrie du PCB pour le placement "tetris" (essai, lecture seule).

A lancer avec le Python embarque de KiCad (celui declare dans KICAD_PYTHON de .claude.json),
car il a besoin du module pcbnew. Ne modifie JAMAIS le fichier .kicad_pcb (LoadBoard seul,
pas de Save).

Usage:
    <venv_kicad>/python.exe tools/kicad_tetris_extract.py <proj.kicad_pcb> <sortie.json>
      [--sheet-map <fichier_json_optionnel>]

Sortie JSON: liste de composants avec reference, valeur, bloc fonctionnel, position/rotation
actuelles (lecture seule, pour les ancres), rectangle d'encombrement (courtyard) en repere
LOCAL non tourne (w, h, offset du centre du rectangle par rapport a l'origine du footprint -
en general (0,0) mais garde par securite), liste des pastilles (nom, reseau, offset local
x/y par rapport au centre du footprint, dans le repere non tourne).

Le bloc fonctionnel (feuille de schema DES-xxx) n'est PAS porte par les proprietes
Sheetname/Sheetfile du footprint sur ce projet (champs vides constate le 2026-11-05) : ces
proprietes ne sont visiblement pas renseignees par la synchronisation schema->PCB utilisee ici.
Contournement repris d'une tache precedente : correspondance reference -> bloc obtenue en
listant les references "(property "Reference" "...")" presentes dans chaque fichier de
sous-feuille .kicad_sch (grep), table ecrite en dur ci-dessous (REF_TO_BLOCK). A refaire si de
nouveaux composants sont ajoutes au schema.
"""
import json
import sys
import os

import pcbnew

# Table de correspondance reference -> bloc fonctionnel (DES-xxx), construite par lecture des
# fichiers de sous-feuille .kicad_sch (grep des proprietes Reference), 2026-11-05.
REF_TO_BLOCK = {}


def _register(block, refs):
    for r in refs:
        REF_TO_BLOCK[r] = block


_register("DES-002-microcontroleur", [
    "C27", "C28", "C29", "C30", "C31", "C32", "C33", "C34", "C35",
    "J2", "R31", "U1",
])
_register("DES-003-centrale-inertielle", ["C19", "C20", "C21", "R24", "U2"])
_register("DES-004-capteur-hauteur", ["C22", "C23", "C24", "R25", "R26", "R27", "R28", "U3"])
_register("DES-005-flux-optique", [
    "C13", "C14", "C15", "C16", "C17", "C18", "R22", "R23",
    "TP1", "TP2", "TP3", "TP4", "TP5", "TP6", "U4", "U6",
])
_register("DES-007-puissance-moteurs", [
    "C2", "C3", "C4", "C5", "C6", "C7", "C9",
    "D1", "D2", "D3", "D4",
    "M1", "M2", "M3", "M4",
    "Q1", "Q2", "Q3", "Q4",
    "R3", "R4", "R5", "R6", "R7", "R8", "R29", "R30",
    "TP11",
])
_register("DES-008-batterie-xt30", ["C8", "FB1", "J1"])
_register("DES-009-regulateur-pont", ["C10", "C11", "C12", "R20", "R21", "U5"])
_register("DES-010-bouton", ["C1", "R1", "R2", "SW1"])
_register("DES-011-voyant-buzzer", [
    "BZ1", "D5", "LED1", "Q5", "Q6", "Q7", "Q8",
    "R9", "R10", "R11", "R12", "R13", "R14", "R15", "R16", "R17", "R18", "R19",
])
_register("DES-012-module-bluetooth", ["C36", "C37", "TP7", "TP8", "TP9", "TP10", "U7"])

# Ancres fixes (contrainte mecanique dure) : ne jamais faire partie du tassement "tetris".
ANCHOR_REFS = {"J1", "M1", "M2", "M3", "M4", "U7"}


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
    if len(sys.argv) < 3:
        print("Usage: kicad_tetris_extract.py <proj.kicad_pcb> <sortie.json>")
        sys.exit(1)
    pcb_path = sys.argv[1]
    out_path = sys.argv[2]

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
        block = REF_TO_BLOCK.get(ref)
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
