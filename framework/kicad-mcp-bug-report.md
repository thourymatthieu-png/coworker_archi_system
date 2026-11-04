# Rapport de problèmes — serveurs MCP KiCad testés (comparaison)

Ce rapport sert de référence pour comparer le serveur MCP KiCad en place à d'éventuelles
alternatives (voir la liste trouvée le 2026-11-04 : `kicad-mcp-pro`, `MJP-Sys/kicad-mcp-server`,
`mixelpixx/kicad-mcp-server`, `lamaalrajih/kicad-mcp`, et `mixelpixx/Konnect` ajouté le même jour).
Constats faits durant le test approfondi du projet Boomrone (DES-010 « Circuit du bouton », DES-011
« Circuit du voyant RGB et du buzzer ») pour le premier serveur (« kicad »), et durant un test séparé
sur un petit schéma jetable (hors projet Boomrone) pour les trois suivants (« kicad-pro »,
« kicad-mixelpixx » et « konnect », 2026-11-04) — pas une évaluation générale du produit dans aucun
des quatre cas. Un cinquième, `Orchis-ai-LLC/Konnect-EDA` (successeur commercial fermé de `konnect`),
a été recherché le 2026-11-04 mais n'a pas pu être testé : sa page Releases ne publie encore aucun
binaire malgré une documentation d'installation qui en suppose un.

## Référence du serveur testé

- **Paquet :** `kicad-eda-mcp` (PyPI), version **0.1.0**.
- **Dépendances déclarées :** `kicad-python`, `kicad-sch-api`, `mcp`, `psutil`, `tabulate`.
- **Exécutable :** `kicad-eda-mcp.exe` (installé dans un venv dédié, `C:\Users\quent\.venvs\kicad-mcp`).
- **Options de lancement utilisées :** `--auto-launch off --tool-mode router --enable-mutations`.
- **Version de KiCad en face :** KiCad 10.0 (Windows).
- Dépôt source non identifié avec certitude (le paquet PyPI ne liste pas de dépôt officiel dans les
  métadonnées relevées) — à retrouver si une comparaison précise de version/commit est nécessaire.

## Référence du second serveur testé

- **Paquet :** `kicad-mcp-pro`, version **4.7.0**, licence MIT.
- **Exécutable :** installé dans un venv dédié, `C:\Users\quent\.venvs\kicad-mcp-pro`.
- **Version de KiCad en face :** KiCad 10.0.6 (Windows), CLI `kicad-cli.exe` trouvée et utilisée pour
  les exports ; IPC KiCad joignable mais aucun document PCB/schéma ouvert en direct dans l'instance
  KiCad testée (`liveSchematicWrite`/`livePcbWrite` indisponibles dans ce mode — le serveur passe par
  des fichiers, pas par une édition « live » dans une fenêtre KiCad ouverte).
- Beaucoup plus large que le premier serveur : ~280 outils (gestion de projet, bibliothèque LCSC,
  schéma, PCB, DRC/ERC avec règles personnalisées, intégrité du signal/alimentation, simulation
  SPICE, export fabrication, gestion de variantes, intégration Git). Seule la partie schéma/projet a
  été testée ici, sur le même périmètre que le premier serveur.
- Un paquet optionnel manque dans ce venv : `sch_render_png` échoue (« PNG rendering requires
  CairoSVG and Pillow »). Contournement utilisé pour ce test : export SVG directement par
  `kicad-cli.exe sch export svg` (hors MCP), recadrage du `viewBox` comme pour le premier serveur.

## Référence du troisième serveur testé

- **Paquet :** `mixelpixx/KiCAD-MCP-Server` (GitHub, branche `stable`), version **2.8.3**, licence MIT.
- **Nature :** serveur hybride Node.js/TypeScript (le process MCP lui-même, SDK officiel
  `@modelcontextprotocol/sdk`) + Python (`python/kicad_interface.py`, le moteur de manipulation
  KiCad, backend `pcbnew` SWIG — les bindings Python natifs de KiCad, pas une bibliothèque tierce
  comme `kicad-sch-api`/`kicad-skip`). 244 outils déclarés.
