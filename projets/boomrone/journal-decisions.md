# Journal des décisions

> **Aperçu** : toute décision (architecture, exigence, accord de porte) est consignée ici avec ses alternatives et sa raison. Les agents recommandent, **l'utilisateur décide**.

Format (exemple, non analysé) :

```
### DEC-001 — Titre court de la décision
**Date :** AAAA-MM-JJ
**Concerne :** ARC-001 « Titre de l'élément d'architecture »
**Décision :** ce qui est retenu.
**Alternatives écartées :** option A (raison), option B (raison).
**Raison :** pourquoi.
**Doutes levés :** DOU-001 « Titre du doute »
```

### DEC-001 — Information de l'utilisateur par signaux lumineux, sonores et suivi sur un autre appareil
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone informe l'utilisateur des 7 étapes du vol (allumé, prêt, lancé, stabilisation, stationnaire, atterrissage, posé) par trois moyens combinés : une LED RGB, un buzzer et une communication sans fil.
**Alternatives écartées :** LED RGB seule (moins redondant) ; buzzer seul (couvert par les moteurs) ; sans fil seul (dépend d'un téléphone sous les yeux).
**Raison :** choix de l'utilisateur ; redondance des canaux. Les motifs précis (couleurs, sons, messages) restent à définir en architecture. Depuis : DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée » — la solution (LED RGB, buzzer) n'est plus qu'une proposition pour l'architecture (`notes-architecture.md`) ; seule l'intention reste décidée : informer l'utilisateur par des signaux lumineux, des signaux sonores et un suivi sur un autre appareil relié sans fil.
**Doutes levés :** DOU-001 « Comment le drone informe-t-il l'utilisateur ? » — mais ouvre DOU-008 « L'utilisateur veut-il suivre le vol depuis un autre appareil ? »

### DEC-002 — Couper les moteurs si le stationnaire n'est pas atteint dans le délai
**Date :** 2026-10-27
**Concerne :** SCN-002 « Échec : stationnaire non atteint dans le délai »
**Décision :** Si le drone n'a pas atteint le vol stationnaire dans le délai maximal, il coupe ses moteurs. La valeur du délai maximal reste à définir (voir DOU-003 « Quel délai pour atteindre le stationnaire ? »). Depuis : le délai est fixé par DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs ».
**Alternatives écartées :** tenter d'atterrir sans stationnaire (complexe, drone instable) ; réessayer la stabilisation (chute plus haute ou plus violente).
**Raison :** choix de l'utilisateur ; simplicité et sécurité.
**Doutes levés :** (aucun, DOU-005 « Que se passe-t-il si le drone n'y arrive pas ? » reste ouvert pour les autres cas). Depuis : DOU-005 « Que se passe-t-il si le drone n'y arrive pas ? » est levé par DEC-012 « Couper les moteurs si le drone bascule après le stationnaire », DEC-013 « Pas de contrôle de la batterie en vol », DEC-014 « Pas de coupure sur choc en vol » et DEC-015 « Bouton appuyé en vol : arrêt d'urgence ».

### DEC-003 — Drone retourné ou très incliné : normal tant que la stabilisation n'est pas finie
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone peut être lancé dans n'importe quelle orientation. Tant qu'il n'a pas fini de se stabiliser, être retourné ou très incliné est normal et ne déclenche aucune coupure.
**Alternatives écartées :** couper les moteurs dès un angle limite dépassé ; essayer de se redresser seulement si l'angle est modéré.
**Raison :** choix de l'utilisateur ; cohérent avec un lancer dans n'importe quel sens. Conséquence : la coupure sur retournement ne concerne que la période après la stabilisation (cas non tranché : DOU-005 « Que se passe-t-il si le drone n'y arrive pas ? »). Depuis : DOU-005 « Que se passe-t-il si le drone n'y arrive pas ? » est levé, voir DEC-012 « Couper les moteurs si le drone bascule après le stationnaire ».
**Doutes levés :** (aucun)

### DEC-004 — Batterie vérifiée à l'armement : pas d'armement si batterie faible
**Date :** 2026-10-27
**Concerne :** SCN-003 « Échec : batterie faible à l'armement »
**Décision :** Au moment de l'armement, si la batterie est faible, le drone le signale et ne s'arme pas.
**Alternatives écartées :** atterrir doucement dès que la batterie devient faible en vol ; couper les moteurs en vol.
**Raison :** choix de l'utilisateur ; évite le cas de la batterie faible en vol, puisque le vol dure environ 15 secondes (depuis : jusqu'à environ 27 secondes, voir DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »). Reste à définir : le seuil, et la marge qui garantit un vol complet (voir DOU-005 « Que se passe-t-il si le drone n'y arrive pas ? »). Depuis : DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone » — la décision reste valable sur le fond (pas d'armement si batterie faible), mais le signal « Batterie faible » local est remplacé par le signal « Armement refusé ».
**Doutes levés :** (aucun)

### DEC-005 — Un signal distinct pour chaque information
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Chaque fois que le drone informe l'utilisateur, il utilise un signal différent. Cela vaut pour les 7 étapes du vol et pour les échecs.
**Alternatives écartées :** signal générique d'échec ; aucun signal d'échec.
**Raison :** choix de l'utilisateur ; l'utilisateur doit toujours savoir de quoi il s'agit. Complète DEC-001 « Information de l'utilisateur par signaux lumineux, sonores et suivi sur un autre appareil ».
**Doutes levés :** (aucun)

### DEC-006 — Le relâchement du bouton armé suffit à démarrer les moteurs
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Une fois le drone armé (bouton maintenu 2 secondes), le relâchement du bouton signale le lancer et suffit : les moteurs démarrent 200 ms plus tard, sans confirmation que le drone a réellement été lancé.
**Alternatives écartées :** confirmer le lancer par la mesure du mouvement (accélération puis chute libre) avant de démarrer les moteurs.
**Raison :** choix de l'utilisateur ; simplicité. Risque résiduel accepté : un relâchement du bouton sans lancer démarre les moteurs, drone en main ou posé. Depuis : confirmée par l'utilisateur le 2026-10-28, signal « Lancé » possible sans lancer, risque accepté (DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard »).
**Doutes levés :** DOU-006 « Comment éviter un départ des moteurs sans vrai lancer ? »

### DEC-007 — Bouton relâché avant 2 secondes : retour en attente
**Date :** 2026-10-27
**Remplacée par :** DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court » le 2026-10-28, après la refonte du bouton demandée par l'utilisateur. Cette décision n'est plus en vigueur ; elle est conservée pour l'historique.
**Concerne :** SCN-004 « Dégradé : appui de moins de 2 secondes sur le bouton »
**Décision :** Si le bouton est relâché avant 2 secondes, le drone n'est pas armé : les moteurs ne démarrent pas et il revient à l'état « allumé, en attente d'un appui », prêt pour un nouvel appui. Le drone signale cet appui trop court avec un signal distinct (voir DEC-005 « Un signal distinct pour chaque information »).
**Alternatives écartées :** aucun signal à l'utilisateur.
**Raison :** choix de l'utilisateur ; l'utilisateur ne doit pas croire que le drone est armé.
**Doutes levés :** DOU-006 « Comment éviter un départ des moteurs sans vrai lancer ? »

### DEC-008 — Désarmement si le bouton reste appuyé plus de 10 secondes
**Date :** 2026-10-27
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Décision :** Si le bouton reste appuyé plus de 10 secondes, le drone se désarme et le signale avec un signal distinct (voir DEC-005 « Un signal distinct pour chaque information »). Pour réarmer, l'utilisateur relâche le bouton puis recommence un appui de 2 secondes.
**Alternatives écartées :** rester armé sans limite de durée.
**Raison :** choix de l'utilisateur ; évite un drone armé en permanence qui démarrerait au premier relâchement.
**Doutes levés :** DOU-006 « Comment éviter un départ des moteurs sans vrai lancer ? »

### DEC-009 — Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone doit être en vol stationnaire au plus tard 2 secondes après le démarrage de ses moteurs, soit environ 2,2 s après le lancer. C'est une limite stricte : au-delà, il coupe ses moteurs (voir DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai »). Le vol stationnaire est atteint quand la vitesse (horizontale et verticale) est inférieure à 0,3 m/s et l'inclinaison inférieure à 10°, tenues pendant 0,5 s. Valeurs provisoires, à confirmer par essais.
**Alternatives écartées :** chrono depuis le relâchement du bouton (plus exigeant) ; objectif de 2 s avec coupure à un délai plus long ; seuils plus stricts (< 0,1 m/s, < 5°, 1 s) ou plus souples (< 0,5 m/s, < 15°, 0,3 s).
**Raison :** choix de l'utilisateur ; critère mesurable par le drone lui-même. Depuis : le critère de stationnaire exige en plus que le drone soit en l'air, au-dessus d'une hauteur minimale, voir DEC-049 « Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale ». Depuis : DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences » — valeurs provisoires (dont le délai de 2 s), à confirmer avant la porte « exigences ».
**Doutes levés :** DOU-003 « Quel délai pour atteindre le stationnaire ? » — mais ouvre DOU-009 « Quelle tolérance d'altitude pendant les 10 secondes de stationnaire ? »

### DEC-010 — Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone doit se stabiliser quand il est lancé (a) dans n'importe quelle orientation, y compris à l'envers ; (b) à une vitesse de lancer de 0,5 à 4 m/s, vers le haut et vers l'avant ; (c) depuis une hauteur d'au moins 1,5 m du sol. Valeurs provisoires, à confirmer par essais.
**Alternatives écartées :** inclinaison initiale limitée à 90° ; plage de vitesse 1 à 3 m/s ou 0,5 à 6 m/s ; hauteur minimale de 1 m ou aucune.
**Raison :** choix de l'utilisateur ; cohérent avec DEC-003 « Drone retourné ou très incliné : normal tant que la stabilisation n'est pas finie » et avec le délai de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs ». Depuis : DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences » — valeurs provisoires (0,5 à 4 m/s, au moins 1,5 m), y compris les limites de la plage, à confirmer avant la porte « exigences ».
**Doutes levés :** DOU-004 « Quelle plage de lancer et quelle orientation initiale ? » — mais ouvre DOU-010 « Quelle rotation au lancer le drone doit-il rattraper ? »

### DEC-011 — Dérive de 30 cm sur 10 s en objectif à valider par essais
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone mesure son mouvement avec une centrale inertielle seule, sans capteur de position (pas de flux optique). La dérive horizontale maximale de 30 cm sur les 10 secondes de stationnaire est un **objectif**, à valider par essais, et non une exigence garantie.
**Alternatives écartées :** capteur de flux optique avec dérive de 30 cm garantie (recommandé par l'architecte : seul moyen fiable de tenir 30 cm) ; centrale inertielle seule sans objectif de dérive.
**Raison :** choix de l'utilisateur, après avertissement de l'architecte : sans capteur de position, la vitesse horizontale se calcule par intégration et dérive (un défaut d'inclinaison de 0,5° produit plusieurs mètres de dérive en 10 s), donc l'objectif de 30 cm risque de ne pas être tenu. Risque accepté : l'échec pourrait n'apparaître qu'après la fabrication de la carte chez JLCPCB. Depuis : DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée » — la solution (centrale inertielle seule, sans capteur de position) n'est plus qu'une proposition pour l'architecture (`notes-architecture.md`) ; seule l'intention reste décidée : une dérive horizontale de 30 cm au plus sur les 10 secondes de stationnaire, objectif à valider par essais et non exigence garantie, sans préjuger du moyen de mesure.
**Doutes levés :** DOU-002 « Que veut dire ne pas dériver horizontalement ? » — mais ouvre DOU-011 « Quelle dérive horizontale reste acceptable si 30 cm n'est pas tenu ? »

### DEC-012 — Couper les moteurs si le drone bascule après le stationnaire
**Date :** 2026-10-27
**Concerne :** SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Décision :** Une fois le stationnaire atteint, si le drone s'incline au-delà d'un angle limite (valeur provisoire : 60°, à confirmer par essais) ou se retourne, il coupe ses moteurs et le signale avec un signal distinct. Cela vaut pendant le stationnaire et la descente. Complète DEC-003 « Drone retourné ou très incliné : normal tant que la stabilisation n'est pas finie ».
**Alternatives écartées :** essayer de se redresser (complexité du comportement de redressement).
**Raison :** choix de l'utilisateur ; un drone déjà stabilisé qui bascule est hors de contrôle. Depuis : DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences » — valeur provisoire (angle limite de 60°), à confirmer avant la porte « exigences ».
**Doutes levés :** DOU-005 « Que se passe-t-il si le drone n'y arrive pas ? » — mais ouvre DOU-012 « Quel angle limite et quelles autres valeurs de coupure retenir ? »

### DEC-013 — Pas de contrôle de la batterie en vol
**Date :** 2026-10-27
**Concerne :** SCN-003 « Échec : batterie faible à l'armement »
**Décision :** Le drone ne contrôle pas la batterie pendant le vol. La vérification se fait uniquement à l'armement (DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible »), avec un seuil d'armement qui garantit un vol complet avec marge.
**Alternatives écartées :** atterrir doucement si la batterie baisse en vol ; couper les moteurs en vol.
**Raison :** choix de l'utilisateur ; simplicité, le vol dure environ 15 secondes (depuis : jusqu'à environ 27 secondes, voir DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »). Risque résiduel accepté : si le seuil est mal choisi, la batterie peut lâcher en vol. À valider par essais.
**Doutes levés :** DOU-005 « Que se passe-t-il si le drone n'y arrive pas ? » — mais ouvre DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? »

### DEC-014 — Pas de coupure sur choc en vol
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Un choc en vol (mur, plafond, personne) ne coupe pas les moteurs. Le drone continue de se stabiliser ; une perturbation trop grande est couverte par DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai » et DEC-012 « Couper les moteurs si le drone bascule après le stationnaire ».
**Alternatives écartées :** couper les moteurs sur choc détecté (risque de fausses détections).
**Raison :** choix de l'utilisateur.
**Doutes levés :** DOU-005 « Que se passe-t-il si le drone n'y arrive pas ? »

### DEC-015 — Bouton appuyé en vol : arrêt d'urgence
**Date :** 2026-10-27
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Si le bouton est appuyé pendant le vol, le drone coupe ses moteurs immédiatement et le signale avec un signal distinct.
**Alternatives écartées :** ignorer le bouton en vol.
**Raison :** choix de l'utilisateur ; arrêt d'urgence sans capteur supplémentaire.
**Doutes levés :** DOU-005 « Que se passe-t-il si le drone n'y arrive pas ? »

### DEC-016 — Public adulte, protège-hélices obligatoires
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone s'adresse à des adultes uniquement ; aucune norme jouet n'est visée. Les protège-hélices sont obligatoires : le drone ne vole pas sans, et leur masse et leur poussée sont prises en compte dans le dimensionnement des moteurs et de la batterie.
**Alternatives écartées :** protège-hélices optionnels (risque reporté sur l'utilisateur) ; enfants possibles avec norme jouet (impact trop fort sur l'architecture et le calendrier).
**Raison :** choix de l'utilisateur, sur recommandation de l'architecte : borne le risque de DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » et de DEC-014 « Pas de coupure sur choc en vol ».
**Doutes levés :** DOU-020 « Quel est le public visé et quel risque pour les personnes est acceptable ? »

### DEC-017 — Pas de protection supplémentaire contre les hélices en rotation sans lancer
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-002 « Échec : stationnaire non atteint dans le délai »
**Décision :** DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » est maintenu tel quel : pas de coupure rapide si aucun lancer n'est détecté, pas de confirmation du lancer.
**Alternatives écartées :** coupure rapide des moteurs si aucun lancer n'est détecté (recommandée par l'architecte) ; confirmation du lancer avant démarrage.
**Raison :** choix de l'utilisateur, après avertissement de l'architecte. Risque accepté : hélices en rotation si le bouton est relâché en main ou drone posé ; limité seulement par les protège-hélices de DEC-016 « Public adulte, protège-hélices obligatoires ». À réexaminer si les essais montrent des démarrages involontaires. Pas de scénario dédié (décision du 2026-10-27) : le cas est couvert par le vol normal, puis par SCN-002 « Échec : stationnaire non atteint dans le délai » si le drone n'est pas lancé. Depuis : cette couverture par SCN-002 « Échec : stationnaire non atteint dans le délai » est assurée par la condition « en l'air » de DEC-049 « Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale » ; la présente décision reste valable avec cette condition.
**Doutes levés :** DOU-016 « Comment limiter le risque d'hélices en rotation sans lancer ? »

### DEC-018 — Jamais de réarmement automatique ; batterie mesurée à vide à l'armement
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-011 « Dégradé : coupure d'alimentation en vol »
**Décision :** (1) Après tout redémarrage du drone (coupure ou chute d'alimentation), le drone reste verrouillé : il exige un nouvel appui sur le bouton, drone au sol et immobile. Jamais de réarmement automatique. (2) La batterie est mesurée **à vide** à l'armement, avec un seuil à marge large qui couvre la chute de tension en charge ; pas de test moteur à l'armement.
**Alternatives écartées :** réarmement automatique si vol détecté (complexe et risqué) ; mesure sous charge avec rotation brève des hélices (en tension avec DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » et DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer ») ; mesure sous charge simulée (matériel ajouté).
**Raison :** choix de l'utilisateur, simplicité. Risque accepté : un vol possible peut être refusé, et le seuil peut rester trop optimiste ; à valider par essais.
**Doutes levés :** DOU-017 « Que se passe-t-il si l'alimentation est coupée ou chute en vol ? » — DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? » reste ouvert (valeur du seuil).

### DEC-019 — Hauteur au-dessus du sol mesurée en vol
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone embarque un capteur de distance de type ToF orienté vers le bas. Il fournit la hauteur au-dessus du sol et la vitesse verticale pour le stationnaire de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs ». Complète DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais » : la centrale inertielle reste le seul capteur de mouvement horizontal.
**Alternatives écartées :** baromètre (recommandé par l'architecte : moins précis, mais pas de limite de portée ni d'orientation) ; baromètre et ToF ensemble ; aucun capteur d'altitude.
**Raison :** choix de l'utilisateur ; meilleure précision de hauteur (de l'ordre du centimètre). Risques acceptés : portée limitée, mesure fausse tant que le drone n'est pas redressé après un lancer dans toute orientation, sensibilité à la lumière et aux sols non réfléchissants. Depuis : DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée » — la solution (capteur de distance de type ToF orienté vers le bas) n'est plus qu'une proposition pour l'architecture (`notes-architecture.md`), et les risques ci-dessus sont ceux de cette proposition ; seule l'intention reste décidée : la hauteur au-dessus du sol est mesurée en vol.
**Doutes levés :** DOU-019 « Quel capteur donne l'altitude et la vitesse verticale ? » — ses limites techniques sont reprises en architecture (`notes-architecture.md`) ; la question côté utilisateur est dans DOU-021 « Que se passe-t-il pour un lancer hors plage ? »

### DEC-020 — Atterrissage sur place
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Après les 10 secondes de stationnaire, le drone descend et se pose à l'endroit où il se trouve, sans revenir vers le point de lancer.
**Alternatives écartées :** retour vers le point de lancer (demande de connaître la position, non retenue avec DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais »).
**Raison :** choix de l'utilisateur ; simplicité.
**Doutes levés :** DOU-007 « Quelles contraintes d'atterrissage ? » (avec DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »)

### DEC-021 — Atterrissage lent, 15 secondes maximum, puis coupure des moteurs
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** À l'atterrissage, la vitesse au contact du sol est de 0,5 m/s au plus (valeur à confirmer par essais). La descente dure 15 secondes au plus ; passé ce délai, le drone coupe ses moteurs.
**Alternatives écartées :** 1 m/s (recommandé par l'architecte) ou 2 m/s au contact ; durée de 5 secondes (recommandée) ou de 3 secondes.
**Raison :** choix de l'utilisateur ; contact très doux. Conséquence : le vol complet dure jusqu'à environ 27 secondes (2 s de stabilisation, 10 s de stationnaire, 15 s de descente), au lieu des 15 secondes supposées par DEC-013 « Pas de contrôle de la batterie en vol » ; le seuil de batterie de DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? » doit couvrir cette durée.
**Doutes levés :** DOU-007 « Quelles contraintes d'atterrissage ? »

### DEC-022 — Moteurs coupés à moins de 2 à 3 cm du sol
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Pendant la descente, dès que le drone mesure qu'il est à moins de 2 à 3 cm du sol (valeur provisoire, à confirmer par essais), il coupe ses moteurs et se déclare posé. Pas de détection de choc ni de réessai après un rebond : la coupure intervient au premier passage sous le seuil. Complète DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs ».
**Alternatives écartées :** détection du posé par l'arrêt de la descente ou le choc.
**Raison :** choix de l'utilisateur ; le drone dispose d'une mesure de hauteur (DEC-019 « Hauteur au-dessus du sol mesurée en vol »). Risque accepté : sur sol très incliné ou irrégulier, la coupure à 2 à 3 cm laisse le drone retomber de cette hauteur.
**Doutes levés :** DOU-018 « Quel est le comportement à l'atterrissage et après le posé ? » (avec DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler »)

### DEC-023 — Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé », SCN-002 « Échec : stationnaire non atteint dans le délai », SCN-006 « Échec : inclinaison excessive après le stationnaire » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Après le posé, ou après toute coupure des moteurs (échec, basculement, arrêt par le bouton, fin du délai de descente), le drone est verrouillé. Pour revoler, l'utilisateur appuie de nouveau 2 secondes sur le bouton, sans débrancher la batterie. Jamais de réarmement automatique, conformément à DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement ».
**Alternatives écartées :** débrancher et rebrancher la batterie ; verrouillage temporisé avant un nouvel appui.
**Raison :** choix de l'utilisateur, sur recommandation de l'architecte ; enchaînement simple des vols.
**Doutes levés :** DOU-018 « Quel est le comportement à l'atterrissage et après le posé ? »

### DEC-024 — Mise en service par programmation avec un programmateur ST-LINK
**Date :** 2026-10-27
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Décision :** La mise en service commence par la programmation du ou des microcontrôleurs du drone avec un programmateur ST-LINK, via JTAG ou SWD. **Contrainte pour l'architecture :** l'utilisateur ne possède que ce programmateur, donc tout microcontrôleur du drone doit pouvoir être programmé avec lui (famille STM32 ou équivalent accessible en JTAG ou SWD).
**Alternatives écartées :** aucune étudiée.
**Raison :** outil disponible chez l'utilisateur ; contrainte exprimée par lui. Depuis : DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée » — la solution (programmateur ST-LINK, JTAG ou SWD) n'est plus qu'une proposition pour l'architecture (`notes-architecture.md`), et non une contrainte imposée ; seule l'intention reste décidée : la mise en service commence par la programmation du drone.
**Doutes levés :** DOU-014 « Quel scénario de mise en service faut-il écrire ? » — mais ouvre DOU-031 « Quelles opérations suivent la programmation à la mise en service ? »

### DEC-025 — Suivi et réglage du drone par le sans fil, y compris en vol
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Le drone est paramétrable sans fil, y compris en vol, pour régler le vol. Il retourne à un appareil de suivi les variables du vol : commandes des moteurs, hauteur, autres données de position. Un mode réglage, accessible par trois appuis sur le bouton (confirmé par DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie »), permet au drone de décoller et de se poser plusieurs fois de suite sur un temps bref pour régler les paramètres.
**Alternatives écartées :** aucune étudiée.
**Raison :** l'asservissement du vol doit être réglé par essais ; l'utilisateur veut voir les variables et agir sur les paramètres pendant les vols.
**Doutes levés :** DOU-008 « L'utilisateur veut-il suivre le vol depuis un autre appareil ? » et DOU-026 « L'utilisateur veut-il régler le drone depuis un autre appareil ? » — mais ouvre DOU-032 « Comment entre-t-on dans le mode réglage et comment en sort-on ? », DOU-033 « Que fait le drone pendant les vols de réglage répétés ? » et DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? »

### DEC-026 — Mise en service : calibrage éventuel renvoyé à l'architecture, réglage du vol par un scénario dédié
**Date :** 2026-10-27
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Décision :** On ne sait pas encore si un calibrage est nécessaire : cela dépend des solutions techniques, donc de l'architecture. Aucune opération de calibrage n'est écrite dans les scénarios. Le réglage du vol fait l'objet du scénario SCN-009 « Réglage et suivi du drone par le sans fil ».
**Alternatives écartées :** décrire un calibrage dès les scénarios (recommandé par l'architecte, écarté : dépend de solutions non choisies).
**Raison :** choix de l'utilisateur ; les scénarios ne décrivent pas de solutions techniques.
**Doutes levés :** DOU-031 « Quelles opérations suivent la programmation à la mise en service ? »

### DEC-027 — Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Le mode réglage s'active par trois appuis sur le bouton, drone posé et non armé ; le drone signale l'entrée dans le mode. On n'en sort que par coupure de la batterie : après un redémarrage, le drone est en mode normal. Précise DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol ».
**Alternatives écartées :** commande sans fil seulement ; trois appuis ou commande sans fil ; sortie par appui sur le bouton, commande sans fil ou fin d'un délai.
**Raison :** choix de l'utilisateur ; simplicité. Risque accepté : on peut oublier d'être en mode réglage, et un appui parasite peut l'activer au sol.
**Doutes levés :** DOU-032 « Comment entre-t-on dans le mode réglage et comment en sort-on ? »

### DEC-028 — Mode réglage : décollage depuis le sol sur commande sans fil
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** En mode réglage, le drone décolle depuis le sol, à chaque fois sur commande de l'utilisateur envoyée par le sans fil. Il ne décolle jamais seul, et aucun nombre de cycles n'est imposé. Exception au lancer à la main de DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs », limitée au mode réglage de DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie ».
**Alternatives écartées :** décollage automatique en boucle sur un nombre de cycles fixé (écarté : hélices qui tournent sans geste de l'utilisateur).
**Raison :** choix de l'utilisateur, sur recommandation de l'architecte ; l'utilisateur garde la main sur chaque décollage.
**Doutes levés :** aucun en entier : DOU-033 « Que fait le drone pendant les vols de réglage répétés ? » reste ouvert (durée et hauteur du vol, lien perdu, bouton en vol de réglage). Depuis : levé par DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu ».

### DEC-029 — Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** À chaque commande sans fil (DEC-028 « Mode réglage : décollage depuis le sol sur commande sans fil »), le vol de réglage est court : stabilisation, stationnaire de 3 secondes, puis atterrissage ; le drone coupe ses moteurs 15 secondes au plus après le décollage (stationnaire de 3 secondes fixe, non réglable ; précisé le 2026-10-27 avec l'utilisateur). Si le lien sans fil est perdu en vol de réglage, le drone atterrit doucement sur place. Le bouton appuyé en vol de réglage reste un arrêt d'urgence (DEC-015 « Bouton appuyé en vol : arrêt d'urgence »).
**Alternatives écartées :** stationnaire jusqu'à la commande de pose (recommandé par l'architecte) ; coupure des moteurs ou poursuite du vol si le lien est perdu ; bouton ignoré en mode réglage.
**Raison :** choix de l'utilisateur ; vol court et borné. Conséquence : peu de temps pour régler un paramètre pendant un seul vol de 3 secondes ; il faut enchaîner les vols.
**Doutes levés :** DOU-033 « Que fait le drone pendant les vols de réglage répétés ? » — mais ouvre DOU-035 « Quelle hauteur de stationnaire vise-t-on ? » et DOU-036 « Après quel délai le lien sans fil est-il considéré comme perdu ? »

### DEC-030 — Drone posé immobile à la mise sous tension ; refus de s'armer si l'initialisation échoue
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé », SCN-010 « Échec : initialisation impossible au démarrage » et SCN-011 « Dégradé : coupure d'alimentation en vol »
**Décision :** L'utilisateur pose le drone immobile avant de brancher la batterie et n'y touche pas pendant quelques secondes (durée à fixer en exigences). Si le drone n'est pas en état de voler au démarrage (par exemple déplacé pendant son démarrage), il ne se déclare pas « allumé, en attente d'un appui », refuse de s'armer, ignore le bouton et donne un signal d'échec d'initialisation distinct. On en sort en débranchant puis en rebranchant la batterie.
**Alternatives écartées :** nouvelle tentative automatique ; aucun contrôle ; aucune consigne d'immobilité.
**Raison :** choix de l'utilisateur, sur recommandation de l'architecte ; évite d'annoncer « prêt » alors que le drone ne peut pas voler. Le calibrage éventuel reste renvoyé à l'architecture (DEC-026 « Mise en service : calibrage éventuel renvoyé à l'architecture, réglage du vol par un scénario dédié »).
**Doutes levés :** DOU-015 « Que se passe-t-il si l'initialisation échoue ? »

### DEC-031 — Arrêt du drone lancé : bouton et commande d'arrêt sans fil
**Date :** 2026-10-27
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Une fois le drone lancé, deux moyens d'arrêt coexistent : le bouton (DEC-015 « Bouton appuyé en vol : arrêt d'urgence ») et une commande d'arrêt sans fil envoyée depuis l'appareil de suivi. La commande sans fil vaut en vol normal comme en vol de réglage. Elle coupe les moteurs et se signale par un signal distinct (DEC-005 « Un signal distinct pour chaque information »). Complète DEC-015 « Bouton appuyé en vol : arrêt d'urgence » et DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol ».
**Alternatives écartées :** A, statu quo : bouton seul (impose de saisir le drone en vol) ; C, atterrissage d'urgence sans fil à la place de la coupure (les hélices tournent encore jusqu'à 15 s) ; D, coupure et atterrissage d'urgence au choix (deux commandes, plus de complexité pour un vol de 27 s).
**Raison :** choix de l'utilisateur (option B, recommandée par l'architecte) ; permet d'arrêter le drone sans toucher les hélices. Le drone tombe, comme avec le bouton. Risque résiduel accepté : si l'appareil de suivi est absent ou le lien perdu, seul le bouton reste. Les protège-hélices restent obligatoires (DEC-016 « Public adulte, protège-hélices obligatoires »). Décision relayée à l'architecte à partir de la réponse de l'utilisateur en chat : à confirmer par l'utilisateur à la porte « scénarios ». **Confirmé par l'utilisateur le 2026-10-27**, après nouvelle présentation des options A, C et D : « B. Bouton + coupure sans fil ».
**Doutes levés :** DOU-024 « Comment arrêter un drone en vol sans le saisir ? » — impact sur DOU-025 « Le drone vole-t-il sans appareil de suivi ? », DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? » et DOU-047 « Appareil de suivi : appairage, absence, plusieurs drones » (non levés). Depuis : DOU-025 « Le drone vole-t-il sans appareil de suivi ? » est levé par DEC-032 « Vol libre : le drone vole sans appareil de suivi », DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? » par DEC-038 « Mode réglage : décollage sans protection supplémentaire » et DOU-047 « Appareil de suivi : appairage, absence, plusieurs drones » par DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée ».

### DEC-032 — Vol libre : le drone vole sans appareil de suivi
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** En vol normal, le drone arme et vole sans appareil de suivi. Un appareil de suivi relié est un plus (suivi, réglage, arrêt sans fil : DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol », DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil »), pas une condition de vol. Perdre le lien en vol normal ne change rien au comportement du drone. Le vol de réglage garde son atterrissage sur place en cas de lien perdu (DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu »).
**Alternatives écartées :** B, appareil obligatoire en vol normal avec atterrissage sur place si le lien est perdu (contredit le drone de poche lancé à la main, dépend d'un appareil chargé et à portée) ; C, vol libre mais atterrissage sur place si un appareil relié à l'armement disparaît en vol (deux comportements à spécifier et tester).
**Raison :** choix de l'utilisateur (option A, recommandée par l'architecte) ; simplicité, cohérent avec le lancer à la main. Risque résiduel accepté : sans appareil de suivi, seul le bouton arrête le drone (DEC-015 « Bouton appuyé en vol : arrêt d'urgence »), sans arrêt sans fil. Décision relayée à l'architecte à partir de la réponse de l'utilisateur en chat.
**Doutes levés :** DOU-025 « Le drone vole-t-il sans appareil de suivi ? » — impact sur DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? » et DOU-047 « Appareil de suivi : appairage, absence, plusieurs drones » (non levés). Depuis : DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? » est levé par DEC-038 « Mode réglage : décollage sans protection supplémentaire » et DOU-047 « Appareil de suivi : appairage, absence, plusieurs drones » par DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée ».

### DEC-033 — Signal Arrêt sans fil distinct du signal Arrêt par le bouton
**Date :** 2026-10-27
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Le 16e signal « Arrêt sans fil » est validé et reste distinct du signal n° 14 « Arrêt par le bouton ». Précise DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » et applique DEC-005 « Un signal distinct pour chaque information ».
**Alternatives écartées :** même signal que « Arrêt par le bouton » (l'utilisateur ne saurait pas quel moyen a coupé les moteurs).
**Raison :** choix de l'utilisateur, relayé à l'architecte à partir de sa réponse en chat ; cohérent avec DEC-005 « Un signal distinct pour chaque information ». La forme du signal (lumière, son, suivi) reste à définir (DOU-027 « Un signal distinct par information, ou par catégorie ? »).
**Doutes levés :** DOU-055 « Le signal Arrêt sans fil (16e signal) est-il validé ? »

### DEC-034 — Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Les réglages sont envoyés au drone par le sans fil. Une commande spécifique demande au drone de les sauvegarder. Au démarrage, quand la batterie est branchée, le drone charge ses dernières valeurs enregistrées depuis sa mémoire non volatile. Aucune configuration n'est poussée par l'appareil de suivi au démarrage : le drone vole sans aucun échange sans fil au départ. Précise DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol » et complète DEC-032 « Vol libre : le drone vole sans appareil de suivi ».
**Conséquence (confirmée par l'utilisateur) :** une valeur envoyée mais non sauvegardée ne survit pas à la coupure de la batterie ; au redémarrage, le drone charge les dernières valeurs enregistrées.
**Alternatives écartées :** non étudiées avec l'utilisateur (par exemple sauvegarde automatique à chaque modification).
**Raison :** choix de l'utilisateur, relayé à l'architecte à partir de sa réponse en chat ; permet d'essayer une valeur sans l'enregistrer.
**Doutes levés :** partiellement DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? » (partie conservation). Reste ouvert et bloquant : le retour à des réglages sûrs. Depuis : DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? » est levé par DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » et DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ».

### DEC-035 — Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** (1) Il n'y a pas de commande de retour aux valeurs d'origine. Le seul recours contre un mauvais réglage sauvegardé est la reprogrammation du drone (SCN-008 « Mise en service : programmation du drone »). (2) Le cas d'une mémoire de réglages corrompue n'est pas traité : le drone ne détecte pas la corruption (pas de contrôle d'intégrité de type somme de contrôle). Complète DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage ».
**Alternatives écartées :** commande sans fil de retour aux valeurs d'origine, retour automatique après un vol raté, geste sur le bouton au démarrage ; détection de la corruption avec valeurs d'origine ou refus de s'armer.
**Raison :** choix de l'utilisateur, relayé à l'architecte à partir de sa réponse en chat : la personne qui règle le drone est expérimentée et assume ses réglages. Risques acceptés : un mauvais réglage sauvegardé impose la reprogrammation ; une mémoire corrompue peut donner un drone instable ou imprévisible, sans signal. Le comportement du drone neuf (mémoire jamais écrite) n'est pas décidé : voir DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? ». Depuis : il est décidé par DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ».
**Doutes levés :** partiellement DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? » (retour aux valeurs d'origine et mémoire corrompue). Reste ouvert : le comportement à la première mise sous tension. Depuis : DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? » est levé par DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ».

### DEC-036 — Drone neuf : valeurs d'origine fixes du logiciel, sans signal
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** À la première mise sous tension d'un drone neuf (mémoire de réglages jamais écrite), le drone utilise des valeurs d'origine fixes du logiciel, sans signal particulier. Complète DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage » et DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée ».
**Alternatives écartées :** refus de s'armer ou signal de mémoire vide (non retenus).
**Raison :** choix de l'utilisateur (option a, recommandée par l'architecte), relayé à l'architecte à partir de sa réponse en chat ; simple, cohérent avec un régleur expérimenté qui assume son test. Reste à fixer : les valeurs d'origine et leurs bornes (DOU-038 « Réglages en vol : valeurs d'origine, bornes, coupures en vol de réglage ? »). Depuis : DOU-038 « Réglages en vol : valeurs d'origine, bornes, coupures en vol de réglage ? » est levé par DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » ; les valeurs d'origine et les bornes numériques restent à fixer dans DOU-058 « Valeurs d'origine et bornes numériques à fixer en architecture ». Depuis : DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » impose des bornes aux seuils de sécurité ; leurs valeurs restent à fixer dans DOU-058 « Valeurs d'origine et bornes numériques à fixer en architecture ».
**Doutes levés :** DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? »

### DEC-037 — Pas d'appairage : le drone obéit à tout appareil de suivi à portée
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Il n'y a pas d'appairage : le drone obéit à tout appareil de suivi à portée. L'absence de l'appareil n'empêche pas le vol (DEC-032 « Vol libre : le drone vole sans appareil de suivi »). Précise DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol » et DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ».
**Alternatives écartées :** A, appairage persistant enregistré dans le drone ; B, appairage à chaque mise sous tension.
**Raison :** choix de l'utilisateur (option C), relayé à l'architecte à partir de sa réponse en chat ; simplicité. **Risques acceptés :** un tiers ou l'appareil d'un autre drone peut envoyer un arrêt, un décollage de réglage ou une sauvegarde de réglages ; une commande peut atteindre plusieurs drones à portée ; le suivi peut être mélangé si plusieurs drones sont à portée. Le risque d'une commande « Décoller » parasite n'est plus couvert par l'appairage : il renforce DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? ». Depuis : DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? » est levé par DEC-038 « Mode réglage : décollage sans protection supplémentaire ».
**Doutes levés :** DOU-047 « Appareil de suivi : appairage, absence, plusieurs drones »

### DEC-038 — Mode réglage : décollage sans protection supplémentaire
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** En mode réglage, la commande sans fil de décollage (DEC-028 « Mode réglage : décollage depuis le sol sur commande sans fil ») n'a aucune protection supplémentaire : ni vérification que le drone est posé, immobile et à plat, ni confirmation en deux temps. Il n'y a donc pas de 17e signal « Décollage refusé ». La commande d'arrêt d'urgence sans fil est couverte par DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ».
**Alternatives écartées :** B, vérification d'état (posé, immobile, à plat) ; C, B plus confirmation en deux temps ; D, condition de bouton.
**Raison :** interprétation de la réponse de l'utilisateur en chat, relayée à l'architecte : « pour le moment il n'y a qu'un drone, il n'y a pas lieu de faire quelque chose de compliqué, lourd ». L'utilisateur n'a pas écrit explicitement « option A » : à confirmer à la porte « scénarios ». **Confirmé par l'utilisateur le 2026-10-27**, après nouvelle présentation des options B, C et D et des cas « drone tenu en main » et « drone retourné » : « A. Aucune protection, le regleur est experimenté ». Risque accepté : une commande « Décoller » parasite est possible (drone tenu en main, tiers à portée), sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »). À réexaminer si un second drone ou des décollages involontaires apparaissent, comme DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer ».
**Doutes levés :** DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? »
**Complétée par :** DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre » le 2026-10-28 : la batterie est vérifiée au décollage de réglage, les autres protections restent exclues.

### DEC-039 — Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** (Q1) Les coupures de DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai » et de DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » valent aussi en vol de réglage. (Q2) Aucune borne sur les valeurs de réglage : le régleur assume tout, comme dans DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée ». (Q3) Les paramètres sont modifiables aussi en vol normal, sans entrer dans le mode réglage. Les valeurs d'origine (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ») et d'éventuelles bornes numériques sont renvoyées à l'architecture.
**Alternatives écartées :** Q1 : coupures désactivées (B) ou seuils élargis (C) ; Q2 : refus des valeurs hors plage fixée dans le logiciel ; Q3 : réglage limité au mode réglage.
**Raison :** choix de l'utilisateur, relayé à l'architecte à partir de ses réponses en chat. **Point à noter, Q3(b) :** elle élargit la portée de DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie ». Le mode réglage reste nécessaire pour le décollage commandé par le sans fil (DEC-028 « Mode réglage : décollage depuis le sol sur commande sans fil »), mais plus pour modifier des valeurs. **Conséquence sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée ») :** un tiers à portée peut modifier ou sauvegarder des paramètres, y compris en vol normal. Risque accepté tel quel (sans borne, un réglage absurde est possible).
**Nuance :** les coupures de la question Q1 ne valent que tant que leurs seuils ne sont pas modifiés : voir DEC-045 « Seuils de sécurité réglables comme le reste, sans borne ». Depuis : DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » remplace DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » — les seuils de sécurité sont bornés ; une valeur ne peut plus désactiver une coupure. « Aucune borne » (Q2) ne vaut plus pour les seuils de sécurité ; il reste valable pour les autres réglages.
**Doutes levés :** DOU-038 « Réglages en vol : valeurs d'origine, bornes, coupures en vol de réglage ? »

### DEC-040 — Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le périmètre d'emploi visé est l'appartement. Le drone sera aussi testé dans un gymnase et dans le jardin si les solutions techniques le permettent : ces essais sont complémentaires, sans objectif garanti, conditionnés aux solutions techniques (capteur de hauteur de DEC-019 « Hauteur au-dessus du sol mesurée en vol », dérive de DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais », vent).
**Alternatives écartées :** A, intérieur seulement en grand volume ; B, intérieur et jardin comme périmètre garanti (non retenus comme tels).
**Raison :** réponse de l'utilisateur en chat (« on vise un appartement, mais il sera aussi testé dans un gymnase et dans le jardin si les solutions techniques le permettent »), relayée à l'architecte ; lecture de l'architecte, plus proche de l'option C que de A. **Tension non résolue :** un appartement est incompatible avec un lancer à 4 m/s (jusqu'à 8 m en 2 s) de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol ». La zone libre minimale, la distance aux personnes et le traitement d'un lancer trop rapide pour la zone ne sont pas tranchés : voir DOU-040 « Quel périmètre d'emploi et quelle zone libre minimale ? ».
**Doutes levés :** aucun en entier : DOU-040 « Quel périmètre d'emploi et quelle zone libre minimale ? » reste ouvert pour la zone libre. Depuis : DOU-040 « Quel périmètre d'emploi et quelle zone libre minimale ? » est levé par DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu ».

### DEC-041 — Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Un lancer plus rapide que ce que la zone ou la plage de lancer permet est hors plage : le drone ne le garantit pas et ne l'empêche pas. Si le drone touche un mur dans ce cas, c'est de la responsabilité de l'utilisateur. Complète DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires » et reste cohérent avec DEC-014 « Pas de coupure sur choc en vol » et DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer ».
**Alternatives écartées :** non étudiées avec l'utilisateur (par exemple limiter la vitesse de lancer par détection).
**Raison :** réponse de l'utilisateur en chat (« si quelqu'un lance le drone trop vite et qu'il tape un mur, c'est de la faute de l'utilisateur »), relayée à l'architecte. Risque accepté. **Ne tranche pas** la valeur de la plage de lancer : DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » reste inchangée à ce jour. La zone libre, la distance aux personnes et la restriction éventuelle de la plage en appartement restent à décider : DOU-040 « Quel périmètre d'emploi et quelle zone libre minimale ? ».
**Doutes levés :** aucun en entier : DOU-040 « Quel périmètre d'emploi et quelle zone libre minimale ? » reste ouvert. Depuis : DOU-040 « Quel périmètre d'emploi et quelle zone libre minimale ? » est levé par DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu ».

### DEC-042 — Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** (1) Le périmètre visé reste celui de DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires ». (2) La plage de lancer de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » est inchangée : aucune restriction propre à l'appartement. (3) Le drone ne sait pas s'il est lancé dans un appartement ou dans un gymnase et ne s'adapte pas au lieu. (4) Aucune zone libre minimale ni distance aux personnes n'est définie dans le produit. (5) L'utilisation dans un lieu trop petit pour la plage relève de la responsabilité de l'utilisateur (DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur »).
**Alternatives écartées :** restriction de la plage de lancer en appartement (par exemple 0,5 à 2 m/s) ; zone libre minimale et distance aux personnes ; ouverture d'un doute dédié à la zone libre.
**Raison :** réponse de l'utilisateur en chat (« le drone ne sait pas s'il est lancé dans un appartement ou dans un gymnase ; tu gardes les paramètres de lancer déjà discutés ; je ne veux pas qu'on parle de zone libre »), relayée à l'architecte. **Conséquence acceptée, écrite honnêtement :** un appartement est incompatible avec un lancer à 4 m/s (jusqu'à 8 m en 2 s) ; un lancer vigoureux dans une pièce peut donc finir contre un mur ou une personne, sans coupure sur choc (DEC-014 « Pas de coupure sur choc en vol »). Risque accepté par l'utilisateur ; à réexaminer si les essais montrent des chocs fréquents.
**Doutes levés :** DOU-040 « Quel périmètre d'emploi et quelle zone libre minimale ? »

### DEC-043 — Commandes sans fil acceptées selon l'état du drone
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Chaque commande sans fil est acceptée, ignorée ou coupe les moteurs selon l'état du drone, d'après la table suivante (une commande ignorée n'a aucun effet). Précise DEC-028 « Mode réglage : décollage depuis le sol sur commande sans fil », DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil », DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage » et DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ».

| État du drone | Décoller | Arrêt | Modifier | Sauvegarder |
|---|---|---|---|---|
| Allumé, en attente d'un appui (au sol, mode normal) | Ignorée | Ignorée | Acceptée | Acceptée |
| Armé, avant le lancer | Ignorée | Ignorée | Acceptée | Acceptée |
| En vol (vol normal) | Ignorée | Coupe les moteurs | Acceptée | Ignorée |
| Mode réglage, posé | Acceptée | Ignorée | Acceptée | Acceptée |
| Vol de réglage | Ignorée | Coupe les moteurs | Acceptée | Ignorée |
| Posé ou moteurs coupés, verrouillé | Ignorée | Ignorée | Acceptée | Acceptée |

**Alternatives écartées :** B, tout accepter partout sauf Décoller, limité au mode réglage posé (écriture mémoire possible en vol, Arrêt accepté hors vol) ; C, Modifier et Sauvegarder limités au mode réglage au sol (contredit DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal »).
**Raison :** choix de l'utilisateur (option A, recommandée par l'architecte), relayé à l'architecte à partir de sa réponse en chat, sans modification de case. Les cases proposées par l'architecte sans décision antérieure (Arrêt ignoré à l'état Armé ; Sauvegarder acceptée à l'état Armé ; Sauvegarder ignorée en vol normal et en vol de réglage) sont validées par cette réponse. Sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »), tout appareil à portée peut envoyer ces commandes : risque accepté.
**Doutes levés :** partiellement DOU-056 « Commande sans fil et état du drone : que fait chaque commande dans chaque état ? » (table des commandes). Reste ouvert : l'état du drone après un vol ou un arrêt de réglage. Depuis : cet état est fixé par DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage », qui lève DOU-056 « Commande sans fil et état du drone : que fait chaque commande dans chaque état ? » (cas de l'arrêt ou de l'échec en vol de réglage à confirmer : DOU-065 « Quelles décisions relayées ou interprétées sont à confirmer explicitement à la porte ? »).

### DEC-044 — Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** En mode réglage, le bouton n'arme pas et n'a pas d'autre rôle de lancement : le seul moyen de décoller est la commande sans fil « Décoller » (DEC-028 « Mode réglage : décollage depuis le sol sur commande sans fil »), et la seule sortie est la coupure de la batterie (DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie »). Après un vol de réglage terminé, le drone reste en mode réglage, posé, prêt à une nouvelle commande « Décoller ». Le verrouillage de DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler » ne s'applique pas en mode réglage. Précise DEC-043 « Commandes sans fil acceptées selon l'état du drone ».
**Confirmé par l'utilisateur le 2026-10-27** (lecture de l'architecte à l'origine ; réponse en chat après présentation des options B « verrouillé jusqu'à la coupure de la batterie » et D « verrouillé jusqu'à un appui de 2 s » : « il faut garder Prêt à redécoller tout de suite via une commande sans fils ») : après un arrêt d'urgence (bouton ou sans fil), un échec de stabilisation ou un basculement en vol de réglage, le drone reste en mode réglage, posé, sans verrouillage. Conséquence : un arrêt d'urgence, même envoyé par un tiers sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »), n'empêche pas un nouveau « Décoller ». Risque accepté, lié à DEC-038 « Mode réglage : décollage sans protection supplémentaire ».
**Alternatives écartées :** A, verrouillé après tout vol de réglage (rend le cycle de réglage impraticable) ; B, verrouillé après un arrêt ou un échec ; D, déverrouillage par un appui de 2 s.
**Raison :** interprétation de la réponse de l'utilisateur en chat, relayée à l'architecte : « pour sortir du mode réglage, il faut déconnecter la batterie. Donc une fois en réglage, on ne peut que faire des décollages via commande sans fil pour régler. » Cohérent avec DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement » : aucun réarmement automatique, chaque décollage de réglage est commandé.
**Doutes levés :** DOU-056 « Commande sans fil et état du drone : que fait chaque commande dans chaque état ? »

### DEC-045 — Seuils de sécurité réglables comme le reste, sans borne
**Date :** 2026-10-27
**Remplacée par :** DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » le 2026-10-27, après revue par l'utilisateur à la porte « scénarios ». Cette décision n'est plus en vigueur ; elle est conservée pour l'historique.
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Les seuils de sécurité sont des paramètres réglables comme les autres, sans borne : le délai de 2 s (DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs »), l'angle limite (DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »), le délai de 15 s (DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs ») et le seuil de batterie (DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement »). Précise DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ».
**Alternatives écartées :** A, seuils figés dans le logiciel, hors des paramètres réglables ; C, seuils réglables mais bornés.
**Raison :** choix de l'utilisateur (option B), relayé à l'architecte à partir de sa réponse en chat ; cohérent avec DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » et DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » : le régleur expérimenté assume tout. **Conséquence acceptée, écrite honnêtement :** la promesse de coupure de DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » (Q1) ne vaut que tant que les seuils ne sont pas modifiés. Une valeur de réglage peut désactiver une coupure (par exemple un délai très long ou un angle limite de 180°). Sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »), un tiers à portée peut le faire, y compris en vol normal (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal », Q3), et le sauvegarder là où DEC-043 « Commandes sans fil acceptées selon l'état du drone » l'autorise (états au sol : allumé en attente, armé, mode réglage posé, posé ou coupé).
**Doutes levés :** DOU-057 « Les seuils de sécurité sont-ils des paramètres réglables sans borne ? »

### DEC-046 — Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Si les 15 secondes de descente s'écoulent sans que le drone soit passé à moins de 2 à 3 cm du sol, il coupe ses moteurs, donne un signal distinct « Délai de descente dépassé » (17e signal) et est verrouillé selon DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler ». Il ne donne pas le signal « Posé ». Précise DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs » et DEC-022 « Moteurs coupés à moins de 2 à 3 cm du sol ».
**Alternatives écartées :** A, même signal « Posé » (trompeur) ; C, réutiliser un signal d'échec existant (information fausse) ; D, cas déclaré impossible, sans traitement.
**Raison :** choix de l'utilisateur (option B, recommandée par l'architecte), relayé à l'architecte à partir de sa réponse en chat ; cohérent avec DEC-005 « Un signal distinct pour chaque information ». Le nombre de signaux passe à dix-sept ; leur regroupement éventuel reste en question dans DOU-027 « Un signal distinct par information, ou par catégorie ? ».
**Doutes levés :** DOU-043 « Quel signal et quel état pour un délai de descente dépassé ? »

### DEC-047 — L'état verrouillé est le même que l'état allumé, en attente d'un appui
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** L'état verrouillé de DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler » est le même que « Allumé, en attente d'un appui » : mêmes vérifications à l'armement (batterie mesurée à vide, DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement »), mêmes signaux, aucune réinitialisation.
**Alternatives écartées :** B, état distinct avec condition d'immobilité avant l'armement ; C, état distinct avec réinitialisation complète de DEC-030 « Drone posé immobile à la mise sous tension ; refus de s'armer si l'initialisation échoue ».
**Raison :** choix de l'utilisateur (option A, recommandée par l'architecte), relayé à l'architecte à partir de sa réponse en chat ; simplicité. **Risque accepté :** pas de vérification après une chute ou une coupure : un drone abîmé ou dont les capteurs ont dérivé peut être réarmé. Les doutes DOU-042 « Quel autotest avant réarmement après un vol raté ? » et DOU-052 « Que fait le drone qui redémarre immobile au sol après une coupure en vol ? » restent ouverts. À réexaminer si les essais montrent des réarmements douteux. Depuis : un appui sur le bouton déjà en cours au moment de la coupure des moteurs est ignoré jusqu'au relâchement, voir DEC-050 « Appui en cours lors d'une coupure des moteurs ignoré jusqu'au relâchement ».
**Doutes levés :** DOU-051 « L'état verrouillé est-il le même que l'état allumé, en attente d'un appui ? »

### DEC-048 — Renommage de SCN-009
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Le scénario porte désormais le titre « Réglage et suivi du drone par le sans fil » (ancien titre : « Réglage : réglage du vol par le sans fil »). Renommage de SCN-009 « Réglage et suivi du drone par le sans fil ».
**Alternatives écartées :** garder l'ancien titre (ne couvrait ni le suivi ni l'arrêt sans fil).
**Raison :** choix de l'utilisateur, relayé à l'architecte à partir de sa réponse en chat.
**Doutes levés :** (aucun)

### DEC-049 — Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-002 « Échec : stationnaire non atteint dans le délai »
**Décision :** Le critère de stationnaire de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » reçoit une condition supplémentaire « en l'air » : le drone n'est déclaré en vol stationnaire que si la hauteur mesurée sous lui dépasse une hauteur minimale. La valeur de cette hauteur minimale (de l'ordre de quelques centimètres) est à fixer en architecture, avec les autres valeurs numériques renvoyées à cette phase (DOU-058 « Valeurs d'origine et bornes numériques à fixer en architecture »). Les autres seuils de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » sont inchangés. Conséquence : un drone posé ou tenu immobile en main n'est jamais déclaré en stationnaire ; un drone relâché sans lancer, ou en contact avec le sol pendant la stabilisation, n'atteint pas le stationnaire et coupe ses moteurs au bout du délai de 2 s, avec le signal Échec de stabilisation (DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai », SCN-002 « Échec : stationnaire non atteint dans le délai »). DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer » reste valable avec cette condition : le cas des hélices en rotation sans lancer est bien couvert par SCN-002 « Échec : stationnaire non atteint dans le délai ».
**Alternatives écartées :** (b) garder le critère de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » tel quel et réaccepter explicitement le risque (drone posé ou tenu en main déclaré en stationnaire au bout de 0,5 s, décollage seul possible de la table ou de la main, justification de DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer » fausse).
**Raison :** décision de l'utilisateur en chat, au sujet de DOU-066 « Le critère de stationnaire peut-il être rempli au sol ou dans la main ? » : « option (a), condition « en l'air » ajoutée au critère de stationnaire. » Un drone immobile au sol ou dans la main ne peut plus remplir le critère de stationnaire, ce qui rétablit la couverture par SCN-002 « Échec : stationnaire non atteint dans le délai » et évite un redécollage seul après un contact au sol, dans l'esprit de DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement ». Cette couverture ne vaut que tant que le délai de 2 s n'est pas modifié (DEC-045 « Seuils de sécurité réglables comme le reste, sans borne »). Depuis : DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » — le délai de 2 s et la hauteur minimale restent dans leurs bornes (hauteur minimale strictement supérieure à 0) : la couverture par SCN-002 « Échec : stationnaire non atteint dans le délai » vaut pour toute valeur réglable.
**Doutes levés :** DOU-066 « Le critère de stationnaire peut-il être rempli au sol ou dans la main ? »

### DEC-050 — Appui en cours lors d'une coupure des moteurs ignoré jusqu'au relâchement
**Date :** 2026-10-27
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol », SCN-002 « Échec : stationnaire non atteint dans le délai » et SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Décision :** Un appui sur le bouton déjà en cours au moment d'une coupure des moteurs (arrêt par le bouton, basculement, échec de stabilisation, et toute autre coupure des moteurs) est ignoré jusqu'au relâchement du bouton. Pour armer le drone, il faut un nouvel appui distinct, commencé après ce relâchement. Précise DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui » et DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler ».
**Alternatives écartées :** compter l'appui en cours pour l'armement (aucun bénéfice d'usage ; risque de redémarrage des moteurs dans la main : l'appui maintenu 2 s armerait le drone, et le relâchement démarrerait les moteurs selon DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs »).
**Raison :** décision de l'utilisateur en chat, au sujet de DOU-067 « L'appui qui arrête le drone peut-il le réarmer ? » : « appui en cours ignoré jusqu'au relâchement. » Empêche qu'un utilisateur qui a saisi le drone et maintient le bouton le réarme sans le vouloir, cohérent avec DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement ».
**Doutes levés :** DOU-067 « L'appui qui arrête le drone peut-il le réarmer ? »

### DEC-051 — Seuils de sécurité réglables dans des bornes fixées par le logiciel
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil », SCN-002 « Échec : stationnaire non atteint dans le délai » et SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Décision :** Les seuils de sécurité restent réglables par le sans fil, mais seulement à l'intérieur de bornes fixées dans le logiciel : le délai de 2 s (DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs »), l'angle limite (DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »), le délai de descente de 15 s (DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »), le seuil de batterie (DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement ») et la hauteur minimale (DEC-049 « Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale »). Une valeur hors bornes est refusée. La borne de la hauteur minimale est strictement supérieure à 0 (un réglage à 0 recréerait le défaut de DOU-066 « Le critère de stationnaire peut-il être rempli au sol ou dans la main ? »). Aucune valeur dans les bornes ne doit pouvoir supprimer une coupure. Les valeurs des bornes sont à fixer en architecture (DOU-058 « Valeurs d'origine et bornes numériques à fixer en architecture ») ; la plage peut rester large. Les autres réglages (gains, etc.) restent sans borne, selon DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ». Remplace DEC-045 « Seuils de sécurité réglables comme le reste, sans borne ». Le comportement du drone à la réception d'une valeur hors bornes (refus silencieux, signal, retour vers l'appareil de suivi) n'est pas décidé : voir DOU-071 « Que fait le drone quand il reçoit une valeur de seuil hors bornes ? ».
**Alternatives écartées :** A, seuils figés, modifiables seulement par reprogrammation (perd le réglage par le sans fil prévu par DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol ») ; B, seuils réglables sans borne, ancienne décision DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » (une valeur, même envoyée par un tiers sans appairage, peut désactiver une coupure).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-27, après revue de DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » à la porte « scénarios » via DOU-065 « Quelles décisions relayées ou interprétées sont à confirmer explicitement à la porte ? » : « C. Réglables mais bornés ». Option recommandée par l'architecte, hauteur minimale incluse. Avec une sécurité très ouverte (pas d'appairage, DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée » ; décollage sans protection, DEC-038 « Mode réglage : décollage sans protection supplémentaire » ; redécollage immédiat, DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage »), les coupures automatiques sont la dernière protection : les bornes garantissent qu'elles existent toujours, quel que soit l'auteur du réglage.
**Doutes levés :** DOU-057 « Les seuils de sécurité sont-ils des paramètres réglables sans borne ? » (réponse révisée) ; partiellement DOU-065 « Quelles décisions relayées ou interprétées sont à confirmer explicitement à la porte ? » (partie DEC-045 « Seuils de sécurité réglables comme le reste, sans borne »).

### DEC-052 — Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Les scénarios sont validés avec les valeurs de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » (délai de 2 s), de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » (0,5 à 4 m/s, au moins 1,5 m du sol) et de DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » (angle limite de 60°), marquées provisoires. Elles sont à confirmer par analyse ou par essais avant la porte « exigences », y compris les limites de la plage de lancer (voir DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m »). Une phrase de SCN-001 « Vol nominal : de la batterie au posé » le dit.
**Alternatives écartées :** (b) confirmer les valeurs maintenant (bloque la porte « scénarios » sans architecture ni prototype) ; (c) tenir les valeurs pour définitives (faux : voir DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m »).
**Raison :** décision de l'utilisateur en chat, au sujet de DOU-030 « Les valeurs provisoires sont-elles à confirmer avant les exigences ? » : « option (a), valeurs provisoires pour cette porte, à confirmer avant la porte exigences, mention dans SCN-001 « Vol nominal : de la batterie au posé » [titre ajouté] ». Les valeurs ne peuvent pas être confirmées sans architecture ni prototype ; elles doivent l'être avant d'être chiffrées dans les exigences.
**Doutes levés :** DOU-030 « Les valeurs provisoires sont-elles à confirmer avant les exigences ? »

### DEC-053 — Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-008 « Mise en service : programmation du drone »
**Décision :** Le journal ne garde que l'intention de DEC-001 « Information de l'utilisateur par signaux lumineux, sonores et suivi sur un autre appareil », DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais », DEC-019 « Hauteur au-dessus du sol mesurée en vol » et DEC-024 « Mise en service par programmation avec un programmateur ST-LINK ». La solution technique qu'elles nommaient (LED RGB et buzzer ; centrale inertielle seule ; capteur de distance de type ToF ; programmateur ST-LINK) est déplacée comme proposition dans « Notes pour l'architecture » — `projets/boomrone/notes-architecture.md`, à arbitrer en architecture. Aucune de ces solutions n'est une contrainte imposée par l'utilisateur. Les quatre décisions ne sont pas réécrites : chacune porte une mention « Depuis » qui reformule l'intention. Les scénarios décrivent l'intention, sans solution.
**Alternatives écartées :** (a) garder ces solutions comme contraintes posées par l'utilisateur, à confirmer en architecture.
**Raison :** décision de l'utilisateur en chat, au sujet de DOU-054 « Les décisions de solution technique restent-elles dans le journal ? » : « option (b), aucune contrainte imposée. » Les scénarios et les besoins ne décrivent pas de solution ; l'architecture reste libre de choisir.
**Doutes levés :** DOU-054 « Les décisions de solution technique restent-elles dans le journal ? »

### DEC-054 — Chrono de 10 secondes compté depuis l'appui initial
**Date :** 2026-10-28
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Décision :** Les 10 secondes de DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes » courent depuis l'appui initial sur le bouton. Un maintien de plus de 10 s avant le lancer désarme le drone. Une fois le drone armé (après 2 s) et lancé, ce chrono ne s'applique plus : le comportement du bouton en vol relève de DEC-015 « Bouton appuyé en vol : arrêt d'urgence » et de DEC-055 « Bouton ignoré pendant une courte garde après le lancer ».
**Alternatives écartées :** chrono compté depuis l'armement (12 s au total depuis l'appui, moins intuitif).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte, « depuis l'appui initial ».
**Doutes levés :** DOU-022 « À partir de quand compte le chrono des 10 secondes, et que fait un lancer avec le bouton encore appuyé ? »

### DEC-055 — Bouton ignoré pendant une courte garde après le lancer
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Tout appui ou relâchement du bouton est ignoré pendant une courte fenêtre de garde qui suit le lancer. Passée cette garde, un appui est l'arrêt d'urgence de DEC-015 « Bouton appuyé en vol : arrêt d'urgence ». La durée de la garde (ordre de grandeur 0,5 s) est à fixer en architecture (voir « Notes pour l'architecture », point Bouton).
**Alternatives écartées :** ignorer seulement le relâchement, sans limite de durée.
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte. Un appui ou relâchement parasite dû au geste du lancer ne doit pas couper les moteurs avec un signal trompeur.
**Doutes levés :** DOU-023 « Quel appui sur le bouton juste après le lancer est ignoré ? »

