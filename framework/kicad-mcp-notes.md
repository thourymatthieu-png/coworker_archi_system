# Notes sur le MCP KiCad — bugs connus et méthode

## Outils MCP « différés » : un agent peut croire un outil absent alors qu'il existe

Constat du 2026-11-05 (préparation du PCB Boomrone, DES-013) : l'agent `electronique-hardware`,
bien que sa liste `tools:` contienne les outils PCB (`place_component`, `run_drc`, `autoroute`,
etc.), a conclu qu'« aucun outil PCB dédié » n'était accessible et a tout fait par script Python
direct sur `pcbnew`. Cause réelle : la plateforme (pas KiCad, pas le serveur MCP) charge certains
outils MCP en différé — leur schéma n'est disponible qu'après un appel `ToolSearch` avec
`query: "select:<noms des outils>"`. Un appel direct avant ce chargement échoue
(`InputValidationError`), ce qui peut laisser croire à tort que l'outil n'existe pas. Il manquait
aussi `ToolSearch` lui-même dans la liste `tools:` de l'agent, qui ne pouvait donc pas charger les
outils différés. Correction appliquée : `ToolSearch` ajouté à la liste `tools:` de
`electronique-hardware.md`, et instruction d'appeler `ToolSearch` en tout début de tâche PCB avant
le premier `place_component`/`route_trace`/etc. Si ça se reproduit avec d'autres outils (schéma ou
PCB), même diagnostic : vérifier `ToolSearch` avant de conclure à une absence d'outil.

Ce document existe pour que ces constats survivent à un changement de machine ou de session
(contrairement à la mémoire d'une session Claude Code, qui est locale). Lu par `electronique-hardware`
avant toute saisie de schéma KiCad.

## J1 (XT30PW-M, connecteur batterie) : sens d'enfichage confirmé par l'utilisateur dans KiCad

Un agent avait déduit le sens d'enfichage de J1 par lecture géométrique du footprint seule (position
des pastilles, forme de la sérigraphie) et conclu qu'il fallait une rotation de 180°. **L'utilisateur
a ouvert KiCad, regardé le connecteur réel et corrigé lui-même : la bonne orientation est rotation
0°**, pas 180°. Leçon : la lecture géométrique d'un footprint importé (surtout EasyEDA/LCSC, cf.
DOU-206/DOU-207 au sujet d'autres pièces) peut induire en erreur sur un détail mécanique comme le sens
d'un connecteur — un rendu visuel zoomé ou, mieux, la confirmation de l'utilisateur dans KiCad priment
sur un raisonnement géométrique seul.

**État de référence confirmé (2026-11-05), carte Boomrone, projet `proj_boomrone`** : J1
(`lib_boomrone:CONN-TH_XT30PW-M`), position (25, 43,4875) mm, **rotation 0°**, couche F.Cu. Broches 1
(GND) et 2 (VBATM, pastilles traversantes Ø2,5 mm) côté nord (y ≈ 38,49, vers le centre de la carte) ;
broches de maintien 3/4 (sans réseau) côté sud (y ≈ 48,49, vers le bord bas de la carte, où le boîtier
dépasse légèrement du contour — comportement attendu, c'est là que le câble s'enfiche depuis
l'extérieur). **Ne pas retourner ce composant dans une future passe de placement** (le passer en
`locked` dans `suggest_placement`) sans revalidation explicite de l'utilisateur.

## Placement PCB : utiliser `suggest_placement`, ne jamais replacer composant par composant

Constat du 2026-11-05 (carte Boomrone, 107 composants) : un premier essai a placé les composants
un par un (`place_component`/`move_component` répétés, découplage ↔ CI redérivé à la main en
relisant chaque feuille de schéma) — lent (~200 appels d'outils pour une carte) et de mauvaise
qualité (106 chevauchements de boîtiers non résolus). **Erreur : `suggest_placement` existe déjà et
fait presque tout ça automatiquement** (lecture du code source du serveur,
`python/commands/placement_optimizer.py`, 835 lignes, pas une supposition) :
- Placement par forces dirigées (refroidissement progressif), `decoupling_boost` (rapproche un
  passif 2 broches de son CI multi-broches **par connectivité réelle**, pas par nom de référence),
  `power_weight`/`power_nets` (réseaux de forte puissance tirés courts et directs).
- Collision sur la **géométrie réelle des boîtiers** (courtyard), pas une boîte approximative.
- `spread` (diffusion de densité) + légalisation (sépare les chevauchements) + `align` (rangées/colonnes).
- **Dry-run par défaut** (`apply: false`), score avant/après (longueur de câblage HPWL, nombre de
  chevauchements) — ne jamais appeler avec `apply: true` sans avoir regardé le score et validé.
- `locked` : fige des ancres (composants à contrainte mécanique dure — connecteurs, pièces RF,
  position imposée) ; le reste se place en tirant sur ces ancres fixes, pas en les traitant comme une
  pénalité parmi d'autres.
- `bounds` + `refs` : regroupement scopé à une zone/un sous-ensemble — reproduit la discipline
  « un bloc à la fois » du schéma, sans perturber le reste de la carte déjà placé.
- Workflow obligatoire : `suggest_placement(apply=false)` → `check_courtyard_overlaps(positions=proposals)`
  pour valider l'hypothèse → seulement alors `suggest_placement(apply=true)` (ou rejouer avec les
  mêmes paramètres et `apply: true`) → vérification visuelle → `autoroute`/routage manuel.