- **Installation :** `git clone --branch stable ...`, `npm install && npm run build` (Node 18+,
  testé avec Node 24.20.0/npm 11.19.0). Côté Python, le script `setup-windows.ps1` fourni installe
  les dépendances (`requirements.txt` : `kicad-python`, `sexpdata`, `kicad-skip`, `Pillow`,
  `pymupdf`, `cairosvg`, `colorlog`, `pydantic`, `requests`, `python-dotenv`) directement dans le
  Python *embarqué* de KiCad (`<install KiCad>\bin\python.exe`), car `pcbnew` n'existe que là (un
  module compilé pour l'ABI exacte du Python embarqué — un venv basé sur le Python système ne peut
  pas l'importer). Pour ce test, contournement plus isolé que le script officiel, afin de ne pas
  toucher à l'installation KiCad existante : création d'un venv **à partir du Python de KiCad**
  (`<python de KiCad> -m venv --system-site-packages ...`), qui expose `pcbnew` via
  `--system-site-packages` sans en modifier le dossier d'origine, puis installation des dépendances
  du serveur dans ce venv. `PYTHONPATH` ne fonctionne **pas** avec le Python embarqué de KiCad pour
  ce contournement : son `sitecustomize.py` fait `sys.path = []` puis le reconstruit lui-même dès
  qu'il n'est pas lancé depuis un venv — un point à connaître avant d'essayer d'isoler un autre
  serveur basé sur `pcbnew`.
- **Test effectué sans l'inscrire dans la configuration MCP de la session** (pas de redémarrage de
  session nécessaire) : un petit client JSON-RPC stdio écrit pour l'occasion
  (`initialize`/`tools/call` ligne à ligne, SDK MCP officiel = un message JSON par ligne) a servi à
  dialoguer directement avec `node dist/index.js`, en lui passant `KICAD_PYTHON` vers le venv créé
  ci-dessus. Script jetable, non conservé dans le dépôt.

## Référence du quatrième serveur testé