### DEC-056 — Armement : drone immobile, sans autotest
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** L'armement exige que le drone soit immobile (au sol ou tenu dans la main, comme dans SCN-001 « Vol nominal : de la batterie au posé »), en plus de la batterie mesurée à vide de DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement ». Aucun autotest des hélices, des moteurs ou des capteurs n'est exigé avant l'armement. Depuis : l'armement exige aussi un drone à plat (DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone »). Cette décision précise la mention « au sol et immobile » de DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement » : la condition est « immobile », au sol ou dans la main.
**Alternatives écartées :** immobile + autotest (capteurs, moteurs, batterie), qui aurait détecté un drone abîmé après un vol raté.
**Raison :** choix de l'utilisateur en chat, le 2026-10-28 (option « immobile seulement », différente de la recommandation de l'architecte). Conséquence acceptée : un drone abîmé peut être réarmé sans vérification. Le comportement en cas de capteur ou moteur défaillant en vol reste à décider (DOU-046 « Capteur ou moteur défaillant en vol : quel comportement ? »).
**Doutes levés :** DOU-042 « Quel autotest avant réarmement après un vol raté ? »

### DEC-057 — Pas de détection dédiée d'un drone attrapé ou posé sur un obstacle
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone n'a aucune détection dédiée d'une main, d'une table ou d'une personne sous lui, ni d'un drone attrapé en vol. Seules les coupures existantes s'appliquent : inclinaison excessive de DEC-012 « Couper les moteurs si le drone bascule après le stationnaire », délai de descente de DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs », arrêt d'urgence par le bouton de DEC-015 « Bouton appuyé en vol : arrêt d'urgence ». Aucun scénario « drone récupéré à la main ou posé sur un obstacle » n'est ajouté.
**Alternatives écartées :** coupure et signal sur détection de saisie ou d'obstacle (inclinaison ou accélération anormale), avec un scénario dédié.
**Raison :** choix de l'utilisateur en chat, le 2026-10-28 (option différente de la recommandation de l'architecte). Risque résiduel accepté : des hélices en rotation peuvent blesser une main avant la coupure. Il est repris par DOU-064 « Drone tenu en main, trois appuis et commande Décoller : quel risque pour la main ? » et par DEC-016 « Public adulte, protège-hélices obligatoires ».
**Doutes levés :** DOU-041 « Que fait le drone si on l'attrape ou s'il descend sur un obstacle ? »