**Méthode à suivre systématiquement** : placer à la main uniquement les quelques composants à
contrainte mécanique dure (connecteur batterie, sorties moteur, pièce RF...), les passer en `locked`,
puis laisser `suggest_placement` faire le reste bloc par bloc. Ne jamais revenir au placement
composant par composant sauf si `suggest_placement` échoue explicitement sur un cas précis.

**Correction d'un constat antérieur** : la note ci-dessus (2026-11-05, « outils MCP différés ») disait
qu'aucun outil PCB dédié n'était accessible — c'était un vrai problème de chargement différé à ce
moment-là, pas une absence réelle d'outils. Une fois `ToolSearch` en place, les outils de placement et
d'optimisation (dont `suggest_placement`) sont bien exposés.

**Contour non rectangulaire** : `add_board_outline` accepte `shape: "polygon"` avec une liste de
`points` — un contour en L/T (ex. languette d'antenne qui dépasse le carré principal) est directement
possible par cet outil, pas besoin d'édition manuelle du `.kicad_pcb` pour ce cas.

## Méthode : bilan de bibliothèque avant tout schéma

Avant de saisir le moindre schéma, faire un bilan de bibliothèque sur toute la nomenclature du
projet : pour chaque composant actif, vérifier qu'un **symbole** ET une **empreinte** existent
(bibliothèques standard KiCad, ou à créer/importer depuis LCSC/EasyEDA) et lever les manques.
Le schéma, puis le routage, ne viennent qu'après ce bilan — pas de contournement improvisé
découvert bloc par bloc pendant la saisie (constat du test Boomrone, DES-011 : pas de symbole
« LED RGB anode commune » standard, pas d'empreinte pour la LED SZYY1615RGB-B ni le buzzer
SMD-9650-3327, découverts seulement pendant la saisie de ce bloc).

## Changement de serveur MCP (2026-11-04) : `kicad` = désormais `mixelpixx/KiCAD-MCP-Server`

Comparaison de quatre serveurs MCP KiCad faite le 2026-11-04 (`framework/kicad-mcp-bug-report.md`) :
l'ancien serveur `kicad` (paquet PyPI `kicad-eda-mcp`, section ci-dessous) et son concurrent
`kicad-pro` ont tous les deux un défaut de texte en miroir après une rotation à 180° ; deux serveurs
sans ce défaut ont été trouvés (`mixelpixx/KiCAD-MCP-Server` et `mixelpixx/Konnect`), et
`mixelpixx/KiCAD-MCP-Server` a été retenu pour rester maintenu en open source (MIT) — `Konnect` vient
d'un dépôt archivé, son successeur commercial `Konnect-EDA` n'a encore publié aucun binaire.

**Les deux anciens serveurs (`kicad`/`kicad-eda-mcp` et `kicad-pro`/`kicad-mcp-pro`) ont été
désinstallés** (venvs supprimés, entrées retirées de `.claude.json`). Tout ce qui suit dans ce
document à propos du comportement d'un « serveur kicad » décrit ce **serveur abandonné**, gardé par
écrit pour comparaison (section « Opérations cassées du serveur » et « Rotation des composants : …») —
pas un bug encore à craindre avec le serveur actuel. Les règles de lisibilité/placement (grille,
symboles de puissance, vérification par rendu visuel) restent valables quel que soit le serveur.

## Mise en route sur une nouvelle machine

- Installer KiCad (testé avec KiCad 10), Node.js 18+ et Python 3.11+ (testé avec Node 24.20.0 et le
  Python embarqué de KiCad, 3.11.5).
- Cloner et construire le serveur `mixelpixx/KiCAD-MCP-Server` (branche `stable`) :
  ```bash
  git clone --branch stable https://github.com/mixelpixx/KiCAD-MCP-Server.git <ailleurs que le dépôt, p. ex. ~/mcp-servers/KiCAD-MCP-Server>
  cd <dossier cloné> && npm install && npm run build   # produit dist/index.js
  ```
- Ce serveur a besoin de `pcbnew` (bindings Python de KiCad), qui n'existe que dans le Python
  **embarqué** de KiCad (`<install KiCad>\bin\python.exe` sur Windows), pas le Python système : un
  venv basé sur le Python système ne peut pas l'importer (ABI différente). **Ne pas suivre le script
  d'installation officiel du projet (`setup-windows.ps1`)**, qui installe les dépendances directement
  dans le dossier d'installation de KiCad (le modifie). À la place, créer un venv **à partir du
  Python de KiCad** avec accès à ses paquets système, qui reste isolé de l'installation KiCad :
  ```bash
  "<install KiCad>\bin\python.exe" -m venv --system-site-packages <chemin du venv, p. ex. ~/.venvs/kicad-mcp>
  "<venv>\Scripts\python.exe" -m pip install -r <dossier cloné>/requirements.txt
  ```
  Piège à connaître : `PYTHONPATH` ne permet **pas** de contourner cette étape pour un Python embarqué
  de KiCad lancé hors venv — son `sitecustomize.py` fait `sys.path = []` puis le reconstruit lui-même
  (ignore `PYTHONPATH`) tant qu'il n'est pas dans un venv (`sys.prefix != sys.base_prefix`).
  Piège : le `pip` du Python embarqué de KiCad plante (« OPENSSL_Uplink … no OPENSSL_Applink »). Contournement :
  piloter l'installation avec un autre Python (ex. Python 3.12 système) qui cible le venv :
  ```bash
  C:\Python312\python.exe -m pip --python <venv>\Scripts\python.exe install -r <dossier cloné>/requirements.txt
  ```
- Piège : **plusieurs versions de KiCad installées** (constaté : 9.0 et 10.0 côte à côte). Le serveur
  ajoute en tête de `sys.path` les `site-packages` de *toutes* les installations trouvées
  (`utils/platform_helper.py`, `get_kicad_python_paths`), la plus ancienne finissant en premier : les
  paquets de KiCad 9 masquent ceux de KiCad 10 et le processus Python meurt au démarrage avec le même
  message `no OPENSSL_Applink`, côté MCP : « Connection closed » dès le premier appel d'outil. Diagnostic :
  lancer le serveur à la main (`node dist/index.js`, avec `KICAD_PYTHON`) et lire le log. Corrections
  possibles : désinstaller l'ancienne version de KiCad, ou limiter la boucle sur `kicad_install_roots()`
  à la première racine (la plus récente) dans `platform_helper.py` (vérifié sur une copie).
- Déclarer le serveur dans `.claude.json` (clé `mcpServers.kicad`, machine-locale, pas dans ce
  dépôt) :
  ```json
  {
    "type": "stdio",
    "command": "node",
    "args": ["<chemin complet vers dist/index.js>"],
    "env": { "KICAD_PYTHON": "<chemin complet vers <venv>\\Scripts\\python.exe>" }
  }
  ```
  Puis redémarrer la session Claude Code pour que les outils apparaissent.
- Pas de variables `KICAD_SYMBOL_DIR`/`KICAD_FOOTPRINT_DIR` à poser pour ce serveur (c'était une
  nécessité du serveur abandonné, voir ci-dessous) : `pcbnew`, via le Python embarqué, connaît déjà
  les bibliothèques de l'installation KiCad.

## Ancien serveur « kicad » (`kicad-eda-mcp`, abandonné le 2026-11-04) — pour mémoire

- Installer KiCad (testé avec KiCad 10).
- Le serveur MCP `kicad` (outil `kicad_schematic_edit`, basé sur `kicad-sch-api`, pur Python) ne lit
  pas le `sym-lib-table` de KiCad : il cherche seulement `KICAD_SYMBOL_DIR` / `KICAD9_SYMBOL_DIR` /
  `KICAD8_SYMBOL_DIR` / `KICAD7_SYMBOL_DIR` (pas `KICAD10_SYMBOL_DIR`). Sans ces variables, les
  symboles de base (`Device:R`, `Device:C`, `Switch:SW_Push`, `power:GND`, etc.) ne sont pas trouvés.

## Opérations cassées du serveur (confirmé, pas de contournement côté serveur)

- `add_label_to_pin` : non implémentée (« 'Schematic' object has no attribute 'add_label_to_pin' »).
  Contournement : `add_wire_to_pin` (petit fil vers un point proche) puis `add_label` à ce point.
- `get_net_for_pin` et `connectivity_check` : erreur interne systématique (« unhashable type: 'Net' »).
  Contournement : s'appuyer sur `erc` / `schematic_quality_gate` / `schematic_connectivity_gate` et
  une relecture manuelle du texte dans le `.kicad_sch` sauvegardé.
- `add_rectangle` : échoue systématiquement (« can only concatenate str (not "int") to str »). Pas de
  cadre de délimitation visuelle possible par ce biais ; se contenter d'un `add_text` en titre de bloc.
- `add_sheet` : échoue systématiquement (« 'SheetManager' object has no attribute 'add' »). Impossible
  de créer une feuille hiérarchique avec cette opération. **Contournement : `tools/add_kicad_sheet.py`**
  (voir plus bas).
- `add_with_pin_at` et `align_pin` : cassés (« missing positional argument », « unsupported operand
  type(s) »). Contournement : `add_component` (positionnement par centre) puis calcul des broches par
  un composant de test jetable (`add_wire_to_pin` vers un point arbitraire, lecture des coordonnées de
  fil dans le fichier sauvegardé, suppression du composant de test) plutôt que par les offsets publiés
  des bibliothèques.
- Rotation des composants (`rotate_component`) : le comportement diffère d'un symbole à l'autre, pas
  seulement la transposition (x, y) déjà documentée pour `Device:R`/`Switch:SW_Push` (voir plus bas).
  Constaté sur DES-011 : `Transistor_FET:AO3400A` à 180° ne retourne que le signe de x (pas y) ;
  `Device:Buzzer` à 180° retourne bien x ET y ; `Diode:SS34` à 90°/270° ne suit pas la même
  transposition que les autres symboles testés. **Ne jamais présumer le comportement d'une rotation
  pour un nouveau symbole : toujours vérifier par un composant de test jetable + lecture du fichier
  avant de figer une disposition.**
- Sous-feuilles (fichier de sous-feuille créé par `tools/add_kicad_sheet.py`) : chaque `save` via
  `kicad_schematic_edit` réinitialise `(sheet_instances (path "/" ...))` à la racine vide au lieu de
  `/<uuid_feuille>`, et chaque nouveau composant est écrit avec `(project "simple_circuit")` et un
  chemin d'instance à un seul segment (`"/<uuid_du_fichier_sous-feuille>"`) au lieu de
  `(project "<nom_du_projet>")` et `"/<uuid_racine>/<uuid_feuille>"` à deux segments. **Non corrigé par
  `tools/fix_kicad_project_uuid.py`** (qui ne traite que l'UUID racine du fichier racine) : après toute
  saisie dans une sous-feuille, relire le `.kicad_sch` de la sous-feuille et corriger à la main (ou par
  un script dédié à écrire) le nom de `project` et le chemin `path` de chaque composant et du
  `sheet_instances`, en comparant avec une sous-feuille déjà correcte (ex. `des-010-bouton.kicad_sch`).
- `remove_label` : renvoie « Label not found » sur un `hierarchical_label` existant (UUID valide) —
  semble ne pas gérer ce type de label. Contournement : éditer directement le `.kicad_sch`.
- `kicad_workflow` `create_project` : génère un `.kicad_sch` avec un UUID racine à zéro
  (`00000000-0000-0000-0000-000000000000`) incohérent avec le `.kicad_pro`, et un nom de projet
  placeholder (`simple_circuit`) dans les blocs `instances` des composants. Résultat : KiCad affiche
  le schéma comme vide (« pas de schématique chargée ») même si le fichier contient les composants.
  **Contournement : `tools/fix_kicad_project_uuid.py` <dossier_projet_kicad> [--check]**, à lancer
  juste après tout `create_project` (et après tout `create` en mémoire suivi d'un `save` vers un
  fichier existant, qui régénère aussi un UUID à zéro).

## Rotation des composants : l'angle stocké n'est pas ce qu'on croit

`rotate_component` à 90° ne fait pas une rotation géométrique propre des broches : pour une broche à
l'offset local (x, y) par rapport au centre du composant, l'offset absolu après rotation devient
empiriquement **(y, x)** (une transposition), confirmé sur `Device:R` et `Switch:SW_Push`. Ne jamais
calculer la position finale d'une broche de tête — toujours vérifier après coup en relisant les
coordonnées des fils dans le `.kicad_sch` sauvegardé (section `(wire (pts (xy ..) (xy ..)))`).

**Angle du texte Référence/Valeur d'un composant tourné.** Mettre l'angle du champ à `0` suffit pour
un composant **non tourné** (texte horizontal correct). Mais pour un composant tourné à 90°, KiCad
recombine l'angle stocké du champ avec la rotation du symbole parent au rendu : il faut mettre l'angle
du champ à l'**opposé** de la rotation du composant (`270` pour un composant tourné à `90`) pour
obtenir un texte horizontal à l'écran. Règle observée : `angle_du_champ = (360 - rotation_du_composant) % 360`.
Aucune opération du MCP ne permet de régler cet angle : éditer directement le `.kicad_sch`, chercher
`(property "Reference" "<ref>" (at x y <angle>))` et `(property "Value" ...)`.

**La formule d'angle ne suffit pas seule à 180°.** Constaté sur `Device:Buzzer` tourné à 180°
(DES-011) : angle de champ à `0` donne un texte horizontal mais rendu en miroir et mal positionné,
car `justify` (gauche/droite) doit aussi être inversé par rapport à un composant non tourné (`right`
au lieu de `left` dans ce cas) pour que le texte s'étende dans le bon sens. Vérifié par rendu
visuel (export SVG), pas par calcul. **À 180°, vérifier angle ET justify par un rendu, ne pas se
fier à la seule formule d'angle validée à 90°/270°.**

**Ne jamais conclure sur l'horizontalité ou le chevauchement d'un texte par la seule lecture des
coordonnées — toujours vérifier par un rendu visuel.** C'est la cause directe des défauts de DES-011
(texte en miroir sur le buzzer, GND superposé aux MOSFET) : une vérification purement géométrique
(lecture des coordonnées dans le fichier) ne les a pas détectés, seul un rendu visuel les a montrés.

## Vérification visuelle d'un bloc (obligatoire avant de rendre la main)

1. Exporter en SVG depuis la **racine** (génère un fichier par page) :
   `kicad_schematic export_svg` sur `<projet>.kicad_sch`, `output_dir` dans un dossier du projet
   (jamais hors projet, sinon le rendu reste une « snapshot statique » et `computer screenshot`
   échoue) — par exemple `<dossier_projet_kicad>/_verif_svg/`.
2. La page entière (A4/A3) est trop grande pour qu'un petit bloc soit lisible tel quel : **recadrer
   le `viewBox`** du SVG exporté sur la zone du bloc avant de l'ouvrir, par un petit script Python
   (pas d'édition manuelle) :
   - Repérer la boîte englobante approximative du bloc en cherchant dans le SVG les coordonnées
     `M x y` qui précèdent les textes des repères du bloc (`D1`, `Q1`, nom du bloc, etc.).
   - Remplacer `width="297.0022mm" height="210.0072mm" viewBox="0.0000 0.0000 297.0022 210.0072"`
     (dimensions exactes de la page A4, à adapter si A3) par
     `width="<L_px>" height="<H_px>" viewBox="<x0> <y0> <largeur_mm> <hauteur_mm>"` avec `L_px`/`H_px`
     en pixels de l'ordre de 800-1300 (pas en mm : un très grand `width`/`height` en mm fait déborder
     le rendu hors du cadre visible du navigateur et donne une capture vide), et une marge de
     quelques mm autour de la boîte englobante trouvée.
   - Sauvegarder ce SVG recadré sous un nom différent (`crop_<bloc>.svg`) dans le même dossier.
3. `navigate` vers le `file:///...crop_<bloc>.svg`, `computer screenshot`, puis `zoom` sur chaque
   sous-zone douteuse (texte, chevauchement, jonction).
4. Confronter ce qui est vu à la checklist « Règles de placement » ci-dessous. Se corriger soi-même,
   ré-exporter, revérifier — **avant** de rendre la main pour relecture.
5. Supprimer les fichiers SVG temporaires (export brut et recadrés) du dossier du projet une fois la
   vérification terminée.

## Grille et lisibilité du schéma (exigé par l'utilisateur)

- Un bloc = une zone groupée visuellement, avec un texte de titre (`add_text`) au-dessus.
- Câblage lisible : des fils réels, **strictement horizontaux ou verticaux**, entre composants
  proches — jamais de fil en diagonale, jamais un fil qui traverse le corps d'un autre composant.
  Les labels de net ne servent que pour ce qui sort du bloc (alimentations, signaux vers le
  microcontrôleur).
- Grille majeure (2,54 mm / 0,1") : choisir les coordonnées des **broches de connexion** (pas
  forcément les centres des composants) comme multiples de 2,54 mm. `Device:R`/`Device:C` ont un
  écartement de broches de 7,62 mm (3×2,54) : si une broche est sur la grille majeure, l'autre l'est
  aussi automatiquement — choisir le centre en conséquence (`centre = broche_cible ∓ 3,81`).
  `Switch:SW_Push` a un écartement de 10,16 mm (4×2,54), même propriété.
- Vérifier qu'aucune broche n'est flottante ni doublement connectée au même point que deux éléments
  différents (piège fréquent : la broche « loin » du nœud qui se retrouve, par erreur de calcul, au
  même endroit que la broche « proche » — l'autre broche reste alors en l'air sans que l'ERC s'en
  plaigne forcément).
- Symboles de puissance (`power:GND`, `power:+3V0`, etc.) plutôt que des labels texte pour les
  alimentations. Le pin de ces symboles est à l'origine locale (0,0) : placer le composant exactement
  aux coordonnées de la broche à alimenter suffit (connexion à distance nulle), pas besoin de fil.
- Chevauchement texte/composant : le gabarit place souvent `Value` exactement au centre du composant,
  invisible en texte vertical (il court le long du corps) mais flagrant une fois à l'horizontal.
  L'ancre de texte est en `(justify left)` par défaut : le texte part de l'ancre et s'étend vers la
  **droite** uniquement. Décaler l'ancre d'au moins 2-3 mm du centre, dans une direction sans fil ni
  broche, et vérifier l'absence de chevauchement avec le texte d'un composant voisin.
- Un bloc à la fois : saisir/retravailler un seul bloc, s'arrêter, laisser l'utilisateur relire
  **directement dans KiCad** (il ne veut pas d'export SVG envoyé systématiquement) avant de continuer.

## Règles de placement (checklist, à vérifier visuellement, pas seulement par calcul)

- **Préférer l'orientation par défaut du symbole à toute rotation.** C'est l'orientation la mieux
  garantie (pas de bug de rotation possible) et c'est aussi celle qui a le texte Référence/Valeur
  déjà horizontal sans correction d'angle. Ne tourner un composant que si le câblage l'exige
  vraiment, et dans ce cas appliquer systématiquement la règle d'angle de champ ci-dessus **et**
  vérifier la rotation par un composant de test jetable avant de l'appliquer au composant réel
  (comportement différent par type de symbole, voir plus haut).
- **Ne jamais mirror un composant pour l'orienter** (même tentation que la rotation) : ça retourne
  le texte en miroir, illisible (constaté sur le buzzer de DES-011). Rotation uniquement.
- **Flux d'alimentation constant dans tout le schéma : l'alimentation (VBATM, +3V0, etc.) en haut,
  la masse (GND) en bas.** Chaque symbole `power:GND` doit être visuellement en dessous du
  composant qu'il dessert, jamais superposé à son corps (défaut constaté sur les 4 MOSFET de
  DES-011 : le GND de la source était placé à l'intérieur du cercle du transistor). Si la broche à
  mettre à la masse n'est pas déjà en bas du symbole, prolonger par un petit fil vertical plutôt que
  de poser le symbole de puissance au même endroit que le corps du composant.
- **Un net qui sort du bloc par la gauche, le label est à gauche du point de sortie ; un net qui
  sort par la droite, le label est à droite.** Le texte du `hierarchical_label`/`label` se lit dans
  le sens où il « pointe » : jamais de texte du mauvais côté de la pointe.
- **Grille régulière entre les répétitions d'un même motif** (ex. plusieurs branches identiques
  d'un même bloc, comme les 3 voies couleur de DES-011) : un pas constant, multiple du pas de grille
  (2,54 mm), entre chaque motif répété, y compris entre le dernier motif d'un groupe et le groupe
  suivant — ne pas resserrer le dernier écart par rapport aux précédents.
- **Aucun texte ne peut chevaucher un autre texte ni un symbole**, y compris deux labels de net
  voisins (constaté : deux labels d'un même net à deux endroits proches qui se recouvraient sur
  DES-011). Si deux éléments de texte doivent coexister à proximité, les décaler d'au moins 2-3 mm
  dans une direction libre.
- **Planifier la disposition avant de placer** : pour un bloc à plusieurs branches similaires,
  écrire d'abord un petit tableau (texte) centre-x / centre-y par composant, vérifier à la main que
  les pas entre colonnes sont constants et suffisants (largeur du composant le plus large du groupe
  + marge), puis placer dans cet ordre — plutôt que placer au fil de l'eau et ajuster après coup.

## Feuilles hiérarchiques (une page par bloc)

**Avec le serveur actuel (`mixelpixx/KiCAD-MCP-Server`), le script `tools/add_kicad_sheet.py`
ci-dessous n'est plus nécessaire** : l'outil MCP `create_hierarchical_subsheet` crée le fichier de
sous-feuille et l'insère dans le schéma parent en un seul appel (voir
`framework/kicad-mcp-bug-report.md`, test comparatif « kicad-mixelpixx »). Le principe reste le même
(un bloc = une page, labels hiérarchiques pour ce qui sort du bloc, vérification par rendu visuel) ;
cette section décrit la méthode avec l'ancien serveur, gardée pour mémoire tant que la méthode avec
le nouveau serveur n'est pas documentée ici après son premier usage réel.

`tools/add_kicad_sheet.py <dossier_projet_kicad> --name "DES-xxx — Titre" --file des-xxx-titre.kicad_sch [--pin NOM:forme ...]`
(forme = `input`/`output`/`bidirectional`/`tri_state`/`passive`, une par signal qui sort du bloc).

1. Le script écrit le `(sheet ...)` dans le schéma racine, met à jour la clé `"sheets"` du
   `.kicad_pro`, crée le fichier de sous-feuille (paysage A4 par défaut, `--paper A3` si besoin de
   place), et affiche le chemin d'instance exact à utiliser dans les composants de la sous-feuille :
   `(path "/<ROOT_UUID>/<SHEET_UUID>" (reference "...") (unit 1))`.
2. Charger la **sous-feuille** (pas la racine) avec `kicad_schematic_edit` `load`, y saisir les
   composants normalement, et poser un `hierarchical_label` (pas un `label` simple) pour chaque
   signal destiné à rejoindre la broche de feuille créée à l'étape 1 (même nom que `--pin`).
3. `kicad_schematic erc` sur le schéma **racine** : l'ERC suit la hiérarchie automatiquement.
4. Vérifier visuellement (export SVG depuis la racine génère un fichier par page :
   `<projet>.svg` pour la racine, `<projet>-<Nom de la feuille>.svg` pour chaque sous-feuille).

Premier bloc fait ainsi : DES-010 « Circuit du bouton » (`des-010-bouton.kicad_sch`), la feuille
racine (`proj_boomrone.kicad_sch`) sert de page d'index avec une case par bloc.

## Serveur `mixelpixx/KiCAD-MCP-Server` : constats du premier usage (2026-11-04, proj_boomrone)

- **Projet** : `create_project` puis `create_hierarchical_subsheet` (une page par bloc, A4 paysage par
  défaut) puis `add_sheet_pin` sur le schéma racine pour chaque `hierarchical_label` de la sous-feuille
  (même nom, même sens). `fix_kicad_project_uuid.py` ne sert plus (format KiCad 10 non reconnu par le
  script, et le bug d'UUID n'existe pas avec ce serveur).
- **Rotation** : les positions de broches après rotation sont correctes (vérifier quand même avec
  `get_schematic_pin_locations` avant de câbler). Les textes Référence/Valeur d'un composant tourné à
  90° s'affichent à la verticale : régler l'angle du champ à 270 avec `set_schematic_component_property`
  (`name` = `Reference` ou `Value`, avec `x`, `y`, `justify`, `hide`).
- **`add_schematic_text` et `justify: "center"`** écrit `(justify center bottom)`, que KiCad 10 refuse à
  l'ouverture (« Attendu left, right, top, bottom, or mirror »). `kicad-cli` ne s'en plaint pas, seule
  l'interface graphique plante. Ne jamais passer `center` à `add_schematic_text` : centrer en décalant
  l'ancre à gauche (largeur ≈ 0,5 × nombre de caractères × taille de police).
- **Symboles de puissance** (`power:GND`, `power:+3V0`) : masquer leur Référence (`hide: true`) ; poser
  le symbole GND sous la broche, relié par un fil, et placer sa Valeur explicitement sous le triangle.
- **Bibliothèque projet** : `create_symbol` / `import_symbol` écrivent des champs `(id N)` d'un ancien
  format et provoquent l'avertissement ERC « lib_symbol_mismatch ». Corriger avec
  `kicad-cli sym upgrade lib_boomrone.kicad_sym` puis `update_symbol_from_library`. Les tables
  `sym-lib-table` / `fp-lib-table` du projet utilisent `${KIPRJMOD}` (pas de chemin absolu).
- **Import EasyEDA/LCSC** : `easyeda2kicad --lcsc_id Cxxxxx --full` (installé dans un venv jetable) donne
  symbole, empreinte et 3D ; les types de broches arrivent tous « unspecified » (à corriger), les chemins
  3D sont absolus (à remplacer par `${KIPRJMOD}/lib_<projet>.3dshapes/...`).
- **Vérification visuelle sans navigateur** : `kicad-cli sch export pdf`, puis rendu d'une page en PNG
  avec `pypdfium2` (rognage en mm), puis lecture de l'image.

## `sync_schematic_to_board` cassé par un bug de la bibliothèque `kicad-skip` (constaté 2026-11-05, proj_boomrone)

L'outil MCP `sync_schematic_to_board` (import du schéma vers le PCB, équivalent F8) échoue
systématiquement dès qu'une sous-feuille du schéma ne contient **qu'une seule** étiquette d'un type
donné (`label`, `global_label` ou `hierarchical_label`) : `TypeError: __bool__ should return bool,
returned str`. Cause : dans la bibliothèque Python `kicad-skip` (utilisée en interne par le serveur
pour lire les sous-feuilles), `sch.label` (au singulier) renvoie l'élément unique directement plutôt
qu'une liste à un élément ; le code du serveur fait `getattr(sch, "label", None) or []`, et
`bool()` sur cet élément unique (`ParsedValue.__bool__`, fichier
`skip/sexp/parser.py`) renvoie la valeur brute (une chaîne, le texte de l'étiquette) au lieu d'un
booléen, ce que Python refuse. Reproduit sur `des-010-bouton.kicad_sch` (un seul
`hierarchical_label`). Confirmé par la trace du serveur
(`~/.kicad-mcp/logs/kicad_interface-*.log`, chercher `__bool__ should return bool`).

**Pas de contournement côté appel d'outil** (aucun paramètre n'évite le scan de cette sous-feuille,
`sync_schematic_to_board` parcourt toute la hiérarchie). Contournement utilisé : un script Python
autonome, lancé avec le même interpréteur que le serveur (`KICAD_PYTHON` de `.claude.json`), qui :
1. copie le paquet `skip` du venv vers un dossier hors du projet (ne jamais modifier
   l'installation du venv partagé — geste irréversible hors du dépôt) ;
2. corrige la copie : `ParsedValue.__bool__` doit renvoyer `bool(self._value)` au lieu de
   `self._value` dans le cas non booléen (`skip/sexp/parser.py`, méthode `__bool__`) ;
3. met cette copie en tête de `sys.path`, puis importe `commands.schematic_handlers` du serveur
   (`<dossier cloné>/python`) et instancie une classe minimale héritant de
   `SchematicHandlersMixin` (avec juste `self.board`, `_safe_load_board` (`pcbnew.LoadBoard`),
   `_update_command_handlers` (no-op) et `_find_kicad_cli_static` (chemin de `kicad-cli.exe`)) pour
   appeler directement `_handle_sync_schematic_to_board({"schematicPath": ..., "boardPath": ...})` —
   réutilise toute la logique réelle du serveur (netliste, assignation des pastilles, ajout des
   empreintes manquantes), seul le bug de `kicad-skip` est contourné.
4. **Fermer le projet côté session MCP (`close_project`, `save: false`) avant de lancer ce script**
   (sinon la sauvegarde du script et celle de la session MCP se marchent dessus), le rouvrir après.

À corriger en amont (remonter le bug à `kicad-skip` ou au serveur `mixelpixx/KiCAD-MCP-Server`) si
revu plus tard ; pour l'instant, le script de contournement n'est pas versionné dans ce dépôt (créé
dans le scratchpad de la session), à refaire à l'identique si le besoin se représente.

## Pas d'outils MCP dédiés pour l'implantation/le contour/les règles de conception du PCB (constaté 2026-11-05)

Le jeu d'outils MCP effectivement exposé pour ce projet ne contient **aucun** outil PCB au-delà de
`sync_schematic_to_board` (pas de contour de carte, pas de règles de conception, pas de classes de
réseaux, pas d'autorouteur, pas d'export SVG/2D du PCB, pas de sauvegarde explicite), alors que le
serveur annonce 244 outils dans ses logs (`All 244 tools visible`) : `KICAD_MCP_TOOLBOXES` limite
probablement l'ensemble exposé à la session. Contournement utilisé pour le contour de carte, le
cuivre/l'épaisseur et les règles de conception : édition directe par script (même interpréteur
`KICAD_PYTHON`) — `pcbnew.LoadBoard` + `pcbnew.PCB_SHAPE` sur `Edge.Cuts` pour le contour,
`BOARD_DESIGN_SETTINGS` (`ds.m_MinClearance`, `ds.m_TrackMinWidth`, `ds.m_ViasMinSize`,
`ds.m_MinThroughDrill`, toutes en unités internes = nanomètres, `pcbnew.FromMM`/`ToMM`) pour les
règles, puis `board.Save(...)`. Les classes de réseaux (KiCad 10) ne sont **pas** dans le
`.kicad_pcb` mais dans le `.kicad_pro` (clé `net_settings.classes` et
`net_settings.netclass_patterns`, liste de `{"netclass": ..., "pattern": ...}` assortie par nom de
réseau) : édition JSON directe la plus simple, `BOARD_STACKUP`/`NETCLASS` ne sont pas exposés
proprement par les bindings SWIG de ce poste (`GetStackupDescriptor()` renvoie un `SwigPyObject`
opaque, pas une classe Python utilisable). La vérification visuelle du PCB se fait par
`kicad-cli pcb export svg --exclude-drawing-sheet --page-size-mode 2 --mode-single` (cadre la page
sur le contour de carte, contrairement à l'export schématique) puis rendu en PNG par Edge headless
(même méthode que pour le schéma).

## Placement automatique des champs : `tools/kicad_place_fields.py`

À lancer après avoir posé les composants d'une feuille (et avant de relire le rendu) :
`python tools/kicad_place_fields.py <feuille>.kicad_sch [--refs R1,R2] [--dry-run]`.
Règles par type de symbole (voir l'en-tête du script) : résistance/condensateur horizontal = textes
au-dessus, vertical = à gauche alignés à droite ; GND = Valeur sous le triangle, alimentations = au-dessus,
Référence des symboles de puissance masquée ; transistor = à droite ; circuit intégré = Référence au-dessus
et Valeur en dessous ; angle du champ = (360 − rotation) % 360 pour 90/270. Le script teste les collisions
(fils, autres symboles, étiquettes, textes déjà placés) et prend le premier emplacement libre.
**À chaque placement manuel nécessaire, améliorer ce script plutôt que de corriger à la main**
(demande de l'utilisateur). Limite connue : des rangées de résistances horizontales espacées de moins de
7,62 mm ne laissent pas la place à deux lignes de texte (prévoir ce pas à la conception de la page).

## Saisie rapide d'une grande feuille : `tools/kicad_add_items.py`

Pour une feuille à nombreuses liaisons (microcontrôleur : 25 étiquettes, ~55 fils), poser les composants par
`batch_add_components` (champs non placés : `auto_position_fields: false`), relever les broches avec
`get_schematic_pin_locations`, écrire un `spec.json` (fils, étiquettes hiérarchiques, étiquettes locales,
croix NC, jonctions) et lancer `python tools/kicad_add_items.py <feuille>.kicad_sch spec.json` ; puis
`python tools/kicad_place_fields.py <feuille>.kicad_sch` ; puis ERC et rendu. Un composant tourné ou déplacé
après coup se corrige en modifiant le fichier (position `(at ...)`) puis en relançant `kicad_place_fields.py`.
Pas d'espacement inférieur à 12,7 mm entre condensateurs verticaux voisins sur un bus (sinon leurs textes
se chevauchent). Papier A3 : remplacer `(paper "A4")` par `(paper "A3")` dans le fichier de la sous-feuille
juste après `create_hierarchical_subsheet`.

**Pas minimal entre composants voisins (règle de conception de page).** `kicad_place_fields.py` signale
« ESPACEMENT » quand deux passifs voisins sont trop serrés pour que leurs textes tiennent. Valeurs à
retenir dès la conception d'une page (0603, police 1,27 mm) : condensateurs ou résistances **verticaux** côte à
côte : au moins 12,7 mm (15,24 mm si une valeur dépasse 6 caractères) ; résistances **horizontales** en
colonne : au moins 10,16 mm ; un symbole de puissance GND sous un composant ajoute environ 5 mm. Choisir ces
pas **avant** de placer, pas après.

**Texte accentué dans les symboles et empreintes.** Le serveur `mixelpixx/KiCAD-MCP-Server` ouvre les fichiers
en cp1252 : un accent (ou un caractère chinois d'un import EasyEDA) dans une description, un champ
« Manufacturer » ou un nom de feuille est écrit en double encodage (« accÃ©lÃ©romÃ¨tre »), ou fait échouer
l'ouverture de la feuille (« 'charmap' codec can't decode byte »). Écrire en ASCII tout ce qui passe par
`create_symbol`, `create_footprint`, `create_hierarchical_subsheet`, et nettoyer les imports EasyEDA.
Contrôle : `grep -P '[^\x00-\x7F]' *.kicad_sch lib_*.kicad_sym lib_*.pretty/*`.

**Avertissement « Ce fichier a été créé par une version plus ancienne de KiCad ».** Le serveur écrit les
feuilles avec un numéro de version de format ancien (`version 20260101`). KiCad 10.0.8 les ouvre mais
prévient. À lancer à la fin d'une session de saisie, sur chaque feuille :
`kicad-cli sch upgrade <feuille>.kicad_sch` (met à jour vers `20260306`, sans changer le contenu ; vérifié :
ERC toujours à 0). Faire de même avec `kicad-cli sym upgrade lib_<projet>.kicad_sym` si la bibliothèque est
signalée.

## Image sur une page dédiée (synoptique) : `tools/kicad_add_image_sheet.py`

KiCad n'importe que des images bitmap dans un schéma (pas de SVG). Méthode utilisée pour le synoptique de Boomrone :

1. Dessin en SVG par un script du dépôt (`tools/gen_synoptique_boomrone.py <sortie.svg>`), qui reprend les repères réels du schéma (J1, U1 à U7, Q1 à Q8...).
2. Rendu en PNG sans outil à installer : Edge en mode sans fenêtre, `msedge.exe --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=<L>,<H> --screenshot=<sortie.png> file:///<chemin>.svg` (fond blanc ; relire l'image avant import).
3. `python tools/kicad_add_image_sheet.py <dossier_projet_kicad> <image.png>` crée la feuille A3 (image à 300 ppp, mise à l'échelle et centrée), ajoute sa case à la racine (premier emplacement libre) ; puis `python tools/kicad_build_root.py <dossier>` (qui conserve la case, la feuille n'ayant aucune broche). Idempotent : relancé, il ne remplace que l'image.
4. Vérifier : `kicad-cli sch erc` (0 violation) et un export PDF de la hiérarchie (page 12 pour Boomrone). Le bloc `(image ...)` se met au format `(at cx cy) (scale s) (uuid) (data "base64"...)` ; l'échelle 1 = taille native à 300 ppp.

## Reprendre le travail sur un autre poste (checklist)

1. Cloner le dépôt ; installer KiCad 10, Node.js 18+, Python 3.11+ ; refaire la section « Mise en route sur une nouvelle machine » plus haut (serveur `mixelpixx/KiCAD-MCP-Server`, venv basé sur le Python de KiCad, déclaration dans `~/.claude.json`, redémarrer la session).
2. Outils Python des scripts du dépôt (aucun n'est dans le dépôt, tout est machine-local) : `kicad-cli` est livré avec KiCad (`<KiCad>\bin\kicad-cli.exe`) ; pour rendre une page en image, un petit venv avec `pypdfium2` et `pillow` ; pour importer une pièce d'EasyEDA/LCSC, un venv avec `easyeda2kicad` (`easyeda2kicad --lcsc_id Cxxxxx --full --output <dossier>/ee`).
3. Mémoire de Claude : elle est locale au poste. Les préférences de l'utilisateur sont donc copiées dans `CLAUDE.md` § 10 ; l'état du projet est dans `projets/<nom>/reprise.md`, les décisions dans `journal-decisions.md`, les doutes dans `registre-doutes.md`.
4. Vérifier que tout fonctionne : `python tools/check_traceability_V2.py projets/boomrone --gate --phase conception` (OK attendu) et `kicad-cli sch erc projets/boomrone/hardware/kicad/proj_boomrone/proj_boomrone.kicad_sch -o rapport.txt` (0 violation attendue).
5. Projet KiCad : toujours l'ouvrir par `proj_boomrone.kicad_pro` (les chemins `${KIPRJMOD}` des bibliothèques en dépendent) ; fichier `*.kicad_prl` (réglages d'affichage locaux) volontairement non versionné.
6. Les fiches techniques PDF (`projets/*/Datasheets/`) sont ignorées par Git (volumineuses) : les recopier à la main sur le nouveau poste (elles servent à vérifier brochages et empreintes ; plusieurs manquent déjà : PMW3901MB, buzzer, voir DOU-185 et DOU-206 dans `registre-doutes.md`).