- **Paquet :** `mixelpixx/Konnect` (GitHub), version **0.13.0**, licence AGPL-3.0 (gratuit pour un
  usage personnel/hobby/étudiant/projet open source — c'est le cas de ce dépôt — payant pour un usage
  commercial, voir `COMMERCIAL.md` du projet). Dépôt **archivé** par son auteur le 2026-11-02 : le
  développement continue sous le nom « Konnect-EDA », qui devient commercial à partir de sa version
  1.0 (gratuit pour l'usage personnel avec une clé gratuite, payant pour les entreprises) ; ce rapport
  teste la dernière version encore publiée sous ce dépôt-ci, pas Konnect-EDA.
- **Nature :** successeur du serveur « kicad-mixelpixx » ci-dessus, réécrit en Rust — un seul
  exécutable natif (~35 Mo) sans dépendance externe à installer, qui parle à KiCad par l'API IPC
  officielle (protobuf sur NNG) pour le PCB, et édite les fichiers `.kicad_sch` par son propre moteur
  S-expression (écriture atomique, pas de bibliothèque tierce) pour le schéma — donc sans avoir besoin
  d'une instance KiCad ouverte pour les opérations testées ici. 228 outils, organisés par « toolsets »
  chargés à la demande (`load_toolset`) pour limiter le coût en contexte d'un client LLM ; seuls deux
  toolsets (`project`, `config`) sont chargés par défaut.
- **Installation :** binaire précompilé téléchargé directement depuis la page des releases GitHub
  (`konnect-v0.13.0-x86_64-pc-windows-msvc.zip`, 13 Mo), sans compilation ni dépendance à poser — la
  plus simple des quatre installations testées. `konnect init` (non exécuté pour ce test) installerait
  des skills/agents/hooks Claude dans `~/.claude` ; évité ici pour ne pas modifier la configuration
  Claude Code de la session sans accord explicite.
- **Test effectué de la même façon que pour « kicad-mixelpixx »** : sans l'inscrire dans la
  configuration MCP de la session, via le même client JSON-RPC stdio jetable (généralisé pour accepter
  n'importe quel exécutable en argument), dialoguant directement avec `konnect.exe`.

## Résumé

**Serveur « kicad » (`kicad-eda-mcp`) :** globalement peu fiable pour une saisie de schéma précise :
plusieurs opérations échouent systématiquement (pas de contournement côté serveur), et plusieurs
autres donnent un résultat géométriquement trompeur (rotation, angle de texte) qui n'est détectable
que par un rendu visuel, pas par le texte brut renvoyé par l'outil. Les détails complets, avec
contournements, sont dans `framework/kicad-mcp-notes.md`.

**Serveur « kicad-pro » (`kicad-mcp-pro`) :** nettement plus fiable et plus complet sur les cinq
opérations rejouées (voir le tableau de résultats plus bas) — feuille hiérarchique, label sur
broche et requête de connectivité fonctionnent directement, sans contournement, et le calcul de
position de broche après rotation est fait par un outil dédié (`sch_get_pin_positions`) plutôt que
déduit empiriquement. Deux défauts subsistent cependant, l'un strictement identique à un défaut du
premier serveur (texte Référence/Valeur en miroir à 180°, non détecté par les outils de contrôle
automatiques du serveur) et l'autre de la même famille que le bug d'UUID du premier serveur mais
localisé aux sous-feuilles (chemin d'instance à un seul segment au lieu de deux dans le fichier de
sous-feuille). Voir le détail plus bas.

**Serveur « kicad-mixelpixx » (`mixelpixx/KiCAD-MCP-Server`) :** le meilleur résultat des trois
serveurs Python/SWIG sur les cinq opérations rejouées — aucune des deux limites encore présentes avec
`kicad-pro` n'a été reproduite. Le texte Référence/Valeur reste lisible (non mis en miroir) sur les
quatre rotations testées, y compris à 180°, et le chemin d'instance des sous-feuilles est écrit
correctement dès la création (deux segments, UUID racine + UUID de feuille cohérents). Contrepartie :
une installation nettement plus lourde (clone Git, build Node, et une dépendance au Python *embarqué*
de KiCad pour accéder à `pcbnew`, avec un contournement non trivial pour l'isoler proprement — voir
plus haut). Voir le détail plus bas.

**Serveur « konnect » (`mixelpixx/Konnect`) :** même résultat impeccable que `kicad-mixelpixx` sur
les cinq opérations (aucun texte en miroir, chemin d'instance de sous-feuille correct), avec en plus
l'installation la plus simple des quatre serveurs testés (un seul exécutable téléchargé, zéro
dépendance à poser) et des réponses d'outils plus riches (lecture immédiate du fichier après écriture,
angle de chaque broche, correction documentée d'un bug connu de KiCad 10.0.6 dans les coordonnées
ERC). C'est le successeur officiel de `kicad-mixelpixx`, réécrit en Rust contre l'API IPC de KiCad
plutôt que les bindings SWIG. Seul bémol : dépôt archivé le 2026-11-02, développement poursuivi sous
licence commerciale (« Konnect-EDA », gratuit pour un usage personnel/hobby après sa version 1.0).
Voir le détail plus bas.

## Serveur « kicad » — opérations cassées (erreur systématique, confirmé sur ce test)

| Opération | Symptôme | Gravité |
|---|---|---|
| `add_sheet` | `'SheetManager' object has no attribute 'add'` | Élevée — impossible de créer une feuille hiérarchique sans contournement externe (`tools/add_kicad_sheet.py`) |
| `add_label_to_pin` | Non implémentée (`'Schematic' object has no attribute 'add_label_to_pin'`) | Moyenne — contournable (`add_wire_to_pin` + `add_label`) |
| `get_net_for_pin` / `connectivity_check` | `unhashable type: 'Net'` systématique | Moyenne — contournable (ERC + relecture manuelle) |
| `add_rectangle` | `can only concatenate str (not "int") to str` | Faible — pas de cadre visuel possible par ce biais |
| `add_with_pin_at` / `align_pin` | Erreur d'argument systématique | Élevée — force un contournement lourd (composant de test jetable + lecture de fichier) pour chaque broche |
| `remove_label` | « Label not found » sur un `hierarchical_label` valide | Faible — contournable par édition directe du fichier |
| `get_pins_info` | Cassé sur le schéma testé (constaté lors de la correction de DES-011) | Moyenne — même contournement que `add_with_pin_at` |

## Serveur « kicad » — comportements trompeurs (pas d'erreur renvoyée, résultat géométriquement faux)

| Comportement | Symptôme | Gravité |
|---|---|---|
| `rotate_component` | Pas une rotation géométrique propre des broches ; comportement différent d'un type de symbole à l'autre (résistance, MOSFET, buzzer, diode tous différents) | Élevée — oblige une vérification empirique par composant de test avant toute rotation |
| Angle de champ Référence/Valeur après rotation | Doit être recalculé manuellement (`(360 - rotation) % 360`), et à 180° cette formule seule ne suffit pas, `justify` doit aussi être inversé | Élevée — cause directe de texte en miroir/illisible si non corrigé (constaté sur DES-011) |
| `kicad_workflow create_project` | UUID racine du `.kicad_sch` généré à zéro, incohérent avec le `.kicad_pro` → KiCad affiche le schéma comme vide | Élevée — contourné par `tools/fix_kicad_project_uuid.py`, mais un piège pour qui ne le sait pas |
| Sauvegarde d'une sous-feuille | `project`/`path` d'instance mal écrits à chaque `save` (nom de projet placeholder, chemin à un seul segment au lieu de deux) | Élevée — non couvert par le script de correction d'UUID racine, nécessite une correction manuelle après chaque saisie de sous-feuille |

## Test comparatif « kicad-pro » (2026-11-04, schéma jetable hors projet Boomrone)

Les cinq opérations du critère de comparaison, rejouées avec `kicad-pro` sur un projet de test créé
pour l'occasion (`kicad_create_new_project`) : une feuille hiérarchique (`sch_create_sheet`), cinq
composants dont trois tournés à 90°/180°/270° (`sch_add_component`, positions de broches lues au
préalable par `sch_get_pin_positions`), un label sur deux broches (`sch_add_pin_labels`), une requête
de connectivité (`sch_trace_net`, `run_erc`), le tout vérifié par rendu visuel (export SVG direct par
`kicad-cli`, recadrage et capture, PNG natif du serveur indisponible dans ce venv).

| Opération | Résultat avec `kicad-pro` | Comparé à `kicad` |
|---|---|---|
| Feuille hiérarchique | `sch_create_sheet` crée la feuille, l'ajoute au schéma racine et pose les pins demandées en un seul appel | Fonctionne directement ; `kicad` nécessitait un script externe (`add_sheet` cassée) |
| Label sur une broche | `sch_add_pin_labels` crée un talon de fil + label local/global/hiérarchique au nom de la broche, en évitant le chevauchement avec le corps du symbole | Fonctionne directement ; `kicad` n'avait pas l'opération (`add_label_to_pin` non implémentée) |
| Position de broche après rotation (0/90/180/270°) | `sch_get_pin_positions` calcule la position absolue exacte pour n'importe quel symbole/rotation, vérifié cohérent sur `Device:R`, `Transistor_FET:AO3400A`, `Device:Buzzer`, `Diode:SS34` | Amélioration nette ; `kicad` n'avait pas de calcul fiable (transposition empirique à vérifier composant par composant) |
| Texte Référence/Valeur après rotation à 180° | **Toujours en miroir, illisible**, constaté par rendu visuel sur `Q1` (AO3400A) et `BZ1` (Buzzer) ; non détecté par `sch_visual_qa` ni `sch_cosmetic_score` (qui ne voient que le chevauchement de texte, pas le miroir) ; `sch_fix_readability` ne corrige rien | **Même défaut que `kicad`** : la rotation à 180° reste le cas à toujours vérifier par rendu, jamais par lecture de coordonnées seule |
| Connectivité d'une broche / d'un net | `sch_trace_net` et `run_erc` fonctionnent pleinement : liste précise par feuille, par broche, avec coordonnées et UUID, sans erreur | Fonctionne directement ; `kicad` renvoyait une erreur interne systématique (`unhashable type: 'Net'`) |
| Créer un projet puis l'ouvrir dans KiCad | UUID racine du `.kicad_sch` cohérent avec le `.kicad_pro`, fichier généré par le vrai `eeschema` (pas de schéma vide) : **le bug précis du premier serveur n'est pas reproduit à la racine**. Mais le fichier de la **sous-feuille** (`bloc-test.kicad_sch`) écrit un chemin d'instance à un seul segment (`/c45e52bb-...`, l'UUID propre du fichier de sous-feuille) au lieu du chemin hiérarchique à deux segments attendu (`/<uuid racine>/<uuid feuille>`), et son `generator_version` (9.0) diffère de celui de la racine (10.0) | **Bug de même famille que `kicad`, mais limité aux sous-feuilles** : le défaut d'UUID racine de `kicad` est corrigé côté `kicad-pro`, le défaut de chemin d'instance de sous-feuille, lui, se reproduit presque à l'identique ; silencieux (non signalé par `run_erc` ni par les outils de qualité) — à vérifier par une ouverture réelle dans KiCad avant de faire confiance à une sous-feuille |

