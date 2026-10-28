# Reprise du projet Boomrone (état au 2026-10-28, après la refonte du bouton)

## Où on en est
Phase « scénarios » (`00-scenarios.md`), porte non franchie. 0 doute bloquant ouvert, 30 non bloquants. Le modèle du bouton a été refondu et inscrit le 2026-10-28 sur accord explicite de l'utilisateur donné en chat : DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court » à DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie ». `check_traceability` : aucune erreur de titre ni de référence ; seuls restent les trous « SCN sans BES » (normaux avant la phase besoins).

Règle de méthode (`CLAUDE.md` §5) : si une réponse contredit une décision antérieure, reposer la question, rappeler la réponse précédente, nommer la contradiction, demander si l'utilisateur change sa réponse.

## Modèle du bouton en vigueur (résumé)
- Appui validé = bouton maintenu 1 s, signal « Appui validé » ; moins de 1 s : rien (DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court »). Signal « Appui trop court » supprimé ; SCN-004 « Dégradé : appui de moins de 2 secondes sur le bouton » refondu.
- Appuis d'affilée (écart d'environ 2 s au plus) ; trois appuis validés, drone posé et immobile : mode réglage dès la 3e validation, sans armement ; en mode réglage le bouton n'arme jamais (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »). DEC-058 « Trois appuis : fenêtre courte, sans signal parasite » et DEC-007 « Bouton relâché avant 2 secondes : retour en attente » sont marquées remplacées.
- 2 s d'appui : signal « Prêt » (batterie suffisante, drone immobile et à plat) ou signal unique « Armement refusé », cause sur le sans fil (DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone »).
- Armé entre 2 s et 10 s : relâchement = signal « Lancé », moteurs 200 ms plus tard, même sans lancer, risque accepté ; plus de 10 s : désarmement (DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard »).
- Décollage de réglage : batterie seulement (DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre »). Initialisation en échec : définitive jusqu'au débranchement (DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie »).
- Tableau des signaux : toujours 17 (Appui trop court supprimé, Batterie faible remplacé par Armement refusé, Appui validé ajouté).

## Doutes nouveaux ou restés ouverts à cause de la refonte
- DOU-079 « Compteur d'appuis validés : remise à zéro par un appui court, cas limites » (hypothèse à confirmer).
- DOU-080 « Seuils de temps du bouton : 1 s, 2 s, 10 s et délai entre appuis » (valeurs provisoires, DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences »).
- DOU-081 « Bouton appuyé en vol de réglage : arrêt d'urgence ou non ? » (non tranché ; les scénarios gardent l'arrêt d'urgence de DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu » en attendant).
- DOU-082 « Sortie du mode réglage : coupure de la batterie seulement, non rediscutée ».
- DOU-083 « Contenu du statut sans fil d'un armement ou d'un décollage refusé ».
- Partiellement répondus, restés ouverts : DOU-073 « Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ? » (reste : tolérance d'« immobile », ordre des tests, appui de plus de 10 s sans armement, bouton après refus), DOU-074 « Une initialisation en échec est-elle définitive jusqu'au débranchement, et la condition à plat vaut-elle aussi après une coupure en vol ? » (reste : la condition à plat au redémarrage après une coupure en vol), DOU-039 « La batterie est-elle vérifiée à chaque décollage de réglage ? » (reste : seuil, chauffe, limite de vols, signal de refus).
- DOU-078 « La commande Sauvegarder est-elle acceptée à l'état armé, alors que l'écriture en mémoire peut retarder le lancer ? » absorbe le point « états d'initialisation et d'échec dans la table des commandes sans fil ».
- Levés : DOU-077 « Séquence de trois appuis : cas incomplets et ambigus » ; la réponse de DOU-044 « Séquence de trois appuis : fenêtre et signal ? » est conservée mais remplacée.

## À faire ensuite
1. Diagrammes : scinder le diagramme d'états de la vue d'ensemble en 3 (non fait volontairement) ; ajouter le lien perdu et le délai de 15 s en vol de réglage, la coupure d'alimentation en phase « Lancé », la branche du signal « Délai de descente dépassé » dans la séquence de SCN-001 « Vol nominal : de la batterie au posé », le sous-état « bouton à relâcher » (DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement ») ; retirer les ID sans titre des libellés ou ajouter une légende. Déjà fait : note de garde de SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol » dans la seule branche bouton, branche « immobile au sol » de SCN-011 « Dégradé : coupure d'alimentation en vol ».
2. Glossaire : restent « En vol » (périmètre), « Posé » / « Moteurs coupés », « descente » = atterrissage. Fait : Appui validé, Armé, Lancé, Armement refusé, drone = Boomrone.
3. Refaire les relectures de porte (`critique`, `coherence-clarte`) sur cette version, y compris le contrôle de la cohérence des diagrammes avec le modèle du bouton.
4. Accord explicite de l'utilisateur pour la porte « scénarios » (et confirmation de DOU-065 « Quelles décisions relayées ou interprétées sont à confirmer explicitement à la porte ? »).
