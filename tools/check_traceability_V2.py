#!/usr/bin/env python3
"""Vérifie la traçabilité du cycle en V, les références (ID + titre), les champs, les statuts,
les doutes et les relectures d'un projet.

Usage :
    python tools/check_traceability_V2.py projets/<nom>
    python tools/check_traceability_V2.py projets/<nom> --gate --phase architecture
    python tools/check_traceability_V2.py projets/<nom> --porte-franchie conception
    python tools/check_traceability_V2.py projets/<nom> --matrice projets/<nom>/06-matrice-tracabilite.md

Trois niveaux de constats :
- ERREURS : références invalides, statuts inconnus, doublons. Font toujours échouer.
- ÉCARTS : trous de traçabilité, champs manquants, doutes mal tenus, relectures absentes ou sans
  sort, valeurs « (à vérifier) » en conception détaillée, tests non exécutés... Font échouer avec --gate.
- AVERTISSEMENTS : éléments trop longs, contenu peut-être périmé, doutes bloquants à une porte future.
  Ne font jamais échouer ; à lire à chaque porte.
Les dossiers dont le nom commence par « _ » (essais, bancs, copies figées) ne sont pas analysés.
--phase limite les contrôles à la phase atteinte. --porte-franchie exige en plus que les éléments
des phases franchies soient « Validé » (à lancer après l'accord de porte).
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

DESIGN_PHASES = ["scenarios", "besoins", "exigences", "architecture", "conception"]
EXEC_PHASES = {"implementation": "TU", "integration": "TI", "systeme": "TS", "recette": "TA"}
PHASE_ORDER = DESIGN_PHASES + list(EXEC_PHASES)
_COV = [set(), {("SCN", "BES"), ("BES", "TA")}, {("BES", "REQ"), ("REQ", "TS")},
        {("REQ", "ARC"), ("ARC", "TI")}, {("ARC", "DES"), ("DES", "TU")}]
PHASES = {}
for _i, _p in enumerate(PHASE_ORDER):
    PHASES[_p] = set().union(*_COV[:min(_i, len(_COV) - 1) + 1])
# types d'éléments rédigés à chaque phase (chaque niveau a son test en face, défini en même temps)
PHASE_TYPES = {"scenarios": {"SCN"}, "besoins": {"BES", "TA"}, "exigences": {"REQ", "TS"},
               "architecture": {"ARC", "TI"}, "conception": {"DES", "TU"}}
MAIN_TYPE = {"scenarios": "SCN", "besoins": "BES", "exigences": "REQ", "architecture": "ARC", "conception": "DES"}
V_TYPES = ("SCN", "BES", "REQ", "ARC", "DES")
T_TYPES = ("TU", "TI", "TS", "TA")
# relecteurs obligatoires : un rapport revues/REV-<phase>-<agent>-v<n>.md chacun
REVIEWERS = {"scenarios": ("critique", "coherence-clarte"),
             "besoins": ("critique", "coherence-clarte", "exigences-tracabilite"),
             "exigences": ("critique", "coherence-clarte", "exigences-tracabilite"),
             "architecture": ("critique", "coherence-clarte", "exigences-tracabilite", "verificateur-sources"),
             "conception": ("critique", "coherence-clarte", "exigences-tracabilite", "verificateur-sources")}
for _p in EXEC_PHASES:
    REVIEWERS[_p] = ("critique", "coherence-clarte")
# mots reconnus dans le champ « Échéance » d'un doute -> phase
DEADLINE_WORDS = [("scenarios", r"sc[ée]narios?"), ("besoins", r"besoins?"), ("exigences", r"exigences?"),
                  ("architecture", r"architecture"), ("conception", r"conception"),
                  ("implementation", r"impl[ée]mentation"), ("integration", r"int[ée]gration"),
                  ("systeme", r"syst[èe]me|essais?|prototype"), ("recette", r"recette")]

REQUIRED = {
    "SCN": ("Réfs amont", "Type", "Situation de départ", "Déroulé", "Résultat attendu", "Statut"),
    "BES": ("Réfs amont", "Énoncé", "Priorité", "Statut"),
    "REQ": ("Réfs amont", "Énoncé", "Priorité", "Vérification", "Statut"),
    "ARC": ("Réfs amont", "Description", "Statut"),
    "DES": ("Réfs amont", "Description", "Statut"),
    "TU": ("Réfs amont", "Résultat attendu", "Statut"),
    "TI": ("Réfs amont", "Résultat attendu", "Statut"),
    "TS": ("Réfs amont", "Résultat attendu", "Statut"),
    "TA": ("Réfs amont", "Scénario rejoué", "Résultat attendu", "Statut"),
    "DOU": ("Statut", "Bloquant", "Question"),
    "DEC": ("Date", "Décidé par", "Décision", "Raison"),
}
STATUS_V = ("Proposé", "Validé", "Modifié", "Abandonné")
STATUS_T = ("À écrire", "Écrit", "Validé", "Modifié", "Exécuté OK", "Exécuté KO", "Abandonné")
STATUSES = {t: STATUS_V for t in V_TYPES}
STATUSES.update({t: STATUS_T for t in T_TYPES})
STATUSES["DOU"] = ("Ouvert", "Levé")
PRIORITY_RANK = {"souhaitable": 1, "important": 2, "essentiel": 3}

MAX_BLOCK_LINES = {"DEC": 15}       # décision : ~10 lignes visées
MAX_BLOCK_LINES_DEFAULT = 30        # élément : ~15 lignes de description visées, champs compris
MAX_BLOCK_CHARS = {"DEC": 1500}
MAX_BLOCK_CHARS_DEFAULT = 3000
STALE_RE = re.compile(r"p[ée]rim[ée]|pr[ée]vaut|prochaine r[ée]vision|[àa] reporter", re.I)
TO_CHECK_RE = re.compile(r"\([^()]*\b(?:[àa] v[ée]rifier|[àa] confirmer|de m[ée]moire)\b[^()]*\)", re.I)
PLACEHOLDER_RE = re.compile(r"xxx|nnn|\(o[ùu]\)|\s/\s.*\s/\s", re.I)

ID = r"(?:%s)-\d{3}" % "|".join(PREFIXES)
DEF_RE = re.compile(r"^###\s+(%s)\s+[—-]\s+(.+?)\s*$" % ID)
REF_RE = re.compile(r"\b(%s)\b(?:\s*«([^»]+)»)?" % ID)
FENCE_RE = re.compile(r"^\s*```")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
FIELD_LINE_RE = re.compile(r"^\*\*([^*:]+?)\s*:\*\*")


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
    """Valeur d'un champ `**Nom :**` : sa ligne et les suivantes, jusqu'au champ suivant."""
    value, inside = [], False
    for line in block:
        m = FIELD_LINE_RE.match(line)
        if m:
            if inside:
                break
            if m.group(1).strip() == name:
                inside = True
                value.append(line[m.end():].strip())
            continue
        if inside:
            value.append(line.strip())
    return " ".join(v for v in value if v).strip()


def has_field(block, name):
    for line in block:
        m = FIELD_LINE_RE.match(line)
        if m and m.group(1).strip() == name:
            return True
    return False


def etype(eid):
    return eid.split("-")[0]


def parse_review(rel, lines):
    """Lignes de tableau d'un rapport de relecture dont l'en-tête a une colonne « Sort »."""
    rows, header, sort_idx, grav_idx = [], None, None, None
    for n, line in enumerate(lines, 1):
        s = line.strip()
        if not s.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            sort_idx = header.index("sort") if "sort" in header else None
            grav_idx = header.index("gravité") if "gravité" in header else None
            continue
        if sort_idx is None or set("".join(cells)) <= set("-: "):
            continue
        get = lambda i: cells[i] if i is not None and i < len(cells) else ""
        rows.append({"file": rel, "line": n, "num": cells[0], "sort": get(sort_idx), "gravite": get(grav_idx)})
    return rows


def parse(project):
    elements, mentions, reviews, review_files = {}, [], [], []
    for path in sorted(project.rglob("*.md")):
        rel = path.relative_to(project).as_posix()
        if any(part.startswith("_") for part in rel.split("/")[:-1]):
            continue  # dossier de travail (essais, bancs, copies figées) : hors documents du projet
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
        if rel.startswith("revues/"):
            review_files.append(path.name)
            reviews.extend(parse_review(rel, lines))
    return elements, mentions, reviews, review_files


def phase_of_deadline(text):
    """Phase la plus tardive citée dans une échéance (None si aucune n'est reconnue)."""
    found = [p for p, pat in DEADLINE_WORDS if re.search(pat, text, re.I)]
    return found[-1] if found else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projet", type=Path)
    ap.add_argument("--gate", action="store_true", help="mode porte : les écarts font aussi échouer")
    ap.add_argument("--phase", choices=PHASE_ORDER, help="phase atteinte (contrôles limités à cette phase)")
    ap.add_argument("--porte-franchie", choices=PHASE_ORDER,
                    help="exige que les éléments des phases franchies jusqu'à celle-ci soient « Validé »")
    ap.add_argument("--matrice", type=Path, help="écrit la matrice de traçabilité dans ce fichier")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not args.projet.is_dir():
        sys.exit("Dossier introuvable : %s" % args.projet)

    phase = args.phase or args.porte_franchie or DESIGN_PHASES[-1]
    pidx = PHASE_ORDER.index(phase)
    upto = PHASE_ORDER[:pidx + 1]
    written_types = set().union(*(PHASE_TYPES.get(p, set()) for p in upto))
    active_types = written_types | {"DOU", "DEC"}

    elements, mentions, reviews, review_files = parse(args.projet)
    errors, gaps, blocking, warnings = [], [], [], []

    def name(eid):
        return "%s « %s »" % (eid, elements[eid]["title"])

    def status(eid):
        return field(elements[eid]["block"], "Statut")

    def abandoned(eid):
        return status(eid).startswith("Abandonné")

    def first_word(text):
        return text.split()[0].lower().strip(".,;") if text else ""

    def live(t):
        return [e for e in elements if etype(e) == t and not abandoned(e)]

    # 1. références : existence, titre (dans revues/, seule l'existence compte : un rapport ne se réécrit pas)
    for rel, n, eid, title, kind in mentions:
        where = "%s:%d" % (rel, n)
        if kind == "dup":
            errors.append("%s : %s défini plusieurs fois" % (where, eid))
            continue
        if eid not in elements:
            errors.append("%s : %s n'est défini nulle part" % (where, eid))
        elif rel.startswith("revues/"):
            continue
        elif elements[eid]["line"] == n and elements[eid]["file"] == rel:
            continue  # la définition elle-même
        elif title is None:
            errors.append("%s : %s cité sans titre (attendu : « %s »)" % (where, eid, elements[eid]["title"]))
        elif title != elements[eid]["title"]:
            errors.append("%s : titre de %s différent (« %s » au lieu de « %s »)"
                          % (where, eid, title, elements[eid]["title"]))

    # 2. champs obligatoires, statuts, taille, contenu périmé
    for eid, el in elements.items():
        t = etype(eid)
        if t not in active_types:
            continue
        where = "%s:%d" % (el["file"], el["line"])
        st = status(eid)
        missing = [f for f in REQUIRED.get(t, ()) if not has_field(el["block"], f)]
        if missing and not abandoned(eid):
            gaps.append("%s : %s, champ(s) manquant(s) : %s" % (where, name(eid), ", ".join(missing)))
        if t in STATUSES and st and not any(st.startswith(s) for s in STATUSES[t]):
            errors.append("%s : %s, statut inconnu « %s » (permis : %s)"
                          % (where, name(eid), st, ", ".join(STATUSES[t])))
        if t != "DOU" and st.startswith("Modifié"):
            gaps.append("%s : %s en cours de modification (statut « Modifié »)" % (where, name(eid)))
        limit = MAX_BLOCK_LINES.get(t, MAX_BLOCK_LINES_DEFAULT)
        climit = MAX_BLOCK_CHARS.get(t, MAX_BLOCK_CHARS_DEFAULT)
        size = sum(1 for line in el["block"] if line.strip())
        chars = sum(len(line.strip()) for line in el["block"])
        if size > limit or chars > climit:
            warnings.append("%s : %s trop long : %d lignes, %d caractères (repères : %d lignes, %d caractères)"
                            % (where, name(eid), size, chars, limit, climit))
        if t in V_TYPES and not abandoned(eid):
            stale = next((line for line in el["block"] if STALE_RE.search(line)), None)
            if stale:
                warnings.append("%s : %s, contenu peut-être périmé : « %s »" % (where, name(eid), stale.strip()[:90]))

    # 2bis. chaque phase de conception atteinte a au moins un élément
    for p in upto:
        if p in MAIN_TYPE and not live(MAIN_TYPE[p]):
            gaps.append("phase « %s » : aucun élément %s" % (p, MAIN_TYPE[p]))

    # 3. liens amont
    down = {eid: [] for eid in elements}
    ups = {}
    for eid, el in elements.items():
        if el["file"].startswith(("registre-doutes", "journal-decisions")):
            continue
        refs = [m.group(1) for m in REF_RE.finditer(field(el["block"], "Réfs amont"))]
        ups[eid] = refs
        t = etype(eid)
        if t == "BES" and not abandoned(eid):
            if not any(r.startswith("SCN-") for r in refs):
                gaps.append("%s : aucun scénario d'utilisation (SCN) en amont" % name(eid))
            for r in refs:
                if r in elements and r.startswith("SCN-"):
                    down[r].append(eid)
        if t in UPSTREAM and not abandoned(eid):
            if not refs:
                gaps.append("%s : aucune référence amont" % name(eid))
            for r in refs:
                if r in elements:
                    down[r].append(eid)
                    if etype(r) != UPSTREAM[t]:
                        errors.append("%s : doit dériver d'un %s, pas de %s" % (name(eid), UPSTREAM[t], r))

    # 4. couverture
    for eid in elements:
        t = etype(eid)
        if t not in COVERAGE or abandoned(eid):
            continue
        for needed in COVERAGE[t]:
            if (t, needed) in PHASES[phase] and not any(etype(d) == needed and not abandoned(d) for d in down[eid]):
                gaps.append("%s : aucun %s ne le couvre" % (name(eid), needed))

    # 4bis. chaque scénario est rejoué par au moins une recette
    if "TA" in written_types:
        replayed = set()
        for ta in live("TA"):
            replayed |= {m.group(1) for m in REF_RE.finditer(field(elements[ta]["block"], "Scénario rejoué"))}
        for scn in live("SCN"):
            if scn not in replayed:
                gaps.append("%s : rejoué par aucune recette (champ « Scénario rejoué » des TA)" % name(scn))

    # 5. exigence <-> test système, priorités
    if "REQ" in written_types:
        for eid in live("REQ"):
            block = elements[eid]["block"]
            cited = [m.group(1) for m in REF_RE.finditer(field(block, "Vérification")) if m.group(1).startswith("TS-")]
            for ts in cited:
                if ts in elements and eid not in ups.get(ts, []):
                    gaps.append("%s cite %s dans « Vérification », mais ce test ne cite pas l'exigence en amont"
                                % (name(eid), name(ts)))
            prio = first_word(field(block, "Priorité"))
            bes = [first_word(field(elements[b]["block"], "Priorité")) for b in ups.get(eid, []) if b in elements]
            bes = [p for p in bes if p in PRIORITY_RANK]
            if prio in PRIORITY_RANK and bes:
                top = max(bes, key=PRIORITY_RANK.get)
                if PRIORITY_RANK[top] > PRIORITY_RANK[prio]:
                    gaps.append("%s : priorité « %s » plus basse que celle de ses besoins (« %s »)"
                                % (name(eid), prio, top))

    # 6. conception détaillée : plus aucune valeur « (à vérifier) » ou « (à confirmer) »
    if "DES" in written_types:
        for eid in live("DES"):
            line = next((x for x in elements[eid]["block"] if TO_CHECK_RE.search(x)), None)
            if line:
                gaps.append("%s : contient encore une valeur non vérifiée : « %s »"
                            % (name(eid), TO_CHECK_RE.search(line).group(0)[:80]))

    # 7. doutes
    for eid in (e for e in elements if etype(e) == "DOU"):
        block = elements[eid]["block"]
        st, bl = status(eid).lower(), field(block, "Bloquant").lower()
        deadline = field(block, "Échéance")
        dphase = phase_of_deadline(deadline) if deadline else None
        if bl and not (bl.startswith("oui") or bl.startswith("non")):
            gaps.append("%s : « Bloquant » doit valoir Oui ou Non (« %s »)" % (name(eid), field(block, "Bloquant")))
        if deadline and dphase is None:
            gaps.append("%s : échéance non reconnue (« %s ») : nommer une phase" % (name(eid), deadline))
        if st.startswith("levé"):
            rep = field(block, "Réponse")
            if not rep or rep.lower().startswith("(à remplir"):
                gaps.append("%s : levé sans réponse écrite" % name(eid))
            continue
        if not st.startswith("ouvert"):
            continue
        if bl.startswith("oui"):
            if dphase and PHASE_ORDER.index(dphase) > pidx:
                warnings.append("%s : doute bloquant à partir de la porte « %s »" % (name(eid), dphase))
            else:
                blocking.append("%s : doute bloquant ouvert" % name(eid))
        elif bl.startswith("non"):
            if not deadline:
                gaps.append("%s : doute non bloquant sans échéance" % name(eid))
            elif dphase and PHASE_ORDER.index(dphase) <= pidx:
                gaps.append("%s : échéance atteinte (« %s ») : à lever ou à passer bloquant" % (name(eid), deadline))

    # 8. relectures : rapports présents, un vrai sort par constat
    if args.gate and phase in REVIEWERS:
        for agent in REVIEWERS[phase]:
            prefix = "REV-%s-%s-v" % (phase, agent)
            if not any(f.startswith(prefix) for f in review_files):
                gaps.append("revues/ : aucun rapport %s*.md (relecture obligatoire à la porte « %s »)" % (prefix, phase))
    for r in reviews:
        where = "%s:%d" % (r["file"], r["line"])
        sort = r["sort"]
        if not sort:
            gaps.append("%s : constat %s sans sort" % (where, r["num"] or "?"))
        elif PLACEHOLDER_RE.search(sort):
            gaps.append("%s : constat %s, sort non rempli (texte du gabarit)" % (where, r["num"] or "?"))
        elif (sort.lower().startswith("rejet") and re.search(r"bloquant|majeur", r["gravite"], re.I)
              and not re.search(r"[«\"]", sort)):
            gaps.append("%s : constat %s %s rejeté sans citer la réponse de l'utilisateur"
                        % (where, r["num"] or "?", r["gravite"]))

    # 9. phases d'exécution : tests exécutés et réussis
    for p, t in EXEC_PHASES.items():
        if PHASE_ORDER.index(p) <= pidx:
            for eid in live(t):
                st = status(eid)
                if st.startswith("Exécuté KO"):
                    gaps.append("%s : exécuté KO" % name(eid))
                elif not st.startswith("Exécuté OK"):
                    gaps.append("%s : non exécuté (statut « %s »)" % (name(eid), st or "absent"))

    # 10. phases franchies : éléments validés
    if args.porte_franchie:
        for eid in elements:
            t = etype(eid)
            if t not in written_types or abandoned(eid):
                continue
            st = status(eid)
            ok = st.startswith("Validé") or (t in T_TYPES and st.startswith("Exécuté"))
            if not ok:
                gaps.append("%s : phase franchie mais statut « %s »" % (name(eid), st or "absent"))

    # rapport
    counts = {p: sum(1 for e in elements if e.startswith(p + "-")) for p in PREFIXES}
    print("Éléments : " + (", ".join("%s=%d" % (p, c) for p, c in counts.items() if c) or "aucun"))
    for title, items in (("ERREURS", errors), ("ÉCARTS", gaps), ("DOUTES BLOQUANTS", blocking),
                         ("AVERTISSEMENTS", warnings)):
        if items:
            print("\n%s (%d)" % (title, len(items)))
            for i in items:
                print("  - " + i)

    if args.matrice:
        rows = ["# Matrice de traçabilité", "",
                "> Généré par `tools/check_traceability_V2.py`. Ne pas modifier à la main.", "",
                "| Besoin | Exigence | Architecture | Test système |", "|---|---|---|---|"]
        for rid in sorted(e for e in elements if e.startswith("REQ-")):
            bes = ", ".join(name(b) for b in ups.get(rid, []) if b in elements) or "—"
            arc = ", ".join(name(d) for d in down[rid] if d.startswith("ARC-")) or "—"
            ts = ", ".join(name(d) for d in down[rid] if d.startswith("TS-")) or "—"
            rows.append("| %s | %s | %s | %s |" % (bes, name(rid), arc, ts))
        args.matrice.write_text("\n".join(rows) + "\n", encoding="utf-8")
        print("\nMatrice écrite : %s" % args.matrice)

    failed = bool(errors) or (args.gate and bool(gaps or blocking))
    summary = "%d erreur(s), %d écart(s), %d doute(s) bloquant(s), %d avertissement(s)" % (
        len(errors), len(gaps), len(blocking), len(warnings))
    print("\n%s%s [phase : %s] — %s" % ("ÉCHEC" if failed else "OK", " (mode porte)" if args.gate else "",
                                       phase, summary))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
