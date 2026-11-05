# Moteur d'optimisation du placement PCB

Moteur Python autonome pour le placement automatique des composants d'une carte KiCad,
oriente vers le routage ulterieur et la compacite. Independant de KiCad pendant les calculs
(aucun module de `tools/pcb_placement/` n'importe `pcbnew`) : KiCad n'intervient que pour
l'import initial (lecture seule) et l'export final (ecriture sur une COPIE du PCB, jamais le
fichier source).

## Principe

```
.kicad_pcb (source)                internal model              .kicad_pcb (copie, optimisee)
        |                                  |                              ^
        | kicad_tetris_extract.py         |  pcb_placement/*            |
        | (Python embarque KiCad,          |  (Python systeme,           |
        |  pcbnew, lecture seule)          |   numpy, pas de pcbnew)     |
        v                                  v                              |
   extract.json  --------------->  optimisation (hierarchy/optimizer) -> best_solution.json
                                                                           |
                                                            kicad_apply_placement.py
                                                            (Python embarque KiCad)
```

Reutilise l'extracteur existant `tools/kicad_tetris_extract.py` (deja ecrit pour un essai
de placement precedent, cf. `git log` / `framework/kicad-mcp-notes.md`) : geometrie
(courtyard), pastilles et reseaux, et la table bloc fonctionnel <- reference qui reprend la
hierarchie du schema (`DES-xxx`). N'utilise PAS l'outil MCP `suggest_placement` du serveur
KiCad (force-directed seul, sans partitionnement ni recuit simule, et qui a besoin d'une
session KiCad/MCP active pour chaque evaluation) : la mission demande un moteur qui calcule
hors KiCad, ce que `suggest_placement` ne permet pas par construction. Les deux outils
restent complementaires : `suggest_placement` reste la methode rapide pour un reglage manuel
ponctuel dans KiCad (cf. `framework/kicad-mcp-notes.md`), ce moteur pour une recherche
automatisee et parametrable, rejouable hors session KiCad.

## Modele interne (`model.py`)

- `Component` : reference, bloc fonctionnel (feuille de schema), rectangle d'encombrement
  (courtyard) en repere local, liste de pastilles, position/rotation courantes. **Rotation
  limitee aux multiples de 90 degres** (simplification volontaire : les rectangles restent
  alors toujours alignes aux axes, donc le test de recouvrement est un simple test de boites
  - une rotation quelconque demanderait un test SAT pour un gain de compacite marginal sur
  des boitiers majoritairement rectangulaires).
- `Net` : liste de (reference, pastille) - pas de position propre, recalculee a la volee.
- `Board` : dictionnaire de composants + reseaux, bbox globale, (dé)serialisation des
  positions.

## Hierarchie a 5 niveaux (`hierarchy.py`)

1. **Composants individuels** : places par le recuit simule (`annealing.py`), qui peut les
   translater, les faire pivoter (0/90/180/270) ou echanger deux positions.
2. **Petits groupes** : chaque bloc fonctionnel est sous-partitionne si necessaire
   (`partition.py`, bissection spectrale + raffinement Kernighan-Lin sur le graphe de
   connectivite en expansion de clique) en groupes de `max_group_size` composants max,
   places individuellement par forces dirigees (`placement.py`) puis polis par recuit.
