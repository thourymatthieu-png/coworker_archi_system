# Reprise du projet Boomrone — état au 2026-10-29

> **Aperçu**
> - Phase « architecture » rédigée par délégation totale (DEC-218 « Délégation totale de la phase architecture à l'architecte ») : 30 éléments d'architecture, 29 tests d'intégration, tous « Proposé » ; trois relectures de porte initiales faites et corrigées, puis une seconde relecture après la révision (DEC-233 « Relecture de porte architecture : corrections décidées par délégation »). Révision du 2026-10-29 pour la contrainte JLCPCB (DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet » à DEC-244 « Relecture de porte de la révision JLCPCB : corrections décidées par délégation ») : carte assemblée par JLCPCB, composants du stock, corrections des deux revues d'experts, nouvelle relecture de porte.
> - Livrables : « Architecture » — `projets/boomrone/03-architecture.md` et section TI de « Plans de test » — `projets/boomrone/05-plans-de-test.md`.
> - La porte « architecture » n'est PAS franchie : l'accord explicite de l'utilisateur est attendu. Réserve majeure : la tension de la batterie sous charge est marginale à infaisable avec les seuils actuels (DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie »).
> - 0 doute bloquant ; non bloquants ouverts : voir ci-dessous. Avant la commande de la carte : tester le module E104-BT02 seul (DOU-151 « Module E104-BT02 : débit par défaut, service, absence de commande AT »), lire le devis de JLCPCB (DOU-153 « Carte double face, assemblage Standard, frais d'extension et délais »), choisir le genre du XT30 (DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion »), faire les mesures au banc.
> - Prochain pas : accord de la porte, puis mesures au banc avant la commande de la carte, puis phase « conception détaillée ».

```mermaid
---
title: "Avancement du cycle en V"
---
flowchart LR
    S["Scénarios : validés"] --> PS{{"Porte scénarios : franchie"}}
    PS --> B["Besoins : validés"]
    B --> PB{{"Porte besoins : franchie"}}
    PB --> R["Exigences : validées"]
    R --> PR{{"Porte exigences : franchie"}}
    PR --> A["Architecture : proposée"]
    A --> PA{{"Porte architecture : en attente de l'utilisateur"}}
    PA --> D["Conception détaillée"]
    D --> I["Implémentation et tests"]
    classDef fait fill:#c8e6c9,stroke:#2e7d32
    classDef cours fill:#ffe9a8,stroke:#c90
    class S,PS,B,PB,R,PR fait
    class A,PA cours
```

## Choix d'architecture clés
- Matériel : carte maison unique double face, fabriquée et assemblée par JLCPCB (composants du stock LCSC relevés le 2026-10-29, voir la nomenclature de « Architecture » — `projets/boomrone/03-architecture.md`), microcontrôleur STM32G431 programmé par SWD avec le ST-LINK, centrale LSM6DSO et capteur de hauteur VL53L1X en puces nues posées par JLCPCB, flux optique PMW3901 sur sa petite carte achetée soudée par 6 fils (nécessaire pour la dérive ; la puce nue est écartée, DOU-152 « PMW3901 : puce nue ou carte achetée, alimentation et refusion »), module BLE Ebyte E104-BT02 à la place du HM-10 (stock nul), 4 moteurs à balais 8520 avec hélices de 45 mm (65 mm ne tiennent pas dans 100 mm) et anneaux, MOSFET à rappel à la masse (un reset coupe les moteurs), batterie 1S 850 mAh avec connecteur XT30, LDO 3,0 V, voyant RGB et buzzer actif (DEC-219 « Structure générale : carte maison unique, microcontrôleur STM32G431, boucle sans système temps réel » à DEC-223 « Radio Bluetooth HM-10, protocole de trames et logiciel d'essai en Python », DEC-228 « Effets locaux : table des dix effets, buzzer actif à un seul timbre »).
- Logiciel : C sans système temps réel, cycle à 1 kHz, une seule machine à états (18 états), chien de garde matériel de 100 ms, réglages en une page de flash, trois jalons J1 vol, J2 radio, J3 mode réglage, logiciel d'essai Python (DEC-224 « Logiciel : une seule machine à états, cycle à 1 kHz, modules » à DEC-227 « Réglages : page de flash de l'image, valeurs hors bornes, sauvegarde au sol », DEC-230 « Plan de livraison par jalons, ordre de livraison levé »).
- Bilan : masse 62 g pour 100 g (65 g avant la révision), poussée/poids 1,41, logique dimensionnée à 130 mA, crête 9,5 A, tension sous charge jusqu'à 3,17 V avec 3,7 V à l'armement ; repli proposé : armement à 3,9 V et sous-tension à 3,0 V (DEC-229 « Faisabilité conjointe : bilan, verdict marginal, mesures au banc avant la commande de la carte »).
- Corrections techniques de la révision : SPI1 à 5,3 MHz et SPI2 à 1,33 MHz (DEC-238 « Fréquences SPI et lecture de la centrale inertielle »), pilote du capteur de hauteur non bloquant avec reprise par niveaux (DEC-239 « Capteur de hauteur : pilote non bloquant, reprise, échec d'initialisation, mesure horodatée »), brochage complété sans timer pour le voyant (DEC-240 « Brochage, timers, voyant et bouton »), règles de mémoire (DEC-241 « Mémoire et ordonnancement : règles de robustesse »). Écart avec REQ-044 « Assemblage à la main » : proposition dans DEC-237 « Écart avec REQ-044 : assemblage par JLCPCB, proposition à valider ».

## Doutes
- Levés pendant l'architecture : DOU-060 « Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle », DOU-109 « Batterie déjà déchargée : redémarrages répétés, décharge profonde et état après une coupure logicielle », DOU-115 « Contenu et interruption de la réécriture de la zone des réglages par la reprogrammation », DOU-118 « Seuil de protection et consommation résiduelle du drone laissé allumé », DOU-120 « Écriture en mémoire sous tension basse ou pendant une phase de vol », DOU-136 « Ordre de livraison : exigence essentielle dépendant du mode réglage souhaitable » (DEC-227 « Réglages : page de flash de l'image, valeurs hors bornes, sauvegarde au sol », DEC-230 « Plan de livraison par jalons, ordre de livraison levé », DEC-231 « Garanties d'arrêt, batterie basse et consommation résiduelle : doutes levés »).
- Ouverts, non bloquants, architecture : DOU-133 « Forme des dix effets locaux : lumière, son, distinction mesurable » (à vérifier à TS-014 « Perceptibilité et distinction des effets ») ; DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie » ; DOU-137 « Latence de bout en bout de l'arrêt sans fil sur Bluetooth » ; DOU-138 « Interprétations de l'architecture logicielle : priorité de l'initialisation, causes de refus, sauvegarde et statut » ; DOU-139 « Capteurs de hauteur et de flux : hauteur de montage et sols sans texture » ; DOU-140 « Défaut de capteur en vol : cause et effet rattachés à l'échec de stabilisation ».
- Ouverts, non bloquants, révision JLCPCB : DOU-142 « Fuite d'entrée de l'ADC et marge de ±50 mV de la mesure de tension » à DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion » (14 doutes) ; DOU-141 « Assemblage de la carte : à la main ou composants posés par JLCPCB, et disponibilité des pièces chez LCSC » est levé (DEC-236 « Assemblage par JLCPCB : puces nues, carte double face, flux acheté »).
- Ouverts, essais sur prototype : DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m », DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal », DOU-116 « Échéance et circularité du report aux essais, comportement de SCN-002 sur la partie infaisable de la plage », DOU-131 « Valeurs provisoires des exigences, à valider aux essais sur prototype ».

## Vérification
`python tools/check_traceability.py projets/boomrone` : aucune erreur de titre ni de référence (état au 2026-10-29 après la révision) ; plus aucun « REQ sans ARC » ni « ARC sans TI ». Trous restants : 30 « ARC sans DES » (attendus avant la conception détaillée) et 12 « SCN sans BES » (défaut connu de l'outil, DEC-156 « Couverture des scénarios vérifiée à la main, outil de traçabilité inchangé »).

## À faire ensuite
1. L'utilisateur donne ou refuse l'accord de la porte « architecture » (statut des ARC « Proposé » à passer à « Validé », à consigner par une décision).
2. Mesurer au banc poussée, courant et résistance interne (TI-007 « Moteurs, poussée, masse et dimensions », TI-008 « Batterie, connecteur, chute de tension et mesure de tension ») avant de commander la carte ; décider du repli R1 + R2 si nécessaire.
3. Phase « conception détaillée » (`04-conception-detaillee.md`), avec les tests unitaires.
4. DOU-150 « Écart entre l'exigence d'assemblage à la main et l'assemblage par JLCPCB » est levé : REQ-044 « Assemblage à la main », TS-020 « Fabrication à la main » et TA-015 « Inspection de la fabrication à la main » sont réécrites (DEC-245 « REQ-044 réécrite : carte fabriquée et assemblée par JLCPCB, raccordements à la main »).
5. Historique : `journal-decisions.md` (DEC-218 « Délégation totale de la phase architecture à l'architecte » à DEC-233 « Relecture de porte architecture : corrections décidées par délégation » pour cette phase) et l'historique git.