### DEC-058 — Trois appuis : fenêtre courte, sans signal parasite
**Date :** 2026-10-28
**Remplacée par :** DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage » le 2026-10-28, après la refonte du bouton. Cette décision n'est plus en vigueur ; elle est conservée pour l'historique. Elle écrivait qu'un appui long en mode réglage gardait son sens d'armement, ce que l'utilisateur a corrigé en chat le 2026-10-28 (contradiction avec DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage »).
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** L'entrée en mode réglage de DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie » se fait par trois appuis rapides dans une fenêtre courte, drone posé et immobile (la durée de la fenêtre est à fixer en architecture). Les deux premiers appuis n'émettent pas le signal « Appui trop court » de SCN-004 « Dégradé : appui de moins de 2 secondes sur le bouton ». Un appui long en mode réglage garde son sens normal (armement, DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes »). Le drone tenu en main n'entre pas en mode réglage (conséquence de DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie »).
**Alternatives écartées :** signaler chaque appui court (signal trompeur pour les deux premiers appuis).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte.
**Doutes levés :** DOU-044 « Séquence de trois appuis : fenêtre et signal ? »

### DEC-059 — Bouton déjà enfoncé : ignoré jusqu'au premier relâchement
**Date :** 2026-10-28
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Décision :** Un bouton enfoncé à la mise sous tension, pendant l'initialisation ou après le désarmement à 10 s de DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes » est ignoré tant qu'il n'a pas été relâché une fois. Seul un nouvel appui après ce relâchement est pris en compte. Cette décision complète DEC-054 « Chrono de 10 secondes compté depuis l'appui initial ».
**Alternatives écartées :** prendre l'appui en compte normalement (le chrono d'armement démarrerait dès le branchement, avec un risque d'armement involontaire, par exemple dans une poche ou un sac).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte.
**Doutes levés :** DOU-045 « Que fait un bouton enfoncé au branchement ou maintenu après désarmement ? »

