"""Collecte les metrics.json du banc et imprime un tableau de synthese (JSON + texte)."""
import glob
import json
import os
import sys

B = sys.argv[1]
rows = []
for path in sorted(glob.glob(os.path.join(B, "resultats", "*", "metrics.json"))):
    with open(path, encoding="utf-8") as f:
        m = json.load(f)
    s, r = m.get("statique", {}), m.get("routage", {})
    integ = s.get("integrite", {})
    rows.append({
        "piste": m.get("piste"),
        "valide": s.get("valide"),
        "recouv": s.get("recouvrement_mm2"),
        "hors": s.get("hors_contour_mm2"),
        "ancres_bougees": len(integ.get("ancres_bougees", [])),
        "faces": len(integ.get("faces_changees", [])),
        "u2": integ.get("u2_rotation_ok"),
        "hpwl": s.get("hpwl_mm"),
        "mst": s.get("arbre_couvrant_mm"),
        "crois": s.get("croisements_chevelu"),
        "dec_hors": s.get("decouplage_hors_5mm"),
        "dec_n": s.get("decouplage_n"),
        "dec_exc": s.get("decouplage_excès_total_mm"),
        "dec_moy": s.get("decouplage_distance_moy_mm"),
        "regles": s.get("regles_excès_mm"),
        "drc_court": s.get("drc_courtyard"),
        "routee": r.get("proportion_routee"),
        "nc_apres": r.get("non_connectes_apres"),
        "nc_avant": r.get("non_connectes_avant"),
        "pistes_mm": r.get("longueur_pistes_mm"),
        "vias": r.get("vias"),
        "err_routage": r.get("erreurs_drc_routage"),
        "statut_routage": r.get("statut"),
        "duree_routage": r.get("duree_s"),
        "png": os.path.exists(os.path.join(os.path.dirname(path), "placement.png")),
        "rapport": os.path.exists(os.path.join(os.path.dirname(path), "RAPPORT.md")),
    })
print(json.dumps(rows, indent=1, ensure_ascii=False))
