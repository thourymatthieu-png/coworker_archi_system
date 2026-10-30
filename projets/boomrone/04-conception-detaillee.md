# Conception détaillée

> **Aperçu**
> - 38 éléments de conception (DES) qui déclinent les 30 éléments de « Architecture » — `projets/boomrone/03-architecture.md` : 14 matériels (schémas, valeurs de composants, mécanique, bilan, numérotés en premier) et 24 logiciels ou documentaires ; 38 tests unitaires (TU) dans « Plans de test » — `projets/boomrone/05-plans-de-test.md`.
> - Rédigée par délégation totale (DEC-254 « Délégation totale de la phase conception détaillée à l'architecte ») ; seuils de batterie conservés (DEC-253 « Seuils de batterie conservés, sans mesures au banc pour la première version »), aucune mesure au banc : gains et constantes de départ provisoires.
> - Aucun code ni schéma KiCad n'existe encore : « Réalisé par » donne les chemins prévus.
> - Schémas SVG des circuits de la carte (un par bloc de circuit, ni mécanique ni logiciel ; dossier `projets/boomrone/schemas/`) : illustrations de conception, pas les schémas KiCad de fabrication (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée ») ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée », broches non relevées : DOU-182 « Noms et numéros de broches des circuits intégrés des schémas SVG non relevés dans les fiches ».
> - État : tous les DES sont « Validé », porte franchie le 2026-10-30 (DEC-276 « Porte conception détaillée franchie : accord explicite de l'utilisateur »). Choix : DEC-255 « Conception détaillée : chaîne de développement et arborescence des fichiers » à DEC-271 « Cycle indépendant du DMA de la centrale et lecture armée après l'initialisation » ; doutes : DOU-167 « Orientation des axes de la centrale et sens de rotation des moteurs » à DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ».

## Vue d'ensemble

```mermaid
---
title: "Vue d'ensemble : 38 éléments de conception par domaine"
---
flowchart LR
    subgraph MAT["Matériel (DES-001 à DES-014)"]
        H1["Carte : schéma, MCU, implantation<br/>DES-001, 002, 013"]
        H2["Capteurs : IMU, hauteur, flux<br/>DES-003, 004, 005"]
        H3["Puissance : moteurs, batterie, alimentation<br/>DES-007, 008, 009"]
        H4["Interface : bouton, voyant, radio<br/>DES-010, 011, 012"]
        H5["Cadre, bilan<br/>DES-006, 014"]
    end
    subgraph LOG["Logiciel (DES-015 à DES-038)"]
        L1["Structure : mémoire, cycle, coupure<br/>DES-015, 016, 017"]
        L2["Pilotes<br/>DES-018 à 022"]
        L3["Estimation et contrôle<br/>DES-023 à 026"]
        L4["Machine, bouton, surveillance, chien de garde, initialisation<br/>DES-027 à 031"]
        L5["Effets, radio, réglage, paramètres<br/>DES-032 à 035"]
        L6["Suivi, jalons, consignes<br/>DES-036 à 038"]
    end
    H2 --> L2
    H3 --> L2
    H4 --> L2
    L2 --> L3 --> L4 --> L5
    L5 --> L6
```

*Légende : un cadre par domaine, les numéros sont ceux des DES ; les éléments sans flèche (carte, cadre, bilan) sont des fondations transverses ; la flèche indique le sens des données ou des dépendances. Les titres complets sont dans la table de couverture et dans les éléments plus bas.*

## Cycle du logiciel

Le logiciel est une boucle à 1 kHz sans système d'exploitation temps réel ; le détail (interruptions, priorités, tâches de fond) est dans DES-016 « Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond ».

```mermaid
---
title: "Chaîne de traitement du cycle de contrôle"
---
flowchart LR
    IMU["IMU lue par DMA<br/>DES-018"] --> ATT["Attitude<br/>DES-023"]
    ADC["Tension<br/>DES-022"] --> SAF["Surveillance<br/>DES-029"]
    ATT --> CRI["Critères<br/>DES-025"]
    TOF["Hauteur 30 Hz<br/>DES-019"] --> HAU["Hauteur et vitesse<br/>DES-024"]
    FLX["Flux 100 Hz<br/>DES-020"] --> CRI
    ATT --> HAU
    HAU --> CRI
    CRI --> FSM["Machine à états<br/>DES-027"]
    CRI --> CTL
    ADC --> CTL
    SAF --> FSM
    BTN["Bouton<br/>DES-028"] --> FSM
    FSM --> CTL["Contrôle et mixeur<br/>DES-026"]
    ATT --> CTL
    HAU --> CTL
    CTL --> MOT["Moteurs<br/>DES-021"]
    FSM --> EFF["Effets<br/>DES-032"]
    FSM <--> RAD["Radio<br/>DES-033"]
```

*Légende : une flèche = « produit une donnée consommée par ». Le chien de garde (DES-030 « Chien de garde matériel et règle de rafraîchissement ») est rafraîchi en fin de cycle.*

## Couverture des éléments d'architecture

Chaque élément d'architecture est cité par au moins un élément de conception (table générée à partir des lignes « Réfs amont » ci-dessous, vérifiée par `python tools/check_traceability_V2.py projets/boomrone --gate --phase conception`).

| Élément d'architecture | Éléments de conception |
|---|---|
| ARC-001 « Structure générale du drone » | DES-001 « Schéma par blocs, réseaux et domaines de tension de la carte » |
| ARC-002 « Microcontrôleur et programmation par liaison SWD » | DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option » |
| ARC-003 « Centrale inertielle » | DES-003 « Raccordement de la centrale inertielle LSM6DSO » ; DES-018 « Pilote de la centrale inertielle » |
| ARC-004 « Capteur de hauteur à temps de vol » | DES-004 « Raccordement du capteur de hauteur VL53L1X » ; DES-019 « Pilote du capteur de hauteur non bloquant » |
| ARC-005 « Capteur de flux optique » | DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V » ; DES-020 « Pilote du flux optique » |
| ARC-006 « Moteurs, hélices et protège-hélices » | DES-006 « Cadre, anneaux, moteurs et hélices » |
| ARC-007 « Étage de puissance des moteurs coupés par défaut » | DES-007 « Circuit de puissance des moteurs » ; DES-017 « Coupure des moteurs, démarrage unique et gestionnaires d'exception » |
| ARC-008 « Batterie et connecteur débranchable » | DES-008 « Batterie, connecteur XT30 et entrée de la carte » |
| ARC-009 « Alimentation de la logique et mesure de la tension » | DES-009 « Régulateur de 3,0 V et pont de mesure de la tension » ; DES-022 « Pilote de la mesure de tension de la batterie » |
| ARC-010 « Bouton » | DES-010 « Circuit du bouton » |
| ARC-011 « Voyant RGB et avertisseur sonore » | DES-011 « Circuit du voyant RGB et du buzzer » |
| ARC-012 « Module radio Bluetooth à basse consommation » | DES-012 « Raccordement du module Bluetooth E104-BT02 » |
| ARC-013 « Carte électronique JLCPCB, câblage et assemblage » | DES-001 « Schéma par blocs, réseaux et domaines de tension de la carte » ; DES-013 « Implantation, routage et fichiers de fabrication pour JLCPCB » |
| ARC-014 « Bilan de masse, de poussée et d'autonomie » | DES-014 « Feuille de calcul du bilan de masse, de poussée et d'autonomie » |
| ARC-015 « Structure logicielle et ordonnancement » | DES-015 « Arborescence du firmware, édition de liens et budget de mémoire » ; DES-016 « Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond » ; DES-017 « Coupure des moteurs, démarrage unique et gestionnaires d'exception » |
| ARC-016 « Pilotes des capteurs et des sorties » | DES-018 « Pilote de la centrale inertielle » ; DES-019 « Pilote du capteur de hauteur non bloquant » ; DES-020 « Pilote du flux optique » ; DES-021 « Pilotes des moteurs, du voyant, du buzzer et de la liaison série » ; DES-022 « Pilote de la mesure de tension de la batterie » |
| ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse » | DES-023 « Filtre d'attitude de Mahony » ; DES-024 « Observateur de hauteur et de vitesse verticale » ; DES-025 « Vitesse horizontale et critères d'immobilité, de platitude et de stationnaire » |
| ARC-018 « Boucle de contrôle du vol » | DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique » |
| ARC-019 « Machine à états du drone » | DES-027 « Machine à états : données, événements et table de transitions » |
| ARC-020 « Gestion logicielle du bouton » | DES-028 « Gestion logicielle du bouton » |
| ARC-021 « Surveillance et coupures automatiques » | DES-029 « Surveillance et coupures automatiques » |
| ARC-022 « Chien de garde » | DES-030 « Chien de garde matériel et règle de rafraîchissement » |
| ARC-023 « Initialisation et échec d'initialisation » | DES-031 « Séquence d'initialisation et échec d'initialisation » |
| ARC-024 « Effets locaux (logiciel) » | DES-032 « Effets locaux : table, séquenceur de lumière et de son » |
| ARC-025 « Protocole et service du statut sans fil » | DES-033 « Trames du statut sans fil, automate de réception et file d'émission » |
| ARC-026 « Mode réglage et vol de réglage » | DES-034 « Mode réglage, filtrage des commandes et vol de réglage » |
| ARC-027 « Paramètres de vol et stockage des réglages » | DES-035 « Paramètres de vol, section d'origine et pilote de flash » |
| ARC-028 « Logiciel d'essai de l'appareil de suivi » | DES-036 « Logiciel de suivi en Python » |
| ARC-029 « Plan de livraison par jalons » | DES-037 « Jalons de livraison et configurations de compilation » |
| ARC-030 « Page de consignes d'emploi » | DES-038 « Contenu de la page de consignes d'emploi » |

## Règles de lecture

- Les valeurs de composants et les constantes numériques marquées « de mémoire » ou « de départ » ne sont pas vérifiées : voir les doutes DOU-172 « Valeurs de configuration des périphériques à vérifier dans le manuel de référence », DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage », DOU-170 « Constantes de capteurs de départ : échelle du flux, retard du capteur de hauteur, filtres », DOU-171 « Gains de référence, poussée de sustentation et linéarisation de la poussée ».
- Chaque DES a un TU de même rang dans « Plans de test » — `projets/boomrone/05-plans-de-test.md` (section « Tests unitaires (TU) »).
- Les champs « Réalisé par » donnent des chemins prévus, relatifs à la racine du dépôt.

## Éléments de conception

Format :

```
### DES-001 — Titre du module ou du circuit
**Réfs amont :** ARC-001 « Titre de l'élément d'architecture »
**Description :** structures, algorithmes, brochage, budgets.
**Réalisé par :** fichier source ou schéma (chemin)
**Statut :** Proposé | Validé | Abandonné
```

### DES-001 — Schéma par blocs, réseaux et domaines de tension de la carte
**Réfs amont :** ARC-001 « Structure générale du drone » ; ARC-013 « Carte électronique JLCPCB, câblage et assemblage »
**Description :** schéma racine de la carte, saisi dans KiCad, avec trois domaines de tension et une table de réseaux (« net » = fil du schéma) qui sert de contrat entre le schéma, le logiciel et les essais.

```mermaid
---
title: "Domaines de tension et réseaux principaux de la carte"
---
flowchart LR
    XT["XT30 (batterie)"] --> VBM["VBATM : moteurs, voyant, buzzer, pont de mesure"]
    XT --> FB["Ferrite 120 ohms"] --> VBL["VBATL : entrée des régulateurs"]
    VBL --> L3["MCP1700 : +3V0 logique"]
    L3 --> L2["XC6206 : +2V0 flux optique"]
    L3 --> MCU["STM32G431"]
    L3 --> CAP["LSM6DSO, VL53L1X, E104-BT02"]
    VBM --> FET["4 MOSFET moteurs + 4 moteurs"]
    VBM --> OUT["Voyant RGB + buzzer (3 + 1 MOSFET)"]
    VBM --> DIV["Pont 100k / 150k vers PA0"]
    MCU -- "PWM, GPIO" --> FET
    MCU -- "GPIO" --> OUT
```

*Légende : VBATM = batterie vue au connecteur (3,1 à 4,2 V, 9,5 A en crête) ; VBATL = batterie filtrée pour les régulateurs ; +3V0 = rail logique (130 mA) ; +2V0 = rail du flux optique (environ 9 mA). Masse unique (plan plein).*

Réseaux de signaux (nom, broche du microcontrôleur, rôle) : M1_G à M4_G (PA8 à PA11, grilles moteurs), IMU_SCK, IMU_MISO, IMU_MOSI (PA5, PA6, PA7), IMU_CS (PA4), IMU_INT1 (PB0), FLX_SCK, FLX_MISO, FLX_MOSI (PB13, PB14, PB15), FLX_CS (PB12), I2C_SCL (PA15), I2C_SDA (PB7), TOF_GPIO1 (PB6), TOF_XSHUT (PB9), BLE_TX (PA2), BLE_RX (PA3), LED_R, LED_G, LED_B (PB1, PB2, PB10), BUZ (PB11), BTN (PB5), VBAT_SENSE (PA0), SWDIO (PA13), SWCLK (PA14), NRST, BOOT0 (PB8). Le détail électrique de chaque bloc est dans DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option » à DES-012 « Raccordement du module Bluetooth E104-BT02 ».

Points d'essai (pastilles de 1 mm, face haute) : +3V0, +2V0, VBATM, VBATL, GND (deux), M1_D (drain du moteur 1), BLE_TX, BLE_RX, TOF_GPIO1. Six plots de repli du flux (3,0 V, masse, SCK, MOSI, MISO, CS) comme dans ARC-013 « Carte électronique JLCPCB, câblage et assemblage ».

Budget de courant : +3V0 130 mA (dimensionnement), VBATM 9,5 A en crête de 2 s. Règle de lecture : un réseau absent de cette liste ne doit pas exister au schéma ; un réseau de la liste doit avoir au moins deux broches (vérifié par TU-001 « Réseaux de la carte : table, ERC et broches uniques »).

![Schéma par blocs de la carte : domaines de tension et blocs](schemas/des-001-blocs-et-reseaux.svg)

*Légende : vue par blocs, le schéma de chaque bloc est dans le DES indiqué dans la boîte. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (page racine « Blocs »), `projets/boomrone/hardware/calculs/calculs.py`, `projets/boomrone/schemas/des-001-blocs-et-reseaux.svg`
**Statut :** Validé

### DES-002 — Microcontrôleur : brochage, horloges, découplage et octets d'option
**Réfs amont :** ARC-002 « Microcontrôleur et programmation par liaison SWD »
**Description :** brochage retenu (celui de ARC-002 « Microcontrôleur et programmation par liaison SWD », à compléter des numéros de broches physiques du LQFP-48 : DOU-148 « Numéros de broches physiques du LQFP-48 à relever dans la fiche DS12589 ») ; toute broche non listée est configurée en entrée analogique à l'initialisation (pas de broche flottante en numérique).

| Fonction | Broche | Mode | Remarque |
|---|---|---|---|
| Moteurs 1 à 4 | PA8, PA9, PA10, PA11 | TIM1 CH1 à CH4 (AF6 pour PA8 à PA10, AF11 pour PA11 de mémoire : DOU-172 « Valeurs de configuration des périphériques à vérifier dans le manuel de référence »), puis sortie basse en coupure | grille via 47 ohms, rappel 100 kohms à la masse |
| IMU SCK, MISO, MOSI | PA5, PA6, PA7 | SPI1 (AF5), mode 3 | diviseur 32 : 5,3125 MHz |
| IMU CS, INT1 | PA4, PB0 | sortie (niveau haut au repos), entrée | rappel de 10 kohms de CS au +3V0 |
| Flux SCK, MISO, MOSI | PB13, PB14, PB15 | SPI2 (AF5), mode 3 | diviseur 128 : 1,328125 MHz |
| Flux CS | PB12 | sortie (niveau haut au repos) | rappel de 10 kohms au +3V0 |
| I2C du capteur de hauteur | PA15 (SCL), PB7 (SDA) | I2C1 (AF4 et AF4), drain ouvert | 400 kHz, rappels 4,7 kohms |
| Capteur de hauteur GPIO1, XSHUT | PB6, PB9 | entrée avec interruption externe (front descendant), sortie | rappels 10 kohms au +3V0 |
| Module radio | PA2 (TX), PA3 (RX) | USART2 (AF7) | 9600 bauds visés |
| Voyant R, V, B ; buzzer | PB1, PB2, PB10 ; PB11 | sorties | grille via 100 ohms, rappel 100 kohms |
| Bouton | PB5 | entrée | rappel externe 10 kohms au +3V0 |
| Mesure de la batterie | PA0 | ADC1 IN1 (analogique) | pont 100 / 150 kohms |
| SWD | PA13, PA14 | SWDIO, SWCLK | en-tête 1 x 5 : VTref, SWDIO, SWCLK, GND, NRST |
| BOOT0 | PB8 | entrée | 10 kohms à la masse |

Horloges (valeurs de DEC-257 « Valeurs de configuration des horloges, timers, bus et convertisseur ») : HSI 16 MHz, PLL avec M = 4, N = 85, R = 2 donnant 170 MHz ; HCLK, PCLK1 et PCLK2 à 170 MHz (diviseurs 1) ; mode « boost » ; flash avec 8 états d'attente, prefetch et caches d'instructions et de données (valeurs à confirmer : DOU-172 « Valeurs de configuration des périphériques à vérifier dans le manuel de référence »). TIM2 : prédiviseur 169, compteur libre de 32 bits à 1 MHz ; TIM6 : prédiviseur 169, rechargement 999, tick de 1 kHz ; TIM1 : prédiviseur 0, rechargement 7082, soit 170 MHz / 7083 = 24,001 kHz, résolution 7083 pas ; SPI1 diviseur 32 et SPI2 diviseur 128 ; USART2 : BRR = 17708, soit 9600,0 bauds (erreur inférieure à 0,01 %) ; I2C1 : registre de timing calculé pour 400 kHz avec l'outil de ST (valeur à relever, DOU-172 « Valeurs de configuration des périphériques à vérifier dans le manuel de référence »). Sortie du verrou moteurs : OSSI = 0 et OSSR = 0, les sorties sont libérées quand MOE = 0.

Découplage (de mémoire, à confirmer dans la fiche DS12589 : DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage ») : 100 nF sur chaque broche VDD, 4,7 µF commun, VDDA 100 nF + 1 µF, NRST 100 nF à la masse, pas de bouton de reset. Octets d'option à programmer (procédure de ARC-002 « Microcontrôleur et programmation par liaison SWD ») : IWDG_SW = 0 (chien de garde matériel), BOR_LEV = 3 (environ 2,5 V de mémoire, inférieur au minimum de 2,6 V du capteur de hauteur : DOU-181 « Bilan d'erreur de la mesure de tension et niveau du BOR »), protection en lecture niveau 0. Règles : PB4 reste inutilisée et PA15 ne commande jamais une grille (JTAG au reset) ; SPI1 au plus 10 MHz, SPI2 au plus 2 MHz. Programmation : STM32CubeProgrammer en SWD, hélices démontées, sans relier le 3,3 V du ST-LINK.

Budgets : flash 128 kio, SRAM 32 kio dont 16 kio de SRAM1 utilisés (le détail est dans DES-015 « Arborescence du firmware, édition de liens et budget de mémoire »).

![Schéma du microcontrôleur : brochage, SWD, BOOT0, NRST et découplage](schemas/des-002-microcontroleur.svg)

*Légende : brochage par groupe de fonctions, programmation SWD, découplage. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ». En orange, éléments à vérifier : DOU-148 « Numéros de broches physiques du LQFP-48 à relever dans la fiche DS12589 » ; DOU-172 « Valeurs de configuration des périphériques à vérifier dans le manuel de référence » ; DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage » ; DOU-181 « Bilan d'erreur de la mesure de tension et niveau du BOR ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (feuille « MCU »), `projets/boomrone/firmware/src/board.c`, `projets/boomrone/firmware/src/board.h`, `projets/boomrone/firmware/src/board_pins.h`, `projets/boomrone/schemas/des-002-microcontroleur.svg`
**Statut :** Validé

### DES-003 — Raccordement de la centrale inertielle LSM6DSO
**Réfs amont :** ARC-003 « Centrale inertielle »
**Description :** LSM6DSOTR (LGA-14) au centre de la face basse. Liaison SPI à 4 fils sur SPI1 (SDO/SA0 vers MISO, SDI vers MOSI), CS sur PA4 avec un rappel de 10 kohms au +3V0 (le composant reste désélectionné pendant le reset du microcontrôleur), INT1 vers PB0, INT2 non raccordée, entrées de la liaison auxiliaire (capteur externe) à la masse ou laissées selon la fiche (à relever, DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage »). VDD et VDDIO au +3V0, 100 nF au plus près de chaque broche et 10 µF commun. Pas de plan de masse coupé sous le composant.

Registres écrits à l'initialisation (valeurs de ARC-003 « Centrale inertielle » et des notes d'architecture, à confirmer dans la fiche ST) : CTRL3_C = 0x44 (BDU et IF_INC, après SW_RESET et attente de fin de reset), CTRL4_C = 0x06 (liaison I2C coupée, filtre passe-bas du gyroscope actif), CTRL1_XL = 0x9C (3,33 kHz, ±8 g), CTRL2_G = 0x9C (3,33 kHz, ±2000 °/s), INT1_CTRL = 0x03 (données prêtes de l'accéléromètre et du gyroscope). Identité WHO_AM_I (0x0F) attendue 0x6C.

Échelles : gyroscope 70 m°/s par pas, accéléromètre 0,244 mg par pas. Axes : la puce est sur la face basse, face vers le bas : la matrice de passage du repère de la puce au repère du drone (x vers l'avant, y vers la gauche, z vers le haut) est une constante de `config_fixed.h`, par défaut une rotation de 180° autour de x (x inchangé, y et z inversés), à confirmer après le routage : DOU-167 « Orientation des axes de la centrale et sens de rotation des moteurs ». Fixation de la carte au cadre par de la mousse fine (DOU-154 « Vibrations des moteurs sur la centrale inertielle posée sur la carte rigide »).

![Schéma du raccordement de la centrale inertielle LSM6DSO](schemas/des-003-centrale-inertielle.svg)

*Légende : liaison SPI1, rappel de CS, alimentations et registres d'initialisation. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ». En orange, éléments à vérifier : DOU-167 « Orientation des axes de la centrale et sens de rotation des moteurs » ; DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage » ; DOU-182 « Noms et numéros de broches des circuits intégrés des schémas SVG non relevés dans les fiches ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (feuille « Capteurs »), `projets/boomrone/firmware/src/drv_imu_regs.h`, `projets/boomrone/schemas/des-003-centrale-inertielle.svg`
**Statut :** Validé

### DES-004 — Raccordement du capteur de hauteur VL53L1X
**Réfs amont :** ARC-004 « Capteur de hauteur à temps de vol »
**Description :** VL53L1CXV0FY/1 (LGA-12) en face basse, regardant le sol. Alimentations AVDD, AVDDVCSEL et IOVDD au +3V0 (le rail descend à environ 2,9 V, minimum 2,6 V du composant) avec 4,7 µF + 100 nF sur AVDDVCSEL et 100 nF sur AVDD et IOVDD (valeurs de la fiche DS12093 de mémoire : DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage »). I2C1 sur PA15 (SCL) et PB7 (SDA), rappels de 4,7 kohms au +3V0, adresse 0x29. GPIO1 vers PB6 (rappel 10 kohms au +3V0), XSHUT vers PB9 (rappel 10 kohms : le capteur est actif dès la mise sous tension). Le temps de montée de l'I2C reste sous les 300 ns exigés à 400 kHz tant que la capacité du bus est inférieure à 75 pF (calcul : 0,8473 x 4,7 kohms x C ; avec 30 pF on obtient 119 ns). Variante VL53L1CX : DOU-157 « VL53L1CX contre VL53L1X : identifiant, bibliothèque et registres ».

Mécanique : fenêtre optique dégagée, cône de 27° sans pièce dessous, capteur à 20 mm du plan de contact (voir DES-006 « Cadre, anneaux, moteurs et hélices ») : hauteur du drone = lecture brute moins 20 mm, coupure à 25 mm de hauteur = lecture brute de 45 mm.

![Schéma du raccordement du capteur de hauteur VL53L1X](schemas/des-004-capteur-hauteur.svg)

*Légende : I2C1 avec rappels, GPIO1, XSHUT, alimentations et découplages. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ». En orange, éléments à vérifier : DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage » ; DOU-157 « VL53L1CX contre VL53L1X : identifiant, bibliothèque et registres » ; DOU-182 « Noms et numéros de broches des circuits intégrés des schémas SVG non relevés dans les fiches ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (feuille « Capteurs »), `projets/boomrone/schemas/des-004-capteur-hauteur.svg`
**Statut :** Validé

### DES-005 — Raccordement du flux optique PMW3901MB et régulateur de 2,0 V
**Réfs amont :** ARC-005 « Capteur de flux optique »
**Description :** puce PMW3901MB-TXQT (COB-28, face basse) alimentée en VDD par un XC6206P202MR-G (SOT-23, 2,0 V) lui-même alimenté par le +3V0 ; VDDIO au +3V0 (VDDIO au moins égale à VDD, respecté dès le démarrage). Régulateur : 1 µF en entrée, 2,2 µF en sortie (valeurs usuelles de la famille, à relever dans la fiche du XC6206 : DOU-165 « Flux optique : alimentation en 2,0 V, valeurs de fiche et mise sous tension »). Bilan : charge 9 mA, pointe de 70 mA à la montée de l'alimentation ; chute minimale du régulateur 0,55 à 0,78 V à 70 à 100 mA, marge disponible 1,0 V (rail à 3,0 V) ou 0,9 V (rail à 2,9 V) ; sortie 1,96 à 2,04 V si la tolérance est de 2 % (à relever), limite de la puce 1,8 à 2,1 V ; dissipation moyenne 9 mW, 70 mW à la pointe. SPI2 sur PB13, PB14, PB15, CS sur PB12 avec un rappel de 10 kohms ; NRESET tirée au +3V0 par 10 kohms ; MOTION non câblée ; plot de masse central soudé à la masse. Condensateurs de la figure 8 de la fiche : empreintes 0603 prévues pour 1 µF et 100 nF sur VDD, 100 nF sur VDDIO et 2,2 µF sur VREG, valeurs finales à relever sur le dessin avant le routage (DOU-165 « Flux optique : alimentation en 2,0 V, valeurs de fiche et mise sous tension »).

Optique : lentille LN03-ZSZ (fournie avec la puce, à confirmer : DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce ») collée à la main sur la puce posée, au centre de l'ouverture, avec une colle époxy ou UV sans dégagement gazeux, sans toucher la fenêtre ; vérifier la hauteur de montage avec la lentille (DOU-166 « PMW3901MB : plage de température de 0 à 40 °C et hauteur de montage avec la lentille »). Six plots de repli de 1,5 x 1,5 mm au pas de 2,54 mm en bord de carte (3,0 V, masse, SCK, MOSI, MISO, CS), reliés aux réseaux du flux par des pistes de moins de 5 mm.

![Schéma du flux optique PMW3901MB et du régulateur de 2,0 V](schemas/des-005-flux-optique-regulateur-2v0.svg)

*Légende : régulateur XC6206 vers +2V0, VDDIO à +3V0, SPI2, NRESET et plots de repli. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ». En orange, éléments à vérifier : DOU-165 « Flux optique : alimentation en 2,0 V, valeurs de fiche et mise sous tension » ; DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce » ; DOU-182 « Noms et numéros de broches des circuits intégrés des schémas SVG non relevés dans les fiches ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (feuille « Capteurs »), `projets/boomrone/schemas/des-005-flux-optique-regulateur-2v0.svg`
**Statut :** Validé

### DES-006 — Cadre, anneaux, moteurs et hélices
**Réfs amont :** ARC-006 « Moteurs, hélices et protège-hélices »
**Description :** cadre en un seul modèle paramétrique OpenSCAD (DEC-268 « Mécanique : anneaux tangents, modèle OpenSCAD et impression en ligne »). Quatre anneaux tangents (diamètre intérieur 47 mm, paroi 1,0 mm, donc diamètre extérieur 49 mm égal à l'entraxe) aux sommets d'un carré de 49 mm : encombrement 98 x 98 mm. Chaque moteur 8520 (diamètre 8,5 mm) est tenu dans une poche de 8,6 mm au centre de l'anneau par deux rayons de 1,0 x 1,5 mm situés sous le plan de l'hélice, qui ne coupent pas le disque des hélices de 45 mm. La carte repose sur quatre plots au centre, face haute vers le haut, le connecteur XT30 au bord accessible entre deux anneaux. Hauteur des anneaux 10 mm centrée sur le plan des hélices (le calibre de 12 mm de REQ-032 « Protège-hélices » ne touche aucune hélice).

Recouvrement : la carte de 40 x 35 mm au centre d'un carré de 49 mm déborde sur les disques des hélices (son coin est à 8 mm du centre d'une hélice dont le rayon est 22,5 mm) ; sa hauteur par rapport au plan des hélices et la poussée perdue sont à chiffrer sur le croquis (DOU-180 « Recouvrement de la carte et des disques d'hélice »).

Sens de rotation : moteurs 1 et 3 dans le sens horaire vu de dessus, moteurs 2 et 4 dans le sens antihoraire (deux paires, chaque hélice du bon pas : 2 hélices de chaque pas) ; numérotation vue de dessus : 1 avant droit, 2 arrière droit, 3 arrière gauche, 4 avant gauche. Cette convention alimente le mixeur de DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique » ; elle est à vérifier sur la potence (DOU-167 « Orientation des axes de la centrale et sens de rotation des moteurs »).

Cotes verticales : capteur de hauteur à 20 mm du plan de contact, hauteur totale environ 35 mm. Les pieds, la hauteur exacte des poches et la position verticale de la carte sont fixés par le croquis coté de DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie » avant la commande de la pièce. Matière et fabricant (DOU-169 « Matière, masse, délai et cotes verticales des pièces imprimées ») : impression en résine par un service en ligne, masse visée 9 g pour le cadre et les anneaux (DES-014 « Feuille de calcul du bilan de masse, de poussée et d'autonomie »).
**Réalisé par :** `projets/boomrone/hardware/mecanique/cadre.scad`, `projets/boomrone/hardware/mecanique/cadre.stl`, `projets/boomrone/hardware/mecanique/verif.py`
**Statut :** Validé

### DES-007 — Circuit de puissance des moteurs
**Réfs amont :** ARC-007 « Étage de puissance des moteurs coupés par défaut »
**Description :** par moteur : un AO3400A (SOT-23) côté bas, drain sur la borne négative du moteur, source à la masse, grille reliée à la sortie TIM1 par 47 ohms, rappel de 100 kohms grille-masse ; diode SS34 en roue libre (cathode côté VBATM, anode côté drain) ; 100 nF aux bornes du moteur ; sur la ligne moteurs, 2 x 22 µF (1206, 25 V) et 100 nF. La grille est pilotée en 3,0 V (le fabricant donne 33 mohms à 2,5 V).

Calculs de contrôle : constante de décharge de la grille au reset, tau = 100 kohms x Ciss ; avec Ciss = 300 pF elle vaut 30 µs et la grille passe sous 1 V en 33 µs, avec 630 pF (valeur haute) en 69 µs, dans les deux cas très en dessous de 1 ms ; constante de commutation 47 ohms x 630 pF = 30 ns, négligeable devant la période de 41,7 µs ; perte par conduction à 2,4 A et 33 mohms : 0,19 W par MOSFET (hausse de 19 à 29 K avec 100 à 150 K/W, acceptable) ; courant de crête de la ligne 9,5 A. Pistes de puissance : voir DES-013 « Implantation, routage et fichiers de fabrication pour JLCPCB ».

Cas non couverts, testés par TI-005 « Moteurs coupés par le matériel » : MOSFET en court-circuit, pont de soudure, rappel ouvert.

![Schéma du circuit de puissance d'un moteur et tableau des quatre voies](schemas/des-007-puissance-moteurs.svg)

*Légende : circuit d'une voie, identique pour les quatre moteurs ; le tableau donne les broches et les repères de chaque voie. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ». En orange, éléments à vérifier : DOU-172 « Valeurs de configuration des périphériques à vérifier dans le manuel de référence ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (feuille « Puissance »), `projets/boomrone/schemas/des-007-puissance-moteurs.svg`
**Statut :** Validé

### DES-008 — Batterie, connecteur XT30 et entrée de la carte
**Réfs amont :** ARC-008 « Batterie et connecteur débranchable »
**Description :** batterie : LiPo 1S 850 mAh, décharge au moins 50C, sans protection, environ 19 g, résistance interne estimée 40 mohms (à mesurer), connecteur XT30 ; achetée, non conçue. XT30PW traversant sur le bord de carte, soudé à la main ; polarité marquée sur la carte (rouge au plus, noir à la masse), détrompage du connecteur seul, aucune protection contre l'inversion ni la surintensité (ARC-008 « Batterie et connecteur débranchable »). Le genre du connecteur de carte est le contraire de celui de la batterie achetée (DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion ») ; à relever avant la commande. Deux branches à partir du connecteur : VBATM (moteurs, voyant, buzzer, pont de mesure) en polygone plein, et VBATL (régulateurs) à travers la ferrite BLM18PG121SN1D, pour que le courant des moteurs ne traverse jamais la ferrite (valeur nominale de 1 A seulement : DEC-269 « Matériel : ferrite hors du chemin des moteurs, mesure en amont, rappels des sélections de bus »). Sur VBATL, 22 µF (1206, 25 V) ; sur VBATM, 2 x 22 µF de DES-007 « Circuit de puissance des moteurs ».

Calculs de contrôle : chute dans la ferrite à 130 mA avec une résistance de 0,1 ohm (ordre de grandeur, à relever DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage ») : 13 mV, sans effet sur la mesure puisque le pont lit VBATM ; résistance d'une piste de 4 mm en cuivre de 35 µm sur 30 mm : 3,7 mohms ; total connecteur, fils et pistes 15 mohms comme dans le bilan de DES-014 « Feuille de calcul du bilan de masse, de poussée et d'autonomie ». Surtension à la connexion : mesurée par TI-008 « Batterie, connecteur, chute de tension et mesure de tension ».

![Schéma de la batterie, du connecteur XT30 et de l'entrée de la carte](schemas/des-008-batterie-xt30-entree.svg)

*Légende : deux branches VBATM et VBATL, ferrite hors du chemin des moteurs. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ». En orange, éléments à vérifier : DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion » ; DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (feuille « Alimentation »), `projets/boomrone/schemas/des-008-batterie-xt30-entree.svg`
**Statut :** Validé

### DES-009 — Régulateur de 3,0 V et pont de mesure de la tension
**Réfs amont :** ARC-009 « Alimentation de la logique et mesure de la tension »
**Description :** MCP1700T-3002E/TT entre VBATL et +3V0 : 1 µF en entrée et 4,7 µF en sortie (le composant exige 1 µF au minimum en céramique ; valeurs à confirmer DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage »). Dimensionnement : 130 mA ; dissipation à 4,2 V : 1,2 V x 0,13 A = 0,16 W ; échauffement de 37 K avec 230 K/W en SOT-23 sans cuivre (40 à 55 °C annoncé, acceptable avec un petit polygone de cuivre) ; sortie réglée tant que la batterie dépasse 3,1 V. Régulateur du flux optique : DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V ».

Pont de mesure sur VBATM : 100 kohms 0,1 % (haut) et 150 kohms 0,1 % (bas), milieu vers PA0 avec 100 nF à la masse ; rapport 0,6 : 4,2 V donne 2,52 V ; courant 16,8 µA ; impédance de source 60 kohms ; pas du convertisseur 3,0 V / 4095 = 0,73 mV sur la broche, soit 1,22 mV sur la batterie. Erreur du pont à 0,1 % : environ 3 mV à 3,7 V. Séquence de conversion et formule : DES-022 « Pilote de la mesure de tension de la batterie ». Étalonnage de gain au multimètre possible, sans obligation (constante `VBAT_GAIN_TRIM` de `config_fixed.h`).

![Schéma du régulateur de 3,0 V et du pont de mesure de la tension](schemas/des-009-regulateur-3v0-pont-mesure.svg)

*Légende : MCP1700 de VBATL vers +3V0 et pont 100 kΩ / 150 kΩ de VBATM vers PA0. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ». En orange, éléments à vérifier : DOU-173 « Composants passifs et découplages à relever dans les fiches avant le routage » ; DOU-182 « Noms et numéros de broches des circuits intégrés des schémas SVG non relevés dans les fiches ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (feuille « Alimentation »), `projets/boomrone/schemas/des-009-regulateur-3v0-pont-mesure.svg`
**Statut :** Validé

### DES-010 — Circuit du bouton
**Réfs amont :** ARC-010 « Bouton »
**Description :** poussoir TS-1088-AR02016 entre un nœud et la masse ; le nœud va à PB5 par 1 kohm en série ; rappel externe de 10 kohms de PB5 au +3V0 ; 10 nF de PB5 à la masse. Constantes de temps : appui, tau = 1 kohm x 10 nF = 10 µs (le condensateur se décharge dans le contact) ; relâchement, tau = (10 kohms + 1 kohm) x 10 nF = 110 µs ; toutes deux très inférieures à l'antirebond logiciel de 10 ms (DES-028 « Gestion logicielle du bouton »). Niveau stable avant la fin du reset grâce au rappel externe (nécessaire pour l'entrée en mode réglage). Courant dans le contact : 0,27 mA. Placé sur la face haute, accessible sans retirer d'anneau.

![Schéma du circuit du bouton](schemas/des-010-bouton.svg)

*Légende : poussoir, 1 kΩ en série, rappel de 10 kΩ et 10 nF. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (feuille « Interface »), `projets/boomrone/schemas/des-010-bouton.svg`
**Statut :** Validé

### DES-011 — Circuit du voyant RGB et du buzzer
**Réfs amont :** ARC-011 « Voyant RGB et avertisseur sonore »
**Description :** voyant SZYY1615RGB-B à anode commune sur VBATM ; cathodes rouge, verte, bleue vers trois AO3400A par 120 ohms (rouge) et 68 ohms (vert et bleu) ; grilles sur PB1, PB2, PB10 par 100 ohms avec rappel de 100 kohms. Courants à 4,2 V : rouge (4,2 - 2,0) / 120 = 18,3 mA, vert et bleu (4,2 - 3,0) / 68 = 17,6 mA avec les tensions directes supposées ; avec celles du catalogue (2,4 V ; 3,4 V) 15 mA et 11,8 mA ; blanc (trois couleurs) au plus 54 mA. Si la tension directe du vert et du bleu vaut 3,4 V, ces couleurs deviennent faibles sous 3,7 V de batterie : DOU-161 « Tensions directes du voyant RGB : visibilité du vert et du bleu entre 3,4 et 3,7 V » ; la LED ou les résistances se changent avant la commande au vu des mesures de TI-009 « Bouton, voyant RGB et avertisseur ».

Buzzer actif SMD-9650-3327 entre VBATM et le drain d'un quatrième AO3400A (grille PB11, 100 ohms, rappel 100 kohms) ; diode SS34 en parallèle (cathode côté VBATM) ; courant environ 30 mA, fréquence propre 2,7 kHz, un seul timbre. Courant total le plus défavorable : 54 mA + 30 mA = 84 mA, très inférieur au courant admissible des MOSFET.

![Schéma du voyant RGB et du buzzer](schemas/des-011-voyant-buzzer.svg)

*Légende : voyant à anode commune sur VBATM, trois AO3400A, buzzer et diode de roue libre sur un quatrième AO3400A. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ». En orange, éléments à vérifier : DOU-161 « Tensions directes du voyant RGB : visibilité du vert et du bleu entre 3,4 et 3,7 V ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (feuille « Interface »), `projets/boomrone/schemas/des-011-voyant-buzzer.svg`
**Statut :** Validé

### DES-012 — Raccordement du module Bluetooth E104-BT02
**Réfs amont :** ARC-012 « Module radio Bluetooth à basse consommation »
**Description :** module E104-BT02 posé en face haute, antenne en dépassement du bord de carte, sans cuivre ni piste ni batterie dessous. Alimentation VCC au +3V0 avec 10 µF + 100 nF au plus près ; TXD du module vers PA3 (RX du microcontrôleur), RXD du module depuis PA2 (TX du microcontrôleur) ; niveaux de 3,0 V des deux côtés. Les autres broches du module sont traitées selon la fiche d'Ebyte (à relever : DOU-151 « Module E104-BT02 : débit par défaut, service, absence de commande AT », DOU-146 « Broches d'état du module Bluetooth et de mouvement du capteur de flux ») ; aucune configuration par commandes AT n'est prévue. Quatre pastilles de repli (3,0 V, masse, TX, RX) pour souder un autre module série. Débit : 9600 bauds visés, soit 104,2 µs par bit et 1,04 ms par octet ; une trame de 14 octets dure 14,6 ms ; la charge utile du protocole (DES-033 « Trames du statut sans fil, automate de réception et file d'émission »), environ 138 octets par seconde, occupe 14 % des 960 octets par seconde disponibles.

![Schéma du raccordement du module Bluetooth E104-BT02](schemas/des-012-module-bluetooth.svg)

*Légende : liaison série croisée avec PA2 et PA3, alimentation 3,0 V et plots de repli. Illustration de conception (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »), pas le schéma KiCad de fabrication ; repères provisoires : DOU-183 « Repères de composants provisoires des schémas SVG de la conception détaillée ». En orange, éléments à vérifier : DOU-151 « Module E104-BT02 : débit par défaut, service, absence de commande AT » ; DOU-146 « Broches d'état du module Bluetooth et de mouvement du capteur de flux » ; DOU-182 « Noms et numéros de broches des circuits intégrés des schémas SVG non relevés dans les fiches ».*

**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_sch` (feuille « Radio »), `projets/boomrone/schemas/des-012-module-bluetooth.svg`
**Statut :** Validé

### DES-013 — Implantation, routage et fichiers de fabrication pour JLCPCB
**Réfs amont :** ARC-013 « Carte électronique JLCPCB, câblage et assemblage » ; ARC-003 « Centrale inertielle » ; ARC-004 « Capteur de hauteur à temps de vol » ; ARC-005 « Capteur de flux optique »
**Description :** carte double face de 40 x 35 mm, épaisseur 1,0 mm, cuivre 1 oz, dessinée dans KiCad (DEC-255 « Conception détaillée : chaîne de développement et arborescence des fichiers »). Implantation : face haute, bouton, voyant, buzzer, module Bluetooth, microcontrôleur, régulateurs, XT30 et en-tête SWD ; face basse, centrale inertielle (au centre de la carte), capteur de hauteur et puce du flux, cônes de 27° et 42° non sécants (croquis coté de DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie » avant le routage). Règles de routage retenues, plus larges que le minimum de JLCPCB (0,10 mm) : pistes et espacements de signaux 0,15 mm, vias 0,3 / 0,6 mm, masse en plan plein sur les deux faces recousu par des vias, découplage à moins de 3 mm de la broche, polygones de VBATM et de masse avec au moins 8 vias entre faces, pistes de puissance de 4 mm au moins, antenne du module dégagée.

Fichiers pour la commande : gerbers et perçages (greffon KiCad pour JLCPCB), nomenclature CSV avec une colonne « LCSC Part # » (une ligne par référence, numéros de « Architecture » — `projets/boomrone/03-architecture.md`, section « Nomenclature et catalogue JLCPCB/LCSC »), fichier de placement (CPL) dont les rotations sont vérifiées dans l'aperçu de JLCPCB, panneau (4 cartes), assemblage Standard double face. Liste de contrôle avant la commande : DOU-153 « Carte double face, assemblage Standard, frais d'extension et délais » (devis), DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce » (puce du flux), DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion » (genre du XT30), DOU-156 « Vérifications avant la commande de la carte » (vérifications préalables), stocks relus le jour de la commande.
**Réalisé par :** `projets/boomrone/hardware/kicad/boomrone.kicad_pcb`, `projets/boomrone/hardware/fab/bom.csv`, `projets/boomrone/hardware/fab/cpl.csv`, `projets/boomrone/hardware/fab/verif_bom.py`
**Statut :** Validé

### DES-014 — Feuille de calcul du bilan de masse, de poussée et d'autonomie
**Réfs amont :** ARC-014 « Bilan de masse, de poussée et d'autonomie »
**Description :** script `bilan.py`, entrées dans un tableau en tête de fichier (masses et incertitudes, poussée par moteur, résistances internes, courants, tension d'armement), sorties : masse totale et incertitudes (cumulée et quadratique), rapport poussée/poids, tensions sous charge des quatre cas du bilan, énergie d'un vol de 30 s. Résultats attendus avec les entrées actuelles : masse 61,1 g, incertitude cumulée 10,1 g, quadratique 4,4 g ; rapport 88 / 61,1 = 1,44 ; tensions 3,36 V ; 3,17 V ; 3,23 V ; 2,83 V ; énergie environ 49 mAh. Le script sert à refaire le bilan après les mesures au banc et à confirmer ou infirmer R1 et R2 (DEC-253 « Seuils de batterie conservés, sans mesures au banc pour la première version » : seuils conservés pour la première version).
**Réalisé par :** `projets/boomrone/hardware/calculs/bilan.py`
**Statut :** Validé

### DES-015 — Arborescence du firmware, édition de liens et budget de mémoire
**Réfs amont :** ARC-015 « Structure logicielle et ordonnancement »
**Description :** arborescence (chemins relatifs à `projets/boomrone/firmware/`) : `src/` (`board`, `drv_*`, `est_*`, `ctl_*`, `app_*`, `main.c`, `config_fixed.h`), `src/hal/` (en-têtes de registres, accès matériel réservé à `board` et `drv_*`), `lib/uld/` (bibliothèque ST du capteur de hauteur), `linker/stm32g431cb.ld`, `startup/`, `test/` (tests unitaires du logiciel), `tools/` (scripts de vérification, DEC-270 « Vérifications par scripts : appels uniques, mémoire et jalons »), `Makefile`. Chaîne : arm-none-eabi-gcc, Cortex-M4 avec FPU simple précision matérielle, `-Os`, `-Wall -Wextra -Werror`, newlib-nano, aucun tas (le lien échoue si `malloc` est utilisé), pas de bibliothèque HAL de ST (registres CMSIS et pilotes LL, DEC-255 « Conception détaillée : chaîne de développement et arborescence des fichiers »).

Plan mémoire. Flash 128 kio à 0x08000000, 64 pages de 2 kio : code de l'application au plus 50 kio, bibliothèque du capteur de hauteur au plus 50 kio (taille à mesurer : DOU-174 « Séquence d'initialisation du flux et bibliothèque ULD : taille, appels bloquants, licence »), page 63 à 0x0801F800 réservée à la section `.settings` (8 octets utiles, DES-035 « Paramètres de vol, section d'origine et pilote de flash ») et jamais utilisée par le code. SRAM1 16 kio à 0x20000000 : `.data` et `.bss` au plus 8 kio, zone `.noinit` de 32 octets (causes de coupure, marqueur de mise sous tension), tampons DMA (IMU 2 x 16 octets, hauteur 20 octets, UART réception 128 octets circulaire, émission 8 x 14 octets) au plus 1 kio, pile de 2 kio en haut de SRAM1 avec motif de remplissage 0xDEADBEEF vérifié chaque seconde (marque haute de la pile) ; total des plafonds 11 kio, soit 69 % de SRAM1 ; SRAM2 et CCM non utilisées. Historique de hauteur de 64 cycles : 512 octets ; fenêtre d'immobilité : 200 octets.

Fichiers de constantes : `config_fixed.h` (les 29 valeurs fixes de REQ-026 « Paramètres de vol réglables », les macros d'origine des 4 paramètres, la matrice d'axes, `VBAT_GAIN_TRIM`, les constantes de capteurs de départ `K_FLOW`, `TOF_DELAY_MS`, `FLOW_SQUAL_MIN`, `TOF_SIGNAL_MIN`) et `config_ctl.h` (gains de référence de DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique ») ; ni l'un ni l'autre n'est adressable par la commande Modifier.

Séquence de démarrage : table de vecteurs, copie de `.data`, mise à zéro de `.bss` (pas de `.noinit`), appel de `board_early_init()` (moteurs coupés d'abord) puis `main()`. Le lien contient des assertions : `.settings` à 0x0801F800, fin de l'image avant cette page, `.noinit` et tampons DMA dans SRAM1.
**Réalisé par :** `projets/boomrone/firmware/Makefile`, `projets/boomrone/firmware/linker/stm32g431cb.ld`, `projets/boomrone/firmware/startup/startup_stm32g431xx.s`, `projets/boomrone/firmware/src/main.c`, `projets/boomrone/firmware/tools/check_map.py`, `projets/boomrone/firmware/test/` (fichiers `test_*.c`, `tu.h`, `mock/`)
**Statut :** Validé

### DES-016 — Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond
**Réfs amont :** ARC-015 « Structure logicielle et ordonnancement »
**Description :** structure du cycle, décidée par DEC-267 « Ordonnancement : voyant dans l'interruption du tick, flux en deux pas, tâches de fond par priorité ».

```mermaid
---
title: "Un cycle de 1 ms"
---
sequenceDiagram
    participant T as TIM6 (interruption, 1 kHz)
    participant D as DMA SPI1 (fin de transfert)
    participant M as Boucle principale
    T->>T: bouton, voyant, CS IMU bas, départ DMA (ADC déclenché par TRGO)
    D->>M: IMU lue (environ 25 µs), drapeau de cycle
    M->>M: capteurs, estimation, surveillance
    M->>M: machine à états, contrôle, sorties moteurs
    M->>M: rafraîchissement du chien de garde
    M->>M: une seule tâche de fond (au plus 200 µs)
    M->>M: attente (WFI)
```

Interruptions (priorité NVIC, 0 la plus haute) : HardFault et NMI à priorité fixe, 0 réservée aux réglages futurs, 1 sur TIM6, 2 sur la fin du DMA SPI1, 3 sur la fin du DMA I2C1 (le SPI2 du flux est scruté), 4 sur l'interruption externe de PB6 (relève TIM2 et lève un drapeau, 1 µs), 5 sur l'USART2 (ligne au repos : drapeau « radio »). Durées en µs de TIM2 ; aucune attente active de plus de 100 µs hors initialisation (le pas B du flux scrute 72 µs).

Cycle sans dépendre du DMA : l'interruption TIM6 lève elle-même le drapeau de cycle si la lecture précédente n'est pas finie (le DMA est alors abandonné, une erreur de bus est comptée, trois erreurs de suite lèvent `imu_failed`), si bien que la surveillance et le chien de garde tournent même si la centrale ne répond plus (DEC-271 « Cycle indépendant du DMA de la centrale et lecture armée après l'initialisation »). La lecture automatique n'est armée (`imu_streaming`) qu'à la fin de l'initialisation de la centrale (DES-018 « Pilote de la centrale inertielle ») ; avant, l'interruption ne fait que le bouton et le voyant.

Boucle principale (pseudo-code) : attendre le drapeau de cycle ; si le drapeau précédent n'avait pas été consommé, incrémenter `missed_cycles` ; `t0` = TIM2 ; lire l'IMU et l'ADC (DES-018 « Pilote de la centrale inertielle », DES-022 « Pilote de la mesure de tension de la batterie ») ; estimation (DES-023 « Filtre d'attitude de Mahony » à DES-025 « Vitesse horizontale et critères d'immobilité, de platitude et de stationnaire ») ; surveillance (DES-029 « Surveillance et coupures automatiques ») ; machine à états (DES-027 « Machine à états : données, événements et table de transitions ») ; contrôle et sorties (DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique », DES-021 « Pilotes des moteurs, du voyant, du buzzer et de la liaison série ») ; marquer `cycle_ran` ; rafraîchissement du chien de garde (DES-030 « Chien de garde matériel et règle de rafraîchissement ») ; une tâche de fond ; durée = TIM2 - `t0` ; mise à jour du maximum, `overrun` si la durée dépasse 800 µs.

Tâches de fond, par priorité décroissante : 1 arrêt radio, 2 capteur de hauteur (drapeau levé par PB6, environ 30 Hz), 3 flux optique (drapeau levé tous les 10 cycles), 4 statut (toutes les 500 ms et à chaque changement d'état) et variables (toutes les 100 ms moteurs en marche), 5 effets (tous les 10 cycles). Chaque tâche est une petite machine à états dont un pas dure au plus 200 µs. Charge des pas par seconde : flux 100 x 2, hauteur 30 x 3, variables 10 x 2, statut 2 x 2, effets 100, soit environ 420 pas sur 1000 cycles : un pas de priorité inférieure attend au plus 20 cycles (critère de TU-016 « Ordonnanceur : choix de la tâche de fond, cycles manqués et durées »). Le voyant (modulation de luminosité) n'est pas une tâche : il tourne dans l'interruption TIM6 (moins de 1 µs). Budget du cycle repris de ARC-015 « Structure logicielle et ordonnancement » : contrôle environ 100 µs, plafond 300 µs, tâche de fond 200 µs, alarme à 800 µs.
**Réalisé par :** `projets/boomrone/firmware/src/main.c`, `projets/boomrone/firmware/src/app_sched.c`, `projets/boomrone/firmware/src/app_sched.h`
**Statut :** Validé

### DES-017 — Coupure des moteurs, démarrage unique et gestionnaires d'exception
**Réfs amont :** ARC-015 « Structure logicielle et ordonnancement » ; ARC-007 « Étage de puissance des moteurs coupés par défaut » ; ARC-019 « Machine à états du drone »
**Description :** `motors_cut()` exécute, dans cet ordre et sans attente : (1) effacer MOE de TIM1 (sorties libérées, les rappels de 100 kohms tiennent les grilles à l'état bas) ; (2) arrêter le compteur de TIM1 ; (3) reconfigurer PA8 à PA11 en sortie à l'état bas (écriture BSRR puis MODER) ; (4) enregistrer l'appel dans un compteur. Elle est idempotente, utilisable depuis une interruption, et dure environ 2 µs. `motors_start()` existe une seule fois, avec deux sites d'appel (ARC-019 « Machine à états du drone ») : le relâchement armé plus 200 ms, et la commande Décoller acceptée ; elle remet les broches en fonction alternative, charge les comparateurs à 0 et valide MOE et le compteur.

Gestionnaires : `HardFault_Handler`, `MemManage_Handler`, `BusFault_Handler`, `UsageFault_Handler` et `Default_Handler` appellent `motors_cut()`, inscrivent « défaut fatal » en `.noinit`, puis bouclent sans rafraîchir le chien de garde (reset environ 100 ms nominal, 112 ms au pire, DES-030 « Chien de garde matériel et règle de rafraîchissement »). `NMI_Handler` lit FLASH_ECCR : si le bit de double erreur ECCD est levé, il l'efface et lève le drapeau `flash_ecc_error` (non fatal, utile à la lecture des réglages, DES-035 « Paramètres de vol, section d'origine et pilote de flash ») ; sinon il traite l'exception comme fatale. Le contrôle des deux sites d'appel de `motors_start()` est fait par un script (DEC-270 « Vérifications par scripts : appels uniques, mémoire et jalons »).
**Réalisé par :** `projets/boomrone/firmware/src/drv_motor.c`, `projets/boomrone/firmware/src/fault.c`, `projets/boomrone/firmware/tools/check_calls.py`
**Statut :** Validé

### DES-018 — Pilote de la centrale inertielle
**Réfs amont :** ARC-016 « Pilotes des capteurs et des sorties » ; ARC-003 « Centrale inertielle » ; ARC-023 « Initialisation et échec d'initialisation »
**Description :** données : `imu_raw_t` (gyroscope x, y, z, accéléromètre x, y, z en `int16`, température, instant TIM2 de la fin de lecture) et `imu_sample_t` (vitesses angulaires en rad/s, accélérations en m/s², instant en µs, repère du drone). Lecture : à chaque tick, l'interruption TIM6 abaisse CS (PA4) et lance le DMA SPI1 de 15 octets (commande 0xA0 = 0x80 | 0x20, puis 14 octets de température, gyroscope et accéléromètre) ; la fin du DMA remonte CS, relève TIM2 et lève le drapeau de cycle ; durée 15 x 8 / 5,3125 MHz = 22,6 µs. Si le DMA n'est pas fini au tick suivant, l'interruption compte une erreur, abandonne la lecture et force le cycle (DES-016 « Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond »). Une centrale figée est détectée par 10 lectures brutes identiques de suite, comptées comme une erreur par cycle suivant. La lecture n'est armée (`imu_streaming`) qu'après l'initialisation. Anti-repliement : DOU-179 « Anti-repliement de la centrale : sortie à 3,33 kHz lue à 1 kHz ». Conversion : vitesse angulaire = brut x 0,070 °/s x pi/180, moins le biais ; accélération = brut x 0,244 mg x 9,80665 ; matrice d'axes constante (DES-003 « Raccordement de la centrale inertielle LSM6DSO », DOU-167 « Orientation des axes de la centrale et sens de rotation des moteurs »). Échantillon répété : deux lectures identiques de suite incrémentent `repeat_count` (diagnostic, pas une erreur) ; trois erreurs consécutives lèvent `imu_failed` (consommé par DES-029 « Surveillance et coupures automatiques »), une lecture correcte (non figée) remet le compteur à zéro. Fonction `imu_calibrate_bias()` : moyenne de 1000 échantillons à l'initialisation (DES-031 « Séquence d'initialisation et échec d'initialisation »). Séquence d'initialisation : reset logiciel, attente de la fin (au plus 20 ms), contrôle de WHO_AM_I, écriture des registres de DES-003 « Raccordement de la centrale inertielle LSM6DSO ».
**Réalisé par :** `projets/boomrone/firmware/src/drv_imu.c`, `projets/boomrone/firmware/src/drv_imu.h`, `projets/boomrone/firmware/src/drv_imu_regs.h`
**Statut :** Validé

### DES-019 — Pilote du capteur de hauteur non bloquant
**Réfs amont :** ARC-004 « Capteur de hauteur à temps de vol » ; ARC-016 « Pilotes des capteurs et des sorties » ; ARC-023 « Initialisation et échec d'initialisation »
**Description :** machine à états du pilote, avec les niveaux de reprise de ARC-004 « Capteur de hauteur à temps de vol » :

```mermaid
---
title: "Pilote du capteur de hauteur : pas de la tâche de fond"
---
stateDiagram-v2
    [*] --> Attente
    Attente --> Lecture: front de GPIO1 (instant TIM2 relevé)
    Lecture --> Acquittement: fin du DMA I2C (17 octets)
    Acquittement --> Attente: écriture 0x0086, mesure publiée
    Lecture --> Niveau1: NACK ou dépassement de 3 ms
    Niveau1 --> Lecture: relance
    Niveau1 --> Niveau2: deuxième échec de suite
    Niveau2 --> Attente: 9 impulsions sur SCL, bus libre
    Niveau2 --> Niveau3: bus toujours bloqué
    Niveau3 --> Attente: XSHUT et ULD (au sol seulement)
```

Données : `tof_meas_t` = distance brute en mm (`uint16`), code d'état de la mesure, taux de signal, instant TIM2 du front, drapeau `valid`. Pas 1 : la tâche voit le drapeau de PB6, lance en DMA l'écriture de l'index 0x0089 puis la lecture de 17 octets et rend la main (moins de 20 µs) ; pas 2 (fin du DMA) : décoder le bloc de résultat (état, distance, taux de signal, selon la structure de résultats de l'ULD, DOU-149 « Valeurs de registres du VL53L1X à vérifier dans la bibliothèque ST (ULD) »), puis lancer l'écriture de 1 dans 0x0086 (acquittement) en DMA ; pas 3 : publier. Mesure valide si le code d'état est « portée valide », le taux de signal au moins égal à `TOF_SIGNAL_MIN` (valeur de départ 0,5 Mcps, provisoire, DOU-160 « Mesure de hauteur valide et sols sombres ou brillants ») et la distance entre 40 et 3000 mm. Niveau 2 : 9 impulsions sur SCL, une par pas de tâche de fond (10 µs), puis réinitialisation du périphérique I2C. L'état Attente a un délai de garde de 100 ms : sans front de GPIO1 pendant ce temps, relecture du registre d'état puis niveau 1. Le niveau 3 (XSHUT et ULD, bloquant de 170 à 650 ms) n'est jamais lancé moteurs en marche ; il n'est lancé qu'à l'initialisation et au sol moteurs coupés, avec rafraîchissement du chien de garde entre les attentes (DOU-158 « Initialisation du capteur de hauteur plus longue que le chien de garde »). La bibliothèque ULD n'est appelée qu'à ces deux endroits (DOU-174 « Séquence d'initialisation du flux et bibliothèque ULD : taille, appels bloquants, licence »). Pour la coupure d'atterrissage (DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique », état Atterrissage seulement), une lecture brute (valide ou non) d'au plus 45 mm, ou un état « hors portée » dont la dernière valeur valide était au plus 60 mm, vaut contact (la fenêtre de validité de 40 mm est étroite à 500 mm/s : DEC-272 « Coupure d'atterrissage tolérante à la fenêtre de validité du capteur de hauteur »). `tof_last_valid_us` alimente la coupure à 200 ms de DES-029 « Surveillance et coupures automatiques ».
**Réalisé par :** `projets/boomrone/firmware/src/drv_tof.c`, `projets/boomrone/firmware/src/drv_tof.h`, `projets/boomrone/firmware/lib/uld/`
**Statut :** Validé

### DES-020 — Pilote du flux optique
**Réfs amont :** ARC-005 « Capteur de flux optique » ; ARC-016 « Pilotes des capteurs et des sorties » ; ARC-023 « Initialisation et échec d'initialisation »
**Description :** initialisation (au sol, bloquante, avec rafraîchissement du chien de garde entre les écritures) : remise à zéro par écriture de 0x5A dans 0x3A, attente de 5 ms, lecture des registres 0x02 à 0x06 pour les vider, contrôle de l'identité (registre 0x00 égal à 0x49 et registre 0x5F égal à 0xB6, valeurs de mémoire à confirmer dans la fiche), suite d'écritures de réglage d'une cinquantaine de registres (provenance et licence à établir : DOU-174 « Séquence d'initialisation du flux et bibliothèque ULD : taille, appels bloquants, licence »), puis attente de 50 ms avant la première mesure valide ; entre deux écritures, 45 µs au moins (temporisation de la fiche). Échec d'identité : échec d'initialisation (DEC-264 « Initialisation : centrale inertielle ou flux optique absent vaut échec d'initialisation »).

Lecture en vol à 100 Hz en deux pas de tâche de fond : pas A : CS bas, envoi de l'adresse du registre de rafale (0x16), attente de 40 µs bornée par TIM2 (en tout moins de 60 µs) ; pas B : lecture de 12 octets (96 bits à 1,328 MHz, 72 µs), CS haut (au repos au moins 500 ns avant la lecture suivante). Les 12 octets (mouvement, observation, delta x et delta y sur 16 bits, qualité de surface SQUAL, somme des pixels, maximum, minimum, obturateur sur 2 octets) donnent `flow_meas_t` = delta x, delta y (`int16`), SQUAL, instant TIM2, drapeau `valid` (SQUAL au moins `FLOW_SQUAL_MIN`, 30 au départ ; l'absence de mouvement donne des deltas nuls, donc une vitesse nulle valide : un drone immobile ne rend pas le flux invalide, DEC-273 « Flux optique : l'absence de mouvement est une vitesse nulle valide »). Les deltas s'accumulent dans la puce entre deux lectures : aucune perte si une lecture est retardée ; le pas de temps est la différence des instants de deux lectures, et l'âge d'un échantillon se compte depuis la dernière lecture réussie, mouvement ou non. Un pas qui dépasse 200 µs est abandonné et compté en erreur.
**Réalisé par :** `projets/boomrone/firmware/src/drv_flow.c`, `projets/boomrone/firmware/src/drv_flow.h`, `projets/boomrone/firmware/src/drv_flow_init.h`
**Statut :** Validé

### DES-021 — Pilotes des moteurs, du voyant, du buzzer et de la liaison série
**Réfs amont :** ARC-016 « Pilotes des capteurs et des sorties »
**Description :** moteurs : `motor_set(const float duty[4])` limite chaque rapport cyclique à [0 ; 1] et charge TIM1->CCRx = rapport x 7083 (arrondi vers le bas) ; `motor_cmd8()` rend la commande sur 0 à 255 pour la télémétrie ; rapport 0 donne un comparateur à 0 (sortie à l'état bas). Voyant : `led_set(r, v, b)` avec des niveaux de 0 à 10 ; `led_tick()` (appelée par l'interruption TIM6, phase de 0 à 9) met chaque sortie à 1 quand son niveau est supérieur à la phase (écritures BSRR), soit une période de 10 ms et 100 Hz ; niveau 0 éteint, niveau 10 allumé en permanence. Buzzer : `buzzer_set(bool)` sur PB11. Liaison série : USART2 8N1 à 9600 bauds, réception en DMA circulaire de 128 octets avec interruption de ligne au repos, `uart_rx_pop()` qui rend l'octet suivant à partir de l'index de queue en lisant l'index de tête du DMA (128 - compteur), détection de dépassement (drapeau ORE effacé et compteur) et de rattrapage de la queue par la tête ; émission en DMA normal, `uart_tx_start(buf, n)` refusé si une émission est en cours (`uart_tx_busy()`).
**Réalisé par :** `projets/boomrone/firmware/src/drv_motor.c`, `projets/boomrone/firmware/src/drv_led.c`, `projets/boomrone/firmware/src/drv_buzzer.c`, `projets/boomrone/firmware/src/drv_uart.c`
**Statut :** Validé

### DES-022 — Pilote de la mesure de tension de la batterie
**Réfs amont :** ARC-009 « Alimentation de la logique et mesure de la tension » ; ARC-016 « Pilotes des capteurs et des sorties »
**Description :** ADC1 en 12 bits, horloge synchrone HCLK/4 (42,5 MHz), temps d'échantillonnage 640,5 cycles (15,1 µs, supérieur aux 6 µs exigés par l'impédance de source de 60 kohms) ; séquence de 14 rangs déclenchée par le tick (TRGO de TIM6) : 10 conversions de PA0 (canal 1) puis 4 conversions de la référence interne VREFINT (canal 18), DMA vers un tampon de 14 mots ; durée 14 x 15,4 µs = 216 µs, résultats lus au tick suivant. Calcul : `vdda` = 3,0 V x VREFINT_CAL / moyenne des 4 mesures de VREFINT (VREFINT_CAL est la valeur d'usine à l'adresse 0x1FFF75AA, mesurée à 3,0 V) ; `vpin` = moyenne des 10 mesures x `vdda` / 4095 ; `vbat_V` = `vpin` x 250 / 150 x `VBAT_GAIN_TRIM` (rapport du pont de DES-009 « Régulateur de 3,0 V et pont de mesure de la tension »). Garde-fous : la tension utilisée pour normaliser les moteurs est limitée à [3,0 V ; 4,3 V] ; une moyenne de VREFINT nulle ou une tension brute hors [2,0 V ; 5,0 V] rend `vbat_valid` faux (pas de division par zéro) ; budget d'erreur estimé ±15 mV à 3,7 V, ondulation des moteurs non comprise, à confirmer à TI-008 « Batterie, connecteur, chute de tension et mesure de tension » (DOU-181 « Bilan d'erreur de la mesure de tension et niveau du BOR »). Sorties : `vbat_cycle` (par tick) et `vbat_100ms` (moyenne glissante de 100 valeurs). Drapeau `vbat_valid` faux jusqu'à la première séquence complète (environ 2 ms après le démarrage) ; si une séquence n'est pas terminée au tick suivant, la valeur précédente est conservée et `adc_stale` s'incrémente. Valeurs d'exemple : 4,2 V donne 2,52 V sur la broche, soit 3440 pas environ avec `vdda` = 3,0 V ; VREFINT nominale 1,212 V, soit environ 1654 pas à 3,0 V (valeurs de mémoire, DOU-172 « Valeurs de configuration des périphériques à vérifier dans le manuel de référence »).
**Réalisé par :** `projets/boomrone/firmware/src/drv_adc.c`, `projets/boomrone/firmware/src/drv_adc.h`
**Statut :** Validé

### DES-023 — Filtre d'attitude de Mahony
**Réfs amont :** ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse »
**Description :** état : quaternion unitaire q = (w, x, y, z), vitesse angulaire filtrée. À chaque cycle, avec dt = écart des instants TIM2 de deux échantillons, borné à [0,5 ms ; 5 ms] : (1) poids de l'accéléromètre `wa` = max(0, 1 - |norme / g - 1| / 0,5), donc 1 à 1 g et 0 sous 0,5 g ou au-delà de 1,5 g ; (2) direction de la gravité estimée v = (2(x z - w y), 2(w x + y z), w² - x² - y² + z²) ; (3) erreur e = a_unitaire x v (produit vectoriel), nulle si la norme de a est nulle ; (4) vitesse corrigée = gyroscope + Kp x `wa` x e, avec Kp = 2,0 s⁻¹ au sol et 0,3 s⁻¹ moteurs en marche (en vol l'accéléromètre mesure la poussée, pas la gravité : DOU-177 « Filtre d'attitude : l'accéléromètre en vol mesure la poussée, pas la gravité »), sans terme intégral (le biais est mesuré à l'initialisation, DES-031 « Séquence d'initialisation et échec d'initialisation ») ; (5) q <- q + 0,5 q (0, vitesse corrigée) dt, puis normalisation par 1/racine (FPU). Initialisation : q déduit de l'accélération moyenne mesurée à l'initialisation (lacet nul). Sorties : cosinus d'inclinaison `tilt_cos` = w² - x² - y² + z² (inclinaison = arccos), vecteur de gravité dans le repère du drone v, vitesse angulaire filtrée par un filtre du premier ordre à 0,3 (environ 57 Hz à 1 kHz). Coût estimé 25 µs (budget de ARC-015 « Structure logicielle et ordonnancement »). Constantes de départ marquées provisoires (DEC-261 « Estimation : filtre de Mahony, observateur de hauteur et compensation du retard », DEC-260 « Gains de référence et constantes de départ provisoires »).
**Réalisé par :** `projets/boomrone/firmware/src/est_attitude.c`, `projets/boomrone/firmware/src/est_attitude.h`
**Statut :** Validé

### DES-024 — Observateur de hauteur et de vitesse verticale
**Réfs amont :** ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse »
**Description :** état (h, v) en m et m/s. Prédiction à chaque cycle : a_z = troisième ligne de la matrice de rotation du repère du drone vers le monde appliquée à l'accélération mesurée, moins g ; h <- h + v dt + 0,5 a_z dt² ; v <- v + a_z dt. À la fin de chaque cycle, après la correction éventuelle, l'état estimé est recopié dans un historique circulaire de 64 cycles. Mise à jour à chaque mesure valide du capteur de hauteur (30 Hz) : hauteur mesurée h_m = (distance brute - 20 mm) x `tilt_cos` (rejetée si `tilt_cos` < 0,5) ; retard k = (instant courant - instant du front) arrondi au ms, plus `TOF_DELAY_MS` (33 ms au départ, DOU-170 « Constantes de capteurs de départ : échelle du flux, retard du capteur de hauteur, filtres »), rejetée si k > 63 ; innovation e = h_m - h_historique(k) ; correction de l'état courant h <- h + 0,396 e et v <- v + 1,188 e (gains L1 = 12 s⁻¹ et L2 = 36 s⁻² multipliés par la période de 33 ms). Anomalies : si |e| > 0,5 m, la mesure est ignorée, sauf à la troisième de suite où l'état est recalé (h = h_m, v = 0 ; limite connue juste après un lancer rapide : DOU-170 « Constantes de capteurs de départ : échelle du flux, retard du capteur de hauteur, filtres »). État initial : première mesure valide, sinon 0. Résultat de simulation de contrôle (rampe de 1 m/s, bruit de 10 mm sur la hauteur et de 0,2 m/s² sur l'accélération, retard de 33 ms) : erreur maximale d'environ 9 cm pendant la rampe, 3 cm en régime (DEC-261 « Estimation : filtre de Mahony, observateur de hauteur et compensation du retard »).
**Réalisé par :** `projets/boomrone/firmware/src/est_hauteur.c`, `projets/boomrone/firmware/src/est_hauteur.h`
**Statut :** Validé

### DES-025 — Vitesse horizontale et critères d'immobilité, de platitude et de stationnaire
**Réfs amont :** ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse »
**Description :** vitesse horizontale : à chaque mesure valide du flux, vitesse angulaire apparente = delta x ou delta y x `K_FLOW` / pas de temps ; moins la vitesse angulaire du gyroscope sur l'axe correspondant (signes à vérifier à TI-004 « Flux optique et vitesse horizontale ») ; fois la distance le long de l'axe optique = h / `tilt_cos` ; filtre du premier ordre à 0,3 à 100 Hz. `K_FLOW` = 0,0021 rad par pas (valeur de départ de mémoire, à étalonner : DOU-170 « Constantes de capteurs de départ : échelle du flux, retard du capteur de hauteur, filtres »). La résolution d'un pas est d'environ 0,21 m/s à 1 m de hauteur et 100 Hz (DOU-175 « Résolution de la vitesse horizontale du flux face au seuil de 0,3 m/s »). La vitesse est invalide si h < 0,08 m, si la qualité du flux est faible, si l'inclinaison dépasse 30° ou si le dernier échantillon date de plus de 50 ms (DEC-262 « Vitesse horizontale invalide : stationnaire non déclaré »).

Critères (calculés à chaque cycle) : à plat si `tilt_cos` >= cos 15° = 0,9659 ; immobile si la norme de la vitesse angulaire filtrée est au plus 30 °/s (0,5236 rad/s) et si, dans une fenêtre de 50 échantillons de la norme de l'accélération pris à 100 Hz (0,5 s), le maximum et le minimum sont à moins de 0,5 m/s² de la moyenne (DEC-263 « Critère d'immobilité : fenêtre de 50 échantillons à 100 Hz ») ; stationnaire si à plat, hauteur h >= 0,3 m, vitesse horizontale valide d'au plus 0,3 m/s avec une vitesse verticale d'au plus 0,3 m/s (norme combinée : lecture de REQ-007 « Critère de vol stationnaire » à valider à la porte, DOU-175 « Résolution de la vitesse horizontale du flux face au seuil de 0,3 m/s »), et ceci pendant 10 cycles consécutifs. Vitesse horizontale invalide : le critère de stationnaire est faux.
**Réalisé par :** `projets/boomrone/firmware/src/est_vitesse.c`, `projets/boomrone/firmware/src/est_criteres.c`, `projets/boomrone/firmware/src/est_criteres.h`
**Statut :** Validé

### DES-026 — Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique
**Réfs amont :** ARC-018 « Boucle de contrôle du vol »
**Description :** commandes exprimées en fraction de poussée (1,0 = poussée maximale d'un moteur à 3,7 V). Valeurs de départ provisoires, non issues de mesures (DEC-260 « Gains de référence et constantes de départ provisoires », DOU-171 « Gains de référence, poussée de sustentation et linéarisation de la poussée ») :

| Constante | Valeur de départ | Rôle |
|---|---|---|
| `K_ANG` | 6 s⁻¹ (consigne de vitesse limitée à 12 rad/s) | erreur d'angle vers vitesse angulaire demandée |
| `KP_RATE`, `KI_RATE`, `KD_RATE` (roulis, tangage) | 0,04 ; 0,02 ; 0,0006 | PID de vitesse angulaire (intégrale limitée à 0,1) |
| `KP_YAW`, `KI_YAW` | 0,02 ; 0,01 | vitesse de lacet visée nulle |
| `T_HOVER` | 0,69 | poussée de sustentation (1 / 1,44 du bilan) |
| `KP_H`, `KD_H`, `KI_H` | 0,5 par m ; 0,3 par m/s ; 0,1 par (m·s) (intégrale limitée à 0,15) | hauteur |
| `K_V` | 0,2 rad par m/s (inclinaison limitée à 10°) | amortissement de la vitesse horizontale |
| `V_REF` | 3,7 V | normalisation par la tension |

Le gain d'inclinaison (paramètre réglable) multiplie `K_ANG` seul (borne haute 2,0 : la boucle d'angle double sans que la boucle de vitesse angulaire bouge) ; le gain de hauteur multiplie `KP_H`, `KD_H` et `KI_H`. Erreurs d'angle de roulis et de tangage tirées du vecteur de gravité dans le repère du drone (atan2 sur les composantes y, z et x, z, valable dans toute orientation, signes à vérifier sur la potence : TI-013 « Boucle de contrôle sur potence »). Hauteur : poussée collective = `T_HOVER` + `KP_H` (h_cible - h) - `KD_H` v + intégrale, divisée par max(`tilt_cos`, 0,5) ; cibles : hauteur visée en Stabilisation et Stationnaire, rampe descendante à la vitesse de descente en Atterrissage (départ à la hauteur estimée), coupure quand la lecture brute est au plus 45 mm ou selon la règle de contact de DES-019 « Pilote du capteur de hauteur non bloquant » (ARC-018 « Boucle de contrôle du vol »). Vitesse horizontale valide : consigne d'inclinaison = -`K_V` x vitesse sur chaque axe (repère du drone).

Mixeur en X (numérotation de DES-006 « Cadre, anneaux, moteurs et hélices ») : poussée du moteur i = collectif + a_i roulis + b_i tangage + c_i lacet, avec (a, b, c) = moteur 1 (-1, -1, +1), moteur 2 (-1, +1, -1), moteur 3 (+1, +1, +1), moteur 4 (+1, -1, -1). Si un moteur dépasse 1 ou passe sous 0, le collectif est décalé pour garder l'écart entre moteurs (priorité à l'attitude) ; si l'écart seul ne tient pas, il est réduit proportionnellement. Conversion : rapport cyclique = racine(poussée limitée à [0 ; 1]) x `V_REF` / `vbat_cycle`, limité à [0 ; 1] (DEC-259 « Contrôle : poussée linéarisée, mixeur en X et priorité à l'attitude »). Démarrage : rampe linéaire de 20 ms sur le rapport cyclique après `motors_start()`.
**Réalisé par :** `projets/boomrone/firmware/src/ctl_attitude.c`, `projets/boomrone/firmware/src/ctl_hauteur.c`, `projets/boomrone/firmware/src/ctl_mixer.c`, `projets/boomrone/firmware/src/ctl_phases.c`, `projets/boomrone/firmware/src/config_ctl.h`
**Statut :** Validé

### DES-027 — Machine à états : données, événements et table de transitions
**Réfs amont :** ARC-019 « Machine à états du drone » ; ARC-024 « Effets locaux (logiciel) » ; ARC-025 « Protocole et service du statut sans fil »
**Description :** `app_fsm.c`, fonction `fsm_step(const fsm_in_t*)` appelée une fois par cycle. États : énumération dont les valeurs sont les numéros de REQ-020 « Statut sans fil » (1 Allumé à 17 Délai de descente dépassé) plus `S_INIT` = 0. Données : `fsm_t` = état, instant d'entrée, instant de départ des moteurs, drapeau « vol de réglage », cause de refus, cause de coupure, instant du relâchement armé. Entrées `fsm_in_t` : événement du bouton (DES-028 « Gestion logicielle du bouton »), niveau filtré du bouton, événements de surveillance (DES-029 « Surveillance et coupures automatiques »), commande radio acceptée (DES-034 « Mode réglage, filtrage des commandes et vol de réglage »), critères (DES-025 « Vitesse horizontale et critères d'immobilité, de platitude et de stationnaire »), état de la batterie, instant courant. Ordre de traitement par cycle : sous-tension, bouton, commande Arrêt, le reste (ARC-019 « Machine à états du drone »). Les transitions sont exactement celles du tableau de « Architecture » — `projets/boomrone/03-architecture.md` (section « Machine à états : transitions »), codées en `switch` par état avec des gardes ; à chaque changement d'état, `btn_set_ignore_if_pressed()` pose le drapeau d'appui en cours. États événements (5, 7, 12, 13 à 17) : le code est publié à l'entrée (DES-033 « Trames du statut sans fil, automate de réception et file d'émission »), l'état suivant est pris au cycle d'après. Effets : états 1 vers effet 1, 3 vers 2, 6 vers 3, 8 à 11 vers 4, 2 vers 9, 4 vers 10 en effet de base ; événements 5 vers 6, 7 vers 7, 12 vers 5, 13 à 17 vers 8, superposés (DES-032 « Effets locaux : table, séquenceur de lumière et de son »). Actions : `motors_start()` aux deux sites d'appel, `motors_cut()` pour toute coupure (en premier), écriture de la cause en `.noinit`. Un Lancé de plus de 500 ms sans moteurs ne rafraîchit plus le chien de garde (DES-030 « Chien de garde matériel et règle de rafraîchissement »).
**Réalisé par :** `projets/boomrone/firmware/src/app_fsm.c`, `projets/boomrone/firmware/src/app_fsm.h`
**Statut :** Validé

### DES-028 — Gestion logicielle du bouton
**Réfs amont :** ARC-020 « Gestion logicielle du bouton »
**Description :** `btn_isr_sample(level)` appelée par l'interruption TIM6 : compteur d'échantillons identiques, niveau filtré modifié quand le compteur atteint 10 (10 ms). Événements dérivés du niveau filtré dans la boucle principale : appui, relâchement, passages à 1,0 s, 2,0 s et 10,0 s depuis l'appui initial (instants TIM2, constantes de `config_fixed.h`). Drapeau `ignore_until_release` : posé par `btn_set_ignore_if_pressed()` à chaque changement d'état, il supprime tous les événements jusqu'au premier relâchement filtré. Garde de 500 ms à partir du relâchement armé : les fronts sont supprimés, l'antirebond continue, et si le niveau filtré est bas à la fin de la garde l'événement `BTN_LOW_AFTER_GUARD` est émis (coupure au cycle suivant) ; pas de garde en vol de réglage. À l'initialisation : `btn_held_since_poweron()` est vrai si le niveau filtré est bas dès la première valeur filtrée (10 ms après le départ) et n'est jamais remonté pendant l'initialisation. Délai de l'arrêt d'urgence : antirebond de 10 ms plus un cycle, environ 12 ms.
**Réalisé par :** `projets/boomrone/firmware/src/app_button.c`, `projets/boomrone/firmware/src/app_button.h`
**Statut :** Validé

### DES-029 — Surveillance et coupures automatiques
**Réfs amont :** ARC-021 « Surveillance et coupures automatiques » ; ARC-015 « Structure logicielle et ordonnancement » ; ARC-016 « Pilotes des capteurs et des sorties »
**Description :** `safety_step()` à chaque cycle avant le contrôle, produit au plus un événement par cycle selon la priorité : sous-tension, coupure demandée par le bouton (via la machine à états), arrêt radio, puis les autres. Sous-tension : compteur de cycles ; sous 3,30 V le compteur augmente, entre 3,30 V et 3,35 V il est conservé, à 3,35 V et plus il est remis à zéro ; à 100 le compteur déclenche l'événement (coupure environ 105 ms après le début du creux) ; actif dans tous les états dès que `vbat_valid` est vrai (DEC-258 « Mesure de la tension : séquence de conversion et zone de maintien de la sous-tension »). Armement : `safety_ready()` évalue au moment des 2,0 s d'appui, par ordre de priorité des causes de refus : batterie (`vbat_100ms` < 3,70 V), mouvement (non immobile), pas à plat (inclinaison supérieure à 15°). Coupures en vol : « stationnaire non atteint » à 2,0 s du démarrage des moteurs sans critère de stationnaire vrai ; « basculement » si `tilt_cos` < 0,5 (60°) pendant 100 cycles, seulement après le stationnaire (états 10 et 11) ; « délai de descente » à 15,0 s après le début de l'atterrissage (en vol de réglage, après le décollage) ; « échec de stabilisation » si `imu_failed` ou si aucune mesure de hauteur valide depuis 200 ms moteurs en marche (DOU-140 « Défaut de capteur en vol : cause et effet rattachés à l'échec de stabilisation ») ; arrêt sans fil traité au cycle suivant la trame. Rattachement aux 17 états : « stationnaire non atteint », `imu_failed` et l'absence de mesure de hauteur donnent tous l'état 13 et le code de coupure 1 « échec de stabilisation ». Le délai de 2,0 s est le même en vol de réglage (seul le maintien du stationnaire passe de 10 s à 3 s). Chaque coupure appelle `motors_cut()`, écrit la cause en `.noinit` (avec contrôle de validité, DES-033 « Trames du statut sans fil, automate de réception et file d'émission ») puis signale l'événement à la machine à états.
**Réalisé par :** `projets/boomrone/firmware/src/app_safety.c`, `projets/boomrone/firmware/src/app_safety.h`
**Statut :** Validé

### DES-030 — Chien de garde matériel et règle de rafraîchissement
**Réfs amont :** ARC-022 « Chien de garde »
**Description :** IWDG avec prédiviseur 8 sur l'oscillateur LSI de 32 kHz (4 kHz) et rechargement 399, soit 100 ms nominal (±10 % de dispersion supposée) ; gelé quand le débogueur arrête le cœur (DBGMCU). Une seule fonction écrit la clé de rafraîchissement : `wdg_refresh(reason)`. En fin de cycle, elle n'écrit que si (1) `cycle_ran` est vrai (puis il est remis à zéro) et (2) l'état Lancé dure moins de 500 ms (TIM2). Elle est aussi appelée avant et après une écriture de flash, et à chaque étape de l'initialisation (DES-031 « Séquence d'initialisation et échec d'initialisation ») et de l'initialisation du capteur de hauteur (DES-019 « Pilote du capteur de hauteur non bloquant »). Pire cas de détection : cycle manquant environ 112 ms après le dernier rafraîchissement ; phase Lancé coupée environ 612 ms après le relâchement. Cause du reset : lue dans RCC_CSR au démarrage (drapeaux IWDG, BOR, broche NRST), mémorisée puis effacée ; elle sert à DES-031 « Séquence d'initialisation et échec d'initialisation ». Les HardFault ne rafraîchissent pas (DES-017 « Coupure des moteurs, démarrage unique et gestionnaires d'exception »).
**Réalisé par :** `projets/boomrone/firmware/src/drv_wdg.c`, `projets/boomrone/firmware/src/app_wdg.c`
**Statut :** Validé

### DES-031 — Séquence d'initialisation et échec d'initialisation
**Réfs amont :** ARC-023 « Initialisation et échec d'initialisation »
**Description :** `app_init()` exécute les étapes suivantes, chacune appelant `wdg_refresh(INIT)` ; durées estimées (somme 1,8 s typique et environ 2,3 s au pire avec 650 ms pour le capteur de hauteur, pour 3,0 s exigées par REQ-017 « Initialisation en 3 secondes ») :

```mermaid
---
title: "Séquence d'initialisation : durées estimées"
---
gantt
    dateFormat  X
    axisFormat %s
    section Étapes
    Horloges, moteurs coupés, cause de reset (1 ms)      :a, 0, 1
    Centrale inertielle (30 ms)                          :b, 1, 31
    Capteur de hauteur ULD (170 ms, au plus 650 ms)      :c, 31, 201
    Flux optique (60 ms)                                 :d, 201, 261
    Attente (500 ms)                                     :e, 261, 761
    Biais du gyroscope et tests (1000 ms)                :f, 761, 1761
    Réglages et décision (5 ms)                          :g, 1761, 1766
```

*Légende : abscisse en millisecondes (axe gradué en secondes par le moteur de rendu).* Étapes : (1) lire la cause de reset et valider le marqueur `.noinit` (mise sous tension reconnue si le marqueur est absent ou invalide, ou si le drapeau de coupure d'alimentation ou de brown-out du reset est levé : mise sous tension, causes remises à zéro, marqueur posé) ; (2) horloges, broches moteurs à l'état bas ; (3) pilote de la centrale ; (4) bouton lu ; (5) capteur de hauteur : au plus 2 tentatives de 300 ms avec remise à zéro par XSHUT, échec déclaré avant 1 s ; (6) flux optique ; (7) attente de 0,5 s (l'ADC démarre, `vbat_valid` devient vrai) ; (8) 1000 échantillons (biais accepté seulement s'il est au plus 3 °/s par axe, sinon échec « mouvement ») : biais du gyroscope, moyenne de l'accélération (attitude initiale), tests d'immobilité (norme angulaire sous 30 °/s et fenêtre d'accélération, DES-025 « Vitesse horizontale et critères d'immobilité, de platitude et de stationnaire ») et d'inclinaison (15°), norme de l'accélération entre 0,8 g et 1,2 g ; (9) charge des réglages (DES-035 « Paramètres de vol, section d'origine et pilote de flash ») ; (10) décision par priorité : échec (REQ-037 « Comportement en échec d'initialisation ») si absence de la centrale, du flux ou du capteur de hauteur (DEC-264 « Initialisation : centrale inertielle ou flux optique absent vaut échec d'initialisation »), mouvement, pas à plat, chute libre ou sous-tension (moins de 3,3 V pendant 100 cycles, DES-029 « Surveillance et coupures automatiques ») ; sinon mode réglage si `btn_held_since_poweron()` et mise sous tension reconnue (marqueur absent) ; sinon Allumé ; drapeau d'appui en cours posé si le bouton est enfoncé. En échec : moteurs jamais armés, bouton et commandes ignorés ; pour l'échec par sous-tension, capteurs en veille et voyant au niveau 1 sur 10, horloge inchangée à 170 MHz (DEC-274 « Échec par sous-tension : horloge conservée à 170 MHz », DOU-178 « Horloge à 16 MHz de l'échec par sous-tension abandonnée », DOU-118 « Seuil de protection et consommation résiduelle du drone laissé allumé »). Aucun statut radio avant la fin de l'étape 10.
Absence de la centrale ou du flux : DEC-264 « Initialisation : centrale inertielle ou flux optique absent vaut échec d'initialisation », DOU-168 « Centrale inertielle ou flux optique absent à l'initialisation ».
**Réalisé par :** `projets/boomrone/firmware/src/app_init.c`, `projets/boomrone/firmware/src/app_init.h`
**Statut :** Validé

### DES-032 — Effets locaux : table, séquenceur de lumière et de son
**Réfs amont :** ARC-024 « Effets locaux (logiciel) »
**Description :** table de 10 lignes en constantes (`effect_t` : niveaux R, V, B de 0 à 10, période de clignotement en ms (0 = fixe), rapport 50 %, motif sonore = nombre de bips, durée d'un bip, pause de 100 ms) : 1 Allumé (0, 10, 0 fixe, aucun son) ; 2 Appui validé (0, 10, 10 fixe, 1 bip de 100 ms) ; 3 Prêt (0, 10, 0 période 250 ms, 2 bips de 100 ms) ; 4 Lancé et vol (10, 10, 10 fixe, aucun son) ; 5 Posé (0, 0, 10 fixe, 1 bip de 250 ms) ; 6 Refus (10, 10, 0 période 250 ms, 3 bips de 100 ms) ; 7 Désarmement (10, 0, 10 fixe, 2 bips de 250 ms) ; 8 Coupure en vol (10, 0, 0 fixe, 1 bip de 500 ms) ; 9 Échec d'initialisation (1, 0, 0 période 1000 ms, 1 bip de 500 ms) ; 10 Mode réglage (0, 0, 10 période 1000 ms, 1 bip de 200 ms). Moteur : `effects_set_base(n)` fixe l'effet de base ; `effects_event(n)` superpose l'effet pendant 1,0 s (les événements 5, 6, 7, 8) puis revient à la base, un nouvel événement remplaçant l'ancien ; la tâche `effects_task()` tourne tous les 10 ms (ordonnanceur, DES-016 « Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond ») et calcule les niveaux (clignotement, séquence de bips). Son : jamais moteurs en marche ; le son d'un événement est repoussé jusqu'à 300 ms après la coupure ; le son est joué une seule fois à l'entrée de l'effet. La teinte du blanc et du cyan varie avec la décharge (anode sur la batterie) : essai à 3,4 V (DOU-133 « Forme des dix effets locaux : lumière, son, distinction mesurable »).
**Réalisé par :** `projets/boomrone/firmware/src/app_effects.c`, `projets/boomrone/firmware/src/app_effects.h`
**Statut :** Validé

### DES-033 — Trames du statut sans fil, automate de réception et file d'émission
**Réfs amont :** ARC-025 « Protocole et service du statut sans fil »
**Description :** format commun : `0xA5`, type, charge (longueur fixe par type), CRC8 (polynôme 0x07, valeur initiale 0, sans inversion) calculé sur le type et la charge ; entiers de plus d'un octet en petit-boutiquier (poids faible d'abord). Types et charges : 0x01 statut = état (1 octet, 1 à 17), dernière cause de refus (1), dernière cause de coupure (1), 4 paramètres en `uint16` (gain d'inclinaison x 1000, gain de hauteur x 1000, hauteur visée en mm, vitesse de descente en mm/s) soit 14 octets de trame ; 0x02 variables = hauteur en mm (`int16`), inclinaison en 0,1° (`int16`), 4 commandes moteur (`uint8`, 0 à 255) soit 11 octets ; 0x10 Décoller, 0x11 Arrêt, 0x13 Sauvegarder = charge vide (3 octets) ; 0x12 Modifier = identifiant (0 à 3 : gain d'inclinaison, gain de hauteur, hauteur visée, vitesse de descente) et valeur `uint16` (6 octets). Causes de refus : 0 aucune, 1 batterie faible, 2 drone en mouvement, 3 drone pas à plat, 4 bouton enfoncé. Causes de coupure : 0 aucune, 1 échec de stabilisation, 2 arrêt par le bouton, 3 arrêt sans fil, 4 basculement, 5 délai de descente dépassé, 6 sous-tension. Vecteurs de référence (trames complètes en hexadécimal) : Arrêt `A5 11 77` ; Décoller `A5 10 70` ; Sauvegarder `A5 13 79` ; Modifier identifiant 0 valeur 1000 `A5 12 00 E8 03 A9` ; statut en état 1, sans cause, paramètres d'origine `A5 01 01 00 00 E8 03 E8 03 E8 03 C8 00 D5` ; variables hauteur 1000 mm, inclinaison 3,5°, moteurs à 179 `A5 02 E8 03 23 00 B3 B3 B3 B3 D4` ; CRC8 de la chaîne « 123456789 » égal à 0xF4. Ces vecteurs sont dans `firmware/test/vecteurs_trames.txt`, lus par le test C et par le script de suivi (DES-036 « Logiciel de suivi en Python »).

Automate de réception : états attente de 0xA5, type, charge, CRC ; un type inconnu ou un CRC faux fait rejouer les octets déjà reçus après le 0xA5 (le module peut couper ou fusionner les trames) ; une trame partielle est abandonnée après 50 ms de silence. Lecture déclenchée par l'interruption de ligne au repos, tâche de priorité 1 (DES-016 « Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond »), commande Arrêt exécutée au cycle suivant (au plus 5 ms après la fin de la trame côté drone). Émission : file de 8 trames de 14 octets ; le statut remplace un statut déjà en attente ; si la file est pleine, la plus ancienne trame de variables est abandonnée ; une trame est lancée quand `uart_tx_busy()` est faux. Causes mémorisées dans `.noinit` : marqueur de 32 bits, deux octets de cause, CRC8 ; à la mise sous tension, RAM invalide donc causes à zéro ; après un reset du chien de garde, les causes sont conservées.
Choix de format : DEC-265 « Protocole sans fil : octets, codes de cause, file d'émission et réception ».
**Réalisé par :** `projets/boomrone/firmware/src/app_proto.c`, `projets/boomrone/firmware/src/app_proto.h`, `projets/boomrone/firmware/src/app_radio.c`, `projets/boomrone/firmware/test/vecteurs_trames.txt`
**Statut :** Validé

### DES-034 — Mode réglage, filtrage des commandes et vol de réglage
**Réfs amont :** ARC-026 « Mode réglage et vol de réglage » ; ARC-025 « Protocole et service du statut sans fil » ; ARC-027 « Paramètres de vol et stockage des réglages »
**Description :** `tuning_accept(etat, commande)` applique le tableau de REQ-023 « Commandes sans fil selon l'état du drone » (source unique, copié dans une table de 18 lignes (états 0 à 17) x 4 commandes ; état 2 : tout ignoré). Décoller : accepté en état 4 si `vbat_100ms` >= 3,70 V et si le niveau du bouton n'est pas bas (REQ-041 « Conditions d'acceptation de la commande Décoller ») ; sinon état 5 avec la cause (batterie, puis bouton), retour à l'état 4. Décoller accepté : drapeau « réglage » levé, `motors_start()` immédiat (sans délai de 200 ms ni état Lancé), état 9. Vol de réglage : mêmes critères et mêmes phases, stationnaire de 3,0 s, pas de garde du bouton, Arrêt et bouton coupent, Modifier acceptée, Sauvegarder ignorée ; la perte du lien n'a aucun effet. Fin du vol : retour à l'état 4 sans verrouillage, sauf sous-tension (état 2). Modifier avec un identifiant supérieur à 3 : trame ignorée, aucun effet (REQ-026 « Paramètres de vol réglables »). Modifier : `param_set(id, valeur)` (DES-035 « Paramètres de vol, section d'origine et pilote de flash ») saturée aux bornes, appliquée au cycle suivant. Sauvegarder : `param_save()` en état 4 seulement, batterie d'au moins 3,5 V ; en état 2 toute commande est ignorée (REQ-037 « Comportement en échec d'initialisation »).
**Réalisé par :** `projets/boomrone/firmware/src/app_tuning.c`, `projets/boomrone/firmware/src/app_tuning.h`
**Statut :** Validé

### DES-035 — Paramètres de vol, section d'origine et pilote de flash
**Réfs amont :** ARC-027 « Paramètres de vol et stockage des réglages »
**Description :** `params_t` = 4 `uint16` (gain d'inclinaison x 1000, gain de hauteur x 1000, hauteur visée en mm, vitesse de descente en mm/s) = un mot de 64 bits. Valeurs d'origine : 1000, 1000, 1000, 200 (macros `PARAM_ORIGIN_*` de `config_fixed.h`). Bornes : gains 500 à 2000, hauteur 500 à 1200, vitesse de descente 150 à 500. Les 29 valeurs fixes de REQ-026 « Paramètres de vol réglables » sont des `#define` de `config_fixed.h` (bouton : 10 ms, 1 s, 2 s, 10 s, 0,5 s, 50 ms, 200 ms ; départ : 30 °/s, 0,5 m/s², 15°, 3,7 V ; stationnaire : 15°, 0,3 m/s, 0,3 m ; coupures : 2,0 s, 60°, 0,1 s, 15,0 s, 100 ms ; batterie : 3,3 V, 100 ms, 250 ms ; blocages : 200 ms, 500 ms ; vol : 10 s, 3 s, 0,5 m/s, 2 à 3 cm ; initialisation 3 s), jamais adressables par `param_set` ; un script les compare à la liste de l'exigence (TU-035 « Paramètres et flash : bornes, valeurs d'origine, séquence de sauvegarde »). Section `.settings` (8 octets alignés) à 0x0801F800, initialisée par l'éditeur de liens avec les macros d'origine : le ST-LINK qui programme l'image écrit donc les valeurs d'origine (REQ-028 « Valeurs d'origine après la programmation »).

`param_load()` : met à zéro `flash_ecc_error`, lit le mot, vérifie le drapeau (le gestionnaire NMI de DES-017 « Coupure des moteurs, démarrage unique et gestionnaires d'exception » l'a peut-être levé), puis valide chaque champ ; un champ hors bornes devient sa valeur d'origine (une page vierge donne donc les valeurs d'origine, jamais un gain maximal) ; erreur ECC : les quatre valeurs d'origine (DEC-266 « Réglages : origine en double dans le code et lecture protégée contre l'erreur ECC »). `param_set(id, v)` : saturation aux bornes. `param_save()` : refusée si la batterie est sous 3,5 V ou si le drone n'est pas en mode réglage au sol ; sinon rafraîchir le chien de garde, déverrouiller la flash, effacer la page 63 (22 à 40 ms), programmer le mot de 64 bits, attendre la fin, verrouiller, relire et comparer, rafraîchir ; durée environ 45 ms ; échec compté. Aucune somme de contrôle (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »).
**Réalisé par :** `projets/boomrone/firmware/src/app_params.c`, `projets/boomrone/firmware/src/app_params.h`, `projets/boomrone/firmware/src/drv_flash.c`, `projets/boomrone/firmware/src/config_fixed.h`, `projets/boomrone/firmware/tools/check_fixed.py`
**Statut :** Validé

### DES-036 — Logiciel de suivi en Python
**Réfs amont :** ARC-028 « Logiciel d'essai de l'appareil de suivi »
**Description :** script `suivi.py` (Python 3.11 ou plus, bibliothèque `bleak`). Modules internes : `Parser` (même automate que DES-033 « Trames du statut sans fil, automate de réception et file d'émission », mêmes vecteurs de test), `Link` (connexion au module par nom ou adresse ; identifiants de service et de caractéristique passés en options `--service` et `--char`, à relever sur le module : DOU-151 « Module E104-BT02 : débit par défaut, service, absence de commande AT » ; réception par notifications, envoi sans réponse découpé en morceaux de 20 octets), `Display` (affichage console rafraîchi cinq fois par seconde : état en code et nom, causes de refus et de coupure en clair, quatre paramètres, hauteur, inclinaison, commandes moteur, trames par seconde, erreurs de CRC), `Journal` (fichier CSV horodaté pour mesurer les fréquences de REQ-020 « Statut sans fil » et REQ-021 « Variables du vol »), `Keys` (d Décoller, a Arrêt, m Modifier avec saisie de l'identifiant et de la valeur, s Sauvegarder, q quitter). Option `--simu` : drone simulé en bouclage (envoie statuts et variables à 2 Hz et 10 Hz, répond aux commandes) pour tester le script sans module.
**Réalisé par :** `projets/boomrone/tools/suivi.py`, `projets/boomrone/tools/test_suivi.py`
**Statut :** Validé

### DES-037 — Jalons de livraison et configurations de compilation
**Réfs amont :** ARC-029 « Plan de livraison par jalons »
**Description :** option de compilation `JALON` = 1, 2 ou 3, utilisée dans le `Makefile` (cibles `j1`, `j2`, `j3`) et dans `config_jalon.h`. Jalon 1 (vol normal) : `main`, `board`, tous les pilotes sauf `drv_flash` en écriture, estimation, contrôle, bouton, surveillance, machine à états, effets, chien de garde, initialisation ; les quatre paramètres sont des constantes aux valeurs d'origine ; `motors_start()` a un seul site d'appel. Jalon 2 : ajoute `app_proto` et `app_radio` ; la machine à états ne reçoit que Arrêt, les autres commandes sont ignorées. Jalon 3 : ajoute `app_tuning`, `param_save()`, le vol de réglage et le second site d'appel de `motors_start()`. Chaque jalon compile sans les modules suivants (remplacés par des fonctions vides dans `stubs_jalon.c`) et a son test d'intégration (TI-025 « Livraison par jalons »).
**Réalisé par :** `projets/boomrone/firmware/Makefile`, `projets/boomrone/firmware/src/config_jalon.h`, `projets/boomrone/firmware/src/stubs_jalon.c`
**Statut :** Validé

### DES-038 — Contenu de la page de consignes d'emploi
**Réfs amont :** ARC-030 « Page de consignes d'emploi »
**Description :** la page « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md` tient sur une face A4, 60 lignes au plus (48 aujourd'hui). À ajouter ou vérifier, une ligne ou deux chacune : (1) après un échec d'initialisation ou une sous-tension, débrancher la batterie ; (2) programmer hélices démontées et sans relier le 3,3 V du ST-LINK à la carte ; (3) hélices de 45 mm et anneaux obligatoires ; (4) un drone laissé branché se décharge en profondeur (consigne « débrancher ») ; (5) et (6), proposés et non exigés par l'architecture : mentionner la marge de batterie faible (DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie ») et la hauteur minimale de lancer de 1,5 m (REQ-006 « Stabilisation après le lancer »). Les points (1) à (4) sont ceux de ARC-030 « Page de consignes d'emploi » ; aucune nouvelle exigence.
**Réalisé par :** `projets/boomrone/consignes-emploi.md`, `projets/boomrone/firmware/tools/check_consignes.py`
**Statut :** Validé

<!-- Ajouter les éléments ci-dessous, au même format, en dehors des blocs de code. -->
