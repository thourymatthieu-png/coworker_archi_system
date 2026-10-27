# Registre de doutes

> **Aperçu** : tout doute, ambiguïté ou hypothèse est inscrit ici. Un doute **bloquant ouvert** empêche de franchir la porte de validation.

Format (exemple, non analysé) :

```
### DOU-001 — Titre court du doute
**Statut :** Ouvert | Levé
**Bloquant :** Oui | Non
**Concerne :** REQ-001 « Titre de l'exigence »
**Question :** ce qu'on ne sait pas.
**Réponse :** (à remplir, avec la source)
**Décision liée :** DEC-001 « Titre de la décision »
```

Les doutes levés sont déplacés dans l'archive en bas de ce fichier : on ne les supprime jamais, car les décisions les citent.

## Doutes ouverts

### DOU-009 — Quelle tolérance d'altitude pendant les 10 secondes de stationnaire ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « Il maintient son altitude » pendant 10 s : quelle variation d'altitude est acceptable (par exemple ± 10 cm) ? À lever avant la porte « exigences », car l'exigence doit être chiffrée. Voir aussi DOU-002 « Que veut dire ne pas dériver horizontalement ? » pour la dérive horizontale.
**Réponse :**
**Décision liée :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs »

### DOU-010 — Quelle rotation au lancer le drone doit-il rattraper ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Un lancer à la main fait souvent tourner le drone sur lui-même. Jusqu'à quelle rotation (en tours par seconde) l'utilisateur s'attend-il à ce que le vol réussisse ? À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :** DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol »

### DOU-011 — Quelle dérive horizontale reste acceptable si 30 cm n'est pas tenu ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** L'objectif de 30 cm sur 10 s n'est pas garanti. Si les essais montrent une dérive plus grande, jusqu'où l'utilisateur l'accepte-t-il dans une pièce d'appartement (par exemple 1 m, 2 m) ? Au-delà, revoit-on l'objectif ou le produit ?
**Réponse :**
**Décision liée :** DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais »

### DOU-012 — Quel angle limite et quelles autres valeurs de coupure retenir ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Question :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » retient 60° à titre provisoire. Quel angle, et quelle durée au-delà de laquelle on coupe (pour éviter une coupure sur une perturbation brève) ? À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »

