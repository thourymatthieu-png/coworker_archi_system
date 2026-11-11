"""Génère rapport-simulation-spice.html (autonome, images incluses) à partir des mesures de resultats/metriques.json."""
import base64, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
m = json.loads((HERE / "resultats" / "metriques.json").read_text())
timing = json.loads((HERE / "resultats" / "timing.json").read_text())
(HERE / "metriques.json").write_text(json.dumps(m, indent=1))
(HERE / "timing.json").write_text(json.dumps(timing, indent=1))


def img(name, alt):
    b = base64.b64encode((HERE / "figures" / name).read_bytes()).decode()
    return f'<figure><img alt="{alt}" src="data:image/png;base64,{b}"><figcaption>{alt}</figcaption></figure>'


def v(x, n=3):
    return f"{x:.{n}f}".replace(".", ",")


def mv(x):
    return f"{x*1e3:.0f}".replace(".", ",")


def c1(load, tool="ngspice"):
    return m[f"cas1/{load}/{tool}"]


n_tran = sum(1 for k in timing if k.startswith("cas") and k.endswith("_ngspice"))
n_net = len(list((HERE / "netlists").glob("*.cir")))
tot_ng = sum(x["s"] for k, x in timing.items() if k.startswith("cas") and k.endswith("_ngspice"))
tot_lt = sum(x["s"] for k, x in timing.items() if k.startswith("cas") and k.endswith("_LTspice"))
hand = {"vol": 3.36, "crete": 3.17, "pess": 2.83}

rows1 = ""
for load, titre in (("vol", "Stationnaire nominal — 5,5 A, 55 mΩ"), ("vol_dec", "Stationnaire, PWM décalées de 90°"),
                    ("crete", "Crête après lancer — 9,5 A, 55 mΩ"), ("pess", "Stationnaire pessimiste — 7,5 A, 110 mΩ")):
    a, b = c1(load), c1(load, "LTspice")
    rows1 += (f"<tr><td>{titre}</td><td>{v(a['ibat_moy'],2)}</td><td>{v(a['vbm_moy'])}</td><td>{v(hand[load],2) if load in hand else '—'}</td>"
              f"<td>{v(a['vbm_min_lisse'])}</td><td><b>{v(a['vbm_pp_lisse'],2)}</b></td><td>{v(a['vbm_pp'],2)} / {v(b['vbm_pp'],2)}</td></tr>")

ma, mb = m["cas2/vol/ngspice"], m["cas2/vol/LTspice"]
rows2 = ""
for load, titre in (("vol", "Stationnaire nominal"), ("crete", "Crête (9,5 A)"), ("pess", "Pessimiste (7,5 A, 110 mΩ)")):
    a = m[f"cas2/{load}/ngspice"]
    rows2 += (f"<tr><td>{titre}</td><td>{v(a['vbl_min'])}</td><td>{v(a['v3_moy'],3)}</td><td>{v(a['v3_min'],3)}</td>"
              f"<td>{mv(a['vbl_h1'])}</td><td>{v(a['v3_h1']*1e3,2)}</td><td>{v(a['v3_pp']*1e3,1)}</td></tr>")

st = m["stab"]


def pmrow(key, nom):
    s = st[key]
    return f"<tr><td>{nom}</td><td>{v(s['fu']/1e3,0)} kHz</td><td>{v(s['pm'],0)}°</td></tr>"


psr = m["psrr"]
dm_c, dm_d = m["dromax/crete/ngspice"], m["dromax/demarrage/ngspice"]
c3 = m["cas3/vol/ngspice"]
fa, fb = m["fin/vol/ngspice"], m["fin/vol/LTspice"]
ca = c1("vol")

