"""Partie KiCad du banc (Python embarque KiCad 10, module pcbnew). Appele par bench_eval.py.

  stats <carte.kicad_pcb> <sortie.json>        positions, rotation, face, verrou ; pistes et vias
  dsn   <carte.kicad_pcb> <sortie.dsn>         export Specctra pour Freerouting
  ses   <carte.kicad_pcb> <session.ses> <sortie.kicad_pcb>   import du routage sur une COPIE

Ne modifie jamais le fichier d'entree (la commande ses ecrit une copie).
"""
import json
import os
import shutil
import sys

import pcbnew


def stats(path, out):
    b = pcbnew.LoadBoard(path)
    fps = {}
    for fp in b.GetFootprints():
        p = fp.GetPosition()
        fps[fp.GetReference()] = {
            "x": round(pcbnew.ToMM(p.x), 4), "y": round(pcbnew.ToMM(p.y), 4),
            "rot": round(fp.GetOrientationDegrees(), 3), "locked": bool(fp.IsLocked()),
            "layer": fp.GetLayerName(),
        }
    length, nseg, nvia = 0.0, 0, 0
    for t in b.GetTracks():
        if t.GetClass() == "PCB_VIA":
            nvia += 1
        else:
            length += pcbnew.ToMM(t.GetLength())
            nseg += 1
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"footprints": fps, "track_length_mm": round(length, 2), "track_segments": nseg,
                   "vias": nvia}, f, indent=1)


def dsn(path, out):
    b = pcbnew.LoadBoard(path)
    ok = pcbnew.ExportSpecctraDSN(b, out)
    print("ExportSpecctraDSN:", ok)
    sys.exit(0 if ok and os.path.exists(out) else 1)


def ses(path, ses_path, out):
    if os.path.abspath(out) == os.path.abspath(path):
        sys.exit("refus : la sortie doit etre une copie")
    shutil.copy2(path, out)
    b = pcbnew.LoadBoard(out)
    ok = pcbnew.ImportSpecctraSES(b, ses_path)
    print("ImportSpecctraSES:", ok)
    b.Save(out)
    sys.exit(0 if ok else 1)


def strip(path, out):
    """Copie de la carte sans pistes ni vias (pour juger le seul placement d'un outil qui route aussi)."""
    if os.path.abspath(out) == os.path.abspath(path):
        sys.exit("refus : la sortie doit etre une copie")
    shutil.copy2(path, out)
    b = pcbnew.LoadBoard(out)
    for t in list(b.GetTracks()):
        b.Remove(t)
    b.Save(out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "strip":
        strip(sys.argv[2], sys.argv[3])
    elif cmd == "stats":
        stats(sys.argv[2], sys.argv[3])
    elif cmd == "dsn":
        dsn(sys.argv[2], sys.argv[3])
    elif cmd == "ses":
        ses(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        sys.exit("commande inconnue : " + cmd)