### DOU-013 — Quelle durée de vol garantit-on après un armement accepté ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-003 « Échec : batterie faible à l'armement »
**Question :** Après un armement accepté, le vol (jusqu'à environ 27 s : 2 s de stabilisation, 10 s de stationnaire, 15 s de descente au plus) doit aller à son terme sans contrôle de la batterie en vol. Quelle marge de durée attend-on (par exemple deux fois la durée du vol) ? À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :** DEC-013 « Pas de contrôle de la batterie en vol »

### DOU-021 — Que se passe-t-il pour un lancer hors plage ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-002 « Échec : stationnaire non atteint dans le délai »
**Question :** Lancer trop bas, trop faible, trop fort ou sous un plafond bas : le drone le distingue-t-il d'un défaut du drone, et quel signal l'utilisateur reçoit-il (le même que l'échec de stabilisation ?) ? Voir DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol ». Que fait le drone s'il ne peut pas évaluer sa hauteur (sol non réfléchissant, vitre, escalier) ?
**Réponse :**
**Décision liée :**

### DOU-022 — À partir de quand compte le chrono des 10 secondes, et que fait un lancer avec le bouton encore appuyé ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Question :** Les 10 secondes de DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes » courent-elles depuis l'appui initial ou depuis l'armement (2 s plus tard) ? L'utilisateur qui lance à 9,9 s et relâche à 10,1 s désarme-t-il le drone ?
**Réponse :**
**Décision liée :** DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes »

### DOU-023 — Quel appui sur le bouton juste après le lancer est ignoré ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Un appui ou un relâchement parasite juste après le lancer ne doit pas déclencher l'arrêt d'urgence de DEC-015 « Bouton appuyé en vol : arrêt d'urgence » avec un signal trompeur. Pendant combien de temps après le lancer le bouton est-il ignoré, et quel appui volontaire reste pris en compte ?
**Réponse :**
**Décision liée :** DEC-015 « Bouton appuyé en vol : arrêt d'urgence »

### DOU-027 — Un signal distinct par information, ou par catégorie ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-005 « Un signal distinct pour chaque information » conduit à 17 signaux, alors qu'en vol l'utilisateur ne perçoit pas toujours les signaux (bruit des moteurs, drone qui s'éloigne). Faut-il un signal par catégorie (prêt, lancé, échec, posé), avec le détail réservé au suivi sur un autre appareil ?
**Réponse :**
**Décision liée :** DEC-005 « Un signal distinct pour chaque information »

### DOU-028 — Faut-il une limite de dérive avant la coupure, entre 10° et 60° d'inclinaison ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Question :** Entre le stationnaire (< 10°) et la coupure à 60° (DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »), un drone à 45° peut dériver de plusieurs mètres vers un mur ou une personne sans coupure. Faut-il une distance ou une durée maximale ? Élargit DOU-012 « Quel angle limite et quelles autres valeurs de coupure retenir ? ».
**Réponse :**
**Décision liée :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »

### DOU-029 — Quelle altitude maximale et quel plafond le drone doit-il tolérer ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** À 4 m/s vers le haut, le drone peut atteindre un plafond en 0,5 s. Quelle altitude maximale vise-t-on, et que se passe-t-il en cas de contact avec le plafond (DEC-014 « Pas de coupure sur choc en vol ») ? Voir DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol ».
**Réponse :**
**Décision liée :** DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol »

### DOU-030 — Les valeurs provisoires sont-elles à confirmer avant les exigences ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs », DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » et DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » portent des valeurs provisoires, à confirmer par essais, alors que leurs doutes sont « Levé ». Les considère-t-on comme levées pour la porte « scénarios », avec confirmation par essais avant la porte « exigences » ?
**Réponse :**
**Décision liée :**

### DOU-035 — Quelle hauteur de stationnaire vise-t-on ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Aucun scénario ne fixe la hauteur du stationnaire, en vol normal comme en vol de réglage. Elle dépend de la hauteur de lancer, et elle fixe la durée de la descente à 0,5 m/s (DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »). Quelle hauteur vise-t-on, ou quelle plage ? À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :**

### DOU-036 — Après quel délai le lien sans fil est-il considéré comme perdu ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** En vol de réglage, le drone atterrit sur place si le lien est perdu. Après combien de temps sans nouvelle de l'appareil de suivi le considère-t-on perdu, pour éviter un atterrissage sur une coupure brève ? À lever avant la porte « exigences ». Complément de la relecture de la porte : sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »), qu'appelle-t-on « le lien sans fil » ? Réception d'un appareil de suivi quelconque à portée ? À fusionner avec la définition du délai.
**Réponse :**
**Décision liée :**

### DOU-039 — La batterie est-elle vérifiée à chaque décollage de réglage ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Quel contrôle de batterie et de chauffe entre deux vols de réglage ? Y a-t-il une limite du nombre de vols ? DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » ne couvre que l'armement. Relevé par la relecture critique. Complément de la relecture de la porte : la batterie est-elle aussi vérifiée avant chaque vol de réglage, compte tenu de DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » ?
**Réponse :**
**Décision liée :**

### DOU-041 — Que fait le drone si on l'attrape ou s'il descend sur un obstacle ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Coupure, poursuite, signal ? Une main, une table ou une personne sous le drone en descente : que se passe-t-il ? Qui peut arrêter le drone sans saisir les hélices ? Scénario manquant proposé : drone récupéré à la main ou posé sur un obstacle. Relevé par la relecture critique.
**Réponse :**
**Décision liée :**

### DOU-042 — Quel autotest avant réarmement après un vol raté ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** L'armement exige-t-il l'immobilité du drone ou un autotest (hélices, mesures) ? DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement » dit « drone au sol et immobile » alors que SCN-001 « Vol nominal : de la batterie au posé » arme le drone dans la main. Après un vol raté, un drone abîmé peut être réarmé sans vérification. Relevé par la relecture critique. Complément de la relecture de la porte : DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement » parle d'un drone « au sol et immobile », alors que SCN-001 « Vol nominal : de la batterie au posé » arme le drone dans la main : quelle condition vaut vraiment ?
**Réponse :**
**Décision liée :**

### DOU-044 — Séquence de trois appuis : fenêtre et signal ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Les deux premiers appuis des trois donnent-ils le signal « Appui trop court » (SCN-004 « Dégradé : bouton relâché avant 2 secondes ») ? Quel délai entre appuis ? Que fait un appui long en mode réglage ? Le drone peut-il être tenu en main (DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie » impose un drone posé) ? Relevé par les deux relectures.
**Réponse :**
**Décision liée :**

### DOU-045 — Que fait un bouton enfoncé au branchement ou maintenu après désarmement ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Question :** Après le désarmement à 10 s, l'appui en cours est-il ignoré jusqu'au relâchement ? Que fait un bouton déjà enfoncé à la mise sous tension (poche, sac) ou pendant l'initialisation ? Précise DOU-022 « À partir de quand compte le chrono des 10 secondes, et que fait un lancer avec le bouton encore appuyé ? ». Relevé par la relecture critique.
**Réponse :**
**Décision liée :**

### DOU-046 — Capteur ou moteur défaillant en vol : quel comportement ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Mesure de hauteur perdue (sol non réfléchissant, escalier, vitre), hélice bloquée, protège-hélice détaché, moteur qui chauffe : quelle coupure, quel signal ? Scénario manquant proposé : mesure ou moteur défaillant en vol. Relevé par la relecture critique.
**Réponse :**
**Décision liée :**

### DOU-048 — Batterie : charge, remplacement, drone laissé allumé
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Question :** Comment la batterie est-elle chargée, remplacée, rangée ? Que fait un drone « allumé, en attente d'un appui » laissé branché des heures ? Y a-t-il un signal de batterie faible hors armement ? Scénario manquant proposé : maintenance de la batterie. Relevé par la relecture critique.
**Réponse :**
**Décision liée :**

### DOU-049 — Programmation : cas d'échec, hélices démontées, essai des moteurs avant le premier vol
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Question :** Que se passe-t-il si la programmation échoue ? La batterie est-elle branchée pendant la programmation, les hélices démontées (consigne de sécurité) ? Faut-il un essai des moteurs avant le premier vol ? Y a-t-il une reprogrammation ou un contrôle de version ? Reprend la partie oubliée de DOU-031 « Quelles opérations suivent la programmation à la mise en service ? ». Relevé par la relecture critique.
**Réponse :**
**Décision liée :**

### DOU-050 — Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Le critère de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » est-il mesurable et réaliste ? Lancé à l'envers depuis 1,5 m, une chute libre dure 0,55 s ; le drone peut toucher le sol avant la fin de la stabilisation, hélices tournantes. À lever avant la porte « exigences », avec DOU-030 « Les valeurs provisoires sont-elles à confirmer avant les exigences ? ». Relevé par la relecture critique.
**Réponse :**
**Décision liée :**

### DOU-052 — Que fait le drone qui redémarre immobile au sol après une coupure en vol ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol »
**Question :** SCN-011 « Dégradé : coupure d'alimentation en vol » suppose que le drone redémarre en mouvement et donne l'échec d'initialisation. Si l'alimentation revient quand le drone est déjà immobile au sol, l'initialisation réussit : annonce-t-il « Allumé » sans que l'utilisateur ait touché la batterie ? Faut-il toujours rebrancher la batterie ? Harmoniser DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement » et DEC-030 « Drone posé immobile à la mise sous tension ; refus de s'armer si l'initialisation échoue ». Relevé par les deux relectures.
**Réponse :**
**Décision liée :**

### DOU-053 — Quels signaux pour les vols de réglage et pour le lien perdu ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Les signaux de vol (Lancé, Stabilisation, En vol stationnaire, Atterrissage, Posé) valent-ils pour les vols de réglage ? Quel signal pour un lien perdu et l'atterrissage sur place qui en résulte ? Relevé par la relecture de cohérence. Complément de la relecture de la porte : le drone acquitte-t-il les commandes sans fil reçues (Décoller, Arrêt, Modifier, Sauvegarder), et par quel signal ?
**Réponse :**
**Décision liée :**

### DOU-054 — Les décisions de solution technique restent-elles dans le journal ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-001 « Information de l'utilisateur par signaux lumineux, sonores et suivi sur un autre appareil », DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais », DEC-019 « Hauteur au-dessus du sol mesurée en vol » et DEC-024 « Mise en service par programmation avec un programmateur ST-LINK » fixent des solutions (LED et buzzer, centrale inertielle seule, capteur de distance, programmateur ST-LINK), alors que les scénarios ne doivent pas en décrire. Deux options : (a) les garder avec le statut « contrainte posée par l'utilisateur, à confirmer en architecture » ; (b) ne garder dans le journal que l'intention et déplacer la solution dans `notes-architecture.md`. Relevé par la relecture de cohérence.
**Réponse :**
**Décision liée :**

### DOU-058 — Valeurs d'origine et bornes numériques à fixer en architecture
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Les valeurs d'origine du drone neuf (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ») et d'éventuelles bornes numériques sont renvoyées à l'architecture par DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ». Les fixer en phase architecture, avec les essais.
**Réponse :**
**Décision liée :**

### DOU-059 — Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Sauvegarde des réglages (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage ») : la commande de sauvegarde est-elle acceptée en vol ? Que se passe-t-il si la batterie est coupée pendant l'écriture ? Comment détecter une mémoire « jamais écrite » (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ») sans contrôle d'intégrité, alors que DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » écarte la détection de corruption ?
**Réponse :**
**Décision liée :**

### DOU-060 — Que font les moteurs pendant un redémarrage ou une chute de tension, et la coupure de la batterie dans chaque état ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol »
**Question :** Quel est l'état des moteurs pendant un redémarrage ou une chute de tension, et que se passe-t-il si la batterie est coupée dans chacun des états du drone ? Précise SCN-011 « Dégradé : coupure d'alimentation en vol ».
**Réponse :**
**Décision liée :**

### DOU-061 — Quelle priorité entre le bouton et l'arrêt sans fil, et l'arrêt est-il pris en compte pendant la phase Lancé ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Quelle priorité entre le bouton et l'arrêt sans fil si les deux arrivent ensemble ? L'arrêt (bouton ou sans fil) est-il pris en compte pendant la phase « Lancé » avant le démarrage des moteurs (voir DOU-023 « Quel appui sur le bouton juste après le lancer est ignoré ? ») ?
**Réponse :**
**Décision liée :**

### DOU-062 — Où l'utilisateur est-il informé des limites d'emploi ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Où l'utilisateur est-il informé des limites d'emploi : plage de lancer (DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol »), lieu (DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires », DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur », DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu ») ? Notice, étiquette, ou rien ?
**Réponse :**
**Décision liée :**

### DOU-063 — Que se passe-t-il lors d'un choc contre un obstacle ou un plafond à 4 m/s ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Que se passe-t-il lors d'un choc contre un obstacle ou un plafond en vol, notamment à 4 m/s (DEC-014 « Pas de coupure sur choc en vol ») ? Étend DOU-041 « Que fait le drone si on l'attrape ou s'il descend sur un obstacle ? » et se rattache à DOU-029 « Quelle altitude maximale et quel plafond le drone doit-il tolérer ? ».
**Réponse :**
**Décision liée :**

### DOU-064 — Drone tenu en main, trois appuis et commande Décoller : quel risque pour la main ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Drone tenu en main, trois appuis puis commande « Décoller » : le drone décolle (DEC-038 « Mode réglage : décollage sans protection supplémentaire ») alors que la main est proche des hélices. Quel risque accepte-t-on ? Voir DOU-044 « Séquence de trois appuis : fenêtre et signal ? ».
**Réponse :**
**Décision liée :**

### DOU-065 — Quelles décisions relayées ou interprétées sont à confirmer explicitement à la porte ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Les décisions relayées à l'architecte ou interprétées (DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » à DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu ») sont-elles confirmées explicitement par l'utilisateur à la porte « scénarios » ? DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » et DEC-038 « Mode réglage : décollage sans protection supplémentaire » portent la mention « à confirmer à la porte ». À confirmer aussi : DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage » (après un arrêt, un échec ou un basculement en vol de réglage, le drone reste en mode réglage, ce que l'utilisateur n'a pas dit explicitement). À confirmer aussi : DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » (seuils de sécurité réglables sans borne, y compris par un tiers sans appairage).
**Réponse :**
**Décision liée :**

<!-- Ajouter les nouveaux doutes ci-dessus, avant ce marqueur, au même format, en dehors des blocs de code. -->

## Archive — doutes levés

### DOU-001 — Comment le drone informe-t-il l'utilisateur ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Le drone « informe » à 7 moments (allumé, prêt, lancé, stabilisation, stationnaire, atterrissage, posé). Par LED, buzzer, vibration, ou sans fil (téléphone) ? Combien de signaux distincts, sachant que le drone vole (la LED est-elle visible, le buzzer audible) ?
**Réponse :** LED RGB, buzzer et communication sans fil, combinés. Motifs précis à définir en architecture ; contenu de la liaison sans fil : voir DOU-008 « L'utilisateur veut-il suivre le vol depuis un autre appareil ? ».
**Décision liée :** DEC-001 « Information de l'utilisateur par signaux lumineux, sonores et suivi sur un autre appareil »

### DOU-002 — Que veut dire ne pas dériver horizontalement ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « Ne dérive pas horizontalement » exige de mesurer la position ou la vitesse horizontale (capteur de flux optique, par exemple). Veux-tu une dérive maximale chiffrée (en cm sur les 10 s), ou seulement une vitesse horizontale proche de zéro ? Le capteur de position est un surcoût en masse et en complexité pour un drone de poche.
**Réponse :** Centrale inertielle seule ; dérive maximale de 30 cm sur 10 s en objectif à valider par essais (non garanti).
**Décision liée :** DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais »

### DOU-003 — Quel délai pour atteindre le stationnaire ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « 2 secondes plus tard il doit être en vol stationnaire » : 2 s après le démarrage des moteurs ou après le lancer ? Est-ce un maximum (exigence) ou un objectif ? Quels seuils précis de vitesse et d'inclinaison pour dire « stationnaire » ?
**Réponse :** 2 s après le démarrage des moteurs, limite stricte ; stationnaire = vitesse < 0,3 m/s, inclinaison < 10°, tenues 0,5 s (provisoire, à confirmer par essais).
**Décision liée :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs »

### DOU-004 — Quelle plage de lancer et quelle orientation initiale ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « Dans n'importe quel sens » : le drone peut-il être lancé dans n'importe quelle orientation (à l'envers, de côté) ? Quelle plage de vitesse et d'angle de lancer le drone doit-il rattraper ? Quelle altitude minimale à la sortie de la main pour avoir le temps de se rétablir ?
**Réponse :** Toute orientation, y compris à l'envers ; vitesse de lancer 0,5 à 4 m/s vers le haut et l'avant ; hauteur d'au moins 1,5 m du sol (valeurs provisoires, à confirmer par essais).
**Décision liée :** DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol »

### DOU-005 — Que se passe-t-il si le drone n'y arrive pas ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Principe retenu : stationnaire non atteint dans le délai → moteurs coupés (DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai »). Retournement normal pendant la stabilisation (DEC-003 « Drone retourné ou très incliné : normal tant que la stabilisation n'est pas finie »). Batterie vérifiée à l'armement (DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible »). Reste à préciser : (a) une fois le stationnaire atteint, une inclinaison excessive ou un retournement doit-il couper les moteurs ? (b) la batterie peut-elle tomber en vol malgré la vérification à l'armement (seuil et marge) ? (c) un choc en vol (mur, plafond) coupe-t-il les moteurs ? (d) que fait le bouton appuyé en vol ?
**Réponse :** Stationnaire non atteint dans le délai : moteurs coupés (DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai »). Retournement normal pendant la stabilisation (DEC-003 « Drone retourné ou très incliné : normal tant que la stabilisation n'est pas finie »), mais moteurs coupés si le drone bascule après le stationnaire (DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »). Batterie vérifiée à l'armement seulement (DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » et DEC-013 « Pas de contrôle de la batterie en vol »). Pas de coupure sur choc (DEC-014 « Pas de coupure sur choc en vol »). Bouton appuyé en vol : moteurs coupés (DEC-015 « Bouton appuyé en vol : arrêt d'urgence »). Chaque cas a un signal distinct (DEC-005 « Un signal distinct pour chaque information »).
**Décision liée :** DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai », DEC-012 « Couper les moteurs si le drone bascule après le stationnaire », DEC-015 « Bouton appuyé en vol : arrêt d'urgence »

### DOU-006 — Comment éviter un départ des moteurs sans vrai lancer ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Les moteurs démarrent 200 ms après le relâchement du bouton. Si l'utilisateur relâche le bouton sans lancer (drone posé ou tenu en main), les hélices tournent. Que doit faire le drone (exigence de sécurité) ? Que se passe-t-il si le bouton est relâché avant 2 s ou maintenu très longtemps ?
**Réponse :** Le relâchement seul suffit (risque accepté : relâcher sans lancer démarre les moteurs). Relâché avant 2 s : retour en attente avec signal. Maintenu plus de 10 s : désarmement avec signal.
**Décision liée :** DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs », DEC-007 « Bouton relâché avant 2 secondes : retour en attente », DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes »

### DOU-007 — Quelles contraintes d'atterrissage ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Atterrissage « doux » : quelle vitesse maximale au contact ? Le drone se pose-t-il à l'endroit où il est (sol plat) ou revient-il vers le point de lancer ? Quelle durée de descente ?
**Réponse :** Le drone se pose sur place ; vitesse au contact de 0,5 m/s au plus ; descente de 15 s au plus, après quoi les moteurs sont coupés.
**Décision liée :** DEC-020 « Atterrissage sur place », DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »

### DOU-008 — L'utilisateur veut-il suivre le vol depuis un autre appareil ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Veut-il voir les états du vol sur un téléphone ou un ordinateur, en plus de ce que le drone signale lui-même ? Faut-il un geste préalable avant le vol ? Le vol doit-il fonctionner sans cet appareil (par défaut oui) ?
**Réponse :** Oui : le drone retourne à un appareil de suivi les variables du vol (commandes des moteurs, hauteur, autres données de position). L'appareil n'est pas précisé à ce stade ; la technologie relève de l'architecture.
**Décision liée :** DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol »

### DOU-014 — Quel scénario de mise en service faut-il écrire ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Question :** Premier montage : flash du micrologiciel avec le ST-LINK, première mise sous tension, calibrage de la centrale inertielle, test des moteurs hélices démontées, sens de rotation, réglage des seuils (batterie, angle). Que doit pouvoir faire l'utilisateur, dans quel ordre, et que se passe-t-il si le calibrage échoue ? Relevé par la relecture du critique à la porte « scénarios ».
**Réponse :** La mise en service est la programmation du ou des microcontrôleurs avec un programmateur ST-LINK (seul outil de programmation disponible), via JTAG ou SWD ; scénario SCN-008 « Mise en service : programmation du drone » écrit. Les opérations suivantes (calibrage, essais des moteurs) font l'objet de DOU-031 « Quelles opérations suivent la programmation à la mise en service ? ».
**Décision liée :** DEC-024 « Mise en service par programmation avec un programmateur ST-LINK »

### DOU-015 — Que se passe-t-il si l'initialisation échoue ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Si le drone n'est pas en état de voler au démarrage (mesure absente, drone déplacé au démarrage), annonce-t-il « allumé » à tort ? Faut-il exiger un drone immobile à la mise sous tension et un signal distinct d'échec ?
**Réponse :** L'utilisateur pose le drone immobile avant de brancher la batterie. Si le drone n'est pas en état de voler au démarrage, il refuse de s'armer, ignore le bouton et donne un signal d'échec d'initialisation distinct ; on en sort en débranchant puis rebranchant la batterie. Durée d'immobilité : à fixer en exigences.
**Décision liée :** DEC-030 « Drone posé immobile à la mise sous tension ; refus de s'armer si l'initialisation échoue »

### DOU-016 — Comment limiter le risque d'hélices en rotation sans lancer ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » accepte le risque sans le borner : relâchement en main, drone posé, doigt qui glisse. Faut-il, au minimum, une coupure rapide des moteurs si aucun lancer n'est détecté, ou reconsidérer la confirmation par la centrale inertielle (écartée par DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs ») ? À arbitrer par l'utilisateur.
**Réponse :** Statu quo : aucune coupure ni confirmation ; risque accepté, limité par les protège-hélices obligatoires.
**Décision liée :** DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer »

### DOU-017 — Que se passe-t-il si l'alimentation est coupée ou chute en vol ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Un lancer vigoureux peut débrancher la batterie ou faire chuter la tension, et le microcontrôleur peut redémarrer en vol. Le drone peut-il alors se réarmer seul, notamment si le bouton est appuyé ? Décision attendue : jamais de réarmement automatique. La batterie est-elle mesurée à vide ou sous charge à l'armement (voir DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? ») ?
**Réponse :** Jamais de réarmement automatique après un redémarrage ; batterie mesurée à vide à l'armement, avec un seuil à marge large (valeur à fixer en DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? »).
**Décision liée :** DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement »

### DOU-018 — Quel est le comportement à l'atterrissage et après le posé ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Quel critère détecte « posé » (arrêt de la descente, choc) sans capteur supplémentaire ? Que se passe-t-il en cas de rebond, d'atterrissage de travers ou sur sol incliné ? La détection de basculement de DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » est-elle désactivée une fois posé ? Quel est l'état du drone après un posé ou une coupure (verrouillé, initialisé), et comment le réarme-t-on, jamais automatiquement ? À traiter avec DOU-007 « Quelles contraintes d'atterrissage ? ».
**Réponse :** Le drone se déclare posé et coupe ses moteurs à moins de 2 à 3 cm du sol (rebond couvert). Après le posé ou toute coupure, il est verrouillé ; un nouvel appui de 2 secondes sur le bouton le réarme, jamais automatiquement.
**Décision liée :** DEC-022 « Moteurs coupés à moins de 2 à 3 cm du sol », DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler »

### DOU-019 — Quel capteur donne l'altitude et la vitesse verticale ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » repose sur un capteur de hauteur, alors que DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais » retient une centrale inertielle seule. Sans capteur d'altitude, l'altitude se calcule par intégration et diverge. Faut-il un baromètre ou un capteur de distance ? À trancher avant les exigences, car cela change la carte.
**Réponse :** Capteur de distance de type ToF, orienté vers le bas, pour la hauteur et la vitesse verticale.
**Décision liée :** DEC-019 « Hauteur au-dessus du sol mesurée en vol »

### DOU-020 — Quel est le public visé et quel risque pour les personnes est acceptable ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Adulte seulement, ou enfant aussi ? Sans cette réponse, les risques de DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » et de DEC-014 « Pas de coupure sur choc en vol » (hélices nues qui continuent après un choc) ne peuvent pas être jugés. Protège-hélices obligatoires ou optionnels ? Norme jouet visée ou non ?
**Réponse :** Public adulte uniquement, pas de norme jouet ; protège-hélices obligatoires.
**Décision liée :** DEC-016 « Public adulte, protège-hélices obligatoires »

### DOU-024 — Comment arrêter un drone en vol sans le saisir ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Atteindre le bouton d'un drone en vol revient à l'attraper, hélices tournantes. Faut-il un arrêt d'urgence par le sans fil (voir DOU-008 « L'utilisateur veut-il suivre le vol depuis un autre appareil ? »), des protège-hélices, ou accepte-t-on que seul le bouton existe ?
**Réponse :** Deux moyens coexistent une fois le drone lancé : le bouton (DEC-015 « Bouton appuyé en vol : arrêt d'urgence ») et une commande d'arrêt sans fil, en vol normal comme en vol de réglage. Sans appareil de suivi, seul le bouton reste. Suites : DOU-025 « Le drone vole-t-il sans appareil de suivi ? », DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? », DOU-047 « Appareil de suivi : appairage, absence, plusieurs drones ».
**Décision liée :** DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil »

### DOU-025 — Le drone vole-t-il sans appareil de suivi ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Le drone arme-t-il et vole-t-il sans téléphone ni ordinateur ? Perdre le suivi en vol change-t-il quelque chose ? Lié à DOU-008 « L'utilisateur veut-il suivre le vol depuis un autre appareil ? ».
**Réponse :** Vol libre : le drone arme et vole sans appareil de suivi ; un appareil présent est un plus, pas une nécessité. La perte du lien en vol normal ne change rien. Les moyens d'arrêt sans fil et de suivi ne sont disponibles que si un appareil est relié (voir DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil »). Suites : DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? », DOU-047 « Appareil de suivi : appairage, absence, plusieurs drones ».
**Décision liée :** DEC-032 « Vol libre : le drone vole sans appareil de suivi »

### DOU-026 — L'utilisateur veut-il régler le drone depuis un autre appareil ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Veut-il seulement être informé, ou aussi régler le drone (seuils, valeurs) ? Si oui, dans quels états (au sol, désarmé seulement) ? Les réglages sont-ils conservés après coupure ?
**Réponse :** Oui : le drone doit être paramétrable sans fil, y compris en vol. États autorisés, entrée dans le mode réglage et conservation des réglages : voir DOU-032 « Comment entre-t-on dans le mode réglage et comment en sort-on ? », DOU-033 « Que fait le drone pendant les vols de réglage répétés ? » et DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? ».
**Décision liée :** DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol »

### DOU-031 — Quelles opérations suivent la programmation à la mise en service ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Question :** Après la programmation, l'utilisateur doit-il faire d'autres opérations avant le premier vol : calibrage des mesures du drone (drone immobile, à plat), essai des moteurs hélices démontées, vérification du sens de rotation, réglage de valeurs (seuil de batterie, angle de coupure) ? Dans quel ordre, et que se passe-t-il si la programmation ou le calibrage échoue ? Voir aussi DOU-015 « Que se passe-t-il si l'initialisation échoue ? ».
**Réponse :** Aucune opération imposée après la programmation à ce stade : un éventuel calibrage dépend des solutions techniques et sera défini en architecture. L'utilisateur règle ensuite le vol (SCN-009 « Réglage et suivi du drone par le sans fil »).
**Décision liée :** DEC-026 « Mise en service : calibrage éventuel renvoyé à l'architecture, réglage du vol par un scénario dédié »

### DOU-032 — Comment entre-t-on dans le mode réglage et comment en sort-on ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** L'utilisateur pense à trois appuis sur le bouton pour entrer dans le mode réglage, sans certitude. Faut-il ce geste, une commande sans fil, ou les deux ? Comment sort-on du mode (appui, commande, fin du délai, coupure de la batterie) ? Le drone signale-t-il l'entrée et la sortie ? Le mode réglage peut-il être déclenché par erreur pendant un vol normal ?
**Réponse :** Entrée par trois appuis sur le bouton, drone au sol et non armé ; le drone signale l'entrée. Sortie seulement par coupure de la batterie : après un redémarrage, le drone est en mode normal.
**Décision liée :** DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie »

### DOU-033 — Que fait le drone pendant les vols de réglage répétés ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** En mode réglage, le drone décolle, se pose, décolle, se pose, un certain nombre de fois sur un temps bref. Combien de cycles, quelle durée, quelle hauteur ? Décolle-t-il seul depuis le sol (exception au lancer à la main de DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs ») ou sur commande de l'utilisateur à chaque fois ? Que se passe-t-il si le lien sans fil est perdu, si l'utilisateur appuie sur le bouton (DEC-015 « Bouton appuyé en vol : arrêt d'urgence ») ou si les réglages rendent le vol instable ?
**Réponse :** Sur commande sans fil, le drone décolle depuis le sol, reste 3 secondes en stationnaire, puis se pose ; il coupe ses moteurs 15 secondes au plus après le décollage, stationnaire de 3 secondes fixe (voir DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu »). Si le lien sans fil est perdu en vol, il atterrit doucement sur place. Le bouton appuyé en vol reste un arrêt d'urgence. Hauteur et délai de lien perdu : DOU-035 « Quelle hauteur de stationnaire vise-t-on ? » et DOU-036 « Après quel délai le lien sans fil est-il considéré comme perdu ? ».
**Décision liée :** DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu »

### DOU-034 — Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Un mauvais réglage peut rendre le drone instable. Existe-t-il un retour aux valeurs d'origine ? Les réglages sont-ils conservés après coupure de la batterie, et que fait le drone au démarrage s'il n'a jamais été réglé ?
**Réponse :** Conservation : une commande sans fil sauvegarde les réglages, le drone charge au démarrage ses dernières valeurs depuis sa mémoire non volatile, sans configuration poussée par l'appareil de suivi (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage »). Retour à des réglages sûrs : pas de commande de retour aux valeurs d'origine (reprogrammation comme seul recours), mémoire corrompue non traitée, risques acceptés (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »). Drone neuf, mémoire jamais écrite : valeurs d'origine fixes du logiciel, sans signal particulier (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal »). Valeurs d'origine et bornes à fixer : DOU-038 « Réglages en vol : valeurs d'origine, bornes, coupures en vol de réglage ? ».
**Décision liée :** DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage », DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée », DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal »

### DOU-037 — Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Une commande d'arrêt d'urgence sans fil existe-t-elle ? La commande « Décoller » exige-t-elle un appairage, une confirmation, ou la vérification que le drone est posé, immobile et à plat ? Que fait le drone s'il est tenu en main ? Le seul arrêt est aujourd'hui le bouton (DEC-015 « Bouton appuyé en vol : arrêt d'urgence »), donc il faut attraper le drone hélices tournantes. Complète DOU-024 « Comment arrêter un drone en vol sans le saisir ? », levé par DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ». Impact de DEC-032 « Vol libre : le drone vole sans appareil de suivi » : la commande d'arrêt sans fil n'est disponible que si un appareil est relié, donc elle n'est pas une condition de sécurité du vol normal. Reste ouvert après cette commande d'arrêt : la commande d'arrêt sans fil existe, mais il faut encore trancher le décollage protégé en mode réglage (appairage, confirmation, drone posé, immobile et à plat, drone tenu en main). Impact de DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée » : sans appairage, le risque d'une commande « Décoller » parasite (tiers, autre drone) n'est plus couvert ailleurs, ce qui renforce la question de la protection du décollage. Relevé par la relecture critique.
**Réponse :** Pas de protection supplémentaire du décollage en mode réglage (interprétation de la réponse de l'utilisateur : « pour le moment il n'y a qu'un drone, il n'y a pas lieu de faire quelque chose de compliqué, lourd »), donc pas de 17e signal « Décollage refusé ». La commande d'arrêt d'urgence sans fil est couverte par DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ». Risque accepté : une commande « Décoller » parasite est possible, sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »).
**Décision liée :** DEC-038 « Mode réglage : décollage sans protection supplémentaire »

### DOU-038 — Réglages en vol : valeurs d'origine, bornes, coupures en vol de réglage ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Que fait un drone neuf non réglé ? (Répondu par DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal » : il utilise des valeurs d'origine fixes. Reste à fixer ces valeurs d'origine et leurs bornes.) Les coupures de stabilisation et de basculement (DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai », DEC-012 « Couper les moteurs si le drone bascule après le stationnaire ») valent-elles en vol de réglage ? Le réglage est-il limité au mode réglage ? Une valeur hors plage est-elle refusée ? Complète DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? ». Relevé par la relecture critique.
**Réponse :** Drone neuf : valeurs d'origine fixes (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal »). Les coupures de stabilisation et de basculement valent aussi en vol de réglage ; aucune borne sur les valeurs de réglage ; réglage possible aussi en vol normal, sans entrer dans le mode réglage (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal »). Les valeurs d'origine et les bornes numériques éventuelles sont renvoyées à l'architecture.
**Décision liée :** DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal », DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal »

### DOU-040 — Quel périmètre d'emploi et quelle zone libre minimale ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Intérieur seulement, ou jardin, avec quelles conditions (soleil, sol, herbe) ? Quelle zone libre minimale et quelle distance aux personnes pour un lancer à 4 m/s ? Un lancer à 4 m/s parcourt jusqu'à 8 m en 2 s, ce qui est incompatible avec une pièce d'appartement et avec la dérive de DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais ». Réponse partielle de l'utilisateur, consignée par DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires » : périmètre visé = appartement, gymnase et jardin en essais complémentaires. Lancer trop rapide pour la zone : hors plage, responsabilité de l'utilisateur (DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur »). Reste à trancher : zone libre minimale, distance aux personnes, plage de lancer à garder ou à restreindre en appartement; ancien libellé : lancer trop rapide pour la zone (hors plage ou plage de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » à restreindre). Relevé par la relecture critique.
**Réponse :** Périmètre visé : l'appartement, gymnase et jardin en essais complémentaires (DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires »). Lancer trop rapide pour le lieu : responsabilité de l'utilisateur (DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur »). Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu, incompatibilité appartement / 4 m/s acceptée (DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu »).
**Décision liée :** DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires », DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur », DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu »

### DOU-043 — Quel signal et quel état pour un délai de descente dépassé ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Si les 15 secondes de descente s'écoulent sans être à moins de 2 à 3 cm du sol, les moteurs sont coupés (DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs ») et SCN-001 « Vol nominal : de la batterie au posé » dit que le drone informe qu'il est posé, alors qu'il peut être en l'air. Même signal « Posé », signal d'échec distinct (DEC-005 « Un signal distinct pour chaque information »), ou cas impossible ? Relevé par les deux relectures.
**Réponse :** Signal distinct « Délai de descente dépassé » (17e signal), moteurs coupés, drone verrouillé selon DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler » (DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé »).
**Décision liée :** DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé »

### DOU-047 — Appareil de suivi : appairage, absence, plusieurs drones
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Comment l'appareil de suivi est-il relié au drone ? Le vol normal fonctionne-t-il sans lui ? Une perte de lien en vol normal change-t-elle quelque chose ? (Répondu par DEC-032 « Vol libre : le drone vole sans appareil de suivi » : oui, vol libre, la perte de lien ne change rien en vol normal.) Reste à trancher : appairage, présence de l'appareil, plusieurs drones. Que se passe-t-il avec deux drones dans la même salle ? Recoupe DOU-025 « Le drone vole-t-il sans appareil de suivi ? ». Impact de DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » : la commande d'arrêt sans fil impose un appairage sûr (pas d'arrêt par l'appareil d'un autre drone ou d'un tiers). Scénario manquant proposé : appareil de suivi absent ou lien perdu hors mode réglage. Relevé par la relecture critique.
**Réponse :** Pas d'appairage : le drone obéit à tout appareil de suivi à portée (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »). Le vol normal fonctionne sans appareil de suivi et la perte de lien ne change rien en vol normal (DEC-032 « Vol libre : le drone vole sans appareil de suivi »). Question sur le nombre d'appareils appairés : sans objet sans appairage. Conséquences résiduelles : un tiers ou l'appareil d'un autre drone peut envoyer arrêt, décollage de réglage ou sauvegarde ; une commande peut atteindre plusieurs drones à portée ; le suivi peut être mélangé si plusieurs drones sont à portée. À traiter en architecture si besoin.
**Décision liée :** DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée », DEC-032 « Vol libre : le drone vole sans appareil de suivi »

### DOU-051 — L'état verrouillé est-il le même que l'état allumé, en attente d'un appui ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Après un posé ou une coupure, DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler » prévoit un nouvel appui de 2 s sans débrancher la batterie. Cet état « verrouillé » est-il le même que « Allumé, en attente d'un appui » (mêmes vérifications, mêmes signaux) ? Dans le diagramme d'états, « Posé » et « Moteurs coupés en vol » n'ont aujourd'hui aucune sortie. Relevé par la relecture de cohérence.
**Réponse :** Oui : l'état verrouillé est le même que « Allumé, en attente d'un appui » (DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »). Risque accepté : aucune vérification après une chute ; voir DOU-042 « Quel autotest avant réarmement après un vol raté ? » et DOU-052 « Que fait le drone qui redémarre immobile au sol après une coupure en vol ? ».
**Décision liée :** DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »

### DOU-055 — Le signal Arrêt sans fil (16e signal) est-il validé ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Pour respecter DEC-005 « Un signal distinct pour chaque information », l'architecte a ajouté un 16e signal « Arrêt sans fil » après DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ». Garde-t-on un signal distinct pour l'arrêt sans fil, ou le même signal que « Arrêt par le bouton » ? Voir aussi DOU-027 « Un signal distinct par information, ou par catégorie ? ».
**Réponse :** Le 16e signal est validé et reste distinct du signal n° 14 « Arrêt par le bouton ».
**Décision liée :** DEC-033 « Signal Arrêt sans fil distinct du signal Arrêt par le bouton »

### DOU-056 — Commande sans fil et état du drone : que fait chaque commande dans chaque état ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Partie levée par DEC-043 « Commandes sans fil acceptées selon l'état du drone » : table des commandes sans fil (Décoller, Arrêt, Modifier, Sauvegarder) selon l'état. **Reste ouvert :** après un vol de réglage terminé normalement, ou après un arrêt (bouton, sans fil, échec, basculement) en vol de réglage, le drone est-il verrouillé (DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler ») ou revient-il au mode réglage au sol, prêt à une nouvelle commande « Décoller » ? Tient compte de DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement », DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée », DEC-028 « Mode réglage : décollage depuis le sol sur commande sans fil » et DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu ». Relevé par les relectures de la porte « scénarios ».
**Réponse :** Table des commandes sans fil selon l'état : DEC-043 « Commandes sans fil acceptées selon l'état du drone ». État après un vol de réglage : le drone reste en mode réglage, posé, prêt à une nouvelle commande « Décoller », sans verrouillage (DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage », interprétation de la réponse de l'utilisateur). Le cas d'un arrêt ou d'un échec en vol de réglage est une lecture de l'architecte, à confirmer à la porte (DOU-065 « Quelles décisions relayées ou interprétées sont à confirmer explicitement à la porte ? »).
**Décision liée :** DEC-043 « Commandes sans fil acceptées selon l'état du drone », DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage »

### DOU-057 — Les seuils de sécurité sont-ils des paramètres réglables sans borne ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Les seuils de sécurité (délai de 2 s de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs », angle limite de DEC-012 « Couper les moteurs si le drone bascule après le stationnaire », délai de 15 s de DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs », seuil de batterie) sont-ils des paramètres réglables ? DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » dit que les coupures valent en vol de réglage (Q1) mais qu'aucune borne ne limite les valeurs (Q2) : un réglage sans borne peut désactiver une coupure. Contradiction à lever. Relevé par les relectures de la porte « scénarios ».
**Réponse :** Les seuils de sécurité sont réglables comme le reste, sans borne (DEC-045 « Seuils de sécurité réglables comme le reste, sans borne »). Conséquence acceptée : une valeur peut désactiver une coupure, y compris par un tiers sans appairage.
**Décision liée :** DEC-045 « Seuils de sécurité réglables comme le reste, sans borne »
