#!/usr/bin/env python3
"""Vérifie la traçabilité du cycle en V, les références (ID + titre) et les doutes d'un projet.

Usage :
    python tools/check_traceability_V2.py projets/<nom>
    python tools/check_traceability_V2.py projets/<nom> --gate
    python tools/check_traceability_V2.py projets/<nom> --matrice projets/<nom>/06-matrice-tracabilite.md

Sans --gate : les erreurs (références invalides) font échouer, les trous de couverture et
les doutes bloquants sont signalés. Avec --gate : tout fait échouer.
"""
import argparse
import re
import sys
from pathlib import Path

PREFIXES = ("SCN", "BES", "REQ", "ARC", "DES", "TU", "TI", "TS", "TA", "DOU", "DEC")
# type de l'élément -> type attendu en amont
UPSTREAM = {"REQ": "BES", "ARC": "REQ", "DES": "ARC", "TA": "BES", "TS": "REQ", "TI": "ARC", "TU": "DES"}
# type de l'élément -> types qui doivent le référencer en aval
COVERAGE = {"SCN": ("BES",), "BES": ("REQ", "TA"), "REQ": ("ARC", "TS"), "ARC": ("DES", "TI"), "DES": ("TU",)}

# V2 : couverture exigée par phase (option --phase) ; sans option, tout le V est exigé
PHASES = {
    "scenarios": set(),
    "besoins": {("SCN", "BES")},
    "exigences": {("SCN", "BES"), ("BES", "REQ"), ("BES", "TA"), ("REQ", "TS")},
    "architecture": {("SCN", "BES"), ("BES", "REQ"), ("BES", "TA"), ("REQ", "TS"), ("REQ", "ARC"), ("ARC", "TI")},
    "conception": {("SCN", "BES"), ("BES", "REQ"), ("BES", "TA"), ("REQ", "TS"), ("REQ", "ARC"), ("ARC", "TI"),
                   ("ARC", "DES"), ("DES", "TU")},
}

ID = r"(?:%s)-\d{3}" % "|".join(PREFIXES)
DEF_RE = re.compile(r"^###\s+(%s)\s+[—-]\s+(.+?)\s*$" % ID)
REF_RE = re.compile(r"\b(%s)\b(?:\s*«([^»]+)»)?" % ID)
FENCE_RE = re.compile(r"^\s*```")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def clean_lines(text):
    """Retire commentaires HTML et blocs de code ; garde la numérotation des lignes."""
    text = COMMENT_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append("")
        else:
            out.append("" if in_fence else line)
    return out


def field(block, name):
    m = re.search(r"\*\*%s\s*:\*\*\s*(.*)" % re.escape(name), "\n".join(block))
    return m.group(1).strip() if m else ""


