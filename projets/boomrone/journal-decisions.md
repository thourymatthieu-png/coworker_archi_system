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
**Précisée par :** DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension » le 2026-10-28 (le seuil d'armement doit rester au-dessus du seuil de sous-tension, valeur à fixer en architecture : DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » ; rapport à qualifier : DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs »).

### DEC-005 — Un signal distinct pour chaque information
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Chaque fois que le drone informe l'utilisateur, il utilise un signal différent. Cela vaut pour les 7 étapes du vol et pour les échecs.
**Alternatives écartées :** signal générique d'échec ; aucun signal d'échec.
**Raison :** choix de l'utilisateur ; l'utilisateur doit toujours savoir de quoi il s'agit. Complète DEC-001 « Information de l'utilisateur par signaux lumineux, sonores et suivi sur un autre appareil ».
**Doutes levés :** (aucun)
**Précisée par :** DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie » le 2026-10-28.
**Précisée par (suite) :** DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté » le 2026-10-28 (confirmée : signaux distincts = événements et statuts sans fil distincts, aucune durée minimale d'effet local de la cause, risque accepté pour l'utilisateur sans appareil de suivi).

### DEC-006 — Le relâchement du bouton armé suffit à démarrer les moteurs
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Une fois le drone armé (bouton maintenu 2 secondes), le relâchement du bouton signale le lancer et suffit : les moteurs démarrent 200 ms plus tard, sans confirmation que le drone a réellement été lancé.
**Alternatives écartées :** confirmer le lancer par la mesure du mouvement (accélération puis chute libre) avant de démarrer les moteurs.
**Raison :** choix de l'utilisateur ; simplicité. Risque résiduel accepté : un relâchement du bouton sans lancer démarre les moteurs, drone en main ou posé. Depuis : confirmée par l'utilisateur le 2026-10-28, signal « Lancé » possible sans lancer, risque accepté (DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard »).
**Doutes levés :** DOU-006 « Comment éviter un départ des moteurs sans vrai lancer ? »
**Précisée par :** DEC-083 « Annulation d'un armement : le maintien jusqu'au désarmement à 10 s reste la seule annulation » le 2026-10-28 (confirmée, risque à documenter).

### DEC-007 — Bouton relâché avant 2 secondes : retour en attente
**Date :** 2026-10-27
**Remplacée par :** DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court » le 2026-10-28, après la refonte du bouton demandée par l'utilisateur. Cette décision n'est plus en vigueur ; elle est conservée pour l'historique.
**Concerne :** SCN-004 « Appui normal : bouton relâché avant 2 secondes »
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
**Précisée par :** DEC-109 « Lancer hors plage ou hauteur non mesurable : échec de stabilisation, limite d'emploi » le 2026-10-28 (lancer hors plage : échec de stabilisation)
**Précisée par :** DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » le 2026-10-28 (plage de lancer à revoir avant les besoins ; valeurs provisoires).

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
**Modifiée par :** DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension » le 2026-10-28 (la coupure des moteurs sur sous-tension en vol est assumée par le logiciel : l'alternative écartée « couper les moteurs en vol » est de fait adoptée pour la sous-tension seulement ; le titre est conservé, il n'y a toujours ni atterrissage ni signal sur batterie faible en vol ; DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? » est relié à SCN-012 « Dégradé : sous-tension de la batterie »).

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
**Précisée par :** DEC-087 « Arrêt d'urgence par le bouton en vol : anti-rebond très court seulement, arrêt quasi immédiat » le 2026-10-28.

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
**Précisée par :** DEC-119 « Appui bref pendant la garde du bouton, relâché avant la fin : risque accepté et documenté » le 2026-10-28 (risque cumulé : appui bref pendant la garde, hélices tournantes en main).

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
**Précisée par :** DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter » le 2026-10-28 (cas d'échec de la programmation hors périmètre, limites d'emploi).

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
**Précisée par :** DEC-079 « Sortie du mode réglage : uniquement en enlevant la batterie » le 2026-10-28 (confirmée) ; DEC-085 « Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé » le 2026-10-28 (« posé » devient « immobile et à plat »).
**Modifiée par :** DEC-175 « Simplification n°2 adoptée : mode réglage par le bouton tenu à la mise sous tension » le 2026-10-29 (les trois appuis sont remplacés par le bouton tenu à la mise sous tension)

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
**Précisée par :** DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage » le 2026-10-28.
**Modifiée par :** DEC-106 « Lien sans fil perdu en vol de réglage : aucune action particulière » le 2026-10-28 (le lien perdu en vol de réglage n'a plus d'effet : plus d'atterrissage sur place, le vol suit son cours ; le reste est inchangé, le titre n'est pas réécrit)

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
**Précisée par :** DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil » le 2026-10-28 (le signal distinct s'entend comme événement et statut sans fil distincts ; l'effet local de la cause est écrasé par « Allumé »).
**Précisée par (suite) :** DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté » le 2026-10-28 (confirmée : signaux distincts = événements et statuts sans fil distincts, aucune durée minimale d'effet local de la cause, risque accepté pour l'utilisateur sans appareil de suivi).

### DEC-034 — Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Les réglages sont envoyés au drone par le sans fil. Une commande spécifique demande au drone de les sauvegarder. Au démarrage, quand la batterie est branchée, le drone charge ses dernières valeurs enregistrées depuis sa mémoire non volatile. Aucune configuration n'est poussée par l'appareil de suivi au démarrage : le drone vole sans aucun échange sans fil au départ. Précise DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol » et complète DEC-032 « Vol libre : le drone vole sans appareil de suivi ».
**Conséquence (confirmée par l'utilisateur) :** une valeur envoyée mais non sauvegardée ne survit pas à la coupure de la batterie ; au redémarrage, le drone charge les dernières valeurs enregistrées.
**Alternatives écartées :** non étudiées avec l'utilisateur (par exemple sauvegarde automatique à chaque modification).
**Raison :** choix de l'utilisateur, relayé à l'architecte à partir de sa réponse en chat ; permet d'essayer une valeur sans l'enregistrer.
**Doutes levés :** partiellement DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? » (partie conservation). Reste ouvert et bloquant : le retour à des réglages sûrs. Depuis : DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? » est levé par DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » et DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ».
**Précisée par :** DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture » le 2026-10-28 (coupure pendant l'écriture : risque accepté, à traiter en architecture) ; DEC-128 « Sauvegarder ignorée aussi à l'état Série d'appuis en cours » le 2026-10-28.

### DEC-035 — Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** (1) Il n'y a pas de commande de retour aux valeurs d'origine. Le seul recours contre un mauvais réglage sauvegardé est la reprogrammation du drone (SCN-008 « Mise en service : programmation du drone »). (2) Le cas d'une mémoire de réglages corrompue n'est pas traité : le drone ne détecte pas la corruption (pas de contrôle d'intégrité de type somme de contrôle). Complète DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage ».
**Alternatives écartées :** commande sans fil de retour aux valeurs d'origine, retour automatique après un vol raté, geste sur le bouton au démarrage ; détection de la corruption avec valeurs d'origine ou refus de s'armer.
**Raison :** choix de l'utilisateur, relayé à l'architecte à partir de sa réponse en chat : la personne qui règle le drone est expérimentée et assume ses réglages. Risques acceptés : un mauvais réglage sauvegardé impose la reprogrammation ; une mémoire corrompue peut donner un drone instable ou imprévisible, sans signal. Le comportement du drone neuf (mémoire jamais écrite) n'est pas décidé : voir DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? ». Depuis : il est décidé par DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ».
**Doutes levés :** partiellement DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? » (retour aux valeurs d'origine et mémoire corrompue). Reste ouvert : le comportement à la première mise sous tension. Depuis : DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? » est levé par DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ».
**Précisée par :** DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule » le 2026-10-28 (paramètres aberrants sauvegardés par un tiers : risque accepté, seule la reprogrammation rétablit les valeurs).
**Précisée par (suite) :** DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture » et DEC-130 « Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté » le 2026-10-28 (écriture interrompue et mémoire neuve : aucun contrôle d'intégrité) ; DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté » le 2026-10-28.

### DEC-036 — Drone neuf : valeurs d'origine fixes du logiciel, sans signal
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** À la première mise sous tension d'un drone neuf (mémoire de réglages jamais écrite), le drone utilise des valeurs d'origine fixes du logiciel, sans signal particulier. Complète DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage » et DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée ».
**Alternatives écartées :** refus de s'armer ou signal de mémoire vide (non retenus).
**Raison :** choix de l'utilisateur (option a, recommandée par l'architecte), relayé à l'architecte à partir de sa réponse en chat ; simple, cohérent avec un régleur expérimenté qui assume son test. Reste à fixer : les valeurs d'origine et leurs bornes (DOU-038 « Réglages en vol : valeurs d'origine, bornes, coupures en vol de réglage ? »). Depuis : DOU-038 « Réglages en vol : valeurs d'origine, bornes, coupures en vol de réglage ? » est levé par DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » ; les valeurs d'origine et les bornes numériques restent à fixer dans DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture ». Depuis : DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » impose des bornes aux seuils de sécurité ; leurs valeurs restent à fixer dans DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture ».
**Doutes levés :** DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? »
**Précisée par :** DEC-130 « Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté » le 2026-10-28 (aucune détection de la mémoire jamais écrite, risque accepté).

### DEC-037 — Pas d'appairage : le drone obéit à tout appareil de suivi à portée
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Il n'y a pas d'appairage : le drone obéit à tout appareil de suivi à portée. L'absence de l'appareil n'empêche pas le vol (DEC-032 « Vol libre : le drone vole sans appareil de suivi »). Précise DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol » et DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ».
**Alternatives écartées :** A, appairage persistant enregistré dans le drone ; B, appairage à chaque mise sous tension.
**Raison :** choix de l'utilisateur (option C), relayé à l'architecte à partir de sa réponse en chat ; simplicité. **Risques acceptés :** un tiers ou l'appareil d'un autre drone peut envoyer un arrêt, un décollage de réglage ou une sauvegarde de réglages ; une commande peut atteindre plusieurs drones à portée ; le suivi peut être mélangé si plusieurs drones sont à portée. Le risque d'une commande « Décoller » parasite n'est plus couvert par l'appairage : il renforce DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? ». Depuis : DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? » est levé par DEC-038 « Mode réglage : décollage sans protection supplémentaire ».
**Doutes levés :** DOU-047 « Appareil de suivi : appairage, absence, plusieurs drones »
**Précisée par :** DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule » le 2026-10-28 (paramètres aberrants sauvegardés par un tiers : risque accepté).
**Précisée par (suite) :** DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté » le 2026-10-28 (un tiers à portée peut écraser les réglages enregistrés d'un drone en échec d'initialisation : risque accepté).

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
**Précisée par :** DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule » le 2026-10-28 (paramètres aberrants sauvegardés par un tiers : risque accepté).
**Modifiée par :** DEC-177 « Simplification n°4 adoptée : commandes sans fil acceptées seulement en mode réglage » le 2026-10-29 (Modifier n'est plus acceptée en vol normal) ; DEC-180 « Simplification n°7 adoptée : valeurs de sécurité fixes dans le logiciel » le 2026-10-29 (valeurs de sécurité fixes) ; DEC-198 « Modifier retiré du vol normal : DEC-177 confirmée contre DEC-039 » le 2026-10-29 (suppression de Modifier en vol normal confirmée, malgré la réponse Q3 de l'utilisateur)

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
**Précisée par :** DEC-109 « Lancer hors plage ou hauteur non mesurable : échec de stabilisation, limite d'emploi » le 2026-10-28 (lancer hors plage : échec de stabilisation, limite d'emploi).

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
**Précisée par :** DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque » le 2026-10-28 (Sauvegarder reste acceptée à l'état armé).
**Complétée par :** DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » le 2026-10-28 (deux lignes ajoutées au tableau : initialisation en cours, échec d'initialisation)
**Modifiée par :** DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer » le 2026-10-28 (ligne « Armé, avant le lancer » : Sauvegarder devient ignorée ; les autres cases sont inchangées). ; DEC-177 « Simplification n°4 adoptée : commandes sans fil acceptées seulement en mode réglage » le 2026-10-29 (tableau réduit à quatre lignes) ; DEC-178 « Simplification n°5 adoptée : échec d'initialisation, toutes les commandes sans fil ignorées » le 2026-10-29 (échec d'initialisation : tout ignoré)
**Modifiée par (suite) :** DEC-120 « Sauvegarder ignorée pendant l'initialisation en cours, Modifier acceptée ; cas de l'échec d'initialisation non tranché » le 2026-10-28 (ligne « Initialisation en cours » : Sauvegarder ignorée) ; DEC-123 « Sauvegarder ignorée aussi à l'état Premier appui validé » le 2026-10-28 (nouvelle ligne « Premier appui validé » : Sauvegarder ignorée ; l'état « Série d'appuis en cours » n'est pas tranché).
**Modifiée par (suite 2) :** DEC-128 « Sauvegarder ignorée aussi à l'état Série d'appuis en cours » le 2026-10-28 (nouvelle ligne « Série d'appuis en cours » : Sauvegarder ignorée ; la ligne « Allumé, en attente d'un appui » n'accepte plus Sauvegarder pendant la série) ; confirmée par DEC-131 « Sauvegarder ignorée en vol : confirmation du tableau des commandes » le 2026-10-28 (Sauvegarder ignorée en vol, aucune case modifiée) ; DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté » le 2026-10-28 (ligne « Échec d'initialisation » : Sauvegarder acceptée, confirmée).

### DEC-044 — Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** En mode réglage, le bouton n'arme pas et n'a pas d'autre rôle de lancement : le seul moyen de décoller est la commande sans fil « Décoller » (DEC-028 « Mode réglage : décollage depuis le sol sur commande sans fil »), et la seule sortie est la coupure de la batterie (DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie »). Après un vol de réglage terminé, le drone reste en mode réglage, posé, prêt à une nouvelle commande « Décoller ». Le verrouillage de DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler » ne s'applique pas en mode réglage. Précise DEC-043 « Commandes sans fil acceptées selon l'état du drone ».
**Confirmé par l'utilisateur le 2026-10-27** (lecture de l'architecte à l'origine ; réponse en chat après présentation des options B « verrouillé jusqu'à la coupure de la batterie » et D « verrouillé jusqu'à un appui de 2 s » : « il faut garder Prêt à redécoller tout de suite via une commande sans fils ») : après un arrêt d'urgence (bouton ou sans fil), un échec de stabilisation ou un basculement en vol de réglage, le drone reste en mode réglage, posé, sans verrouillage. Conséquence : un arrêt d'urgence, même envoyé par un tiers sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »), n'empêche pas un nouveau « Décoller ». Risque accepté, lié à DEC-038 « Mode réglage : décollage sans protection supplémentaire ».
**Alternatives écartées :** A, verrouillé après tout vol de réglage (rend le cycle de réglage impraticable) ; B, verrouillé après un arrêt ou un échec ; D, déverrouillage par un appui de 2 s.
**Raison :** interprétation de la réponse de l'utilisateur en chat, relayée à l'architecte : « pour sortir du mode réglage, il faut déconnecter la batterie. Donc une fois en réglage, on ne peut que faire des décollages via commande sans fil pour régler. » Cohérent avec DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement » : aucun réarmement automatique, chaque décollage de réglage est commandé.
**Doutes levés :** DOU-056 « Commande sans fil et état du drone : que fait chaque commande dans chaque état ? »
**Précisée par :** DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage » le 2026-10-28.

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
**Précisée par :** DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil » le 2026-10-28 (le signal distinct s'entend comme événement et statut sans fil distincts ; l'effet local de la cause est écrasé par « Allumé »).
**Précisée par (suite) :** DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté » le 2026-10-28 (confirmée : signaux distincts = événements et statuts sans fil distincts, aucune durée minimale d'effet local de la cause, risque accepté pour l'utilisateur sans appareil de suivi).

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
**Décision :** Le critère de stationnaire de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » reçoit une condition supplémentaire « en l'air » : le drone n'est déclaré en vol stationnaire que si la hauteur mesurée sous lui dépasse une hauteur minimale. La valeur de cette hauteur minimale (de l'ordre de quelques centimètres) est à fixer en architecture, avec les autres valeurs numériques renvoyées à cette phase (DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture »). Les autres seuils de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » sont inchangés. Conséquence : un drone posé ou tenu immobile en main n'est jamais déclaré en stationnaire ; un drone relâché sans lancer, ou en contact avec le sol pendant la stabilisation, n'atteint pas le stationnaire et coupe ses moteurs au bout du délai de 2 s, avec le signal Échec de stabilisation (DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai », SCN-002 « Échec : stationnaire non atteint dans le délai »). DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer » reste valable avec cette condition : le cas des hélices en rotation sans lancer est bien couvert par SCN-002 « Échec : stationnaire non atteint dans le délai ».
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
**Précisée par :** DEC-082 « Retours à l'attente après le posé ou une coupure des moteurs : compteur à zéro, appui en cours ni pris en compte ni compté » le 2026-10-28.

### DEC-051 — Seuils de sécurité réglables dans des bornes fixées par le logiciel
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil », SCN-002 « Échec : stationnaire non atteint dans le délai » et SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Décision :** Les seuils de sécurité restent réglables par le sans fil, mais seulement à l'intérieur de bornes fixées dans le logiciel : le délai de 2 s (DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs »), l'angle limite (DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »), le délai de descente de 15 s (DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »), le seuil de batterie (DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement ») et la hauteur minimale (DEC-049 « Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale »). Une valeur hors bornes est refusée. La borne de la hauteur minimale est strictement supérieure à 0 (un réglage à 0 recréerait le défaut de DOU-066 « Le critère de stationnaire peut-il être rempli au sol ou dans la main ? »). Aucune valeur dans les bornes ne doit pouvoir supprimer une coupure. Les valeurs des bornes sont à fixer en architecture (DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture ») ; la plage peut rester large. Les autres réglages (gains, etc.) restent sans borne, selon DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ». Remplace DEC-045 « Seuils de sécurité réglables comme le reste, sans borne ». Le comportement du drone à la réception d'une valeur hors bornes (refus silencieux, signal, retour vers l'appareil de suivi) n'est pas décidé : voir DOU-071 « Que fait le drone quand il reçoit une valeur de seuil hors bornes ? ».
**Alternatives écartées :** A, seuils figés, modifiables seulement par reprogrammation (perd le réglage par le sans fil prévu par DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol ») ; B, seuils réglables sans borne, ancienne décision DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » (une valeur, même envoyée par un tiers sans appairage, peut désactiver une coupure).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-27, après revue de DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » à la porte « scénarios » via DOU-065 « Quelles décisions relayées ou interprétées sont à confirmer explicitement à la porte ? » : « C. Réglables mais bornés ». Option recommandée par l'architecte, hauteur minimale incluse. Avec une sécurité très ouverte (pas d'appairage, DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée » ; décollage sans protection, DEC-038 « Mode réglage : décollage sans protection supplémentaire » ; redécollage immédiat, DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage »), les coupures automatiques sont la dernière protection : les bornes garantissent qu'elles existent toujours, quel que soit l'auteur du réglage.
**Doutes levés :** DOU-057 « Les seuils de sécurité sont-ils des paramètres réglables sans borne ? » (réponse révisée) ; partiellement DOU-065 « Quelles décisions relayées ou interprétées sont à confirmer explicitement à la porte ? » (partie DEC-045 « Seuils de sécurité réglables comme le reste, sans borne »).
**Modifiée par :** DEC-180 « Simplification n°7 adoptée : valeurs de sécurité fixes dans le logiciel » le 2026-10-29 (les bornes sont remplacées par des valeurs de sécurité fixes)

### DEC-052 — Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Les scénarios sont validés avec les valeurs de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » (délai de 2 s), de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » (0,5 à 4 m/s, au moins 1,5 m du sol) et de DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » (angle limite de 60°), marquées provisoires. Elles sont à confirmer par analyse ou par essais avant la porte « exigences », y compris les limites de la plage de lancer (voir DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m »). Une phrase de SCN-001 « Vol nominal : de la batterie au posé » le dit.
**Alternatives écartées :** (b) confirmer les valeurs maintenant (bloque la porte « scénarios » sans architecture ni prototype) ; (c) tenir les valeurs pour définitives (faux : voir DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m »).
**Raison :** décision de l'utilisateur en chat, au sujet de DOU-030 « Les valeurs provisoires sont-elles à confirmer avant les exigences ? » : « option (a), valeurs provisoires pour cette porte, à confirmer avant la porte exigences, mention dans SCN-001 « Vol nominal : de la batterie au posé » [titre ajouté] ». Les valeurs ne peuvent pas être confirmées sans architecture ni prototype ; elles doivent l'être avant d'être chiffrées dans les exigences.
**Doutes levés :** DOU-030 « Les valeurs provisoires sont-elles à confirmer avant les exigences ? »
**Précisée par :** DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » le 2026-10-28 (échéance avancée à « avant les besoins » pour la plage de lancer et le stationnaire de 2 s).

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
**Précisée par :** DEC-078 « Garde du bouton après le lancer : attachée au lancer au relâchement, pas décidée pour le décollage de réglage » le 2026-10-28. ; DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement » le 2026-10-28.

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
**Décision :** L'entrée en mode réglage de DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie » se fait par trois appuis rapides dans une fenêtre courte, drone posé et immobile (la durée de la fenêtre est à fixer en architecture). Les deux premiers appuis n'émettent pas le signal « Appui trop court » de SCN-004 « Appui normal : bouton relâché avant 2 secondes ». Un appui long en mode réglage garde son sens normal (armement, DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes »). Le drone tenu en main n'entre pas en mode réglage (conséquence de DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie »).
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
**Précisée par :** DEC-081 « Bouton encore enfoncé après un refus ou un désarmement : ignoré jusqu'au premier relâchement, puis nouvel appui possible tout de suite » le 2026-10-28. ; DEC-088 « Bouton coincé ou maintenu en permanence au démarrage : statut sans fil seulement, aucun signal local » le 2026-10-28.
**Précisée par (suite) :** DEC-115 « Troisième appui encore maintenu à l'entrée en mode réglage : maintien ignoré jusqu'au premier relâchement » le 2026-10-28 (3e appui encore maintenu à l'entrée en mode réglage : ignoré jusqu'au premier relâchement) ; DEC-117 « Bouton en échec d'initialisation : ignoré pour toujours après le premier relâchement, aucun effet ni signal » le 2026-10-28 (en échec d'initialisation, le bouton est ignoré pour toujours après le premier relâchement : le titre de la présente décision ne vaut que pour l'initialisation en cours et les autres cas).

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
**Précisée par :** DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation » le 2026-10-28 (immobile et à plat).

### DEC-062 — Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Pendant la phase « Lancé », avant le démarrage des moteurs (200 ms, DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs »), l'arrêt du drone lancé de DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » n'est pas pris en compte, qu'il vienne du bouton ou du sans fil. Un arrêt demandé dans cet intervalle est perdu. Le bouton et l'arrêt sans fil ayant le même effet (coupure), la question de leur priorité relative ne se pose pas. Le sort des commandes Décoller, Modifier et Sauvegarder dans cet intervalle n'est pas tranché : voir DOU-072 « Commandes sans fil reçues pendant la phase Lancé : ignorées ou refusées ? ».
**Alternatives écartées :** arrêt toujours prioritaire, pris en compte dès « Lancé » (après la garde de DEC-055 « Bouton ignoré pendant une courte garde après le lancer »), option recommandée par l'architecte.
**Raison :** choix de l'utilisateur en chat, le 2026-10-28 (option différente de la recommandation de l'architecte). L'intervalle est court, 200 ms ; un arrêt demandé dans ce délai est perdu, mais les moteurs n'ont pas encore démarré.
**Doutes levés :** DOU-061 « Quelle priorité entre le bouton et l'arrêt sans fil, et l'arrêt est-il pris en compte pendant la phase Lancé ? »
**Précisée par :** DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale » le 2026-10-28 (le chien de garde couvre la phase Lancé, de durée maximale).

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
**Précisée par :** DEC-085 « Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé » le 2026-10-28 (la prémisse « trois appuis exigeant un drone posé » devient « immobile et à plat ») ; DEC-086 « Décollage de réglage : batterie seulement, risque cumulé avec les décisions sans appairage et sans verrouillage accepté » le 2026-10-28 (risque cumulé).

### DEC-065 — Logiciel bloqué en vol : coupure des moteurs par un chien de garde
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Si le logiciel se bloque en vol, les moteurs sont coupés par un mécanisme indépendant du logiciel (intention : chien de garde ou équivalent). Le drone redémarre ensuite comme après une coupure d'alimentation (SCN-011 « Dégradé : coupure d'alimentation en vol »). Le délai de détection est à chiffrer en exigences ; le mécanisme est à choisir en architecture.
**Alternatives écartées :** hors périmètre (le seul recours serait de débrancher la batterie, hélices tournantes).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte. Le bouton, l'arrêt sans fil et toutes les coupures dépendent du même logiciel ; une protection indépendante est la dernière.
**Doutes levés :** DOU-068 « Que se passe-t-il si le logiciel se bloque en vol ? »
**Précisée par :** DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale » le 2026-10-28 (couvre tout état où les moteurs peuvent être alimentés).

### DEC-066 — Commande sans fil corrompue : aucun contrôle d'intégrité
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Le drone ne vérifie pas l'intégrité des commandes sans fil : une commande reçue est appliquée telle quelle. Une trame tronquée ou bruitée peut donc produire une valeur aberrante, appliquée puis rendue permanente par « Sauvegarder » (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »). Les seuils de sécurité restent protégés par les bornes de DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » ; les autres réglages (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ») et les valeurs aberrantes situées dans les bornes ne sont pas protégés. Ce risque technique s'ajoute au risque « commandes d'un tiers » de DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée ». La couche de liaison choisie en architecture peut fournir un contrôle d'erreur sans que ce soit une exigence.
**Alternatives écartées :** rejet de toute commande dont le contrôle d'intégrité échoue, valeur précédente conservée (option recommandée par l'architecte).
**Raison :** choix de l'utilisateur en chat, le 2026-10-28 (option différente de la recommandation de l'architecte). Risque résiduel accepté.
**Doutes levés :** DOU-069 « Une commande sans fil corrompue est-elle rejetée ? »
**Précisée par :** DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule » le 2026-10-28 (paramètres aberrants sauvegardés par un tiers : risque accepté).

### DEC-067 — Démarrage à plat exigé, sinon échec de l'initialisation avec signal
**Date :** 2026-10-28
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage »
**Décision :** À la mise sous tension, le drone doit être posé à plat. Au-delà d'une inclinaison limite au démarrage, l'initialisation échoue, avec le signal d'échec d'initialisation de SCN-010 « Échec : initialisation impossible au démarrage » et le refus de s'armer de DEC-030 « Drone posé immobile à la mise sous tension ; refus de s'armer si l'initialisation échoue ». La valeur de l'inclinaison limite est à chiffrer en exigences. Aucun calibrage ni recalage sur surface inclinée n'est demandé (DEC-026 « Mise en service : calibrage éventuel renvoyé à l'architecture, réglage du vol par un scénario dédié » reste valable pour les autres besoins de calibrage).
**Alternatives écartées :** tolérer une surface inclinée en recalant l'horizontale de référence (calibrage ou référence plus élaborés).
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte. Évite une horizontale de référence faussée, donc une dérive ou un critère d'inclinaison jamais rempli.
**Doutes levés :** DOU-070 « Le drone doit-il démarrer posé à plat, ou tolérer une surface inclinée ? »
**Précisée par :** DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation » le 2026-10-28 (vaut aussi au redémarrage après une coupure en vol).

### DEC-068 — Seuil hors bornes : refus silencieux, valeur relue sur l'appareil de suivi
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Quand le drone reçoit une valeur de seuil de sécurité hors bornes (DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel »), il la refuse sans signal ni message d'erreur, et conserve la valeur précédente. L'appareil de suivi relit la valeur effectivement détenue par le drone : c'est la valeur affichée qui fait foi, et c'est ainsi que l'utilisateur constate que son réglage n'a pas été pris en compte. Aucun signal lumineux ou sonore n'est ajouté pour ce cas.
**Alternatives écartées :** refus avec retour explicite vers l'appareil de suivi (option recommandée par l'architecte) ; signal lumineux ou sonore sur le drone.
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : « refus silencieux, la valeur relue par l'appareil de suivi sera la valeur conservée par le drone ». Le suivi de DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol » doit donc permettre de relire les réglages.
**Doutes levés :** DOU-071 « Que fait le drone quand il reçoit une valeur de seuil hors bornes ? »
**Modifiée par :** DEC-180 « Simplification n°7 adoptée : valeurs de sécurité fixes dans le logiciel » le 2026-10-29 (plus de valeur hors bornes à refuser)

### DEC-069 — Commandes sans fil reçues pendant la phase Lancé : ignorées
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Pendant la phase « Lancé », avant le démarrage des moteurs, les commandes sans fil Décoller, Modifier et Sauvegarder sont ignorées, comme l'arrêt de DEC-062 « Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs ». Aucune commande sans fil n'est prise en compte dans cet état. La table de DEC-043 « Commandes sans fil acceptées selon l'état du drone » est à compléter d'une ligne « Lancé, avant démarrage des moteurs : aucune commande acceptée ».
**Alternatives écartées :** commandes refusées avec retour vers l'appareil de suivi.
**Raison :** réponse de l'utilisateur en chat, le 2026-10-28 : option recommandée par l'architecte.
**Doutes levés :** DOU-072 « Commandes sans fil reçues pendant la phase Lancé : ignorées ou refusées ? »

### DEC-070 — Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court
**Date :** 2026-10-28
**Concerne :** SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Décision :** L'« appui validé » est la brique unique du bouton : le bouton maintenu 1 s. Au moment de la validation, le drone donne un signal visuel et sonore « Appui validé ». Un appui de moins de 1 s n'a aucun effet et ne donne aucun signal. Le signal 4 « Appui trop court » est supprimé. SCN-004 « Appui normal : bouton relâché avant 2 secondes » (même identifiant, ancien titre « Dégradé : bouton relâché avant 2 secondes ») est refondu : moins de 1 s, rien ; relâché entre 1 s et 2 s, un appui validé est compté et le drone n'arme ni ne lance jamais. Les valeurs de 1 s et 2 s sont provisoires (DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences »). Remplace DEC-007 « Bouton relâché avant 2 secondes : retour en attente ».
**Alternatives écartées :** conserver le signal « Appui trop court » donné à chaque relâchement avant 2 s, immédiat ou retardé après la fenêtre des trois appuis (signal trompeur pour les appuis d'une séquence, question restée non tranchée).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 : modèle du bouton validé explicitement.
**Doutes levés :** (aucun) ; ouvre DOU-079 « Compteur d'appuis validés : remise à zéro par un appui de moins de 1 s, cas limites » et DOU-080 « Seuils de temps du bouton : 1 s, 2 s, 10 s et délai entre appuis »

### DEC-071 — Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Décision :** Après un appui validé (DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court »), l'utilisateur relâche ou reste appuyé. S'il relâche, l'appui est compté et il peut refaire un appui validé. Les appuis comptent « d'affilée » si l'écart entre deux est d'environ 2 s au plus (durée exacte à fixer en architecture) ; au-delà, le compteur repart à zéro. Un appui de moins de 1 s remet le compteur à zéro (hypothèse du modèle, à confirmer : DOU-079 « Compteur d'appuis validés : remise à zéro par un appui de moins de 1 s, cas limites »). Trois appuis validés d'affilée, drone posé et immobile (non armé) : entrée en mode réglage dès la 3e validation, signal « Mode réglage », sans armement même si le 3e appui est maintenu. En mode réglage, le bouton n'arme jamais (DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage » confirmée). Précise DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie » ; la sortie par coupure de la batterie n'est pas rediscutée (DOU-082 « Sortie du mode réglage : coupure de la batterie seulement, non rediscutée »). Remplace DEC-058 « Trois appuis : fenêtre courte, sans signal parasite ».
**Alternatives écartées :** conserver DEC-058 « Trois appuis : fenêtre courte, sans signal parasite », qui laissait un appui long armer en mode réglage (contradiction avec DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage ») ; entrée en mode réglage au relâchement du 3e appui (le 3e appui maintenu aurait pu armer).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 : modèle du bouton validé, et réponse selon laquelle le bouton n'arme pas en mode réglage, ce qui contredisait DEC-058 « Trois appuis : fenêtre courte, sans signal parasite » (règle de contradiction de `CLAUDE.md` §5 : la réponse de l'utilisateur donne raison à DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage »).
**Doutes levés :** DOU-077 « Séquence de trois appuis : cas incomplets et ambigus » ; la réponse de DOU-044 « Séquence de trois appuis : fenêtre et signal ? » (issue de DEC-058 « Trois appuis : fenêtre courte, sans signal parasite ») est remplacée
**Précisée par :** DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série » le 2026-10-28 ; DEC-085 « Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé » le 2026-10-28. ; DEC-089 « Appui de moins de 1 s au milieu d'une série d'appuis : compteur remis à zéro » et DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus » le 2026-10-28.
**Précisée par :** DEC-116 « Bouton en mode réglage, moteurs coupés : aucun effet et aucun signal, il ne sert qu'en vol de réglage » le 2026-10-28 (en mode réglage au sol, le bouton n'a aucun effet et ne donne aucun signal ; il ne sert qu'en vol de réglage).
**Modifiée par :** DEC-175 « Simplification n°2 adoptée : mode réglage par le bouton tenu à la mise sous tension » le 2026-10-29 (plus de série de trois appuis)

### DEC-072 — Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-003 « Échec : batterie faible à l'armement »
**Décision :** Si l'utilisateur reste appuyé jusqu'à 2 s au total depuis l'appui initial, le drone s'arme à condition que la batterie soit suffisante et que le drone soit immobile et à plat : signal « Prêt » (signal 6, distinct du signal « Appui validé »). Sinon, il donne le signal « Armement refusé » : un seul signal visuel et sonore pour toutes les causes (batterie faible, drone en mouvement, drone pas à plat). La cause est transmise par le statut sans fil, différent selon la cause (contenu à définir : DOU-083 « Contenu du statut sans fil d'un armement ou d'un décollage refusé »). Le signal 5 « Batterie faible » local est remplacé par « Armement refusé » ; DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » reste valable sur le fond. Complète DEC-056 « Armement : drone immobile, sans autotest » : la condition d'armement devient « immobile et à plat ». Le tableau des signaux est renuméroté : Appui validé ajouté, Armement refusé à la place de Batterie faible, Appui trop court supprimé, soit toujours 17 signaux.
**Alternatives écartées :** un signal par cause de refus (batterie faible, mouvement, pas à plat), qui aurait gardé le signal « Batterie faible » et ajouté deux signaux ; refus sans signal.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 : modèle du bouton validé. Conséquence : un utilisateur sans appareil de suivi ne connaît pas la cause du refus (DEC-032 « Vol libre : le drone vole sans appareil de suivi »).
**Doutes levés :** DOU-073 « Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ? » en partie (signal et comportement en cas de refus) ; reste ouvert : la tolérance de mouvement
**Précisée par :** DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série » le 2026-10-28 ; DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté » et DEC-081 « Bouton encore enfoncé après un refus ou un désarmement : ignoré jusqu'au premier relâchement, puis nouvel appui possible tout de suite » le 2026-10-28. ; DEC-091 « Un seul signal Refus pour tout refus, armement ou mode réglage » le 2026-10-28 (renommage du signal 5 en « Refus », sans modifier le titre de cette décision). ; DEC-110 « Armement refusé à 2 secondes d'appui : tous les tests faits, un seul signal Refus, sans attente de l'immobilité » le 2026-10-28 (tous les tests faits à 2 s, ordre sans importance)

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
**Précisée par :** DEC-086 « Décollage de réglage : batterie seulement, risque cumulé avec les décisions sans appairage et sans verrouillage accepté » le 2026-10-28 (confirmée). ; DEC-108 « Vols de réglage répétés : aucune limite de nombre ni contrôle de chauffe, risque accepté » le 2026-10-28 (pas de limite de vols ni de contrôle de chauffe) ; DEC-102 « Décollage de réglage refusé : signal Refus, statut de refus lisible jusqu'à la commande suivante » le 2026-10-28 (signal Refus en cas de batterie insuffisante)

### DEC-075 — Initialisation en échec : définitive jusqu'au débranchement de la batterie
**Date :** 2026-10-28
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-011 « Dégradé : coupure d'alimentation en vol »
**Décision :** Une initialisation en échec est définitive jusqu'au débranchement de la batterie : le drone ne refait pas l'initialisation en continu, même s'il se pose ensuite immobile. Un redémarrage en l'air qui échoue laisse donc le drone en « Échec d'initialisation » jusqu'au débranchement.
**Alternatives écartées :** initialisation refaite en continu, avec passage à « Allumé » dès que le drone est immobile et à plat.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28, à la première partie de DOU-074 « Une initialisation en échec est-elle définitive jusqu'au débranchement, et la condition à plat vaut-elle aussi après une coupure en vol ? ».
**Doutes levés :** DOU-074 « Une initialisation en échec est-elle définitive jusqu'au débranchement, et la condition à plat vaut-elle aussi après une coupure en vol ? » en partie ; reste ouvert : la condition « à plat » au redémarrage après une coupure en vol
**Précisée par :** DEC-117 « Bouton en échec d'initialisation : ignoré pour toujours après le premier relâchement, aucun effet ni signal » le 2026-10-28 (bouton ignoré pour toujours en échec d'initialisation, sans effet ni signal).

### DEC-076 — Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série
**Date :** 2026-10-28
**Concerne :** SCN-004 « Appui normal : bouton relâché avant 2 secondes », SCN-001 « Vol nominal : de la batterie au posé » et SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** L'armement (maintien de 2 s au total, DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone ») n'est possible que depuis le premier appui d'une série (compteur d'appuis validés à 1). Si le premier appui est relâché avant 2 s (appui normal, compté), le drone est dans la série de trois appuis (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage ») : aucun appui suivant ne peut armer. Pendant la série (2e appui), maintenir le bouton au-delà de 2 s ne fait rien : ni armement, ni signal, ni annulation de la série ; l'appui reste compté à 1 s. Le 3e appui validé entre en mode réglage dès sa validation (inchangé). Si 2 s s'écoulent sans nouvel appui, le compteur repart à zéro et l'armement redevient possible au prochain appui (inchangé). Le désarmement à 10 s et le lancer au relâchement ne concernent qu'un drone armé, donc armé depuis le premier appui : la question « 10 s depuis quel appui » ne se pose plus (DEC-054 « Chrono de 10 secondes compté depuis l'appui initial » et DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard » inchangées).
**Alternatives écartées :** (aucune exposée)
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun) ; précise une partie de DOU-079 « Compteur d'appuis validés : remise à zéro par un appui de moins de 1 s, cas limites » (le 3e appui, et tout appui de la série, n'arme pas)
**Précisée par :** DEC-084 « Appui ignoré pendant une série d'appuis : aucun signal, risque accepté et documenté » le 2026-10-28.
**Modifiée par :** DEC-175 « Simplification n°2 adoptée : mode réglage par le bouton tenu à la mise sous tension » le 2026-10-29 (plus de premier appui d'une série)

### DEC-077 — Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Un appui sur le bouton pendant un vol de réglage est un arrêt d'urgence : les moteurs sont coupés et le drone reste en mode réglage, posé, sans verrouillage. Le bouton n'arme pas en mode réglage (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »). Précise DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu » (qui renvoyait à DEC-015 « Bouton appuyé en vol : arrêt d'urgence ») et DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage ». Le signal donné n'est pas défini : voir DOU-053 « Vols de réglage : signaux des phases, signal du lien perdu, acquittement des commandes ».
**Alternatives écartées :** bouton ignoré en vol de réglage ; appui sans effet sur les moteurs.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28. Aucune contradiction : confirme DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu » telle qu'écrite.
**Doutes levés :** DOU-081 « Bouton appuyé en vol de réglage : arrêt d'urgence ou non ? »
**Précisée par :** DEC-094 « Bouton appuyé après un décollage de réglage : pris en compte tout de suite, sans garde » et DEC-100 « Issues du vol de réglage : signaux du vol normal réutilisés, signal du lien perdu à définir » le 2026-10-28.
**Précisée par :** DEC-116 « Bouton en mode réglage, moteurs coupés : aucun effet et aucun signal, il ne sert qu'en vol de réglage » le 2026-10-28 (en mode réglage au sol, le bouton n'a aucun effet ; l'arrêt d'urgence ne vaut qu'en vol de réglage) ; DEC-115 « Troisième appui encore maintenu à l'entrée en mode réglage : maintien ignoré jusqu'au premier relâchement » le 2026-10-28 (un maintien hérité de l'entrée en mode réglage ne peut pas déclencher d'arrêt).

### DEC-078 — Garde du bouton après le lancer : attachée au lancer au relâchement, pas décidée pour le décollage de réglage
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol » et SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** La courte garde pendant laquelle le bouton est ignoré (DEC-055 « Bouton ignoré pendant une courte garde après le lancer ») ne s'applique qu'après un lancer au relâchement du bouton. Pour le vol de réglage, décollage sur commande sans fil (DEC-028 « Mode réglage : décollage depuis le sol sur commande sans fil »), l'existence d'une garde après le décollage n'est pas décidée : voir DOU-084 « Garde du bouton après le décollage de réglage ? ».
**Alternatives écartées :** aucune exposée.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 : la garde de DEC-055 « Bouton ignoré pendant une courte garde après le lancer » ne concerne que le lancer au relâchement.
**Doutes levés :** (aucun) ; ouvre DOU-084 « Garde du bouton après le décollage de réglage ? »
**Précisée par :** DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement » le 2026-10-28.
**Précisée par (suite) :** DEC-094 « Bouton appuyé après un décollage de réglage : pris en compte tout de suite, sans garde » le 2026-10-28.

### DEC-079 — Sortie du mode réglage : uniquement en enlevant la batterie
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** La seule façon de sortir du mode réglage est d'enlever la batterie ; ni le bouton, ni le sans fil, ni un délai ne font sortir du mode. Confirme DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie » après le nouveau modèle du bouton (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »).
**Alternatives écartées :** aucune exposée.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-082 « Sortie du mode réglage : coupure de la batterie seulement, non rediscutée »

### DEC-080 — Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté
**Date :** 2026-10-28
**Concerne :** SCN-003 « Échec : batterie faible à l'armement », SCN-004 « Appui normal : bouton relâché avant 2 secondes » et SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Décision :** Après un armement refusé (DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone ») ou un désarmement par appui de plus de 10 s (DEC-054 « Chrono de 10 secondes compté depuis l'appui initial »), le drone revient à l'état « Allumé, en attente d'un appui », le compteur d'appuis de la série est à zéro, et l'appui long (2 s ou plus) ne compte pas comme appui de la série. Précise DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone » et DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série ».
**Alternatives écartées :** appui long compté à 1 dans la série (le prochain appui serait un 2e appui, qui ne peut pas armer).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun) ; répond en partie à DOU-079 « Compteur d'appuis validés : remise à zéro par un appui de moins de 1 s, cas limites » (appui long après refus ou désarmement)
**Précisée par :** DEC-118 « Signal Allumé au retour à l'attente après un posé, un refus ou un désarmement » le 2026-10-28 (signal « Allumé » au retour à l'attente après un refus ou un désarmement).

### DEC-081 — Bouton encore enfoncé après un refus ou un désarmement : ignoré jusqu'au premier relâchement, puis nouvel appui possible tout de suite
**Date :** 2026-10-28
**Concerne :** SCN-003 « Échec : batterie faible à l'armement » et SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Décision :** Après un armement refusé ou un désarmement, le bouton encore enfoncé est ignoré jusqu'à son premier relâchement (DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement », étendue au cas de l'armement refusé). Après ce relâchement, un nouvel appui peut armer immédiatement, car le compteur est à zéro (DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté »). Conséquence : un appui maintenu plus de 10 s après un armement refusé n'a aucun effet de plus (pas de désarmement, pas de signal), le bouton étant ignoré.
**Alternatives écartées :** aucune exposée.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 ; la conséquence sur l'appui de plus de 10 s sans armement, tirée par l'architecte de cette réponse, a été validée explicitement par l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun) ; répond en partie à DOU-073 « Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ? » (bouton après refus ; appui de plus de 10 s sans armement)

### DEC-082 — Retours à l'attente après le posé ou une coupure des moteurs : compteur à zéro, appui en cours ni pris en compte ni compté
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** La logique de DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté » et DEC-081 « Bouton encore enfoncé après un refus ou un désarmement : ignoré jusqu'au premier relâchement, puis nouvel appui possible tout de suite » s'applique aux autres retours à l'attente : après le posé ou une coupure des moteurs, le drone est dans le même état que « Allumé, en attente d'un appui » (DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »), compteur à zéro, et un appui déjà en cours est ignoré jusqu'au relâchement (DEC-050 « Appui en cours lors d'une coupure des moteurs ignoré jusqu'au relâchement »), donc non compté. Un nouvel appui, commencé après ce relâchement, peut armer. Le lancer n'est pas un retour à l'attente : le drone vole, et n'y revient que par le posé ou une coupure, compteur à zéro. Déduction de l'architecte à partir de DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler », des deux décisions rappelées ci-dessus, soumise à l'utilisateur dans le rapport.
**Alternatives écartées :** aucune exposée.
**Raison :** déduction de l'architecte à partir des décisions existantes, validée explicitement par l'utilisateur en chat, 2026-10-28 ; aucune décision existante n'est contredite.
**Doutes levés :** (aucun) ; répond en partie à DOU-079 « Compteur d'appuis validés : remise à zéro par un appui de moins de 1 s, cas limites »
**Précisée par :** DEC-118 « Signal Allumé au retour à l'attente après un posé, un refus ou un désarmement » le 2026-10-28 (signal « Allumé » au retour à l'attente après un posé).

### DEC-083 — Annulation d'un armement : le maintien jusqu'au désarmement à 10 s reste la seule annulation
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Décision :** Le seul moyen de renoncer à un armement est de rester appuyé jusqu'au désarmement à 10 s d'appui (DEC-054 « Chrono de 10 secondes compté depuis l'appui initial »), soit environ 8 s après le signal « Prêt ». Aucune fenêtre d'annulation, aucun seuil plus court, aucun autre geste. Risque accepté, à documenter dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? ») : relâcher le bouton armé démarre les moteurs 200 ms plus tard, y compris dans la main ; renoncer demande de rester appuyé jusqu'à 10 s. Confirme DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » et DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard » ; DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer » inchangée.
**Alternatives écartées :** fenêtre d'annulation après le signal Prêt ; seuil de désarmement plus court ; commande sans fil d'annulation.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-088 « Annulation d'un armement : comment renoncer après le signal Prêt ? »

### DEC-084 — Appui ignoré pendant une série d'appuis : aucun signal, risque accepté et documenté
**Date :** 2026-10-28
**Concerne :** SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Décision :** Le 2e appui maintenu au-delà de 2 s pendant une série d'appuis (DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série ») ne donne aucun signal, comme décidé jusqu'ici. Risque accepté, à documenter dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? ») : l'utilisateur peut ne pas comprendre pourquoi rien ne se passe, et retaper jusqu'à entrer en mode réglage par erreur (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »), dont la seule sortie est d'enlever la batterie (DEC-079 « Sortie du mode réglage : uniquement en enlevant la batterie »).
**Alternatives écartées :** signal pour l'appui ignoré dans la série (existant ou nouveau), en lien avec DEC-005 « Un signal distinct pour chaque information ».
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-087 « Appui ignoré en silence pendant une série d'appuis : faut-il un signal ? »
**Précise :** DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série ».
**Modifiée par :** DEC-175 « Simplification n°2 adoptée : mode réglage par le bouton tenu à la mise sous tension » le 2026-10-29 (plus de série d'appuis)

### DEC-085 — Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Décision :** Les trois appuis validés n'entrent en mode réglage que si le drone est immobile et à plat, et non armé. Le mot « posé » n'est plus une condition : le drone ne sait pas s'il est posé (DEC-057 « Pas de détection dédiée d'un drone attrapé ou posé sur un obstacle »). Même condition que l'armement (DEC-056 « Armement : drone immobile, sans autotest » ; DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone »). Un drone tenu en main, immobile et à plat, peut donc entrer en mode réglage. La tolérance d'« immobile » reste dans DOU-073 « Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ? ». Le comportement de la 3e validation quand la condition n'est pas remplie n'est pas décidé : DOU-079 « Compteur d'appuis validés : remise à zéro par un appui de moins de 1 s, cas limites » (3e appui sur un drone en mouvement).
**Alternatives écartées :** aucune condition ; « immobile » seulement.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-085 « Entrée en mode réglage : exiger drone immobile seulement, ou aussi à plat ? »
**Précise :** DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage » et DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie » (« posé » devient « immobile et à plat »). La raison de DEC-064 « Main près des hélices en mode réglage : risque accepté et documenté » (« trois appuis exigeant un drone posé ») est précisée de même, sans réécrire l'historique.
**Précisée par :** DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus » le 2026-10-28.
**Précisée par :** DEC-115 « Troisième appui encore maintenu à l'entrée en mode réglage : maintien ignoré jusqu'au premier relâchement » le 2026-10-28 (bouton encore maintenu à l'entrée en mode réglage : ignoré jusqu'au premier relâchement).

### DEC-086 — Décollage de réglage : batterie seulement, risque cumulé avec les décisions sans appairage et sans verrouillage accepté
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** La commande Décoller en mode réglage ne vérifie que la batterie, sans condition de position (DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre » confirmée). Le risque cumulé de DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée », DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage » et DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre » est explicitement accepté : un appareil à portée peut faire décoller un drone retourné ou tenu en main en mode réglage, hélices contre le sol ou dans une main. À documenter dans les limites d'emploi, avec DEC-064 « Main près des hélices en mode réglage : risque accepté et documenté » (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »).
**Alternatives écartées :** condition supplémentaire (drone à plat ou immobile, délai après un arrêt).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-086 « Décollage de réglage commandé par un tiers, drone en main ou retourné : risque cumulé accepté ? »
**Précise :** DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre » et DEC-064 « Main près des hélices en mode réglage : risque accepté et documenté ».

### DEC-087 — Arrêt d'urgence par le bouton en vol : anti-rebond très court seulement, arrêt quasi immédiat
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** En vol, passé la garde du lancer (DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement »), l'appui sur le bouton est filtré par un anti-rebond très court seulement (quelques millisecondes, valeur à fixer en architecture) et coupe les moteurs quasi immédiatement. Il n'y a ni durée minimale de 100 ms, ni validation de 1 s : la validation de 1 s de DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court » ne vaut qu'au sol. Risque connu et accepté : un parasite plus long que l'anti-rebond peut couper les moteurs en vol. Ce risque est à reporter dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »).
**Alternatives écartées :** durée minimale d'appui de 100 ms ; validation de 1 s comme au sol (arrêt d'urgence trop tardif) ; aucun filtrage.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-089 « Arrêt d'urgence par le bouton en vol : filtrage du rebond et des parasites »
**Précise :** DEC-015 « Bouton appuyé en vol : arrêt d'urgence » (« immédiatement » = anti-rebond de quelques millisecondes).

### DEC-088 — Bouton coincé ou maintenu en permanence au démarrage : statut sans fil seulement, aucun signal local
**Date :** 2026-10-28
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Si le bouton est coincé ou maintenu en permanence au démarrage, seul le statut envoyé sur le sans fil le signale : l'appareil de suivi indique « bouton maintenu ». Aucun nouveau signal local n'est créé ; le drone reste silencieux au bouton, comme prévu par DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement ». Risque accepté pour l'utilisateur sans appareil de suivi, qui ne sait pas pourquoi le drone ne s'arme pas ; à documenter dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »). Le moment où le statut apparaît (dès le démarrage ou après un délai) et son contenu exact sont à fixer en architecture.
**Alternatives écartées :** signal local existant ou nouveau après un délai donné.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-090 « Bouton coincé ou maintenu en permanence au démarrage : faut-il un signal ? »
**Précise :** DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement ». Écart de forme avec DEC-005 « Un signal distinct pour chaque information » (une information sans signal local) : même logique que DEC-084 « Appui ignoré pendant une série d'appuis : aucun signal, risque accepté et documenté », et DOU-027 « Un signal distinct par information, ou par catégorie ? » reste ouvert.
**Modifiée par :** DEC-175 « Simplification n°2 adoptée : mode réglage par le bouton tenu à la mise sous tension » le 2026-10-29 (un bouton coincé au démarrage mène au mode réglage)

### DEC-089 — Appui de moins de 1 s au milieu d'une série d'appuis : compteur remis à zéro
**Date :** 2026-10-28
**Concerne :** SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Décision :** Un appui de moins de 1 s, au milieu d'une série d'appuis validés, remet le compteur d'appuis à zéro. Il ne fait rien d'autre, ni effet ni signal (DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court »).
**Alternatives écartées :** appui de moins de 1 s ignoré, compteur inchangé.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 : confirme l'hypothèse de DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage ».
**Doutes levés :** DOU-079 « Compteur d'appuis validés : remise à zéro par un appui de moins de 1 s, cas limites » (avec DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus »)
**Précise :** DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage ».

### DEC-090 — Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Décision :** Si le 3e appui validé arrive alors que le drone n'est pas immobile et à plat (condition de DEC-085 « Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé »), le mode réglage est refusé et le drone donne le signal « Refus » (voir DEC-091 « Un seul signal Refus pour tout refus, armement ou mode réglage »). Le drone reste en mode normal, non armé. La cause est transmise par le statut sans fil. Le signal « Mode réglage » n'est donné qu'à une entrée réussie (déjà décidé par DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »).
**Alternatives écartées :** 3e appui ignoré sans signal ; entrée en mode réglage malgré la condition (contredit DEC-085 « Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 (d'abord « signal de refus », puis, après rappel du conflit avec DEC-005 « Un signal distinct pour chaque information » et DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone », choix d'un seul signal Refus). Le compteur après ce refus, déduit par l'architecte, a été confirmé par l'utilisateur (DEC-093 « Mode réglage refusé : retour à l'attente, compteur à zéro, bouton encore enfoncé ignoré »).
**Doutes levés :** DOU-079 « Compteur d'appuis validés : remise à zéro par un appui de moins de 1 s, cas limites » (point du 3e appui sur un drone en mouvement)
**Précise :** DEC-085 « Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé » et DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage ».

### DEC-091 — Un seul signal Refus pour tout refus, armement ou mode réglage
**Date :** 2026-10-28
**Concerne :** SCN-003 « Échec : batterie faible à l'armement », SCN-001 « Vol nominal : de la batterie au posé » et SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Le signal 5 « Armement refusé » est renommé « Refus ». C'est un seul signal visuel et sonore pour tout refus : armement refusé à 2 s d'appui (batterie faible, drone en mouvement, pas à plat) ou mode réglage refusé au 3e appui validé (DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus »). La cause est donnée par le statut sans fil. Le tableau reste à 17 signaux. Le renommage touche le tableau des signaux, le glossaire, les diagrammes, les séquences et les légendes de `00-scenarios.md`. Les titres des décisions existantes ne sont pas modifiés (DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone » et DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté ») et les mentions « Armement refusé » des corps de texte historiques du journal restent.
**Alternatives écartées :** un signal distinct « Mode réglage refusé » (18 signaux, mieux conforme à DEC-005 « Un signal distinct pour chaque information »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28, après rappel du conflit avec DEC-005 « Un signal distinct pour chaque information » (déjà assoupli par DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone », qui regroupe plusieurs causes sous un signal). DOU-027 « Un signal distinct par information, ou par catégorie ? » reste ouvert.
**Doutes levés :** (aucun)
**Précise :** DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone ».
**Précisée par :** DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie » le 2026-10-28 (DOU-027 « Un signal distinct par information, ou par catégorie ? » levé). ; DEC-102 « Décollage de réglage refusé : signal Refus, statut de refus lisible jusqu'à la commande suivante » le 2026-10-28 (le décollage de réglage refusé donne aussi le signal Refus)

### DEC-092 — Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol » et SCN-002 « Échec : stationnaire non atteint dans le délai »
**Décision :** La garde de DEC-055 « Bouton ignoré pendant une courte garde après le lancer » ignore les fronts du bouton (appuis et relâchements) mais pas son niveau. Si le bouton est encore enfoncé quand la garde se termine, c'est un arrêt d'urgence (DEC-015 « Bouton appuyé en vol : arrêt d'urgence »), pris en compte à la fin de la garde. La garde commence au relâchement du bouton (le geste du lancer) : elle couvre donc la phase « Lancé » de 200 ms (DEC-062 « Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs ») puis le démarrage des moteurs. Durée de l'ordre de 0,5 s, à fixer en architecture. Le réflexe de ré-appui après un relâchement sans lancer (SCN-002 « Échec : stationnaire non atteint dans le délai ») reste efficace, avec au plus la durée de la garde de retard (DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer »).
**Alternatives écartées :** garde sans mémoire du niveau (un appui maintenu après la garde serait ignoré jusqu'à un nouveau front) ; arrêt différé seulement au relâchement.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-076 « Garde du bouton après le lancer : front ou niveau, et quelle origine par rapport à la phase Lancé ? »
**Précise :** DEC-055 « Bouton ignoré pendant une courte garde après le lancer » et DEC-078 « Garde du bouton après le lancer : attachée au lancer au relâchement, pas décidée pour le décollage de réglage » (la garde du décollage de réglage reste dans DOU-084 « Garde du bouton après le décollage de réglage ? »).
**Précisée par :** DEC-119 « Appui bref pendant la garde du bouton, relâché avant la fin : risque accepté et documenté » le 2026-10-28 (appui bref relâché avant la fin de la garde : sans effet, risque accepté ; la présente décision reste inchangée).

### DEC-093 — Mode réglage refusé : retour à l'attente, compteur à zéro, bouton encore enfoncé ignoré
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Décision :** Après un mode réglage refusé au 3e appui validé (DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus »), le drone revient à « Allumé, en attente d'un appui » : le compteur d'appuis est à zéro, le 3e appui n'est pas compté, et le bouton encore enfoncé est ignoré jusqu'à son premier relâchement (même logique que DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté » et DEC-081 « Bouton encore enfoncé après un refus ou un désarmement : ignoré jusqu'au premier relâchement, puis nouvel appui possible tout de suite »). Un nouvel essai est possible tout de suite, après le relâchement.
**Alternatives écartées :** garder la série en cours (compteur laissé à 3 : un appui parasite pourrait entrer en mode réglage).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 (option recommandée par l'architecte, déduction confirmée).
**Doutes levés :** DOU-091 « Compteur d'appuis après un mode réglage refusé : retour à l'attente, compteur à zéro ? »
**Précise :** DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus »

### DEC-094 — Bouton appuyé après un décollage de réglage : pris en compte tout de suite, sans garde
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Après un décollage de réglage sur commande sans fil, le bouton est pris en compte tout de suite comme arrêt d'urgence (DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage »), filtré par l'anti-rebond de quelques millisecondes seulement (DEC-087 « Arrêt d'urgence par le bouton en vol : anti-rebond très court seulement, arrêt quasi immédiat »). Il n'y a pas de garde après ce décollage : aucun geste de lancer ne produit d'appui parasite. La garde de DEC-055 « Bouton ignoré pendant une courte garde après le lancer » et de DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement » reste réservée au lancer au relâchement. Conséquence connue : une main proche du bouton peut couper les moteurs sans le vouloir pendant un vol de réglage.
**Alternatives écartées :** une garde aussi après le décollage de réglage.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-084 « Garde du bouton après le décollage de réglage ? »
**Précise :** DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage » et DEC-078 « Garde du bouton après le lancer : attachée au lancer au relâchement, pas décidée pour le décollage de réglage ».

### DEC-095 — Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** La commande « Sauvegarder » reste acceptée à l'état « Armé, avant le lancer », comme dans la table de DEC-043 « Commandes sans fil acceptées selon l'état du drone » (inchangée). Risque accepté : une écriture en mémoire non volatile peut retarder le lancer, c'est-à-dire le démarrage des moteurs après le relâchement du bouton (DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard »). Ce risque est à traiter en architecture ; il est aussi une limite d'emploi à documenter (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »).
**Alternatives écartées :** ignorer « Sauvegarder » à l'état armé.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-078 « Initialisation en cours et échec d'initialisation : quelles commandes sans fil sont acceptées ? » en partie (le cas de l'état armé) ; reste ouvert : l'initialisation en cours et l'échec d'initialisation, non répondus
**Précise :** DEC-043 « Commandes sans fil acceptées selon l'état du drone ».
**Précisée par :** DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » le 2026-10-28 (Modifier et Sauvegarder aussi acceptées pendant l'initialisation et après un échec d'initialisation)
**Modifiée par :** DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer » le 2026-10-28 (Sauvegarder est ignorée à l'état armé ; l'alternative écartée ci-dessus est de fait adoptée ; le titre est conservé).

### DEC-096 — Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Le chien de garde couvre tout état où les moteurs peuvent être alimentés, donc aussi la phase « Lancé » (DEC-065 « Logiciel bloqué en vol : coupure des moteurs par un chien de garde »). La phase « Lancé » a une durée maximale, de l'ordre de quelques centaines de millisecondes, valeur à fixer en architecture et provisoire (DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences »). L'arrêt reste ignoré pendant cette phase (DEC-062 « Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs ») : c'est le chien de garde, indépendant du logiciel, qui évite qu'un drone reste sourd à tout. La durée maximale doit au moins couvrir le délai de 200 ms avant le démarrage des moteurs (DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard ») ; son articulation avec la garde du bouton de l'ordre de 0,5 s (DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement ») est à fixer en architecture. Ce que fait le drone quand cette durée maximale est dépassée n'a pas été répondu : voir DOU-093 « Dépassement de la durée maximale de la phase Lancé : que fait le drone ? ».
**Alternatives écartées :** chien de garde limité à « En vol » et « Vol de réglage » ; phase « Lancé » sans durée maximale.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-075 « Le chien de garde couvre-t-il la phase Lancé, et cette phase a-t-elle une durée maximale ? » ; ouvre DOU-093 « Dépassement de la durée maximale de la phase Lancé : que fait le drone ? »
**Précise :** DEC-065 « Logiciel bloqué en vol : coupure des moteurs par un chien de garde » et DEC-062 « Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs ».
**Précisée par :** DEC-103 « Phase Lancé trop longue : coupure et redémarrage par le chien de garde, sans nouvel état ni signal » le 2026-10-28 (dépassement de la durée maximale de la phase Lancé : coupure et redémarrage par le chien de garde)

### DEC-097 — Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé
**Date :** 2026-10-28
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol »
**Décision :** Pendant un redémarrage ou une chute de tension, y compris pendant la phase « Lancé », les moteurs s'arrêtent et le drone est verrouillé : même état que « Allumé, en attente d'un appui » (DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »), sans jamais reprendre le vol seul (DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement »). La coupure d'alimentation en phase « Lancé » mène donc à « Éteint, moteurs arrêtés », puis au redémarrage selon DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation ». Hypothèse à valider par l'architecture matérielle : l'alimentation des moteurs doit garantir leur arrêt lors d'un redémarrage ou d'une chute de tension.
**Alternatives écartées :** état « À définir » pour la coupure en phase « Lancé » dans les diagrammes.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-060 « Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle » en partie (état des moteurs pendant un redémarrage ou une chute de tension, coupure en phase « Lancé ») ; reste ouvert : la coupure de la batterie dans chaque état, et la validation matérielle
**Précise :** DEC-061 « Redémarrage immobile au sol : allumé mais jamais armé » et DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard ».
**Précisée par :** DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre » le 2026-10-28 (la sous-tension de la batterie est une cause de coupure d'alimentation sans signal propre : SCN-012 « Dégradé : sous-tension de la batterie »).

### DEC-098 — Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation
**Date :** 2026-10-28
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol » et SCN-010 « Échec : initialisation impossible au démarrage »
**Décision :** Après une coupure d'alimentation en vol, le drone redémarre « Allumé, en attente d'un appui », jamais armé, seulement s'il est immobile et à plat. Sinon (en mouvement, ou immobile mais pas à plat, par exemple tombé sur la tranche ou retourné), l'initialisation échoue avec le signal « Échec d'initialisation », définitif jusqu'au débranchement de la batterie (DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie »). La condition « à plat » de DEC-067 « Démarrage à plat exigé, sinon échec de l'initialisation avec signal » vaut donc aussi au redémarrage après une coupure en vol.
**Alternatives écartées :** « Allumé » dès que le drone est immobile, sans condition à plat (lecture littérale de DEC-061 « Redémarrage immobile au sol : allumé mais jamais armé »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 : d'abord « Échec d'initialisation » à l'option sur la tranche, puis confirmation de « immobile et à plat » après rappel de la précision de DEC-061 « Redémarrage immobile au sol : allumé mais jamais armé ».
**Doutes levés :** DOU-074 « Une initialisation en échec est-elle définitive jusqu'au débranchement, et la condition à plat vaut-elle aussi après une coupure en vol ? » (seconde partie ; la première l'avait été par DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie »)
**Précise :** DEC-061 « Redémarrage immobile au sol : allumé mais jamais armé » et DEC-067 « Démarrage à plat exigé, sinon échec de l'initialisation avec signal ».

### DEC-099 — Un statut sans fil distinct par état, effets locaux regroupables par catégorie
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Chaque état du drone reste distinct et chaque état a un statut sans fil distinct. Les effets visuels et sonores locaux peuvent, eux, être regroupés par catégorie, pour la praticité ; la liste des effets locaux est à définir en architecture. Un signal du tableau de `00-scenarios.md` est donc un événement distinct (donc un statut sans fil distinct), et non forcément un effet local distinct ; le tableau garde 17 événements. Cela s'accorde avec DEC-091 « Un seul signal Refus pour tout refus, armement ou mode réglage » (un seul effet Refus, la cause étant donnée par le statut sans fil).
**Alternatives écartées :** un effet local distinct pour chaque événement (lecture littérale de DEC-005 « Un signal distinct pour chaque information ») ; un effet par catégorie seulement, sans statut sans fil distinct par état.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-027 « Un signal distinct par information, ou par catégorie ? » ; la persistance de l'effet de la cause d'une coupure n'a pas été répondue, elle est reprise dans DOU-094 « Signal de la cause d'une coupure : combien de temps persiste-t-il après le retour à l'attente ? »
**Précise :** DEC-005 « Un signal distinct pour chaque information ». Points de vocabulaire nommés sans être tranchés : DEC-033 « Signal Arrêt sans fil distinct du signal Arrêt par le bouton » et DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé » parlent d'un signal distinct, à lire comme un événement et un statut sans fil distincts, l'effet local restant regroupable ; les écarts de forme de DEC-084 « Appui ignoré pendant une série d'appuis : aucun signal, risque accepté et documenté » et de DEC-088 « Bouton coincé ou maintenu en permanence au démarrage : statut sans fil seulement, aucun signal local » (information sans effet local) restent inchangés.
**Précisée par :** DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil » le 2026-10-28 (le signal local de la cause d'une coupure ne persiste pas)

### DEC-100 — Issues du vol de réglage : signaux du vol normal réutilisés, signal du lien perdu à définir
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Les issues d'un vol de réglage réutilisent les signaux du vol normal : posé (signal « Posé »), arrêt par le bouton (signal « Arrêt par le bouton »), arrêt sans fil (signal « Arrêt sans fil »), échec de stabilisation (signal « Échec de stabilisation »), basculement (signal « Basculement »), délai de 15 s dépassé (signal « Délai de descente dépassé »). Le lien perdu a un signal propre ou passe par le statut sans fil, à définir en architecture. Le tableau des signaux garde 17 événements.
**Alternatives écartées :** signaux propres au vol de réglage pour chaque issue.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-053 « Vols de réglage : signaux des phases, signal du lien perdu, acquittement des commandes » en partie (signaux des issues) ; reste ouvert : signaux des phases du vol de réglage, signal du lien perdu (avec le délai de DOU-036 « Après quel délai le lien sans fil est-il considéré comme perdu ? »), acquittement des commandes, relation entre l'atterrissage sur lien perdu et le délai de 15 s
**Précise :** DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage » (signal donné) et DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu ».
**Modifiée par :** DEC-106 « Lien sans fil perdu en vol de réglage : aucune action particulière » le 2026-10-28 (le lien perdu n'est plus une issue du vol de réglage ; le titre n'est pas réécrit)
**Précisée par :** DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement » le 2026-10-28 (signaux des phases du vol de réglage)

### DEC-101 — Statut sans fil d'un refus : cause précise, liste exacte à fixer en architecture
**Date :** 2026-10-28
**Concerne :** SCN-003 « Échec : batterie faible à l'armement » et SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Le statut sans fil donne la cause précise d'un refus (batterie faible, drone en mouvement, drone pas à plat, bouton maintenu au démarrage, etc.) pour l'armement refusé, le mode réglage refusé et le décollage de réglage refusé. La liste exacte des causes est à fixer en architecture.
**Alternatives écartées :** statut sans fil générique, sans cause.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-083 « Contenu du statut sans fil d'un armement ou d'un décollage refusé » ; hors de la réponse, repris dans DOU-092 « Décollage de réglage refusé : quel signal local, et combien de temps le statut de refus est-il conservé ? » : le signal local du décollage refusé et la durée de conservation du statut
**Précise :** DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone », DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus », DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre » et DEC-088 « Bouton coincé ou maintenu en permanence au démarrage : statut sans fil seulement, aucun signal local ».
**Précisée par :** DEC-102 « Décollage de réglage refusé : signal Refus, statut de refus lisible jusqu'à la commande suivante » le 2026-10-28 (signal local et conservation du statut du décollage refusé) ; DEC-110 « Armement refusé à 2 secondes d'appui : tous les tests faits, un seul signal Refus, sans attente de l'immobilité » le 2026-10-28 (causes listées pour l'armement refusé)
**Modifiée par :** DEC-179 « Simplification n°6 adoptée : statut sans fil par code d'état et dernières causes » le 2026-10-29 (trois causes de refus fixes sur le statut sans fil)

### DEC-102 — Décollage de réglage refusé : signal Refus, statut de refus lisible jusqu'à la commande suivante
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Un décollage de réglage refusé (batterie insuffisante : DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre ») donne le même signal « Refus » que les autres refus (DEC-091 « Un seul signal Refus pour tout refus, armement ou mode réglage »). Le statut de refus reste lisible sur le sans fil jusqu'à la commande suivante ; la durée exacte est à fixer en architecture. Points nommés sans être tranchés : la réponse porte sur le décollage de réglage refusé ; son extension aux refus d'armement et de mode réglage (où la « commande suivante » n'est pas une commande sans fil) n'a pas été répondue, et la durée exacte est reportée avec les autres valeurs à fixer en architecture (DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture »).
**Alternatives écartées :** un autre signal local pour le décollage refusé ; aucun signal local.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-092 « Décollage de réglage refusé : quel signal local, et combien de temps le statut de refus est-il conservé ? »
**Précise :** DEC-091 « Un seul signal Refus pour tout refus, armement ou mode réglage » et DEC-101 « Statut sans fil d'un refus : cause précise, liste exacte à fixer en architecture ».
**Modifiée par :** DEC-179 « Simplification n°6 adoptée : statut sans fil par code d'état et dernières causes » le 2026-10-29 (dernière cause de refus conservée jusqu'à la mise hors tension)

### DEC-103 — Phase Lancé trop longue : coupure et redémarrage par le chien de garde, sans nouvel état ni signal
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol » et SCN-011 « Dégradé : coupure d'alimentation en vol »
**Décision :** Si la phase « Lancé » dépasse sa durée maximale sans démarrage des moteurs (DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale »), le chien de garde coupe et redémarre le drone comme pour un logiciel bloqué (DEC-065 « Logiciel bloqué en vol : coupure des moteurs par un chien de garde »), puis le redémarrage suit DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation ». Aucun nouvel état ni nouveau signal : le drone donne ensuite le signal « Allumé » ou « Échec d'initialisation », déjà existants.
**Alternatives écartées :** retour à l'attente sans redémarrage, avec un signal ; nouvel état dédié.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-093 « Dépassement de la durée maximale de la phase Lancé : que fait le drone ? »
**Précise :** DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale ».
**Précisée par :** DEC-136 « Écriture de réglages commencée à l'état Allumé et encore en cours au relâchement du lancer : risque accepté » le 2026-10-28 (une écriture de réglages encore en cours au relâchement du lancer peut dépasser la durée maximale de la phase Lancé : coupure et redémarrage par le chien de garde, risque accepté).

### DEC-104 — Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** Après une coupure en vol, le signal local de la cause (Échec de stabilisation, Arrêt par le bouton, Arrêt sans fil, Basculement, Délai de descente dépassé) ne persiste pas : le signal « Allumé » prend le relais tout de suite, à l'entrée dans l'état verrouillé (DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »). La cause est conservée dans le statut sans fil distinct par état (DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie »). Conséquence : sans appareil de suivi, l'utilisateur qui ramasse le drone ne connaît pas la cause de la chute, risque accepté à documenter dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »). Tensions nommées sans être tranchées : (1) DEC-033 « Signal Arrêt sans fil distinct du signal Arrêt par le bouton » et DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé » parlent d'un signal distinct, à lire comme un événement et un statut sans fil distincts (voir DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie »), mais l'effet local de la cause est écrasé par « Allumé » ; la durée perceptible de l'effet de la cause avant ce relais est à fixer en architecture (DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture ») ; (2) les résultats attendus de SCN-002 « Échec : stationnaire non atteint dans le délai », SCN-006 « Échec : inclinaison excessive après le stationnaire » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol » (« l'utilisateur sait que… ») ne valent plus, après les premiers instants, qu'avec un appareil de suivi ; (3) le signal « Posé » (fin nominale) n'est pas concerné par cette réponse, sa persistance n'a pas été posée.
**Alternatives écartées :** effet local de la cause conservé pendant une durée fixée ; « Allumé » retardé jusqu'à la fin de l'effet de la cause.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-094 « Signal de la cause d'une coupure : combien de temps persiste-t-il après le retour à l'attente ? »
**Précise :** DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie ».
**Confirmée et précisée par :** DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté » le 2026-10-28 (confirmée telle quelle ; les tensions nommées ci-dessus sont assumées par l'utilisateur).
**Précisée par (suite) :** DEC-118 « Signal Allumé au retour à l'attente après un posé, un refus ou un désarmement » le 2026-10-28 (même logique de relais du signal « Allumé » après un posé, un refus et un désarmement).

### DEC-105 — Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-010 « Échec : initialisation impossible au démarrage »
**Décision :** Pendant l'initialisation et après un échec d'initialisation, les commandes sans fil « Modifier » et « Sauvegarder » sont acceptées ; « Décoller » et « Arrêt » sont ignorées (commandes de vol). Ces deux lignes complètent la table de DEC-043 « Commandes sans fil acceptées selon l'état du drone » (ajoutées au tableau de `00-scenarios.md`). Risque accepté, à documenter dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? ») et à traiter en architecture : écrire des réglages sur un drone non initialisé. Point nommé sans être tranché : pendant l'initialisation en cours, les réglages enregistrés ne sont peut-être pas encore chargés (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage ») ; une commande « Sauvegarder » à ce moment pourrait enregistrer des valeurs incomplètes ou d'origine à la place des réglages sauvegardés. Cohérent avec DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque » (écriture en mémoire non volatile acceptée hors vol).
**Alternatives écartées :** toutes les commandes ignorées dans ces états ; Modifier seule acceptée.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-078 « Initialisation en cours et échec d'initialisation : quelles commandes sans fil sont acceptées ? »
**Précise :** DEC-043 « Commandes sans fil acceptées selon l'état du drone » et DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque ».
**Modifiée par :** DEC-120 « Sauvegarder ignorée pendant l'initialisation en cours, Modifier acceptée ; cas de l'échec d'initialisation non tranché » le 2026-10-28 (état « Initialisation en cours » : Sauvegarder devient ignorée, Modifier reste acceptée ; l'état « Échec d'initialisation » est inchangé, sa question reste dans DOU-098 « Commande Sauvegarder après un échec d'initialisation : acceptée ou ignorée » ; le titre est conservé). ; DEC-178 « Simplification n°5 adoptée : échec d'initialisation, toutes les commandes sans fil ignorées » le 2026-10-29 (Modifier et Sauvegarder ignorées en échec d'initialisation)
**Précisée par :** DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté » le 2026-10-28 (état « Échec d'initialisation » : Modifier et Sauvegarder acceptées confirmées, la question de DOU-098 « Commande Sauvegarder après un échec d'initialisation : acceptée ou ignorée » est tranchée).

### DEC-106 — Lien sans fil perdu en vol de réglage : aucune action particulière
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** En vol de réglage, il n'y a aucune action particulière si le lien sans fil est perdu : le vol de réglage suit son cours (stationnaire de 3 secondes, atterrissage, coupure des moteurs au plus 15 secondes après le décollage). Il n'y a donc plus d'atterrissage sur place sur lien perdu, plus de signal du lien perdu et plus de délai de perte du lien ; l'état « Atterrissage sur place » est retiré du diagramme c de `00-scenarios.md`, de SCN-009 « Réglage et suivi du drone par le sans fil », des légendes, des signaux et du glossaire. Cette décision **modifie** DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu » (seule la phrase sur le lien perdu change ; son titre est conservé) et DEC-100 « Issues du vol de réglage : signaux du vol normal réutilisés, signal du lien perdu à définir » (le lien perdu n'est plus une issue ; son titre est conservé). Écarts nommés sans être tranchés : (1) le titre de DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu » et celui de DEC-100 « Issues du vol de réglage : signaux du vol normal réutilisés, signal du lien perdu à définir » parlent encore du lien perdu, ils ne sont pas réécrits ; (2) l'alternative « poursuite du vol si le lien est perdu », écartée dans DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu », est de fait adoptée ; (3) la raison de DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage » dit qu'elle confirme la décision sur le vol de réglage « telle qu'écrite » : c'est exact à sa date, la modification est postérieure ; (4) DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol », DEC-032 « Vol libre : le drone vole sans appareil de suivi » et DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée » ne disent rien du lien perdu en vol de réglage : aucun écart ; (5) le garde-fou reste la coupure des moteurs au plus 15 secondes après le décollage, et l'arrêt sans fil devient impossible si le lien est perdu, seul le bouton arrête alors le drone (risque à documenter dans les limites d'emploi, DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »).
**Alternatives écartées :** atterrissage sur place sur lien perdu (DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu » telle qu'écrite) ; coupure des moteurs sur lien perdu.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28. L'utilisateur l'a d'abord dit, puis confirmé « Oui, aucune action spéciale » après rappel de la contradiction avec DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu » et DEC-100 « Issues du vol de réglage : signaux du vol normal réutilisés, signal du lien perdu à définir ».
**Doutes levés :** DOU-036 « Après quel délai le lien sans fil est-il considéré comme perdu ? » (sans objet : plus de délai de perte du lien) ; élimine aussi les points (b), (d) et (e) de DOU-053 « Vols de réglage : signaux des phases, signal du lien perdu, acquittement des commandes »
**Modifie :** DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu » et DEC-100 « Issues du vol de réglage : signaux du vol normal réutilisés, signal du lien perdu à définir ».

### DEC-107 — Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** (a) Les signaux des phases du vol de réglage (stabilisation, vol stationnaire, atterrissage) sont ceux du vol normal, comme ses issues (DEC-100 « Issues du vol de réglage : signaux du vol normal réutilisés, signal du lien perdu à définir »). (c) Le drone acquitte les commandes sans fil (Décoller, Arrêt, Modifier, Sauvegarder) par le statut sans fil seulement (état et valeur relue, comme DEC-068 « Seuil hors bornes : refus silencieux, valeur relue sur l'appareil de suivi »), sans signal local supplémentaire. Les points (b), (d) et (e) de DOU-053 « Vols de réglage : signaux des phases, signal du lien perdu, acquittement des commandes » sont sans objet, le lien perdu n'ayant plus d'effet (DEC-106 « Lien sans fil perdu en vol de réglage : aucune action particulière »). Points nommés sans être tranchés : le signal « Lancé » n'a pas d'équivalent en vol de réglage (pas de lancer au relâchement) ; un décollage de réglage refusé reste signalé par « Refus » (DEC-102 « Décollage de réglage refusé : signal Refus, statut de refus lisible jusqu'à la commande suivante »), seule exception à l'absence de signal local d'acquittement ; la seconde moitié de (d), dire si le délai de 15 secondes après le décollage est le délai de descente réglable de DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel », est reportée en architecture (DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture »).
**Alternatives écartées :** signaux propres aux phases du vol de réglage ; signal local d'acquittement de chaque commande.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-053 « Vols de réglage : signaux des phases, signal du lien perdu, acquittement des commandes »
**Précise :** DEC-100 « Issues du vol de réglage : signaux du vol normal réutilisés, signal du lien perdu à définir » et DEC-068 « Seuil hors bornes : refus silencieux, valeur relue sur l'appareil de suivi ».

### DEC-108 — Vols de réglage répétés : aucune limite de nombre ni contrôle de chauffe, risque accepté
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Il n'y a ni limite du nombre de vols de réglage ni contrôle de chauffe entre deux vols de réglage. La batterie est vérifiée à chaque décollage de réglage (DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre »). Risque accepté (chauffe des moteurs, de l'électronique et de la batterie en vols répétés) et documenté dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »). Point nommé sans être tranché : le seuil de batterie du décollage de réglage (le même que celui de l'armement, DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » ?) n'a pas été répondu, il est fixé en architecture avec les autres seuils (DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture »).
**Alternatives écartées :** limite du nombre de vols ; contrôle de la chauffe ; délai minimal entre deux vols de réglage.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-039 « La batterie est-elle vérifiée à chaque décollage de réglage ? »
**Précise :** DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre ».

### DEC-109 — Lancer hors plage ou hauteur non mesurable : échec de stabilisation, limite d'emploi
**Date :** 2026-10-28
**Concerne :** SCN-002 « Échec : stationnaire non atteint dans le délai »
**Décision :** Un lancer hors plage (DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol ») ou une hauteur impossible à mesurer (sol non réfléchissant, vitre, escalier) donne un échec de stabilisation : même signal « Échec de stabilisation » et même coupure que SCN-002 « Échec : stationnaire non atteint dans le délai », sans signal ni comportement propre. Le drone ne distingue pas ces cas d'un défaut du drone. Limite d'emploi à documenter (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »). Suite logique des décisions existantes, nommée sans décision nouvelle : sans hauteur mesurée, le stationnaire n'est jamais déclaré (DEC-049 « Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale ») ; à l'atterrissage, sans hauteur mesurée le passage sous 2 à 3 cm n'est pas détecté et le signal est « Délai de descente dépassé » après 15 s (DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé ») ; la défaillance d'un capteur reste hors périmètre (DEC-060 « Défaillance d'un capteur ou d'un moteur en vol : hors périmètre »).
**Alternatives écartées :** signal ou comportement propre au lancer hors plage ; détection de l'impossibilité de mesurer la hauteur avec un signal dédié.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-021 « Que se passe-t-il pour un lancer hors plage ? »
**Précise :** DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » et DEC-049 « Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale ».

### DEC-110 — Armement refusé à 2 secondes d'appui : tous les tests faits, un seul signal Refus, sans attente de l'immobilité
**Date :** 2026-10-28
**Concerne :** SCN-003 « Échec : batterie faible à l'armement » et SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Si l'appui de 2 secondes a lieu sur un drone en mouvement, pas à plat ou à batterie faible, tous les tests sont faits à 2 secondes et le drone donne un seul signal « Refus » (DEC-091 « Un seul signal Refus pour tout refus, armement ou mode réglage »). Le statut sans fil liste les causes constatées (DEC-101 « Statut sans fil d'un refus : cause précise, liste exacte à fixer en architecture »). L'ordre des tests n'a pas d'importance pour l'utilisateur. Le drone n'attend pas l'immobilité. Reste à fixer en architecture : la tolérance de mouvement (vitesse, rotation) de « immobile », fusionnée dans DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture ».
**Alternatives écartées :** attente de l'immobilité avant de refuser ; refus au premier test échoué, sans lister les autres causes.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-073 « Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ? » pour ce qui est répondu ; le reste (tolérance de « immobile ») est fusionné dans DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture »
**Précise :** DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone » et DEC-056 « Armement : drone immobile, sans autotest ».

### DEC-111 — Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter
**Date :** 2026-10-28
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Décision :** La batterie et la programmation sont hors périmètre des scénarios : ce sont des limites d'emploi, documentées dans la notice. Le drone ne gère rien de la batterie (charge, remplacement, stockage, drone laissé allumé) ni des cas d'échec de la programmation (programmation interrompue, hélices démontées, essai des moteurs avant le premier vol). Il n'y a donc pas de douzième scénario et aucun cas n'est ajouté à SCN-008 « Mise en service : programmation du drone ». Limites d'emploi reportées dans DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? » et dans la liste des risques de `reprise.md` : (a) la charge et le stockage de la batterie lithium relèvent de l'utilisateur ; (b) un drone laissé allumé (« Allumé, en attente d'un appui ») décharge la batterie, avec un risque de décharge profonde pour une batterie lithium ; (c) les hélices sont à démonter pendant la programmation, et l'essai des moteurs avant le premier vol n'est pas couvert. Conséquence de méthode (règle de la phase 0 : chaque besoin cite au moins un scénario amont) : aucun besoin ne pourra porter sur la gestion de la batterie (charge, remplacement, stockage, drone laissé allumé) ni sur les cas d'échec de la programmation. Restent en périmètre, car décrites par des scénarios, la vérification de la batterie à l'armement et au décollage de réglage (DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » ; DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre » ; SCN-003 « Échec : batterie faible à l'armement »). Points nommés sans être tranchés : (1) la question « signal de batterie faible hors armement » de DOU-048 « Batterie : charge, remplacement, drone laissé allumé » reçoit la réponse « aucune gestion de la batterie par le drone », cohérente avec DEC-013 « Pas de contrôle de la batterie en vol » ; (2) la reprogrammation et le contrôle de version, cités dans DOU-049 « Programmation : cas d'échec, hélices démontées, essai des moteurs avant le premier vol », ne sont pas nommés dans la réponse : lecture de l'architecte, hors périmètre au même titre, à confirmer à la porte « scénarios » ; (3) le calibrage éventuel reste renvoyé à l'architecture (DEC-026 « Mise en service : calibrage éventuel renvoyé à l'architecture, réglage du vol par un scénario dédié »).
**Alternatives écartées :** un scénario dédié à la maintenance de la batterie (charge, remplacement, stockage, drone laissé allumé) ; des cas d'échec de la programmation ajoutés à SCN-008 « Mise en service : programmation du drone ».
**Raison :** réponse de l'utilisateur en chat, 2026-10-28. Après explication de l'intérêt d'un scénario dédié à la batterie, l'utilisateur a choisi l'option « hors périmètre, limite d'emploi ».
**Doutes levés :** DOU-048 « Batterie : charge, remplacement, drone laissé allumé » ; DOU-049 « Programmation : cas d'échec, hélices démontées, essai des moteurs avant le premier vol »
**Précise :** DEC-024 « Mise en service par programmation avec un programmateur ST-LINK ».
**Précisée par :** DEC-125 « Limites d'emploi informées par une notice écrite à la phase besoins, le drone n'affiche rien » le 2026-10-28 (les limites d'emploi sont informées par une notice écrite à la phase besoins).
**Modifiée par :** DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre » le 2026-10-28 (la protection matérielle de sous-tension de la batterie devient le scénario SCN-012 « Dégradé : sous-tension de la batterie » ; la phrase « il n'y a donc pas de douzième scénario » et la conséquence « aucun besoin sur la gestion de la batterie » ne valent plus pour cette protection seule ; charge, remplacement, stockage, drone laissé allumé et programmation restent hors périmètre ; le titre est conservé).
**Modifiée par (suite) :** DEC-133 « SCN-012 inclut le drone laissé allumé en attente d'un appui : sous-tension dans le périmètre » le 2026-10-28 (le drone laissé allumé en attente d'un appui n'est plus hors périmètre : sa sous-tension est décrite par SCN-012 « Dégradé : sous-tension de la batterie » et un besoin pourra citer SCN-012 « Dégradé : sous-tension de la batterie » pour ce cas ; charge, remplacement, stockage et programmation restent hors périmètre ; le titre est conservé).

### DEC-112 — Sauvegarder ignorée à l'état armé, avant le lancer
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** La commande sans fil « Sauvegarder » est ignorée à l'état « Armé, avant le lancer » : aucune écriture en mémoire non volatile, aucun effet. Les autres cases du tableau de DEC-043 « Commandes sans fil acceptées selon l'état du drone » sont inchangées (Modifier reste acceptée à l'état armé ; Sauvegarder reste acceptée en attente d'un appui, en mode réglage, pendant l'initialisation et après un échec d'initialisation, ignorée en vol et en phase « Lancé »). Raison technique rappelée à l'utilisateur : une écriture longue pendant le lancer peut dépasser la durée maximale de la phase « Lancé » et provoquer, par le chien de garde, une coupure puis un redémarrage en l'air (DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale » ; DEC-103 « Phase Lancé trop longue : coupure et redémarrage par le chien de garde, sans nouvel état ni signal »). Le risque de retard du lancer par une écriture, accepté dans DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque », disparaît pour l'état armé. Contradiction nommée : l'utilisateur avait répondu « acceptée comme aujourd'hui » (DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque »), puis, après rappel de l'interaction avec le chien de garde, il a changé sa réponse ; cette décision **modifie** DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque » (son alternative écartée « ignorer Sauvegarder à l'état armé » est de fait adoptée) et la ligne « Armé, avant le lancer » de DEC-043 « Commandes sans fil acceptées selon l'état du drone ». Points nommés sans être tranchés : (1) une écriture commencée avant l'armement (état « Allumé ») et encore en cours au relâchement n'est pas traitée ici, reportée dans DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite » ; (2) la commande ignorée n'a pas de signal local et son acquittement ne passe que par le statut sans fil (DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement ») : l'utilisateur qui envoie Sauvegarder pendant l'armement doit relire le statut, limite d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? ») ; (3) la dernière phrase de DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » (sa mention de cohérence avec la décision sur Sauvegarder à l'état armé) n'est plus exacte pour l'état armé ; cette décision n'est pas réécrite. DOU-098 « Commande Sauvegarder après un échec d'initialisation : acceptée ou ignorée » reste ouvert.
**Alternatives écartées :** Sauvegarder acceptée à l'état armé, comme dans DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque » (risque de retard du lancer et de coupure par le chien de garde en l'air).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28, après rappel de l'interaction avec le chien de garde de DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale » et de DEC-103 « Phase Lancé trop longue : coupure et redémarrage par le chien de garde, sans nouvel état ni signal ».
**Doutes levés :** DOU-095 « Commande Sauvegarder à l'état armé : écriture en mémoire non volatile et durée maximale de la phase Lancé »
**Modifie :** DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque » et DEC-043 « Commandes sans fil acceptées selon l'état du drone » (ligne « Armé, avant le lancer »).
**Étendue par :** DEC-123 « Sauvegarder ignorée aussi à l'état Premier appui validé » le 2026-10-28 (Sauvegarder est aussi ignorée à l'état « Premier appui validé »).
**Étendue par (suite) :** DEC-128 « Sauvegarder ignorée aussi à l'état Série d'appuis en cours » le 2026-10-28 (Sauvegarder est aussi ignorée à l'état « Série d'appuis en cours »).

### DEC-113 — Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté
**Date :** 2026-10-28
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil » est confirmée telle quelle : après une coupure en vol, « Allumé » prend le relais tout de suite, sans durée minimale d'effet de la cause ; le drone signale la coupure, puis la cause ne se lit plus que sur le statut sans fil (DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie »). Risque accepté et documenté dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? ») : un utilisateur sans appareil de suivi n'est pas informé de la cause d'une coupure. Précision : les « signaux distincts » de DEC-033 « Signal Arrêt sans fil distinct du signal Arrêt par le bouton », DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé » et DEC-005 « Un signal distinct pour chaque information » s'entendent comme des événements et des statuts sans fil distincts ; la distinction locale des causes n'est pas garantie perceptible. Points nommés sans être tranchés : (1) la raison de DEC-005 « Un signal distinct pour chaque information » (« l'utilisateur doit toujours savoir de quoi il s'agit ») n'est plus tenue pour la cause d'une coupure sans appareil de suivi : écart assumé par l'utilisateur ; (2) la durée perceptible de la cause avant le relais d'« Allumé » disparaît de DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » ; (3) vérifiabilité : en test, le signal de la cause se vérifie à son émission (événement et statut sans fil), pas à sa perception ; à reprendre en exigences. Les scénarios SCN-002 « Échec : stationnaire non atteint dans le délai », SCN-006 « Échec : inclinaison excessive après le stationnaire » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol » sont alignés (« le drone signale la coupure ; la cause se lit sur le statut sans fil »).
**Alternatives écartées :** durée minimale d'effet de la cause avant le relais d'« Allumé » ; « Allumé » retardé jusqu'à la fin de l'effet de la cause (déjà écartées dans DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 (confirmation de DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil »).
**Doutes levés :** DOU-096 « Durée minimale perceptible du signal de cause d'une coupure en vol »
**Précise :** DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil », DEC-033 « Signal Arrêt sans fil distinct du signal Arrêt par le bouton », DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé » et DEC-005 « Un signal distinct pour chaque information ».
**Précisée par :** DEC-118 « Signal Allumé au retour à l'attente après un posé, un refus ou un désarmement » le 2026-10-28 (le relais immédiat du signal « Allumé » vaut aussi après un posé, un refus et un désarmement).
**Modifiée par :** DEC-176 « Simplification n°3 adoptée : dix effets locaux au lieu de dix-sept signaux » le 2026-10-29 (l'effet de la coupure dure au moins 0,5 s)

### DEC-114 — Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-002 « Échec : stationnaire non atteint dans le délai »
**Décision :** Jalon : DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » est à lever **avant la phase « besoins »** (et non seulement avant les exigences). Avant de rédiger les besoins, une analyse de faisabilité est faite (mesure de la vitesse horizontale, stationnaire en 2 s après le démarrage des moteurs, lancer à l'envers depuis 1,5 m) et la plage de lancer de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » est revue (hauteur minimale, vitesse). La même échéance « avant les besoins » vaut pour DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal » et, pour la part qui conditionne la faisabilité des scénarios (tolérance de « immobile », plage de lancer), pour DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » ; le reste de DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » reste à fixer en architecture. SCN-001 « Vol nominal : de la batterie au posé » et SCN-002 « Échec : stationnaire non atteint dans le délai » gardent les valeurs de la plage de lancer comme provisoires (DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences »). Points nommés sans être tranchés : (1) l'échéance de DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences » (« avant les exigences ») est avancée à « avant les besoins » pour la plage de lancer et le stationnaire de 2 s ; son titre n'est pas réécrit ; (2) DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » reste non bloquant pour la porte « scénarios » (l'utilisateur veut le lever avant les besoins, pas avant cette porte) : l'architecte n'ouvre pas la phase « besoins » tant qu'il est ouvert ; rendre ce jalon bloquant dans l'outil de porte est une question posée à l'utilisateur ; (3) la portée exacte de l'échéance pour DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » (lecture ci-dessus) est à confirmer.
**Alternatives écartées :** lever DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » seulement avant les exigences ; garder la plage de lancer telle quelle sans analyse.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun) ; échéance « avant les besoins » fixée pour DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m », DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » (en partie) et DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal »
**Précise :** DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences » et DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol ».
**Précisée par :** DEC-122 « Jalon avant les besoins : promesse de l'architecte, sans modification de l'outil de porte » le 2026-10-28 (le jalon reste une promesse de l'architecte, sans modification de l'outil de porte).
**Modifiée par :** DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée » et DEC-138 « Tolérance d'immobile et part de DOU-058 liée à la faisabilité : jalon déplacé aux essais » le 2026-10-28 (jalon « avant les besoins » abandonné, validation par essais sur prototype).

### DEC-115 — Troisième appui encore maintenu à l'entrée en mode réglage : maintien ignoré jusqu'au premier relâchement
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Si le bouton est encore enfoncé quand le 3e appui est validé (entrée en mode réglage), le maintien est ignoré jusqu'au premier relâchement, comme pour un bouton déjà enfoncé (DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement »). Ce maintien ne peut ni armer (le bouton n'arme jamais en mode réglage : DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »), ni déclencher d'arrêt d'urgence si une commande Décoller arrive avant le relâchement (DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage » ; DEC-094 « Bouton appuyé après un décollage de réglage : pris en compte tout de suite, sans garde »). Seul un nouvel appui, après le premier relâchement, peut ensuite couper les moteurs en vol de réglage. Cas voisin traité pour un refus : DEC-093 « Mode réglage refusé : retour à l'attente, compteur à zéro, bouton encore enfoncé ignoré ».
**Alternatives écartées :** maintien pris en compte tout de suite (une commande Décoller reçue avant le relâchement aurait coupé les moteurs aussitôt).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-097 « Bouton encore maintenu à l'entrée en mode réglage (3e appui) »
**Précise :** DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement » et DEC-085 « Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé ».

### DEC-116 — Bouton en mode réglage, moteurs coupés : aucun effet et aucun signal, il ne sert qu'en vol de réglage
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Dans l'état « Mode réglage, moteurs coupés » (au sol), le bouton n'a aucun effet et ne donne aucun signal : pas de signal « Appui validé » à 1 s, aucun signal à 2 s ni à 10 s, aucun 4e appui compté, aucun maintien pris en compte. Le bouton ne sert plus, en mode réglage, qu'en vol de réglage, où il est l'arrêt d'urgence (DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage »). Points nommés sans être tranchés : (1) cette décision précise DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage », qui ne disait que « le bouton n'arme jamais » ; (2) le compteur d'appuis ne s'applique plus une fois le mode réglage atteint ; (3) au retour d'un vol de réglage, un bouton encore enfoncé reste sans effet puisqu'au sol il n'en a aucun (DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage »).
**Alternatives écartées :** appui validé et signal « Appui validé » en mode réglage ; signal à 2 s ou à 10 s ; 4e appui compté.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-105 « Bouton en mode réglage, moteurs coupés : comportement autre que ne jamais armer »
**Précise :** DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage » et DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage ».

### DEC-117 — Bouton en échec d'initialisation : ignoré pour toujours après le premier relâchement, aucun effet ni signal
**Date :** 2026-10-28
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-011 « Dégradé : coupure d'alimentation en vol »
**Décision :** À l'état « Échec d'initialisation », après un premier relâchement, le bouton est ignoré pour toujours : aucun effet, aucun signal (pas de signal « Refus » à 2 s d'appui). L'échec est définitif jusqu'au débranchement de la batterie (DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie »). Pendant « Initialisation en cours », le bouton enfoncé reste ignoré jusqu'au premier relâchement seulement (DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement »), puisque l'initialisation peut réussir. Cette décision lève l'écart entre la note du diagramme a de `00-scenarios.md` (ignoré jusqu'au premier relâchement) et SCN-010 « Échec : initialisation impossible au démarrage » et SCN-011 « Dégradé : coupure d'alimentation en vol » (le drone « ignore le bouton »).
**Alternatives écartées :** bouton ignoré seulement jusqu'au premier relâchement, puis pris en compte ; signal « Refus » à 2 s d'appui en échec d'initialisation.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-106 « Bouton en échec d'initialisation après un premier relâchement »
**Précise :** DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie » et DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement ».

### DEC-118 — Signal Allumé au retour à l'attente après un posé, un refus ou un désarmement
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé », SCN-003 « Échec : batterie faible à l'armement » et SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Décision :** Au retour à l'état « Allumé, en attente d'un appui » après un posé, un refus ou un désarmement, le drone donne le signal « Allumé » : il prend le relais après le signal de l'événement (« Posé », « Refus », « Désarmement »). C'est la même logique que pour une coupure en vol (DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté »). Les diagrammes a et b, le tableau des signaux et SCN-001 « Vol nominal : de la batterie au posé », SCN-003 « Échec : batterie faible à l'armement » et SCN-005 « Dégradé : bouton maintenu plus de 10 secondes » sont alignés. Points nommés sans être tranchés : (1) un refus du mode réglage au 3e appui revient aussi à l'attente (DEC-093 « Mode réglage refusé : retour à l'attente, compteur à zéro, bouton encore enfoncé ignoré ») : lecture de l'architecte, il donne aussi « Allumé » ; (2) un décollage de réglage refusé ne revient pas à l'attente (le drone reste en « Mode réglage, moteurs coupés ») : lecture de l'architecte, pas de signal « Allumé » ; (3) le signal « Allumé » est donné même si le bouton est encore enfoncé (appui ignoré jusqu'au premier relâchement : DEC-081 « Bouton encore enfoncé après un refus ou un désarmement : ignoré jusqu'au premier relâchement, puis nouvel appui possible tout de suite ») ; (4) la durée du signal de l'événement avant le relais d'« Allumé », et l'enchaînement perceptible, ne sont pas fixés par les scénarios (effets locaux à définir en architecture, DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture »).
**Alternatives écartées :** drone silencieux au retour à l'attente après un posé, un refus ou un désarmement.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-103 « Signal Allumé après Posé, Refus et Désarmement : donné au retour à l'attente ou silencieux ? »
**Précise :** DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil », DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté », DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté » et DEC-082 « Retours à l'attente après le posé ou une coupure des moteurs : compteur à zéro, appui en cours ni pris en compte ni compté ».

### DEC-119 — Appui bref pendant la garde du bouton, relâché avant la fin : risque accepté et documenté
**Date :** 2026-10-28
**Concerne :** SCN-002 « Échec : stationnaire non atteint dans le délai »
**Décision :** Un utilisateur qui relâche le bouton sans lancer, hélices tournantes en main, puis appuie brièvement et relâche avant la fin de la garde, n'obtient aucun effet : les hélices continuent de tourner. Ce risque est accepté et documenté. DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement » reste inchangée. Limite d'emploi à documenter : tenir le bouton jusqu'à la fin de la garde pour obtenir l'arrêt d'urgence. Risque cumulé avec DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer ».
**Alternatives écartées :** modifier DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement » pour mémoriser un appui bref pendant la garde.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-100 « Appui bref pendant la garde du bouton, relâché avant la fin, hélices tournantes en main »
**Précise :** DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement » et DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer ».

### DEC-120 — Sauvegarder ignorée pendant l'initialisation en cours, Modifier acceptée ; cas de l'échec d'initialisation non tranché
**Date :** 2026-10-28
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Tant que les réglages enregistrés ne sont pas chargés (état « Initialisation en cours »), la commande sans fil « Sauvegarder » est ignorée : elle ne peut plus écraser des réglages enregistrés non encore chargés. « Modifier » reste acceptée. Cette décision **modifie** DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » pour l'état « Initialisation en cours » seulement. **Non tranché :** pour l'état « Échec d'initialisation », Sauvegarder reste acceptée à ce jour (DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées », inchangée pour cet état), sans qu'il soit dit si les réglages sont alors chargés : la question reste dans DOU-098 « Commande Sauvegarder après un échec d'initialisation : acceptée ou ignorée », retitré. Points nommés sans être tranchés : (1) Sauvegarder est désormais ignorée à trois états sans vol (« Initialisation en cours » ici, « Premier appui validé » : DEC-123 « Sauvegarder ignorée aussi à l'état Premier appui validé », et « Armé » : DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer ») ; (2) la commande ignorée n'a pas de signal local, l'acquittement se lit sur le statut sans fil (DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement ») ; (3) la perte persistante de réglages n'est écartée que pour l'initialisation en cours : un risque subsiste après un échec d'initialisation si les réglages ne sont pas chargés.
**Alternatives écartées :** Sauvegarder acceptée pendant l'initialisation en cours, comme dans DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » (risque d'écraser des réglages non chargés).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-098 « Commande Sauvegarder après un échec d'initialisation : acceptée ou ignorée » en partie (initialisation en cours) ; reste ouvert : l'état « Échec d'initialisation »
**Modifie :** DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » (état « Initialisation en cours » seulement) et DEC-043 « Commandes sans fil acceptées selon l'état du drone » (ligne « Initialisation en cours »).
**Précisée par :** DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté » le 2026-10-28 (le cas de l'échec d'initialisation, resté non tranché, est tranché : Sauvegarder acceptée).

### DEC-121 — Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Le risque qu'un tiers à portée envoie des paramètres de vol aberrants, puis les sauvegarde, est accepté et documenté. Il découle de DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée », DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal », DEC-066 « Commande sans fil corrompue : aucun contrôle d'intégrité » et DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée ». Les réglages sauvegardés sont rechargés à chaque démarrage (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage ») : seule la reprogrammation du drone (SCN-008 « Mise en service : programmation du drone ») rétablit les valeurs d'origine. Limite d'emploi à inscrire dans « Risques acceptés » — `projets/boomrone/risques-acceptes.md`. Précision du tableau de DEC-043 « Commandes sans fil acceptées selon l'état du drone » : Modifier est acceptée en vol, Sauvegarder est ignorée en vol et acceptée au sol. Point nommé sans être tranché : il reste à vérifier en architecture que la reprogrammation efface bien la zone des réglages sauvegardés ; sinon elle ne rétablirait pas les valeurs d'origine.
**Alternatives écartées :** borner ou limiter les paramètres de vol ; ajouter une commande de retour aux valeurs d'origine (déjà écartée dans DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-099 « Paramètres de vol sans borne : modification en vol et sauvegarde par un tiers »
**Précise :** DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée », DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal », DEC-066 « Commande sans fil corrompue : aucun contrôle d'intégrité » et DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée ».
**Précisée par :** DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine » le 2026-10-28 (la reprogrammation réécrit la zone des réglages : DOU-110 « La reprogrammation efface-t-elle la zone des réglages sauvegardés ? » levé).

### DEC-122 — Jalon avant les besoins : promesse de l'architecte, sans modification de l'outil de porte
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le jalon de DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » (lever DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » et DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal » avant les besoins) reste une promesse de l'architecte, inscrite ici : l'architecte n'ouvre pas la phase « besoins » tant que ces deux doutes sont ouverts. L'outil `tools/check_traceability.py` n'est pas modifié ; ces doutes restent non bloquants pour la porte « scénarios ». Point nommé sans être tranché : aucun contrôle outillé ne retient l'architecte, la promesse repose sur sa seule discipline et sur la relecture de l'utilisateur.
**Alternatives écartées :** marquer ces doutes bloquants (ils bloqueraient la porte « scénarios », ce que l'utilisateur ne veut pas) ; ajouter à l'outil une option de phase ou une échéance par doute.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-104 « Jalon avant les besoins non contrôlé par l'outil de porte »
**Précise :** DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir ».
**Modifiée par :** DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée » et DEC-138 « Tolérance d'immobile et part de DOU-058 liée à la faisabilité : jalon déplacé aux essais » le 2026-10-28 (plus aucun doute n'a l'échéance « avant les besoins »).

### DEC-123 — Sauvegarder ignorée aussi à l'état Premier appui validé
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** La commande sans fil « Sauvegarder » est aussi ignorée à l'état « Premier appui validé » (bouton maintenu de 1 à 2 s, seul état d'où l'armement est possible : DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série »), comme à l'état armé (DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer »). Cette décision **étend** DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer » et modifie la ligne « Allumé, en attente d'un appui » du tableau de DEC-043 « Commandes sans fil acceptées selon l'état du drone » (le tableau de `00-scenarios.md` a désormais une ligne « Premier appui validé »). Points nommés sans être tranchés : (1) l'état « Série d'appuis en cours » n'est pas tranché : Sauvegarder y reste acceptée à ce jour (noté dans DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite ») ; (2) une écriture commencée à l'état « Allumé » et encore en cours à l'armement ou au relâchement reste à traiter en architecture (DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite ») ; (3) DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite » reste ouvert pour ses autres aspects (écriture en vol, coupure pendant l'écriture, mémoire jamais écrite).
**Alternatives écartées :** Sauvegarder acceptée à l'état « Premier appui validé » avec traitement de l'écriture en cours en architecture seulement.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun) ; répond à la question complémentaire de DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite », qui reste ouvert
**Étend :** DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer ».
**Modifie :** DEC-043 « Commandes sans fil acceptées selon l'état du drone » (état « Premier appui validé »).
**Étendue par :** DEC-128 « Sauvegarder ignorée aussi à l'état Série d'appuis en cours » le 2026-10-28 (l'état « Série d'appuis en cours », laissé non tranché, est tranché : Sauvegarder ignorée).

### DEC-124 — Registre consolidé des risques acceptés dans un fichier dédié
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Les risques acceptés sont consolidés dans un fichier dédié, « Risques acceptés » — `projets/boomrone/risques-acceptes.md` : un risque par ligne, avec son numéro, sa décision ou son doute d'origine (ID « titre »), son scénario et la limite d'emploi à documenter. Le fichier reprend les quinze risques de `reprise.md` et les risques acceptés du journal qui n'y figuraient pas (vol libre, mémoire corrompue, valeurs d'origine fixes, armement sans autotest, réglages sans borne, drone attrapé ou posé sur un obstacle, défaillance d'un capteur ou d'un moteur, choc, absence de contrôle de la batterie en vol, absence de coupure sur choc, commande corrompue, lancer hors plage, lieu inconnu du drone), plus l'appui bref pendant la garde (DEC-119 « Appui bref pendant la garde du bouton, relâché avant la fin : risque accepté et documenté ») et les paramètres aberrants (DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule »). Chaque décision d'origine y est citée avec son ID et son titre. `reprise.md` y renvoie au lieu de les lister. Point nommé sans être tranché : DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » est remplacée par DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » : elle n'est pas un risque en vigueur ; ne reste sans borne que ce que DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » laisse sans borne (réglages hors seuils de sécurité).
**Alternatives écartées :** liste maintenue dans `reprise.md` ; registre dans le journal des décisions.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-102 « Registre consolidé des risques acceptés »

### DEC-125 — Limites d'emploi informées par une notice écrite à la phase besoins, le drone n'affiche rien
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Les limites d'emploi sont portées à la connaissance de l'utilisateur par une notice, écrite à la phase « besoins », qui reprend « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (DEC-124 « Registre consolidé des risques acceptés dans un fichier dédié »). Le drone n'affiche rien lui-même, hors statut sans fil (ni étiquette sur le drone, ni signal dédié). Points nommés sans être tranchés : (1) la notice est un livrable documentaire ; si elle donne lieu à des besoins, leur scénario amont reste à choisir (règle de la phase 0 : chaque besoin cite au moins un scénario ; DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter ») ; (2) la plage de lancer et le lieu (DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » ; DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires » ; DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur » ; DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu ») relèvent de la notice, la plage de lancer pouvant changer après DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir ».
**Alternatives écartées :** étiquette sur le drone ; aucune information de l'utilisateur ; affichage de l'information par le drone lui-même.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »
**Précise :** DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter ».

### DEC-126 — Protection de sous-tension de la batterie : scénario court, coupure sans signal propre
**Date :** 2026-10-28
**Concerne :** SCN-012 « Dégradé : sous-tension de la batterie »
**Décision :** Un scénario court est créé pour la protection de sous-tension (décharge profonde) de la batterie : SCN-012 « Dégradé : sous-tension de la batterie ». En cas de sous-tension, le drone se coupe sans signal propre, comme pour une coupure d'alimentation : moteurs arrêtés, drone verrouillé (DEC-097 « Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé »), redémarrage selon DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation ». Aucun nouveau signal (le tableau reste à dix-sept signaux). Le seuil de sous-tension est une valeur à fixer en architecture (ajouté à DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture »). Cette décision **modifie** DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter » pour la seule protection matérielle de sous-tension (titre inchangé) : charge, remplacement, stockage, drone laissé allumé et programmation restent hors périmètre. **Contradiction nommée :** l'utilisateur avait d'abord proposé « contraintes hors scénario » ; après rappel de la règle « chaque besoin cite au moins un scénario » (`CLAUDE.md` §2), il a choisi « Non, un scénario court ». **Non couvertes, à voir en architecture, non traitées ici :** surintensité, inversion de polarité, surchauffe de la batterie ; la CEM n'est pas non plus traitée par cette décision, et le brown-out du microcontrôleur n'est couvert que par la chute de tension de DEC-097 « Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé » (lecture de l'architecte). **Tensions nommées sans être tranchées :** (1) DEC-013 « Pas de contrôle de la batterie en vol » : une coupure sur sous-tension en vol est soit un contrôle de la batterie en vol, soit une protection matérielle hors logiciel de vol, à qualifier en architecture ; (2) DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » : le seuil d'armement garantit un vol complet avec marge, alors que le seuil de sous-tension coupe en vol ; leur relation (le seuil d'armement doit rester au-dessus du seuil de sous-tension) est à fixer en architecture ; (3) un drone qui tombe sur sous-tension en vol ne signale rien, par cohérence avec DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté » ; (4) le « douzième scénario » écarté dans le texte de DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter » concernait un scénario de maintenance de la batterie ; SCN-012 « Dégradé : sous-tension de la batterie » est un scénario de protection, d'un autre objet, et des besoins sur la sous-tension pourront le citer ; (5) un redémarrage avec une batterie encore déchargée (tension remontée à vide) n'est pas décrit : risque de redémarrages répétés et de décharge profonde, à traiter en architecture matérielle ; le risque « drone laissé allumé » de « Risques acceptés » — `projets/boomrone/risques-acceptes.md` reste documenté, la protection n'étant pas garantie suffisante.
**Alternatives écartées :** « contraintes hors scénario » (première proposition de l'utilisateur) ; exception de méthode consignée ; protections de surintensité, d'inversion de polarité et de surchauffe (non retenues).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-107 « Exigences sans scénario amont : protections de la batterie, sous-tension, brown-out, CEM »
**Modifie :** DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter » (protection matérielle de sous-tension seulement).
**Précise :** DEC-097 « Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé ».
**Modifiée par :** DEC-133 « SCN-012 inclut le drone laissé allumé en attente d'un appui : sous-tension dans le périmètre » le 2026-10-28 (la phrase « drone laissé allumé ... restent hors périmètre » ne vaut plus pour le drone laissé allumé, inclus dans SCN-012 « Dégradé : sous-tension de la batterie »).
**Précisée par :** DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension » le 2026-10-28 (la coupure est assumée par le logiciel : la tension (1) nommée avec DEC-013 « Pas de contrôle de la batterie en vol » est tranchée par l'utilisateur) ; DEC-135 « Chute en vol sur sous-tension, sans signal, avec des personnes dessous : risque accepté » le 2026-10-28 (la chute en vol sur sous-tension est un risque accepté).

### DEC-127 — Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté
**Date :** 2026-10-28
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** À l'état « Échec d'initialisation », la commande sans fil « Sauvegarder » reste ACCEPTÉE (Modifier aussi ; Décoller et Arrêt ignorées) : DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » est inchangée pour cet état. Le risque qu'une commande « Sauvegarder » écrase les réglages enregistrés par des valeurs non chargées, déclenchée par un tiers à portée (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »), est accepté explicitement, avec sa perte persistante : seule la reprogrammation rétablit les valeurs (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »). Consigné dans « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (ligne 11), limite d'emploi : ne pas envoyer de réglages à un drone en échec d'initialisation. L'utilisateur avait vu l'option « Ignorée (recommandée) » et a choisi « Acceptée ». Points nommés sans être tranchés : (1) tension avec DEC-120 « Sauvegarder ignorée pendant l'initialisation en cours, Modifier acceptée ; cas de l'échec d'initialisation non tranché », dont la raison (ne pas écraser des réglages non chargés) vaut tout autant à l'état d'échec : les deux états de l'initialisation ont désormais un traitement opposé de Sauvegarder ; (2) il n'est pas dit si les réglages enregistrés sont chargés ou non à l'état d'échec (question de DOU-098 « Commande Sauvegarder après un échec d'initialisation : acceptée ou ignorée »), laissé à l'architecture ; (3) le risque se cumule avec DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule » (même recours, la reprogrammation) ; (4) un tiers peut aussi viser un drone en échec d'initialisation dont l'utilisateur ne connaît pas la cause sans appareil de suivi (DEC-088 « Bouton coincé ou maintenu en permanence au démarrage : statut sans fil seulement, aucun signal local »).
**Alternatives écartées :** « Ignorée (recommandée) » : Sauvegarder ignorée à l'état d'échec d'initialisation, comme pendant l'initialisation en cours (DEC-120 « Sauvegarder ignorée pendant l'initialisation en cours, Modifier acceptée ; cas de l'échec d'initialisation non tranché »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-098 « Commande Sauvegarder après un échec d'initialisation : acceptée ou ignorée »
**Précise :** DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » (état « Échec d'initialisation » confirmé) et DEC-120 « Sauvegarder ignorée pendant l'initialisation en cours, Modifier acceptée ; cas de l'échec d'initialisation non tranché » (cas de l'échec d'initialisation tranché).
**Modifiée par :** DEC-178 « Simplification n°5 adoptée : échec d'initialisation, toutes les commandes sans fil ignorées » le 2026-10-29 (Sauvegarder ignorée en échec d'initialisation)

### DEC-128 — Sauvegarder ignorée aussi à l'état Série d'appuis en cours
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Décision :** La commande sans fil « Sauvegarder » est aussi IGNORÉE à l'état « Série d'appuis en cours » (au moins un appui validé relâché, moins de 2 s écoulées), comme aux états « Premier appui validé » et « Armé, avant le lancer ». Cette décision **étend** DEC-123 « Sauvegarder ignorée aussi à l'état Premier appui validé » et DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer », et modifie le tableau de DEC-043 « Commandes sans fil acceptées selon l'état du drone » : la ligne « Allumé, en attente d'un appui » n'accepte plus Sauvegarder pendant la série ; une ligne « Série d'appuis en cours » (Modifier acceptée, Sauvegarder ignorée, Décoller et Arrêt ignorées) est ajoutée dans `00-scenarios.md`. Points nommés sans être tranchés : (1) la ligne « Allumé, en attente d'un appui » n'accepte donc Sauvegarder qu'avant un appui validé et après le retour à l'attente (compteur à zéro) ; (2) un appui en cours de moins de 1 s, non encore validé, laisse le drone dans l'état d'attente : une écriture commencée alors peut encore être en cours quand le premier appui est validé, puis à l'armement, ce que l'architecture doit couvrir avec DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture » ; (3) la commande ignorée n'a pas de signal local, l'acquittement se lit sur le statut sans fil (DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement ») ; (4) la phrase de DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer » selon laquelle Sauvegarder « reste acceptée en attente d'un appui » n'est plus exacte pour la série d'appuis (décision non réécrite).
**Alternatives écartées :** Sauvegarder acceptée à l'état « Série d'appuis en cours » (situation d'avant la réponse).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite » (point (a) ; les autres points sont répondus par les décisions de la même série)
**Étend :** DEC-123 « Sauvegarder ignorée aussi à l'état Premier appui validé » et DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer ».
**Modifie :** DEC-043 « Commandes sans fil acceptées selon l'état du drone » (état « Série d'appuis en cours »).

### DEC-129 — Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Une coupure de la batterie pendant l'écriture des réglages en mémoire non volatile (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage ») est un risque accepté. Il est à traiter en architecture par le choix de la mémoire ou de la séquence d'écriture, sans contrôle d'intégrité (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »). Consigné dans « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (ligne 33), limite d'emploi : ne pas débrancher la batterie pendant une sauvegarde ; seul recours, la reprogrammation. Points nommés sans être tranchés : (1) une écriture interrompue peut laisser une mémoire corrompue que le drone charge au démarrage suivant sans la détecter (même risque que DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »), avec un drone possiblement instable ; (2) frontière avec DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » : une séquence d'écriture à indicateur de validité ou à double copie serait-elle un contrôle d'intégrité exclu, ou un choix d'écriture permis ? À qualifier en architecture ; (3) l'architecture doit aussi couvrir une écriture commencée à l'état « Allumé » et encore en cours à l'armement ou au relâchement du bouton, qui pourrait dépasser la durée maximale de la phase « Lancé » (DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale » ; DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer »), ce point n'ayant pas reçu de réponse propre de l'utilisateur ; (4) la coupure de la batterie dans chaque état reste dans DOU-060 « Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle ».
**Alternatives écartées :** non étudiées avec l'utilisateur (par exemple un contrôle d'intégrité des réglages, déjà écarté par DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite » (point (b) ; les autres points sont répondus par les décisions de la même série)
**Précise :** DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage » et DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée ».
**Précisée par :** DEC-136 « Écriture de réglages commencée à l'état Allumé et encore en cours au relâchement du lancer : risque accepté » le 2026-10-28 (une écriture commencée à l'état Allumé et encore en cours au relâchement du lancer : risque accepté, documenté).

### DEC-130 — Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** Une mémoire de réglages « jamais écrite » (drone neuf) n'est pas détectée : aucun contrôle ni signal. Le drone utilise les valeurs d'origine fixes du logiciel (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal »), risque accepté, sans contrôle d'intégrité (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »). Consigné dans « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (ligne 34), limite d'emploi : vérifier le comportement d'un drone neuf avant usage normal (voir aussi ligne 21). Points nommés sans être tranchés : (1) tension de formulation avec DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal », qui suppose que le drone sait quand utiliser ses valeurs d'origine, alors qu'aucune détection n'est faite : le mécanisme (par exemple une zone programmée avec les valeurs d'origine, ou une valeur d'effacement reconnue) est laissé à l'architecture, sans que cela devienne un contrôle d'intégrité (même frontière que le point (2) de DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture ») ; (2) une mémoire vierge lue comme valeurs de réglage pourrait donner des valeurs aberrantes sans le savoir : risque couvert par la présente décision ; (3) la vérification que la reprogrammation rétablit les valeurs d'origine reste à faire en architecture (DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule »).
**Alternatives écartées :** détecter la mémoire jamais écrite (non retenu, déjà écarté par DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal » : refus de s'armer ou signal de mémoire vide).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite » (point (c) ; les autres points sont répondus par les décisions de la même série)
**Précise :** DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal » et DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée ».
**Précisée par :** DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine » le 2026-10-29 (la programmation écrit la zone avec les valeurs d'origine ; propagation : DEC-141 « Reprogrammation : propagation de DEC-139 aux scénarios et au registre des risques »).

### DEC-131 — Sauvegarder ignorée en vol : confirmation du tableau des commandes
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Décision :** La commande sans fil « Sauvegarder » est ignorée en vol (vol normal et vol de réglage), ainsi qu'en phase « Lancé ». C'est déjà ce que décide le tableau de DEC-043 « Commandes sans fil acceptées selon l'état du drone » (lignes « En vol (vol normal) » et « Vol de réglage » : Sauvegarder ignorée ; phase « Lancé » : DEC-069 « Commandes sans fil reçues pendant la phase Lancé : ignorées ») et le rappelle DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule ». Vérifié par l'architecte : aucune contradiction, aucune modification du tableau. Modifier reste acceptée en vol. La réponse de l'utilisateur la confirme explicitement comme point (d) de DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite ». Point nommé sans être tranché : la commande ignorée n'a pas de signal local, l'acquittement se lit sur le statut sans fil (DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement »).
**Alternatives écartées :** Sauvegarder acceptée en vol (alternative B de DEC-043 « Commandes sans fil acceptées selon l'état du drone », écriture mémoire possible en vol).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite » (point (d) ; les autres points sont répondus par les décisions de la même série)
**Précise :** DEC-043 « Commandes sans fil acceptées selon l'état du drone ».

### DEC-132 — Revue d'ensemble de Sauvegarder : états acceptés confirmés, aucun acquittement ni contrôle d'intégrité ajoutés
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-010 « Échec : initialisation impossible au démarrage »
**Décision :** Après une revue d'ensemble de la commande « Sauvegarder » (tableau des commandes de DEC-043 « Commandes sans fil acceptées selon l'état du drone », DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer », DEC-120 « Sauvegarder ignorée pendant l'initialisation en cours, Modifier acceptée ; cas de l'échec d'initialisation non tranché », DEC-123 « Sauvegarder ignorée aussi à l'état Premier appui validé », DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté », DEC-128 « Sauvegarder ignorée aussi à l'état Série d'appuis en cours » et DEC-131 « Sauvegarder ignorée en vol : confirmation du tableau des commandes »), l'utilisateur confirme que Sauvegarder reste acceptée dans trois états seulement : « Allumé, en attente d'un appui », « Échec d'initialisation » et « Mode réglage, moteurs coupés ». Elle reste ignorée dans tous les autres. Aucun acquittement supplémentaire n'est ajouté (DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement » reste inchangée, l'utilisateur n'ayant pas de préférence). Aucun contrôle d'intégrité des réglages n'est ajouté : DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée », DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture » et DEC-130 « Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté » sont maintenues.
**Alternatives écartées :** accepter Sauvegarder en mode réglage seulement ; ignorer Sauvegarder en échec d'initialisation (l'utilisateur a d'abord répondu « pas l'échec », puis, devant le cas A et le cas B, a confirmé « Acceptée » : DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté » est maintenue) ; ajouter un indicateur de validité de la mémoire.
**Raison :** réponses de l'utilisateur en chat, 2026-10-28, après une vue d'ensemble de la commande ; la dernière réponse sur l'état d'échec prévaut.
**Doutes levés :** (aucun)
**Confirme :** DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté » et DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement ».

### DEC-133 — SCN-012 inclut le drone laissé allumé en attente d'un appui : sous-tension dans le périmètre
**Date :** 2026-10-28
**Concerne :** SCN-012 « Dégradé : sous-tension de la batterie »
**Décision :** SCN-012 « Dégradé : sous-tension de la batterie » INCLUT le drone laissé allumé en attente d'un appui : la sous-tension (décharge profonde) d'un drone allumé est dans le périmètre, comme celle d'un drone en vol. Les états couverts sont ceux où le drone est sous tension : en attente d'un appui, Série d'appuis en cours, Premier appui validé, armé, phase « Lancé », en vol, vol de réglage, mode réglage et initialisation. Un besoin pourra donc citer SCN-012 « Dégradé : sous-tension de la batterie » pour un drone laissé allumé. Charge, remplacement, stockage de la batterie et programmation restent hors périmètre (limites d'emploi, DEC-125 « Limites d'emploi informées par une notice écrite à la phase besoins, le drone n'affiche rien »). **Contradictions nommées :** cette décision **modifie** DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter » (« drone laissé allumé » n'est plus hors périmètre) et DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre » (sa phrase « drone laissé allumé ... restent hors périmètre ») ; les titres ne sont pas réécrits. L'utilisateur avait vu l'option « Non, retirer ce cas (recommandée) » et a choisi « Oui, l'inclure ». Points nommés sans être tranchés : (1) le rapport entre le seuil d'armement et le seuil de sous-tension : DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs » ; (2) un drone coupé sur sous-tension puis rebranché sur une batterie encore déchargée : DOU-109 « Batterie déjà déchargée : redémarrages répétés, décharge profonde et état après une coupure logicielle ».
**Alternatives écartées :** « Non, retirer ce cas (recommandée) » : le drone laissé allumé reste hors périmètre, limite d'emploi seule.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun)
**Modifie :** DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter » (drone laissé allumé) et DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre ».

### DEC-134 — Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension
**Date :** 2026-10-28
**Concerne :** SCN-012 « Dégradé : sous-tension de la batterie » et SCN-003 « Échec : batterie faible à l'armement »
**Décision :** La coupure des moteurs sur sous-tension, y compris en vol, est assumée PAR LE LOGICIEL : le drone surveille la tension de la batterie et coupe les moteurs sous le seuil de sous-tension. Le seuil d'armement doit rester au-dessus du seuil de sous-tension (valeur en architecture : DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture »). **Contradictions nommées :** cette décision **modifie** DEC-013 « Pas de contrôle de la batterie en vol » (l'alternative écartée « couper les moteurs en vol » est de fait adoptée pour la sous-tension ; le titre est conservé) et **précise** DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » (relation des deux seuils) ; elle tranche la tension (1) nommée dans DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre » (protection matérielle hors logiciel de vol, ou contrôle en vol). Elle précise DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? » en le reliant à SCN-012 « Dégradé : sous-tension de la batterie ». L'utilisateur avait vu « Protection matérielle hors logiciel (recommandée) » et a choisi « Coupure assumée en vol par le logiciel ». Points nommés sans être tranchés : (1) DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre » et SCN-012 « Dégradé : sous-tension de la batterie » décrivent la sous-tension « comme une coupure d'alimentation » (moteurs arrêtés, drone verrouillé, état « Éteint » des diagrammes) alors qu'une coupure par le logiciel laisse le microcontrôleur alimenté : le drone reste-t-il sous tension (verrouillé) ou s'éteint-il ? À fixer : DOU-109 « Batterie déjà déchargée : redémarrages répétés, décharge profonde et état après une coupure logicielle » ; (2) l'affaissement de tension au démarrage des moteurs peut franchir le seuil de sous-tension à l'armement ou au lancer : DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs » ; (3) la surveillance logicielle ne protège pas un logiciel bloqué, que le chien de garde traite déjà (DEC-065 « Logiciel bloqué en vol : coupure des moteurs par un chien de garde »).
**Alternatives écartées :** protection matérielle hors logiciel, sans contrôle de la batterie par le logiciel (recommandée par l'architecte, non retenue).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun)
**Modifie :** DEC-013 « Pas de contrôle de la batterie en vol ».
**Précise :** DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » et DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre ».

### DEC-135 — Chute en vol sur sous-tension, sans signal, avec des personnes dessous : risque accepté
**Date :** 2026-10-28
**Concerne :** SCN-012 « Dégradé : sous-tension de la batterie »
**Décision :** Le risque qu'un drone en vol chute sur sous-tension, sans signal, avec des personnes dessous, y compris pendant le lancer (phase « Lancé », moteurs non encore démarrés, drone dans la main ou lâché), est ACCEPTÉ et documenté : consigné dans « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (ligne 35), dans les limites d'emploi de la notice (DEC-125 « Limites d'emploi informées par une notice écrite à la phase besoins, le drone n'affiche rien ») et dans SCN-012 « Dégradé : sous-tension de la batterie ». Aucun signal propre, par cohérence avec DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre » et DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté ». Cumul nommé sans être tranché : DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension » fait de la chute une conséquence voulue de la coupure sous le seuil, donc d'un seuil mal placé (DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs »).
**Alternatives écartées :** (non précisées dans la réponse) ; un atterrissage doux sur batterie faible avait été écarté par DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » et DEC-013 « Pas de contrôle de la batterie en vol ».
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun)
**Précise :** DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre ».
**Maintenue par :** DEC-140 « Chute brutale sur sous-tension maintenue en connaissance de cause, sans seuil d'alerte » le 2026-10-29 (la raison d'écarter l'atterrissage doux a changé, DEC-013 « Pas de contrôle de la batterie en vol » étant modifiée par DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension »).

### DEC-136 — Écriture de réglages commencée à l'état Allumé et encore en cours au relâchement du lancer : risque accepté
**Date :** 2026-10-28
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Une écriture de réglages commencée à l'état « Allumé, en attente d'un appui » (par exemple pendant un appui de moins de 1 s, non encore validé) et encore en cours au relâchement du lancer est un risque ACCEPTÉ et documenté : elle peut dépasser la durée maximale de la phase « Lancé » et être coupée par le chien de garde (DEC-103 « Phase Lancé trop longue : coupure et redémarrage par le chien de garde, sans nouvel état ni signal »), sans que les moteurs aient démarré, avec une mémoire possiblement interrompue (DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture »). Consigné dans « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (ligne 36), limite d'emploi de la notice (DEC-125 « Limites d'emploi informées par une notice écrite à la phase besoins, le drone n'affiche rien »). Les textes des scénarios qui disaient « aucune écriture en mémoire pendant l'armement ni le lancer » sont corrigés (règle complémentaire du tableau, légende du diagramme a, SCN-009 « Réglage et suivi du drone par le sans fil » étape 7) : « Sauvegarder n'est pas acceptée à partir de l'appui validé ; une écriture déjà commencée reste un risque accepté (DEC-136 « Écriture de réglages commencée à l'état Allumé et encore en cours au relâchement du lancer : risque accepté ») ». **Contradiction nommée :** la raison de DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer » (ne pas retarder le lancer) n'est pas atteinte pour une écriture commencée avant l'appui validé ; DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer » est conservée, le résiduel est accepté ici. Point nommé sans être tranché : la durée d'une écriture dépend de la mémoire choisie en architecture (DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture »), donc la fenêtre du risque est inconnue.
**Alternatives écartées :** (non précisées dans la réponse).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun)
**Précise :** DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture », DEC-128 « Sauvegarder ignorée aussi à l'état Série d'appuis en cours » et DEC-103 « Phase Lancé trop longue : coupure et redémarrage par le chien de garde, sans nouvel état ni signal ».

### DEC-137 — Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-002 « Échec : stationnaire non atteint dans le délai »
**Décision :** La plage de lancer de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » n'est pas resserrée maintenant : elle reste provisoire et sera validée par essais sur prototype. Le jalon « analyse de faisabilité avant les besoins » de DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » est abandonné pour DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » : le doute reste ouvert jusqu'aux essais et n'empêche plus d'ouvrir la phase « besoins ». Réponse donnée d'abord (« ne rien changer, valider par essais »), puis confirmée après rappel de la contradiction avec DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » et DEC-122 « Jalon avant les besoins : promesse de l'architecte, sans modification de l'outil de porte ». Risque nommé : besoins et exigences écrits sur une plage peut-être infaisable (le bas de la plage, drone lancé à l'envers depuis 1,5 m, laisse environ 0,4 s avant le sol selon le calcul de la relecture critique), à reprendre après les essais. Portée : DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » seulement ; le sort de DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal », de la part de DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » liée à DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » et de DOU-110 « La reprogrammation efface-t-elle la zone des réglages sauvegardés ? » n'est pas encore tranché.
**Alternatives écartées :** vitesse minimale plus haute (recommandée) ; hauteur minimale plus haute ; orientation restreinte ; calcul rapide puis essais.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun)
**Modifie :** DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » et DEC-122 « Jalon avant les besoins : promesse de l'architecte, sans modification de l'outil de porte ».

### DEC-138 — Tolérance d'immobile et part de DOU-058 liée à la faisabilité : jalon déplacé aux essais
**Date :** 2026-10-28
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Même report aux essais que DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée » : DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal » et la part de DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » liée à DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » (tolérance de « immobile », plage de lancer) restent ouverts jusqu'aux essais sur prototype et n'empêchent plus d'ouvrir la phase « besoins ». Les valeurs restent provisoires dans les scénarios. Risque nommé : un besoin d'armement écrit avant de connaître la tolérance réaliste d'un drone tenu en main peut devoir être repris après les essais. Non tranché : DOU-110 « La reprogrammation efface-t-elle la zone des réglages sauvegardés ? » (question de fait sur la reprogrammation, à poser séparément).
**Alternatives écartées :** garder l'échéance « avant les besoins » pour ces deux doutes.
**Raison :** réponse de l'utilisateur en chat, 2026-10-28.
**Doutes levés :** (aucun)
**Modifie :** DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » et DEC-122 « Jalon avant les besoins : promesse de l'architecte, sans modification de l'outil de porte ».
**Précise :** DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée ».

### DEC-139 — Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine
**Date :** 2026-10-28
**Concerne :** SCN-008 « Mise en service : programmation du drone » et SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** La reprogrammation du drone réécrit la zone des réglages sauvegardés avec les valeurs d'origine du logiciel. Elle reste ainsi le recours des quatre risques de « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (réglages aberrants envoyés par un tiers, mémoire corrompue, écriture interrompue par une coupure, mémoire jamais écrite), selon DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule » et DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée ». Conséquence acceptée : les réglages sauvegardés sont perdus à chaque reprogrammation. Les valeurs d'origine sont fixes et propres au logiciel (DEC-130 « Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté »). Le mécanisme de réécriture est à traiter en architecture (`notes-architecture.md`).
**Alternatives écartées :** zone non touchée (les quatre risques perdent leur recours) ; effacement sans valeurs d'origine (demande de reconnaître une zone vide, écarté par DEC-130 « Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-28 (option recommandée par l'architecte).
**Doutes levés :** DOU-110 « La reprogrammation efface-t-elle la zone des réglages sauvegardés ? »
**Précise :** DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule ».

### DEC-140 — Chute brutale sur sous-tension maintenue en connaissance de cause, sans seuil d'alerte
**Date :** 2026-10-29
**Concerne :** SCN-012 « Dégradé : sous-tension de la batterie » et SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** DEC-135 « Chute en vol sur sous-tension, sans signal, avec des personnes dessous : risque accepté » est maintenue après rappel que DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension » a modifié DEC-013 « Pas de contrôle de la batterie en vol », qui était l'une des raisons d'écarter l'atterrissage doux. Aucun seuil d'alerte au-dessus du seuil de coupure, aucun atterrissage normal sur batterie faible : le drone coupe les moteurs sous le seuil de sous-tension, sans signal propre. La raison d'écarter l'atterrissage doux n'est plus « pas de contrôle de la batterie en vol » : c'est le choix explicite de l'utilisateur, qui connaît le risque pour les personnes dessous.
**Alternatives écartées :** seuil d'alerte supérieur au seuil de coupure déclenchant l'atterrissage normal de SCN-001 « Vol nominal : de la batterie au posé », sans nouveau signal (option recommandée par l'architecte : moins de chutes sur des personnes, mais SCN-012 « Dégradé : sous-tension de la batterie » à compléter et deux seuils à fixer, lié à DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-29, option « Maintenir la chute brutale » choisie après exposé des options.
**Doutes levés :** (aucun)
**Précise :** DEC-135 « Chute en vol sur sous-tension, sans signal, avec des personnes dessous : risque accepté ».

### DEC-141 — Reprogrammation : propagation de DEC-139 aux scénarios et au registre des risques
**Date :** 2026-10-29
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Décision :** DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine » est propagée : SCN-008 « Mise en service : programmation du drone » dit que la programmation réécrit la zone des réglages avec les valeurs d'origine et que les réglages sauvegardés sont perdus ; DEC-130 « Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté » est notée précisée par DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine » ; les lignes 21 et 34 de « Risques acceptés » — `projets/boomrone/risques-acceptes.md` renvoient à DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine » (sur un drone programmé, la mémoire jamais écrite ne subsiste que si la programmation n'écrit pas la zone). Propagation de forme, sans changer le fond de DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine ».
**Alternatives écartées :** laisser DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine » connue du seul journal (incohérence persistante entre DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine », DEC-130 « Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté » et SCN-008 « Mise en service : programmation du drone »).
**Raison :** réponse de l'utilisateur en chat, 2026-10-29, option « Oui, propager » (recommandée par l'architecte).
**Doutes levés :** (aucun)
**Précise :** DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine ».

### DEC-142 — Porte scénarios franchie : accord explicite de l'utilisateur
**Date :** 2026-10-29
**Concerne :** « Scénarios » — `projets/boomrone/00-scenarios.md` (SCN-001 « Vol nominal : de la batterie au posé » à SCN-012 « Dégradé : sous-tension de la batterie »)
**Décision :** la porte « scénarios » est franchie ; la phase « besoins » peut s'ouvrir. État au franchissement : tag `gate-1-scenarios-ready-v1`, aucun doute bloquant ouvert, 25 doutes non bloquants (liste dans `registre-doutes.md`), cinq relectures de porte faites (`critique`, `coherence-clarte`).
**Alternatives écartées :** continuer la phase « scénarios » (aucun doute bloquant, toutes les décisions demandées sont prises).
**Raison :** accord explicite de l'utilisateur en chat, 2026-10-29 : « passons la gate ». Rappels : `check_traceability --gate` échoue seulement sur les douze « SCN sans BES », normaux avant la phase « besoins » ; la notice des limites d'emploi est à écrire en phase « besoins » (DEC-125 « Limites d'emploi informées par une notice écrite à la phase besoins, le drone n'affiche rien ») ; si les essais contredisent la plage de lancer, les besoins seront à reprendre (DOU-116 « Échéance et circularité du report aux essais, comportement de SCN-002 sur la partie infaisable de la plage »).
**Doutes levés :** (aucun)

### DEC-143 — Délégation de la phase besoins à l'architecte
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`
**Décision :** pour la phase « besoins » seulement, l'utilisateur ne veut aucune question : l'architecte décide seul, consigne chaque choix en DEC et prépare un dossier fini. Cette délégation remplace pour cette phase la règle « l'utilisateur décide » ; la porte « besoins » n'est pas franchie par l'architecte, l'accord explicite de l'utilisateur reste requis.
**Alternatives écartées :** poser les questions une à une comme en phase « scénarios » (refusé par l'utilisateur) ; franchir aussi la porte (l'accord explicite de l'utilisateur reste obligatoire, charte §3).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-144 — Ligne directrice : simplicité, un seul utilisateur qui accepte les risques
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`
**Décision :** critère unique de la phase : Boomrone est un premier drone, un jeu, avec un seul utilisateur (son concepteur) qui accepte les risques et les dangers, fabrique l'électronique et programme le logiciel lui-même. En cas de choix, l'option retenue est la plus simple à utiliser, à spécifier, à fabriquer et à programmer. Peu de fonctions, besoins simples.
**Alternatives écartées :** reprendre tous les cas des scénarios un par un en besoins (une quarantaine de besoins, lourds) ; ajouter des besoins de sécurité de tiers, de public ou de conformité (voir DEC-153 « Pas de besoin de sécurité des tiers, de conformité, de durée de vie ni de gestion de la batterie »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-145 — Treize besoins : regroupements retenus
**Date :** 2026-10-29
**Concerne :** BES-001 « Lancer le drone à la main » à BES-013 « Voler en appartement avec un drone de poche protégé »
**Décision :** treize besoins au total, une intention chacun : tous les refus en un besoin, toutes les coupures des moteurs en un besoin, l'information de l'utilisateur en un besoin, le réglage en deux besoins, le suivi en un besoin. Chaque scénario est couvert par au moins un besoin.
**Alternatives écartées :** un besoin par scénario (douze besoins quasi identiques aux scénarios, sans gain) ; un besoin par signal ou par cas de bouton (dizaines de besoins, solution déjà dans les scénarios).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-146 — Besoins qualitatifs : une seule valeur chiffrée, les 10 s de stationnaire
**Date :** 2026-10-29
**Concerne :** BES-003 « Rester en vol stationnaire 10 s puis atterrir doucement »
**Décision :** les besoins sont qualitatifs, sans solution ni valeur chiffrée, sauf les 10 s de stationnaire qui font l'intention du produit. Les seuils de temps du bouton, les délais, les angles et les tensions viennent aux exigences.
**Alternatives écartées :** chiffrer les besoins (les valeurs sont provisoires et des doutes ouverts les portent : DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m », DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture ») ; retirer aussi les 10 s (c'est l'intention du produit).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-147 — Priorités des besoins : le vol sûr d'abord, le réglage et le suivi ensuite
**Date :** 2026-10-29
**Concerne :** BES-001 « Lancer le drone à la main » à BES-013 « Voler en appartement avec un drone de poche protégé »
**Décision :** Essentiel (sept besoins) : lancer, stationnaire et atterrissage, ne pas voler non prêt, couper les moteurs, arrêt en vol, information locale, programmation. Important (cinq) : ne pas armer par erreur, mode réglage, réglage et sauvegarde, page de consignes, lieu d'emploi. Souhaitable (un) : suivi sur appareil de suivi.
**Alternatives écartées :** tout en Essentiel (n'aide pas à décider quoi livrer d'abord) ; réglage en Essentiel (le drone vole avec les valeurs d'origine sans lui).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)
**Modifiée par :** DEC-159 « Réglage et suivi alignés en Souhaitable, subordonnés au suivi » le 2026-10-29 (BES-008 « Entrer en mode réglage et faire des vols de réglage » et BES-009 « Régler et sauvegarder les paramètres de vol » passent d'Important à Souhaitable : sept Essentiels, trois Importants, trois Souhaitables ; le reste est inchangé).

### DEC-148 — Un seul besoin pour tous les refus et l'échec d'initialisation
**Date :** 2026-10-29
**Concerne :** BES-004 « Ne pas voler quand le drone n'est pas prêt »
**Décision :** le refus d'armement (batterie faible, mouvement, pas à plat), le refus du mode réglage, le refus de décoller en réglage et l'échec d'initialisation forment un seul besoin : le drone ne vole pas tant qu'il n'est pas prêt, et le dit. Les différences de cas restent aux scénarios et aux exigences.
**Alternatives écartées :** un besoin pour l'armement et un pour l'initialisation (même intention : ne pas voler non prêt) ; un besoin par cause de refus (solution déjà détaillée aux scénarios).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-124 « Les refus d'initialisation et de mode réglage entrent-ils dans le besoin de refus d'armement ? »

### DEC-149 — Un seul besoin pour toutes les coupures des moteurs
**Date :** 2026-10-29
**Concerne :** BES-005 « Couper les moteurs quand le vol ne peut pas continuer »
**Décision :** échec de stabilisation, basculement, atterrissage trop long, coupure d'alimentation, batterie trop basse et logiciel bloqué forment un seul besoin : les moteurs s'arrêtent et le drone ne reprend jamais le vol seul. L'arrêt voulu par l'utilisateur reste un besoin à part (BES-006 « Arrêter le drone en vol d'un geste »), car c'est une action de sa part.
**Alternatives écartées :** un besoin par cause (six besoins de même intention) ; fusionner aussi l'arrêt par l'utilisateur (action volontaire, intention différente).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-150 — Réglage en deux besoins, suivi en un besoin souhaitable
**Date :** 2026-10-29
**Concerne :** BES-008 « Entrer en mode réglage et faire des vols de réglage », BES-009 « Régler et sauvegarder les paramètres de vol » et BES-010 « Suivre le drone sur un appareil de suivi »
**Décision :** le mode réglage avec ses vols (Important), le réglage et la sauvegarde des paramètres (Important) et le suivi sur appareil de suivi (Souhaitable) sont trois besoins courts, sans enrichissement : pas d'appairage, pas de contrôle d'intégrité, pas de limite de vols (risques déjà acceptés dans « Risques acceptés » — `projets/boomrone/risques-acceptes.md`).
**Alternatives écartées :** un seul besoin de réglage et suivi (mélange trois intentions et trois priorités) ; suivi Important (le drone vole sans appareil de suivi : DEC-032 « Vol libre : le drone vole sans appareil de suivi »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-121 « Le suivi sans fil est-il un besoin à part entière ? »
**Modifiée par :** DEC-159 « Réglage et suivi alignés en Souhaitable, subordonnés au suivi » le 2026-10-29 (BES-008 « Entrer en mode réglage et faire des vols de réglage » et BES-009 « Régler et sauvegarder les paramètres de vol » passent en Souhaitable).

### DEC-151 — Un besoin sur le lieu d'emploi et les protège-hélices
**Date :** 2026-10-29
**Concerne :** BES-013 « Voler en appartement avec un drone de poche protégé »
**Décision :** un besoin court porte le cadre d'emploi (drone de poche, appartement, protège-hélices ; gymnase et jardin en essais complémentaires) pour qu'une décision structurante antérieure (DEC-016 « Public adulte, protège-hélices obligatoires » ; DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires ») ait un besoin en aval. Priorité Important.
**Alternatives écartées :** ne rien écrire (le cadre d'emploi n'aurait aucun besoin et les exigences de taille et de protection n'auraient pas d'amont) ; le mettre dans la page de consignes seulement (une consigne n'est pas un besoin vérifiable).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-122 « Faut-il un besoin sur le lieu d'emploi et les protège-hélices ? »

### DEC-152 — Information de l'utilisateur : un seul besoin, sur le drone lui-même
**Date :** 2026-10-29
**Concerne :** BES-007 « Savoir où en est le drone sans autre appareil »
**Décision :** l'information de l'utilisateur est un seul besoin, satisfait sur le drone sans appareil de suivi ; la cause détaillée sur appareil de suivi relève de BES-010 « Suivre le drone sur un appareil de suivi » (Souhaitable). Le nombre de signaux, leur forme et leur regroupement sont des sujets d'exigences et d'architecture (DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie »).
**Alternatives écartées :** un besoin par étape du vol ou par signal (dix-sept besoins, solution déjà dans les scénarios) ; deux besoins (vol / échecs), sans gain.
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-153 — Pas de besoin de sécurité des tiers, de conformité, de durée de vie ni de gestion de la batterie
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`
**Décision :** aucun besoin sur la sécurité des tiers, le public, la conformité, la protection contre un tiers malveillant, la durée de vie, ni la gestion de la batterie (charge, remplacement, stockage) : l'utilisateur est seul et accepte les risques. La protection de sous-tension reste portée par BES-005 « Couper les moteurs quand le vol ne peut pas continuer » (DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre »). Ces points sont rappelés dans les consignes d'emploi.
**Alternatives écartées :** besoins de sécurité du public ou de conformité (hors du jeu d'un utilisateur unique qui accepte les risques) ; besoin de gestion de la batterie (contredit DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-125 « Faut-il des besoins sur la sécurité des tiers, la conformité, la durée de vie ou la gestion de la batterie ? »

### DEC-154 — Notice des limites d'emploi : une page de consignes d'emploi
**Date :** 2026-10-29
**Concerne :** BES-012 « Disposer d'une page de consignes d'emploi »
**Décision :** la notice de DEC-125 « Limites d'emploi informées par une notice écrite à la phase besoins, le drone n'affiche rien » prend sa forme la plus légère : une seule page, « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md`, une quinzaine de consignes courtes (avant le vol, lancer, réglage, après le vol). « Risques acceptés » — `projets/boomrone/risques-acceptes.md` reste la source, sans nouveau registre. Le drone n'affiche rien de plus.
**Alternatives écartées :** notice complète reprenant les 36 lignes du registre (lourde, l'utilisateur la connaît déjà) ; nouveau registre de limites d'emploi (doublon de DEC-124 « Registre consolidé des risques acceptés dans un fichier dédié »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-123 « Quelle forme donner à la page de consignes d'emploi ? »

### DEC-155 — Scénarios inchangés : les complexités inutiles sont notées en simplifications possibles
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`, section « Simplifications possibles »
**Décision :** les douze scénarios validés ne sont pas modifiés. Six complexités qui pèsent sur la fabrication et la programmation sont notées dans un tableau de recommandations à l'utilisateur, qui décide (série de trois appuis, dix-sept signaux, états de Sauvegarder, commandes après échec d'initialisation, cause précise sur le sans fil, bornes des seuils).
**Alternatives écartées :** modifier les scénarios (validés par DEC-142 « Porte scénarios franchie : accord explicite de l'utilisateur », hors délégation) ; ignorer ces complexités (l'utilisateur ne saurait pas qu'il peut les retirer).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun) ; ouvre DOU-126 « Simplifications possibles des scénarios : choix de l'utilisateur »
**Modifiée par :** DEC-160 « Cadrage des besoins : contraintes du projet et simplification n°1 recommandée » le 2026-10-29 (sept lignes au lieu de six, la nouvelle en première position).

### DEC-156 — Couverture des scénarios vérifiée à la main, outil de traçabilité inchangé
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`, section « Couverture des scénarios »
**Décision :** `tools/check_traceability.py` ne compte pas le lien besoin vers scénario et laissera les douze scénarios « sans BES » ; la couverture des douze scénarios est vérifiée à la main et écrite dans « Besoins » (diagramme et tableau). L'outil n'est pas modifié ; les « BES sans REQ » et « BES sans TA » sont normaux avant les phases suivantes.
**Alternatives écartées :** modifier l'outil (interdit pour cette phase) ; ne rien vérifier (trou possible non vu).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-157 — Doutes de la phase besoins tranchés par l'architecte
**Date :** 2026-10-29
**Concerne :** « Registre de doutes » — `projets/boomrone/registre-doutes.md`
**Décision :** les doutes qui relèvent d'un choix de besoin sont notés puis tranchés par l'architecte (cinq doutes de la série numérotée 121 à 125, listés dans « Doutes levés » ci-dessous, chacun levé par la décision de son besoin). Ceux qui relèvent des exigences, de l'architecture ou des essais restent ouverts, non bloquants, avec leur échéance ; DOU-126 « Simplifications possibles des scénarios : choix de l'utilisateur » est ouvert pour que l'utilisateur choisisse à la porte « besoins ». Aucun doute bloquant n'est ouvert.
**Alternatives écartées :** laisser les doutes de besoin ouverts (la délégation demande de trancher) ; trancher aussi les doutes d'exigences et d'essais (hors du choix de besoin).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-121 « Le suivi sans fil est-il un besoin à part entière ? » (DEC-150 « Réglage en deux besoins, suivi en un besoin souhaitable ») ; DOU-122 « Faut-il un besoin sur le lieu d'emploi et les protège-hélices ? » (DEC-151 « Un besoin sur le lieu d'emploi et les protège-hélices ») ; DOU-123 « Quelle forme donner à la page de consignes d'emploi ? » (DEC-154 « Notice des limites d'emploi : une page de consignes d'emploi ») ; DOU-124 « Les refus d'initialisation et de mode réglage entrent-ils dans le besoin de refus d'armement ? » (DEC-148 « Un seul besoin pour tous les refus et l'échec d'initialisation ») ; DOU-125 « Faut-il des besoins sur la sécurité des tiers, la conformité, la durée de vie ou la gestion de la batterie ? » (DEC-153 « Pas de besoin de sécurité des tiers, de conformité, de durée de vie ni de gestion de la batterie »)

### DEC-158 — Énoncés des besoins resserrés : une intention, testable, sans solution
**Date :** 2026-10-29
**Concerne :** BES-001 « Lancer le drone à la main » à BES-013 « Voler en appartement avec un drone de poche protégé »
**Décision :** après les trois relectures de porte, chaque énoncé est ramené à une intention courte, critères chiffrés renvoyés aux exigences. BES-001 « Lancer le drone à la main » : titre « Lancer le drone à la main » (ancien : « ... avec un seul bouton »), « sans viser une orientation précise », promesse dépendante des essais (DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m », DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal », DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée ») ; « se stabiliser seul » reste dans BES-003 « Rester en vol stationnaire 10 s puis atterrir doucement ». BES-002 « Ne pas armer ni lancer par erreur » : appui involontaire ou hésitant sans lancer, renoncer après l'armement. BES-003 « Rester en vol stationnaire 10 s puis atterrir doucement » : « sans s'éloigner de façon sensible », « sans choc violent », attente d'un nouvel appui après le posé. BES-004 « Ne pas voler quand le drone n'est pas prêt » : « conditions de départ non réunies », « échec d'initialisation », énergie d'un vol complet une fois armé (DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? », DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs » non levés), phrase d'avertissement retirée. BES-005 « Couper les moteurs quand le vol ne peut pas continuer » : causes en liste, « défaillance du drone » (SCN-011 « Dégradé : coupure d'alimentation en vol »), retour de l'alimentation sans reprise. BES-006 « Arrêter le drone en vol d'un geste » : « une fois le lancer terminé », bouton seul suffisant, arrêt sans fil facultatif, SCN-009 « Réglage et suivi du drone par le sans fil » ajouté aux références. BES-007 « Savoir où en est le drone sans autre appareil » : situations où un signal est possible, liste minimale prêt, lancé, refus, échec, coupure des moteurs en vol, posé, aucun signal après coupure d'alimentation ou sous-tension, six scénarios ajoutés aux références. BES-008 « Entrer en mode réglage et faire des vols de réglage » : besoin d'essai de réglage en vol. BES-009 « Régler et sauvegarder les paramètres de vol » : seul recours aux réglages aberrants ou perdus = reprogrammer. BES-010 « Suivre le drone sur un appareil de suivi » : état et causes de refus ou de coupure, sans recouvrement avec BES-007 « Savoir où en est le drone sans autre appareil », « sans appareil de suivi » dit une seule fois dans les contraintes (DEC-032 « Vol libre : le drone vole sans appareil de suivi »). BES-011 « Fabriquer et programmer le drone soi-même » (ancien titre : « Programmer le drone depuis l'ordinateur », retitré par DEC-166 « BES-011 retitré : fabriquer et programmer le drone soi-même ») : « avec son programmateur » retiré. BES-012 « Disposer d'une page de consignes d'emploi » : « chacun des risques de la liste de référence », test par inspection, chemin de fichier en références. BES-013 « Voler en appartement avec un drone de poche protégé » : appartement, poche, protège-hélices ; gymnase et jardin en note de périmètre.
**Alternatives écartées :** garder les énoncés longs (ils mélangeaient besoin, solution et valeurs) ; retirer « se stabiliser seul » de BES-003 « Rester en vol stationnaire 10 s puis atterrir doucement » (c'est son cœur).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun) ; ouvre DOU-127 « Couverture ligne à ligne des risques acceptés par les consignes d'emploi »
**Modifiée par :** DEC-164 « Seconde relecture de porte : énoncés des besoins repris » le 2026-10-29 (énoncés des treize besoins repris).

### DEC-159 — Réglage et suivi alignés en Souhaitable, subordonnés au suivi
**Date :** 2026-10-29
**Concerne :** BES-008 « Entrer en mode réglage et faire des vols de réglage », BES-009 « Régler et sauvegarder les paramètres de vol », BES-010 « Suivre le drone sur un appareil de suivi »
**Décision :** les trois besoins sont Souhaitables : le drone vole avec ses valeurs d'origine sans appareil de suivi (DEC-032 « Vol libre : le drone vole sans appareil de suivi »). BES-008 « Entrer en mode réglage et faire des vols de réglage » et BES-009 « Régler et sauvegarder les paramètres de vol » sont subordonnés à BES-010 « Suivre le drone sur un appareil de suivi ». Décompte : 7 Essentiels, 3 Importants, 3 Souhaitables. Modifie DEC-147 « Priorités des besoins : le vol sûr d'abord, le réglage et le suivi ensuite ».
**Alternatives écartées :** garder BES-008 « Entrer en mode réglage et faire des vols de réglage » et BES-009 « Régler et sauvegarder les paramètres de vol » Importants alors que BES-010 « Suivre le drone sur un appareil de suivi » Souhaitable les conditionne (priorités incohérentes).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-160 — Cadrage des besoins : contraintes du projet et simplification n°1 recommandée
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`, sections « Contraintes du projet » et « Annexe B — Simplifications possibles »
**Décision :** une section « Contraintes du projet » (propriétaire qui fabrique l'électronique et programme, un seul utilisateur qui accepte les risques, fonctionnement sans appareil de suivi) sans nouveau besoin. En première ligne des simplifications : « retirer le sans fil de réglage et de suivi (SCN-009 « Réglage et suivi du drone par le sans fil », BES-008 « Entrer en mode réglage et faire des vols de réglage », BES-009 « Régler et sauvegarder les paramètres de vol », BES-010 « Suivre le drone sur un appareil de suivi ») : le réglage se fait en reprogrammant », recommandée, avec gain, coût et colonne « Décision de l'utilisateur » à remplir. C'est le seul choix qui modifierait des scénarios validés. DOU-126 « Simplifications possibles des scénarios : choix de l'utilisateur » reste ouvert, non bloquant. Modifie DEC-155 « Scénarios inchangés : les complexités inutiles sont notées en simplifications possibles ».
**Alternatives écartées :** retirer le sans fil d'office (modifie des scénarios validés, hors délégation) ; ne pas le proposer (l'utilisateur ne verrait pas le gain).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)
**Précisée par :** DEC-163 « Communication sans fil conservée : simplification n°1 écartée » le 2026-10-29 (la n°1 recommandée est écartée par l'utilisateur) ; DEC-168 « Annexe B des besoins : quatre colonnes, simplifications n°2 à n°7 recommandées » le 2026-10-29.

### DEC-161 — Lisibilité du dossier des besoins : ordre, parcours, tableau, annexes, écarts de l'outil
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`
**Décision :** ordre : aperçu de cinq lignes, parcours de l'utilisateur (diagramme, ID seuls), tableau récapitulatif, besoins, contraintes, annexes (couverture, simplifications, doutes). Le tableau de couverture redondant est supprimé ; le diagramme scénarios vers besoins est allégé (titres abrégés, légende). Un encadré explique pourquoi `--gate` affiche ÉCHEC (12 « SCN sans BES », défaut connu de l'outil : DEC-156 « Couverture des scénarios vérifiée à la main, outil de traçabilité inchangé » ; « BES sans REQ » et « BES sans TA » : phases suivantes).
**Alternatives écartées :** garder tableau et diagramme de couverture (doublon) ; modifier l'outil (interdit).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-162 — Consignes d'emploi : une consigne par ligne, les dangers en tête
**Date :** 2026-10-29
**Concerne :** « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md`
**Décision :** une consigne par puce, phrases de quinze mots au plus, sans jargon ; les trois consignes les plus dangereuses en tête (relâcher le bouton prêt démarre les moteurs, ne pas lancer vers des personnes, débrancher la batterie au moindre doute) ; diagramme des trois risques majeurs ; lien vers « Besoins ». Le mot « notice » devient « consignes d'emploi » dans la page et le glossaire (hors citations de titres de décisions). Précise DEC-154 « Notice des limites d'emploi : une page de consignes d'emploi ».
**Alternatives écartées :** garder la forme dense (phrases doubles, jargon) ; reprendre les 36 lignes du registre sans regrouper.
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-163 — Communication sans fil conservée : simplification n°1 écartée
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`, section « Annexe B — Simplifications possibles », ligne n°1 ; SCN-009 « Réglage et suivi du drone par le sans fil », BES-008 « Entrer en mode réglage et faire des vols de réglage », BES-009 « Régler et sauvegarder les paramètres de vol », BES-010 « Suivre le drone sur un appareil de suivi »
**Décision :** le sans fil de réglage et de suivi est conservé ; la simplification n°1 (le retirer) est écartée. SCN-009 « Réglage et suivi du drone par le sans fil » et les mentions du sans fil dans les autres scénarios restent inchangés. Rien d'autre n'est décidé : les trois besoins restent Souhaitables et BES-008 « Entrer en mode réglage et faire des vols de réglage » et BES-009 « Régler et sauvegarder les paramètres de vol » restent subordonnés à BES-010 « Suivre le drone sur un appareil de suivi » (DEC-159 « Réglage et suivi alignés en Souhaitable, subordonnés au suivi » inchangée). Les six autres simplifications restent à décider par l'utilisateur (DOU-126 « Simplifications possibles des scénarios : choix de l'utilisateur », ouvert, non bloquant). Précise DEC-160 « Cadrage des besoins : contraintes du projet et simplification n°1 recommandée » (la n°1 recommandée est écartée par l'utilisateur) et DEC-159 « Réglage et suivi alignés en Souhaitable, subordonnés au suivi » (priorités confirmées).
**Alternatives écartées :** retirer le sans fil de réglage et de suivi (recommandation de l'architecte : gain en radio, protocole, mode réglage ; coût en arrêt sans fil, suivi et cause lisible).
**Raison :** décision de l'utilisateur en chat, 2026-10-29 : « on garde la communication sans fils ».
**Doutes levés :** (aucun) ; DOU-126 « Simplifications possibles des scénarios : choix de l'utilisateur » reçoit une réponse partielle

### DEC-164 — Seconde relecture de porte : énoncés des besoins repris
**Date :** 2026-10-29
**Concerne :** BES-001 « Lancer le drone à la main » à BES-013 « Voler en appartement avec un drone de poche protégé » (BES-006 « Arrêter le drone en vol d'un geste », BES-010 « Suivre le drone sur un appareil de suivi » et BES-011 « Fabriquer et programmer le drone soi-même » sont aussi traités par DEC-165 « Arrêt sans fil déplacé de BES-006 vers BES-010 » et DEC-166 « BES-011 retitré : fabriquer et programmer le drone soi-même »)
**Décision :** BES-001 « Lancer le drone à la main » : les moteurs démarrent au relâchement du bouton armé, note « essais » conservée. BES-002 « Ne pas armer ni lancer par erreur » : un appui bref ne fait ni armer ni lancer, le seul renoncement après l'armement est de maintenir le bouton jusqu'au désarmement, relâcher plus tôt démarre les moteurs (risque accepté ; DEC-083 « Annulation d'un armement : le maintien jusqu'au désarmement à 10 s reste la seule annulation », DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard »), « hésitant » et « involontaire » supprimés car non testables. BES-003 « Rester en vol stationnaire 10 s puis atterrir doucement » : critères aux exigences (DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais »). BES-004 « Ne pas voler quand le drone n'est pas prêt » : une seule intention, refuser le départ ; la promesse d'énergie pour un vol complet est remplacée par un refus sous un seuil de batterie, durée de vol garantie à fixer (DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? », DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs ») ; mode réglage et décollage en réglage déplacés dans BES-008 « Entrer en mode réglage et faire des vols de réglage » ; SCN-011 « Dégradé : coupure d'alimentation en vol » ajouté aux références ; « prêt » défini au glossaire. BES-005 « Couper les moteurs quand le vol ne peut pas continuer » : causes exactes (stationnaire non atteint, basculement, atterrissage trop long, batterie trop basse, logiciel bloqué ou alimentation coupée), pannes de moteur ou de capteur non détectées, sous-tension d'un drone laissé allumé rattachée à SCN-012 « Dégradé : sous-tension de la batterie » et au même effet. BES-007 « Savoir où en est le drone sans autre appareil » : liste complétée (appui validé, désarmement, mode réglage), signaux perceptibles, exceptions dites (bouton coincé sans signal local, aucun signal après coupure d'alimentation ou sous-tension, cause de coupure non conservée : DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté »), SCN-004 « Appui normal : bouton relâché avant 2 secondes » ajouté. BES-008 « Entrer en mode réglage et faire des vols de réglage » : refus d'entrer en mode réglage ou de décoller en réglage, limite « lien perdu en vol de réglage » (DEC-106 « Lien sans fil perdu en vol de réglage : aucune action particulière »), « usage normal » devient « mode normal ». BES-009 « Régler et sauvegarder les paramètres de vol » : aucun réglage ne désactive les coupures de sécurité (DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » ; DEC-068 « Seuil hors bornes : refus silencieux, valeur relue sur l'appareil de suivi »), valeurs d'origine rattachées à BES-011 « Fabriquer et programmer le drone soi-même », la phrase « seul recours = reprogrammer » passe dans les contraintes. BES-013 « Voler en appartement avec un drone de poche protégé » : DEC-016 « Public adulte, protège-hélices obligatoires » citée pour les seuls protège-hélices, « Note » fusionnée dans l'énoncé. Vocabulaire : « propriétaire » devient « utilisateur », « information locale » devient « signal ». Parcours : flèche en pointillé Atterrissage vers Arrêt en vol, étiquettes « Signaux sur le drone » et « Lieu et protège-hélices ». La section sur les écarts de l'outil de porte quitte l'annexe A pour une annexe D. Modifie DEC-158 « Énoncés des besoins resserrés : une intention, testable, sans solution ».
**Alternatives écartées :** garder les énoncés de DEC-158 « Énoncés des besoins resserrés : une intention, testable, sans solution » (relecture `critique` : formulations non testables ou en contradiction avec les scénarios) ; ajouter des besoins (le jeu reste à treize besoins).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun) ; ouvre DOU-128 « Durée minimale perceptible des signaux » et DOU-129 « Plage de lancer et hauteur d'un appartement (plafond) »

### DEC-165 — Arrêt sans fil déplacé de BES-006 vers BES-010
**Date :** 2026-10-29
**Concerne :** BES-006 « Arrêter le drone en vol d'un geste » et BES-010 « Suivre le drone sur un appareil de suivi »
**Décision :** BES-006 « Arrêter le drone en vol d'un geste » ne porte que le bouton : après la garde qui suit le lancer, un appui coupe les moteurs rapidement (DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » ; DEC-087 « Arrêt d'urgence par le bouton en vol : anti-rebond très court seulement, arrêt quasi immédiat »), en priorité Essentiel, sans « facultative ». La commande d'arrêt sans fil passe dans BES-010 « Suivre le drone sur un appareil de suivi » (Souhaitable), qui fournit la liaison sans fil (suivi, causes de refus et de coupure, variables du vol, arrêt sans fil) ; SCN-003 « Échec : batterie faible à l'armement », SCN-006 « Échec : inclinaison excessive après le stationnaire » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol » y sont ajoutés. Le titre de BES-010 « Suivre le drone sur un appareil de suivi » est conservé.
**Alternatives écartées :** garder l'arrêt sans fil facultatif dans un besoin Essentiel (priorité floue) ; créer un besoin à part (le jeu reste à treize besoins).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-166 — BES-011 retitré : fabriquer et programmer le drone soi-même
**Date :** 2026-10-29
**Concerne :** BES-011 « Fabriquer et programmer le drone soi-même » (ancien titre : « Programmer le drone depuis l'ordinateur »)
**Décision :** BES-011 « Fabriquer et programmer le drone soi-même » devient le parent des futures exigences de fabrication : l'utilisateur assemble l'électronique à la main avec des composants accessibles et programme le drone depuis son ordinateur (DEC-144 « Ligne directrice : simplicité, un seul utilisateur qui accepte les risques » ; SCN-008 « Mise en service : programmation du drone »). La contrainte correspondante devient un renvoi dans « Contraintes du projet ». L'identifiant est conservé, le nouveau titre est propagé dans les documents. Priorité Essentiel inchangée.
**Alternatives écartées :** garder la fabrication en simple contrainte (aucun besoin en amont des exigences de fabrication) ; créer un quatorzième besoin (le jeu reste à treize).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-167 — BES-012 : contrôle croisé, consignes complétées, DOU-127 levé
**Date :** 2026-10-29
**Concerne :** BES-012 « Disposer d'une page de consignes d'emploi » et « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md`
**Décision :** la page rappelle les risques majeurs et ceux qui demandent un geste de l'utilisateur ; l'inspection est un contrôle croisé avec « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (35 risques, 36 numéros), sans exigence de reprendre chaque ligne. La page passe à 42 consignes : quatre réflexes essentiels en tête, dont « Hélices en rotation : ne pas toucher le drone ; maintenir le bouton ou attendre l'arrêt » et « Drone au sol et hélices arrêtées : en cas de doute, débrancher la batterie » (cohérents avec BES-006 « Arrêter le drone en vol d'un geste » et la ligne 26 des risques acceptés) ; consignes ajoutées : parasites sur le bouton, bouton coincé, pas de réglage après un échec d'initialisation, rester à portée du sans fil, vérifier un drone neuf, bornes des réglages ; « après une chute ou un posé » (drone verrouillé, allumé, rien à rebrancher) séparé de « démarrage raté » (débrancher puis rebrancher) ; verbe « débrancher » unifié avec le glossaire. Précise DEC-162 « Consignes d'emploi : une consigne par ligne, les dangers en tête ».
**Alternatives écartées :** reprendre chaque ligne des risques acceptés dans la page (lourd, contraire à DEC-154 « Notice des limites d'emploi : une page de consignes d'emploi ») ; garder DOU-127 « Couverture ligne à ligne des risques acceptés par les consignes d'emploi » ouvert (l'exigence de couverture ligne à ligne disparaît).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-127 « Couverture ligne à ligne des risques acceptés par les consignes d'emploi »

### DEC-168 — Annexe B des besoins : quatre colonnes, simplifications n°2 à n°7 recommandées
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`, section « Annexe B — Simplifications possibles »
**Décision :** après DEC-163 « Communication sans fil conservée : simplification n°1 écartée », le tableau passe à quatre colonnes (numéro, simplification, gain et coût en une phrase, recommandation) ; la n°1 est réduite à une phrase hors tableau (« Écartée ») ; les n°2, 4, 5, 6 et 7 sont « Recommandée », la n°3 « Recommandée (se décide aux exigences) » ; la variante « entrer en mode réglage par le sans fil » est retirée de la n°2 (elle aggraverait le risque sans appairage). L'introduction dit que la n°1 était la seule à retirer un scénario et que les autres modifient des détails de scénarios validés, à reprendre avec l'accord de l'utilisateur. Pas de colonne « Décision » (aucune décision à y inscrire). Précise DEC-160 « Cadrage des besoins : contraintes du projet et simplification n°1 recommandée ».
**Alternatives écartées :** garder « Inutile si la n°1 est retenue » (n°1 écartée) ; garder la colonne « Décision » vide.
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun) ; DOU-126 « Simplifications possibles des scénarios : choix de l'utilisateur » reste ouvert

### DEC-169 — Trois priorités définies : Essentiel, Important, Souhaitable
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md` et « Glossaire » — `projets/boomrone/00-glossaire.md`
**Décision :** Essentiel = sans lui le drone ne vole pas ou n'est pas utilisable ; Important = prévu et attendu ; Souhaitable = prévu et conservé (le sans fil est gardé), livré après les autres, sans valoir « facultatif ». Définitions dans le glossaire, rappelées avant le tableau récapitulatif et dans l'aperçu de « Besoins ». Décompte recompté après les changements : 7 Essentiels (BES-001 « Lancer le drone à la main », BES-003 « Rester en vol stationnaire 10 s puis atterrir doucement », BES-004 « Ne pas voler quand le drone n'est pas prêt », BES-005 « Couper les moteurs quand le vol ne peut pas continuer », BES-006 « Arrêter le drone en vol d'un geste », BES-007 « Savoir où en est le drone sans autre appareil », BES-011 « Fabriquer et programmer le drone soi-même »), 3 Importants (BES-002 « Ne pas armer ni lancer par erreur », BES-012 « Disposer d'une page de consignes d'emploi », BES-013 « Voler en appartement avec un drone de poche protégé »), 3 Souhaitables (BES-008 « Entrer en mode réglage et faire des vols de réglage », BES-009 « Régler et sauvegarder les paramètres de vol », BES-010 « Suivre le drone sur un appareil de suivi »). Précise DEC-147 « Priorités des besoins : le vol sûr d'abord, le réglage et le suivi ensuite ».
**Alternatives écartées :** laisser le mot « Souhaitable » sans définition (lu comme « facultatif », contraire à DEC-163 « Communication sans fil conservée : simplification n°1 écartée »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-170 — Consigne d'arrêt en vol par le bouton : formulation prudente
**Date :** 2026-10-29
**Concerne :** « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md` et BES-006 « Arrêter le drone en vol d'un geste »
**Décision :** « Pour arrêter un drone en vol, appuie sur le bouton ; fais-le avec prudence, les hélices tournent » ; « ne pas attraper le drone » vaut pour les autres cas. BES-006 « Arrêter le drone en vol d'un geste » parle d'un appui franchissant l'anti-rebond. Écart BES-007 « Savoir où en est le drone sans autre appareil » / BES-008 « Entrer en mode réglage et faire des vols de réglage » noté dans BES-007 « Savoir où en est le drone sans autre appareil ». Retouches de forme associées (réflexe 4, titre du diagramme, contraintes du projet).
**Alternatives écartées :** interdire de toucher le drone (rend l'arrêt par le bouton impossible).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : simplicité, utilisateur qui accepte les risques.
**Doutes levés :** (aucun) ; DOU-130 « Arrêt d'un drone en vol par le bouton sans le toucher » ouvert

### DEC-171 — Porte besoins franchie : accord explicite de l'utilisateur
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md` (BES-001 « Lancer le drone à la main » à BES-013 « Voler en appartement avec un drone de poche protégé »)
**Décision :** la porte « besoins » est franchie ; les treize besoins passent à « Validé » ; la phase « exigences » peut s'ouvrir. État au franchissement : tag `gate-2-besoins-ready-v0`, aucun doute bloquant ouvert, 29 doutes non bloquants (liste dans `registre-doutes.md`), deux passes de relecture de porte (`critique`, `coherence-clarte`, `exigences-tracabilite`) plus une vérification ciblée.
**Alternatives écartées :** continuer la phase « besoins » (aucun doute bloquant, toutes les décisions demandées sont prises).
**Raison :** accord explicite de l'utilisateur en chat, 2026-10-29 : « passons la porte ». Rappels : `check_traceability --gate` échoue pour les douze « SCN sans BES » (défaut connu de l'outil, DEC-156 « Couverture des scénarios vérifiée à la main, outil de traçabilité inchangé » ; couverture vérifiée à la main) et pour les « BES sans REQ » et « BES sans TA » (phases suivantes) ; DOU-126 « Simplifications possibles des scénarios : choix de l'utilisateur » (six simplifications) reste ouvert, à trancher avant les exigences concernées ; si les essais contredisent la plage de lancer, les besoins seront à reprendre (DOU-116 « Échéance et circularité du report aux essais, comportement de SCN-002 sur la partie infaisable de la plage », DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m », DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal »).
**Doutes levés :** (aucun)

### DEC-172 — Délégation de la phase exigences à l'architecte
**Date :** 2026-10-29
**Concerne :** « Exigences système » — `projets/boomrone/02-exigences.md` et « Plans de test » — `projets/boomrone/05-plans-de-test.md`
**Décision :** pour la phase « exigences » seulement, l'utilisateur ne veut aucune question : l'architecte décide seul, consigne chaque choix en DEC et prépare un dossier fini. Cette délégation remplace pour cette phase la règle « l'utilisateur décide » ; la porte « exigences » n'est pas franchie par l'architecte, l'accord explicite de l'utilisateur reste requis. Elle couvre aussi le choix des six simplifications de DOU-126 « Simplifications possibles des scénarios : choix de l'utilisateur ».
**Alternatives écartées :** poser les questions une à une (refusé par l'utilisateur) ; franchir aussi la porte (l'accord explicite de l'utilisateur reste obligatoire, charte §3).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité. Même régime que DEC-143 « Délégation de la phase besoins à l'architecte ».
**Doutes levés :** (aucun)

### DEC-173 — Ligne directrice de la phase exigences : simplicité, valeurs chiffrées, aucune solution
**Date :** 2026-10-29
**Concerne :** « Exigences système » — `projets/boomrone/02-exigences.md`
**Décision :** reprise de DEC-144 « Ligne directrice : simplicité, un seul utilisateur qui accepte les risques » : premier drone, jeu, un seul utilisateur qui accepte les risques, fabrique et programme lui-même. En cas de choix, l'option la plus simple à utiliser, à spécifier, à fabriquer et à programmer. Une exigence énonce un comportement mesurable (valeur, tolérance, méthode de vérification) et ne nomme aucun composant, broche, bus ni langage : cela reste à l'architecture. Les valeurs sont reprises des scénarios et des décisions ; à défaut, une valeur simple est posée et marquée « provisoire, à valider aux essais sur prototype ».
**Alternatives écartées :** exigences à solution imposée (composants, protocoles : c'est l'architecture) ; exigences qualitatives sans valeur (non testables).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-174 — Trente-quatre exigences : regroupements, champs et priorités
**Date :** 2026-10-29
**Concerne :** REQ-001 « Anti-rebond du bouton » à REQ-034 « Page de consignes d'emploi »
**Décision :** 34 exigences en 10 groupes (bouton et départ, vol normal, coupures et arrêt, initialisation, information, sans fil, réglage, fabrication, cadre d'emploi, consignes), au lieu des 45 à 55 estimées. Les règles transversales sont factorisées en une exigence qui cite plusieurs besoins : chronologie du bouton (REQ-002 « Chronologie d'un appui sur le bouton »), invariant de démarrage (REQ-005 « Démarrage des moteurs sur geste volontaire seulement »), verrouillage (REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage »), coupures automatiques (REQ-011 « Coupures automatiques en vol »), effets locaux (REQ-018 « Effets locaux par situation »), commandes sans fil par état (REQ-023 « Commandes sans fil selon l'état du drone »), valeurs de sécurité (REQ-026 « Paramètres de vol réglables »). Champs d'une exigence du projet : `Réfs amont` (besoins seulement, le principal en premier), `Décisions liées` (3 au plus), `Énoncé`, `Priorité`, `Vérification`, `Statut`. La priorité est la plus haute des besoins cités. Les 13 besoins ont au moins une exigence (annexe A de « Exigences système »).
**Alternatives écartées :** une exigence par signal, par cas de bouton ou par ligne des tableaux (45 à 55 exigences, doublons) ; une exigence par besoin (13 exigences trop larges pour être testables).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)
**Modifiée par :** DEC-195 « Relecture de porte exigences : corrections décidées par délégation, identifiants conservés » (le total devient 45 exigences après la relecture de porte) le 2026-10-29

### DEC-175 — Simplification n°2 adoptée : mode réglage par le bouton tenu à la mise sous tension
**Date :** 2026-10-29
**Concerne :** REQ-024 « Entrée en mode réglage par le bouton », REQ-002 « Chronologie d'un appui sur le bouton »
**Décision :** le mode réglage s'entre en maintenant le bouton enfoncé de la mise sous tension jusqu'à la fin d'une initialisation réussie (drone immobile et à plat) ; le drone donne l'effet Mode réglage. La série de trois appuis, le compteur d'appuis, l'écart de 2 s entre appuis et la règle « armement seulement depuis le premier appui d'une série » disparaissent : tout appui suit la chronologie de REQ-002 « Chronologie d'un appui sur le bouton ». L'effet « Appui validé » à 1 s est conservé (BES-007 « Savoir où en est le drone sans autre appareil » le liste). Un bouton coincé au démarrage mène donc au mode réglage, avec son effet. Modifie SCN-004 « Appui normal : bouton relâché avant 2 secondes », SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-010 « Échec : initialisation impossible au démarrage » ; remplace DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage » (trois appuis), DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série » (premier appui d'une série), DEC-084 « Appui ignoré pendant une série d'appuis : aucun signal, risque accepté et documenté » (appui ignoré dans une série), DEC-089 « Appui de moins de 1 s au milieu d'une série d'appuis : compteur remis à zéro », DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus », DEC-093 « Mode réglage refusé : retour à l'attente, compteur à zéro, bouton encore enfoncé ignoré » et DEC-115 « Troisième appui encore maintenu à l'entrée en mode réglage : maintien ignoré jusqu'au premier relâchement » pour l'entrée (le maintien du bouton à l'entrée reste ignoré jusqu'au premier relâchement) ; précise DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement » et DEC-088 « Bouton coincé ou maintenu en permanence au démarrage : statut sans fil seulement, aucun signal local ». Signalé : les énoncés de BES-007 « Savoir où en est le drone sans autre appareil » (exception du bouton coincé) et de BES-008 « Entrer en mode réglage et faire des vols de réglage » (référence à DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie ») sont partiellement périmés ; les besoins ne sont pas modifiés.
**Alternatives écartées :** garder les trois appuis (compteur, état de série, appui ignoré sans signal, un risque accepté de plus) ; entrée par commande sans fil (aggrave le risque sans appairage, déjà écartée à l'annexe B des besoins) ; appui long dédié (se confond avec la fenêtre d'armement de 2 s à 10 s).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité (moins d'états à écrire et à tester).
**Doutes levés :** DOU-112 « Bouton enfoncé jusqu'à la fin de l'initialisation : état et signal »

### DEC-176 — Simplification n°3 adoptée : dix effets locaux au lieu de dix-sept signaux
**Date :** 2026-10-29
**Concerne :** REQ-018 « Effets locaux par situation », REQ-019 « Perceptibilité et distinction des effets » ; modifie SCN-001 « Vol nominal : de la batterie au posé » (liste des signaux)
**Décision :** les dix-sept états de « Scénarios d'utilisation » restent des statuts sans fil distincts (REQ-020 « Statut sans fil »), mais sur le drone ils se regroupent en dix effets locaux distincts : Allumé, Appui validé, Prêt, Vol (Lancé, Stabilisation, En vol stationnaire, Atterrissage), Posé, Refus, Désarmement, Coupure en vol (les cinq causes), Échec d'initialisation, Mode réglage. Chaque situation de BES-007 « Savoir où en est le drone sans autre appareil » reste distincte. Effets d'événement (Appui validé, Posé, Refus, Désarmement, Coupure en vol) : durée d'au moins 0,5 s, même si l'état suivant est déjà atteint ; effets d'état : tant que l'état dure. Perceptibilité : à 1 m, lumière dans une pièce éclairée (300 lux environ), son moteurs arrêtés. Précise DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie » et DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté » : « Allumé » prend toujours le relais tout de suite pour l'état et le statut sans fil, mais l'effet de la coupure reste perçu 0,5 s (la durée « aucune » de DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté » est remplacée par 0,5 s, sans mémoire de la cause sur le drone).
**Alternatives écartées :** dix-sept effets distincts (plus de motifs à écrire, à régler et à distinguer) ; moins de dix effets (fusionner Refus et Désarmement ou Posé et Allumé rendrait BES-007 « Savoir où en est le drone sans autre appareil » non testable) ; durée nulle pour la coupure (non testable, DOU-128 « Durée minimale perceptible des signaux »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-128 « Durée minimale perceptible des signaux »
**Modifiée par :** DEC-197 « Effet Lancé et vol : pas d'onzième effet » (l'effet n°4 s'appelle Lancé et vol) ; DEC-212 « Effets locaux : lumière ou son, distinction en une passe » (lumière ou son, distinction en une passe) le 2026-10-29

### DEC-177 — Simplification n°4 adoptée : commandes sans fil acceptées seulement en mode réglage
**Date :** 2026-10-29
**Concerne :** REQ-023 « Commandes sans fil selon l'état du drone », REQ-026 « Paramètres de vol réglables », REQ-027 « Sauvegarde et chargement des réglages » ; modifie SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-010 « Échec : initialisation impossible au démarrage »
**Décision :** Décoller, Modifier et Sauvegarder ne sont acceptées qu'en mode réglage (Décoller et Sauvegarder au sol, moteurs coupés ; Modifier au sol et en vol de réglage) ; Arrêt n'agit qu'en vol (normal ou de réglage). Toute autre combinaison est ignorée sans effet. Le tableau des commandes passe de dix lignes à quatre ; Modifier en vol normal (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ») est retirée en même temps (plus de réglage par un tiers pendant un vol normal). Remplace le tableau de DEC-043 « Commandes sans fil acceptées selon l'état du drone » et les règles de Sauvegarder de DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer », DEC-120 « Sauvegarder ignorée pendant l'initialisation en cours, Modifier acceptée ; cas de l'échec d'initialisation non tranché », DEC-123 « Sauvegarder ignorée aussi à l'état Premier appui validé », DEC-128 « Sauvegarder ignorée aussi à l'état Série d'appuis en cours », DEC-131 « Sauvegarder ignorée en vol : confirmation du tableau des commandes », DEC-136 « Écriture de réglages commencée à l'état Allumé et encore en cours au relâchement du lancer : risque accepté » ; lève trois risques acceptés (lignes 4, 9 et 36 de « Risques acceptés »).
**Alternatives écartées :** garder le tableau de dix lignes (états à coder et à tester un par un) ; garder Modifier en vol normal (réglage à distance d'un drone en vol, par un tiers sans appairage).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-113 « Ordre entre Modifier pendant l'initialisation et chargement des réglages enregistrés »

### DEC-178 — Simplification n°5 adoptée : échec d'initialisation, toutes les commandes sans fil ignorées
**Date :** 2026-10-29
**Concerne :** REQ-017 « Initialisation en 3 secondes », REQ-023 « Commandes sans fil selon l'état du drone » ; modifie SCN-010 « Échec : initialisation impossible au démarrage »
**Décision :** à l'état « Échec d'initialisation » (et pendant « Initialisation en cours »), les quatre commandes sans fil sont ignorées ; le statut sans fil reste émis. Remplace DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » (Modifier et Sauvegarder acceptées) et DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté » (écrasement des réglages par un tiers) ; lève le risque accepté de la ligne 11 de « Risques acceptés ».
**Alternatives écartées :** Modifier acceptée en échec d'initialisation (cas à tester et risque d'écrasement).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-114 « Réglages enregistrés chargés ou non à l'état d'échec d'initialisation »

### DEC-179 — Simplification n°6 adoptée : statut sans fil par code d'état et dernières causes
**Date :** 2026-10-29
**Concerne :** REQ-020 « Statut sans fil » ; modifie SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-003 « Échec : batterie faible à l'armement »
**Décision :** le statut sans fil porte trois champs : l'état courant (un des dix-sept codes), la dernière cause de refus (batterie faible, drone en mouvement, drone pas à plat ; plusieurs possibles) et la dernière cause de coupure en vol (six valeurs : les cinq causes et la sous-tension), conservées jusqu'à la mise hors tension. Plus de liste de causes précises à fixer (précise DEC-101 « Statut sans fil d'un refus : cause précise, liste exacte à fixer en architecture »), plus de statut « bouton maintenu », plus de statut de refus « lisible jusqu'à la commande suivante » (DEC-102 « Décollage de réglage refusé : signal Refus, statut de refus lisible jusqu'à la commande suivante » remplacée). La cause de sous-tension y figure quand le drone reste alimenté.
**Alternatives écartées :** une liste détaillée de causes (plus de cas à coder et à tester) ; un seul code d'état sans cause (BES-010 « Suivre le drone sur un appareil de suivi » perdrait « causes de refus et de coupure »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-117 « Cause de sous-tension sur le statut sans fil »

### DEC-180 — Simplification n°7 adoptée : valeurs de sécurité fixes dans le logiciel
**Date :** 2026-10-29
**Concerne :** REQ-026 « Paramètres de vol réglables », REQ-011 « Coupures automatiques en vol » ; modifie SCN-002 « Échec : stationnaire non atteint dans le délai », SCN-006 « Échec : inclinaison excessive après le stationnaire » et SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** les valeurs de sécurité (délai de stationnaire 2 s, angle de basculement 60° et sa durée, délai d'atterrissage 15 s, seuils de batterie, hauteur minimale, durées des chiens de garde) sont fixes dans le logiciel : seule la reprogrammation les change. Les autres paramètres de vol sont réglables sans borne. Plus de bornes numériques à définir ni de refus silencieux d'une valeur hors bornes. Remplace DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » (bornes) et DEC-068 « Seuil hors bornes : refus silencieux, valeur relue sur l'appareil de suivi » (refus silencieux hors bornes) ; BES-009 « Régler et sauvegarder les paramètres de vol » reste satisfait (aucun réglage ne désactive les coupures).
**Alternatives écartées :** seuils réglables dans des bornes (bornes à fixer, refus à coder, et la coupure de sécurité reste atteignable par un tiers sans appairage).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » (bornes devenues sans objet ; valeurs et durées fixées par DEC-182 « Valeurs du bouton : 1 s, 2 s, 10 s, anti-rebond, garde, délai des moteurs » à DEC-187 « Valeurs du cadre d'emploi : poche, protège-hélices, pièce d'essai » ; tolérance d'immobile renvoyée à DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal » ; liste des paramètres réglables renvoyée à l'architecture)

### DEC-181 — Simplifications de l'annexe B tranchées : DOU-126 levé
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`, annexe B ; « Scénarios d'utilisation » — `projets/boomrone/00-scenarios.md`
**Décision :** bilan : n°1 écartée par l'utilisateur (DEC-163 « Communication sans fil conservée : simplification n°1 écartée ») ; n°2 à n°7 adoptées, toutes recommandées (DEC-175 « Simplification n°2 adoptée : mode réglage par le bouton tenu à la mise sous tension », DEC-176 « Simplification n°3 adoptée : dix effets locaux au lieu de dix-sept signaux », DEC-177 « Simplification n°4 adoptée : commandes sans fil acceptées seulement en mode réglage », DEC-178 « Simplification n°5 adoptée : échec d'initialisation, toutes les commandes sans fil ignorées », DEC-179 « Simplification n°6 adoptée : statut sans fil par code d'état et dernières causes », DEC-180 « Simplification n°7 adoptée : valeurs de sécurité fixes dans le logiciel »). Les scénarios sont mis à jour de façon minimale : un encart au début de « Scénarios d'utilisation » liste les six modifications, les phrases et tableaux contradictoires sont corrigés, les mots devenus vides (série d'appuis, compteur) sont déclarés sans objet. Aucun besoin n'est modifié ; les écarts à signaler sont dans le rapport de phase (BES-007 « Savoir où en est le drone sans autre appareil », BES-008 « Entrer en mode réglage et faire des vols de réglage », BES-009 « Régler et sauvegarder les paramètres de vol »).
**Alternatives écartées :** n'en adopter que quelques-unes (chacune retire de la logique à coder, l'utilisateur veut peu de fonctions) ; réécrire les scénarios (hors de la consigne « minimal »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-126 « Simplifications possibles des scénarios : choix de l'utilisateur »

### DEC-182 — Valeurs du bouton : 1 s, 2 s, 10 s, anti-rebond, garde, délai des moteurs
**Date :** 2026-10-29
**Concerne :** REQ-001 « Anti-rebond du bouton », REQ-002 « Chronologie d'un appui sur le bouton », REQ-004 « Démarrage des moteurs 200 ms après le relâchement », REQ-015 « Garde du bouton après le lancer »
**Décision :** valeurs des scénarios reprises, provisoires, à valider aux essais : appui validé à 1,0 s (±0,1 s) ; contrôle d'armement à 2,0 s (±0,1 s) ; désarmement au-delà de 10,0 s (±0,2 s) depuis l'appui initial ; moteurs 200 ms (±50 ms) après le relâchement, effet Lancé au plus 50 ms après ; garde de 0,5 s (±0,1 s) ; anti-rebond unique de 10 ms (±2 ms) pour tout le bouton. Plus de délai entre appuis (série supprimée par DEC-175 « Simplification n°2 adoptée : mode réglage par le bouton tenu à la mise sous tension »).
**Alternatives écartées :** deux anti-rebonds (un au sol, un en vol : deux réglages) ; garde plus longue (retarde l'arrêt par réflexe) ; anti-rebond de 5 ms (rebonds d'un bouton ordinaire).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-080 « Seuils de temps du bouton : 1 s, 2 s, 10 s et délai entre appuis »

### DEC-183 — Valeurs de départ : immobile, à plat, batterie à l'armement
**Date :** 2026-10-29
**Concerne :** REQ-003 « Conditions de départ du drone », REQ-017 « Initialisation en 3 secondes »
**Décision :** valeurs provisoires, à valider aux essais : « immobile » = vitesse de rotation ≤ 30 °/s et norme de l'accélération mesurée entre 9,3 et 10,3 m/s² pendant 0,5 s ; « à plat » = inclinaison ≤ 15° (une seule valeur pour l'initialisation, l'armement, le mode réglage et le critère de stationnaire) ; initialisation terminée en 3 s au plus. Un seuil unique de batterie sert à l'armement et à Décoller (DEC-186 « Valeurs de batterie : seuils par élément, confirmation, vol complet »). La tolérance d'immobile reste un doute d'essai (DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal »).
**Alternatives écartées :** deux inclinaisons (10° au vol, 15° au sol) ; tolérance d'immobile plus serrée (armement dans la main impossible : DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun) ; DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal » reste ouvert, valeur provisoire écrite

### DEC-184 — Valeurs du vol : lancer, stationnaire, hauteur, dérive, atterrissage
**Date :** 2026-10-29
**Concerne :** REQ-006 « Stabilisation après le lancer », REQ-007 « Critère de vol stationnaire », REQ-008 « Tenue du vol stationnaire », REQ-009 « Atterrissage doux »
**Décision :** plage de lancer de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » inchangée (toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol) avec une rotation d'au plus 1 tour/s (360 °/s) au relâchement (provisoire, DOU-010 « Quelle rotation au lancer le drone doit-il rattraper ? ») ; stationnaire en 2,0 s dans au moins 90 % de 20 lancers (provisoire, DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m ») ; critère de stationnaire : inclinaison ≤ 15°, vitesse ≤ 0,3 m/s, hauteur ≥ 0,3 m ; hauteur de stationnaire visée 1,0 m (tolérance ±0,2 m, de la 3e à la 10e seconde) ; dérive horizontale ≤ 1,0 m exigée, 0,3 m en objectif mesuré (DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais ») ; atterrissage à 0,5 m/s au plus, moteurs coupés à 2 à 3 cm du sol, en 15 s au plus. Hauteur fixe de 1,0 m : prévisible, compatible avec un plafond d'appartement et avec la durée d'atterrissage de 15 s.
**Alternatives écartées :** tenir la hauteur atteinte au lancer (dépend du lancer, peut frôler le plafond) ; altitude à ±10 cm (précision de mesure incertaine pour un premier drone) ; exigence de dérive 0,3 m (non garantie : DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-009 « Quelle tolérance d'altitude pendant les 10 secondes de stationnaire ? », DOU-010 « Quelle rotation au lancer le drone doit-il rattraper ? », DOU-011 « Quelle dérive horizontale reste acceptable si 30 cm n'est pas tenu ? », DOU-035 « Quelle hauteur de stationnaire vise-t-on ? »
**Modifiée par :** DEC-200 « Hauteur visée 1,0 m, dérive 0,5 m, pièce d'essai 4 m × 4 m × 2,5 m » (dérive exigée de 0,5 m au lieu de 1,0 m) le 2026-10-29

### DEC-185 — Valeurs de coupure : basculement, pas de limite de dérive ni d'altitude
**Date :** 2026-10-29
**Concerne :** REQ-011 « Coupures automatiques en vol », REQ-033 « Vol dans une pièce d'appartement »
**Décision :** basculement : inclinaison > 60° (±5°) pendant plus de 0,1 s après le stationnaire, coupure ≤ 100 ms après la détection. Aucune coupure sur dérive entre 15° et 60° (DOU-028 « Faut-il une limite de dérive avant la coupure, entre 10° et 60° d'inclinaison ? »), aucune limite d'altitude ni réaction au plafond (DOU-029 « Quelle altitude maximale et quel plafond le drone doit-il tolérer ? ») : risque accepté, ajouté à « Risques acceptés » (ligne 37), rappelé aux consignes. La compatibilité plage de lancer et plafond (DOU-129 « Plage de lancer et hauteur d'un appartement (plafond) ») relève de l'utilisateur, qui adapte le lancer au lieu (DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu », ligne 30 des risques) ; l'essai d'appartement se fait en lancer doux dans une pièce de 3 m × 3 m × 2,5 m.
**Alternatives écartées :** coupure sur dérive ou sur altitude (capteurs et seuils de plus, fausses coupures) ; limiter la plage de lancer pour l'appartement (contredit DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée », plage inchangée).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-012 « Quel angle limite et quelles autres valeurs de coupure retenir ? », DOU-028 « Faut-il une limite de dérive avant la coupure, entre 10° et 60° d'inclinaison ? », DOU-029 « Quelle altitude maximale et quel plafond le drone doit-il tolérer ? », DOU-129 « Plage de lancer et hauteur d'un appartement (plafond) »

### DEC-186 — Valeurs de batterie : seuils par élément, confirmation, vol complet
**Date :** 2026-10-29
**Concerne :** REQ-003 « Conditions de départ du drone », REQ-012 « Coupure sur sous-tension de la batterie », REQ-013 « Marge de batterie pour un vol complet »
**Décision :** valeurs provisoires par élément de batterie lithium, à valider aux essais : seuil d'armement 3,7 V à vide (±0,05 V) ; seuil de sous-tension 3,3 V sous charge, confirmé 100 ms (±20 ms) avant la coupure, sans hystérésis (la coupure dure jusqu'au débranchement) ; vol complet de 30 s (27,2 s de vol maximal plus une marge) garanti à partir d'une batterie juste acceptée à 3,7 V. Le même seuil sert à Décoller en mode réglage. La tension est lue en continu, moteurs en marche.
**Alternatives écartées :** marge ×2 sur la durée (60 s : seuil d'armement trop haut, batterie refusée trop tôt) ; hystérésis et seuil d'alerte (fonctions de plus, DEC-140 « Chute brutale sur sous-tension maintenue en connaissance de cause, sans seuil d'alerte »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? », DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs », DOU-119 « Filtrage, hystérésis et mesure sous charge de la tension »
**Modifiée par :** DEC-210 « Délais uniques : atterrissage 15,0 s ±0,5 s, sous-tension 250 ms, vol de réglage scindé » (délai unique de 250 ms pour la sous-tension) le 2026-10-29

### DEC-187 — Valeurs du cadre d'emploi : poche, protège-hélices, pièce d'essai
**Date :** 2026-10-29
**Concerne :** REQ-031 « Drone de poche », REQ-032 « Protège-hélices », REQ-033 « Vol dans une pièce d'appartement »
**Décision :** valeurs provisoires : drone de poche = au plus 100 mm × 100 mm × 50 mm, protège-hélices compris, et 100 g batterie comprise ; protège-hélices : un calibre de 12 mm de diamètre ne touche aucune hélice depuis l'extérieur ; pièce d'essai d'appartement : 3 m × 3 m × 2,5 m, lancer doux de 0,5 à 1 m/s depuis le centre, tout le vol dans la pièce, 9 vols sur 10.
**Alternatives écartées :** dimensions plus petites (impose des composants plus chers à braser) ; pièce plus grande (n'est plus un appartement type).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)
**Modifiée par :** DEC-200 « Hauteur visée 1,0 m, dérive 0,5 m, pièce d'essai 4 m × 4 m × 2,5 m » (pièce d'essai de 4 m × 4 m × 2,5 m au lieu de 3 m × 3 m × 2,5 m) le 2026-10-29

### DEC-188 — Bouton : un appui commencé avant une coupure ou un décollage est ignoré jusqu'au relâchement
**Date :** 2026-10-29
**Concerne :** REQ-016 « Arrêt d'urgence par le bouton », REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage »
**Décision :** règle unique : tout appui déjà en cours à un changement d'état (retour à l'attente, coupure des moteurs, décollage de réglage, entrée en mode réglage) est ignoré jusqu'à son premier relâchement ; seul un nouvel appui compte (front). Pour Décoller, un bouton déjà enfoncé n'est donc pas un arrêt d'urgence immédiat.
**Alternatives écartées :** niveau pris en compte à l'acceptation de Décoller (arrêt immédiat parasite, deux règles différentes).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité (une seule règle pour tous les cas).
**Doutes levés :** DOU-111 « Niveau ou front du bouton à l'acceptation de Décoller »
**Modifiée par :** DEC-205 « Bouton : règle unique de l'appui en cours, garde du lancer, Décoller refusé si le bouton est enfoncé » (pour Décoller, un bouton déjà enfoncé est refusé ; règle écrite dans une seule exigence) le 2026-10-29

### DEC-189 — Arrêt d'un drone en vol : bouton ou arrêt sans fil, pas d'autre option
**Date :** 2026-10-29
**Concerne :** REQ-016 « Arrêt d'urgence par le bouton », REQ-022 « Arrêt sans fil », REQ-034 « Page de consignes d'emploi »
**Décision :** l'arrêt sans fil existe déjà (REQ-022 « Arrêt sans fil », Souhaitable) pour qui n'a pas à toucher le drone ; sans appareil de suivi, seul le bouton arrête, et la consigne dit d'appuyer avec prudence (DEC-170 « Consigne d'arrêt en vol par le bouton : formulation prudente »). Aucune autre option n'est ajoutée.
**Alternatives écartées :** deuxième bouton ou télécommande dédiée (matériel de plus) ; interdire de toucher le drone (rend l'arrêt par le bouton impossible).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-130 « Arrêt d'un drone en vol par le bouton sans le toucher »

### DEC-190 — Recettes : un TA par scénario et trois TA par inspection
**Date :** 2026-10-29
**Concerne :** TA-001 « Recette du vol nominal » à TA-015 « Inspection de la fabrication à la main »
**Décision :** 15 recettes : une par scénario (douze, TA-001 « Recette du vol nominal » à TA-012 « Recette de la sous-tension de la batterie », qui rejouent le scénario) et trois par inspection pour les besoins sans scénario propre (TA-013 « Inspection des consignes d'emploi » pour BES-012 « Disposer d'une page de consignes d'emploi », TA-014 « Inspection du drone de poche protégé » pour BES-013 « Voler en appartement avec un drone de poche protégé », TA-015 « Inspection de la fabrication à la main » pour BES-011 « Fabriquer et programmer le drone soi-même »). Un TA cite les besoins couverts par le scénario en `Réfs amont` ; le scénario rejoué est écrit dans le champ texte `Scénario rejoué`.
**Alternatives écartées :** une recette par besoin (13 recettes qui ne rejouent pas les scénarios) ; pas de recette par inspection (BES-012 « Disposer d'une page de consignes d'emploi », BES-013 « Voler en appartement avec un drone de poche protégé » et BES-011 « Fabriquer et programmer le drone soi-même » resteraient sans recette propre).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-191 — Tests système : vingt-quatre TS, un par exigence ou groupe
**Date :** 2026-10-29
**Concerne :** TS-001 « Anti-rebond et chronologie d'un appui » à TS-024 « Page de consignes d'emploi »
**Décision :** 24 tests système couvrent les 34 exigences (chaque exigence a au moins un test) ; une exigence voisine d'une autre partage leur test quand l'essai est le même. Moyens simples : banc maison, alimentation de laboratoire, chronomètre ou caméra, oscilloscope ou analyseur logique, appareil de suivi, pièce d'essai. Pas encore de TI ni de TU : ils viennent avec l'architecture et la conception détaillée.
**Alternatives écartées :** un test par exigence (34 tests, essais répétés) ; un test par groupe (trop gros pour un verdict net).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)
**Modifiée par :** DEC-195 « Relecture de porte exigences : corrections décidées par délégation, identifiants conservés » (26 tests système au lieu de 24) le 2026-10-29

### DEC-192 — Outil de traçabilité inchangé : TA vers BES, scénario en champ texte, DEC en champ séparé
**Date :** 2026-10-29
**Concerne :** `tools/check_traceability.py`
**Décision :** l'outil n'est pas modifié. Il impose TA vers BES (un TA qui cite un scénario en `Réfs amont` est une erreur) et REQ vers BES, TS vers REQ : le scénario rejoué est donc écrit dans le champ `Scénario rejoué` des TA, et les décisions liées d'une exigence sont écrites dans le champ `Décisions liées`, jamais dans `Réfs amont` (une décision y serait signalée comme erreur). Les trous attendus avant l'architecture restent : les exigences sans ARC, et les 12 « SCN sans BES » (défaut connu, DEC-156 « Couverture des scénarios vérifiée à la main, outil de traçabilité inchangé »).
**Alternatives écartées :** modifier l'outil (interdit pour cette phase) ; citer les décisions dans `Réfs amont` (erreur de l'outil).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-193 — Documents liés mis à jour : scénarios, glossaire, consignes, risques acceptés
**Date :** 2026-10-29
**Concerne :** « Scénarios d'utilisation » — `projets/boomrone/00-scenarios.md`, « Glossaire » — `projets/boomrone/00-glossaire.md`, « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md`, « Risques acceptés » — `projets/boomrone/risques-acceptes.md`
**Décision :** mises à jour minimales pour qu'aucun texte ne contredise une exigence : encart et corrections dans les scénarios (voir DEC-181 « Simplifications de l'annexe B tranchées : DOU-126 levé ») ; glossaire : termes de la série d'appuis marqués sans objet, définitions de « Mode réglage » et de « Appui validé » corrigées, termes ajoutés (immobile, à plat, valeur de sécurité, valeur d'origine, paramètre de vol, effet d'événement) ; consignes : cinq lignes corrigées, une ligne ajoutée (dérive) ; risques acceptés : lignes 4, 9, 11 et 36 levées, ligne 8 et ligne 23 modifiées, ligne 37 ajoutée. « Besoins » : une seule note en annexe B, aucun besoin modifié.
**Alternatives écartées :** réécrire les scénarios et le glossaire (hors de la consigne « minimal ») ; laisser les textes périmés (contradiction avec les exigences).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-194 — Doutes de la phase exigences : levés, conservés et ouverts
**Date :** 2026-10-29
**Concerne :** « Registre de doutes » — `projets/boomrone/registre-doutes.md`
**Décision :** 21 doutes levés par une valeur écrite ou une simplification : DOU-009 « Quelle tolérance d'altitude pendant les 10 secondes de stationnaire ? », DOU-010 « Quelle rotation au lancer le drone doit-il rattraper ? », DOU-011 « Quelle dérive horizontale reste acceptable si 30 cm n'est pas tenu ? », DOU-012 « Quel angle limite et quelles autres valeurs de coupure retenir ? », DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? », DOU-028 « Faut-il une limite de dérive avant la coupure, entre 10° et 60° d'inclinaison ? », DOU-029 « Quelle altitude maximale et quel plafond le drone doit-il tolérer ? », DOU-035 « Quelle hauteur de stationnaire vise-t-on ? », DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture », DOU-080 « Seuils de temps du bouton : 1 s, 2 s, 10 s et délai entre appuis », DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs », DOU-111 « Niveau ou front du bouton à l'acceptation de Décoller », DOU-112 « Bouton enfoncé jusqu'à la fin de l'initialisation : état et signal », DOU-113 « Ordre entre Modifier pendant l'initialisation et chargement des réglages enregistrés », DOU-114 « Réglages enregistrés chargés ou non à l'état d'échec d'initialisation », DOU-117 « Cause de sous-tension sur le statut sans fil », DOU-119 « Filtrage, hystérésis et mesure sous charge de la tension », DOU-126 « Simplifications possibles des scénarios : choix de l'utilisateur », DOU-128 « Durée minimale perceptible des signaux », DOU-129 « Plage de lancer et hauteur d'un appartement (plafond) », DOU-130 « Arrêt d'un drone en vol par le bouton sans le toucher ». Restent ouverts, non bloquants : DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m », DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal », DOU-116 « Échéance et circularité du report aux essais, comportement de SCN-002 sur la partie infaisable de la plage » (essais, valeur provisoire écrite) ; DOU-060 « Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle », DOU-109 « Batterie déjà déchargée : redémarrages répétés, décharge profonde et état après une coupure logicielle », DOU-115 « Contenu et interruption de la réécriture de la zone des réglages par la reprogrammation », DOU-118 « Seuil de protection et consommation résiduelle du drone laissé allumé », DOU-120 « Écriture en mémoire sous tension basse ou pendant une phase de vol » (architecture). Quatre doutes sont ouverts : DOU-131 « Valeurs provisoires des exigences, à valider aux essais sur prototype » (valeurs provisoires, essais), DOU-132 « Liste des paramètres de vol réglables et leurs valeurs d'origine » (liste des paramètres réglables, architecture), DOU-133 « Forme des dix effets locaux : lumière, son, distinction mesurable » (forme des effets locaux, architecture), DOU-134 « Drone tenu en main au-dessus de la hauteur minimale et critère de stationnaire » (drone tenu en main et stationnaire, architecture et essais). Aucun doute bloquant.
**Alternatives écartées :** garder les doutes de valeurs ouverts (la délégation demande de trancher) ; lever les doutes d'essai (seul un essai les tranche).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** voir la décision (21 doutes) ; ouvre DOU-131 « Valeurs provisoires des exigences, à valider aux essais sur prototype », DOU-132 « Liste des paramètres de vol réglables et leurs valeurs d'origine », DOU-133 « Forme des dix effets locaux : lumière, son, distinction mesurable » et DOU-134 « Drone tenu en main au-dessus de la hauteur minimale et critère de stationnaire »
**Modifiée par :** DEC-215 « Doutes de la relecture de porte : levés, ouverts et déplacés » (DOU-132 « Liste des paramètres de vol réglables et leurs valeurs d'origine » et DOU-134 « Drone tenu en main au-dessus de la hauteur minimale et critère de stationnaire » levés ; DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie » et DOU-136 « Ordre de livraison : exigence essentielle dépendant du mode réglage souhaitable » ouverts) le 2026-10-29

### DEC-195 — Relecture de porte exigences : corrections décidées par délégation, identifiants conservés
**Date :** 2026-10-29
**Concerne :** « Exigences système » — `projets/boomrone/02-exigences.md`, « Plans de test » — `projets/boomrone/05-plans-de-test.md`
**Décision :** les trois relectures de la porte « exigences » (`critique` : non franchissable, deux bloquants de cohérence ; `coherence-clarte` : non tant que des majeurs de forme subsistent ; `exigences-tracabilite` : oui avec 14 majeurs de rédaction) sont traitées par les décisions de DEC-196 « Drone tenu en main à plus de 0,3 m : limite assumée, DOU-134 levé » à DEC-215 « Doutes de la relecture de porte : levés, ouverts et déplacés ». Règles : aucun identifiant n'est réutilisé ni renuméroté ; une exigence scindée garde son identifiant et les parties nouvelles prennent les identifiants à la suite (REQ-035 « Appui en cours à un changement d'état » à REQ-045 « Batterie débranchable à la main ») ; aucune exigence n'est abandonnée ; tous les REQ, TS et TA restent « Proposé » ou « Écrit » ; les besoins ne sont pas modifiés ; l'outil de traçabilité n'est pas modifié ; la porte n'est pas franchie.
**Alternatives écartées :** rouvrir les besoins (déjà validés) ; renuméroter pour garder l'ordre des groupes (casserait les renvois du journal).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité, un seul utilisateur qui accepte les risques et fabrique et programme le drone lui-même.
**Doutes levés :** (aucun, voir DEC-215 « Doutes de la relecture de porte : levés, ouverts et déplacés »)
**Modifie :** DEC-174 « Trente-quatre exigences : regroupements, champs et priorités » et DEC-191 « Tests système : vingt-quatre TS, un par exigence ou groupe » pour les nombres (45 exigences, 26 tests système).

### DEC-196 — Drone tenu en main à plus de 0,3 m : limite assumée, DOU-134 levé
**Date :** 2026-10-29
**Concerne :** REQ-007 « Critère de vol stationnaire », TA-002 « Recette de l'échec de stationnaire », TS-008 « Coupures automatiques en vol »
**Décision :** le critère de REQ-007 « Critère de vol stationnaire » reste inchangé. Un drone tenu en main à plus de 0,3 m, immobile et à plat, peut se croire en vol stationnaire : c'est une limite d'emploi assumée (ligne 38 de « Risques acceptés » — `projets/boomrone/risques-acceptes.md`, une ligne dans « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md`). Les essais de coupure sur stationnaire non atteint se font drone posé sur une table, hélices démontées, ou drone posé au sol (hauteur de moins de 0,3 m) : TA-002 « Recette de l'échec de stationnaire » et TS-008 « Coupures automatiques en vol » sont corrigés.
**Alternatives écartées :** condition de poussée ou de variation de hauteur en plus du critère (capteurs et réglages de plus, hors simplicité) ; interdire l'essai en main (le cas reste possible pour l'utilisateur, seulement non garanti).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-134 « Drone tenu en main au-dessus de la hauteur minimale et critère de stationnaire »
**Précise :** DEC-049 « Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale ».

### DEC-197 — Effet Lancé et vol : pas d'onzième effet
**Date :** 2026-10-29
**Concerne :** REQ-018 « Effets locaux par situation », REQ-004 « Démarrage des moteurs 200 ms après le relâchement », TS-003 « Démarrage des moteurs : délai et geste volontaire », TA-001 « Recette du vol nominal »
**Décision :** l'effet n°4 de REQ-018 « Effets locaux par situation » s'appelle « Lancé et vol » et démarre au relâchement du bouton armé ; il n'y a pas d'onzième effet pour la phase Lancé. REQ-004 « Démarrage des moteurs 200 ms après le relâchement » exige l'effet Lancé et vol au plus 50 ms après le relâchement ; TS-003 « Démarrage des moteurs : délai et geste volontaire » et TA-001 « Recette du vol nominal » sont alignés. L'état Lancé reste un état distinct sur le statut sans fil (REQ-020 « Statut sans fil »).
**Alternatives écartées :** onzième effet « Lancé » (un motif de plus, l'effet ne dure que 200 ms).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)
**Précise :** DEC-176 « Simplification n°3 adoptée : dix effets locaux au lieu de dix-sept signaux », dont la liste des dix effets plaçait Lancé dans l'effet « Vol » alors que REQ-004 « Démarrage des moteurs 200 ms après le relâchement » et TS-003 « Démarrage des moteurs : délai et geste volontaire » le traitaient comme un effet propre.

### DEC-198 — Modifier retiré du vol normal : DEC-177 confirmée contre DEC-039
**Date :** 2026-10-29
**Concerne :** REQ-023 « Commandes sans fil selon l'état du drone », REQ-026 « Paramètres de vol réglables », « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (ligne 23), SCN-009 « Réglage et suivi du drone par le sans fil »
**Décision :** la simplification de DEC-177 « Simplification n°4 adoptée : commandes sans fil acceptées seulement en mode réglage » est gardée : Modifier, Décoller et Sauvegarder ne sont acceptées qu'en mode réglage. Elle contredit la réponse Q3 de l'utilisateur dans DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » (2026-10-27 : paramètres modifiables aussi en vol normal). DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » est annotée « Modifiée par DEC-177 « Simplification n°4 adoptée : commandes sans fil acceptées seulement en mode réglage » » ; la ligne 23 de « Risques acceptés » et les références amont de SCN-009 « Réglage et suivi du drone par le sans fil » sont corrigées.
**Alternatives écartées :** rétablir Modifier en vol normal (réglage à distance d'un drone en vol par un tiers sans appairage, tableau des commandes plus long).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité ; la contradiction avec sa réponse antérieure est signalée en tête du rapport de l'architecte.
**Doutes levés :** (aucun)
**Confirme :** DEC-177 « Simplification n°4 adoptée : commandes sans fil acceptées seulement en mode réglage » ; **modifie :** DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ».

### DEC-199 — Sous-tension : verrouillage dans tous les états, mode réglage compris
**Date :** 2026-10-29
**Concerne :** REQ-012 « Coupure sur sous-tension de la batterie », REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage », REQ-023 « Commandes sans fil selon l'état du drone », TS-009 « Coupure sur sous-tension et marge de batterie », TS-007 « Verrouillage après un posé, une coupure ou un redémarrage », SCN-012 « Dégradé : sous-tension de la batterie »
**Décision :** la coupure sur sous-tension verrouille le drone dans tous les états, mode réglage compris ; la sécurité de la batterie passe avant le confort du réglage. L'exception « retour au mode réglage sans verrouillage » de REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage » exclut explicitement la sous-tension. En mode réglage, « verrouillé » veut dire : moteurs arrêtés et commande Décoller ignorée jusqu'à la mise hors tension. SCN-012 « Dégradé : sous-tension de la batterie » (« verrouillé, jamais armé tout seul », tous états dont le mode réglage) est déjà d'accord.
**Alternatives écartées :** retour au mode réglage après une sous-tension (la batterie remontée en tension à vide pourrait faire accepter un nouveau décollage).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-200 — Hauteur visée 1,0 m, dérive 0,5 m, pièce d'essai 4 m × 4 m × 2,5 m
**Date :** 2026-10-29
**Concerne :** REQ-006 « Stabilisation après le lancer », REQ-008 « Tenue du vol stationnaire », REQ-033 « Vol dans une pièce d'appartement », TS-004 « Stabilisation après le lancer », TS-005 « Critère et tenue du vol stationnaire », TS-023 « Vol dans une pièce d'appartement »
**Décision :** hauteur visée du stationnaire 1,0 m, fenêtre 0,8 m à 1,2 m de la 3e à la 10e seconde, le drone convergeant vers 1,0 m depuis la hauteur du lancer (REQ-006 « Stabilisation après le lancer », REQ-008 « Tenue du vol stationnaire ») ; dérive exigée d'au plus 0,5 m, objectif de 0,3 m inchangé en note ; pièce d'essai de 4 m × 4 m × 2,5 m, lancers à vitesse horizontale d'au plus 1 m/s, critère « aucune partie du drone ne sort du volume de la pièce », 9 vols sur 10 ; les lancers à 2 et 4 m/s de TS-004 « Stabilisation après le lancer » se font dans un lieu plus grand (gymnase ou jardin).
**Alternatives écartées :** garder 3 m × 3 m (trop petit pour un stationnaire à 1,0 m avec des fenêtres de 1 m de dérive) ; dérive de 1,0 m (laisse le drone toucher un mur d'une petite pièce).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun : le doute sur la pièce d'essai évoqué par la relecture n'a pas d'entrée dans le registre ; la question est tranchée ici, et DOU-129 « Plage de lancer et hauteur d'un appartement (plafond) » est déjà levé)
**Modifie :** DEC-184 « Valeurs du vol : lancer, stationnaire, hauteur, dérive, atterrissage » (dérive 1,0 m devenue 0,5 m) ; DEC-187 « Valeurs du cadre d'emploi : poche, protège-hélices, pièce d'essai » (pièce de 3 m × 3 m × 2,5 m devenue 4 m × 4 m × 2,5 m).

### DEC-201 — Quatre paramètres de vol réglables, valeurs d'origine provisoires : DOU-132 levé
**Date :** 2026-10-29
**Concerne :** REQ-026 « Paramètres de vol réglables », REQ-043 « Valeurs de sécurité fixes », REQ-038 « Causes et paramètres dans le statut sans fil », REQ-020 « Statut sans fil », REQ-023 « Commandes sans fil selon l'état du drone », TS-019 « Paramètres, sauvegarde et valeurs d'origine »
**Décision :** REQ-026 « Paramètres de vol réglables » est scindée : (a) modification et relecture des paramètres réglables ; (b) valeurs de sécurité fixes, listées une seule fois dans REQ-043 « Valeurs de sécurité fixes ». Liste minimale provisoire de quatre paramètres : gain d'inclinaison (1,0), gain de hauteur (1,0), hauteur visée du stationnaire (1,0 m), vitesse de descente (0,2 m/s) ; valeurs à valider aux essais. « Relecture » : la valeur courante de chaque paramètre figure dans le statut sans fil (REQ-038 « Causes et paramètres dans le statut sans fil »), sans cinquième commande ; l'acquittement d'une commande Modifier est la valeur relue.
**Alternatives écartées :** liste renvoyée à l'architecture (laisse REQ-026 « Paramètres de vol réglables » non testable) ; commande de relecture dédiée (cinquième commande, tableau de REQ-023 « Commandes sans fil selon l'état du drone » plus long).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-132 « Liste des paramètres de vol réglables et leurs valeurs d'origine »

### DEC-202 — Statut sans fil en trois exigences
**Date :** 2026-10-29
**Concerne :** REQ-020 « Statut sans fil », REQ-038 « Causes et paramètres dans le statut sans fil », REQ-039 « Cadence et portée du statut sans fil », REQ-011 « Coupures automatiques en vol », REQ-012 « Coupure sur sous-tension de la batterie », REQ-022 « Arrêt sans fil »
**Décision :** REQ-020 « Statut sans fil » est scindée : l'état (tableau des dix-sept états) reste dans REQ-020 « Statut sans fil » ; les causes de refus, les causes de coupure et les paramètres relus passent dans REQ-038 « Causes et paramètres dans le statut sans fil » ; la cadence (2 fois par seconde et à chaque changement d'état) et la portée (5 m) dans REQ-039 « Cadence et portée du statut sans fil ». REQ-011 « Coupures automatiques en vol », REQ-012 « Coupure sur sous-tension de la batterie » et REQ-022 « Arrêt sans fil » n'écrivent plus « enregistre la cause sur le statut » : c'est REQ-038 « Causes et paramètres dans le statut sans fil » qui la porte. TS-008 « Coupures automatiques en vol » et TS-009 « Coupure sur sous-tension et marge de batterie » sont adaptés. Un envoi à chaque changement d'état rend testables les états qui ne durent qu'un instant.
**Alternatives écartées :** une seule exigence de huit lignes (non atomique).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-203 — Coupure sur logiciel bloqué et coupure sur phase Lancé : deux exigences
**Date :** 2026-10-29
**Concerne :** REQ-014 « Coupure sur logiciel bloqué », REQ-036 « Coupure sur phase Lancé trop longue », TS-010 « Coupure sur logiciel bloqué ou phase Lancé trop longue »
**Décision :** REQ-014 « Coupure sur logiciel bloqué » est scindée : (a) logiciel bloqué, moteurs coupés au plus 200 ms après la dernière exécution correcte du logiciel ; (b) phase Lancé de plus de 500 ms, dans la nouvelle REQ-036 « Coupure sur phase Lancé trop longue ». « Puis redémarrer » et tout nom de moyen sont retirés des énoncés ; l'indépendance vis-à-vis du logiciel bloqué reste une contrainte d'exigence.
**Alternatives écartées :** garder « puis redémarrer » (impose une solution).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)
**Précise :** DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale » et DEC-103 « Phase Lancé trop longue : coupure et redémarrage par le chien de garde, sans nouvel état ni signal » pour les exigences (leurs solutions restent à l'architecture).

### DEC-204 — Protège-hélices : calibre sur les côtés, dessus et dessous en limite assumée
**Date :** 2026-10-29
**Concerne :** REQ-032 « Protège-hélices », TS-022 « Dimensions, masse et protège-hélices »
**Décision :** le calibre de 12 mm s'applique dans le plan des hélices (par les côtés) seulement ; le dessus et le dessous ne sont pas couverts : limite assumée (ligne 39 de « Risques acceptés » — `projets/boomrone/risques-acceptes.md`, une ligne dans « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md`).
**Alternatives écartées :** calibre dans toutes les directions (impose un carénage complet, plus lourd que 100 g).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)
**Précise :** DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer ».

### DEC-205 — Bouton : règle unique de l'appui en cours, garde du lancer, Décoller refusé si le bouton est enfoncé
**Date :** 2026-10-29
**Concerne :** REQ-035 « Appui en cours à un changement d'état », REQ-015 « Garde du bouton après le lancer », REQ-016 « Arrêt d'urgence par le bouton », REQ-041 « Conditions d'acceptation de la commande Décoller », REQ-002 « Chronologie d'un appui sur le bouton », REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage », REQ-024 « Entrée en mode réglage par le bouton »
**Décision :** la règle « un appui déjà en cours à un changement d'état est ignoré jusqu'à son relâchement » est écrite dans une seule exigence, REQ-035 « Appui en cours à un changement d'état » ; les autres exigences y renvoient. Elle ne s'applique pas à la garde du lancer : un appui encore enfoncé à la fin de la garde de 0,5 s arrête les moteurs (REQ-015 « Garde du bouton après le lancer »). La commande Décoller est refusée (effet Refus) si le bouton est enfoncé (REQ-041 « Conditions d'acceptation de la commande Décoller ») ; un appui après le décollage de réglage coupe aussitôt, sans garde (REQ-016 « Arrêt d'urgence par le bouton »). Les mots « décollage » seul sont remplacés par « démarrage des moteurs » ou « décollage de réglage ».
**Alternatives écartées :** règle répétée dans chaque exigence (contradictions entre REQ-015 « Garde du bouton après le lancer » et REQ-016 « Arrêt d'urgence par le bouton »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)
**Précise :** DEC-188 « Bouton : un appui commencé avant une coupure ou un décollage est ignoré jusqu'au relâchement » (pour Décoller, le bouton déjà enfoncé est maintenant un refus, non un appui ignoré).

### DEC-206 — Conditions de départ : immobilité mesurée en relatif, cas Décoller séparé
**Date :** 2026-10-29
**Concerne :** REQ-003 « Conditions de départ du drone », REQ-041 « Conditions d'acceptation de la commande Décoller », REQ-017 « Initialisation en 3 secondes », TS-002 « Conditions de départ et refus d'armement »
**Décision :** REQ-003 « Conditions de départ du drone » est scindée : (a) conditions de départ (immobile, à plat, batterie) ; (b) cas de la commande Décoller en mode réglage, dans REQ-041 « Conditions d'acceptation de la commande Décoller ». Immobile = vitesse de rotation d'au plus 30 °/s et norme de l'accélération qui reste à ±0,5 m/s² de sa moyenne sur 0,5 s (mesure relative : la valeur absolue de 9,3 à 10,3 m/s² est abandonnée, car elle dépend du calibrage). La condition « aucun échec d'initialisation » est retirée de REQ-003 « Conditions de départ du drone » : elle créait un cycle avec REQ-017 « Initialisation en 3 secondes ». TS-002 « Conditions de départ et refus d'armement » reçoit des cas chiffrés.
**Alternatives écartées :** garder la valeur absolue de la norme (dépend du calibrage de l'accéléromètre).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun ; le calibrage reste dans DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal »)
**Précise :** DEC-183 « Valeurs de départ : immobile, à plat, batterie à l'armement ».

### DEC-207 — Appareil de suivi et batterie débranchable : deux exigences ajoutées
**Date :** 2026-10-29
**Concerne :** REQ-040 « Appareil de suivi », REQ-045 « Batterie débranchable à la main », TS-025 « Appareil de suivi et logiciel d'essai », TS-026 « Batterie débranchable à la main »
**Décision :** REQ-040 « Appareil de suivi » (Souhaitable, BES-010 « Suivre le drone sur un appareil de suivi ») : l'appareil de suivi est un ordinateur ou un téléphone relié au drone par la liaison sans fil, avec un logiciel d'essai écrit par l'utilisateur, livrable du projet ; le protocole relève de l'architecture. REQ-045 « Batterie débranchable à la main » (Essentiel, BES-004 « Ne pas voler quand le drone n'est pas prêt » et BES-011 « Fabriquer et programmer le drone soi-même ») : la batterie se débranche à la main, drone moteurs arrêtés, le connecteur restant accessible malgré les protège-hélices (c'est le dernier recours des consignes d'emploi).
**Alternatives écartées :** laisser l'appareil de suivi hors exigences (les tests sans fil n'auraient pas d'outil) ; interrupteur sur le drone (masse et composant de plus).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-208 — Fabrication : approvisionnement et assemblage séparés
**Date :** 2026-10-29
**Concerne :** REQ-029 « Composants disponibles à l'unité », REQ-044 « Assemblage à la main », TS-020 « Fabrication à la main », TA-015 « Inspection de la fabrication à la main »
**Décision :** REQ-029 « Composants disponibles à l'unité » devient l'approvisionnement : chaque composant s'achète à l'unité, sans commande minimale, chez au moins un revendeur en ligne grand public (« au moins 2 » devient « au moins un »). REQ-044 « Assemblage à la main » porte l'assemblage à la main : pas de broches d'au moins 0,5 mm, pas de BGA, pas de brasage en four ; câblage sur modules, carte à trous et circuit imprimé sur mesure commandé en ligne permis. TS-020 « Fabrication à la main » inspecte la nomenclature ; le montage d'une carte est fait dans TA-015 « Inspection de la fabrication à la main ».
**Alternatives écartées :** deux revendeurs minimum (contrainte de plus pour un seul utilisateur).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-209 — Batterie de référence choisie à l'architecture, faisabilité conjointe en doute
**Date :** 2026-10-29
**Concerne :** REQ-013 « Marge de batterie pour un vol complet », REQ-031 « Drone de poche », REQ-006 « Stabilisation après le lancer »
**Décision :** la batterie de référence de REQ-013 « Marge de batterie pour un vol complet » est la batterie réellement choisie à l'architecture ; essais sur banc. Le mot « lithium » est retiré des énoncés (on dit « par élément »). La faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie est ouverte en doute non bloquant : DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie ».
**Alternatives écartées :** fixer une batterie type dans l'exigence (c'est une solution).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-210 — Délais uniques : atterrissage 15,0 s ±0,5 s, sous-tension 250 ms, vol de réglage scindé
**Date :** 2026-10-29
**Concerne :** REQ-009 « Atterrissage doux », REQ-011 « Coupures automatiques en vol », REQ-012 « Coupure sur sous-tension de la batterie », REQ-025 « Vol de réglage », REQ-042 « Vol de réglage indépendant du lien sans fil »
**Décision :** le délai d'atterrissage de 15 s n'est défini que dans REQ-011 « Coupures automatiques en vol », comme seuil de coupure « 15,0 s (±0,5 s) » ; REQ-009 « Atterrissage doux » dit « avant la coupure de REQ-011 « Coupures automatiques en vol » » et s'écrit « à la fin du stationnaire (10 s, ou 3 s en vol de réglage) ». Le délai de REQ-012 « Coupure sur sous-tension de la batterie » est une durée unique : coupure au plus 250 ms après le passage sous 3,3 V par élément, la tension y restant 100 ms ±20 ms ou plus. REQ-025 « Vol de réglage » est scindée : décollage et stationnaire dans REQ-025 « Vol de réglage », indépendance du lien sans fil dans REQ-042 « Vol de réglage indépendant du lien sans fil ».
**Alternatives écartées :** deux tolérances empilées sur 15 s.
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-211 — Initialisation en deux exigences, démarrage des moteurs sans chevauchement
**Date :** 2026-10-29
**Concerne :** REQ-017 « Initialisation en 3 secondes », REQ-037 « Comportement en échec d'initialisation », REQ-005 « Démarrage des moteurs sur geste volontaire seulement », REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage », TS-003 « Démarrage des moteurs : délai et geste volontaire », TS-012 « Initialisation et échec d'initialisation »
**Décision :** REQ-017 « Initialisation en 3 secondes » est scindée : initialisation en 3 s au plus (REQ-017 « Initialisation en 3 secondes ») ; comportement en échec (REQ-037 « Comportement en échec d'initialisation »). Un appui commencé pendant l'initialisation et encore enfoncé à la fin est ignoré jusqu'au relâchement (règle de REQ-035 « Appui en cours à un changement d'état »). REQ-005 « Démarrage des moteurs sur geste volontaire seulement » ne dit plus que les deux seuls cas de démarrage des moteurs ; REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage » dit l'état après une coupure ; le chevauchement disparaît. Le compte de TS-003 « Démarrage des moteurs : délai et geste volontaire » est « 0 sur 31 » (10 + 10 + 10 + 1).
**Alternatives écartées :** garder la liste des cas interdits dans REQ-005 « Démarrage des moteurs sur geste volontaire seulement » (doublon de REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage »).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-212 — Effets locaux : lumière ou son, distinction en une passe
**Date :** 2026-10-29
**Concerne :** REQ-019 « Perceptibilité et distinction des effets », REQ-018 « Effets locaux par situation », TS-014 « Perceptibilité et distinction des effets »
**Décision :** chaque effet est donné par la lumière, par le son ou par les deux ; aucun buzzer n'est imposé ; moteurs en marche, l'effet passe par la lumière. Critère de distinction : un observateur identifie les dix effets présentés dans un ordre aléatoire, 10 sur 10 en une passe.
**Alternatives écartées :** deux passes de dix (plus long, même information) ; imposer lumière et son (une solution).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun ; la forme reste dans DOU-133 « Forme des dix effets locaux : lumière, son, distinction mesurable »)
**Précise :** DEC-176 « Simplification n°3 adoptée : dix effets locaux au lieu de dix-sept signaux ».

### DEC-213 — Valeurs provisoires : règle unique de marquage, annexe B complète, page de 60 lignes
**Date :** 2026-10-29
**Concerne :** « Exigences système » — `projets/boomrone/02-exigences.md` (annexe B), REQ-034 « Page de consignes d'emploi », TS-024 « Page de consignes d'emploi », TA-013 « Inspection des consignes d'emploi »
**Décision :** toute valeur ou tolérance qui ne vient pas d'une décision de l'utilisateur est marquée « provisoire » dans l'énoncé et dans le tableau récapitulatif, et l'annexe B les liste toutes (le texte des valeurs de sécurité y renvoie à REQ-043 « Valeurs de sécurité fixes » au lieu de les répéter). Les valeurs décidées par l'utilisateur ne sont pas provisoires. La page de consignes tient sur une face A4 : au plus 60 lignes de 15 mots au plus, une consigne à l'infinitif par ligne (REQ-034 « Page de consignes d'emploi », TS-024 « Page de consignes d'emploi », TA-013 « Inspection des consignes d'emploi » alignés).
**Alternatives écartées :** 50 lignes (la page compte déjà plus de consignes utiles) ; supprimer la limite d'une face (BES-012 « Disposer d'une page de consignes d'emploi » demande une page).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-214 — Documents liés recomptés et alignés après les corrections de la porte exigences
**Date :** 2026-10-29
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`, « Scénarios d'utilisation » — `projets/boomrone/00-scenarios.md`, « Glossaire » — `projets/boomrone/00-glossaire.md`, « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md`, « Risques acceptés » — `projets/boomrone/risques-acceptes.md`, « Reprise du projet Boomrone » — `projets/boomrone/reprise.md`, les gabarits `framework/templates/02-exigences.md` et `framework/templates/05-plans-de-test.md`
**Décision :** aperçus et décomptes recomptés depuis le registre par script ; aucun besoin modifié (BES-001 « Lancer le drone à la main » à BES-013 « Voler en appartement avec un drone de poche protégé » restent « Validé »), une note dans l'annexe B de « Besoins » signale les énoncés périmés de BES-007 « Savoir où en est le drone sans autre appareil », BES-008 « Entrer en mode réglage et faire des vols de réglage » et BES-009 « Régler et sauvegarder les paramètres de vol » (à reprendre à la prochaine révision) ; le glossaire précise « Variables du vol », « signal / état / effet local », « Prêt » (effet) et « prêt » (conditions de départ), « décollage de réglage », « appareil de suivi », « stationnaire déclaré » ; les consignes sont coupées à 15 mots par ligne, à l'infinitif, avec les deux lignes nouvelles ; les gabarits reprennent les champs Priorité, Décisions liées, Vérification, Scénario rejoué, Résultat attendu.
**Alternatives écartées :** réécrire les besoins (validés).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)

### DEC-215 — Doutes de la relecture de porte : levés, ouverts et déplacés
**Date :** 2026-10-29
**Concerne :** « Registre de doutes » — `projets/boomrone/registre-doutes.md`
**Décision :** levés : DOU-134 « Drone tenu en main au-dessus de la hauteur minimale et critère de stationnaire » (limite assumée, DEC-196 « Drone tenu en main à plus de 0,3 m : limite assumée, DOU-134 levé ») et DOU-132 « Liste des paramètres de vol réglables et leurs valeurs d'origine » (liste fixée, DEC-201 « Quatre paramètres de vol réglables, valeurs d'origine provisoires : DOU-132 levé »). Ouverts, non bloquants : DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie » (architecture : faisabilité conjointe) et DOU-136 « Ordre de livraison : exigence essentielle dépendant du mode réglage souhaitable » (livraison : REQ-005 « Démarrage des moteurs sur geste volontaire seulement » dépend du mode réglage). Complétés : DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal » (calibrage de l'accéléromètre) et DOU-120 « Écriture en mémoire sous tension basse ou pendant une phase de vol » (écriture en mémoire et blocage du logiciel de 200 ms). DOU-127 « Couverture ligne à ligne des risques acceptés par les consignes d'emploi », déjà levé, est déplacé dans l'archive.
**Alternatives écartées :** garder DOU-134 « Drone tenu en main au-dessus de la hauteur minimale et critère de stationnaire » et DOU-132 « Liste des paramètres de vol réglables et leurs valeurs d'origine » ouverts (la délégation demande de trancher).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** DOU-134 « Drone tenu en main au-dessus de la hauteur minimale et critère de stationnaire » ; DOU-132 « Liste des paramètres de vol réglables et leurs valeurs d'origine » ; ouvre DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie » et DOU-136 « Ordre de livraison : exigence essentielle dépendant du mode réglage souhaitable »
**Modifie :** DEC-194 « Doutes de la phase exigences : levés, conservés et ouverts » (listes de doutes).

### DEC-216 — Fusions de simplicité et sous-tension en échec d'initialisation : retouches finales de la porte exigences
**Date :** 2026-10-29
**Concerne :** « Exigences système » — `projets/boomrone/02-exigences.md`, « Plans de test » — `projets/boomrone/05-plans-de-test.md`, REQ-012 « Coupure sur sous-tension de la batterie », REQ-037 « Comportement en échec d'initialisation »
**Décision :** (1) quatre fusions, identifiants conservés en « Abandonné » avec renvoi, TS réattachés : REQ-001 « Anti-rebond du bouton » dans REQ-002 « Chronologie d'un appui sur le bouton » ; REQ-039 « Cadence et portée du statut sans fil » dans REQ-020 « Statut sans fil » ; REQ-042 « Vol de réglage indépendant du lien sans fil » dans REQ-025 « Vol de réglage » ; REQ-043 « Valeurs de sécurité fixes » dans REQ-026 « Paramètres de vol réglables » (seuls 4 paramètres modifiables, 29 valeurs fixes listées une fois, priorité Essentiel). 41 exigences actives : 27 Essentielles, 10 Souhaitables, 4 Importantes. (2) Retouches : REQ-009 « Atterrissage doux » avec les valeurs d'origine ; REQ-006 « Stabilisation après le lancer » sans convergence vers 1,0 m (laissée à REQ-008 « Tenue du vol stationnaire ») ; REQ-003 « Conditions de départ du drone » sans « fin de l'initialisation » et batterie contrôlée à l'armement seulement (REQ-017 « Initialisation en 3 secondes ») ; REQ-015 « Garde du bouton après le lancer » : arrêt 50 ms après la fin de la garde ; TS-017 « Commandes sans fil selon l'état » : état Lancé forcé par un logiciel d'essai ou inspection ; note dans DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m ». (3) Sous-tension sans redémarrage, drone encore alimenté : il reste verrouillé et donne l'effet Échec d'initialisation, état inutilisable jusqu'à la mise hors tension (bouton sans effet, il faut débrancher) ; écrit dans REQ-012 « Coupure sur sous-tension de la batterie », REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage », REQ-037 « Comportement en échec d'initialisation », REQ-018 « Effets locaux par situation », REQ-020 « Statut sans fil », REQ-023 « Commandes sans fil selon l'état du drone », TS-009 « Coupure sur sous-tension et marge de batterie », TA-012 « Recette de la sous-tension de la batterie ». (4) Colonne « Valeur clé » et annexe B alignées (300 lux, 80 ms, valeurs provisoires marquées une à une ; le délai de 2,0 s de REQ-006 « Stabilisation après le lancer » reste « décidé », DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs »).
**Alternatives écartées :** garder les quatre exigences séparées (plus de numéros, aucun gain de précision) ; laisser le drone sans effet après une sous-tension (l'utilisateur ne saurait pas qu'il faut débrancher) ; ouvrir un nouveau doute (la consommation résiduelle relève de DOU-118 « Seuil de protection et consommation résiduelle du drone laissé allumé », note ajoutée).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 : décide seul, vise la simplicité.
**Doutes levés :** (aucun)
**Modifie :** DEC-195 « Relecture de porte exigences : corrections décidées par délégation, identifiants conservés » (« aucune exigence n'est abandonnée » ne vaut plus), DEC-199 « Sous-tension : verrouillage dans tous les états, mode réglage compris » (le verrouillage est l'état d'échec d'initialisation) et DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre » (l'effet Échec d'initialisation est donné).

### DEC-217 — Porte exigences franchie : accord explicite de l'utilisateur
**Date :** 2026-10-29
**Concerne :** « Exigences système » — `projets/boomrone/02-exigences.md` (41 exigences actives) et « Plans de test » — `projets/boomrone/05-plans-de-test.md` (26 TS, 15 TA)
**Décision :** la porte « exigences » est franchie ; les 41 exigences actives passent à « Validé » (les quatre fusionnées restent « Abandonné ») ; la phase « architecture » peut s'ouvrir. État au franchissement : tag `gate-3-exigences-ready-v0`, aucun doute bloquant ouvert, 12 doutes non bloquants (liste dans `registre-doutes.md`), relectures de porte faites par `critique`, `coherence-clarte` et `exigences-tracabilite` (DEC-195 « Relecture de porte exigences : corrections décidées par délégation, identifiants conservés »), sans nouvelle relecture après les retouches de DEC-216 « Fusions de simplicité et sous-tension en échec d'initialisation : retouches finales de la porte exigences ».
**Alternatives écartées :** demander une dernière passe des trois relecteurs avant la porte (proposée, non retenue par l'utilisateur) ; continuer la phase « exigences » (aucun doute bloquant, décisions prises).
**Raison :** accord explicite de l'utilisateur en chat, 2026-10-29 : « accord explicite sur la porte exigences ». Rappels : `check_traceability --gate` échoue pour les 41 « REQ sans ARC » (phase suivante) et les 12 « SCN sans BES » (défaut connu, DEC-156 « Couverture des scénarios vérifiée à la main, outil de traçabilité inchangé ») ; les valeurs provisoires (annexe B) restent à valider aux essais sur prototype (DOU-131 « Valeurs provisoires des exigences, à valider aux essais sur prototype »).
**Doutes levés :** (aucun)

### DEC-218 — Délégation totale de la phase architecture à l'architecte
**Date :** 2026-10-29
**Concerne :** « Architecture » — `projets/boomrone/03-architecture.md`, « Plans de test » — `projets/boomrone/05-plans-de-test.md` (section TI)
**Décision :** l'utilisateur ne veut aucune question pendant la phase « architecture » : l'architecte décide seul de tous les points, toujours la solution la plus simple qui fonctionne (premier drone, composants à l'unité, assemblage à la main, programmation depuis l'ordinateur, drone de poche de moins de 100 g). Chaque trou est tranché et écrit (décision, doute levé ou doute ouvert non bloquant). Les éléments d'architecture restent « Proposé » : la porte « architecture » n'est pas franchie sans l'accord explicite de l'utilisateur. Pas de commit ni d'étiquette.
**Alternatives écartées :** poser les choix de composants à l'utilisateur un par un (refusé par l'utilisateur).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29, à la suite de DEC-217 « Porte exigences franchie : accord explicite de l'utilisateur ».
**Doutes levés :** (aucun)

### DEC-219 — Structure générale : carte maison unique, microcontrôleur STM32G431, boucle sans système temps réel
**Date :** 2026-10-29
**Concerne :** REQ-030 « Programmation depuis l'ordinateur », REQ-029 « Composants disponibles à l'unité », REQ-044 « Assemblage à la main », REQ-014 « Coupure sur logiciel bloqué »
**Décision :** une carte électronique maison à deux couches (commandée en ligne, soudure au fer), un microcontrôleur STM32G431CBT6 (FPU, chien de garde indépendant, programmable avec le ST-LINK de l'utilisateur par un en-tête SWD de 5 broches), logiciel en C sans système d'exploitation temps réel. Octets d'option : IWDG_SW = 0 et BOR_LEV = 3. Éléments : ARC-001 « Structure générale du drone », ARC-002 « Microcontrôleur et programmation par liaison SWD », ARC-013 « Carte électronique JLCPCB, câblage et assemblage », ARC-015 « Structure logicielle et ordonnancement ».
**Alternatives écartées :** STM32F103, STM32G0 (sans FPU), ESP32 (seconde chaîne de programmation) ; carte à trous ; système temps réel.
**Raison :** délégation, simplicité ; correction apportée par l'électronique : NRST ajouté à l'en-tête SWD, BOOT0 tiré à la masse.
**Doutes levés :** (aucun)

### DEC-220 — Capteurs : centrale LSM6DSO, hauteur VL53L1X, flux optique PMW3901
**Date :** 2026-10-29
**Concerne :** REQ-007 « Critère de vol stationnaire », REQ-008 « Tenue du vol stationnaire », REQ-009 « Atterrissage doux », REQ-006 « Stabilisation après le lancer »
**Décision :** centrale LSM6DSO sur SPI, capteur de hauteur VL53L1X en mode long sur I2C, capteur de flux optique PMW3901 sur SPI, tous trois sur cartes d'évaluation soudées par fils ou broches. Le flux optique est retenu dès maintenant : sans lui la dérive de 0,5 m en 10 s de REQ-008 « Tenue du vol stationnaire » est hors d'atteinte, et il donne la vitesse horizontale qui manquait (DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m »). Éléments : ARC-003 « Centrale inertielle », ARC-004 « Capteur de hauteur à temps de vol », ARC-005 « Capteur de flux optique », ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse ». Le capteur de hauteur est monté à environ 20 mm au-dessus du plan de contact (mesure fiable à partir de 40 mm).
**Alternatives écartées :** centrale seule (dérive de plusieurs mètres) ; VL53L0X (2 m) ; baromètre ; caméra.
**Raison :** délégation, la solution simple qui fonctionne.
**Doutes levés :** (aucun)

### DEC-221 — Moteurs à balais 8520, hélices de 45 mm, étage de puissance coupé par défaut
**Date :** 2026-10-29
**Concerne :** REQ-031 « Drone de poche », REQ-032 « Protège-hélices », REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage », REQ-014 « Coupure sur logiciel bloqué », REQ-005 « Démarrage des moteurs sur geste volontaire seulement »
**Décision :** quatre moteurs coreless à balais 8520 avec hélices de 45 mm (les hélices de 65 mm exigent environ 138 mm de côté et ne tiennent pas dans 100 mm), anneaux de protection à paroi continue, un MOSFET AO3400A côté bas par moteur avec rappel de 100 kΩ grille-masse : tout reset coupe les moteurs sans logiciel. Éléments : ARC-006 « Moteurs, hélices et protège-hélices », ARC-007 « Étage de puissance des moteurs coupés par défaut ».
**Alternatives écartées :** hélices de 65 mm ; brushless 1S ou 2S (contrôleur à acheter fait, DShot) ; pilote de moteurs intégré.
**Raison :** délégation, simplicité de la commande et sûreté par construction.
**Doutes levés :** (aucun)

### DEC-222 — Batterie 1S 850 mAh, connecteur XT30, alimentation 3,0 V et mesure de tension
**Date :** 2026-10-29
**Concerne :** REQ-013 « Marge de batterie pour un vol complet », REQ-012 « Coupure sur sous-tension de la batterie », REQ-045 « Batterie débranchable à la main », REQ-003 « Conditions de départ du drone »
**Décision :** batterie LiPo 1S de 850 mAh d'au moins 50C sans circuit de protection, connecteur XT30 détrompé au bord du drone, sans interrupteur ; régulateur LDO 3,0 V à faible chute (un 3,3 V ne tient pas quand la batterie descend à 3,3 V et moins) ; mesure de la tension par pont diviseur à 0,1 % et correction par la référence interne. Risques résiduels (inversion de polarité, surintensité, décharge profonde si le drone reste branché) notés dans ARC-008 « Batterie et connecteur débranchable » et ARC-030 « Page de consignes d'emploi », sans protection supplémentaire. Éléments : ARC-008 « Batterie et connecteur débranchable », ARC-009 « Alimentation de la logique et mesure de la tension ».
**Alternatives écartées :** JST-PH (2 A par contact) ; 2S ; régulateur 3,3 V ; protection d'inversion par MOSFET P (chute de tension, composant en plus).
**Raison :** délégation, simplicité.
**Doutes levés :** (aucun)

### DEC-223 — Radio Bluetooth HM-10, protocole de trames et logiciel d'essai en Python
**Date :** 2026-10-29
**Concerne :** REQ-020 « Statut sans fil », REQ-021 « Variables du vol », REQ-022 « Arrêt sans fil », REQ-023 « Commandes sans fil selon l'état du drone », REQ-038 « Causes et paramètres dans le statut sans fil », REQ-040 « Appareil de suivi »
**Décision :** module BLE série transparent HM-10 à 9600 bauds sans configuration ni appairage ; trames binaires de 14 octets au plus, octet de synchronisation 0xA5, type, charge, CRC8 ; statut à 2 Hz et à chaque changement, variables à 10 Hz, quatre commandes ; logiciel d'essai `tools/suivi.py` (Python et bleak). Éléments : ARC-012 « Module radio Bluetooth à basse consommation », ARC-025 « Protocole et service du statut sans fil », ARC-028 « Logiciel d'essai de l'appareil de suivi ».
**Alternatives écartées :** RN4871 (configuration AT), ESP32 (seconde chaîne de programmation), STM32WB (pile lourde) ; texte ASCII ; application pour téléphone.
**Raison :** délégation, simplicité ; l'octet de synchronisation est ajouté car le module peut couper ou fusionner les trames.
**Doutes levés :** (aucun)

### DEC-224 — Logiciel : une seule machine à états, cycle à 1 kHz, modules
**Date :** 2026-10-29
**Concerne :** REQ-004 « Démarrage des moteurs 200 ms après le relâchement », REQ-005 « Démarrage des moteurs sur geste volontaire seulement », REQ-016 « Arrêt d'urgence par le bouton », REQ-021 « Variables du vol »
**Décision :** cycle de contrôle à 1 kHz dans la boucle principale (tick en interruption), tâches de fond coopératives, une seule machine à états de 18 états avec deux seuls sites de démarrage des moteurs, filtre de Mahony, observateur de hauteur, cascade angle-vitesse angulaire, gestion du bouton par compteur à 1 kHz. Éléments : ARC-015 « Structure logicielle et ordonnancement », ARC-016 « Pilotes des capteurs et des sorties », ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse », ARC-018 « Boucle de contrôle du vol », ARC-019 « Machine à états du drone », ARC-020 « Gestion logicielle du bouton ».
**Alternatives écartées :** machine à états par domaine, contrôle dans l'interruption, filtre de Kalman complet.
**Raison :** délégation, simplicité.
**Doutes levés :** (aucun)

### DEC-225 — Chien de garde matériel et coupures automatiques
**Date :** 2026-10-29
**Concerne :** REQ-014 « Coupure sur logiciel bloqué », REQ-036 « Coupure sur phase Lancé trop longue », REQ-011 « Coupures automatiques en vol », REQ-012 « Coupure sur sous-tension de la batterie »
**Décision :** chien de garde indépendant de 100 ms rendu matériel par l'octet d'option, rafraîchi une fois par cycle sain et refusé quand l'état Lancé dépasse 500 ms ; coupure dans le logiciel (`motors_cut()`) pour les causes de REQ-011 « Coupures automatiques en vol » et la sous-tension de REQ-012 « Coupure sur sous-tension de la batterie », cause mémorisée en RAM non initialisée. Éléments : ARC-021 « Surveillance et coupures automatiques », ARC-022 « Chien de garde ».
**Alternatives écartées :** chien de garde externe ; coupure sur seuil de tension instantané.
**Raison :** délégation, aucun composant en plus.
**Doutes levés :** (aucun)

### DEC-226 — Initialisation : priorités, mode réglage après mise sous tension, causes conservées après reset
**Date :** 2026-10-29
**Concerne :** REQ-017 « Initialisation en 3 secondes », REQ-037 « Comportement en échec d'initialisation », REQ-024 « Entrée en mode réglage par le bouton », REQ-038 « Causes et paramètres dans le statut sans fil »
**Décision :** à la fin de l'initialisation, priorité à l'échec (mouvement ou pas à plat), puis au mode réglage (bouton tenu depuis la mise sous tension), puis à Allumé ; le mode réglage n'est accordé que si la cause de reset est une mise sous tension ; une norme d'accélération hors de 0,8 à 1,2 g est « pas à plat » (redémarrage en l'air = échec) ; les deux causes de REQ-038 « Causes et paramètres dans le statut sans fil » sont conservées en RAM non initialisée avec marqueur et CRC pour survivre à un reset du chien de garde. Élément : ARC-023 « Initialisation et échec d'initialisation ».
**Alternatives écartées :** mode réglage prioritaire sur l'échec ; registre de sauvegarde TAMP.
**Raison :** délégation ; interprétations consignées dans DOU-138 « Interprétations de l'architecture logicielle : priorité de l'initialisation, causes de refus, sauvegarde et statut ».
**Doutes levés :** (aucun)

### DEC-227 — Réglages : page de flash de l'image, valeurs hors bornes, sauvegarde au sol
**Date :** 2026-10-29
**Concerne :** REQ-026 « Paramètres de vol réglables », REQ-027 « Sauvegarde et chargement des réglages », REQ-028 « Valeurs d'origine après la programmation »
**Décision :** les 29 valeurs fixes sont des constantes de compilation ; les 4 paramètres réglables (un mot de 64 bits) vivent dans la dernière page de flash, dont les valeurs d'origine sont dans l'image programmée (la programmation écrit donc les valeurs d'origine) ; aucune calibration par drone ; sans somme de contrôle ; une valeur lue hors bornes revient à la valeur d'origine du paramètre ; Sauvegarder seulement en mode réglage au sol, batterie d'au moins 3,5 V, environ 45 ms, chien de garde rafraîchi avant et après ; bornes de Modifier : gains 0,5 à 2,0, hauteur visée 0,5 à 1,2 m, vitesse de descente 0,15 à 0,5 m/s. Éléments : ARC-026 « Mode réglage et vol de réglage », ARC-027 « Paramètres de vol et stockage des réglages ».
**Alternatives écartées :** double copie à indicateur de validité ; saturation à la lecture (une page vierge donnerait un gain maximal).
**Raison :** délégation, simplicité, compatible avec DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » et DEC-130 « Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté ».
**Doutes levés :** DOU-115 « Contenu et interruption de la réécriture de la zone des réglages par la reprogrammation », DOU-120 « Écriture en mémoire sous tension basse ou pendant une phase de vol »

### DEC-228 — Effets locaux : table des dix effets, buzzer actif à un seul timbre
**Date :** 2026-10-29
**Concerne :** REQ-018 « Effets locaux par situation », REQ-019 « Perceptibilité et distinction des effets »
**Décision :** voyant RGB (couleur et rythme) et buzzer magnétique actif (nombre et durée des bips), table des dix effets dans « Architecture » ; effets d'événement de 1,0 s ; moteurs en marche, lumière seule. Éléments : ARC-011 « Voyant RGB et avertisseur sonore », ARC-024 « Effets locaux (logiciel) ». La distinction reste à vérifier à TS-014 « Perceptibilité et distinction des effets ».
**Alternatives écartées :** piézo passif (environ 50 dB à 1 m, à peine audible) ; sons à plusieurs fréquences (buzzer actif impossible).
**Raison :** délégation, simplicité.
**Doutes levés :** (aucun)

### DEC-229 — Faisabilité conjointe : bilan, verdict marginal, mesures au banc avant la commande de la carte
**Date :** 2026-10-29
**Concerne :** REQ-031 « Drone de poche », REQ-013 « Marge de batterie pour un vol complet », REQ-012 « Coupure sur sous-tension de la batterie », REQ-003 « Conditions de départ du drone », REQ-006 « Stabilisation après le lancer »
**Décision :** le bilan (masse 65 g pour 100 g, poussée/poids 1,35, 5,5 A en stationnaire et 9,5 A en crête, chute de tension jusqu'à 3,17 V avec 3,7 V à l'armement) donne un verdict marginal à infaisable pour la tension. Les valeurs de « Exigences système » ne sont pas modifiées maintenant. Avant de commander la carte, mesurer au banc la poussée, le courant et la résistance interne. Si le banc donne moins de 20 g par moteur ou plus de 60 mΩ, l'architecte proposera à l'utilisateur de relever le seuil d'armement à 3,9 V et d'abaisser la sous-tension à 3,0 V sous charge (modification de REQ-003 « Conditions de départ du drone » et REQ-012 « Coupure sur sous-tension de la batterie »), puis d'étudier le brushless 1S. Éléments : ARC-014 « Bilan de masse, de poussée et d'autonomie », ARC-006 « Moteurs, hélices et protège-hélices », ARC-008 « Batterie et connecteur débranchable ».
**Alternatives écartées :** modifier tout de suite les seuils (hypothèses non mesurées) ; batterie 1300 mAh (+9 g, rapport 1,19).
**Raison :** délégation ; toutes les valeurs du bilan sont des estimations.
**Doutes levés :** (aucun) ; DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie » reste ouvert, non bloquant.

### DEC-230 — Plan de livraison par jalons, ordre de livraison levé
**Date :** 2026-10-29
**Concerne :** REQ-005 « Démarrage des moteurs sur geste volontaire seulement », REQ-026 « Paramètres de vol réglables », REQ-041 « Conditions d'acceptation de la commande Décoller »
**Décision :** trois jalons : J1 vol normal complet (valeurs fixes et valeurs d'origine en constantes), J2 radio (statut, variables, Arrêt), J3 mode réglage (Décoller, Modifier, Sauvegarder, flash). REQ-005 « Démarrage des moteurs sur geste volontaire seulement » est vraie avec son seul premier cas jusqu'à J3. Élément : ARC-029 « Plan de livraison par jalons ».
**Alternatives écartées :** tout livrer d'un coup ; radio avant le vol.
**Raison :** délégation, un vol le plus tôt possible.
**Doutes levés :** DOU-136 « Ordre de livraison : exigence essentielle dépendant du mode réglage souhaitable »

### DEC-231 — Garanties d'arrêt, batterie basse et consommation résiduelle : doutes levés
**Date :** 2026-10-29
**Concerne :** REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage », REQ-012 « Coupure sur sous-tension de la batterie », REQ-037 « Comportement en échec d'initialisation »
**Décision :** (1) arrêt des moteurs garanti par le matériel à tout reset, brown-out ou débranchement (rappel de grille), par le chien de garde en cas de blocage, et par l'échec d'initialisation après un redémarrage en l'air ; non couverts : MOSFET en court-circuit, pont de soudure, carte en débogage (hélices démontées pour programmer, à écrire dans la page de consignes). (2) Après une sous-tension, état absorbant sans hystérésis : pas de redémarrage ; une batterie déjà sous 3,3 V au branchement finit en échec d'initialisation ; BOR niveau 3 (environ 2,5 V). (3) Pas de seuil de protection distinct ; en échec par sous-tension le logiciel met les capteurs en veille et passe l'horloge à 16 MHz (environ 12 mA, soit 1,4 à 2,8 h avant 3,0 V, estimation à mesurer) ; la page de consignes dit de débrancher ; risque accepté. Éléments : ARC-007 « Étage de puissance des moteurs coupés par défaut », ARC-009 « Alimentation de la logique et mesure de la tension », ARC-022 « Chien de garde », ARC-023 « Initialisation et échec d'initialisation ».
**Alternatives écartées :** détecteur matériel à 2,9 V coupant le LDO (composant en plus, repli) ; hystérésis et réarmement automatique (contraire à REQ-037 « Comportement en échec d'initialisation »).
**Raison :** délégation, simplicité.
**Doutes levés :** DOU-060 « Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle », DOU-109 « Batterie déjà déchargée : redémarrages répétés, décharge profonde et état après une coupure logicielle », DOU-118 « Seuil de protection et consommation résiduelle du drone laissé allumé »

### DEC-232 — Nouveaux doutes d'architecture ouverts
**Date :** 2026-10-29
**Concerne :** REQ-022 « Arrêt sans fil », REQ-017 « Initialisation en 3 secondes », REQ-009 « Atterrissage doux », REQ-008 « Tenue du vol stationnaire »
**Décision :** trois doutes non bloquants sont ouverts : DOU-137 « Latence de bout en bout de l'arrêt sans fil sur Bluetooth » (latence de l'arrêt sans fil sur Bluetooth), DOU-138 « Interprétations de l'architecture logicielle : priorité de l'initialisation, causes de refus, sauvegarde et statut » (interprétations de l'architecture logicielle) et DOU-139 « Capteurs de hauteur et de flux : hauteur de montage et sols sans texture » (hauteur de montage du capteur de hauteur, sols sans texture pour le flux optique). DOU-133 « Forme des dix effets locaux : lumière, son, distinction mesurable » et DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie » restent ouverts.
**Alternatives écartées :** trancher sans essai ce qui dépend de la mesure.
**Raison :** délégation : doute ouvert non bloquant quand seule une mesure peut répondre.
**Doutes levés :** (aucun)

### DEC-233 — Relecture de porte architecture : corrections décidées par délégation
**Date :** 2026-10-29
**Concerne :** « Architecture » — `projets/boomrone/03-architecture.md`, « Plans de test » — `projets/boomrone/05-plans-de-test.md`
**Décision :** les trois relectures de porte (`critique`, `coherence-clarte`, `exigences-tracabilite`) sont traitées sans question à l'utilisateur. (1) `motors_cut()` force d'abord les sorties du timer à l'état bas avant d'arrêter le timer ; tension de grille mesurée à {TI-011 « Cadence du cycle et temps de réponse de l'arrêt d'urgence »}. (2) {REQ-013 « Marge de batterie pour un vol complet »} n'est pas établie avant les mesures au banc : les valeurs des exigences ne sont pas changées, les critères de {TI-008 « Batterie, connecteur, chute de tension et mesure de tension »} (résistance totale d'au plus 60 mΩ, tension sous 3,3 V moins de 100 ms) déclenchent le repli R1 + R2 ({DEC-229 « Faisabilité conjointe : bilan, verdict marginal, mesures au banc avant la commande de la carte »}) ; la porte « architecture », si l'utilisateur l'accorde, vaut avec cette réserve. (3) Hauteur du drone = lecture du capteur moins 20 mm de montage, coupure à une lecture brute d'environ 45 mm. (4) Le chien de garde est rafraîchi par l'initialisation et autour des écritures de flash. (5) Mise sous tension reconnue à l'absence du marqueur de la RAM `.noinit` (et non au drapeau de reset), causes conservées avec marqueur et CRC. (6) Budget unique du cycle : 300 µs, tâche de fond 200 µs, alarme 500 µs. (7) Délais alignés : arrêt par le bouton 12 ms estimé et 15 ms d'essai depuis l'appui, arrêt sans fil 5 ms côté drone, phase Lancé 612 ms estimée et 700 ms d'essai. (8) Défaut de capteur en vol : coupure, cause « échec de stabilisation » ({DOU-140 « Défaut de capteur en vol : cause et effet rattachés à l'échec de stabilisation »}). (9) Tests ajoutés : garde du bouton, délai de Modifier, critères de stationnaire, configuration de la centrale, gains aux bornes, effets à 3,4 V, critères numériques de {TI-008 « Batterie, connecteur, chute de tension et mesure de tension »}, {TI-010 « Liaison Bluetooth à basse consommation »} et {TI-021 « Arrêt sans fil et filtrage des commandes par état »}. (10) Glossaire fusionné sans doublon, sons définis (court 100 ms, long 250 ms, très long 500 ms), débit 140 octets/s, autonomie 49 mAh, incertitude ±4,5 g, diagrammes corrigés. Le défaut de l'outil (12 « SCN sans BES ») n'est pas corrigé ici : hors périmètre ({DEC-156 « Couverture des scénarios vérifiée à la main, outil de traçabilité inchangé »}).
**Alternatives écartées :** imposer R1 + R2 maintenant (hypothèses non mesurées) ; ouvrir des doutes bloquants (la porte reste à l'utilisateur) ; retirer le seuil de 3,5 V de Sauvegarder (gardé, signalé dans {DOU-138 « Interprétations de l'architecture logicielle : priorité de l'initialisation, causes de refus, sauvegarde et statut »}).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}).
**Doutes levés :** (aucun) ; doute ouvert : {DOU-140 « Défaut de capteur en vol : cause et effet rattachés à l'échec de stabilisation »}.

### DEC-234 — JLCPCB, fabricant de la carte : contrainte de début de projet
**Date :** 2026-10-29
**Concerne :** « Architecture » — `projets/boomrone/03-architecture.md` (ARC-013 « Carte électronique JLCPCB, câblage et assemblage »), « Notes d'architecture » — `projets/boomrone/notes-architecture.md`
**Décision :** la carte électronique est fabriquée par JLCPCB. C'est une **contrainte donnée par l'utilisateur dès le début du projet** (citée dans DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais » et dans les notes d'architecture), pas un choix de l'architecte. Les règles de fabrication de JLCPCB (largeur de piste et de via, cuivre, épaisseur, délais) s'imposent à ARC-013 « Carte électronique JLCPCB, câblage et assemblage » ; les composants de la carte sont à choisir **le plus possible parmi les pièces en stock chez JLCPCB** (catalogue LCSC), précision de l'utilisateur le 2026-10-29. Exceptions admises : les moteurs, les hélices, la batterie et les autres pièces mécaniques ou d'énergie (cadre, anneaux de protection, connecteur batterie si absent du stock). Les cartes de capteurs et le module Bluetooth, achetés tout faits ailleurs, ne sont pas dans cette liste : ils restent permis mais sont à confirmer un à un ({DOU-141 « Assemblage de la carte : à la main ou composants posés par JLCPCB, et disponibilité des pièces chez LCSC »}), en préférant la puce nue en stock chez JLCPCB quand l'assemblage s'y prête. La contrainte reste à écrire dans les exigences à la prochaine révision (aucune exigence validée n'est modifiée ici).
**Alternatives écartées :** laisser « commandée en ligne » sans fabricant (la contrainte se perdrait) ; changer de fabricant (non demandé).
**Raison :** précisions de l'utilisateur en chat, 2026-10-29 : « il faut ajouter que JLCPCB est une contrainte du début de projet », puis « il faut aussi utiliser le plus possible des composants en stock chez JLCPCB sauf moteur, hélice, batterie... ».
**Doutes levés :** (aucun) ; ouvre {DOU-141 « Assemblage de la carte : à la main ou composants posés par JLCPCB, et disponibilité des pièces chez LCSC »}.

### DEC-235 — Catalogue JLCPCB/LCSC vérifié : composants retenus
**Date :** 2026-10-29
**Concerne :** « Architecture » — `projets/boomrone/03-architecture.md` (section « Nomenclature et catalogue JLCPCB/LCSC »), ARC-007 « Étage de puissance des moteurs coupés par défaut », ARC-009 « Alimentation de la logique et mesure de la tension », ARC-011 « Voyant RGB et avertisseur sonore », ARC-012 « Module radio Bluetooth à basse consommation »
**Décision :** stocks relevés le 2026-10-29 par l'interface publique de recherche de composants de JLCPCB (le site de LCSC refuse l'accès automatique, les fiches techniques n'ont pas pu être lues). Composants retenus, tous en stock : STM32G431CBT6 (C529355), LSM6DSOTR (C2655100), VL53L1CXV0FY/1 (C190004), AO3400A (C20917, basic), diode SS34 (C8678, basic) à la place de SS24 (frais d'extension), MCP1700T-3002E/TT (C62244), XT30PW mâle (C431092), bouton TS-1088-AR02016 (C720477), voyant SZYY1615RGB-B (C3029071), buzzer SMD-9650-3327 (C42420997), ferrite 120 Ω (C14709) à la place de 220 Ω, condensateur de 22 µF en 1206 25 V (C12891), passifs 0603 « basic », pont de mesure à 0,1 %. Le module HM-10 et ses clones (JDY-23, HC-08, JDY-18, DX-BT24) sont à stock 0 : remplacé par l'Ebyte E104-BT02 (C411314, 649 en stock, DA14580). Aucune valeur non vérifiée n'est présentée comme vérifiée : débit, service et commandes AT du E104-BT02, et assemblage du PMW3901, restent « non vérifiés » (DOU-151 « Module E104-BT02 : débit par défaut, service, absence de commande AT », DOU-152 « PMW3901 : puce nue ou carte achetée, alimentation et refusion »).
**Alternatives écartées :** garder le HM-10 acheté ailleurs (hors stock JLCPCB, contraire à DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet ») ; ESP32-C3 (seconde chaîne de programmation) ; inventer ou recopier des numéros de pièce sans vérification.
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) ; contrainte de {DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »}.
**Doutes levés :** (aucun)

### DEC-236 — Assemblage par JLCPCB : puces nues, carte double face, flux acheté
**Date :** 2026-10-29
**Concerne :** ARC-013 « Carte électronique JLCPCB, câblage et assemblage », ARC-003 « Centrale inertielle », ARC-004 « Capteur de hauteur à temps de vol », ARC-005 « Capteur de flux optique », ARC-012 « Module radio Bluetooth à basse consommation », DOU-141 « Assemblage de la carte : à la main ou composants posés par JLCPCB, et disponibilité des pièces chez LCSC »
**Décision :** (1) Assemblage PCBA par JLCPCB de tous les composants CMS, y compris le LQFP-48 ; restent à la main : 8 fils des moteurs, XT30, en-tête SWD, carte du flux et batterie. (2) Puces nues sur la carte pour la centrale inertielle (LGA-14) et le capteur de hauteur (LGA-12), qui sont en stock et assemblables ; masse recalculée plus faible. (3) Pour le flux optique : carte achetée (Pimoroni ou équivalent) soudée par 6 fils, car la puce nue PMW3901 annonce 1,8 à 2,1 V au catalogue, avec un profil de refusion inconnu et un assemblage non vérifié (exception admise à regret par simplicité : DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet » demande de préférer la puce nue ; doute DOU-152 « PMW3901 : puce nue ou carte achetée, alimentation et refusion »). (4) Carte double face : capteurs vers le sol sur la face basse, bouton, voyant, buzzer et module BLE sur la face haute ; assemblage « Standard » de JLCPCB (panneau de 4 cartes, fiduciaires), frais d'extension et délais à lire sur le devis (DOU-153 « Carte double face, assemblage Standard, frais d'extension et délais »). (5) Quantité de 5 cartes à la première commande.
**Alternatives écartées :** tout à la main (LQFP-48 et LGA trop risqués pour un premier drone) ; carte simple face « Économique » (refusion à 255 °C fixe, bouton et voyant du mauvais côté) gardée en repli ; PMW3901 nu avec LDO de 1,8 V (assemblage et optique non vérifiés) ; cartes capteurs achetées (hors stock, plus lourdes).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) ; contrainte de {DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »}.
**Doutes levés :** DOU-141 « Assemblage de la carte : à la main ou composants posés par JLCPCB, et disponibilité des pièces chez LCSC » ; ouvre DOU-152 « PMW3901 : puce nue ou carte achetée, alimentation et refusion », DOU-153 « Carte double face, assemblage Standard, frais d'extension et délais », DOU-154 « Vibrations des moteurs sur la centrale inertielle posée sur la carte rigide »

### DEC-237 — Écart avec REQ-044 : assemblage par JLCPCB, proposition à valider
**Date :** 2026-10-29
**Concerne :** REQ-044 « Assemblage à la main », REQ-029 « Composants disponibles à l'unité », ARC-013 « Carte électronique JLCPCB, câblage et assemblage »
**Décision :** REQ-044 « Assemblage à la main » (validée) demande un assemblage à la main ; l'architecture suit DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet » et DEC-236 « Assemblage par JLCPCB : puces nues, carte double face, flux acheté » : composants CMS posés par JLCPCB. Les exigences validées ne sont pas modifiées. Proposition de l'architecte à valider aux prochaines révisions des exigences : remplacer l'exigence par « La carte est fabriquée et assemblée par JLCPCB ; les moteurs, connecteurs et la batterie sont raccordés à la main avec un fer à souder, sans four ni outil spécial » et ajouter la contrainte JLCPCB et le stock du catalogue à REQ-029 « Composants disponibles à l'unité ». D'ici là, l'élément ARC-013 « Carte électronique JLCPCB, câblage et assemblage » est déclaré en écart avec REQ-044 « Assemblage à la main », l'écart étant suivi par DOU-150 « Écart entre l'exigence d'assemblage à la main et l'assemblage par JLCPCB » (non bloquant).
**Alternatives écartées :** modifier REQ-044 « Assemblage à la main » tout de suite (exigence validée, la modification appartient à l'utilisateur) ; garder l'assemblage à la main (contraire à la contrainte JLCPCB).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) ; contrainte de {DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »}.
**Doutes levés :** (aucun) ; ouvre DOU-150 « Écart entre l'exigence d'assemblage à la main et l'assemblage par JLCPCB »

### DEC-238 — Fréquences SPI et lecture de la centrale inertielle
**Date :** 2026-10-29
**Concerne :** ARC-003 « Centrale inertielle », ARC-005 « Capteur de flux optique », ARC-016 « Pilotes des capteurs et des sorties »
**Décision :** Corrections des deux revues d'experts. SPI1 (centrale) à 5,3 MHz au plus : 170 MHz divisé par 32 ; 8 MHz est impossible (diviseurs de 2 : 10,6 puis 5,3 MHz) et 10,6 MHz dépasse les 10 MHz du composant. SPI2 (flux) à 1,33 MHz : 170 MHz divisé par 128 ; 2,66 MHz dépasse les 2 MHz du composant. Centrale lue à chaque tick de 1 kHz avec un débit de sortie de 3,33 kHz (retard d'au plus 0,3 ms), pas de temps mesuré avec TIM2 ; INT1 (donnée prête) câblée sur PB0 pour l'initialisation et comme repli de lecture. Le détail des registres est renvoyé aux notes d'architecture.
**Alternatives écartées :** lecture déclenchée par INT1 à 1,66 kHz (plus de câblage et d'interruptions, gardée en repli) ; SPI1 à 10,6 MHz (hors limite du composant).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) ; contrainte de {DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »}.
**Doutes levés :** (aucun)

### DEC-239 — Capteur de hauteur : pilote non bloquant, reprise, échec d'initialisation, mesure horodatée
**Date :** 2026-10-29
**Concerne :** ARC-004 « Capteur de hauteur à temps de vol », ARC-016 « Pilotes des capteurs et des sorties », ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse », ARC-023 « Initialisation et échec d'initialisation », DOU-140 « Défaut de capteur en vol : cause et effet rattachés à l'échec de stabilisation »
**Décision :** (1) Interface câblée complétée : GPIO1 sur PB6 (interruption externe) et XSHUT sur PB9. (2) Pilote non bloquant en vol : interruption de GPIO1 et lecture par DMA sur l'I2C, tâche de fond d'au plus 200 µs par appel ; la bibliothèque ST (ULD) ne sert qu'à l'initialisation, avant le cycle de 1 kHz. (3) Reprise par niveaux : relance de la lecture, déblocage du bus par 9 impulsions sur SCL, remise à zéro par XSHUT et ré-initialisation (110 à 170 ms estimés, du même ordre que les 200 ms de DOU-140 « Défaut de capteur en vol : cause et effet rattachés à l'échec de stabilisation ») réservée au sol : en vol, la reprise se limite aux deux niveaux rapides, la coupure à 200 ms de ARC-021 « Surveillance et coupures automatiques » reste le filet. (4) Capteur de hauteur absent ou muet après 2 tentatives de 300 ms avec remise à zéro par XSHUT entre elles : échec d'initialisation (REQ-037 « Comportement en échec d'initialisation »), déclaré avant 1 s, donc sous les 3 s de REQ-017 « Initialisation en 3 secondes ». (5) Mesure de hauteur horodatée (TIM2 au front de GPIO1), retard de 33 ms compensé par un recalage sur l'estimation des 64 derniers cycles.
**Alternatives écartées :** ULD appelée en vol (bloquante, jusqu'à plusieurs ms) ; tout reporter en conception détaillée ; ré-initialisation complète en vol (trop longue).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) ; contrainte de {DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »}.
**Doutes levés :** (aucun)

### DEC-240 — Brochage, timers, voyant et bouton
**Date :** 2026-10-29
**Concerne :** ARC-002 « Microcontrôleur et programmation par liaison SWD », ARC-010 « Bouton », ARC-011 « Voyant RGB et avertisseur sonore », ARC-024 « Effets locaux (logiciel) », « Notes d'architecture » — `projets/boomrone/notes-architecture.md`
**Décision :** (1) Affectation proposée : voyant rouge PB1, vert PB2, bleu PB10, buzzer PB11, bouton PB5, GPIO1 PB6, XSHUT PB9, SCL PA15, SDA PB7 ; PA15 et PB4 (JTAG, rappel haut au reset) jamais sur une grille. (2) Conflits de timers supprimés par construction : le voyant est modulé par le logiciel au tick de 1 kHz (10 niveaux), le buzzer est actif sur une simple sortie ; seuls TIM1 (moteurs), TIM2 (chronomètre libre de 1 MHz) et TIM6 (tick) sont utilisés, donc plus de conflit de TIM3 avec PB0 (INT1 de l'IMU) ni de TIM15 avec USART2. (3) Une résistance par couleur du voyant, calculée sur la LED retenue : rouge 120 Ω, vert et bleu 68 Ω, au plus 20 mA par couleur (47 Ω auraient donné environ 36 mA sur le rouge). (4) Rappel externe de 10 kΩ au 3,0 V pour le bouton (niveau stable avant la fin du reset pour le mode réglage). (5) Rappel de 100 kΩ à la masse sur les huit grilles (moteurs, voyant, buzzer). Numéros de broches physiques à relever dans la fiche (DOU-148 « Numéros de broches physiques du LQFP-48 à relever dans la fiche DS12589 »).
**Alternatives écartées :** voyant sur TIM3 ou TIM15 (conflits de broches) ; rappel interne seul pour le bouton (incertain au reset) ; affectation à confirmer plus tard sans proposition (l'utilisateur a demandé de la compléter).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) ; contrainte de {DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »}.
**Doutes levés :** (aucun) ; ouvre DOU-146 « Broches d'état du module Bluetooth et de mouvement du capteur de flux », DOU-147 « Compatibilité de l'empreinte avec le STM32G474 », DOU-148 « Numéros de broches physiques du LQFP-48 à relever dans la fiche DS12589 »

### DEC-241 — Mémoire et ordonnancement : règles de robustesse
**Date :** 2026-10-29
**Concerne :** ARC-015 « Structure logicielle et ordonnancement », ARC-007 « Étage de puissance des moteurs coupés par défaut », ARC-022 « Chien de garde », ARC-027 « Paramètres de vol et stockage des réglages »
**Décision :** (1) `.noinit` et tampons DMA en SRAM1 ; comportement de la SRAM2 au reset (option SRAM2_RST) à vérifier dans le manuel de référence. (2) Durées mesurées avec TIM2 et non par comptage de ticks, car une écriture de flash gèle l'exécution de 22 à 40 ms. (3) Règle « une seule tâche de fond par cycle ». (4) Le gestionnaire de HardFault appelle `motors_cut()`. (5) `motors_cut()` reconfigure explicitement les quatre broches moteur en sortie à l'état bas après avoir arrêté le timer.
**Alternatives écartées :** garder le comptage de ticks (faux après un gel de flash) ; plusieurs tâches de fond par cycle (dépassement du budget de 300 µs).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) ; contrainte de {DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »}.
**Doutes levés :** (aucun)

### DEC-242 — Alimentation de la logique à 130 mA et masse recalculée à 62 g
**Date :** 2026-10-29
**Concerne :** ARC-009 « Alimentation de la logique et mesure de la tension », ARC-014 « Bilan de masse, de poussée et d'autonomie », REQ-031 « Drone de poche », REQ-013 « Marge de batterie pour un vol complet »
**Décision :** (1) La consommation logique de 80 mA était sous-estimée : 76 mA typique, 103 mA au pire estimé, 130 mA retenus pour le dimensionnement. Le MCP1700T-3002E/TT (250 mA) convient : dissipation 0,16 W à 4,2 V, chute d'environ 0,1 à 0,2 V. L'autonomie de 49 mAh est inchangée (arrondi). (2) Masse recalculée : puces nues sur la carte (plus de cartes IMU et ToF), module BLE de 1,0 g, moins de fils : 62,3 g ±10,5 g (65 g avant), marge d'au moins 27 g, rapport poussée/poids 1,41. Les courants et les chutes de tension du bilan ne sont pas recalculés (choix prudent). (3) Pont de mesure à 0,1 % : incertitude estimée ±25 mV contre ±50 mV de REQ-003 « Conditions de départ du drone » ; la fuite d'entrée n'est pas relevée (DOU-142 « Fuite d'entrée de l'ADC et marge de ±50 mV de la mesure de tension »). Les tensions acceptées par les capteurs à 3,0 V sont suivies par DOU-143 « Tensions d'alimentation acceptées par les capteurs et le module à 3,0 V ».
**Alternatives écartées :** garder 80 mA (sous-estimé) ; régulateur 3,3 V (ne tient pas).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) ; contrainte de {DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »}.
**Doutes levés :** (aucun) ; ouvre DOU-142 « Fuite d'entrée de l'ADC et marge de ±50 mV de la mesure de tension », DOU-143 « Tensions d'alimentation acceptées par les capteurs et le module à 3,0 V », DOU-144 « Courant du buzzer, diode et tensions directes du voyant RGB », DOU-145 « Vol entre la dernière mesure de hauteur et la coupure à 200 ms »

### DEC-243 — Latence de l'arrêt sans fil et module Bluetooth : mesure avant la commande de la carte
**Date :** 2026-10-29
**Concerne :** REQ-022 « Arrêt sans fil », ARC-012 « Module radio Bluetooth à basse consommation », ARC-025 « Protocole et service du statut sans fil », DOU-137 « Latence de bout en bout de l'arrêt sans fil sur Bluetooth »
**Décision :** La latence de bout en bout de l'arrêt sans fil (200 ms de REQ-022 « Arrêt sans fil ») est mesurée tôt, avec un module E104-BT02 seul relié à l'ordinateur par un adaptateur USB-UART, avant de commander la carte (TI-010 « Liaison Bluetooth à basse consommation »). Le HM-10 n'étant pas en stock chez JLCPCB, le module retenu est l'Ebyte E104-BT02 (DEC-235 « Catalogue JLCPCB/LCSC vérifié : composants retenus »), avec quatre pastilles pour souder un autre module en plan B (E104-BT52 en repli). DOU-137 « Latence de bout en bout de l'arrêt sans fil sur Bluetooth » reste ouvert.
**Alternatives écartées :** commander la carte avant la mesure ; laisser le HM-10 hors catalogue.
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) ; contrainte de {DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »}.
**Doutes levés :** (aucun) ; ouvre DOU-151 « Module E104-BT02 : débit par défaut, service, absence de commande AT » et DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion »

### DEC-244 — Relecture de porte de la révision JLCPCB : corrections décidées par délégation
**Date :** 2026-10-29
**Concerne :** « Architecture » — `projets/boomrone/03-architecture.md`, « Plans de test » — `projets/boomrone/05-plans-de-test.md`, « Notes d'architecture » — `projets/boomrone/notes-architecture.md`
**Décision :** les trois relectures (`critique`, `coherence-clarte`, `exigences-tracabilite`) de la révision, de DEC-235 « Catalogue JLCPCB/LCSC vérifié : composants retenus » à DEC-243 « Latence de l'arrêt sans fil et module Bluetooth : mesure avant la commande de la carte », sont traitées sans question. (1) Huit doutes non bloquants ouverts : DOU-156 « Vérifications avant la commande de la carte », DOU-157 « VL53L1CX contre VL53L1X : identifiant, bibliothèque et registres », DOU-158 « Initialisation du capteur de hauteur plus longue que le chien de garde », DOU-159 « Ordonnancement des tâches de fond : flux à 100 Hz, pilote de hauteur et latence de l'arrêt sans fil », DOU-160 « Mesure de hauteur valide et sols sombres ou brillants », DOU-161 « Tensions directes du voyant RGB : visibilité du vert et du bleu entre 3,4 et 3,7 V », DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie », DOU-163 « Valeurs de fiche à relever : rappel de GPIO1, résistance de l'AO3400A, USB du G431 ». (2) Tâches de fond choisies par priorité et seuil d'alarme du cycle porté de 500 à 800 µs (le pire cas de 300 + 200 µs égalait l'ancien seuil). (3) Attentes de la bibliothèque du capteur de hauteur découpées ou liées au rafraîchissement du chien de garde. (4) Une mesure de hauteur non valide plus de 200 ms coupe les moteurs (choix prudent). (5) `motors_cut()` : avec MOE = 0 les sorties sont libérées et tenues basses par les rappels, puis reconfigurées en sortie basse. (6) Courants du voyant écrits avec leurs hypothèses (18 mA, ou 15 et 12 mA). (7) Notes ajoutées à TA-015 « Inspection de la fabrication à la main » et TS-020 « Fabrication à la main » : écart connu avec l'assemblage par JLCPCB (DOU-150 « Écart entre l'exigence d'assemblage à la main et l'assemblage par JLCPCB »). Cet écart n'est pas rendu bloquant par l'architecte (la porte appartient à l'utilisateur), mais `reprise.md` invite l'utilisateur à le trancher avant la porte. (8) ARC-030 « Page de consignes d'emploi » : la page actuelle ne contient pas encore les consignes de l'architecture, à compléter en conception détaillée.
**Alternatives écartées :** rendre DOU-150 « Écart entre l'exigence d'assemblage à la main et l'assemblage par JLCPCB » bloquant (décision de l'utilisateur) ; modifier REQ-044 « Assemblage à la main » (exigence validée).
**Raison :** délégation explicite de l'utilisateur, 2026-10-29 ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}).
**Doutes levés :** (aucun)

### DEC-245 — REQ-044 réécrite : carte fabriquée et assemblée par JLCPCB, raccordements à la main
**Date :** 2026-10-29
**Concerne :** REQ-044 « Assemblage à la main », TS-020 « Fabrication à la main », TA-015 « Inspection de la fabrication à la main »
**Décision :** REQ-044 « Assemblage à la main » est réécrite sur la proposition de DEC-237 « Écart avec REQ-044 : assemblage par JLCPCB, proposition à valider » : la carte est fabriquée et assemblée par JLCPCB ; les moteurs, le connecteur de batterie, l'en-tête de programmation et les cartes de capteurs achetées sont raccordés à la main sans four ni outil spécial ; aucun composant à souder à la main n'est un BGA ni n'a un pas de moins de 0,5 mm ; les composants de la carte sont pris le plus possible parmi les pièces en stock chez JLCPCB, sauf moteurs, hélices, batterie et pièces mécaniques (DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »). Les titres de REQ-044 « Assemblage à la main », TS-020 « Fabrication à la main » et TA-015 « Inspection de la fabrication à la main » sont conservés (les raccordements restent à la main) ; TS-020 « Fabrication à la main » vérifie le stock JLCPCB ou l'exception de chaque ligne et TA-015 « Inspection de la fabrication à la main » rejoue le raccordement à la main. Le statut de REQ-044 « Assemblage à la main » reste « Validé » sur accord de l'utilisateur.
**Alternatives écartées :** garder l'énoncé d'origine (il contredit l'assemblage par JLCPCB) ; renommer REQ-044 « Assemblage à la main » (les raccordements restent à la main, les renvois seraient à refaire).
**Raison :** accord explicite de l'utilisateur en chat, 2026-10-29 : « Oui, réécris ».
**Doutes levés :** DOU-150 « Écart entre l'exigence d'assemblage à la main et l'assemblage par JLCPCB »
**Modifie :** DEC-237 « Écart avec REQ-044 : assemblage par JLCPCB, proposition à valider » (la proposition est appliquée).

### DEC-246 — Flux optique : puce PMW3901MB-TXQT achetée et posée par JLCPCB
**Date :** 2026-10-29
**Concerne :** ARC-005 « Capteur de flux optique », ARC-013 « Carte électronique JLCPCB, câblage et assemblage », ARC-014 « Bilan de masse, de poussée et d'autonomie », REQ-044 « Assemblage à la main », DEC-236 « Assemblage par JLCPCB : puces nues, carte double face, flux acheté », DOU-152 « PMW3901 : puce nue ou carte achetée, alimentation et refusion »
**Décision :** (1) Le capteur de flux optique est la puce PMW3901MB-TXQT de PixArt (C43496881, boîtier COB-28 de 6 × 6 × 2,28 mm, 182 en stock le 2026-10-29, « expand »), achetée et posée par JLCPCB sur la face basse de la carte, à la place de la petite carte achetée ailleurs (Pimoroni ou équivalent) de DEC-236 « Assemblage par JLCPCB : puces nues, carte double face, flux acheté » (point 3 remplacé ; les autres points de DEC-236 « Assemblage par JLCPCB : puces nues, carte double face, flux acheté » restent). (2) Les 6 fils de la carte du flux disparaissent de la liste des raccordements à la main : restent les 8 fils des moteurs, le XT30, l'en-tête SWD, la batterie et la lentille du flux (DEC-248 « Flux optique : lentille collée à la main et repli sur carte achetée »). (3) La nomenclature et le tableau des choix de « Architecture » — `projets/boomrone/03-architecture.md` sont mis à jour ; la fiche PixArt version 1.00 du 2017-03-20 a été téléchargée par la page de détail de LCSC et lue le 2026-10-29. (4) DOU-152 « PMW3901 : puce nue ou carte achetée, alimentation et refusion » est levé ; les points restants sont suivis par DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce » et DOU-166 « PMW3901MB : plage de température de 0 à 40 °C et hauteur de montage avec la lentille ». REQ-044 « Assemblage à la main » (énoncé inchangé : « toute carte de capteur achetée toute faite » reste vrai pour le repli) cite cette décision.
**Alternatives écartées :** garder la carte achetée par 6 fils (contraire à DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet » quand la puce est en stock) ; capteur différent (PAW3903, moins documenté ; Flow deck v2 de Bitcraze, hors catalogue).
**Raison :** instruction de l'utilisateur en chat, 2026-10-29 : le capteur de flux optique doit être acheté et posé par JLCPCB, tout ce qui peut être pris chez JLCPCB l'est ({DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »}) ; exceptions inchangées : moteurs, hélices, batterie, cadre et anneaux ; délégation totale pour le reste ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}).
**Doutes levés :** DOU-152 « PMW3901 : puce nue ou carte achetée, alimentation et refusion » ; ouvre DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce », DOU-166 « PMW3901MB : plage de température de 0 à 40 °C et hauteur de montage avec la lentille »
**Modifie :** DEC-236 « Assemblage par JLCPCB : puces nues, carte double face, flux acheté » (point 3, flux optique).

### DEC-247 — Flux optique : alimentation en 2,0 V par un régulateur dédié, signaux en 3,0 V
**Date :** 2026-10-29
**Concerne :** ARC-009 « Alimentation de la logique et mesure de la tension », ARC-005 « Capteur de flux optique », ARC-002 « Microcontrôleur et programmation par liaison SWD », DOU-143 « Tensions d'alimentation acceptées par les capteurs et le module à 3,0 V »
**Décision :** (1) La fiche PixArt lue donne VDD de 1,8 à 2,1 V (2,0 V typique, maximum absolu 2,1 V, bruit compris) et VDDIO de 1,8 à 3,6 V, environ 9 mA. VDD est donc alimenté en 2,0 V par un régulateur linéaire dédié XC6206P202MR-G (SOT-23, 2,0 V fixe, 120 mA au catalogue, C2891260, 2 103 en stock le 2026-10-29, « expand », 0,215 dollar) lui-même alimenté par le rail de 3,0 V du MCP1700T-3002E/TT (marge de chute de 0,9 V avec le rail à 2,9 V). (2) VDDIO est au rail de 3,0 V : les signaux de SPI2 restent à 3,0 V, aucun décalage de niveau n'est ajouté ; NRESET tirée au 3,0 V par 10 kΩ, MOTION non câblée (DEC-240 « Brochage, timers, voyant et bouton » conservé). (3) La charge de 9 mA est comptée dans les 130 mA de DEC-242 « Alimentation de la logique à 130 mA et masse recalculée à 62 g » ; dissipation de 9 mW ; courant batterie inchangé. (4) Valeurs non relevées, marquées « à vérifier dans la fiche » : tolérance de la sortie, chute à 9 mA et capacité de sortie du XC6206, condensateurs de la figure 8, seuil d'entrée haut du G431 (DOU-165 « Flux optique : alimentation en 2,0 V, valeurs de fiche et mise sous tension »).
**Alternatives écartées :** ME6211C18M5G-N (1,8 V, C236671, 49 683 en stock : la sortie nominale est le minimum de VDD, sans marge) ; alimenter VDD directement au rail de 3,0 V (dépasse le maximum absolu de 2,1 V) ; décalage de niveau pour SPI2 (inutile puisque VDDIO accepte 3,6 V) ; régulateur 2,0 V alimenté par la batterie (même consommation, mais exposé aux surtensions de la connexion de DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion »).
**Raison :** instruction de l'utilisateur en chat, 2026-10-29 (puce posée par JLCPCB) ; délégation totale ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) : la solution la plus simple qui respecte la fiche.
**Doutes levés :** (aucun) ; ouvre DOU-165 « Flux optique : alimentation en 2,0 V, valeurs de fiche et mise sous tension » ; met à jour DOU-143 « Tensions d'alimentation acceptées par les capteurs et le module à 3,0 V »

### DEC-248 — Flux optique : lentille collée à la main et repli sur carte achetée
**Date :** 2026-10-29
**Concerne :** ARC-005 « Capteur de flux optique », ARC-013 « Carte électronique JLCPCB, câblage et assemblage », TI-004 « Flux optique et vitesse horizontale », TA-015 « Inspection de la fabrication à la main », TS-020 « Fabrication à la main », REQ-044 « Assemblage à la main »
**Décision :** (1) La fiche donne la lentille LN03-ZSZ (« Lens Assembly ») comme une pièce séparée, sans mise au point ; le catalogue de JLCPCB n'a pas cette référence (recherche du 2026-10-29), mais décrit C43496881 comme un lot de 2 pièces (photo : puce et lentille). Hypothèse retenue, à confirmer (DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce ») : la lentille est livrée avec la puce et collée à la main sur la puce posée. (2) TA-015 « Inspection de la fabrication à la main » et TS-020 « Fabrication à la main » remplacent « carte du flux raccordée à la main » par « lentille du flux collée à la main » ; titres inchangés, énoncé de REQ-044 « Assemblage à la main » inchangé. (3) Repli : si JLCPCB refuse d'assembler la puce, si la lentille manque, ou si l'essai de TI-004 « Flux optique et vitesse horizontale » est mauvais avec la puce, retour à la carte achetée Pimoroni PMW3901 (6 plots sur la carte, alimentation de la carte à relever) ; les 6 plots peuvent être prévus dès la première carte (quelques mm², sans coût) : à décider au routage, non fait ici.
**Alternatives écartées :** abandonner le flux (la dérive de 0,5 m en 10 s est hors d'atteinte sans lui) ; commander la lentille ailleurs sans avoir vérifié le lot (coût inutile si elle est fournie).
**Raison :** délégation totale ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}) ; la simplicité d'abord, mais sans supposer la lentille.
**Doutes levés :** (aucun) ; suivi par DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce »
**Modifie :** DEC-245 « REQ-044 réécrite : carte fabriquée et assemblée par JLCPCB, raccordements à la main » (la liste des raccordements à la main de TA-015 « Inspection de la fabrication à la main » et de TS-020 « Fabrication à la main » ne cite plus la carte du flux).

### DEC-249 — Flux optique : masse recalculée à 61 g, essais et documents mis à jour
**Date :** 2026-10-29
**Concerne :** ARC-014 « Bilan de masse, de poussée et d'autonomie », REQ-031 « Drone de poche », TI-001 « Alimentation, programmation SWD et octets d'option », TI-002 « Bus SPI, I2C et capteurs », TI-004 « Flux optique et vitesse horizontale »
**Décision :** (1) Masse : puce et lentille 0,4 g ±0,1 g (poids du lot au catalogue : 0,357 g) à la place de la carte achetée de 1,5 g ±0,4 g ; carte assemblée 5,2 g ±1,0 g (régulateur et passifs du flux, estimation) ; câblage 2,2 g ±0,7 g (6 fils en moins, estimation) ; total 61,1 g (au pire 71,2 g), ±10,1 g cumulé, ±4,4 g quadratique ; marge d'au moins 28 g sous 100 g (REQ-031 « Drone de poche ») ; rapport poussée/poids 1,44 (88 g sur 61,1 g, plage de 0,8 à 2,2 non recalculée). Les courants et chutes de tension ne sont pas recalculés. (2) TI-001 « Alimentation, programmation SWD et octets d'option » mesure le rail de 2,0 V entre 1,8 et 2,1 V et le courant du flux ; TI-002 « Bus SPI, I2C et capteurs » vérifie les niveaux de SPI2 ; TI-004 « Flux optique et vitesse horizontale » mesure sol texturé et sol sans texture, la température de la puce et l'effet de la lentille, avec le critère de repli de DEC-248 « Flux optique : lentille collée à la main et repli sur carte achetée ». (3) « Notes d'architecture », « Glossaire » (entrée « COB, lentille du flux optique »), « Reprise », « Registre de doutes » et « Journal des décisions » mis à jour.
**Alternatives écartées :** garder 62,3 g (l'écart de 1,2 g est dans l'incertitude, mais le bilan reste honnête et traçable).
**Raison :** délégation totale ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}).
**Doutes levés :** (aucun)
**Modifie :** DEC-242 « Alimentation de la logique à 130 mA et masse recalculée à 62 g » (masse 62,3 g remplacée par 61,1 g ; les 9 mA du flux étaient déjà inclus dans les 130 mA : la somme des consommations détaillées, 61 à 81 mA, laisse l'écart avec le typique de 76 mA et le pire de 103 mA, estimation).

### DEC-250 — Flux optique : corrections des relectures, plots de repli prévus dès la première carte
**Date :** 2026-10-29
**Concerne :** ARC-005 « Capteur de flux optique », ARC-009 « Alimentation de la logique et mesure de la tension », ARC-013 « Carte électronique JLCPCB, câblage et assemblage », TI-001 « Alimentation, programmation SWD et octets d'option », TI-002 « Bus SPI, I2C et capteurs », TI-004 « Flux optique et vitesse horizontale », TA-015 « Inspection de la fabrication à la main », TS-020 « Fabrication à la main », REQ-044 « Assemblage à la main »
**Décision :** les relectures de `critique`, `coherence-clarte` et `exigences-tracabilite` sont traitées sans question. (1) Six plots de repli (3,0 V, masse, SCK, MOSI, MISO, CS) sont prévus dès la première carte (quelques mm², sans composant) pour souder la carte achetée si la puce ou la lentille pose problème (reprend le point 3 de DEC-248 « Flux optique : lentille collée à la main et repli sur carte achetée », « à décider au routage », maintenant décidé). (2) DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce » complété (ordre des faces, humidité, unité du stock, collage) ; DOU-165 « Flux optique : alimentation en 2,0 V, valeurs de fiche et mise sous tension » complété (séquence, creux du rail, tolérance du XC6206, à lever avant le gel de la nomenclature) ; DOU-166 « PMW3901MB : plage de température de 0 à 40 °C et hauteur de montage avec la lentille » complété (échauffement du régulateur MCP1700T-3002E/TT, absence d'exigence de température ambiante). (3) TI-001 « Alimentation, programmation SWD et octets d'option », TI-002 « Bus SPI, I2C et capteurs », TI-004 « Flux optique et vitesse horizontale », TA-015 « Inspection de la fabrication à la main » et TS-020 « Fabrication à la main » précisés (bornes de courant, coupures rapides, MISO à 2,55 V, essai sans lentille avant collage, critère d'acceptation du collage). (4) ARC-005 « Capteur de flux optique » cite REQ-044 « Assemblage à la main » et REQ-029 « Composants disponibles à l'unité ». (5) La plage de poussée/poids de 0,8 à 2,2 n'est plus citée (non reproductible). (6) Non fait : l'énoncé de REQ-044 « Assemblage à la main » (validée par l'utilisateur) n'est pas modifié ; il reste vrai pour le repli mais ne cite pas la lentille collée à la main : à soumettre à l'utilisateur. Aucun doute de la phase n'est rendu bloquant (la porte appartient à l'utilisateur).
**Alternatives écartées :** rendre DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce » bloquant (décision de l'utilisateur) ; modifier REQ-044 « Assemblage à la main » seul.
**Raison :** délégation totale ({DEC-218 « Délégation totale de la phase architecture à l'architecte »}).
**Doutes levés :** (aucun)

### DEC-251 — Porte architecture franchie : accord explicite de l'utilisateur
**Date :** 2026-10-30
**Concerne :** « Architecture » — `projets/boomrone/03-architecture.md` (30 éléments ARC) et « Plans de test » — `projets/boomrone/05-plans-de-test.md` (29 TI)
**Décision :** la porte « architecture » est franchie ; les 30 éléments ARC passent à « Validé » (les TI restent « Écrit », comme les TS et TA après leur porte) ; la phase « conception détaillée » peut s'ouvrir. État au franchissement : tag `gate-4-architecture-ready-v0`, aucun doute bloquant ouvert, doutes non bloquants listés dans `registre-doutes.md`, relectures de porte faites par `critique`, `coherence-clarte` et `exigences-tracabilite` (DEC-233 « Relecture de porte architecture : corrections décidées par délégation », DEC-244 « Relecture de porte de la révision JLCPCB : corrections décidées par délégation »).
**Alternatives écartées :** attendre les mesures au banc avant de franchir la porte (non retenu par l'utilisateur) ; continuer la phase « architecture ».
**Raison :** accord explicite de l'utilisateur en chat, 2026-10-30 : « passe la porte ». Rappels : DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie » reste ouvert, non bloquant (tension de la batterie sous charge marginale ; REQ-013 « Marge de batterie pour un vol complet » non établie avant les mesures au banc ; repli proposé : armement à 3,9 V et sous-tension à 3,0 V) ; avant la commande de la carte : mesures au banc (TI-007 « Moteurs, poussée, masse et dimensions », TI-008 « Batterie, connecteur, chute de tension et mesure de tension »), test du module Bluetooth seul (DOU-151 « Module E104-BT02 : débit par défaut, service, absence de commande AT »), devis JLCPCB (DOU-153 « Carte double face, assemblage Standard, frais d'extension et délais », DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce »), genre du XT30 (DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion ») ; `check_traceability --gate` échoue pour les 30 « ARC sans DES » (phase suivante) et les 12 « SCN sans BES » (défaut connu, DEC-156 « Couverture des scénarios vérifiée à la main, outil de traçabilité inchangé ») ; `tools/check_traceability_V2.py --gate --phase architecture` donne OK.
**Doutes levés :** (aucun)

### DEC-252 — Phase conception détaillée ouverte avant les mesures au banc
**Date :** 2026-10-30
**Concerne :** « Conception détaillée » — `projets/boomrone/04-conception-detaillee.md`, DEC-229 « Faisabilité conjointe : bilan, verdict marginal, mesures au banc avant la commande de la carte », DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie »
**Décision :** la phase « conception détaillée » est ouverte juste après la porte « architecture » (DEC-251 « Porte architecture franchie : accord explicite de l'utilisateur »), sans attendre les mesures au banc. Instruction de l'utilisateur en chat, 2026-10-30 : « cette première version ne sera pas passée par les mesures au banc ». Les 30 ARC sont à décliner en DES, avec les tests unitaires (TU) définis en même temps.
**Alternatives écartées :** faire les mesures au banc avant d'ouvrir la phase (proposé, non retenu).
**Raison :** instruction explicite de l'utilisateur. Écart signalé : DEC-229 « Faisabilité conjointe : bilan, verdict marginal, mesures au banc avant la commande de la carte » prévoyait ces mesures avant la commande de la carte ; la question de savoir si l'écart vaut renonciation à cette décision (seuils conservés ou repli à 3,9 V et 3,0 V) est tranchée par DEC-253 « Seuils de batterie conservés, sans mesures au banc pour la première version » ; DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie » reste ouvert, non bloquant.
**Doutes levés :** (aucun)

### DEC-253 — Seuils de batterie conservés, sans mesures au banc pour la première version
**Date :** 2026-10-30
**Concerne :** REQ-003 « Conditions de départ du drone », REQ-012 « Coupure sur sous-tension de la batterie », REQ-013 « Marge de batterie pour un vol complet », DEC-229 « Faisabilité conjointe : bilan, verdict marginal, mesures au banc avant la commande de la carte », DEC-252 « Phase conception détaillée ouverte avant les mesures au banc »
**Décision :** la conception détaillée garde les seuils actuels de REQ-003 « Conditions de départ du drone » et REQ-012 « Coupure sur sous-tension de la batterie » (pas de repli à 3,9 V et 3,0 V). La première version de la carte est commandée sans mesures au banc ; DEC-229 « Faisabilité conjointe : bilan, verdict marginal, mesures au banc avant la commande de la carte » n'est plus appliquée pour cette version. Les seuils restent réglables dans leurs bornes (DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel »), le repli reste possible après les premiers essais.
**Alternatives écartées :** repli à 3,9 V à l'armement et 3,0 V en sous-tension (modification des deux exigences) ; faire les mesures au banc avant la commande.
**Raison :** réponse de l'utilisateur en chat, 2026-10-30 : « Seuils actuels ». Risque connu : tension sous charge estimée à 3,17 V, REQ-013 « Marge de batterie pour un vol complet » non établie ; DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie » reste ouvert, non bloquant, à vérifier aux essais sur prototype.
**Doutes levés :** (aucun)

### DEC-254 — Délégation totale de la phase conception détaillée à l'architecte
**Date :** 2026-10-30
**Concerne :** « Conception détaillée » — `projets/boomrone/04-conception-detaillee.md` et section TU de « Plans de test » — `projets/boomrone/05-plans-de-test.md`
**Décision :** l'architecte rédige seul les DES et les TU de la phase « conception détaillée », comme pour l'architecture (DEC-218 « Délégation totale de la phase architecture à l'architecte »). Il choisit la solution la plus simple qui fonctionne, consigne ses décisions dans le journal et ses doutes dans le registre, fait relire par `critique`, `coherence-clarte` et `exigences-tracabilite`, et ne franchit pas la porte : l'accord explicite de l'utilisateur reste requis.
**Alternatives écartées :** consulter l'utilisateur à chaque module.
**Raison :** réponse de l'utilisateur en chat, 2026-10-30 : « l'architecte rédige les DES et les TU seul, comme pour l'architecture ».
**Doutes levés :** (aucun)

### DEC-255 — Conception détaillée : chaîne de développement et arborescence des fichiers
**Date :** 2026-10-30
**Concerne :** DES-001 « Schéma par blocs, réseaux et domaines de tension de la carte », DES-013 « Implantation, routage et fichiers de fabrication pour JLCPCB », DES-015 « Arborescence du firmware, édition de liens et budget de mémoire », DES-036 « Logiciel de suivi en Python »
**Décision :** (1) Matériel dessiné dans KiCad, exports vers JLCPCB par le greffon dédié, fichiers sous `projets/boomrone/hardware/`. (2) Firmware sous `projets/boomrone/firmware/` : arm-none-eabi-gcc, Makefile, registres CMSIS et pilotes LL de ST (pas la bibliothèque HAL, trop lourde et opaque pour un premier drone), bibliothèque ULD de ST pour le capteur de hauteur seulement. (3) Logiciel de suivi sous `projets/boomrone/tools/suivi.py` (le chemin `tools/suivi.py` de ARC-028 « Logiciel d'essai de l'appareil de suivi » se lit relativement au projet, pour ne pas toucher aux outils du dépôt). (4) Programmation par STM32CubeProgrammer et ST-LINK.
**Alternatives écartées :** STM32CubeIDE avec HAL (projet généré difficile à relire, tests sur PC malaisés) ; PlatformIO (une dépendance de plus) ; Eagle ou EasyEDA (EasyEDA relie à JLCPCB mais enferme les fichiers dans un service en ligne).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; la solution la plus simple qui fonctionne et qui reste lisible et testable.
**Doutes levés :** (aucun)

### DEC-256 — Tests unitaires compilés sur PC avec maquette des registres
**Date :** 2026-10-30
**Concerne :** section « Tests unitaires (TU) » de « Plans de test » — `projets/boomrone/05-plans-de-test.md`, DES-015 « Arborescence du firmware, édition de liens et budget de mémoire », DES-016 « Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond »
**Décision :** les tests unitaires du logiciel sont compilés avec `gcc` sur le PC et lancés par `make -C projets/boomrone/firmware test`. Les modules d'estimation, de contrôle et d'application n'accèdent jamais directement aux registres : ils passent par des fonctions de pilote que les tests remplacent par des maquettes. Les pilotes se testent avec une maquette des structures de registres de ST (fichier d'entête de substitution dans `firmware/test/mock/`). Macros d'assertion maison (`tu.h`, quelques lignes), sans bibliothèque extérieure. Les tests qui exigent le temps réel ou les bus réels sont ceux d'intégration (TI). Les calculs et les circuits sont vérifiés par script Python (`calculs.py`).
**Alternatives écartées :** tests uniquement sur la cible (lents, impossibles à automatiser, peu de cas limites) ; Unity ou CppUTest (dépendance sans nécessité) ; aucun test avant l'intégration.
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; les cas limites (seuils, priorités) se testent mieux en machine hôte, avec un temps simulé.
**Doutes levés :** (aucun) ; limite suivie par DOU-176 « Tests unitaires sur PC : écart entre la maquette de registres et le composant réel »

### DEC-257 — Valeurs de configuration des horloges, timers, bus et convertisseur
**Date :** 2026-10-30
**Concerne :** DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option », DES-022 « Pilote de la mesure de tension de la batterie », DES-016 « Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond »
**Décision :** HSI 16 MHz avec PLL M = 4, N = 85, R = 2 pour 170 MHz ; diviseurs de bus 1 ; flash à 8 états d'attente avec prefetch et caches ; TIM2 (compteur libre 1 MHz, prédiviseur 169), TIM6 (tick 1 kHz), TIM1 (rechargement 7082, 24,001 kHz) ; SPI1 diviseur 32, SPI2 diviseur 128 ; USART2 BRR 17708 ; ADC en horloge synchrone HCLK/4, temps d'échantillonnage 640,5 cycles, déclenché par TIM6. Les valeurs de registres de ST sont reprises de mémoire et à confirmer.
**Alternatives écartées :** quartz externe (composant en plus, inutile) ; ADC à 247,5 cycles (5,8 µs, inférieur aux 6 µs exigés par la source de 60 kohms) ; suréchantillonnage matériel x16 de l'ADC (le x10 de ARC-009 « Alimentation de la logique et mesure de la tension » est conservé).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; chaque valeur est la plus simple compatible avec les limites de DEC-238 « Fréquences SPI et lecture de la centrale inertielle ».
**Doutes levés :** (aucun) ; suivi par DOU-172 « Valeurs de configuration des périphériques à vérifier dans le manuel de référence »

### DEC-258 — Mesure de la tension : séquence de conversion et zone de maintien de la sous-tension
**Date :** 2026-10-30
**Concerne :** DES-022 « Pilote de la mesure de tension de la batterie », DES-029 « Surveillance et coupures automatiques », REQ-012 « Coupure sur sous-tension de la batterie », ARC-021 « Surveillance et coupures automatiques »
**Décision :** (1) Séquence de 14 conversions par tick : 10 de la batterie et 4 de la référence interne (le maximum de l'ADC est de 16 rangs). (2) Le compteur de sous-tension de ARC-021 « Surveillance et coupures automatiques » augmente sous 3,30 V, est conservé entre 3,30 V et 3,35 V et est remis à zéro à 3,35 V et plus, pour qu'un bruit de quelques millivolts autour du seuil n'empêche jamais indéfiniment la coupure ; le seuil de 3,3 V et la confirmation de 100 ms de REQ-012 « Coupure sur sous-tension de la batterie » ne changent pas. (3) Seuils conservés tels quels (DEC-253 « Seuils de batterie conservés, sans mesures au banc pour la première version »).
**Alternatives écartées :** remise à zéro dès 3,30 V (une oscillation de 5 mV autour du seuil empêcherait la coupure) ; hystérésis de 100 mV (retarde la remise à zéro inutilement).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte »).
**Doutes levés :** (aucun)

### DEC-259 — Contrôle : poussée linéarisée, mixeur en X et priorité à l'attitude
**Date :** 2026-10-30
**Concerne :** DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique », ARC-018 « Boucle de contrôle du vol »
**Décision :** les commandes du régulateur sont des fractions de poussée ; le rapport cyclique est la racine de la poussée multipliée par 3,7 V / tension de la batterie, limité à 0-1 (la poussée d'une hélice varie comme le carré de la vitesse, donc de la tension). Le mixeur est en X avec la numérotation et les signes de DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique ». En cas de saturation, le collectif est décalé pour conserver l'écart entre moteurs (l'attitude passe avant la hauteur).
**Alternatives écartées :** rapport cyclique directement proportionnel à la commande (gains qui varient avec le point de fonctionnement) ; priorité au collectif (perte d'attitude à pleine poussée, lancer à 4 m/s).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; une racine carrée de plus, calculée par le FPU en 14 cycles, pour des gains presque constants.
**Doutes levés :** (aucun) ; hypothèse suivie par DOU-171 « Gains de référence, poussée de sustentation et linéarisation de la poussée »

### DEC-260 — Gains de référence et constantes de départ provisoires
**Date :** 2026-10-30
**Concerne :** DES-023 « Filtre d'attitude de Mahony », DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique », REQ-026 « Paramètres de vol réglables », REQ-006 « Stabilisation après le lancer »
**Décision :** les gains, la poussée de sustentation de 0,69, le gain Kp du filtre de 2,0 s⁻¹, les gains de l'observateur et les seuils de qualité des capteurs sont des valeurs de départ, tirées de la théorie et de réglages connus de petits drones, non de mesures. Ils sont marqués provisoires comme les autres valeurs de DOU-131 « Valeurs provisoires des exigences, à valider aux essais sur prototype » et se règlent sur la potence puis en vol (TI-013 « Boucle de contrôle sur potence » et suivants). Aucun n'est une valeur de sécurité (les valeurs de sécurité sont les 29 valeurs fixes de REQ-026 « Paramètres de vol réglables »).
**Alternatives écartées :** attendre les mesures au banc (écarté par DEC-252 « Phase conception détaillée ouverte avant les mesures au banc ») ; recopier le réglage d'un autre drone sans le dire (suppose des moteurs et une masse identiques).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; ne pas bloquer la conception sur des valeurs que seuls les essais peuvent fixer.
**Doutes levés :** (aucun) ; suivi par DOU-171 « Gains de référence, poussée de sustentation et linéarisation de la poussée » et DOU-170 « Constantes de capteurs de départ : échelle du flux, retard du capteur de hauteur, filtres »

### DEC-261 — Estimation : filtre de Mahony, observateur de hauteur et compensation du retard
**Date :** 2026-10-30
**Concerne :** DES-023 « Filtre d'attitude de Mahony », DES-024 « Observateur de hauteur et de vitesse verticale », ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse »
**Décision :** filtre de Mahony sans terme intégral (biais du gyroscope mesuré à l'initialisation, Kp = 2,0 s⁻¹, poids de l'accéléromètre linéaire entre 0,5 g et 1,5 g) ; observateur de hauteur à deux états avec gains L1 = 12 s⁻¹ et L2 = 36 s⁻² (pôles doubles à 6 rad/s), correction par l'innovation calculée à l'instant de la mesure grâce à l'historique de 64 cycles, retard de 33 ms (valeur de départ) ; rejet d'une mesure aberrante isolée. Une simulation de contrôle avant écriture donne 9 cm d'erreur maximale pendant une rampe de 1 m/s et 3 cm en régime.
**Alternatives écartées :** filtre de Kalman complet (réglage lourd) ; filtre complémentaire sans compensation du retard (erreur de 3 cm par m/s de vitesse verticale) ; filtre de Madgwick (même résultat, plus de calcul).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte »).
**Doutes levés :** (aucun) ; suivi par DOU-170 « Constantes de capteurs de départ : échelle du flux, retard du capteur de hauteur, filtres »

### DEC-262 — Vitesse horizontale invalide : stationnaire non déclaré
**Date :** 2026-10-30
**Concerne :** DES-025 « Vitesse horizontale et critères d'immobilité, de platitude et de stationnaire », REQ-007 « Critère de vol stationnaire », DOU-139 « Capteurs de hauteur et de flux : hauteur de montage et sols sans texture »
**Décision :** quand la vitesse horizontale est invalide (hauteur sous 8 cm, qualité faible, inclinaison supérieure à 30°, échantillon vieux de plus de 50 ms), le critère de stationnaire de REQ-007 « Critère de vol stationnaire » est faux : le drone ne se croit jamais stationnaire sans mesure de dérive, et la coupure de REQ-011 « Coupures automatiques en vol » à 2,0 s s'applique.
**Alternatives écartées :** déclarer le stationnaire avec la seule vitesse verticale (un drone qui dérive ou qui est porté s'en croirait stationnaire) ; geler la dernière vitesse connue.
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; le choix sûr, le plus simple.
**Doutes levés :** (aucun) ; conséquence sur sol sans texture suivie par DOU-139 « Capteurs de hauteur et de flux : hauteur de montage et sols sans texture »

### DEC-263 — Critère d'immobilité : fenêtre de 50 échantillons à 100 Hz
**Date :** 2026-10-30
**Concerne :** DES-025 « Vitesse horizontale et critères d'immobilité, de platitude et de stationnaire », REQ-003 « Conditions de départ du drone »
**Décision :** la condition « la norme de l'accélération ne s'écarte pas de plus de ±0,5 m/s² de sa moyenne pendant les 0,5 s précédentes » est calculée sur 50 échantillons de la norme pris à 100 Hz : chaque échantillon doit être à moins de 0,5 m/s² de la moyenne de la fenêtre (maximum et minimum comparés à la moyenne).
**Alternatives écartées :** fenêtre de 500 échantillons à 1 kHz (500 comparaisons par cycle) ; moyenne exponentielle (ne donne pas un maximum d'écart sur 0,5 s).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; 200 octets de mémoire et 50 comparaisons tous les 10 ms.
**Doutes levés :** (aucun)

### DEC-264 — Initialisation : centrale inertielle ou flux optique absent vaut échec d'initialisation
**Date :** 2026-10-30
**Concerne :** DES-031 « Séquence d'initialisation et échec d'initialisation », DES-020 « Pilote du flux optique », ARC-023 « Initialisation et échec d'initialisation », REQ-037 « Comportement en échec d'initialisation »
**Décision :** l'absence de réponse de la centrale inertielle, du flux optique (identité fausse) ou du capteur de hauteur à l'initialisation est un échec d'initialisation (moteurs jamais armés, état 2), comme le prévoit déjà ARC-023 « Initialisation et échec d'initialisation » pour le capteur de hauteur. Sans la centrale le drone ne peut ni voler ni juger l'immobilité ; sans le flux, la dérive est hors d'atteinte et le stationnaire ne serait jamais déclaré.
**Alternatives écartées :** continuer sans le flux (coupure à 2 s à chaque vol, sans message clair) ; échec seulement pour la centrale.
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; extension de ARC-023 « Initialisation et échec d'initialisation » et de REQ-017 « Initialisation en 3 secondes » au-delà de leurs deux causes (mouvement, pas à plat), signalée par DOU-168 « Centrale inertielle ou flux optique absent à l'initialisation ».
**Doutes levés :** (aucun) ; suivi par DOU-168 « Centrale inertielle ou flux optique absent à l'initialisation »

### DEC-265 — Protocole sans fil : octets, codes de cause, file d'émission et réception
**Date :** 2026-10-30
**Concerne :** DES-033 « Trames du statut sans fil, automate de réception et file d'émission », ARC-025 « Protocole et service du statut sans fil »
**Décision :** longueur de charge fixe par type, petit-boutiquier, CRC8 polynôme 0x07 initial 0 ; codes de cause numérotés comme dans DES-033 « Trames du statut sans fil, automate de réception et file d'émission » (refus 1 à 4, coupure 1 à 6) ; réception déclenchée par la ligne au repos de l'USART (priorité de l'arrêt) ; reprise des octets après un CRC faux ; file d'émission de 8 trames où le statut remplace le statut en attente ; vecteurs de test communs au C et au Python.
**Alternatives écartées :** champ de longueur dans la trame (inutile, longueurs fixes) ; sondage de l'USART à chaque cycle (retarde l'arrêt jusqu'à 1 ms sans gain) ; CRC16.
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte »).
**Doutes levés :** (aucun)

### DEC-266 — Réglages : origine en double dans le code et lecture protégée contre l'erreur ECC
**Date :** 2026-10-30
**Concerne :** DES-035 « Paramètres de vol, section d'origine et pilote de flash », DES-017 « Coupure des moteurs, démarrage unique et gestionnaires d'exception », ARC-027 « Paramètres de vol et stockage des réglages »
**Décision :** la section d'origine est initialisée par l'éditeur de liens à partir des mêmes macros que le code ; une page vierge, un mot hors bornes ou une erreur ECC donnent les valeurs d'origine des macros. L'erreur ECC double à la lecture (écriture interrompue par une coupure de la batterie) déclenche une interruption non masquable ; son gestionnaire lève un drapeau et ne coupe rien, et `param_load()` teste le drapeau. Pas de somme de contrôle (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »).
**Alternatives écartées :** deux copies avec indicateur de validité (contraire à DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » et inutile avec un mot unique) ; ignorer l'interruption non masquable (le drone redémarrerait en boucle après une écriture interrompue).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; réponse au risque inscrit dans « Architecture » (écriture de 64 bits interrompue).
**Doutes levés :** (aucun)

### DEC-267 — Ordonnancement : voyant dans l'interruption du tick, flux en deux pas, tâches de fond par priorité
**Date :** 2026-10-30
**Concerne :** DES-016 « Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond », DES-020 « Pilote du flux optique », DES-021 « Pilotes des moteurs, du voyant, du buzzer et de la liaison série », DOU-159 « Ordonnancement des tâches de fond : flux à 100 Hz, pilote de hauteur et latence de l'arrêt sans fil »
**Décision :** (1) la modulation du voyant (10 niveaux, 100 Hz) est faite dans l'interruption TIM6 (moins de 1 µs) car elle doit tourner à chaque milliseconde ; la séquence des effets, elle, est une tâche de fond tous les 10 ms. (2) la lecture du flux est découpée en deux pas (adresse puis 12 octets), chacun inférieur à 200 µs. (3) le drapeau de cycle est levé par la fin du DMA de l'IMU (et non par TIM6) pour que la lecture soit terminée avant le calcul. (4) priorités de tâches : arrêt radio, hauteur, flux, statut ou variables, effets ; charge d'environ 420 pas par seconde. L'alarme de 800 µs de DOU-159 « Ordonnancement des tâches de fond : flux à 100 Hz, pilote de hauteur et latence de l'arrêt sans fil » est conservée.
**Alternatives écartées :** voyant en tâche de fond (la modulation se déformerait avec les pas des autres tâches) ; timer matériel du voyant (conflits de broches de DEC-240 « Brochage, timers, voyant et bouton ») ; flux en un seul pas de 120 µs (reste dans le budget, mais près de la limite de 200 µs avec les attentes de la fiche).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte »).
**Doutes levés :** (aucun) ; DOU-159 « Ordonnancement des tâches de fond : flux à 100 Hz, pilote de hauteur et latence de l'arrêt sans fil » reste ouvert jusqu'à la mesure de TI-011 « Cadence du cycle et temps de réponse de l'arrêt d'urgence »

### DEC-268 — Mécanique : anneaux tangents, modèle OpenSCAD et impression en ligne
**Date :** 2026-10-30
**Concerne :** DES-006 « Cadre, anneaux, moteurs et hélices », ARC-006 « Moteurs, hélices et protège-hélices »
**Décision :** cadre fait de quatre anneaux tangents (diamètre extérieur égal à l'entraxe de 49 mm), sans bras ; modèle paramétrique OpenSCAD ; impression en résine par un service en ligne (sans imprimante personnelle supposée). Cotes verticales fixées par le croquis de DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie ».
**Alternatives écartées :** bras en croix entre les moteurs (plus de masse, encombrement identique) ; carte de circuit imprimé comme cadre (rigide mais lourd et cher) ; impression sur l'imprimante de l'utilisateur (non connue).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; la forme la plus simple qui tient dans 98 x 98 mm.
**Doutes levés :** (aucun) ; suivi par DOU-169 « Matière, masse, délai et cotes verticales des pièces imprimées »

### DEC-269 — Matériel : ferrite hors du chemin des moteurs, mesure en amont, rappels des sélections de bus
**Date :** 2026-10-30
**Concerne :** DES-008 « Batterie, connecteur XT30 et entrée de la carte », DES-009 « Régulateur de 3,0 V et pont de mesure de la tension », DES-003 « Raccordement de la centrale inertielle LSM6DSO », DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V », ARC-009 « Alimentation de la logique et mesure de la tension »
**Décision :** (1) la ferrite d'entrée (1 A nominal) n'est que dans la branche des régulateurs ; les moteurs, le voyant, le buzzer et le pont de mesure sont sur la branche directe du connecteur. (2) Le pont de mesure lit la batterie en amont de la ferrite (la chute de 13 mV de la ferrite ne fausse pas la mesure). (3) Les lignes de sélection de puce (CS) de la centrale et du flux sont rappelées au +3V0 par 10 kohms, pour qu'aucun composant ne soit sélectionné pendant le reset.
**Alternatives écartées :** ferrite sur l'entrée complète (brûlerait à 9,5 A) ; mesure après la ferrite (erreur de la chute, variable avec la consommation).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; précision apportée à ARC-009 « Alimentation de la logique et mesure de la tension » qui disait « entrée filtrée » sans préciser la branche.
**Doutes levés :** (aucun)

### DEC-270 — Vérifications par scripts : appels uniques, mémoire et jalons
**Date :** 2026-10-30
**Concerne :** DES-015 « Arborescence du firmware, édition de liens et budget de mémoire », DES-017 « Coupure des moteurs, démarrage unique et gestionnaires d'exception », DES-030 « Chien de garde matériel et règle de rafraîchissement », DES-037 « Jalons de livraison et configurations de compilation », DES-038 « Contenu de la page de consignes d'emploi »
**Décision :** les propriétés de structure que le compilateur ne contrôle pas sont vérifiées par de courts scripts Python sous `firmware/tools/` : nombre de sites d'appel de `motors_start()` (REQ-005 « Démarrage des moteurs sur geste volontaire seulement »), unicité de l'écriture de la clé du chien de garde, plan mémoire du fichier `.map`, longueur et mots-clés de la page de consignes.
**Alternatives écartées :** revue manuelle seule (une régression passerait inaperçue) ; analyse statique complète (outil lourd).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte »).
**Doutes levés :** (aucun)

### DEC-271 — Cycle indépendant du DMA de la centrale et lecture armée après l'initialisation
**Date :** 2026-10-30
**Concerne :** DES-016 « Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond », DES-018 « Pilote de la centrale inertielle », DES-029 « Surveillance et coupures automatiques »
**Décision :** l'interruption TIM6 lève le drapeau de cycle même si la lecture précédente de la centrale n'est pas finie (erreur comptée, trois erreurs : `imu_failed`), pour que la surveillance et le chien de garde ne dépendent pas du DMA ; la lecture automatique n'est armée qu'après l'initialisation de la centrale ; 10 lectures brutes identiques valent une erreur par cycle suivant (blocage détecté après au moins 12 cycles).
**Alternatives écartées :** cycle déclenché seulement par le DMA (une centrale muette supprime la surveillance et provoque un reset sans cause) ; délai de garde par un comparateur de TIM2.
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; point relevé par la relecture critique de la phase.
**Doutes levés :** (aucun)

### DEC-272 — Coupure d'atterrissage tolérante à la fenêtre de validité du capteur de hauteur
**Date :** 2026-10-30
**Concerne :** DES-019 « Pilote du capteur de hauteur non bloquant », DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique », ARC-018 « Boucle de contrôle du vol », DOU-160 « Mesure de hauteur valide et sols sombres ou brillants »
**Décision :** une lecture brute (valide ou non) d'au plus 45 mm, en état Atterrissage seulement,, ou un état hors portée dont la dernière valeur valide était d'au plus 60 mm, vaut contact et coupe les moteurs, car la fenêtre de validité (40 à 45 mm) est franchie en moins de 33 ms à 0,5 m/s.
**Alternatives écartées :** abaisser la borne de validité à 20 mm (mesure non fiable sous 40 mm) ; attendre la coupure par absence de mesure à 200 ms (mauvaise cause, moteurs en marche au sol).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte »).
**Doutes levés :** (aucun)

### DEC-273 — Flux optique : l'absence de mouvement est une vitesse nulle valide
**Date :** 2026-10-30
**Concerne :** DES-020 « Pilote du flux optique », DES-025 « Vitesse horizontale et critères d'immobilité, de platitude et de stationnaire », DEC-262 « Vitesse horizontale invalide : stationnaire non déclaré »
**Décision :** la validité d'une mesure de flux ne dépend que de la qualité de surface (SQUAL) ; un bit de mouvement absent donne des deltas nuls, donc une vitesse nulle valide ; l'âge de l'échantillon se compte depuis la dernière lecture réussie.
**Alternatives écartées :** exiger un mouvement détecté (un drone immobile serait coupé à 2 s).
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; précise DEC-262 « Vitesse horizontale invalide : stationnaire non déclaré ».
**Doutes levés :** (aucun)

### DEC-274 — Échec par sous-tension : horloge conservée à 170 MHz
**Date :** 2026-10-30
**Concerne :** DES-031 « Séquence d'initialisation et échec d'initialisation », ARC-023 « Initialisation et échec d'initialisation », DOU-118 « Seuil de protection et consommation résiduelle du drone laissé allumé »
**Décision :** en échec d'initialisation par sous-tension, le drone garde l'horloge à 170 MHz (capteurs en veille, voyant au niveau 1 sur 10) au lieu des 16 MHz de ARC-023 « Initialisation et échec d'initialisation » : tous les chronomètres, le débit série et les bus sont calés sur 170 MHz et une seconde table de constantes serait un risque de plus. La consommation résiduelle est donc supérieure aux 12 mA estimés.
**Alternatives écartées :** seconde table de constantes à 16 MHz (complexité, tests supplémentaires) ; supprimer le voyant.
**Raison :** délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte »).
**Doutes levés :** (aucun) ; écart signalé par DOU-178 « Horloge à 16 MHz de l'échec par sous-tension abandonnée »

### DEC-275 — Schémas SVG des circuits de la carte dans la conception détaillée
**Date :** 2026-10-30
**Concerne :** DES-001 « Schéma par blocs, réseaux et domaines de tension de la carte », DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option », DES-003 « Raccordement de la centrale inertielle LSM6DSO », DES-004 « Raccordement du capteur de hauteur VL53L1X », DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V », DES-007 « Circuit de puissance des moteurs », DES-008 « Batterie, connecteur XT30 et entrée de la carte », DES-009 « Régulateur de 3,0 V et pont de mesure de la tension », DES-010 « Circuit du bouton », DES-011 « Circuit du voyant RGB et du buzzer », DES-012 « Raccordement du module Bluetooth E104-BT02 »
**Décision :** instruction de l'utilisateur en chat, 2026-10-30 : ajouter dans la conception détaillée des schémas SVG, comme des morceaux de schéma électronique, pour tout ce qui concerne la carte. Périmètre : la carte seulement, sans la mécanique (DES-006 « Cadre, anneaux, moteurs et hélices ») ni le logiciel pour le moment. Un SVG par bloc de circuit, dans `projets/boomrone/schemas/`, inséré dans le DES concerné avec une légende ; DES-013 « Implantation, routage et fichiers de fabrication pour JLCPCB » n'a pas de schéma (le texte ne fixe aucune position de composant, ce qui est l'objet du croquis de DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie »). Les schémas SVG sont des illustrations de conception, rédigées à partir du texte des DES : ce ne sont pas les schémas KiCad de fabrication, qui restent à saisir (« Réalisé par » de chaque DES) et qui font foi pour la commande de la carte. Le texte technique des DES n'est pas modifié ; les éléments que le texte ne donne pas (repères, noms de broches) sont marqués provisoires ou à vérifier dans les SVG et suivis par DOU-182 « Noms et numéros de broches des circuits intégrés des schémas SVG non relevés dans les fiches », DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée » et DOU-184 « Condensateurs d'entrée du régulateur de 3,0 V : 22 µF sur VBATL et 1 µF sur l'entrée du composant ».
**Alternatives écartées :** diagrammes Mermaid (pas de symboles de composants ni de broches, illisibles pour un circuit) ; schémas KiCad saisis dès maintenant (travail de saisie lourd avant que les fiches de composants soient relevées, DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage » ; reste prévu plus tard, les SVG serviront de brouillon) ; schémas pour la mécanique et le logiciel (hors du périmètre demandé pour le moment).
**Raison :** une image de circuit se relit et se critique plus vite qu'une phrase de valeurs de composants, et fait apparaître les oublis de brochage avant la saisie KiCad ; la règle « Mermaid par défaut, SVG quand Mermaid ne suffit pas » de `framework/regles-documentaires.md` autorise le SVG pour un schéma de carte. Les SVG sont du XML sans dépendance externe, avec un fond blanc ou sombre selon le thème (le rendu ne dépend pas du thème de l'éditeur) et des traits en couleurs sûres. Ils restent « Proposé » comme les DES qu'ils illustrent.
**Doutes levés :** (aucun) ; doutes ouverts : DOU-182 « Noms et numéros de broches des circuits intégrés des schémas SVG non relevés dans les fiches », DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée », DOU-184 « Condensateurs d'entrée du régulateur de 3,0 V : 22 µF sur VBATL et 1 µF sur l'entrée du composant »

### DEC-276 — Porte conception détaillée franchie : accord explicite de l'utilisateur
**Date :** 2026-10-30
**Concerne :** « Conception détaillée » — `projets/boomrone/04-conception-detaillee.md` (38 DES, 11 schémas SVG) et section TU de « Plans de test » — `projets/boomrone/05-plans-de-test.md` (38 TU)
**Décision :** la porte « conception détaillée » est franchie ; les 38 DES passent à « Validé » (les TU restent « Écrit », comme les TI, TS et TA après leur porte) ; la phase « implémentation » peut s'ouvrir. État au franchissement : tag `gate-5-conception-ready-v0`, aucun doute bloquant ouvert, doutes non bloquants listés dans `registre-doutes.md`, relectures de porte faites par `critique`, `coherence-clarte` et `exigences-tracabilite` (DEC-271 « Cycle indépendant du DMA de la centrale et lecture armée après l'initialisation » à DEC-274 « Échec par sous-tension : horloge conservée à 170 MHz »), la seconde relecture de `critique` n'ayant été corrigée que partiellement.
**Alternatives écartées :** trancher les sept points de la porte un par un avant le franchissement ; continuer la phase.
**Raison :** accord explicite de l'utilisateur en chat, 2026-10-30 : « franchire la porte ». Les sept points présentés par l'architecte sont acceptés tels que rédigés dans les DES : DEC-264 « Initialisation : centrale inertielle ou flux optique absent vaut échec d'initialisation » (absence de la centrale ou du flux optique = échec d'initialisation, extension de REQ-017 « Initialisation en 3 secondes » et ARC-023 « Initialisation et échec d'initialisation »), DEC-262 « Vitesse horizontale invalide : stationnaire non déclaré » et DEC-273 « Flux optique : l'absence de mouvement est une vitesse nulle valide » (critère de stationnaire faux si la vitesse horizontale est invalide), DEC-258 « Mesure de la tension : séquence de conversion et zone de maintien de la sous-tension » (compteur de sous-tension cumulatif), DEC-274 « Échec par sous-tension : horloge conservée à 170 MHz » (horloge à 170 MHz en échec par sous-tension, écart avec ARC-023 « Initialisation et échec d'initialisation »), DEC-272 « Coupure d'atterrissage tolérante à la fenêtre de validité du capteur de hauteur » (contact en atterrissage), DES-038 « Contenu de la page de consignes d'emploi » (points 5 et 6 de la page de consignes proposés), gains de départ non mesurés conservés (DEC-253 « Seuils de batterie conservés, sans mesures au banc pour la première version »). Rappels : ARC-023 « Initialisation et échec d'initialisation » et REQ-017 « Initialisation en 3 secondes » ne sont pas modifiés, l'écart est porté par les DES ; réserves restantes : valeurs « de mémoire » à relever dans les fiches (DOU-172 « Valeurs de configuration des périphériques à vérifier dans le manuel de référence », DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage », DOU-181 « Bilan d'erreur de la mesure de tension et niveau du BOR »), broche PA11 du moteur 4 à vérifier avant le routage, tension sous charge marginale (DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie »), TU-019 « Pilote du capteur de hauteur : pas, reprise par niveaux et publication », TU-026 « Contrôle : signes du mixeur, saturation, conversion en rapport cyclique » et TU-029 « Surveillance : sous-tension, armement et coupures en vol » à compléter, calcul d'inclinaison du TU-023 « Filtre d'attitude : stabilité, intégration sans accéléromètre, convergence » à refaire, constantes absentes de `check_fixed.py` ; `check_traceability_V2.py --gate --phase conception` donne OK, l'original échoue pour les 12 « SCN sans BES » (DEC-156 « Couverture des scénarios vérifiée à la main, outil de traçabilité inchangé »).
**Doutes levés :** (aucun)

<!-- Ajouter les décisions ci-dessous, au même format, en dehors des blocs de code. -->
