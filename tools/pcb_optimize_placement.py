"""Ligne de commande du moteur d'optimisation de placement PCB (independant de KiCad pour les
calculs, cf. tools/pcb_placement/). Trois sous-commandes :

  extract    lance tools/kicad_tetris_extract.py avec le Python embarque de KiCad (--kicad-python
             ou variable d'environnement KICAD_PYTHON) pour produire le JSON d'entree.
  optimize   execute le moteur (plusieurs strategies en parallele, cf. config) sur ce JSON,
             ecrit la meilleure solution, un rapport et une image avant/apres.
  apply      lance tools/kicad_apply_placement.py (Python embarque) pour ecrire la solution
             sur une COPIE du .kicad_pcb d'origine.

Exemple (flux complet) :
    python tools/pcb_optimize_placement.py extract <proj.kicad_pcb> --out-dir resultats/
    python tools/pcb_optimize_placement.py optimize resultats/extract.json --out-dir resultats/
    python tools/pcb_optimize_placement.py apply <proj.kicad_pcb> resultats/best_solution.json <proj_optimise.kicad_pcb>
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from pcb_placement.config import EngineConfig  # noqa: E402
from pcb_placement.io_data import apply_constraints, apply_decoupling, load_board, save_solution, load_solution_into  # noqa: E402
from pcb_placement.optimizer import run_parallel_strategies, best_of  # noqa: E402
from pcb_placement.visualize import save_comparison, format_report  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def resolve_kicad_python(arg):
    """--kicad-python, sinon $KICAD_PYTHON, sinon le venv ~/.venvs/kicad-mcp du poste courant."""
    if arg:
        return arg
    if os.environ.get("KICAD_PYTHON"):
        return os.environ["KICAD_PYTHON"]
    exe = os.path.join("Scripts", "python.exe") if os.name == "nt" else os.path.join("bin", "python")
    cand = os.path.join(os.path.expanduser("~"), ".venvs", "kicad-mcp", exe)
    return cand if os.path.exists(cand) else None


def cmd_extract(args: argparse.Namespace) -> None:
    kicad_python = resolve_kicad_python(args.kicad_python)
    if not kicad_python:
        print("Indiquer --kicad-python <chemin> ou definir la variable d'environnement "
              "KICAD_PYTHON (Python embarque de KiCad, seul a savoir importer pcbnew). "
              "Chemin habituel de ce depot : voir .claude.json, cle mcpServers.kicad.env.KICAD_PYTHON.")
        sys.exit(1)
    os.makedirs(args.out_dir, exist_ok=True)
    out_json = os.path.join(args.out_dir, "extract.json")
    extractor = os.path.join(HERE, "kicad_tetris_extract.py")
    subprocess.run([kicad_python, extractor, args.pcb_path, out_json], check=True)
    print(f"Extrait : {out_json}")


def start_live(args, config, board):
    """Suivi en direct : ecrit la description de la carte, copie la page web et la sert en
    local (http://127.0.0.1:<port>/index.html). Les strategies ecrivent leurs instantanes
    dans le meme dossier (config.live_dir)."""
    import functools
    import http.server
    import shutil
    import socketserver
    import threading
    from pcb_placement import live
    from pcb_placement.visualize import block_colors, block_label
    live_dir = os.path.abspath(args.live_dir or os.path.join(args.out_dir, "live"))
    os.makedirs(live_dir, exist_ok=True)
    shutil.copy(os.path.join(HERE, "pcb_placement", "viewer", "index.html"), os.path.join(live_dir, "index.html"))
    for old in os.listdir(live_dir):  # instantanes d'un run precedent
        if old.startswith("state_"):
            os.remove(os.path.join(live_dir, old))
    config.live_dir = live_dir
    colors = block_colors(board)
    live.write_static(live_dir, board, config.n_parallel_strategies, colors,
                      {b: block_label(b) for b in colors})

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    srv = Server(("127.0.0.1", args.port), functools.partial(Quiet, directory=live_dir))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print("Suivi en direct : http://127.0.0.1:%d/index.html" % args.port, flush=True)
    return srv


def cmd_optimize(args: argparse.Namespace) -> None:
    os.makedirs(args.out_dir, exist_ok=True)

    if args.config:
        config = EngineConfig.load(args.config)
    else:
        config = EngineConfig()
        config_default_path = os.path.join(args.out_dir, "config_utilisee.json")
        config.save(config_default_path)
        print(f"Aucune config fournie : parametres par defaut ecrits dans {config_default_path} (modifiable pour un prochain essai).")

    if args.decoupling:
        config.decoupling_file = args.decoupling
    if args.decoupling_max_mm is not None:
        config.decoupling_max_mm = args.decoupling_max_mm

    board_before = load_board(args.extract_json)
    if args.constraints:
        apply_constraints(board_before, args.constraints)
    if config.decoupling_file:
        info = apply_decoupling(board_before, config.decoupling_file, config.decoupling_max_mm)
        print(f"Decouplage : {info['rules']} regle(s) (distance par defaut {config.decoupling_max_mm} mm), "
              f"ignorees : {info['skipped'] or 'aucune'}")
    live_server = start_live(args, config, board_before) if args.live else None

    t_start = time.time()
    results = run_parallel_strategies(args.extract_json, config, parallel=not args.no_parallel, constraints_path=args.constraints)
    best = best_of(results)
    elapsed = time.time() - t_start

    board_after = load_board(args.extract_json)
    if args.constraints:
        apply_constraints(board_after, args.constraints)
    if config.decoupling_file:
        apply_decoupling(board_after, config.decoupling_file, config.decoupling_max_mm)
    board_after.restore_positions(best.positions)

    sol_path = os.path.join(args.out_dir, "best_solution.json")
    save_solution(board_after, sol_path, extra={
        "total_cost": best.best_cost.total,
        "area_mm2": best.best_cost.area_mm2,
        "wirelength_mm": best.best_cost.wirelength_mm,
        "congestion": best.best_cost.congestion,
        "crossings": best.best_cost.crossings,
        "vias_estimate": best.best_cost.vias_estimate,
        "overlap_mm2": best.best_cost.overlap_mm2,
        "feasible": best.best_cost.feasible,
        "seed_retenue": best.seed,
        "temps_calcul_s": elapsed,
    })

    # Sauvegarde de TOUTES les strategies (section 9 : comparer/reprendre), pas seulement la meilleure.
    all_path = os.path.join(args.out_dir, "toutes_les_strategies.json")
    with open(all_path, "w", encoding="utf-8") as f:
        json.dump(
            [
                {
                    "seed": r.seed,
                    "elapsed_s": r.elapsed_s,
                    "best_cost": r.best_cost.__dict__,
                    "history": [{"cycle": h.cycle, "cost": h.cost.__dict__} for h in r.history],
                }
                for r in results
            ],
            f,
            indent=2,
        )

    img_path = os.path.join(args.out_dir, "comparaison.png")
    save_comparison(board_before, board_after, None, best.best_cost, img_path)

    report = format_report(None, best.best_cost, elapsed)
    report_path = os.path.join(args.out_dir, "rapport.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\nStrategie retenue : graine {best.seed}")
    print(f"Solution : {sol_path}")
    print(f"Toutes les strategies : {all_path}")
    print(f"Image avant/apres : {img_path}")
    print(f"Rapport : {report_path}")
    if live_server is not None and args.live_hold_s > 0:  # apres l'ecriture des resultats
        print("Page de suivi servie encore %.0f s." % args.live_hold_s, flush=True)
        time.sleep(args.live_hold_s)


def cmd_apply(args: argparse.Namespace) -> None:
    kicad_python = resolve_kicad_python(args.kicad_python)
    if not kicad_python:
        print("Indiquer --kicad-python <chemin> ou definir KICAD_PYTHON.")
        sys.exit(1)
    applier = os.path.join(HERE, "kicad_apply_placement.py")
    subprocess.run([kicad_python, applier, args.pcb_path, args.solution_json, args.out_pcb], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_extract = sub.add_parser("extract", help="Extraire la geometrie/connectivite du PCB (besoin de pcbnew)")
    p_extract.add_argument("pcb_path")
    p_extract.add_argument("--out-dir", default="resultats_placement")
    p_extract.add_argument("--kicad-python", default=None)
    p_extract.set_defaults(func=cmd_extract)

    p_opt = sub.add_parser("optimize", help="Optimiser le placement (pur Python, sans KiCad)")
    p_opt.add_argument("extract_json")
    p_opt.add_argument("--out-dir", default="resultats_placement")
    p_opt.add_argument("--config", default=None, help="Fichier de config JSON (EngineConfig) ; defaut si omis")
    p_opt.add_argument("--live", action="store_true", help="suivi en direct dans le navigateur (page web locale)")
    p_opt.add_argument("--live-dir", default=None, help="dossier des instantanes du suivi (defaut : <out-dir>/live)")
    p_opt.add_argument("--port", type=int, default=8765, help="port de la page de suivi (defaut 8765)")
    p_opt.add_argument("--live-hold-s", type=float, default=60.0, help="secondes pendant lesquelles la page reste servie apres le calcul")
    p_opt.add_argument("--decoupling", default=None, help="decouplage.json (condensateur -> broche d'alimentation) : ajoute une penalite de distance")
    p_opt.add_argument("--decoupling-max-mm", type=float, default=None, help="distance max de decouplage par defaut (mm), 5 par defaut")
    p_opt.add_argument("--constraints", default=None, help="Fichier JSON de contraintes mecaniques (contour de carte fixe, ancres, debords) - cf. README")
    p_opt.add_argument("--no-parallel", action="store_true", help="Force l'execution sequentielle des strategies (debogage)")
    p_opt.set_defaults(func=cmd_optimize)

    p_apply = sub.add_parser("apply", help="Ecrire la solution sur une COPIE du .kicad_pcb (besoin de pcbnew)")
    p_apply.add_argument("pcb_path")
    p_apply.add_argument("solution_json")
    p_apply.add_argument("out_pcb")
    p_apply.add_argument("--kicad-python", default=None)
    p_apply.set_defaults(func=cmd_apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