def parse(project):
    elements, mentions = {}, []  # elements[id] = dict ; mentions = (file, line, id, title|None)
    for path in sorted(project.rglob("*.md")):
        rel = path.relative_to(project).as_posix()
        lines = clean_lines(path.read_text(encoding="utf-8-sig"))
        current = None
        for n, line in enumerate(lines, 1):
            d = DEF_RE.match(line)
            if d:
                eid, title = d.group(1), d.group(2)
                if eid in elements:
                    mentions.append((rel, n, eid, None, "dup"))
                current = elements.setdefault(eid, {"title": title, "file": rel, "line": n, "block": []})
                continue
            if line.startswith("#"):
                current = None
            if current is not None:
                current["block"].append(line)
            for m in REF_RE.finditer(line):
                mentions.append((rel, n, m.group(1), (m.group(2) or "").strip() or None, "ref"))
    return elements, mentions


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projet", type=Path)
    ap.add_argument("--gate", action="store_true", help="mode porte : tout écart fait échouer")
    ap.add_argument("--phase", choices=list(PHASES),
                    help="ne vérifie la couverture que jusqu'à cette phase (les niveaux suivants n'existent pas encore)")
    ap.add_argument("--matrice", type=Path, help="écrit la matrice de traçabilité dans ce fichier")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not args.projet.is_dir():
        sys.exit("Dossier introuvable : %s" % args.projet)

    elements, mentions = parse(args.projet)
    errors, gaps, blocking = [], [], []

    # 1. références : existence, titre
    for rel, n, eid, title, kind in mentions:
        where = "%s:%d" % (rel, n)
        if kind == "dup":
            errors.append("%s : %s défini plusieurs fois" % (where, eid))
            continue
        if eid not in elements:
            errors.append("%s : %s n'est défini nulle part" % (where, eid))
        elif elements[eid]["line"] == n and elements[eid]["file"] == rel:
            continue  # la définition elle-même
        elif title is None:
            errors.append("%s : %s cité sans titre (attendu : « %s »)" % (where, eid, elements[eid]["title"]))
        elif title != elements[eid]["title"]:
            errors.append("%s : titre de %s différent (« %s » au lieu de « %s »)"
                          % (where, eid, title, elements[eid]["title"]))

    # 2. liens amont
    down = {eid: [] for eid in elements}
    ups = {}
    for eid, el in elements.items():
        if el["file"].startswith(("registre-doutes", "journal-decisions")):
            continue
        refs = [m.group(1) for m in REF_RE.finditer(field(el["block"], "Réfs amont"))]
        ups[eid] = refs
        etype = eid.split("-")[0]
        # un besoin peut aussi citer des décisions : il doit citer au moins un scénario
        if etype == "BES" and "Abandonné" not in field(el["block"], "Statut") \
                and not any(r.startswith("SCN-") for r in refs):
            gaps.append("%s « %s » : aucun scénario d'utilisation (SCN) en amont" % (eid, el["title"]))
        # V2 : un besoin couvre les scénarios qu'il cite (il peut aussi citer des DEC)
        if etype == "BES" and "Abandonné" not in field(el["block"], "Statut"):
            for r in refs:
                if r in elements and r.startswith("SCN-"):
                    down[r].append(eid)
        if etype in UPSTREAM and "Abandonné" not in field(el["block"], "Statut"):
            if not refs:
                gaps.append("%s « %s » : aucune référence amont" % (eid, el["title"]))
            for r in refs:
                if r in elements:
                    down[r].append(eid)
                    if r.split("-")[0] != UPSTREAM[etype]:
                        errors.append("%s : %s doit dériver d'un %s, pas de %s"
                                      % (eid, eid, UPSTREAM[etype], r))

    # 3. couverture
    for eid, el in elements.items():
        etype = eid.split("-")[0]
        if etype not in COVERAGE or "Abandonné" in field(el["block"], "Statut"):
            continue
        for needed in COVERAGE[etype]:
            if args.phase and (etype, needed) not in PHASES[args.phase]:
                continue
            if not any(d.startswith(needed + "-") and "Abandonné" not in field(elements[d]["block"], "Statut")
                       for d in down[eid]):
                gaps.append("%s « %s » : aucun %s ne le couvre" % (eid, el["title"], needed))

    # 4. doutes bloquants
    for eid, el in elements.items():
        if eid.startswith("DOU-") and field(el["block"], "Statut").lower().startswith("ouvert") \
                and field(el["block"], "Bloquant").lower().startswith("oui"):
            blocking.append("%s « %s » : doute bloquant ouvert" % (eid, el["title"]))

    # rapport
    counts = {p: sum(1 for e in elements if e.startswith(p + "-")) for p in PREFIXES}
    print("Éléments : " + (", ".join("%s=%d" % (p, c) for p, c in counts.items() if c) or "aucun"))
    for title, items in (("ERREURS", errors), ("TROUS DE TRAÇABILITÉ", gaps), ("DOUTES BLOQUANTS", blocking)):
        if items:
            print("\n%s (%d)" % (title, len(items)))
            for i in items:
                print("  - " + i)

    if args.matrice:
        rows = ["# Matrice de traçabilité", "",
                "> Généré par `tools/check_traceability_V2.py`. Ne pas modifier à la main.", "",
                "| Besoin | Exigence | Architecture | Test système |", "|---|---|---|---|"]
        ref = lambda i: "%s « %s »" % (i, elements[i]["title"])
        for rid in sorted(e for e in elements if e.startswith("REQ-")):
            bes = ", ".join(ref(b) for b in ups.get(rid, []) if b in elements) or "—"
            arc = ", ".join(ref(d) for d in down[rid] if d.startswith("ARC-")) or "—"
            ts = ", ".join(ref(d) for d in down[rid] if d.startswith("TS-")) or "—"
            rows.append("| %s | %s | %s | %s |" % (bes, ref(rid), arc, ts))
        args.matrice.write_text("\n".join(rows) + "\n", encoding="utf-8")
        print("\nMatrice écrite : %s" % args.matrice)

    failed = bool(errors) or (args.gate and (gaps or blocking))
    print("\n" + ("ÉCHEC" if failed else "OK") + (" (mode porte)" if args.gate else "")
          + (" [phase : %s]" % args.phase if args.phase else ""))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