### DEC-060 — Défaillance d'un capteur ou d'un moteur en vol : hors périmètre
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone ne détecte pas la défaillance d'un capteur ou d'un moteur en vol (mesure de hauteur perdue, hélice bloquée, protège-hélice détaché, moteur qui chauffe). Seules les coupures existantes s'appliquent : inclinaison excessive de DEC-012 « Couper les moteurs si le drone bascule après le stationnaire », délai de descente de DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs », arrêt d'urgence par le bouton de DEC-015 « Bouton appuyé en vol : arrêt d'urgence ». Aucun scénario « mesure ou moteur défaillant en vol » n'est ajouté.
**Alternatives écartées :** atterrissage lent ou coupure avec signal sur défaillance détectée, avec un scénario dédié.
**Raison :** choix de l'utilisateur en chat, le 2026-10-28 (option différente de la recommandation de l'architecte), dans la ligne de DEC-056 « Armement : drone immobile, sans autotest » et DEC-057 « Pas de détection dédiée d'un drone attrapé ou posé sur un obstacle ». Risque résiduel accepté : un drone sans mesure de hauteur valable peut monter ou descendre sans que le logiciel le sache, jusqu'à la coupure par inclinaison ou par délai.
**Doutes levés :** DOU-046 « Capteur ou moteur défaillant en vol : quel comportement ? »