3. **Bloc fonctionnel** : les groupes du bloc sont assembles en rigide (translation +
   rotation d'ensemble, `assemble_rigid_groups`) sans deformer leur agencement interne, puis
   un recuit fin libre repasse sur tout le bloc pour polir les jonctions entre groupes.
4. **Assemblage des blocs** : memes outils (`assemble_rigid_groups`) appliques aux blocs
   entiers les uns par rapport aux autres.
5. **Optimisation globale** : recuit sur la carte entiere
   (`run_global_annealing_with_block_moves`) qui ajoute un type de mouvement specifique :
   deplacer/tourner un **bloc entier** en rigide. Un bloc n'est donc jamais definitivement
   fige apres son placement local : il peut encore bouger, tourner et voir son contenu
   repolisse a ce niveau.

Les ancres mecaniques dures (`is_anchor` dans l'extraction, ex. connecteur batterie, moteurs,
module radio - cf. `kicad_tetris_extract.ANCHOR_REFS`) sont marquees `fixed=True` et ne sont
jamais deplacees ni tournees par le moteur, a aucun niveau.

## Fonction de cout (`cost.py`, `routability.py` integre dans `cost.py`)

Cout total pondere = somme de :
- **Surface** (`board_area`) : boite englobante de tous les composants, objectif prioritaire.
- **Longueur de cablage estimee** (`hpwl`) : demi-perimetre par reseau (HPWL), proxy standard
  rapide.
- **Congestion** (`congestion_grid`) : grille 2D, densite de segments (arbre couvrant minimal
  par reseau, pas une clique complete) + occupation physique des composants ; le score penalise
  le carre de la densite (une cellule tres chargee compte plus qu'une cellule un peu chargee).
- **Croisements** (`crossing_count`) : paires de segments de reseaux DIFFERENTS qui se
  croisent geometriquement - proxy des connexions difficiles/detours probables.
- **Vias estimes** (`via_estimate`) : la moitie du nombre de croisements (une piste sur deux
  change de couche pour eviter l'autre) - proxy grossier, pas un routage reel.
- **Accessibilite des pastilles** (`accessibility_penalty`) : penalise une pastille dont les
  4 directions (haut/bas/gauche/droite) sont toutes bloquees par un autre composant a courte
  distance.
- **Recouvrement** (`overlap_penalty`) : CONTRAINTE DURE, poids ecrasant
  (`overlap_penalty_weight`, defaut 1000x) - une solution avec un recouvrement residuel est
  `feasible=False` et n'est JAMAIS retenue comme meilleure solution si une solution faisable
  existe, quel que soit son score sur les autres criteres.

## Contour de carte fixe et contraintes mecaniques (`io_data.apply_constraints`)

Par defaut, le moteur choisit librement la taille de la carte (compacte la boite englobante
des composants). Si la carte a un contour deja impose par la mecanique (chassis, bras
moteur, dimensions arretees ailleurs dans le cycle en V), passer `--constraints
<fichier.json>` a `optimize` :

```json
{
  "outline_mm": [0.0, 0.0, 50.0, 50.0],
  "overhang_refs": ["J1", "U7"],
  "positions": {
    "M1": {"x_mm": 3.89, "y_mm": 3.89, "rotation_deg": 135, "fixed": true}
  },
  "courtyard_overrides": {
    "M1": {"courtyard_w_mm": 8.0, "courtyard_h_mm": 3.0, "courtyard_offset_x_mm": 0.0, "courtyard_offset_y_mm": 0.0}
  }
}
```

- `outline_mm` : contour FIXE (xmin, ymin, xmax, ymax) - tout composant qui en sort (hors
  `overhang_refs`) rend la solution infaisable (meme poids que le recouvrement, cf.
  `cost.out_of_bounds_penalty`).
- `overhang_refs` : references dont le debord est une decision mecanique deja prise
  (connecteur, antenne) - exemptees du contour, jamais decide par le moteur lui-meme.
- `positions` : ecrase x/y/rotation/fixed de references precises - pour des ancres dont la
  position exacte (coin de carte, bord, debord) est deja connue plutot que laissee a
  l'extraction du PCB courant.
- `courtyard_overrides` : corrige la geometrie d'une reference si celle de l'extraction est
  fausse/provisoire (ex. empreinte de substitution). Applique avant `positions`.

Aucune de ces valeurs n'est devinee par le moteur : toutes viennent de contraintes
mecaniques deja tranchees par l'utilisateur (cf. le cas Boomrone plus bas, DOU-162/DOU-204).

## Compactage deterministe (`compaction.py`)

Le recuit simule + la legalisation (poussee locale) peuvent laisser des chevauchements
residuels si le budget d'iterations est insuffisant, ET laisser de grands vides (rien ne
pousse activement a remplir l'espace - cf. retour utilisateur du 2026-11-05). Depuis cette
version, une passe de **compactage deterministe** (bottom-left-fill, repris de l'essai
`tools/kicad_tetris_placement.py`) tourne en fin de pipeline (`HierarchyConfig.use_compaction`,
`True` par defaut) : chaque composant mobile est replace par tassement autour des ancres
fixes et des composants deja poses, en respectant le contour si impose. **Garantit 0
recouvrement et 0 hors-contour par construction** (tant qu'il y a physiquement la place),
contrairement au recuit seul. Prix a payer : le resultat est un peu moins affine cote
cablage qu'un recuit qui converge parfaitement (le compactage deplace les composants apres
coup, sans regarder le cout de cablage). Desactivable (`use_compaction: false` dans la
config) pour revenir au comportement historique (legalisation seule) si besoin de comparer.

## Partitionnement (`partition.py`)

Bissection spectrale (vecteur de Fiedler du Laplacien, `numpy.linalg.eigh`) + raffinement
Kernighan-Lin (echange de paires tant que ca reduit le poids de coupe). Pas de dependance a
`networkx` (non installe sur ce poste) : la matrice de poids est petite (un bloc fait au plus
quelques dizaines de composants), `numpy` dense suffit.

Sur Boomrone, les blocs de haut niveau viennent deja de la hierarchie du schema (une feuille
`DES-xxx` = un bloc) : ce module ne sert qu'a sous-decouper un bloc trop gros. Pour une carte
sans cette information (`block` absent/constant), le meme algorithme peut etre utilise en
partitionnement generique de haut niveau (a cabler si besoin, `partition_refs` ne suppose
rien de specifique a Boomrone).

## Boucle d'optimisation et strategies paralleles (`optimizer.py`)

Chaque **strategie** (une graine aleatoire) execute plusieurs **cycles** : placement complet
(`hierarchy.optimize_board`) -> evaluation -> comparaison a la meilleure solution FAISABLE
connue -> on recommence (nouvelle graine de cycle = nouveau point de depart par forces
dirigees) jusqu'a `stopping.max_cycles`, `stopping.no_improve_cycles` sans amelioration, ou
`stopping.time_budget_s`. Plusieurs strategies tournent en parallele
(`ProcessPoolExecutor`, `n_parallel_strategies`) ; la meilleure solution FAISABLE toutes
strategies confondues est retenue (`best_of`). Si aucune strategie n'est faisable (carte trop
dense pour la config donnee), le dernier essai est quand meme ecrit pour diagnostic.

## Configuration (`config.py`)

`EngineConfig`, serialisable en JSON (`--config fichier.json` de la ligne de commande), avec
tous les poids de cout, les tailles/iterations de chaque niveau de la hierarchie, les
parametres du recuit (temperatures initiale/finale, iterations), les criteres d'arret et le
nombre de strategies paralleles. Valeurs par defaut pensees pour une carte type Boomrone
(~100 composants, quelques cm2) ; voir les docstrings des champs pour leur role. Un essai
rapide (moins d'iterations, une seule strategie) donne une idee de la structure obtenue en
quelques dizaines de secondes ; la qualite finale (surface compacte, 0 recouvrement) demande
les valeurs par defaut ou plus (plusieurs minutes a quelques dizaines de minutes selon le
nombre de composants et de strategies paralleles).

## Resultat valide sur Boomrone (2026-11-05)

Essai sur l'extraction reelle des 107 composants de `proj_boomrone` (snapshot pris avant la
remise a zero du `.kicad_pcb` demandee ce jour-la ; le PCB du projet est reste vide, cet essai
a tourne sur une copie hors du depot). Config `examples/config_qualite.json` (= les valeurs
par defaut de `EngineConfig`), 2 strategies paralleles x 3 cycles chacune :

| | Surface | Cablage (HPWL) | Croisements | Vias estimes | Recouvrement |
|---|---|---|---|---|---|
| PCB d'origine (snapshot) | ~2900 mm2 | - | - | - | - |
| 6 essais (2 strategies x 3 cycles) | 4871 a 5522 mm2 | 1298 a 2370 mm | 176 a 510 | 88 a 255 | **0 sur les 6** |
| Meilleur retenu | **4871 mm2** (1,7x l'origine) | 1384 mm | 176 | 88 | 0 |

Temps de calcul total : 1292 s (~21,5 min) pour les 6 essais sur un poste de bureau (pas de
GPU). Trois bugs ont ete trouves et corriges pendant cette validation (voir l'historique git
de ce paquet si besoin de detail) : l'echelle du placement par forces dirigees qui explosait
pour un petit groupe, une contamination par un type numpy qui cassait la serialisation JSON,
et surtout - le plus important - un groupe/bloc contenant une ancre mecanique fixe (moteur,
connecteur batterie, module radio) etait deplace comme un corps rigide alors que
`rigid_transform` ignore deja les composants fixes en son sein : le groupe perdait sa rigidite
a chaque iteration et ses membres libres derivaient a plus de 100 mm de l'ancre en quelques
dizaines d'iterations. Les groupes contenant une ancre sont maintenant immobiles au niveau
assemblage (section "Hierarchie" plus haut).

## Limites connues (honnetes, pas de pretention a un routeur)

- **Rotations a 90 degres seulement** (voir plus haut) : un composant ne peut pas etre
  place a un angle quelconque meme si ca liberait de la place.
- **HPWL/MST/croisements sont des proxys**, pas un routage reel : une solution bien notee
  ici peut quand meme presenter des difficultes de routage non anticipees (vias empiles,
  regles de longueur appairee, plan de masse troue...). Le moteur sert a preparer un
  placement FACILITANT le routage, pas a le remplacer - il est explicitement prevu pour etre
  complete plus tard par un vrai moteur de routage autonome (cf. mission).
- **Pas de prise en compte des couches** au-dela du proxy "vias estimes" : une carte
  multicouche avec des contraintes d'empilement specifiques n'est pas modelisee.
- **La congestion est une grille uniforme** (taille de cellule fixe, defaut 2 mm) : ne
  distingue pas un contournement obligatoire (sous un connecteur par exemple) d'une simple
  zone chargee.
- **Accessibilite simplifiee** : 4 directions cardinales sondees a une distance fixe, pas une
  vraie analyse d'encombrement local.
- `kicad_tetris_extract.py` porte une table `REF_TO_BLOCK` ecrite en dur pour Boomrone (les
  proprietes Sheetname/Sheetfile des footprints ne sont pas renseignees par la
  synchronisation schema->PCB utilisee sur ce projet, cf. l'en-tete du script) : a refaire
  si de nouveaux composants sont ajoutes au schema, ou a remplacer par une lecture propre de
  ces proprietes si une synchronisation future les renseigne.

## Utilisation

Le Python de KiCad 10 (seul a importer `pcbnew`) est cherche dans l'ordre : option
`--kicad-python`, variable `KICAD_PYTHON`, puis le venv `~/.venvs/kicad-mcp` du poste (aucun
chemin propre a un poste dans ce depot). Le Python systeme a besoin de `numpy` et `matplotlib`.

```bash
# 1. Extraction (Python embarque KiCad, a cause de pcbnew)
python tools/pcb_optimize_placement.py extract <proj.kicad_pcb> --out-dir resultats/

# 2. Optimisation (Python systeme, pas besoin de pcbnew)
python tools/pcb_optimize_placement.py optimize resultats/extract.json --out-dir resultats/ \
    --config tools/pcb_placement/examples/config_qualite.json

# 3. Application sur une COPIE du PCB (Python embarque KiCad)
python tools/pcb_optimize_placement.py apply <proj.kicad_pcb> resultats/best_solution.json \
    <proj_optimise.kicad_pcb>
```

Sorties de l'etape 2, dans `--out-dir` : `best_solution.json` (positions + metriques),
`toutes_les_strategies.json` (comparaison, pour reprendre/comparer, section 9 de la
mission), `comparaison.png` (avant/apres), `rapport.md` (metriques lisibles).

`proj_optimise.kicad_pcb` est un nouveau fichier : ouvrir ce fichier dans KiCad pour relire
visuellement le resultat AVANT de l'adopter (verification visuelle obligatoire du projet,
cf. `framework/kicad-mcp-notes.md`) ; rien n'est ecrase automatiquement.


## Mise a jour du 2026-11-05 (soir) : ce qui a change depuis les sections ci-dessus

Ces points remplacent les passages correspondants plus haut quand ils se contredisent.

### Entrees lues dans KiCad (plus de liste en dur)
- **Contour** : lu sur la couche *Edge.Cuts* (`outline_mm` dans `extract.json`), plus besoin de
  `placement_constraints.json` pour le contour.
- **Pieces fixes** : toute empreinte **verrouillee** dans KiCad (clic droit > *Locked*, ou touche
  `L`) est une ancre fixe. `ANCHOR_REFS` n'est plus utilise.
- **Debords** : une piece fixe qui depasse du contour est exemptee automatiquement
  (`io_data.auto_overhang`).
- **Blocs** : un bloc qui contient plusieurs pieces verrouillees est decoupe en un sous-bloc par
  ancre (`io_data.split_blocks_by_anchor`) : `DES-007` donne `-M1` a `-M4`, chaque composant
  etant rattache a l'ancre la plus proche dans le schema (reseaux de 8 pastilles au plus).

### Pipeline (`hierarchy.optimize_board`)
1. Chaque bloc, separement et dans un repere arbitraire : groupes (<= 10), forces dirigees,
   legalisation, recuit, assemblage rigide des groupes, recuit du bloc.
2. **Pose des blocs sur la carte** (`assemble_blocks`) : rectangles rigides, du plus grand au plus
   petit, a l'emplacement libre le plus proche de ce a quoi ils sont relies, avec la rotation
   (0/90/180/270) qui minimise le cablage vers l'existant. Un bloc qui contient une piece
   verrouillee reste en place (ses composants sont deja tires vers ses ancres) et sert
   d'obstacle. Sans contour impose : ancien assemblage par forces dirigees.
3. Legalisation puis **remise en etat faisable** avant le recuit global.
4. Recuit global (mouvements de composants et de blocs entiers, 40 % de blocs, temperature de
   depart 1,5 mm).
5. Remise en etat faisable finale.

### Remise en etat faisable (`compaction.compact`)
Un composant qui se recouvre ou depasse n'est plus « teleporte » : (1) `spread_resolve`, relaxation
locale - les paires qui se recouvrent sont ecartees, le deplacement etant partage entre les deux
(les petits cedent plus, une piece verrouillee ne bouge pas), les parois ramenent vers l'interieur,
la poussee se propage de proche en proche ; (2) repli `compact_minimal` (place libre la plus
proche, balayage vectorise) ; (3) repli `_compact_repack` (repavage complet, plus gros d'abord).
Cause du changement : le repavage complet defaisait le travail du recuit (condensateurs de
decouplage eloignes de leur circuit, blocs eclates).

### Cout incremental (`incremental.py`)
Meme fonction de cout que `cost.total_cost`, mise a jour seulement pour ce qu'un deplacement
change (paires recouvrantes, reseaux touches, segments modifies de l'arbre couvrant, cellules de
congestion, pastilles voisines). Parite verifiee a 0 ecart sur des deplacements aleatoires ; ~2,4
ms par pas contre ~110 ms. La congestion utilise une grille a origine fixe (valeur absolue ~7 %
plus basse que `cost.congestion_grid`). Resynchronisation complete tous les 1500 commits.

### Regle de decouplage (`--decoupling decouplage.json`)
Penalite par mm au-dela de `distance_max_mm` (5 mm par defaut, valeur de projet, pas de fiche)
entre le centre du condensateur et la broche d'alimentation la plus proche de son circuit (groupes
de condensateurs equivalents acceptes). Poids `weight_decoupling` (10 par mm). Fichier produit par
l'agent `electronique-hardware` a partir du schema et des fiches ; il porte la source et la
certitude de chaque appariement. Sans l'option, aucun effet.

### Suivi en direct (`--live`)
`optimize --live` ecrit des instantanes JSON (`live.py`) et sert `viewer/index.html` sur
`http://127.0.0.1:8765` (option `--port`, pause apres le calcul `--live-hold-s`). La page montre le
carre de la carte, le bloc en cours au centre et les autres en grappes sur les cotes, puis les
vraies positions, le chevelu (arbre couvrant par reseau), les paires de decouplage (vert/rouge),
la couleur par bloc, les mesures et un menu de strategie. Accessible depuis le PC seulement.

### Couleurs et rapports
`comparaison.png` colore chaque bloc (palette de 14 couleurs, legende, pieces verrouillees
hachurees) ; `rapport.md` donne le depassement de decouplage.

### Configurations d'exemple
`config_rapide.json` (2 strategies), `config_parallele.json` (10 strategies), `config_qualite.json`.
Defauts modifies : `sa_global_t0` 1,5 (au lieu de 6), `block_move_prob` 0,4 (au lieu de 0,15).
Le Python de KiCad 10 est cherche dans l'ordre : `--kicad-python`, `KICAD_PYTHON`,
`~/.venvs/kicad-mcp`. Le Python systeme a besoin de `numpy` et `matplotlib`.

### Resultats de reference (Boomrone, 107 composants, contour 50 x 50 mm, 10 strategies)
| | Sans regle (coup 1) | Regle, ancien pipeline | Pipeline du soir |
|---|---|---|---|
| Cout | 5014 | 7513 | 4327 |
| Cablage | 2275 mm | 1985 mm | 1250 mm |
| Croisements | 830 | 676 | 340 |
| Depassement de decouplage | 371 mm | 274 mm | 15 mm |
Temps : 388 s, 413 s, 517 s.
