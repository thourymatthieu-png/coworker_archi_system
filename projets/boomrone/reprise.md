# Reprise du projet Boomrone (état au 2026-10-28, changement de poste)

## Où on en est
Phase « scénarios » (`00-scenarios.md`), porte non franchie. Les relectures `critique` et `coherence-clarte` sur les diagrammes ont été faites le 2026-10-28 (rapports non conservés dans le dépôt, synthèse ci-dessous). Titres de DEC/DOU corrigés : `check_traceability` ne signale plus d'erreur de titre.

## Prochaine étape décidée par l'utilisateur
**Refaire le comportement du bouton par une série de questions, pour obtenir un comportement simple.** Les décisions ci-dessous attendent cette refonte et ne sont pas encore inscrites au journal.

Règle de méthode (ajoutée à `CLAUDE.md` §5) : si une réponse contredit une décision antérieure, reposer la question, rappeler la réponse précédente, nommer la contradiction, demander si l'utilisateur change sa réponse.

## Réponses données en chat, pas encore consignées (DEC à écrire)
- En mode réglage, le bouton **n'arme pas** le drone (DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage » et SCN-009 « Réglage et suivi du drone par le sans fil » ont raison). **Contradiction à corriger** : DEC-058 « Trois appuis : fenêtre courte, sans signal parasite » écrit le contraire.
- Bouton armé relâché sans vrai lancer : **le drone démarre quand même** (DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » confirmée) ; signal « Lancé » possible sans lancer, risque accepté.
- Décollage en mode réglage : **vérifie la batterie seulement** (complète DEC-038 « Mode réglage : décollage sans protection supplémentaire »).
- Initialisation en échec : **définitive jusqu'au débranchement** (répond à DOU-074).
- Signal « Appui trop court » (immédiat ou retardé après la fenêtre des trois appuis) : **non tranché**, à reprendre dans la refonte du bouton. Recommandation : retardé.

## À faire ensuite
1. Série de questions sur le bouton, puis DEC correspondantes (avec la règle de contradiction).
2. Nouveaux doutes proposés par `critique` : décollage de réglage (batterie), signal « Lancé » sans lancer, états d'initialisation dans la table des commandes (à fusionner avec DOU-056).
3. Diagrammes : scinder le diagramme d'états de la vue d'ensemble en 3 ; ajouter le lien perdu et le délai de 15 s en vol de réglage, la coupure d'alimentation en phase « Lancé », la branche « immobile au sol » de SCN-011, la branche du signal « Délai de descente dépassé » dans SCN-001, le sous-état « bouton à relâcher » (DEC-059) ; corriger la note de garde de SCN-007 ; retirer les ID sans titre des libellés ou ajouter une légende.
4. Glossaire : « Armé » (drone immobile), phase « Lancé », périmètre de « En vol », « Posé » / « Moteurs coupés », « descente » = atterrissage, « drone » = Boomrone.
5. Refaire les relectures de porte, puis accord explicite de l'utilisateur pour la porte « scénarios ».
