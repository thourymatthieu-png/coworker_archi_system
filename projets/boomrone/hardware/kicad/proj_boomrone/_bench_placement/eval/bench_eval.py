"""Banc COMMUN d'evaluation des placements de la carte Boomrone (Python systeme : numpy, matplotlib).

Toutes les pistes du banc sont jugees par CE script, sans modification (le juge est fige : copie du
moteur maison dans eval/moteur, extracteur dans eval/kicad_tetris_extract.py).

  python bench_eval.py statique <carte_placee.kicad_pcb> --piste <nom>
  python bench_eval.py routage  <carte_placee.kicad_pcb> --piste <nom> [--passes 25] [--limite 480]

Sorties dans resultats/<piste>/ : extract.json, stats.json, drc_placement.json, placement.png,
metrics.json (cumule statique + routage), metrics.md ; pour le routage : carte.dsn, carte.ses,
freerouting.log, routee.kicad_pcb, drc_routage.json.

Metriques statiques : integrite (memes references, pieces verrouillees immobiles, faces
inchangees, rotation imposee de U2), recouvrement et debord (moteur maison, courtyards en
rectangles, marge 0,3 mm), longueur estimee (HPWL et arbre couvrant), croisements du chevelu,
decouplage (distance PASTILLE du condensateur -> broche, regle de 5 mm de decouplage.json),
regles actives (U2 au centre, isolements I-01..I-03), DRC KiCad (hors connexions non routees).
Metriques de routage : Freerouting 2.5 sur 2 couches avec les regles de la carte ; proportion de
connexions routees (DRC : connexions manquantes apres / avant), longueur de pistes, vias, erreurs DRC.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BANC = os.path.dirname(HERE)
ENTREE = os.path.join(BANC, "entree")
RESULTATS = os.path.join(BANC, "resultats")
REF_PCB = os.path.join(ENTREE, "proj_boomrone.kicad_pcb")
SOURCE_PCB = os.path.abspath(os.path.join(BANC, "..", "proj_boomrone.kicad_pcb"))
DECOUPLAGE = os.path.join(ENTREE, "decouplage.json")
REGLES = os.path.join(ENTREE, "regles_actives.json")
SCRATCH = r"C:\Users\quent\AppData\Local\Temp\claude\2278bd884c6d4164\2d2231f5-79a6-428c-9a77-48e2659475b1\scratchpad"
KICAD_PY = os.environ.get("KICAD_PYTHON") or os.path.expanduser(r"~\.venvs\kicad-mcp\Scripts\python.exe")
KICAD_CLI = os.environ.get("KICAD_CLI") or r"C:\Users\quent\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe"
JAVA = os.environ.get("BANC_JAVA") or os.path.join(SCRATCH, r"dl_jre25\jdk-25.0.5+8-jre\bin\java.exe")
FREEROUTING = os.environ.get("BANC_FREEROUTING") or os.path.join(SCRATCH, r"dl_freerouting\freerouting-2.5.0.jar")
DMAX_DECOUPLAGE = 5.0

sys.path.insert(0, os.path.join(HERE, "moteur"))
sys.path.insert(0, HERE)
from pcb_placement import cost, io_data  # noqa: E402  (copie figee du moteur maison)
import verrou  # noqa: E402


def _run(cmd, timeout=None, log=None):
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    if log:
        with open(log, "w", encoding="utf-8") as f:
            f.write(r.stdout + "\n--- stderr ---\n" + r.stderr)
    return r, time.time() - t0


def _kpy(*args, timeout=600):
    r, _ = _run([KICAD_PY, os.path.join(HERE, "bench_pcbnew.py"), *args], timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"bench_pcbnew {args[0]} a echoue :\n{r.stdout}\n{r.stderr}")
    return r


def _out_dir(piste):
    d = os.path.join(RESULTATS, piste)
    os.makedirs(d, exist_ok=True)
    return d


def _check_input(pcb):
    p = os.path.abspath(pcb)
    if p in (SOURCE_PCB, os.path.abspath(REF_PCB)):
        sys.exit("Refus : evaluer une COPIE placee, pas la carte source ni la reference du banc.")
    if not os.path.exists(p):
        sys.exit(f"Introuvable : {p}")
    return p


def _load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)


# ----------------------------------------------------------------------------- DRC KiCad
def drc(pcb, out_json):
    r, _ = _run([KICAD_CLI, "pcb", "drc", "--format", "json", "--severity-all", "--units", "mm",
                 "-o", out_json, pcb], timeout=600)
    data = _load_json(out_json, {}) or {}
    par_type = {}
    for v in data.get("violations", []):
        par_type[v.get("type", "?")] = par_type.get(v.get("type", "?"), 0) + 1
    return {"par_type": dict(sorted(par_type.items(), key=lambda kv: -kv[1])),
            "non_connectes": len(data.get("unconnected_items", [])),
            "code_retour": r.returncode}


DRC_DEFAUTS = ("courtyards_overlap", "shorting_items", "clearance", "copper_edge_clearance",
               "solder_mask_bridge", "pth_inside_courtyard")


def ref_drc():
    path = os.path.join(HERE, "ref_drc.json")
    if not os.path.exists(path):
        d = drc(REF_PCB, os.path.join(HERE, "ref_drc_kicad.json"))
        _save_json(path, d)
    return _load_json(path)


# ----------------------------------------------------------------------------- integrite
def ref_stats():
    path = os.path.join(HERE, "ref_stats.json")
    if not os.path.exists(path):
        _kpy("stats", REF_PCB, path)
    return _load_json(path)


def integrite(st, ref):
    a, b = ref["footprints"], st["footprints"]
    manquants = sorted(set(a) - set(b))
    en_trop = sorted(set(b) - set(a))
    ancres_bougees, faces_changees, verrous_perdus = [], [], []
    for r, fa in a.items():
        fb = b.get(r)
        if fb is None:
            continue
        if fa["layer"] != fb["layer"]:
            faces_changees.append(r)
        if fa["locked"]:
            if not fb["locked"]:
                verrous_perdus.append(r)
            drot = abs(((fa["rot"] - fb["rot"]) + 180) % 360 - 180)
            if math.hypot(fa["x"] - fb["x"], fa["y"] - fb["y"]) > 0.01 or drot > 0.1:
                ancres_bougees.append(r)
    u2 = b.get("U2", {}).get("rot")
    return {"manquants": manquants, "en_trop": en_trop, "ancres_bougees": ancres_bougees,
            "verrous_perdus": verrous_perdus, "faces_changees": faces_changees,
            "u2_rotation_deg": u2, "u2_rotation_ok": u2 is not None and abs(((u2 + 180) % 360) - 180) < 0.1,
            "ancres_reference": sorted(r for r, f in a.items() if f["locked"])}


# ----------------------------------------------------------------------------- moteur fige
def metriques_moteur(extract_json):
    board = io_data.load_board(extract_json)
    io_data.apply_decoupling(board, DECOUPLAGE, default_mm=DMAX_DECOUPLAGE)
    regles_dec = list(board.decoupling_rules)
    io_data.apply_active_rules(board, REGLES)
    refs = list(board.components)
    br = cost.total_cost(board, refs, board.nets, cost.CostWeights())
    segs = cost.net_segments(board, board.nets)
    mst = sum(math.hypot(p[0] - q[0], p[1] - q[1]) for p, q, _ in segs)

    # Decouplage : distance PASTILLE du condensateur (celle sur le reseau decouple) -> broche
    dec = []
    for rule in regles_dec:
        cap, ic = board.components[rule["cap"]], board.components[rule["ic"]]
        cap_pads = [p for p in cap.pads if rule.get("net") and p.net == rule["net"]] or cap.pads
        best = None
        for cp in cap_pads:
            cx, cy = cap.pad_world_pos(cp)
            for ip in ic.pads:
                if ip.name in rule["pins"]:
                    px, py = ic.pad_world_pos(ip)
                    d = math.hypot(px - cx, py - cy)
                    best = d if best is None else min(best, d)
        if best is not None:
            dec.append({"cap": rule["cap"], "ic": rule["ic"], "d_mm": round(best, 2),
                        "dmax_mm": rule["dmax"], "excès_mm": round(max(0.0, best - rule["dmax"]), 2)})
    regles = {}
    for rule in board.decoupling_rules[len(regles_dec):]:
        nom = rule.get("id") or (f"proximite {rule.get('cap')}" if rule.get("kind") is None else rule.get("kind"))
        regles[nom] = round(cost.decoupling_excess(board, rule), 2)
    disp, _ = cost.block_dispersion(board)
    return board, {
        "faisable_moteur": bool(br.feasible),
        "recouvrement_mm2": round(br.overlap_mm2, 2),
        "hors_contour_mm2": round(br.out_of_bounds_mm2, 2),
        "hpwl_mm": round(br.wirelength_mm, 1),
        "arbre_couvrant_mm": round(mst, 1),
        "croisements_chevelu": int(br.crossings),
        "vias_estimes": int(br.vias_estimate),
        "surface_englobante_mm2": round(br.area_mm2, 1),
        "dispersion_blocs_mm": round(disp, 2),
        "decouplage_n": len(dec),
        "decouplage_hors_5mm": sum(1 for d in dec if d["excès_mm"] > 0),
        "decouplage_excès_total_mm": round(sum(d["excès_mm"] for d in dec), 2),
        "decouplage_distance_moy_mm": round(sum(d["d_mm"] for d in dec) / len(dec), 2) if dec else None,
        "decouplage_detail": dec,
        "regles_excès_mm": regles,
    }


def image(board, path, titre):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from pcb_placement.visualize import draw_board
    fig, ax = plt.subplots(figsize=(8, 8))
    draw_board(board, ax, titre)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def _ecrire(out, metrics):
    _save_json(os.path.join(out, "metrics.json"), metrics)
    s = metrics.get("statique", {})
    rt = metrics.get("routage", {})
    lignes = [f"# Banc de placement - piste {metrics['piste']}", "",
              f"Carte evaluee : `{metrics['carte']}`", "",
              "| Metrique | Valeur |", "|---|---|"]
    for k in ("valide", "valide_cuivre", "recouvrement_mm2", "hors_contour_mm2", "hpwl_mm", "arbre_couvrant_mm",
              "croisements_chevelu", "decouplage_hors_5mm", "decouplage_excès_total_mm",
              "decouplage_distance_moy_mm", "regles_excès_mm", "drc_courtyard", "drc_defauts_placement"):
        if k in s:
            lignes.append(f"| {k} | {s[k]} |")
    for k in ("proportion_routee", "non_connectes_avant", "non_connectes_apres", "longueur_pistes_mm",
              "vias", "erreurs_drc_routage", "duree_s", "statut"):
        if k in rt:
            lignes.append(f"| routage.{k} | {rt[k]} |")
    lignes += ["", "Integrite : " + json.dumps(s.get("integrite", {}), ensure_ascii=False)]
    with open(os.path.join(out, "metrics.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")


def cmd_statique(a):
    pcb = _check_input(a.carte)
    out = _out_dir(a.piste)
    ext = os.path.join(out, "extract.json")
    r, _ = _run([KICAD_PY, os.path.join(HERE, "kicad_tetris_extract.py"), pcb, ext], timeout=600)
    if r.returncode != 0:
        sys.exit("Extraction en echec :\n" + r.stdout + r.stderr)
    st_path = os.path.join(out, "stats.json")
    _kpy("stats", pcb, st_path)
    st = _load_json(st_path)
    integ = integrite(st, ref_stats())
    board, m = metriques_moteur(ext)
    d = drc(pcb, os.path.join(out, "drc_placement.json"))
    # Defauts de cuivre crees par le placement = compte DRC au-dessus de celui de la carte d'entree
    # (composants ecartes : ses 14 'clearance' sont internes aux empreintes, presents partout).
    # Correction du 2026-11-06 : l'ancien 'drc_courtyard' comptait aussi 'silk_overlap' (serigraphie).
    rd = ref_drc()
    defauts = {k: max(0, d["par_type"].get(k, 0) - rd["par_type"].get(k, 0)) for k in DRC_DEFAUTS}
    m.update({
        "integrite": integ,
        "drc_par_type": d["par_type"],
        "drc_courtyard": d["par_type"].get("courtyards_overlap", 0),
        "drc_defauts_placement": defauts,
        "drc_defauts_total": sum(defauts.values()),
        "non_connectes_initial": d["non_connectes"],
    })
    m["valide"] = (not integ["manquants"] and not integ["en_trop"] and not integ["ancres_bougees"]
                   and not integ["faces_changees"] and integ["u2_rotation_ok"]
                   and m["recouvrement_mm2"] <= 0.01 and m["hors_contour_mm2"] <= 0.01
                   and defauts["courtyards_overlap"] == 0)
    m["valide_cuivre"] = m["valide"] and m["drc_defauts_total"] == 0
    image(board, os.path.join(out, "placement.png"),
          f"{a.piste} - HPWL {m['hpwl_mm']} mm, recouvrement {m['recouvrement_mm2']} mm2")
    metrics = _load_json(os.path.join(out, "metrics.json"), {}) or {}
    metrics.update({"piste": a.piste, "carte": pcb, "statique": m, "date_statique": time.strftime("%Y-%m-%d %H:%M")})
    _ecrire(out, metrics)
    print(json.dumps({k: v for k, v in m.items() if k not in ("decouplage_detail", "drc_par_type")},
                     indent=1, ensure_ascii=False))
    print(f"Ecrit : {out}")


def cmd_routage(a):
    pcb = _check_input(a.carte)
    out = _out_dir(a.piste)
    if a.retirer_pistes:  # outil qui place ET route (Quilter...) : on rejuge le placement seul
        nue = os.path.join(out, "placee_sans_pistes.kicad_pcb")
        _kpy("strip", pcb, nue)
        pcb = nue
    if not verrou.prendre("routage", a.piste, attente=a.attente_verrou):
        print("Verrou 'routage' occupe : attendre (python verrou.py attendre routage) puis relancer.")
        sys.exit(3)
    try:
        dsn = os.path.join(out, "carte.dsn")
        ses = os.path.join(out, "carte.ses")
        if os.path.exists(ses):
            os.remove(ses)
        _kpy("dsn", pcb, dsn)
        cmd = [JAVA, "-Xmx3g", "-jar", FREEROUTING, "-de", dsn, "-do", ses, "-mp", str(a.passes),
               "-mt", "8", "--gui.enabled=false", "--usage_and_diagnostic_data.disable_analytics=true",
               "--api_server.enabled=false", "--mcp_server.enabled=false",
               "--router.optimizer.enabled=false"]  # routage seul : duree bornee et comparable
        statut = "termine"
        try:
            _, duree = _run(cmd, timeout=a.limite, log=os.path.join(out, "freerouting.log"))
        except subprocess.TimeoutExpired:
            statut, duree = f"coupe a {a.limite} s", a.limite
    finally:
        verrou.rendre("routage", a.piste)
    rt = {"statut": statut, "duree_s": round(duree, 1), "passes_max": a.passes}
    if os.path.exists(ses):
        routee = os.path.join(out, "routee.kicad_pcb")
        _kpy("ses", pcb, ses, routee)
        d_av = drc(pcb, os.path.join(out, "drc_placement.json"))
        d_ap = drc(routee, os.path.join(out, "drc_routage.json"))
        st = os.path.join(out, "stats_routee.json")
        _kpy("stats", routee, st)
        s = _load_json(st)
        av, ap = d_av["non_connectes"], d_ap["non_connectes"]
        erreurs = {k: v for k, v in d_ap["par_type"].items()
                   if k in ("clearance", "shorting_items", "tracks_crossing", "hole_clearance",
                            "copper_edge_clearance", "track_dangling", "via_dangling")}
        rt.update({"non_connectes_avant": av, "non_connectes_apres": ap,
                   "proportion_routee": round(1 - ap / av, 3) if av else None,
                   "longueur_pistes_mm": s["track_length_mm"], "vias": s["vias"],
                   "erreurs_drc_routage": erreurs})
    else:
        rt["statut"] += " (pas de fichier .ses)"
    metrics = _load_json(os.path.join(out, "metrics.json"), {}) or {}
    metrics.update({"piste": a.piste, "carte": pcb, "routage": rt, "date_routage": time.strftime("%Y-%m-%d %H:%M")})
    _ecrire(out, metrics)
    print(json.dumps(rt, indent=1, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("statique")
    s.add_argument("carte")
    s.add_argument("--piste", required=True)
    r = sub.add_parser("routage")
    r.add_argument("carte")
    r.add_argument("--piste", required=True)
    r.add_argument("--passes", type=int, default=25)
    r.add_argument("--limite", type=float, default=480, help="duree max de Freerouting (s)")
    r.add_argument("--attente-verrou", type=float, default=60)
    r.add_argument("--retirer-pistes", action="store_true",
                   help="retirer les pistes deja presentes (carte rendue placee ET routee par l'outil)")
    a = ap.parse_args()
    {"statique": cmd_statique, "routage": cmd_routage}[a.cmd](a)


if __name__ == "__main__":
    main()