html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Simulation SPICE Boomrone</title>
<style>
:root{{--bg:#fbfbfa;--fg:#1d2330;--mut:#5d6677;--card:#fff;--line:#e3e5ea;--acc:#1f77b4;--acc2:#d62728;--ok:#1b7837;--warn:#b35900;--bad:#b3261e}}
@media (prefers-color-scheme:dark){{:root{{--bg:#14171d;--fg:#e8eaee;--mut:#9aa3b2;--card:#1c2028;--line:#2d333f;--acc:#6aaed6;--acc2:#ef7b7b;--ok:#6fcf97;--warn:#f2a65a;--bad:#f28b82}}}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:1080px;margin:0 auto;padding:28px 16px 80px}}
h1{{font-size:1.9rem;margin:.2em 0 .1em}} h2{{margin-top:2.2em;border-bottom:2px solid var(--line);padding-bottom:.25em}} h3{{margin-top:1.6em}}
.sub{{color:var(--mut)}} .grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));margin:16px 0}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}} .card b.k{{display:block;font-size:1.5rem}}
.ok{{color:var(--ok)}} .warn{{color:var(--warn)}} .bad{{color:var(--bad)}}
table{{border-collapse:collapse;width:100%;margin:12px 0;font-size:.92rem;background:var(--card)}} th,td{{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}}
th{{background:rgba(127,127,127,.12)}} td:not(:first-child),th:not(:first-child){{text-align:right}} table.txt td,table.txt th{{text-align:left}}
figure{{margin:18px 0}} img{{max-width:100%;height:auto;border:1px solid var(--line);border-radius:8px;background:#fff}} figcaption{{font-size:.85rem;color:var(--mut);margin-top:4px}}
.note{{border-left:4px solid var(--warn);background:rgba(179,89,0,.08);padding:10px 14px;border-radius:0 8px 8px 0;margin:14px 0}}
code{{background:rgba(127,127,127,.15);padding:1px 5px;border-radius:4px;font-size:.88em}}
.tag{{display:inline-block;font-size:.75rem;padding:1px 8px;border-radius:99px;border:1px solid var(--line);color:var(--mut)}}
</style></head><body><main>

<p class="sub">Projet Boomrone · module d'essai de simulation · rapport rédigé le 2026-11-11</p>
<h1>Simulation de l'alimentation : ngspice contre LTspice</h1>
<p class="sub">Batterie, résistance interne, 4 moteurs en PWM, LDO 3,0 V (MCP1700) et LDO 2,0 V (XC6206) du capteur de flux, simulés dans les deux outils avec <b>les mêmes netlists</b>.</p>

<h2>En bref</h2>
<div class="grid">
<div class="card"><b class="k ok">Les deux outils s'accordent</b>Ondulation lissée de VBATM : {v(ca['vbm_pp_lisse'],3)} V (ngspice) et {v(c1('vol','LTspice')['vbm_pp_lisse'],3)} V (LTspice). PSRR identique à 10⁻⁵ dB près.</div>
<div class="card"><b class="k warn">PWM en phase : {v(ca['vbm_pp_lisse'],2)} V d'ondulation</b>Avec des PWM décalées de 90° elle tombe à {v(c1('vol_dec')['vbm_pp_lisse'],2)} V, soit 8 fois moins. Rien n'impose aujourd'hui ce décalage dans la conception.</div>
<div class="card"><b class="k bad">Cas pessimiste : +3V0 s'effondre</b>À 7,5 A et 110 mΩ (cas de « Architecture »), le régulateur 3,0 V décroche : +3V0 moyen {v(m['cas2/pess/ngspice']['v3_moy'],2)} V, creux à {v(m['cas2/pess/ngspice']['v3_min'],2)} V. Confirme DOU-135.</div>
<div class="card"><b class="k ok">Ondulation sur +3V0 et +2V0 : négligeable</b>{v(m['cas2/vol/ngspice']['v3_pp']*1e3,1)} mV crête-à-crête sur +3V0 en stationnaire ; moins de 1 µV sur +2V0 (modèle).</div>
</div>

<div class="note"><b>À lire avant tout chiffre.</b> Aucune fiche technique ne donne le moteur 8520 (R, L : DOU-190), le comportement dynamique des LDO au-delà de 100 Hz ni la diode SS34 exacte. Ces valeurs sont des <b>hypothèses « HYP »</b> (liste complète au § 6). Les chiffres sont valables <i>pour ces hypothèses</i> ; les comparaisons entre cas (PWM en phase ou décalées, nominal ou pessimiste) sont plus fiables que les valeurs absolues. Rien ici ne remplace les trois mesures au banc prévues (poussée, courant, résistance interne). Aucun élément « Validé » n'est modifié.</div>

<h2>1. Les deux outils, côte à côte</h2>
<table class="txt"><tr><th></th><th>ngspice 47</th><th>LTspice 26.1</th></tr>
<tr><td>Installation sur ce poste</td><td>Difficile : pas d'installeur sans droits administrateur, SourceForge bloque les scripts. Installé à la main depuis les paquets MSYS2 (3,6 Mo, plus ses bibliothèques), dans <code>C:\\Users\\33766\\tools\\ngspice_pkg</code></td><td>Une commande : <code>winget install AnalogDevices.LTspice --source winget --scope user</code></td></tr>
<tr><td>Lancement en ligne de commande</td><td><code>ngspice_con -b netlist.cir</code>, sorties par <code>wrdata</code> dans un bloc <code>.control</code></td><td><code>LTspice.exe -b netlist.cir</code>, fichier <code>.raw</code> binaire (lu avec <code>spicelib</code>)</td></tr>
<tr><td>Netlist partagée</td><td colspan="2">La même netlist tourne dans les deux outils. Seul le bloc de sortie <code>.control … wrdata</code> est propre à ngspice.</td></tr>
<tr><td>Temps pour les {n_tran} simulations temporelles</td><td>{tot_ng:.0f} s</td><td>{tot_lt:.0f} s (environ {str(round(tot_ng/tot_lt,1)).replace(".", ",")}× plus rapide)</td></tr>
<tr><td>Ondulation lissée de VBATM (stationnaire)</td><td>{v(ca['vbm_pp_lisse'],4)} V</td><td>{v(c1('vol','LTspice')['vbm_pp_lisse'],4)} V</td></tr>
<tr><td>Ondulation brute (pointes de commutation comprises)</td><td>{v(ca['vbm_pp'],3)} V</td><td>{v(c1('vol','LTspice')['vbm_pp'],3)} V</td></tr>
<tr><td>Rejet à 24 kHz, MCP1700, 4,7 µF</td><td>{v(psr['mcp/ngspice']['at24k'],2)} dB</td><td>{v(psr['mcp/LTspice']['at24k'],2)} dB</td></tr>
<tr><td>Licence, portabilité</td><td>Libre, Windows, Linux, macOS ; convient à l'automatisation et à l'intégration continue</td><td>Gratuit mais fermé, Windows et macOS ; bibliothèque de modèles Analog Devices fournie ; éditeur de schémas</td></tr>
</table>
<p><b>Ce que l'écart sur l'ondulation brute veut dire.</b> Les pointes de quelques nanosecondes à la fermeture des interrupteurs (décharge des 100 nF de chaque moteur, sans inductance de câblage dans le modèle) dépendent du pas de calcul de chaque outil : un pas cinq fois plus fin ne rapproche pas les deux outils ({v(fa['vbm_pp'],3)} V contre {v(fb['vbm_pp'],3)} V). Après une moyenne glissante de 0,5 µs, qui supprime ces pointes, les deux outils et les deux pas de calcul donnent le même résultat à moins de 1 mV. Je donne donc le <b>chiffre lissé</b> comme ondulation de la ligne.</p>
{img('fig5_comparaison_outils.png', 'Temps de calcul et ondulation de VBATM : les pointes brutes diffèrent d\'un outil à l\'autre, le chiffre lissé non.')}
<p><b>Mon avis.</b> ngspice pour l'automatisation (scripts, reproductibilité, Linux), LTspice pour l'essai interactif et les modèles de fabricants au format Analog Devices. Avec les mêmes netlists, rien ne les départage sur la précision ici. L'écart réel est la facilité d'installation, en faveur de LTspice sur ce poste.</p>

<h2>2. Cas 1 — batterie, résistance interne et 4 moteurs en PWM</h2>
<p>Batterie 3,70 V à vide, 40 mΩ plus 15 mΩ de connecteur et de pistes, deux condensateurs de 22 µF et un de 100 nF sur la ligne moteurs, MOSFET AO3400A (36 mΩ), diode de roue libre, 100 nF par moteur, PWM à 24 kHz (DES-007). La force contre-électromotrice est calibrée pour retrouver le courant du bilan de « Architecture » : 5,5 A, 9,5 A, 7,5 A.</p>
<table><tr><th>Cas</th><th>I batterie moy. (A)</th><th>VBATM moy. (V)</th><th>Calcul à la main du bilan (V)</th><th>VBATM min lissé (V)</th><th>Ondulation lissée (V c-à-c)</th><th>Brute ngspice / LTspice (V)</th></tr>{rows1}</table>
{img('fig1_batterie_moteurs.png', 'Cas 1 : tension de la ligne moteurs sur 3 périodes (en haut à gauche), courant batterie, et démarrage des moteurs (en bas).')}
<ul>
<li><b>Le calcul à la main du bilan est retrouvé</b> à moins de 60 mV près sur la moyenne ({v(hand['vol'],2)} V, {v(hand['crete'],2)} V, {v(hand['pess'],2)} V contre {v(ca['vbm_moy'],2)} V, {v(c1('crete')['vbm_moy'],2)} V, {v(c1('pess')['vbm_moy'],2)} V). La simulation confirme donc le bilan en moyenne, mais ajoute ce que le bilan ne voit pas : l'ondulation.</li>
<li><b>Le creux de tension ne vient pas du démarrage</b> avec ce modèle de moteur : au démarrage la tension minimale lissée est {v(m['cas1/demarrage/ngspice']['vbm_min_lisse'],2)} V, comparée à {v(ca['vbm_min_lisse'],2)} V en régime établi ; le courant moyen monte à environ 6,3 A contre 5,5 A (+15 %). Un rotor bloqué donnerait plus : le courant de calage n'est pas connu (DOU-190).</li>
<li><b>La mesure de tension par l'ADC n'est pas gênée</b> : le pont 100 kΩ / 150 kΩ et le condensateur de 100 nF forment un filtre de 6 ms, qui réduit l'ondulation de 24 kHz d'un facteur 900 environ.</li>
</ul>
<h3>Effet du décalage des PWM</h3>
{img('fig1b_phase_pwm.png', 'PWM en phase (vert) ou décalées de 90° (violet) : la composante à 24 kHz disparaît quand les quatre phases sont décalées.')}
<p>Le courant de la batterie passe de {v(ca['ibat_pp'],1)} à {v(c1('vol_dec')['ibat_pp'],1)} A crête-à-crête et la composante à 24 kHz de VBATM de {mv(ca['vbm_h1'])} mV à zéro. La conception ne précise pas la phase des quatre sorties de TIM1 ; par défaut elles sont en phase. <span class="tag">piste, pas une décision</span> : un décalage des quatre voies serait un choix à présenter, avec ses avantages et ses coûts, avant toute modification.</p>

<h2>3. Cas 2 — LDO 3,0 V : ondulation, rejet et stabilité</h2>
<p>La chaîne simulée : VBATM → ferrite (0,1 Ω, hypothèse) → VBATL (22 µF + 1 µF) → MCP1700 → +3V0 (4,7 µF, charge 130 mA, DES-009). Le régulateur est un <b>modèle comportemental</b> : décrochage tiré de la fiche (178 mV à 250 mA, p. 3), rejet continu calé sur la fiche (44 dB à 100 Hz, p. 4), boucle de régulation en hypothèse.</p>
<table><tr><th>Cas</th><th>VBATL min (V)</th><th>+3V0 moy. (V)</th><th>+3V0 min (V)</th><th>VBATL à 24 kHz (mV)</th><th>+3V0 à 24 kHz (mV)</th><th>+3V0 c-à-c (mV)</th></tr>{rows2}</table>
{img('fig2_psrr.png', 'Rejet d\'ondulation (PSRR) des deux régulateurs : ngspice, LTspice et un calcul indépendant sous numpy se superposent.')}
<ul>
<li>Le modèle retrouve la valeur de la fiche : {v(psr['mcp_test/ngspice']['at100'],2)} dB à 100 Hz. <b>La fiche ne donne le rejet qu'à 100 Hz</b> (la courbe 2-15 de la p. 7 existe mais n'est pas extraite) : le rejet à 24 kHz, {v(psr['mcp/ngspice']['at24k'],1)} dB ici, repose sur l'hypothèse de boucle.</li>
<li>Mesuré dans la simulation temporelle, VBATL porte {mv(ma['vbl_h1'])} mV à 24 kHz et +3V0 {v(ma['v3_h1']*1e3,2)} mV, soit un rejet de {v(20*__import__('math').log10(ma['v3_h1']/ma['vbl_h1']),1)} dB, en accord avec la courbe.</li>
<li><b>Marge de décrochage.</b> En crête, VBATL descend à {v(m['cas2/crete/ngspice']['vbl_min'],2)} V. Avec le décrochage typique de la fiche, +3V0 reste à 3,00 V. Avec le décrochage maximal garanti (350 mV à 250 mA), +3V0 moyen tombe à {v(dm_c['v3_moy_fin'],3)} V et son creux à {v(dm_c['v3_min'],3)} V : la marge sur les 2,91 V visés par DES-009 n'est plus que d'environ {mv(dm_c['v3_moy_fin']-2.91)} mV. Au démarrage des moteurs, +3V0 ne bouge pas ({v(dm_d['v3_min'],3)} V même au décrochage maximal).</li>
<li><b>Cas pessimiste (7,5 A, 110 mΩ).</b> VBATL descend à {v(m['cas2/pess/ngspice']['vbl_min'],2)} V, sous le seuil de régulation : +3V0 n'est plus tenu, il ondule de {v(m['cas2/pess/ngspice']['v3_pp'],2)} V et atteint {v(m['cas2/pess/ngspice']['v3_min'],2)} V. Un microcontrôleur serait alors en réinitialisation. C'est la situation que DOU-135 et DEC-229 décrivent comme « marginal à infaisable » ; la simulation la reproduit à partir des chiffres de « Architecture ».</li>
</ul>
<h3>Stabilité</h3>
{img('fig3_stabilite.png', 'Gain de boucle et phase des deux LDO pour plusieurs résistances série du condensateur de sortie.')}
<table><tr><th>MCP1700, 4,7 µF</th><th>Fréquence de coupure</th><th>Marge de phase</th></tr>{pmrow('mcp_0.005','ESR 5 mΩ')}{pmrow('mcp_0.1','ESR 0,1 Ω')}{pmrow('mcp_2','ESR 2 Ω (limite de la fiche)')}<tr><th>XC6206, 2,2 µF</th><th></th><th></th></tr>{pmrow('xc_0.005','ESR 5 mΩ')}{pmrow('xc_2','ESR 2 Ω')}</table>
<div class="note"><b>Cette partie démontre la méthode, pas la stabilité des vrais composants.</b> Le modèle de boucle est une hypothèse (gain de transconductance 1,26 S, pôles à 1 et 3 MHz) : il est stable pour toute ESR de 5 mΩ à 2 Ω, ce qui est cohérent avec la plage ESR de 0 à 2 Ω de la fiche (DES-009), mais cela ne le prouve pas. Une vraie analyse de stabilité demande le modèle SPICE du fabricant ; Microchip et Torex en proposent peut-être (non vérifié). À défaut, le critère reste celui de la fiche : COUT d'au moins 1 µF et ESR de 0 à 2 Ω, respecté avec 4,7 µF et 2,2 µF céramiques.</div>

<h2>4. Cas 3 — LDO 2,0 V du capteur de flux</h2>
{img('fig4_chaine_alimentation.png', 'La chaîne complète : ondulation en stationnaire, démarrage des moteurs et impulsion de 70 mA du capteur sur +2V0.')}
<ul>
<li><b>Ondulation sur +2V0 : négligeable.</b> Le rejet continu de la fiche (0,05 %/V typique, p. 4) donne {v(psr['xc/ngspice']['dc'],0)} dB, et l'ondulation de +3V0 à 24 kHz ({v(c3['v3_h1']*1e3,2)} mV) arrive à moins de 1 µV sur +2V0.</li>
<li><b>Point à vérifier : l'impulsion de 70 mA à la mise sous tension du capteur</b> (DES-005) fait descendre +2V0 de 2,000 V à {v(c3['v2_min_pk'],3)} V pendant les 100 µs, soit −2,4 %, hors de la précision de ±2 % de la fiche (1,96 à 2,04 V). Le creux dépend du modèle de boucle (HYP), donc c'est un signal à contrôler, pas un résultat. Le seuil minimal d'alimentation du PMW3901MB à ce moment est à relever (DOU-165).</li>
</ul>

<h2>5. Ce qu'il faut retenir pour le projet</h2>
<table class="txt"><tr><th>Constat (simulé)</th><th>Fiabilité</th><th>Suite possible (décision à prendre)</th></tr>
<tr><td>Ondulation de VBATM : {v(ca['vbm_pp_lisse'],2)} V crête-à-crête avec PWM en phase, {v(c1('vol_dec')['vbm_pp_lisse'],2)} V décalées de 90°</td><td>Moyenne : dépend de L du moteur (HYP) ; l'écart entre les deux cas est robuste</td><td>Question à poser : décaler les phases de TIM1 ?</td></tr>
<tr><td>Le bilan de « Architecture » est retrouvé en moyenne (à moins de 60 mV)</td><td>Bonne : repose sur les chiffres du bilan</td><td>Aucune</td></tr>
<tr><td>+3V0 s'effondre dans le cas pessimiste (7,5 A, 110 mΩ)</td><td>Bonne pour le sens ; les chiffres suivent les entrées du bilan</td><td>Mesurer la résistance interne et le courant au banc ; sinon R1 + R2 de DEC-229</td></tr>
<tr><td>Marge de décrochage de +3V0 de 60 mV environ au décrochage maximal en crête</td><td>Moyenne : feuille de fiche, ferrite et batterie en hypothèse</td><td>Relever la fiche de la ferrite (DOU-186) et vérifier le LDO de repli ME6211</td></tr>
<tr><td>Creux de +2V0 de −2,4 % à la mise sous tension du capteur</td><td>Faible : boucle en hypothèse</td><td>Mesurer ou obtenir le modèle du XC6206 ; relever la tolérance du PMW3901MB</td></tr>
</table>

<h2>6. Hypothèses et sources</h2>
<table class="txt"><tr><th>Paramètre</th><th>Valeur</th><th>Source ou statut</th></tr>
<tr><td>Batterie : tension, résistance</td><td>3,70 V ; 40 mΩ + 15 mΩ</td><td>« Architecture » — bilan (résistance à mesurer)</td></tr>
<tr><td>Courants moyens</td><td>5,5 / 9,5 / 7,5 A</td><td>« Architecture » — bilan, DES-014</td></tr>
<tr><td>Fréquence PWM</td><td>24 kHz</td><td>DES-007</td></tr>
<tr><td>AO3400A</td><td>36 mΩ</td><td>Fiche AO3400A rev 3 p. 1-2 (24 typ. / 48 max. à VGS = 2,5 V ; valeur à 3,0 V non trouvée, DOU-199)</td></tr>
<tr><td>Condensateurs de découplage</td><td>2 × 22 µF, 100 nF, 100 nF/moteur</td><td>DES-007, DES-008</td></tr>
<tr><td>ESR des condensateurs</td><td>5 mΩ</td><td><span class="tag">HYP</span></td></tr>
<tr><td>Moteur 8520</td><td>1 Ω, 25 µH</td><td><span class="tag">HYP</span> (DOU-190, fiche absente)</td></tr>
<tr><td>Diode SS34</td><td>Is 3 µA, N 1,05, Rs 40 mΩ, Cj 200 pF</td><td><span class="tag">HYP</span></td></tr>
<tr><td>Front de grille</td><td>65 ns</td><td><span class="tag">HYP</span> : 2,2 × 47 Ω × 630 pF (DES-007)</td></tr>
<tr><td>Ferrite</td><td>0,1 Ω</td><td>Ordre de grandeur de DES-008 (fiche absente, DOU-186)</td></tr>
<tr><td>MCP1700 : décrochage, courant de repos, rejet</td><td>178 mV à 250 mA ; 1,6 µA ; 44 dB à 100 Hz</td><td>Fiche DS20001826C p. 3-4</td></tr>
<tr><td>XC6206 : décrochage, rejet continu</td><td>350 mV à 100 mA ; 0,05 %/V</td><td>Fiche ETR0305_004b p. 4-5 et DES-005</td></tr>
<tr><td>Boucle des LDO</td><td>1,26 S ; pôles à 1 et 3 MHz</td><td><span class="tag">HYP</span> (aucune fiche)</td></tr>
<tr><td>Charges</td><td>130 mA (logique), 9 mA + pointe de 70 mA (capteur)</td><td>DES-009, DES-005</td></tr>
</table>

<h2>7. Refaire la simulation</h2>
<p>Tout est dans <code>projets/boomrone/simulation/</code> : <code>sim_boomrone.py</code> (netlists, lancement, calibration), <code>analyse_boomrone.py</code> (mesures et courbes), <code>build_report.py</code> (ce rapport), <code>netlists/</code> (les {n_net} netlists produites), <code>figures/</code>, <code>metriques.json</code>. Dans le dossier :</p>
<p><code>python sim_boomrone.py all</code> puis <code>python build_report.py</code> (environ une minute). Les chemins de ngspice et de LTspice se règlent avec les variables <code>NGSPICE_EXE</code> et <code>LTSPICE_EXE</code>. Les sorties brutes (900 Mo) ne sont pas conservées dans le dépôt.</p>
</main></body></html>
"""
(HERE / "rapport-simulation-spice.html").write_text(html, encoding="utf-8")
print("ok", len(html) // 1024, "Ko")