### DEC-061 — Redémarrage immobile au sol : allumé mais jamais armé
**Date :** 2026-10-28
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol »
**Décision :** Si l'alimentation revient quand le drone est déjà immobile au sol, l'initialisation réussit et le drone annonce « Allumé », comme à une mise sous tension normale (DEC-030 « Drone posé immobile à la mise sous tension ; refus de s'armer si l'initialisation échoue »). Il n'est pas armé : il attend un appui, jamais de réarmement automatique (DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement »). Il n'est pas nécessaire de débrancher la batterie.
**Alternatives écartées :** exiger un débranchement de la batterie après une coupure en vol (drone verrouillé jusque-là).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte.
**Doutes levés :** DOU-052 « Que fait le drone qui redémarre immobile au sol après une coupure en vol ? »

### DEC-062 — Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Pendant la phase « Lancé », avant le démarrage des moteurs (200 ms, DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs »), l'arrêt du drone lancé de DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » n'est pas pris en compte, qu'il vienne du bouton ou du sans fil. Un arrêt demandé dans cet intervalle est perdu. Le bouton et l'arrêt sans fil ayant le même effet (coupure), la question de leur priorité relative ne se pose pas. Le sort des commandes Décoller, Modifier et Sauvegarder dans cet intervalle n'est pas tranché : voir DOU-072 « Commandes sans fil reçues pendant la phase Lancé : ignorées ou refusées ? ».
**Alternatives écartées :** arrêt toujours prioritaire, pris en compte dès « Lancé » (après la garde de DEC-055 « Bouton ignoré pendant une courte garde après le lancer »), option recommandée par l'architecte.
**Raison :** choix de l'utilisateur en chat, le 2026-10-28 (option différente de la recommandation de l'architecte). L'intervalle est court, 200 ms ; un arrêt demandé dans ce délai est perdu, mais les moteurs n'ont pas encore démarré.
**Doutes levés :** DOU-061 « Quelle priorité entre le bouton et l'arrêt sans fil, et l'arrêt est-il pris en compte pendant la phase Lancé ? »

