---
name: modification
description: "Modifie un élément déjà validé du cycle en V (scénario, besoin, exigence, architecture, conception ou test) sans laisser d'incohérence : doute, analyse d'impact, décision de l'utilisateur, mise à jour de tous les documents touchés, relecture de l'écart. À utiliser dès qu'un élément « Validé » doit changer, y compris quand le problème vient de l'aval (fiche technique, composant indisponible, test KO) ; argument : l'ID de l'élément et, si besoin, le projet."
---

Tu agis comme l'**architecte système** : applique `.claude/agents/architecte-systeme.md`, `CLAUDE.md` (§3 et §5), `framework/garde-fous-agents.md` et **`framework/procedure-modification.md`**, que cette procédure met en œuvre pas à pas.

Arguments : `$ARGUMENTS` → l'ID de l'élément (ex. `ARC-012`), puis le projet si plusieurs sont en cours.

## Étapes
1. **Doute** : ouvre un `DOU-xxx` qui décrit le problème et sa cause, avec sa source (fiche, mesure, réponse du fabricant, test).
2. **Analyse d'impact** :
   - vers l'amont : les éléments cités dans les « Réfs amont » de l'élément ;
   - vers l'aval : tous les éléments et tests qui citent l'élément (cherche son ID dans tous les fichiers du projet) ;
   - les décisions qui le citent, et les documents hors V (consignes d'emploi, risques acceptés, budgets, schémas, notes de module).
   Remonte jusqu'au niveau le plus haut réellement touché (tableau « Cas fréquents » de la procédure).
3. **Présentation à l'utilisateur** : le problème, la liste des éléments touchés (ID « titre »), les options avec leurs avantages et inconvénients, ta recommandation. Un élément de niveau D2 n'est jamais modifié par délégation. **Attends sa décision.**
4. **Décision** : `DEC-xxx` « Décidé par : Utilisateur », avec la ligne « Modifie : » qui liste chaque élément touché.
5. **Mise à jour dans le même lot** : passe les éléments touchés à « Modifié », corrige-les tous (fais rédiger chaque partie par l'expert concerné), puis vérifie qu'aucun passage ne dit « périmé », « à reporter » ou « tel document prévaut » : le texte faux est corrigé là où il est.
6. **Relecture de l'écart** : `critique`, `coherence-clarte` et `exigences-tracabilite`, plus `verificateur-sources` si des valeurs ont changé, chacun avec la seule liste des fichiers modifiés ; rapports `projets/<nom>/revues/REV-modification-<DOU>-<agent>-v<n>.md` ; un sort par constat.
7. **Retour à « Validé »** sur accord de l'utilisateur ; lève le doute ; `python tools/check_traceability_V2.py projets/<nom> --gate --phase <phase atteinte>` doit rendre OK. Mets à jour `reprise.md` et propose le commit (avec l'accord de l'utilisateur).
