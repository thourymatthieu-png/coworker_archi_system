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
**Raison :** choix de l'utilisateur ; redondance des canaux. Les motifs précis (couleurs, sons, messages) restent à définir en architecture.
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
**Raison :** choix de l'utilisateur ; évite le cas de la batterie faible en vol, puisque le vol dure environ 15 secondes (depuis : jusqu'à environ 27 secondes, voir DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »). Reste à définir : le seuil, et la marge qui garantit un vol complet (voir DOU-005 « Que se passe-t-il si le drone n'y arrive pas ? »).
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
**Raison :** choix de l'utilisateur ; simplicité. Risque résiduel accepté : un relâchement du bouton sans lancer démarre les moteurs, drone en main ou posé.
**Doutes levés :** DOU-006 « Comment éviter un départ des moteurs sans vrai lancer ? »

### DEC-007 — Bouton relâché avant 2 secondes : retour en attente
**Date :** 2026-10-27
**Concerne :** SCN-004 « Dégradé : bouton relâché avant 2 secondes »
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
**Raison :** choix de l'utilisateur ; critère mesurable par le drone lui-même.
**Doutes levés :** DOU-003 « Quel délai pour atteindre le stationnaire ? » — mais ouvre DOU-009 « Quelle tolérance d'altitude pendant les 10 secondes de stationnaire ? »

### DEC-010 — Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone doit se stabiliser quand il est lancé (a) dans n'importe quelle orientation, y compris à l'envers ; (b) à une vitesse de lancer de 0,5 à 4 m/s, vers le haut et vers l'avant ; (c) depuis une hauteur d'au moins 1,5 m du sol. Valeurs provisoires, à confirmer par essais.
**Alternatives écartées :** inclinaison initiale limitée à 90° ; plage de vitesse 1 à 3 m/s ou 0,5 à 6 m/s ; hauteur minimale de 1 m ou aucune.
**Raison :** choix de l'utilisateur ; cohérent avec DEC-003 « Drone retourné ou très incliné : normal tant que la stabilisation n'est pas finie » et avec le délai de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs ».
**Doutes levés :** DOU-004 « Quelle plage de lancer et quelle orientation initiale ? » — mais ouvre DOU-010 « Quelle rotation au lancer le drone doit-il rattraper ? »

### DEC-011 — Dérive de 30 cm sur 10 s en objectif à valider par essais
**Date :** 2026-10-27
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Décision :** Le drone mesure son mouvement avec une centrale inertielle seule, sans capteur de position (pas de flux optique). La dérive horizontale maximale de 30 cm sur les 10 secondes de stationnaire est un **objectif**, à valider par essais, et non une exigence garantie.
**Alternatives écartées :** capteur de flux optique avec dérive de 30 cm garantie (recommandé par l'architecte : seul moyen fiable de tenir 30 cm) ; centrale inertielle seule sans objectif de dérive.
**Raison :** choix de l'utilisateur, après avertissement de l'architecte : sans capteur de position, la vitesse horizontale se calcule par intégration et dérive (un défaut d'inclinaison de 0,5° produit plusieurs mètres de dérive en 10 s), donc l'objectif de 30 cm risque de ne pas être tenu. Risque accepté : l'échec pourrait n'apparaître qu'après la fabrication de la carte chez JLCPCB.
**Doutes levés :** DOU-002 « Que veut dire ne pas dériver horizontalement ? » — mais ouvre DOU-011 « Quelle dérive horizontale reste acceptable si 30 cm n'est pas tenu ? »

### DEC-012 — Couper les moteurs si le drone bascule après le stationnaire
**Date :** 2026-10-27
**Concerne :** SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Décision :** Une fois le stationnaire atteint, si le drone s'incline au-delà d'un angle limite (valeur provisoire : 60°, à confirmer par essais) ou se retourne, il coupe ses moteurs et le signale avec un signal distinct. Cela vaut pendant le stationnaire et la descente. Complète DEC-003 « Drone retourné ou très incliné : normal tant que la stabilisation n'est pas finie ».
**Alternatives écartées :** essayer de se redresser (complexité du comportement de redressement).
**Raison :** choix de l'utilisateur ; un drone déjà stabilisé qui bascule est hors de contrôle.
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
**Raison :** choix de l'utilisateur, après avertissement de l'architecte. Risque accepté : hélices en rotation si le bouton est relâché en main ou drone posé ; limité seulement par les protège-hélices de DEC-016 « Public adulte, protège-hélices obligatoires ». À réexaminer si les essais montrent des démarrages involontaires. Pas de scénario dédié (décision du 2026-10-27) : le cas est couvert par le vol normal, puis par SCN-002 « Échec : stationnaire non atteint dans le délai » si le drone n'est pas lancé.
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
**Raison :** choix de l'utilisateur ; meilleure précision de hauteur (de l'ordre du centimètre). Risques acceptés : portée limitée, mesure fausse tant que le drone n'est pas redressé après un lancer dans toute orientation, sensibilité à la lumière et aux sols non réfléchissants.
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
**Raison :** outil disponible chez l'utilisateur ; contrainte exprimée par lui.
**Doutes levés :** DOU-014 « Quel scénario de mise en service faut-il écrire ? » — mais ouvre DOU-031 « Quelles opérations suivent la programmation à la mise en service ? »

### DEC-025 — Suivi et réglage du drone par le sans fil, y compris en vol
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage : réglage du vol par le sans fil »
**Décision :** Le drone est paramétrable sans fil, y compris en vol, pour régler le vol. Il retourne à un appareil de suivi les variables du vol : commandes des moteurs, hauteur, autres données de position. Un mode réglage, accessible par trois appuis sur le bouton (confirmé par DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie »), permet au drone de décoller et de se poser plusieurs fois de suite sur un temps bref pour régler les paramètres.
**Alternatives écartées :** aucune étudiée.
**Raison :** l'asservissement du vol doit être réglé par essais ; l'utilisateur veut voir les variables et agir sur les paramètres pendant les vols.
**Doutes levés :** DOU-008 « L'utilisateur veut-il suivre le vol depuis un autre appareil ? » et DOU-026 « L'utilisateur veut-il régler le drone depuis un autre appareil ? » — mais ouvre DOU-032 « Comment entre-t-on dans le mode réglage et comment en sort-on ? », DOU-033 « Que fait le drone pendant les vols de réglage répétés ? » et DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? »

### DEC-026 — Mise en service : calibrage éventuel renvoyé à l'architecture, réglage du vol par un scénario dédié
**Date :** 2026-10-27
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Décision :** On ne sait pas encore si un calibrage est nécessaire : cela dépend des solutions techniques, donc de l'architecture. Aucune opération de calibrage n'est écrite dans les scénarios. Le réglage du vol fait l'objet du scénario SCN-009 « Réglage : réglage du vol par le sans fil ».
**Alternatives écartées :** décrire un calibrage dès les scénarios (recommandé par l'architecte, écarté : dépend de solutions non choisies).
**Raison :** choix de l'utilisateur ; les scénarios ne décrivent pas de solutions techniques.
**Doutes levés :** DOU-031 « Quelles opérations suivent la programmation à la mise en service ? »

### DEC-027 — Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage : réglage du vol par le sans fil »
**Décision :** Le mode réglage s'active par trois appuis sur le bouton, drone posé et non armé ; le drone signale l'entrée dans le mode. On n'en sort que par coupure de la batterie : après un redémarrage, le drone est en mode normal. Précise DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol ».
**Alternatives écartées :** commande sans fil seulement ; trois appuis ou commande sans fil ; sortie par appui sur le bouton, commande sans fil ou fin d'un délai.
**Raison :** choix de l'utilisateur ; simplicité. Risque accepté : on peut oublier d'être en mode réglage, et un appui parasite peut l'activer au sol.
**Doutes levés :** DOU-032 « Comment entre-t-on dans le mode réglage et comment en sort-on ? »

### DEC-028 — Mode réglage : décollage depuis le sol sur commande sans fil
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage : réglage du vol par le sans fil »
**Décision :** En mode réglage, le drone décolle depuis le sol, à chaque fois sur commande de l'utilisateur envoyée par le sans fil. Il ne décolle jamais seul, et aucun nombre de cycles n'est imposé. Exception au lancer à la main de DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs », limitée au mode réglage de DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie ».
**Alternatives écartées :** décollage automatique en boucle sur un nombre de cycles fixé (écarté : hélices qui tournent sans geste de l'utilisateur).
**Raison :** choix de l'utilisateur, sur recommandation de l'architecte ; l'utilisateur garde la main sur chaque décollage.
**Doutes levés :** aucun en entier : DOU-033 « Que fait le drone pendant les vols de réglage répétés ? » reste ouvert (durée et hauteur du vol, lien perdu, bouton en vol de réglage). Depuis : levé par DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu ».

### DEC-029 — Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu
**Date :** 2026-10-27
**Concerne :** SCN-009 « Réglage : réglage du vol par le sans fil »
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

<!-- Ajouter les décisions ci-dessous, au même format, en dehors des blocs de code. -->
