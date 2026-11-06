"""Applique best_solution.json du moteur sur une copie, avec la rotation corrigee.
Le modele tourne en sens horaire ecran avec l'angle KiCad lu a l'extraction (theta) ; l'angle a ecrire
pour que KiCad reproduise la position des pastilles du modele est psi = (2*theta - phi) mod 360."""
import json, shutil, sys, pcbnew
src, sol, ext, out = sys.argv[1:5]
pos = json.load(open(sol, encoding="utf-8"))["positions"]
theta = {c["ref"]: c["current_rotation_deg"] for c in json.load(open(ext, encoding="utf-8"))["components"]}
shutil.copy2(src, out)
b = pcbnew.LoadBoard(out); n = 0
for fp in b.GetFootprints():
    r = fp.GetReference(); p = pos.get(r)
    if p is None or fp.IsLocked():
        continue
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(p["x_mm"]), pcbnew.FromMM(p["y_mm"])))
    fp.SetOrientationDegrees((2 * theta[r] - p["rotation_deg"]) % 360)
    n += 1
b.Save(out); print("appliquees", n, "->", out)
