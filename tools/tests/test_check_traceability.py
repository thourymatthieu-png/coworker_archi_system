"""Tests de tools/check_traceability_V2.py sur de petits projets construits à la volée.
Lancer : python -m unittest discover -s tools/tests -v
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "check_traceability_V2.py"

SCN = """# Scénarios
### SCN-001 — Allumer la lampe
**Réfs amont :** Utilisateur (entretien du 2026-01-01)
**Type :** Nominal
**Situation de départ :** lampe éteinte.
**Déroulé :** 1. appui sur le bouton.
**Résultat attendu :** la lampe s'allume.
**Statut :** {scn_statut}
"""
BES = """# Besoins
### BES-001 — Avoir de la lumière
**Réfs amont :** SCN-001 « Allumer la lampe »
**Énoncé :** l'utilisateur veut de la lumière.
**Priorité :** {bes_prio}
**Statut :** Validé
"""
REQ = """# Exigences
### REQ-001 — Allumage en moins d'une seconde
**Réfs amont :** BES-001 « Avoir de la lumière »
**Énoncé :** Quand le bouton est appuyé, le système doit allumer la lampe en 1,0 s (±0,1 s) au plus.
**Priorité :** {req_prio}
**Vérification :** essai, TS-001 « Mesure du temps d'allumage »
**Statut :** {req_statut}
"""
TESTS = """# Plans de test
### TS-001 — Mesure du temps d'allumage
**Réfs amont :** {ts_amont}
**Résultat attendu :** 1,0 s (±0,1 s) au plus.
**Statut :** {ts_statut}

### TA-001 — Recette de l'allumage
**Réfs amont :** BES-001 « Avoir de la lumière »
**Scénario rejoué :** {ta_scn}
**Résultat attendu :** la lampe s'allume.
**Statut :** Écrit
"""
DOUTES = """# Registre de doutes
```
### DOU-999 — Exemple dans un bloc de code, ignoré
```
{doutes}
"""
ARC = """### ARC-001 — Bloc lampe
**Réfs amont :** REQ-001 « Allumage en moins d'une seconde »
**Description :** une LED.
**Statut :** Validé
"""
DES = """### DES-001 — Circuit de la LED
**Réfs amont :** ARC-001 « Bloc lampe »
**Description :** courant 20 mA {des_marque}.
**Statut :** {des_statut}
"""
TESTS_BAS = """
### TI-001 — Intégration de la lampe
**Réfs amont :** ARC-001 « Bloc lampe »
**Résultat attendu :** la LED s'allume.
**Statut :** Écrit