**Autres constats :**
- Installation : un venv dédié comme pour `kicad`, pas plus complexe. Un paquet optionnel manque
  pour le rendu PNG natif (`sch_render_png`) dans ce venv (CairoSVG/Pillow) ; contournable par export
  SVG via `kicad-cli` directement (déjà la méthode utilisée pour `kicad`).
- `sch_visual_qa` et `sch_cosmetic_score` détectent par la seule lecture du fichier (sans rendu)
  certains défauts de lisibilité que `kicad` ne permettait de voir que par rendu — par exemple le
  chevauchement entre le label `TEST_NET` et le symbole `GND` posé juste en dessous a été repéré
  automatiquement par ces deux outils. Ça ne remplace pas le rendu visuel (le miroir de texte à 180°
  leur échappe), mais ça réduit le nombre de rendus nécessaires pendant la saisie.
- `run_erc` donne, pour chaque violation, la feuille, la broche concernée (référence + nom/numéro),
  les coordonnées et un UUID stable — largement suffisant comme substitut à une requête de
  connectivité broche par broche.

## Test comparatif « kicad-mixelpixx » (2026-11-04, schéma jetable hors projet Boomrone)

Mêmes cinq opérations, mêmes symboles (`Device:R` ×2, `Transistor_FET:AO3400A`, `Device:Buzzer`,
`Diode:SS34`), même méthode de vérification (export SVG natif du serveur — `export_sch_svg` —
recadrage et capture), rejouées via le client stdio jetable décrit plus haut plutôt que comme outils
Claude Code enregistrés (le serveur n'a pas été ajouté à la configuration MCP de la session).

| Opération | Résultat avec `kicad-mixelpixx` | Comparé à `kicad-pro` / `kicad` |
|---|---|---|
| Feuille hiérarchique | `create_hierarchical_subsheet` crée le fichier de sous-feuille **et** l'insère dans le schéma parent en un seul appel (fusion de `create_schematic` + `add_hierarchical_sheet`) | Encore plus direct que `kicad-pro` (deux appels) ; `kicad` nécessitait un script externe |
| Label sur une broche | `connect_to_net` ajoute le talon de fil et le label au bon endroit en un appel, et renvoie `pin_location`/`label_location`/`wire_stub` pour vérification immédiate sans avoir à relire le fichier | Fonctionne directement, au même niveau que `kicad-pro` |
| Position de broche après rotation (0/90/180/270°) | `get_schematic_pin_locations` renvoie position **et angle** de chaque broche après placement réel (pas un calcul à part : interroge le composant déjà posé) | Équivalent à `sch_get_pin_positions` de `kicad-pro`, avec l'angle de broche en plus |
| Texte Référence/Valeur après rotation (0/90/180/270°) | **Toujours lisible, jamais en miroir**, vérifié par rendu visuel sur les quatre rotations (`Q1`/`BZ1` à 180° lisibles ; `D1` à 270° lisible, affiché à la verticale — comportement standard de KiCad, le texte tourne avec le symbole mais ne se retrouve jamais inversé) | **Seul des trois serveurs sans ce défaut** : `kicad` et `kicad-pro` affichent tous deux un texte en miroir à 180° |
| Connectivité d'une broche / d'un net | `get_net_connections` et `list_schematic_nets` fonctionnent pleinement, réponse concise (liste des broches par net) | Fonctionne directement, au même niveau que `kicad-pro`/`sch_trace_net` |
| Créer un projet puis l'ouvrir dans KiCad | UUID racine du `.kicad_sch` cohérent avec le `.kicad_pro`, généré par le vrai `eeschema` (version 10.0, comme la racine). Le fichier de la **sous-feuille** écrit d'emblée le chemin d'instance à deux segments correct (`/<uuid racine>/<uuid feuille>`), avec le nom de projet exact — pas de version de générateur qui diverge entre racine et sous-feuille | **Seul des trois serveurs sans le bug de chemin d'instance de sous-feuille**, y compris comparé à `kicad-pro` qui le reproduit |

**Autres constats :**
- Backend : le serveur annonce `"_backend": "swig"` dans ses réponses — il passe par les bindings
  Python officiels de KiCad (`pcbnew`), pas par une bibliothèque tierce de parsing de fichier
  `.kicad_sch`. C'est probablement ce qui explique l'absence des deux défauts (texte en miroir,
  chemin d'instance de sous-feuille) encore présents chez `kicad-pro` : la géométrie et les champs
  de texte sont calculés par le moteur KiCad lui-même, pas réimplémentés côté serveur.
- Aucune opération cassée ni erreur inattendue rencontrée sur le périmètre testé.
- Installation sensiblement plus lourde que les deux autres serveurs Python/SWIG : dépôt Git à
  cloner, build TypeScript (Node 18+), et une dépendance incontournable au Python embarqué de KiCad
  pour `pcbnew` — contrairement à `kicad`/`kicad-pro` qui s'installent comme un simple paquet PyPI
  dans un venv autonome. Le script d'installation officiel (`setup-windows.ps1`) installe les
  dépendances directement dans le Python de KiCad (modifie l'installation KiCad existante) ; un venv
  `--system-site-packages` construit à partir de ce même Python, comme fait pour ce test, l'évite.

## Test comparatif « konnect » (2026-11-04, schéma jetable hors projet Boomrone)

Mêmes cinq opérations, mêmes symboles, même méthode de vérification (export SVG natif —
`export_schematic_svg` — recadrage et capture), rejouées via le même client stdio jetable que pour
« kicad-mixelpixx », généralisé pour viser directement `konnect.exe` (binaire téléchargé depuis les
releases GitHub, pas de build).

| Opération | Résultat avec `konnect` | Comparé aux trois autres |
|---|---|---|
| Feuille hiérarchique | `add_hierarchical_sheet` crée le fichier de sous-feuille **et** l'insère dans le schéma parent en un seul appel, et patche immédiatement les chemins d'instance des symboles si le fichier existait déjà avec du contenu | Aussi direct que `create_hierarchical_subsheet` de `kicad-mixelpixx` |
| Label sur une broche | `connect_to_net` ajoute le talon de fil et le label, et renvoie la direction choisie, la position du label et les coordonnées du fil pour vérification immédiate | Équivalent à `connect_to_net` de `kicad-mixelpixx` (même nom d'outil, même comportement) |
| Position de broche après rotation (0/90/180/270°) | `get_schematic_pin_locations` renvoie position, **angle d'orientation** et longueur de chaque broche, par unité, directement depuis le composant placé | Équivalent à `kicad-mixelpixx`, légèrement plus détaillé (longueur de broche en plus) |
| Texte Référence/Valeur après rotation (0/90/180/270°) | **Toujours lisible, jamais en miroir**, vérifié par rendu visuel sur les quatre rotations (`Q1`/`BZ1` à 180° lisibles ; `D1` à 270° lisible, affiché à la verticale, même convention que `kicad-mixelpixx`) ; chaque appel `add_schematic_component` renvoie déjà la position et la rotation calculées de chaque champ (`field_placements`), avant même le rendu | **Même absence de défaut que `kicad-mixelpixx`** ; `kicad` et `kicad-pro` affichent tous deux un texte en miroir à 180° |
| Connectivité d'une broche / d'un net | `get_net_connections` et `list_schematic_nets` fonctionnent pleinement ; `run_erc` documente explicitement un bug connu de KiCad 10.0.6 (coordonnées ERC rapportées 100× trop petites, kicad#25582) et corrige la valeur avant de la renvoyer, en précisant qu'il l'a fait | Au même niveau fonctionnel que `kicad-mixelpixx`, avec une transparence inhabituelle sur un bug de KiCad lui-même plutôt que du serveur |
| Créer un projet puis l'ouvrir dans KiCad | UUID racine du `.kicad_sch` cohérent avec le `.kicad_pro`. Le fichier de la **sous-feuille** écrit d'emblée le chemin d'instance à deux segments correct (`/<uuid racine>/<uuid feuille>`), avec le nom de projet exact. Seule différence cosmétique : `(generator "konnect")` au lieu de `"eeschema"` dans l'en-tête du fichier (le serveur ne se fait pas passer pour eeschema, ce qui est plus honnête, et reste un `.kicad_sch` standard valide) | **Même absence du bug de chemin d'instance de sous-feuille que `kicad-mixelpixx`** |

**Autres constats :**
- Installation la plus simple des quatre serveurs testés : un seul exécutable téléchargé (13 Mo
  compressés), aucune dépendance à installer, aucun build. Le paquet « PCM » (gestionnaire de
  greffons KiCad) existe aussi pour une installation intégrée à l'interface KiCad, non testé ici (le
  binaire autonome suffisait pour parler MCP en ligne de commande).
- Chaque réponse d'outil est beaucoup plus détaillée que les trois autres serveurs : positions de
  chaque champ de texte (`field_placements`), chemins d'instance complets, confirmation de lecture du
  fichier après écriture (`"source":"saved_file_readback"`). Utile pour vérifier un résultat sans
  appel supplémentaire, mais verbeux — pertinent à mettre en balance avec le coût en contexte d'un
  outil agentique (le README du projet met en avant son système de « toolsets » à charger à la
  demande pour cette raison).
- Aucune opération cassée ni erreur inattendue rencontrée sur le périmètre testé ; la seule erreur
  obtenue (`toolset_not_loaded`) est un garde-fou volontaire et explicite du routeur d'outils, pas un
  bug.
- Pas testé ici : les outils PCB (nécessitent KiCad ouvert avec l'API IPC activée) et `konnect init`
  (installation de compétences/agents Claude), hors du périmètre des cinq opérations comparées.

## Recommandation (révisée après vérification du statut des dépôts)

**`konnect` et `kicad-mixelpixx` obtiennent le même résultat impeccable** sur les cinq opérations
comparées (aucun des deux défauts qui obligeaient encore `kicad-pro` à des vérifications manuelles —
texte en miroir à 180°, chemin d'instance de sous-feuille — n'a été reproduit par l'un ou l'autre).
La différence qui tranche n'est pas technique mais tient au **statut des deux projets** :

- `konnect` vient d'un dépôt **archivé** le 2026-11-02 : plus aucun correctif n'y arrivera. Son
  successeur commercial (`Konnect-EDA`, Orchis-ai-LLC) est fermé et, au 2026-11-04, ne publie encore
  aucun binaire téléchargeable (page Releases vide) — inutilisable en l'état, licence AGPL-3.0/
  commerciale à surveiller si ça change.
- `kicad-mixelpixx` (`mixelpixx/KiCAD-MCP-Server`) reste un dépôt **actif et maintenu**, licence MIT
  sans ambiguïté — Konnect lui-même le décrit comme « remains fully open (MIT) and maintained » dans
  son propre README.

**Choix retenu : `kicad-mixelpixx` pour la suite de la saisie des blocs KiCad de Boomrone**
(DES-008, DES-009, DES-004, DES-002, et reprise de DES-010/DES-011 avec ce serveur). Le prix à payer
est une installation plus lourde (clone Git, build Node, venv basé sur le Python embarqué de KiCad
pour `pcbnew`, bindings SWIG que KiCad déprécie) — mais rien de tout cela n'a posé de problème pendant
le test, et avoir un outil vivant plutôt qu'un instantané figé pèse plus lourd pour un projet qui va
encore saisir une douzaine de blocs sur plusieurs mois.

La précaution de vérification par rendu visuel après une rotation (`framework/kicad-mcp-notes.md`)
peut être allégée mais pas supprimée : seuls quatre symboles, deux rotations chacun, ont été vérifiés
ici — pas l'exhaustivité de la nomenclature Boomrone.

## Critère de comparaison utilisé pour ce test

Rejouer, avec le nouveau serveur, les mêmes opérations qui ont posé problème avec `kicad` : créer une
feuille hiérarchique, poser un label sur une broche, tourner un composant à 90°/180°/270° et vérifier
le texte par rendu, interroger la connectivité d'une broche, créer un projet puis l'ouvrir dans
KiCad. Comparer aussi la facilité d'installation/configuration (variables d'environnement,
dépendances).
