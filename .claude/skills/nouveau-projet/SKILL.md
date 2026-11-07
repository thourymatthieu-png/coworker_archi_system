---
name: nouveau-projet
description: "Crée un nouveau projet embarqué à partir des gabarits du framework (projets/<nom>/), remplit son profil et ouvre la phase « scénarios » avec l'utilisateur. À utiliser quand l'utilisateur veut démarrer un nouveau projet ; argument : le nom du projet."
---

Tu agis comme l'**architecte système** : applique `.claude/agents/architecte-systeme.md`, `CLAUDE.md` et `framework/garde-fous-agents.md`.

Projet demandé : `$ARGUMENTS` (si vide, demande le nom à l'utilisateur).

## Étapes
1. **Nom** : en minuscules, sans espace ni accent (ex. `enregistreur-temperature`). Vérifie que `projets/<nom>/` n'existe pas ; s'il existe, arrête-toi et demande à l'utilisateur.
2. **Copie** : copie tout le contenu de `framework/templates/` dans `projets/<nom>/` (le dossier `revues/` et son gabarit compris). Ne modifie rien dans `framework/`.
3. **Profil** : demande à l'utilisateur, en une phrase, le but de l'appareil ; inscris le nom et le but dans `projets/<nom>/projet.md`. Laisse les autres rubriques « à déterminer » : elles seront décidées plus tard (le plus souvent en architecture), chacune par une décision `DEC-xxx`.
4. **Contrôle** : lance `python tools/check_traceability_V2.py projets/<nom> --phase scenarios`. Résultat attendu : OK, avec un seul écart « aucun élément SCN ».
5. **Phase « scénarios »** : explique en deux phrases la méthode (scénarios d'abord, puis besoins, exigences, architecture, conception détaillée, chacun fermé par une porte avec ton accord explicite). Puis pose les questions des scénarios, sans proposer de solution technique :
   - qui utilise l'appareil, où, dans quelles conditions ;
   - le cas nominal, du début à la fin ;
   - les cas dégradés et les cas d'échec (appuie-toi sur la section « Scénarios » de `framework/checklists/critique.md` : alimentation, coupure, liaison perdue, capteur défaillant, mauvais usage…) ;
   - la mise en service, la mise à jour, la maintenance.
   Rédige les scénarios avec l'utilisateur dans `projets/<nom>/00-scenarios.md`, au format du gabarit.
6. **Fin** : dis où en est le projet et que la porte se franchira avec `/porte scenarios`. Ne commite rien sans l'accord de l'utilisateur.
