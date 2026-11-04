# Notes sur le MCP KiCad — bugs connus et méthode

Ce document existe pour que ces constats survivent à un changement de machine ou de session
(contrairement à la mémoire d'une session Claude Code, qui est locale). Lu par `electronique-hardware`
avant toute saisie de schéma KiCad.

## Méthode : bilan de bibliothèque avant tout schéma

Avant de saisir le moindre schéma, faire un bilan de bibliothèque sur toute la nomenclature du
projet : pour chaque composant actif, vérifier qu'un **symbole** ET une **empreinte** existent
(bibliothèques standard KiCad, ou à créer/importer depuis LCSC/EasyEDA) et lever les manques.
Le schéma, puis le routage, ne viennent qu'après ce bilan — pas de contournement improvisé
découvert bloc par bloc pendant la saisie (constat du test Boomrone, DES-011 : pas de symbole
« LED RGB anode commune » standard, pas d'empreinte pour la LED SZYY1615RGB-B ni le buzzer
SMD-9650-3327, découverts seulement pendant la saisie de ce bloc).

## Mise en route sur une nouvelle machine

- Installer KiCad (testé avec KiCad 10).
- Le serveur MCP `kicad` (outil `kicad_schematic_edit`, basé sur `kicad-sch-api`, pur Python) ne lit
  pas le `sym-lib-table` de KiCad : il cherche seulement `KICAD_SYMBOL_DIR` / `KICAD9_SYMBOL_DIR` /
  `KICAD8_SYMBOL_DIR` / `KICAD7_SYMBOL_DIR` (pas `KICAD10_SYMBOL_DIR`). Sans ces variables, les
  symboles de base (`Device:R`, `Device:C`, `Switch:SW_Push`, `power:GND`, etc.) ne sont pas trouvés.
  **À refaire sur chaque machine** : ajouter `KICAD_SYMBOL_DIR` et `KICAD_FOOTPRINT_DIR` (pointant
  vers le dossier `share/kicad/symbols` et `share/kicad/footprints` de l'installation locale) à la
  config du serveur MCP `kicad` dans `.claude.json`, à côté des `KICAD10_*` déjà présentes, puis
  redémarrer le serveur.

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
racine (`boomrone.kicad_sch`) sert de page d'index avec une case par bloc.