### DEC-063 — Choc contre un obstacle ou un plafond : aucune réaction dédiée
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone ne réagit pas spécifiquement à un choc contre un obstacle ou un plafond, y compris à 4 m/s. Cela prolonge DEC-014 « Pas de coupure sur choc en vol » : seules les coupures existantes s'appliquent (inclinaison, délai de descente, arrêt d'urgence par le bouton). L'altitude maximale et le plafond restent à traiter dans DOU-029 « Quelle altitude maximale et quel plafond le drone doit-il tolérer ? ».
**Alternatives écartées :** coupure sur choc (revient sur DEC-014 « Pas de coupure sur choc en vol », demande un seuil de choc et risque des coupures intempestives au lancer).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte.
**Doutes levés :** DOU-063 « Que se passe-t-il lors d'un choc contre un obstacle ou un plafond à 4 m/s ? »

### DEC-064 — Main près des hélices en mode réglage : risque accepté et documenté
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Le risque pour la main d'un drone qui décolle en mode réglage (DEC-038 « Mode réglage : décollage sans protection supplémentaire ») est accepté, sans protection supplémentaire du logiciel. Il est atténué par les trois appuis exigeant un drone posé (DEC-058 « Trois appuis : fenêtre courte, sans signal parasite ») et par les protège-hélices (DEC-016 « Public adulte, protège-hélices obligatoires »). La consigne de sécurité est à écrire dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »).
**Alternatives écartées :** refuser la commande Décoller si le drone est porté (condition de sécurité ajoutée à DEC-038 « Mode réglage : décollage sans protection supplémentaire »).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte, dans la ligne de DEC-057 « Pas de détection dédiée d'un drone attrapé ou posé sur un obstacle ».
**Doutes levés :** DOU-064 « Drone tenu en main, trois appuis et commande Décoller : quel risque pour la main ? »

