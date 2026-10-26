# Journal des décisions — Boomrone

> **Aperçu** : décisions prises par l'utilisateur, avec alternatives et raison. Les agents recommandent, **l'utilisateur décide**.

### DEC-001 — Critère de rétablissement : vitesse et inclinaison
**Date :** 2026-10-26
**Concerne :** BES-002 « Se rétablir rapidement en vol stationnaire »
**Décision :** Le drone est « rétabli » quand sa vitesse (horizontale et verticale) et son inclinaison sont sous des seuils, tenus pendant une courte durée. Valeurs provisoires proposées : vitesse < 0,3 m/s, inclinaison < 10°, tenue 0,5 s. À confirmer par essais.
**Alternatives écartées :** position horizontale fixe (exigerait un capteur de position, ex. flux optique).
**Raison :** critère mesurable avec une centrale inertielle et un capteur de hauteur, sans capteur de position.
**Doutes levés :** DOU-001 « Que veut dire se rétablir en vol stationnaire ? »

### DEC-002 — La rapidité de rétablissement sert de score de jeu
**Date :** 2026-10-26
**Concerne :** BES-002 « Se rétablir rapidement en vol stationnaire »
**Décision :** Le temps entre le lancer et le rétablissement est le score du jeu. Il n'y a pas de seuil de réussite.
**Alternatives écartées :** temps maximal fixé dès maintenant ; objectif chiffré après essais.
**Raison :** choix de l'utilisateur.
**Doutes levés :** DOU-002 « Que veut dire au plus vite ? »

### DEC-003 — Stationnaire à l'altitude atteinte
**Date :** 2026-10-26
**Concerne :** BES-003 « Tenir le vol stationnaire 10 secondes »
**Décision :** Le drone tient l'altitude qu'il a au moment du rétablissement. Aucune altitude cible n'est réglée.
**Alternatives écartées :** altitude cible réglable sans fil.
**Raison :** plus simple, cohérent avec un jeu où l'altitude dépend du lancer.
**Doutes levés :** DOU-003 « À quelle altitude et sur quoi se stabilise-t-on ? »

### DEC-004 — Atterrissage doux : vitesse maximale au contact
**Date :** 2026-10-26
**Concerne :** BES-004 « Se poser doucement »
**Décision :** Descente contrôlée avec une vitesse verticale au contact sous un seuil (valeur proposée : < 0,5 m/s, à confirmer par essais). Moteurs coupés après le contact. Sol plat, atterrissage possible n'importe où.
**Alternatives écartées :** retour au point de lancer.
**Raison :** choix de l'utilisateur ; pas de capteur de position nécessaire.
**Doutes levés :** DOU-004 « Qu'est-ce qu'un atterrissage doux ? »

### DEC-005 — Armement par bouton-poussoir maintenu, lancer détecté au relâchement
**Date :** 2026-10-26
**Concerne :** BES-001 « Lancer à la main »
**Décision :** Un bouton-poussoir est maintenu appuyé pour armer le drone. Quand l'utilisateur le lance, le bouton passe de « appuyé » à « relâché ». Les moteurs démarrent 200 ms après ce relâchement.
**Alternatives écartées :** détection du lancer par accélération puis chute libre ; moteurs déjà en rotation dans la main.
**Raison :** choix de l'utilisateur ; sécurité (moteurs arrêtés tant que le bouton est appuyé).
**Doutes levés :** DOU-005 « Comment le drone sait-il qu'il est lancé, et quand les moteurs démarrent-ils ? » — mais ouvre DOU-012 « Que se passe-t-il si le bouton est relâché sans vrai lancer ? » et DOU-013 « Le délai de 200 ms est-il compatible avec le rétablissement ? »

### DEC-006 — Public : adultes seulement
**Date :** 2026-10-26
**Concerne :** BES-001 « Lancer à la main »
**Décision :** Le drone est destiné à des adultes avertis. La coupure des moteurs en cas d'anomalie est obligatoire. Les protections d'hélices sont optionnelles. Pas de norme jouet visée.
**Alternatives écartées :** public large avec protections obligatoires ; conformité à une norme jouet.
**Raison :** choix de l'utilisateur.
**Doutes levés :** DOU-006 « Quelle exigence de sécurité pour les personnes ? »

### DEC-007 — En cas d'échec, couper les moteurs
**Date :** 2026-10-26
**Concerne :** BES-002 « Se rétablir rapidement en vol stationnaire »
**Décision :** Principe général : toujours couper les moteurs en cas d'échec. Les scénarios d'échec sont à détailler avec l'utilisateur avant de lever le doute.
**Alternatives écartées :** atterrissage forcé selon le cas.
**Raison :** choix de l'utilisateur ; simplicité de sécurité.
**Doutes levés :** (aucun, DOU-007 « Que fait le drone si ça se passe mal ? » reste ouvert pour détailler les scénarios)

### DEC-008 — Réglage et visualisation sans fil, y compris en vol, temps réel
**Date :** 2026-10-26
**Concerne :** BES-005 « Régler le drone sans fil »
**Décision :** Les paramètres de réglage (par exemple les gains PID) se modifient sans fil depuis un ordinateur et/ou un téléphone, avec visualisation des variables en temps réel, y compris pendant le vol.
**Alternatives écartées :** réglage au sol seulement ; télémétrie lue après le vol.
**Raison :** choix de l'utilisateur ; réglage efficace de la régulation.
**Doutes levés :** DOU-008 « Que doit-on régler et lire sans fil, et avec quoi ? » — mais ouvre DOU-014 « Quels paramètres, quelle portée et quelle cadence de visualisation ? »

### DEC-009 — Quadricoptère de moins de 100 g
**Date :** 2026-10-26
**Concerne :** BES-009 « Utiliser moteurs, batterie et hélices du commerce »
**Décision :** Le drone est un quadricoptère de masse inférieure à 100 g.
**Alternatives écartées :** 100 à 250 g.
**Raison :** assez léger pour un lancer à la main.
**Doutes levés :** DOU-009 « Quelle taille, masse et forme de drone ? »

### DEC-010 — ST-LINK disponible, microcontrôleur libre
**Date :** 2026-10-26
**Concerne :** BES-007 « Programmer le drone par câble avec l'outillage STMicroelectronics »
**Décision :** L'utilisateur possède un ST-LINK ; la programmation se fait par SWD. Le choix du STM32 est laissé à l'architecture, selon le besoin et le stock JLCPCB.
**Alternatives écartées :** microcontrôleur imposé.
**Raison :** choix de l'utilisateur.
**Doutes levés :** DOU-010 « Quelle famille de STM32, et quels outils de programmation exactement ? »

### DEC-011 — Prototypes, quelques exemplaires
**Date :** 2026-10-26
**Concerne :** BES-010 « Fabriquer avec JLCPCB en composants en stock »
**Décision :** Production visée : prototypes en quelques exemplaires. Budget et délai non précisés.
**Alternatives écartées :** petite série.
**Raison :** choix de l'utilisateur.
**Doutes levés :** DOU-011 « Quel budget, quelle quantité, quel délai ? » — mais ouvre DOU-015 « Quel budget et quelle échéance ? »
