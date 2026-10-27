# Glossaire

> **Aperçu** : définitions uniques des termes du projet. Un terme = un sens. Ne pas créer de synonymes.

| Terme | Définition | Document de première apparition |
|---|---|---|
| Armé / armement / désarmement | État où le drone est prêt à voler : le bouton a été appuyé 2 secondes et la batterie est suffisante. L'armement est le passage à cet état, le désarmement le retour à « allumé, en attente d'un appui ». | `00-scenarios.md` |
| Allumé, en attente d'un appui | État du drone après la mise sous tension réussie, avant tout appui sur le bouton (anciennement « initialisé »). | `00-scenarios.md` |
| Verrouillé | État du drone après un posé ou une coupure des moteurs : il ne reprend jamais le vol seul ; un nouvel appui de 2 secondes est nécessaire (identique à l'état « Allumé, en attente d'un appui » : DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »). | `journal-decisions.md` |
| Prêt | Signal donné quand le drone est armé et peut être lancé. | `00-scenarios.md` |
| Lancé | Le bouton est relâché après l'armement ; les moteurs démarrent peu après. | `00-scenarios.md` |
| Stabilisation | Phase qui suit le lancer, où le drone cherche à se redresser ; être retourné ou très incliné y est normal. | `00-scenarios.md` |
| Vol stationnaire (stationnaire) | Le drone est immobile en l'air et à plat ; critère chiffré dans DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs ». | `00-scenarios.md` |
| Atterrissage | Descente lente après les 10 secondes de stationnaire. | `00-scenarios.md` |
| Posé | Le drone est à moins de 2 à 3 cm du sol ; les moteurs sont coupés. Si le délai de descente est dépassé, le drone n'est pas déclaré posé : il donne le signal « Délai de descente dépassé » (DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé »). | `00-scenarios.md` |
| En vol | Du lancer au posé ou à la coupure des moteurs : stabilisation, stationnaire, atterrissage. | `00-scenarios.md` |
| Moteurs coupés | Les moteurs sont arrêtés ; le drone tombe s'il est en l'air. | `00-scenarios.md` |
| Basculement | Le drone s'incline fortement ou se retourne après le stationnaire (SCN-006 « Échec : inclinaison excessive après le stationnaire »). | `00-scenarios.md` |
| Arrêt d'urgence | Coupure immédiate des moteurs en vol, par l'un de deux moyens : un appui sur le bouton (signal « Arrêt par le bouton ») ou une commande d'arrêt sans fil (signal « Arrêt sans fil »), voir DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ». | `00-scenarios.md` |
| Échec d'initialisation | Le drone n'est pas en état de voler au démarrage ; il refuse de s'armer et donne un signal distinct. | `00-scenarios.md` |
| Signal | Information donnée à l'utilisateur ; la forme (lumière, son, suivi) est à définir. Dix-sept signaux sont listés dans `00-scenarios.md`. | `00-scenarios.md` |
| Appareil de suivi | Téléphone ou ordinateur relié sans fil au drone, qui affiche les variables du vol et permet de le régler. Synonymes écartés : « un autre appareil » (utilisé dans des titres de décisions). | `00-scenarios.md` |
| Lien sans fil | Liaison entre le drone et l'appareil de suivi. | `00-scenarios.md` |
| Lien perdu | Le drone ne reçoit plus l'appareil de suivi ; délai à définir (DOU-036 « Après quel délai le lien sans fil est-il considéré comme perdu ? »). | `00-scenarios.md` |
| Mode réglage | Mode atteint par trois appuis sur le bouton, drone au sol, où l'on règle le vol par le sans fil ; on en sort par coupure de la batterie. | `00-scenarios.md` |
| Vol de réglage | Vol court déclenché par commande sans fil en mode réglage : décollage du sol, 3 secondes de stationnaire, pose. | `00-scenarios.md` |
| Variables du vol | Données renvoyées à l'appareil de suivi : commandes des moteurs, hauteur, données de position. | `00-scenarios.md` |
| Protège-hélices | Protection des hélices, obligatoire (DEC-016 « Public adulte, protège-hélices obligatoires »). | `journal-decisions.md` |
| Mise en service | Premier montage du drone : programmation, puis réglage du vol. | `00-scenarios.md` |
| Appairage | Association persistante d'un appareil de suivi à un drone. Non retenu : le drone obéit à tout appareil de suivi à portée (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »). | `journal-decisions.md` |
| Vol normal / vol libre | Vol lancé à la main, hors mode réglage. Vol libre : le drone vole sans appareil de suivi (DEC-032 « Vol libre : le drone vole sans appareil de suivi »). | `journal-decisions.md` |
| Mémoire non volatile | Mémoire du drone qui conserve les réglages sauvegardés après la coupure de la batterie ; le drone les charge au démarrage (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage »). | `journal-decisions.md` |
| Centrale inertielle | Capteur de mouvement du drone (accélérations et rotations), seul capteur de mouvement horizontal (DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais »). | `journal-decisions.md` |
| ToF | Capteur de distance orienté vers le bas, qui donne la hauteur au-dessus du sol et la vitesse verticale (DEC-019 « Hauteur au-dessus du sol mesurée en vol »). | `journal-decisions.md` |
| ST-LINK | Programmateur imposé par l'utilisateur pour programmer les microcontrôleurs du drone (DEC-024 « Mise en service par programmation avec un programmateur ST-LINK »). | `journal-decisions.md` |
| JTAG / SWD | Liaisons de programmation et de débogage utilisées avec le ST-LINK (DEC-024 « Mise en service par programmation avec un programmateur ST-LINK »). | `journal-decisions.md` |