### DEC-065 — Logiciel bloqué en vol : coupure des moteurs par un chien de garde
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Si le logiciel se bloque en vol, les moteurs sont coupés par un mécanisme indépendant du logiciel (intention : chien de garde ou équivalent). Le drone redémarre ensuite comme après une coupure d'alimentation (SCN-011 « Dégradé : coupure d'alimentation en vol »). Le délai de détection est à chiffrer en exigences ; le mécanisme est à choisir en architecture.
**Alternatives écartées :** hors périmètre (le seul recours serait de débrancher la batterie, hélices tournantes).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte. Le bouton, l'arrêt sans fil et toutes les coupures dépendent du même logiciel ; une protection indépendante est la dernière.
**Doutes levés :** DOU-068 « Que se passe-t-il si le logiciel se bloque en vol ? »

### DEC-066 — Commande sans fil corrompue : aucun contrôle d'intégrité
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Le drone ne vérifie pas l'intégrité des commandes sans fil : une commande reçue est appliquée telle quelle. Une trame tronquée ou bruitée peut donc produire une valeur aberrante, appliquée puis rendue permanente par « Sauvegarder » (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »). Les seuils de sécurité restent protégés par les bornes de DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » ; les autres réglages (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ») et les valeurs aberrantes situées dans les bornes ne sont pas protégés. Ce risque technique s'ajoute au risque « commandes d'un tiers » de DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée ». La couche de liaison choisie en architecture peut fournir un contrôle d'erreur sans que ce soit une exigence.
**Alternatives écartées :** rejet de toute commande dont le contrôle d'intégrité échoue, valeur précédente conservée (option recommandée par l'architecte).
**Raison :** choix de l'utilisateur en chat, le 2026-10-28 (option différente de la recommandation de l'architecte). Risque résiduel accepté.
**Doutes levés :** DOU-069 « Une commande sans fil corrompue est-elle rejetée ? »

