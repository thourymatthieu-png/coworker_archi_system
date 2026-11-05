# Réponses de l'utilisateur sur les règles de placement (essai des outils)

Notes de travail du 2026-11-05, **non décisionnelles** : phase de test des outils de placement
(`tools/pcb_placement/`). Aucune de ces réponses n'est inscrite dans `journal-decisions.md` ni dans
`registre-doutes.md` ; elles servent à régler le moteur. Fichier de règles proposé par l'agent
`electronique-hardware` : `regles_placement.json` (même dossier). Les numéros de question sont ceux
du rapport de l'agent.

| N° | Question | Réponse de l'utilisateur | Conséquence pour le moteur |
|---|---|---|---|
| 1 | Géométrie des pièces verrouillées | **PCB KiCad** (M1 sud-ouest, M2 nord-ouest, M3 nord-est, M4 sud-est ; U7 en (9 ; 25) avec le corps sur la carte et l'antenne seule en débord) | Le PCB est la source de vérité. `placement_constraints.json` est **périmé** (M1 au nord-ouest, U7 entièrement hors carte) : ne plus l'utiliser. |
| 2 | « Centre de la face basse » de DES-003 « Raccordement de la centrale inertielle LSM6DSO » | **Centre de la carte** (25 ; 25) | Zone souple de U2 autour du centre de la carte. (Le centre des moteurs serait (25 ; 27,9), non retenu.) |
| 3 | Position de la batterie | **Au-dessus, centrée** | Pas encore de règle (dimensions de la batterie inconnues). À contrôler : accès à SW1, visibilité de LED1, sortie du son de BZ1, et recouvrement du corps de U7 (x de 1,25 à 16,75). |
| 4 | Rotation de U2 | **Imposer 0°** | Rotation de U2 verrouillée à 0° : la matrice de passage du firmware (DOU-167 « Orientation des axes de la centrale et sens de rotation des moteurs ») ne dépend pas du placement. |
| 5 | Distances d'isolement | **Seulement celles qui ont une source** | Les 6 isolements restent documentés ; leurs distances sont à `null`, donc sans effet tant qu'une source ou l'utilisateur n'en donne pas. |
| 6 | Bord et face des plots TP1 à TP6 (flux) et TP7 à TP10 (radio) | **Aucune contrainte** | La règle « bord de carte » de DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V » n'est pas appliquée pour l'instant. |
| 7 | Fiches PMW3901MB et PB-03F absentes | **Continuer sans les fiches** | Valeurs reprises d'ARC-005 « Capteur de flux optique », DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V » et DES-012 « Raccordement du module Bluetooth PB-03F », marquées « à vérifier ». |
| 8 | Règles « hypothèse » I-05, Z-05, Z-09, B-10 | **Seulement les règles sourcées** | Ces 4 règles restent documentées, non appliquées. |
| 9 | Réservoir C6, C7, C9 du rail VBATM | **Près de J1 (tête de ligne)** | Règle d'essai demandée explicitement. **À noter** : c'est une règle sans source de fiche, exception voulue à la réponse 8 (qui avait écarté Z-05, de même nature) ; à confirmer si l'on veut la généraliser. |
| 10 | Cônes d'exclusion du VL53L1X (36,5° et 39,6°) contre les 27° du projet | **Pas de zone interdite pour l'instant** | Aucune zone interdite. Fait vérifié (DS12385 figure 19, page 24) : cônes d'exclusion mécaniques « RTN » 39,6° (Ø1,08 mm) et « EMT » 36,5° (Ø0,84 mm), plus larges que le champ de vue optique de 27° (page 4) retenu par ARC-004 « Capteur de hauteur à temps de vol », DES-004 « Raccordement du capteur de hauteur VL53L1X » et DES-013 « Implantation, routage et fichiers de fabrication pour JLCPCB ». À présenter à l'architecte plus tard. |
| 11 | Faces haute et basse | **2D pour l'instant, faces plus tard** | Le moteur traite tout sur une couche ; la face reste une étiquette. Gestion des deux faces : suggestion dans `tools/pcb_placement/TODO.md`. |
| 12 | Pas des pastilles moteur | **5,8 mm**, après rappel de DEC-290 « Schéma KiCad proj_boomrone : bibliothèque locale, feuilles hiérarchiques, validation page par page » | DEC-290 « Schéma KiCad proj_boomrone : bibliothèque locale, feuilles hiérarchiques, validation page par page » reste valable. Le « 5,08 mm » de l'essai du 5 novembre est périmé ; DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie » n'est pas modifié. |
| 13 | Côté d'accouplement du XT30 (J1) | **Vers le sud** | J1 reste au bord sud, le sud est le côté d'enfichage libre. DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion » reste ouvert pour le genre. |

## Contradictions relevées pendant les réponses
- Question 12 : la première réponse (5,08 mm) contredisait DEC-290 « Schéma KiCad proj_boomrone : bibliothèque locale, feuilles hiérarchiques, validation page par page » ; l'utilisateur a confirmé
  5,8 mm après rappel. Aucune décision changée.
- Question 9 contre question 8 : règle d'essai demandée pour C6, C7, C9 alors que les règles sans
  source étaient écartées. Traitée comme une exception explicite (voir ci-dessus).

## Restent ouverts (hors de ces questions)
- Fiches en anglais du PMW3901MB et du PB-03F, fiche du buzzer SMD-9650-3327 (orifice sonore inconnu).
- Contour : 50 x 50 mm est un essai, DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie » ; 40 x 35 mm dans ARC-013 « Carte électronique JLCPCB, câblage et assemblage ».
- Longueur de VL53L1X du module : 4,4 mm (tableau 2, page 4) contre 4,9 mm (figure 18, page 23) :
  vérifier l'empreinte.
