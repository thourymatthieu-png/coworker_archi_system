---
name: porte
description: "Déroule une porte de validation du cycle en V (relectures indépendantes, sort de chaque constat, contrôle outillé, synthèse, accord explicite de l'utilisateur, décision et étiquette). À utiliser quand les documents d'une phase sont rédigés et qu'on veut la clore ; argument : la phase (scenarios, besoins, exigences, architecture, conception, implementation, integration, systeme, recette) et, si besoin, le nom du projet."
---

Tu agis comme l'**architecte système** : applique `.claude/agents/architecte-systeme.md`, `CLAUDE.md` (§3 à §5), `framework/garde-fous-agents.md` et **`framework/portes.md`**, que cette procédure met en œuvre pas à pas.

Arguments : `$ARGUMENTS` → la phase, puis le projet. Si le projet n'est pas donné et qu'il n'y en a qu'un en cours, demande confirmation ; sinon, demande-le.

## 0. Préparer
- Lis `projets/<nom>/projet.md`, le `README.md` de chaque module actif (section « Conditions de porte ») et la liste de contrôle de la porte dans `framework/portes.md`.
- Lance `python tools/check_traceability_V2.py projets/<nom> --phase <phase>` (sans `--gate`) et corrige ou fais corriger ce qui relève de la rédaction avant les relectures.

## 1. Relectures indépendantes
Lance les relecteurs **en parallèle**, chacun comme une nouvelle instance, avec ce message et rien d'autre (pas de résumé, pas d'avis, pas de consigne d'indulgence) :

> Porte « <phase> » du projet <nom>. Fichiers à relire : <liste des chemins de la phase et des phases amont utiles>. Écris ton rapport dans `projets/<nom>/revues/REV-<phase>-<agent>-v<n>.md` selon `framework/templates/revues/gabarit-revue.md`, colonne « Sort » vide. Ne modifie aucun autre fichier.

| Phase | Relecteurs obligatoires |
|---|---|
| scenarios | `critique`, `coherence-clarte` |
| besoins, exigences | `critique`, `coherence-clarte`, `exigences-tracabilite` |
| architecture, conception | `critique`, `coherence-clarte`, `exigences-tracabilite`, `verificateur-sources` |
| implementation, integration, systeme, recette | `critique`, `coherence-clarte` |

À la porte « conception », si le projet a du matériel et du logiciel, fais aussi relire les interfaces ensemble par `electronique-hardware` et `logiciel-embarque` (rapport `REV-conception-interfaces-v1.md`).

## 2. Sort de chaque constat
- Lis chaque rapport en entier. Pour chaque constat, propose un sort : corrigé (où), `DOU-xxx` ouvert, rejeté (raison), risque accepté.
- Présente à l'utilisateur tout ce qui demande sa décision : rejet d'un constat bloquant ou majeur, risque à accepter, choix de niveau D2. Il décide ; tu cites sa réponse entre guillemets dans le sort.
- Remplis seulement la colonne « Sort » ; ne retouche jamais les autres colonnes d'un rapport.
- Après des corrections suite à un constat bloquant ou majeur, fais relire l'écart par le relecteur concerné (rapport `v<n+1>`).

## 3. Contrôle outillé
Lance `python tools/check_traceability_V2.py projets/<nom> --gate --phase <phase>` et lis tout le résultat. Tant qu'il échoue (erreur, écart, doute bloquant, rapport manquant, constat sans sort), la porte ne se présente pas. Vérifie aussi, case par case, la liste de `framework/portes.md` et les conditions de porte des modules actifs.

## 4. Synthèse et accord
Présente, dans cet ordre :
1. nombre de constats par gravité et leur sort (chemins des rapports) ;
2. décisions prises par délégation D1 pendant la phase, une ligne chacune ;
3. doutes ouverts non bloquants, avec leur échéance ;
4. risques acceptés ;
5. la question : « Accordez-vous la porte « <phase> » ? »

**Arrête-toi et attends la réponse.** Laisse à l'utilisateur le temps de lire ; ne prends pas un silence, un « ok » ambigu ou une autre question pour un accord.

## 5. Après un accord explicite
1. Décision `DEC-xxx` de porte dans `journal-decisions.md`, « Décidé par : Utilisateur » avec sa réponse citée mot pour mot.
2. Éléments de la phase et tests définis avec eux passés à « Validé ».
3. `python tools/check_traceability_V2.py projets/<nom> --porte-franchie <phase>` sans écart.
4. Mise à jour de `reprise.md`.
5. Propose le commit et l'étiquette `gate-<n>-<phase>-passed` ; ne les fais qu'avec l'accord de l'utilisateur.

## Ne jamais
- franchir la porte avec un doute bloquant ouvert, un constat sans sort, un rapport manquant ou l'outil en échec ;
- résumer un rapport en l'adoucissant, ou décider à la place de l'utilisateur.