### DEC-067 — Démarrage à plat exigé, sinon échec de l'initialisation avec signal
**Date :** 2026-10-28
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage »
**Décision :** À la mise sous tension, le drone doit être posé à plat. Au-delà d'une inclinaison limite au démarrage, l'initialisation échoue, avec le signal d'échec d'initialisation de SCN-010 « Échec : initialisation impossible au démarrage » et le refus de s'armer de DEC-030 « Drone posé immobile à la mise sous tension ; refus de s'armer si l'initialisation échoue ». La valeur de l'inclinaison limite est à chiffrer en exigences. Aucun calibrage ni recalage sur surface inclinée n'est demandé (DEC-026 « Mise en service : calibrage éventuel renvoyé à l'architecture, réglage du vol par un scénario dédié » reste valable pour les autres besoins de calibrage).
**Alternatives écartées :** tolérer une surface inclinée en recalant l'horizontale de référence (calibrage ou référence plus élaborés).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte. Évite une horizontale de référence faussée, donc une dérive ou un critère d'inclinaison jamais rempli.
**Doutes levés :** DOU-070 « Le drone doit-il démarrer posé à plat, ou tolérer une surface inclinée ? »

### DEC-068 — Seuil hors bornes : refus silencieux, valeur relue sur l'appareil de suivi
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Quand le drone reçoit une valeur de seuil de sécurité hors bornes (DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel »), il la refuse sans signal ni message d'erreur, et conserve la valeur précédente. L'appareil de suivi relit la valeur effectivement détenue par le drone : c'est la valeur affichée qui fait foi, et c'est ainsi que l'utilisateur constate que son réglage n'a pas été pris en compte. Aucun signal lumineux ou sonore n'est ajouté pour ce cas.
**Alternatives écartées :** refus avec retour explicite vers l'appareil de suivi (option recommandée par l'architecte) ; signal lumineux ou sonore sur le drone.
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : « refus silencieux, la valeur relue par l'appareil de suivi sera la valeur conservée par le drone ». Le suivi de DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol » doit donc permettre de relire les réglages.
**Doutes levés :** DOU-071 « Que fait le drone quand il reçoit une valeur de seuil hors bornes ? »

### DEC-069 — Commandes sans fil reçues pendant la phase Lancé : ignorées
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Pendant la phase « Lancé », avant le démarrage des moteurs, les commandes sans fil Décoller, Modifier et Sauvegarder sont ignorées, comme l'arrêt de DEC-062 « Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs ». Aucune commande sans fil n'est prise en compte dans cet état. La table de DEC-043 « Commandes sans fil acceptées selon l'état du drone » est à compléter d'une ligne « Lancé, avant démarrage des moteurs : aucune commande acceptée ».
**Alternatives écartées :** commandes refusées avec retour vers l'appareil de suivi.
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte.
**Doutes levés :** DOU-072 « Commandes sans fil reçues pendant la phase Lancé : ignorées ou refusées ? »

### DEC-070 — Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court
**Date :** 2026-10-28
**Concerne :** SCN-004 « Dégradé : appui de moins de 2 secondes sur le bouton »
**Décision :** L'« appui validé » est la brique unique du bouton : le bouton maintenu 1 s. Au moment de la validation, le drone donne un signal visuel et sonore « Appui validé ». Un appui de moins de 1 s n'a aucun effet et ne donne aucun signal. Le signal 4 « Appui trop court » est supprimé. SCN-004 « Dégradé : appui de moins de 2 secondes sur le bouton » (même identifiant, ancien titre « Dégradé : bouton relâché avant 2 secondes ») est refondu : moins de 1 s, rien ; relâché entre 1 s et 2 s, un appui validé est compté et le drone n'arme ni ne lance jamais. Les valeurs de 1 s et 2 s sont provisoires (DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences »). Remplace DEC-007 « Bouton relâché avant 2 secondes : retour en attente ».
**Alternatives écartées :** conserver le signal « Appui trop court » donné à chaque relâchement avant 2 s, immédiat ou retardé après la fenêtre des trois appuis (signal trompeur pour les appuis d'une séquence, question restée non tranchée).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 : modèle du bouton validé explicitement.
**Doutes levés :** (aucun) ; ouvre DOU-079 « Compteur d'appuis validés : remise à zéro par un appui court, cas limites » et DOU-080 « Seuils de temps du bouton : 1 s, 2 s, 10 s et délai entre appuis »

### DEC-071 — Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-004 « Dégradé : appui de moins de 2 secondes sur le bouton »
**Décision :** Après un appui validé (DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court »), l'utilisateur relâche ou reste appuyé. S'il relâche, l'appui est compté et il peut refaire un appui validé. Les appuis comptent « d'affilée » si l'écart entre deux est d'environ 2 s au plus (durée exacte à fixer en architecture) ; au-delà, le compteur repart à zéro. Un appui de moins de 1 s remet le compteur à zéro (hypothèse du modèle, à confirmer : DOU-079 « Compteur d'appuis validés : remise à zéro par un appui court, cas limites »). Trois appuis validés d'affilée, drone posé et immobile (non armé) : entrée en mode réglage dès la 3e validation, signal « Mode réglage », sans armement même si le 3e appui est maintenu. En mode réglage, le bouton n'arme jamais (DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage » confirmée). Précise DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie » ; la sortie par coupure de la batterie n'est pas rediscutée (DOU-082 « Sortie du mode réglage : coupure de la batterie seulement, non rediscutée »). Remplace DEC-058 « Trois appuis : fenêtre courte, sans signal parasite ».
**Alternatives écartées :** conserver DEC-058 « Trois appuis : fenêtre courte, sans signal parasite », qui laissait un appui long armer en mode réglage (contradiction avec DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage ») ; entrée en mode réglage au relâchement du 3e appui (le 3e appui maintenu aurait pu armer).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 : modèle du bouton validé, et réponse selon laquelle le bouton n'arme pas en mode réglage, ce qui contredisait DEC-058 « Trois appuis : fenêtre courte, sans signal parasite » (règle de contradiction de `CLAUDE.md` §5 : la réponse de l'utilisateur donne raison à DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage »).
**Doutes levés :** DOU-077 « Séquence de trois appuis : cas incomplets et ambigus » ; la réponse de DOU-044 « Séquence de trois appuis : fenêtre et signal ? » (issue de DEC-058 « Trois appuis : fenêtre courte, sans signal parasite ») est remplacée

### DEC-072 — Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-003 « Échec : batterie faible à l'armement »
**Décision :** Si l'utilisateur reste appuyé jusqu'à 2 s au total depuis l'appui initial, le drone s'arme à condition que la batterie soit suffisante et que le drone soit immobile et à plat : signal « Prêt » (signal 6, distinct du signal « Appui validé »). Sinon, il donne le signal « Armement refusé » : un seul signal visuel et sonore pour toutes les causes (batterie faible, drone en mouvement, drone pas à plat). La cause est transmise par l'état envoyé sur le sans fil, différent selon la cause (contenu à définir : DOU-083 « Contenu du statut sans fil d'un armement ou d'un décollage refusé »). Le signal 5 « Batterie faible » local est remplacé par « Armement refusé » ; DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » reste valable sur le fond. Complète DEC-056 « Armement : drone immobile, sans autotest » : la condition d'armement devient « immobile et à plat ». Le tableau des signaux est renuméroté : Appui validé ajouté, Armement refusé à la place de Batterie faible, Appui trop court supprimé, soit toujours 17 signaux.
**Alternatives écartées :** un signal par cause de refus (batterie faible, mouvement, pas à plat), qui aurait gardé le signal « Batterie faible » et ajouté deux signaux ; refus sans signal.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 : modèle du bouton validé. Conséquence : un utilisateur sans appareil de suivi ne connaît pas la cause du refus (DEC-032 « Vol libre : le drone vole sans appareil de suivi »).
**Doutes levés :** DOU-073 « Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ? » en partie (signal et comportement en cas de refus) ; reste ouvert : la tolérance de mouvement

### DEC-073 — Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Décision :** Le drone est « Armé » entre 2 s et 10 s d'appui total depuis l'appui initial. Le relâchement dans cette plage donne le signal « Lancé », puis les moteurs démarrent 200 ms plus tard, même sans vrai lancer : DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » est confirmée, le signal « Lancé » peut être donné sans lancer, risque accepté. « Lancé » désigne aussi la phase qui court du relâchement au démarrage des moteurs. Au-delà de 10 s d'appui depuis l'appui initial, le drone se désarme (DEC-054 « Chrono de 10 secondes compté depuis l'appui initial » inchangée ; DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes » inchangée). Restent inchangés : la garde après le lancer (DEC-055 « Bouton ignoré pendant une courte garde après le lancer »), l'arrêt d'urgence par le bouton en vol (DEC-015 « Bouton appuyé en vol : arrêt d'urgence »), le bouton déjà enfoncé ignoré (DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement »), DEC-050 « Appui en cours lors d'une coupure des moteurs ignoré jusqu'au relâchement » et DEC-062 « Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs ».
**Alternatives écartées :** confirmer le lancer par la mesure du mouvement avant de démarrer les moteurs (déjà écarté par DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 : modèle du bouton validé et confirmation de DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » ; risque accepté.
**Doutes levés :** (aucun)

### DEC-074 — Décollage en mode réglage : la batterie est vérifiée, rien d'autre
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** À la commande « Décoller » en mode réglage, le drone vérifie seulement la batterie. Les autres protections restent exclues : ni posé, ni immobile, ni à plat, ni confirmation en deux temps. Complète DEC-038 « Mode réglage : décollage sans protection supplémentaire ». Le signal et l'état envoyé quand la batterie est insuffisante ne sont pas décidés (DOU-083 « Contenu du statut sans fil d'un armement ou d'un décollage refusé »).
**Alternatives écartées :** aucune vérification de la batterie (DEC-038 « Mode réglage : décollage sans protection supplémentaire » telle qu'écrite à l'origine) ; vérification complète posé, immobile et à plat.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-039 « La batterie est-elle vérifiée à chaque décollage de réglage ? » en partie (la batterie est vérifiée) ; reste ouvert : chauffe, limite du nombre de vols

### DEC-075 — Initialisation en échec : définitive jusqu'au débranchement de la batterie
**Date :** 2026-10-28
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-011 « Dégradé : coupure d'alimentation en vol »
**Décision :** Une initialisation en échec est définitive jusqu'au débranchement de la batterie : le drone ne refait pas l'initialisation en continu, même s'il se pose ensuite immobile. Un redémarrage en l'air qui échoue laisse donc le drone en « Échec d'initialisation » jusqu'au débranchement.
**Alternatives écartées :** initialisation refaite en continu, avec passage à « Allumé » dès que le drone est immobile et à plat.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28, à la première partie de DOU-074 « Une initialisation en échec est-elle définitive jusqu'au débranchement, et la condition à plat vaut-elle aussi après une coupure en vol ? ».
**Doutes levés :** DOU-074 « Une initialisation en échec est-elle définitive jusqu'au débranchement, et la condition à plat vaut-elle aussi après une coupure en vol ? » en partie ; reste ouvert : la condition « à plat » au redémarrage après une coupure en vol

<!-- Ajouter les décisions ci-dessous, au même format, en dehors des blocs de code. -->
