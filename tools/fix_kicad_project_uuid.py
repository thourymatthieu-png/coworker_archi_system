#!/usr/bin/env python3
"""Vérifie et corrige la cohérence d'UUID entre un projet KiCad (.kicad_pro) et son
schéma racine (.kicad_sch) généré par le MCP kicad (kicad_workflow create_project).

Bug connu de kicad-sch-api : le .kicad_sch créé a un UUID racine à zéro
("00000000-0000-0000-0000-000000000000") et un nom de projet placeholder
("simple_circuit") dans les blocs d'instance de chaque composant, qui ne
correspondent pas à l'UUID de feuille racine attendu par le .kicad_pro
(clé "sheets"). Résultat : KiCad affiche le schéma comme vide
(« pas de schématique chargée ») même si le fichier contient bien les composants.

Usage :
    python tools/fix_kicad_project_uuid.py <dossier_du_projet_kicad_ou_fichier.kicad_pro>
    python tools/fix_kicad_project_uuid.py <...> --check

Sans --check : corrige le .kicad_sch en place (UUID racine + blocs instances) et
affiche ce qui a été changé. Avec --check : ne corrige rien, sort avec le code 1
si une incohérence est détectée (porte, comme tools/check_traceability.py --gate).

À lancer par l'agent electronique-hardware juste après tout
kicad_workflow create_project, avant toute saisie de composants.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT_UUID_RE = re.compile(r'\(uuid "([0-9a-fA-F-]{36})"\)')
INSTANCE_RE = re.compile(r'\(project "([^"]*)"\s*\(path "/([0-9a-fA-F-]{36})"')


def find_files(target):
    target = Path(target)
    if target.is_file() and target.suffix == ".kicad_pro":
        pro = target
    elif target.is_dir():
        pros = sorted(target.glob("*.kicad_pro"))
        if not pros:
            sys.exit(f"Aucun .kicad_pro trouvé dans {target}")
        if len(pros) > 1:
            sys.exit(f"Plusieurs .kicad_pro trouvés dans {target}, précise le fichier")
        pro = pros[0]
    else:
        sys.exit(f"{target} : ni un .kicad_pro ni un dossier")
    sch = pro.with_suffix(".kicad_sch")
    if not sch.exists():
        sys.exit(f"{sch} introuvable à côté de {pro}")
    return pro, sch


def expected_uuid(pro_path):
    data = json.loads(pro_path.read_text(encoding="utf-8"))
    sheets = data.get("sheets")
    if not sheets or not sheets[0]:
        sys.exit(f"{pro_path} : pas de clé \"sheets\" exploitable")
    return sheets[0][0]


def check(pro_path, sch_path):
    """Retourne la liste des incohérences (vide si tout est cohérent)."""
    expected = expected_uuid(pro_path)
    project_name = pro_path.stem
    text = sch_path.read_text(encoding="utf-8")

    problems = []
    root_match = ROOT_UUID_RE.search(text.split("(lib_symbols", 1)[0])
    if not root_match:
        problems.append("UUID racine introuvable avant (lib_symbols")
    elif root_match.group(1) != expected:
        problems.append(f"UUID racine {root_match.group(1)} != attendu {expected} (d'après {pro_path.name})")

    for name, path_uuid in INSTANCE_RE.findall(text):
        if name != project_name:
            problems.append(f"instance avec project=\"{name}\" au lieu de \"{project_name}\"")
        if path_uuid != expected:
            problems.append(f"instance avec path UUID {path_uuid} != attendu {expected}")

    return expected, project_name, problems


def fix(pro_path, sch_path):
    expected, project_name, problems = check(pro_path, sch_path)
    if not problems:
        return expected, project_name, []

    text = sch_path.read_text(encoding="utf-8")
    head, rest = text.split("(lib_symbols", 1)
    head, n_root = ROOT_UUID_RE.subn(f'(uuid "{expected}")', head, count=1)
    text = head + "(lib_symbols" + rest

    def repl(m):
        return f'(project "{project_name}"\n\t\t\t\t(path "/{expected}"'

    text, n_instances = INSTANCE_RE.subn(repl, text)
    sch_path.write_text(text, encoding="utf-8")

    changes = []
    if n_root:
        changes.append("UUID racine du document corrigé")
    if n_instances:
        changes.append(f"{n_instances} bloc(s) instance corrigé(s) (project + path)")
    return expected, project_name, changes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="dossier du projet KiCad ou chemin du .kicad_pro")
    ap.add_argument("--check", action="store_true", help="ne corrige rien, échoue si incohérence")
    args = ap.parse_args()

    pro_path, sch_path = find_files(args.target)

    if args.check:
        expected, project_name, problems = check(pro_path, sch_path)
        if problems:
            print(f"Incohérences UUID entre {pro_path.name} et {sch_path.name} :")
            for p in problems:
                print(f"  - {p}")
            sys.exit(1)
        print(f"OK : {sch_path.name} cohérent avec {pro_path.name} (UUID racine {expected})")
        return

    expected, project_name, changes = fix(pro_path, sch_path)
    if not changes:
        print(f"OK : {sch_path.name} était déjà cohérent avec {pro_path.name} (UUID racine {expected})")
    else:
        print(f"{sch_path} corrigé (projet \"{project_name}\", UUID racine {expected}) :")
        for c in changes:
            print(f"  - {c}")


if __name__ == "__main__":
    main()
