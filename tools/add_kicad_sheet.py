#!/usr/bin/env python3
"""Ajoute une feuille hiérarchique KiCad (une page par bloc) à un projet, en
contournant le bug de `kicad_workflow`/`kicad_schematic_edit` opération
`add_sheet` du MCP kicad (« 'SheetManager' object has no attribute 'add' »).

Écrit directement le bloc (sheet ...) dans le schéma racine, met à jour la
clé "sheets" du .kicad_pro, et crée un fichier de sous-feuille minimal (prêt
à être rempli avec kicad_schematic_edit load / add_component / ...).

Usage :
    python tools/add_kicad_sheet.py <dossier_projet_kicad> \
        --name "DES-011 — Circuit du voyant RGB et du buzzer" \
        --file des-011-voyant-buzzer.kicad_sch \
        --pin PB1:bidirectional --pin PB2:bidirectional --pin PB10:bidirectional \
        --pin PB11:bidirectional \
        [--paper A4|A3]

Après coup :
    python tools/fix_kicad_project_uuid.py <dossier_projet_kicad> --check
    (la cohérence racine n'est pas touchée par ce script, mais le vérifier
    reste une bonne habitude après toute manipulation du projet)
    python -c "..." kicad_schematic_edit load <sous-feuille>, puis saisir les
    composants normalement, puis kicad_schematic erc sur le schéma racine.
"""
import argparse
import json
import re
import sys
import uuid
from pathlib import Path

PAPER_SIZE = {"A4": (297, 210), "A3": (420, 297)}
SHEET_BOX_W, SHEET_BOX_H = 70, 45  # mm, taille des cases sur la page d'index
MARGIN_X, MARGIN_Y = 20, 20
COLS = 3


def find_root(project_dir):
    pros = sorted(project_dir.glob("*.kicad_pro"))
    if len(pros) != 1:
        sys.exit(f"Attendu un seul .kicad_pro dans {project_dir}, trouvé {len(pros)}")
    pro = pros[0]
    root_sch = pro.with_suffix(".kicad_sch")
    if not root_sch.exists():
        sys.exit(f"{root_sch} introuvable")
    return pro, root_sch


def existing_sheet_count(root_text):
    return len(re.findall(r"^\t\(sheet\n", root_text, flags=re.M))


def next_box_position(index):
    col = index % COLS
    row = index // COLS
    x = MARGIN_X + col * (SHEET_BOX_W + 15)
    y = MARGIN_Y + 15 + row * (SHEET_BOX_H + 15)
    return x, y


def sheet_block(sheet_uuid, name, filename, x, y, w, h, pins, root_uuid, page, project_name):
    pin_blocks = []
    pin_y = y + 8
    for pname, shape in pins:
        pin_blocks.append(
            f'\t\t(pin "{pname}" {shape}\n'
            f"\t\t\t(at {x} {pin_y} 180)\n"
            f"\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify right)\n\t\t\t)\n"
            f'\t\t\t(uuid "{uuid.uuid4()}")\n'
            f"\t\t)\n"
        )
        pin_y += 5.08
    pins_text = "".join(pin_blocks)
    return (
        f"\t(sheet\n"
        f"\t\t(at {x} {y})\n"
        f"\t\t(size {w} {h})\n"
        f"\t\t(fields_autoplaced yes)\n"
        f"\t\t(stroke\n\t\t\t(width 0.1524)\n\t\t\t(type solid)\n\t\t)\n"
        f"\t\t(fill\n\t\t\t(color 0 0 0 0.0000)\n\t\t)\n"
        f'\t\t(uuid "{sheet_uuid}")\n'
        f'\t\t(property "Sheetname" "{name}"\n'
        f"\t\t\t(at {x} {y - 0.8} 0)\n"
        f"\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify left bottom)\n\t\t\t)\n\t\t)\n"
        f'\t\t(property "Sheetfile" "{filename}"\n'
        f"\t\t\t(at {x} {y + h + 1.2} 0)\n"
        f"\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify left top)\n\t\t\t)\n\t\t)\n"
        f"{pins_text}"
        f"\t\t(instances\n\t\t\t(project \"{project_name}\"\n"
        f'\t\t\t\t(path "/{root_uuid}"\n'
        f'\t\t\t\t\t(page "{page}")\n'
        f"\t\t\t\t)\n\t\t\t)\n\t\t)\n"
        f"\t)\n"
    )


