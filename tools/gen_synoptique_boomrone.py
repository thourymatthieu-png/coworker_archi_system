"""Génère le synoptique de la carte Boomrone (SVG).

Usage : python tools/gen_synoptique_boomrone.py projets/boomrone/schemas/synoptique-boomrone.svg
Les repères (J1, U1 à U7, Q1 à Q8...) sont ceux du projet KiCad proj_boomrone.
"""
import sys

W, H = 2000, 1280
o = []
C = dict(bat="#dc2626", l3="#2563eb", l2="#9333ea", sig="#059669", ser="#0891b2", gnd="#374151", warn="#d97706")


def a(s):
    o.append(s)


def t(x, y, s, col="#1f2937", size=12, anchor="start", bold=False):
    b = ' font-weight="bold"' if bold else ""
    a(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{col}"{b}>{s}</text>')


def box(x, y, w, h, title, sub=(), fill="#f8fafc", tw=14):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="#1f2937" stroke-width="1.8"/>')
    t(x + w / 2, y + 20, title, size=tw, anchor="middle", bold=True)
    for i, s in enumerate(sub):
        t(x + w / 2, y + 38 + i * 15, s, size=12, anchor="middle")


def line(pts, col, w=2.4, dash=None, arrow=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#ar_{arrow})"' if arrow else ""
    p = " ".join(f"{x},{y}" for x, y in pts)
    a(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="{w}"{d}{m} stroke-linejoin="round"/>')


def dot(x, y, col):
    a(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{col}"/>')


def zone(x, y, w, h, title, col):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{col}" fill-opacity="0.06" '
      f'stroke="{col}" stroke-width="1.5" stroke-dasharray="7 5"/>')
    t(x + 10, y + 18, title, col, 13, bold=True)


a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'font-family="Segoe UI,Arial,sans-serif">')
a('<title>Synoptique de la carte Boomrone</title><defs>')
for k, c in C.items():
    a(f'<marker id="ar_{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
      f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
a('</defs><rect width="100%" height="100%" fill="#ffffff"/>')

t(30, 38, "Boomrone — Synoptique de la carte (drone de poche, 100 g au plus)", size=24, bold=True)
t(30, 60, "Carte unique double face 40 × 35 mm, fabriquée et assemblée par JLCPCB · STM32G431 à 170 MHz, "
          "cycle de contrôle 1 kHz · vue d'ensemble de DES-001 « Schéma par blocs, réseaux et domaines de tension de la carte »",
  size=12, col="#4b5563")

# ------------------------------------------------------------------ extérieur
zone(20, 85, 250, 1150, "EXTÉRIEUR DE LA CARTE", "#6b7280")
box(40, 120, 210, 90, "Batterie LiPo 1S 850 mAh", ["3,1 à 4,2 V · 50C au moins", "sans protection · ~19 g", "connecteur XT30"])
box(40, 650, 210, 80, "ST-LINK", ["programmation du firmware", "liaison SWD (pas d'USB)"])
box(40, 760, 210, 80, "Ordinateur / téléphone", ["logiciel d'essai Python", "Bluetooth basse consommation"])
box(40, 870, 210, 70, "Utilisateur", ["appui bouton · voit le voyant", "entend le buzzer"])
box(40, 970, 210, 70, "Sol survolé", ["vu par U3 (hauteur)", "et U4 (flux optique)"])
box(40, 1070, 210, 70, "Cadre imprimé 3D", ["4 anneaux tangents", "hélices de 45 mm"])

# ------------------------------------------------------------------ carte
zone(290, 85, 1700, 1150, "CARTE ÉLECTRONIQUE 40 × 35 mm — un bloc = une feuille hiérarchique KiCad", "#1f2937")

# --- alimentation
zone(310, 110, 800, 335, "ALIMENTATION", C["bat"])
box(345, 160, 100, 70, "J1", ["XT30PW", "DES-008"])
line([(250, 195), (345, 195)], C["bat"], 3.4)
dot(325, 195, C["bat"])
t(255, 182, "VBATM", C["bat"], 10, bold=True)
line([(445, 195), (900, 195)], C["bat"], 3.4)
t(460, 185, "VBATM  3,1 à 4,2 V · crête 9,5 A pendant 2 s", C["bat"], 13, bold=True)
dot(480, 195, C["bat"])
line([(480, 195), (480, 259), (500, 259)], C["bat"], 2.6)
box(500, 230, 110, 58, "FB1", ["ferrite 120 Ω", "DES-008"])
line([(610, 259), (650, 259)], C["bat"], 2.6)
t(612, 250, "VBATL", C["bat"], 11, bold=True)
t(500, 306, "22 µF en tête de VBATL", C["bat"], 11)
box(650, 230, 140, 58, "U5  MCP1700", ["LDO 3,0 V · DES-009"])
line([(790, 259), (1130, 259)], C["l3"], 3.4)
t(800, 250, "+3V0  (130 mA dimensionné)", C["l3"], 13, bold=True)
dot(1050, 259, C["l3"])
line([(1050, 259), (1050, 300)], C["l3"], 2.6)
box(1000, 300, 100, 58, "U6  XC6206", ["LDO 2,0 V", "DES-005"], tw=13)
line([(1050, 358), (1050, 395), (1100, 395)], C["l2"], 3)
t(1000, 380, "+2V0", C["l2"], 12, anchor="end", bold=True)
t(1000, 396, "≈ 9 mA vers U4", C["l2"], 11, anchor="end")
dot(900, 195, C["bat"])
line([(900, 195), (900, 330)], C["bat"], 2.4)
box(840, 330, 120, 70, "Pont diviseur", ["100 kΩ / 150 kΩ", "DES-009"], tw=13)
t(970, 420, "VBAT_SENSE vers PA0 (ADC)", C["sig"], 11)
t(330, 330, "Masse unique : plan plein", C["gnd"], 12, bold=True)
t(330, 348, "Points d'essai : +3V0, +2V0, VBATM, VBATL, GND ×2", C["gnd"], 11)
t(330, 364, "Aucune protection contre l'inversion ni la surintensité", C["warn"], 11)
t(330, 380, "Batterie sous charge : jusqu'à 3,17 V (marginal, DOU-135)", C["warn"], 11)

# --- actionneurs
zone(310, 470, 800, 755, "ACTIONNEURS : alimentés en VBATM, pilotés par MOSFET AO3400A côté bas", C["bat"])
# tronc VBATM
line([(325, 195), (325, 1190)], C["bat"], 3.4)
t(333, 1005, "VBATM", C["bat"], 12, bold=True)
rows = [510, 630, 750, 870]
for i, y in enumerate(rows):
    n = i + 1
    box(360, y, 150, 90, f"M{n}  moteur 8520", ["à balais", "hélice de 45 mm", "SS34 + 100 nF"], tw=13)
    dot(325, y + 45, C["bat"])
    line([(325, y + 45), (360, y + 45)], C["bat"], 2.6)
    box(590, y, 150, 90, f"Q{n}  AO3400A", [f"grille ← M{n}_G (PA{8 + i})", "47 Ω série · 100 kΩ rappel", "DES-007"], tw=13)
    line([(510, y + 45), (590, y + 45)], C["bat"], 2.6)
    t(515, y + 38, "drain", C["bat"], 10)
    line([(1120, y + 45), (740, y + 45)], C["sig"], 2.6, arrow="sig")
    t(930, y + 38, f"M{n}_G  PWM TIM1", C["sig"], 11, anchor="middle")
# tronc de commande
line([(1160, 390), (1120, 390), (1120, 1010)], C["sig"], 2.6)
dot(1120, 390, C["sig"])
# voyant + buzzer
line([(325, 1190), (870, 1190)], C["bat"], 3.4)
box(360, 1030, 280, 140, "LED1  voyant RGB SZYY1615RGB-B",
    ["anode commune sur VBATM", "Q5, Q6, Q7 ← LED_R/G/B (PB1, PB2, PB10)",
     "120 Ω rouge, 68 Ω vert et bleu", "15 à 18 mA par couleur · DES-011"], tw=13)
box(670, 1030, 200, 140, "BZ1  buzzer actif",
    ["SMD-9650-3327 · 3,3 V · 30 mA", "80 dB à 10 cm · 2 700 Hz", "Q8 ← BUZ (PB11)", "DES-011"], tw=13)
line([(500, 1190), (500, 1170)], C["bat"], 2.6)
line([(770, 1190), (770, 1170)], C["bat"], 2.6)
dot(500, 1190, C["bat"])
dot(770, 1190, C["bat"])
line([(1120, 1010), (500, 1010), (500, 1030)], C["sig"], 2.6, arrow="sig")
line([(770, 1010), (770, 1030)], C["sig"], 2.6, arrow="sig")
dot(770, 1010, C["sig"])

# --- microcontrôleur et ses voisins
zone(1130, 110, 430, 1115, "MICROCONTRÔLEUR ET PÉRIPHÉRIQUES", C["l3"])
box(1160, 150, 360, 260, "U1  STM32G431CBT6",
    ["Cortex-M4F 170 MHz · LQFP-48 · 128 Ko de flash",
     "cycle 1 kHz · machine à états unique (18 états)",
     "chien de garde matériel de 100 ms · BOR",
     "SPI1 · SPI2 · I²C1 · USART2 · TIM1 · ADC1",
     "SWD (PA13, PA14) · NRST · BOOT0 (PB8)",
     "DES-002 · découplage de VDD et VDDA"], fill="#eff6ff", tw=17)
line([(1130, 259), (1160, 259)], C["l3"], 3.4)
t(1165, 428, "Sorties de TIM1 (PA8 à PA11) vers les grilles Q1 à Q4 : bloc ACTIONNEURS", C["sig"], 11)
# tronc de signaux à droite
line([(1520, 300), (1535, 300), (1535, 1075)], C["sig"], 2.6)
dot(1535, 300, C["sig"])

zone(1150, 445, 390, 335, "CAPTEURS (face basse)", C["sig"])
sens = [(470, "U2  LSM6DSO · centrale inertielle", ["accéléromètre + gyroscope 3 axes", "SPI1 PA4–PA7 (5,3 MHz) · INT1 PB0 · DES-003"], C["sig"]),
        (555, "U3  VL53L1CX · hauteur par temps de vol", ["fiable dès 40 mm · I²C1 PA15/PB7", "XSHUT PB9 · GPIO1 PB6 · DES-004"], C["sig"]),
        (640, "U4  PMW3901MB · flux optique", ["dérive horizontale · SPI2 PB12–PB15 (1,33 MHz)", "VDD 2,0 V · VDDIO 3,0 V · lentille collée · DES-005"], C["sig"])]
for y, ti, su, c in sens:
    box(1170, y, 330, 70, ti, su, tw=13)
    line([(1500, y + 35), (1535, y + 35)], c, 2.4)
    dot(1535, y + 35, c)
t(1170, 735, "Alimentés en +3V0 (U4 : VDD en +2V0 et VDDIO en +3V0).", C["l3"], 11)
t(1170, 751, "Coupure des moteurs à 2–3 cm du sol (lecture brute ≈ 45 mm).", C["warn"], 11)

zone(1150, 795, 390, 190, "RADIO", C["ser"])
box(1170, 825, 330, 90, "U7  PB-03F (Ai-Thinker)",
    ["PHY6252 · Bluetooth 5.2 · antenne sur le module", "USART2 : PA2 → RXD (P10), TXD (P9) → PA3", "115 200 bauds · DES-012"], tw=14)
line([(1500, 870), (1542, 870), (1542, 350), (1520, 350)], C["ser"], 2.6, arrow="ser")
t(1170, 940, "Microprogramme d'origine, aucune commande envoyée :", C["warn"], 11)
t(1170, 956, "à essayer seul avant la commande (DOU-200).", C["warn"], 11)
t(1170, 972, "Antenne en dépassement du bord de carte (DOU-204).", C["warn"], 11)

zone(1150, 1000, 390, 215, "INTERFACES LOCALES", "#9333ea")
box(1170, 1030, 330, 60, "SW1  bouton", ["PB5 · rappel 10 kΩ · RC antirebond · DES-010"], tw=13)
box(1170, 1105, 330, 60, "J2  en-tête SWD 1×5", ["VTref · SWDIO (PA13) · SWCLK (PA14) · GND · NRST"], tw=13)
line([(1500, 1060), (1535, 1060)], C["sig"], 2.4)
dot(1535, 1060, C["sig"])
line([(1500, 1135), (1548, 1135), (1548, 380), (1520, 380)], C["gnd"], 2.4, dash="6 4", arrow="gnd")
t(1170, 1190, "Entrée en mode réglage : bouton tenu à la mise sous tension.", C["gnd"], 11)
t(1170, 1206, "Un reset du MCU coupe les moteurs (rappel de grille à la masse).", C["gnd"], 11)

# --- liens extérieur -> carte (flèches de principe)
def stub(y, label, col, dash=None, both=False):
    a(f'<polyline points="250,{y} 292,{y}" fill="none" stroke="{col}" stroke-width="2.4"'
      f'{" stroke-dasharray=\"6 4\"" if dash else ""} marker-end="url(#ar_{col_name[col]})"'
      f'{" marker-start=\"url(#ar_" + col_name[col] + ")\"" if both else ""}/>')
    t(271, y - 14, label, col, 11, anchor="middle", bold=True)


col_name = {v: k for k, v in C.items()}
stub(690, "SWD", C["gnd"], dash=True)
stub(800, "BLE", C["ser"], both=True)
stub(905, "SW1", C["sig"])
stub(1005, "mesure", C["warn"])
stub(1105, "fixé", C["gnd"], dash=True)

# --- légende
zone(1580, 110, 400, 700, "LÉGENDE ET CHIFFRES CLÉS", "#6b7280")
items = [("VBATM / VBATL (batterie)", C["bat"], None), ("+3V0 (logique)", C["l3"], None),
         ("+2V0 (flux optique)", C["l2"], None), ("Signaux SPI, I²C, GPIO, PWM", C["sig"], None),
         ("Liaison série U1 ↔ U7", C["ser"], None), ("Programmation SWD, liens extérieurs", C["gnd"], "6 4"),
         ("Point d'attention", C["warn"], None)]
for i, (lab, c, d) in enumerate(items):
    line([(1600, 150 + i * 24), (1650, 150 + i * 24)], c, 3, dash=d)
    t(1660, 154 + i * 24, lab, size=12)
t(1595, 350, "Chiffres clés", size=13, bold=True)
facts = ["Masse 61 g pour 100 g permis · poussée/poids 1,44",
         "Logique : 130 mA · moteurs : 9,5 A en crête (2 s)",
         "Batterie sous charge jusqu'à 3,17 V : marginal",
         "Moteurs coupés par défaut (rappel de grille)",
         "Hauteur : fiable dès 40 mm (U3)",
         "Flux optique : dérive horizontale (U4)",
         "18 états logiciels · cycle 1 kHz · chien de garde 100 ms"]
for i, s in enumerate(facts):
    t(1595, 372 + i * 19, "• " + s, size=12)
t(1595, 530, "Fabrication", size=13, bold=True)
for i, s in enumerate(["JLCPCB pose les puces et le module radio.", "À la main : XT30, bouton, lentille du flux.",
                       "Carte 40 × 35 mm, 1,0 mm, double face."]):
    t(1595, 552 + i * 19, "• " + s, size=12)
t(1595, 630, "Points d'essai (TP1 à TP11)", size=13, bold=True)
for i, s in enumerate(["+3V0, +2V0, VBATM, VBATL, GND ×2,", "M1_D, BLE_TX, BLE_RX, TOF_GPIO1,", "plus 6 plots de repli du flux optique."]):
    t(1595, 652 + i * 19, s, size=12)
t(1595, 730, "Un diagramme par bloc : feuilles DES-002 à DES-012", size=12, col="#4b5563")
t(1595, 748, "du projet KiCad (DES-006 : mécanique, hors carte).", size=12, col="#4b5563")

t(30, 1268, "Illustration de conception, pas le schéma de fabrication. Sources : « Conception détaillée » — projets/boomrone/04-conception-detaillee.md "
            "et « Architecture » — projets/boomrone/03-architecture.md.", size=11, col="#6b7280")
a("</svg>")
open(sys.argv[1], "w", encoding="utf8").write("\n".join(o))
