# Notes sur le MCP KiCad — bugs connus et méthode

Ce document existe pour que ces constats survivent à un changement de machine ou de session
(contrairement à la mémoire d'une session Claude Code, qui est locale). Lu par `electronique-hardware`
avant toute saisie de schéma KiCad.

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

**Ne jamais conclure sur l'horizontalité ou le chevauchement d'un texte par la seule lecture des
coordonnées — toujours vérifier par un rendu visuel.** Exporter en SVG (`kicad_schematic export_svg`),
copier le fichier dans un dossier du projet (pas un dossier hors projet, sinon le rendu reste une
« snapshot statique » et `computer screenshot` échoue), `navigate` vers le `file:///...svg`, puis
`computer screenshot` (zoomer sur les zones douteuses). Supprimer le SVG temporaire après coup.

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
