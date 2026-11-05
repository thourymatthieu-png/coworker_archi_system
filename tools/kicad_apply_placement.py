"""Applique une solution de placement (JSON produit par tools/pcb_optimize_placement.py) sur
une COPIE du PCB d'origine - ne modifie JAMAIS le fichier source.

A lancer avec le Python embarque de KiCad (celui declare dans KICAD_PYTHON de .claude.json),
car il a besoin du module pcbnew.

Usage:
    <venv_kicad>/python.exe tools/kicad_apply_placement.py <proj.kicad_pcb> <solution.json> <sortie.kicad_pcb>
"""
import json
import os
import shutil
import sys

import pcbnew


def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: kicad_apply_placement.py <proj.kicad_pcb> <solution.json> <sortie.kicad_pcb>")
        sys.exit(1)
    pcb_path, solution_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

    if os.path.abspath(out_path) == os.path.abspath(pcb_path):
        print("Refus : le fichier de sortie doit etre different du fichier source "
              "(le PCB original ne doit jamais etre ecrase directement).")
        sys.exit(1)

    with open(solution_path, "r", encoding="utf-8") as f:
        solution = json.load(f)
    positions = solution["positions"]

    board = pcbnew.LoadBoard(pcb_path)
    applied, skipped_locked, missing = 0, 0, []
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        pos = positions.get(ref)
        if pos is None:
            missing.append(ref)
            continue
        if fp.IsLocked():
            skipped_locked += 1
            continue
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(pos["x_mm"]), pcbnew.FromMM(pos["y_mm"])))
        fp.SetOrientationDegrees(pos["rotation_deg"])
        applied += 1

    # Copie d'abord le fichier tel quel (conserve toutes les sections non touchees :
    # contour, regles, classes de reseau...), puis ecrit les positions par-dessus la copie
    # pour rester au plus proche d'une simple "mise a jour de positions" plutot qu'une
    # reecriture complete du fichier par pcbnew.
    shutil.copy2(pcb_path, out_path)
    board2 = pcbnew.LoadBoard(out_path)
    for fp in board2.GetFootprints():
        ref = fp.GetReference()
        pos = positions.get(ref)
        if pos is None or fp.IsLocked():
            continue
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(pos["x_mm"]), pcbnew.FromMM(pos["y_mm"])))
        fp.SetOrientationDegrees(pos["rotation_deg"])
    board2.Save(out_path)

    print(f"Positions appliquees : {applied}")
    print(f"Ignorees (verrouillees dans KiCad) : {skipped_locked}")
    print(f"Sans position dans la solution : {missing}")
    print(f"Ecrit : {out_path} (fichier source {pcb_path} non modifie)")


if __name__ == "__main__":
    main()
