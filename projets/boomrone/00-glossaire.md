# Glossaire

> **Aperçu** : définitions uniques des termes du projet. Un terme = un sens. Ne pas créer de synonymes.

| Terme | Définition | Document de première apparition |
|---|---|---|
| Armé / armement / désarmement | État où le drone est prêt à voler : le bouton a été appuyé 2 secondes et la batterie est suffisante. L'armement est le passage à cet état, le désarmement le retour à « allumé, en attente d'un appui ». | `00-scenarios.md` |
| Allumé, en attente d'un appui | État du drone après la mise sous tension réussie, avant tout appui sur le bouton (anciennement « initialisé »). | `00-scenarios.md` |
| Verrouillé | État du drone après un posé ou une coupure des moteurs : il ne reprend jamais le vol seul ; un nouvel appui de 2 secondes est nécessaire (voir DOU-051 « L'état verrouillé est-il le même que l'état allumé, en attente d'un appui ? »). | `journal-decisions.md` |
| Prêt | Signal donné quand le drone est armé et peut être lancé. | `00-scenarios.md` |
| Lancé | Le bouton est relâché après l'armement ; les moteurs démarrent peu après. | `00-scenarios.md` |
| Stabilisation | Phase qui suit le lancer, où le drone cherche à se redresser ; être retourné ou très incliné y est normal. | `00-scenarios.md` |
| Vol stationnaire (stationnaire) | Le drone est immobile en l'air et à plat ; critère chiffré dans DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs ». | `00-scenarios.md` |
| Atterrissage | Descente lente après les 10 secondes de stationnaire. | `00-scenarios.md` |
| Posé | Le drone est à moins de 2 à 3 cm du sol ; les moteurs sont coupés. | `00-scenarios.md` |
| En vol | Du lancer au posé ou à la coupure des moteurs : stabilisation, stationnaire, atterrissage. | `00-scenarios.md` |
| Moteurs coupés | Les moteurs sont arrêtés ; le drone tombe s'il est en l'air. | `00-scenarios.md` |
| Basculement | Le drone s'incline fortement ou se retourne après le stationnaire (SCN-006 « Échec : inclinaison excessive après le stationnaire »). | `00-scenarios.md` |
| Arrêt d'urgence | Coupure immédiate des moteurs par un appui sur le bouton en vol (signal « Arrêt par le bouton »). | `00-scenarios.md` |
| Échec d'initialisation | Le drone n'est pas en état de voler au démarrage ; il refuse de s'armer et donne un signal distinct. | `00-scenarios.md` |
| Signal | Information donnée à l'utilisateur ; la forme (lumière, son, suivi) est à définir. Quinze signaux sont listés dans `00-scenarios.md`. | `00-scenarios.md` |
| Appareil de suivi | Téléphone ou ordinateur relié sans fil au drone, qui affiche les variables du vol et permet de le régler. Synonymes écartés : « un autre appareil » (utilisé dans des titres de décisions). | `00-scenarios.md` |
| Lien sans fil | Liaison entre le drone et l'appareil de suivi. | `00-scenarios.md` |
| Lien perdu | Le drone ne reçoit plus l'appareil de suivi ; délai à définir (DOU-036 « Après quel délai le lien sans fil est-il considéré comme perdu ? »). | `00-scenarios.md` |
| Mode réglage | Mode atteint par trois appuis sur le bouton, drone au sol, où l'on règle le vol par le sans fil ; on en sort par coupure de la batterie. | `00-scenarios.md` |
| Vol de réglage | Vol court déclenché par commande sans fil en mode réglage : décollage du sol, 3 secondes de stationnaire, pose. | `00-scenarios.md` |
| Variables du vol | Données renvoyées à l'appareil de suivi : commandes des moteurs, hauteur, données de position. | `00-scenarios.md` |
| Protège-hélices | Protection des hélices, obligatoire (DEC-016 « Public adulte, protège-hélices obligatoires »). | `journal-decisions.md` |
| Mise en service | Premier montage du drone : programmation, puis réglage du vol. | `00-scenarios.md` |