def subsheet_stub(sheet_uuid, root_uuid, name, paper, page, project_name):
    file_uuid = uuid.uuid4()
    return file_uuid, (
        "(kicad_sch\n"
        "\t(version 20250114)\n"
        '\t(generator "eeschema")\n'
        '\t(generator_version "9.0")\n'
        f'\t(uuid "{file_uuid}")\n'
        f'\t(paper "{paper}")\n'
        "\t(title_block\n"
        f'\t\t(title "{project_name}")\n'
        "\t)\n"
        "\t(lib_symbols\n\t)\n"
        f'\t(text "{name}"\n'
        "\t\t(exclude_from_sim no)\n"
        "\t\t(at 15 10 0.0000)\n"
        "\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 2.5 2.5)\n\t\t\t)\n\t\t)\n"
        f'\t\t(uuid "{uuid.uuid4()}")\n'
        "\t)\n"
        "\t(sheet_instances\n"
        f'\t\t(path "/{sheet_uuid}"\n'
        f'\t\t\t(page "{page}")\n'
        "\t\t)\n\t)\n"
        "\t(embedded_fonts no)\n"
        ")\n"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project_dir", help="dossier du projet KiCad (contient le .kicad_pro)")
    ap.add_argument("--name", required=True, help='nom de la feuille, ex. "DES-011 — Titre"')
    ap.add_argument("--file", required=True, help="nom du fichier .kicad_sch de la sous-feuille")
    ap.add_argument("--pin", action="append", default=[], metavar="NOM:forme",
                     help="broche à exposer sur le symbole de feuille (répétable), forme = input|output|bidirectional|tri_state|passive")
    ap.add_argument("--paper", default="A4", choices=sorted(PAPER_SIZE))
    args = ap.parse_args()

    project_dir = Path(args.project_dir)
    pro, root_sch = find_root(project_dir)
    sub_path = project_dir / args.file
    if sub_path.exists():
        sys.exit(f"{sub_path} existe déjà, choisis un autre nom ou supprime-le d'abord")

    root_text = root_sch.read_text(encoding="utf-8")
    m = re.search(r'\(uuid "([0-9a-fA-F-]{36})"\)', root_text.split("(lib_symbols", 1)[0])
    if not m:
        sys.exit(f"UUID racine introuvable dans {root_sch}")
    root_uuid = m.group(1)

    index = existing_sheet_count(root_text)
    x, y = next_box_position(index)
    page = str(index + 2)  # page 1 = racine

    pins = []
    for p in args.pin:
        if ":" not in p:
            sys.exit(f"--pin {p} : format attendu NOM:forme")
        pname, shape = p.split(":", 1)
        pins.append((pname, shape))

    project_name = pro.stem
    sheet_uuid = uuid.uuid4()
    block = sheet_block(sheet_uuid, args.name, args.file, x, y, SHEET_BOX_W, SHEET_BOX_H, pins, root_uuid, page, project_name)

    if "(sheet_instances" not in root_text:
        sys.exit(f"{root_sch} : pas de (sheet_instances ...), format inattendu")
    root_text = root_text.replace("\t(sheet_instances", block + "\t(sheet_instances", 1)
    root_sch.write_text(root_text, encoding="utf-8")

    file_uuid, sub_text = subsheet_stub(sheet_uuid, root_uuid, args.name, args.paper, page, project_name)
    sub_path.write_text(sub_text, encoding="utf-8")

    pro_data = json.loads(pro.read_text(encoding="utf-8"))
    pro_data.setdefault("sheets", []).append([str(sheet_uuid), args.name])
    pro.write_text(json.dumps(pro_data, indent=2) + "\n", encoding="utf-8")

    print(f"Feuille ajoutée : {root_sch.name} (symbole à {x},{y}) -> {sub_path.name} (page {page})")
    print(f"  UUID feuille (sheet symbol) : {sheet_uuid}")
    print(f"  UUID du fichier de sous-feuille : {file_uuid}")
    print(f"  Chemin d'instance à utiliser dans {sub_path.name} pour chaque composant :")
    print(f'    (path "/{root_uuid}/{sheet_uuid}" (reference "...") (unit 1))')
    print("Prochaine étape : charger la sous-feuille avec kicad_schematic_edit (operation load) et y saisir les composants.")


if __name__ == "__main__":
    main()