### TU-001 — Mesure du courant de la LED
**Réfs amont :** DES-001 « Circuit de la LED »
**Résultat attendu :** 20 mA (±2 mA).
**Statut :** Écrit
"""
REVUE = ("| N° | Élément | Constat | Scénario d'échec | Gravité | Proposition | Sort |\n"
         "|---|---|---|---|---|---|---|\n"
         "| 1 | REQ-001 « Allumage en moins d'une seconde » | flou | x | {gravite} | y | {sort} |\n")
REVIEWERS = {"scenarios": ("critique", "coherence-clarte"),
             "exigences": ("critique", "coherence-clarte", "exigences-tracabilite"),
             "conception": ("critique", "coherence-clarte", "exigences-tracabilite", "verificateur-sources")}
DEFAULT = dict(scn_statut="Validé", bes_prio="Essentiel", req_prio="Essentiel", req_statut="Proposé",
               ts_amont="REQ-001 « Allumage en moins d'une seconde »", ts_statut="Écrit",
               ta_scn="SCN-001 « Allumer la lampe »", doutes="", des_marque="[fiche LED, rév. 2, p. 3]",
               des_statut="Proposé", reviews=("exigences",), sort="corrigé dans REQ-001", gravite="mineur",
               conception=False)


def build(tmp, **over):
    v = dict(DEFAULT, **over)
    p = Path(tmp)
    (p / "00-scenarios.md").write_text(SCN.format(**v), encoding="utf-8")
    (p / "01-besoins.md").write_text(BES.format(**v), encoding="utf-8")
    (p / "02-exigences.md").write_text(REQ.format(**v), encoding="utf-8")
    tests = TESTS.format(**v)
    if v["conception"]:
        (p / "03-architecture.md").write_text(ARC, encoding="utf-8")
        (p / "04-conception-detaillee.md").write_text(DES.format(**v), encoding="utf-8")
        tests += TESTS_BAS
    (p / "05-plans-de-test.md").write_text(tests, encoding="utf-8")
    (p / "registre-doutes.md").write_text(DOUTES.format(**v), encoding="utf-8")
    (p / "revues").mkdir()
    for phase in v["reviews"]:
        for agent in REVIEWERS[phase]:
            (p / "revues" / ("REV-%s-%s-v1.md" % (phase, agent))).write_text(REVUE.format(**v), encoding="utf-8")
    return p


def run(project, *args):
    r = subprocess.run([sys.executable, str(TOOL), str(project), *args],
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout


class CheckTraceability(unittest.TestCase):
    def check(self, args=("--gate", "--phase", "exigences"), expect_ok=True, contains=None, **over):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run(build(tmp, **over), *args)
            if expect_ok:
                self.assertEqual(code, 0, out)
            else:
                self.assertNotEqual(code, 0, out)
            if contains:
                self.assertIn(contains, out)
            return out

    # --- projet valide et références
    def test_projet_valide(self):
        self.check()

    def test_projet_vide(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run(Path(tmp), "--gate", "--phase", "scenarios")
            self.assertNotEqual(code, 0)
            self.assertIn("aucun élément SCN", out)

    def test_reference_sans_titre(self):
        self.check(expect_ok=False, contains="cité sans titre", ts_amont="REQ-001")

    def test_titre_ancien_dans_une_revue_tolere(self):
        self.check(sort="corrigé dans REQ-001 « Ancien titre »")

    # --- exigences et tests
    def test_test_qui_ne_cite_pas_son_exigence(self):
        self.check(expect_ok=False, contains="ne cite pas l'exigence", ts_amont="BES-001 « Avoir de la lumière »")

    def test_priorite_plus_basse_que_le_besoin(self):
        self.check(expect_ok=False, contains="priorité « souhaitable »", req_prio="Souhaitable")

    def test_scenario_sans_recette(self):
        self.check(expect_ok=False, contains="rejoué par aucune recette", ta_scn="aucun, inspection")

    def test_phase_d_execution_exige_tests_ok(self):
        self.check(args=("--phase", "systeme", "--gate"), expect_ok=False, contains="non exécuté",
                   reviews=())
        self.check(args=("--phase", "systeme"), ts_statut="Exécuté KO", reviews=(), contains="exécuté KO")

    # --- statuts
    def test_statut_inconnu(self):
        self.check(expect_ok=False, contains="statut inconnu", req_statut="Approuvé")

    def test_statut_modifie_bloque_la_porte(self):
        self.check(expect_ok=False, contains="en cours de modification", req_statut="Modifié")

    def test_porte_franchie_exige_valide(self):
        self.check(args=("--gate", "--porte-franchie", "exigences"), expect_ok=False,
                   contains="phase franchie mais statut « Proposé »")

    # --- doutes
    def test_doute_non_bloquant_sans_echeance(self):
        d = "### DOU-001 — Couleur\n**Statut :** Ouvert\n**Bloquant :** Non\n**Question :** quelle couleur ?\n"
        self.check(expect_ok=False, contains="sans échéance", doutes=d)

    def test_echeance_future_puis_atteinte(self):
        d = ("### DOU-001 — Couleur\n**Statut :** Ouvert\n**Bloquant :** Non\n"
             "**Échéance :** porte « architecture »\n**Question :** quelle couleur ?\n")
        self.check(doutes=d)
        self.check(args=("--phase", "architecture"), contains="échéance atteinte", doutes=d)

    def test_echeance_non_reconnue(self):
        d = ("### DOU-001 — Couleur\n**Statut :** Ouvert\n**Bloquant :** Non\n"
             "**Échéance :** plus tard\n**Question :** quelle couleur ?\n")
        self.check(expect_ok=False, contains="échéance non reconnue", doutes=d)

    def test_bloquant_flou(self):
        d = ("### DOU-001 — Couleur\n**Statut :** Ouvert\n**Bloquant :** À classer\n"
             "**Échéance :** porte « conception »\n**Question :** quelle couleur ?\n")
        self.check(expect_ok=False, contains="doit valoir Oui ou Non", doutes=d)

    def test_doute_bloquant_ouvert(self):
        d = "### DOU-001 — Tension\n**Statut :** Ouvert\n**Bloquant :** Oui\n**Question :** quelle tension ?\n"
        self.check(expect_ok=False, contains="doute bloquant ouvert", doutes=d)

    def test_doute_bloquant_a_une_porte_future(self):
        d = ("### DOU-001 — Tension\n**Statut :** Ouvert\n**Bloquant :** Oui\n"
             "**Échéance :** porte « conception »\n**Question :** quelle tension ?\n")
        self.check(doutes=d, contains="bloquant à partir de la porte « conception »")

    def test_doute_leve_sans_reponse(self):
        d = ("### DOU-001 — Couleur\n**Statut :** Levé\n**Bloquant :** Non\n"
             "**Question :** quelle couleur ?\n**Réponse :** (à remplir)\n")
        self.check(expect_ok=False, contains="levé sans réponse", doutes=d)

    # --- relectures
    def test_relectures_absentes(self):
        self.check(expect_ok=False, contains="aucun rapport REV-exigences-critique-v", reviews=())

    def test_constat_sans_sort(self):
        self.check(expect_ok=False, contains="constat 1 sans sort", sort="")

    def test_sort_texte_du_gabarit(self):
        self.check(expect_ok=False, contains="texte du gabarit",
                   sort="corrigé (où) / DOU-xxx / rejeté : raison / risque accepté : DEC-xxx")

    def test_rejet_majeur_sans_citation(self):
        self.check(expect_ok=False, contains="rejeté sans citer", gravite="majeur", sort="rejeté : inutile")
        self.check(gravite="majeur", sort="rejeté : l'utilisateur a répondu « garder tel quel »")

    # --- champs
    def test_champ_manquant(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = build(tmp)
            f = p / "02-exigences.md"
            f.write_text(f.read_text(encoding="utf-8").replace("**Vérification :**", "**Verif :**"), encoding="utf-8")
            code, out = run(p, "--gate", "--phase", "exigences")
            self.assertNotEqual(code, 0)
            self.assertIn("champ(s) manquant(s) : Vérification", out)
            code, _ = run(p, "--phase", "exigences")
            self.assertEqual(code, 0, "sans --gate, un écart ne fait pas échouer")

    # --- conception détaillée
    def test_conception_valeur_a_verifier_vue_avant_validation(self):
        args = ("--gate", "--phase", "conception")
        self.check(args=args, conception=True, reviews=("conception",))
        self.check(args=args, expect_ok=False, contains="valeur non vérifiée", conception=True,
                   reviews=("conception",), des_marque="(à vérifier, DOU-001 « Courant »)")
        self.check(args=args, expect_ok=False, contains="valeur non vérifiée", conception=True,
                   reviews=("conception",), des_marque="(à confirmer)")


if __name__ == "__main__":
    unittest.main()
