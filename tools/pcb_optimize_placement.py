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
from pcb_placement.io_data import apply_constraints, load_board, save_solution, load_solution_into  # noqa: E402
from pcb_placement.optimizer import run_parallel_strategies, best_of  # noqa: E402
from pcb_placement.visualize import save_comparison, format_report  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def cmd_extract(args: argparse.Namespace) -> None:
    kicad_python = args.kicad_python or os.environ.get("KICAD_PYTHON")
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


def cmd_optimize(args: argparse.Namespace) -> None:
    os.makedirs(args.out_dir, exist_ok=True)

    if args.config:
        config = EngineConfig.load(args.config)
    else:
        config = EngineConfig()
        config_default_path = os.path.join(args.out_dir, "config_utilisee.json")
        config.save(config_default_path)
        print(f"Aucune config fournie : parametres par defaut ecrits dans {config_default_path} (modifiable pour un prochain essai).")

    board_before = load_board(args.extract_json)
    if args.constraints:
        apply_constraints(board_before, args.constraints)

    t_start = time.time()
    results = run_parallel_strategies(args.extract_json, config, parallel=not args.no_parallel, constraints_path=args.constraints)
    best = best_of(results)
    elapsed = time.time() - t_start

    board_after = load_board(args.extract_json)
    if args.constraints:
        apply_constraints(board_after, args.constraints)
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


def cmd_apply(args: argparse.Namespace) -> None:
    kicad_python = args.kicad_python or os.environ.get("KICAD_PYTHON")
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
