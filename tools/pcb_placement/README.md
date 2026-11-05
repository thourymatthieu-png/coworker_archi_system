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

```bash
# 1. Extraction (Python embarque KiCad, a cause de pcbnew)
python tools/pcb_optimize_placement.py extract <proj.kicad_pcb> --out-dir resultats/ \
    --kicad-python "C:\Users\quent\.venvs\kicad-mcp\Scripts\python.exe"

# 2. Optimisation (Python systeme, pas besoin de pcbnew)
python tools/pcb_optimize_placement.py optimize resultats/extract.json --out-dir resultats/ \
    --config tools/pcb_placement/examples/config_qualite.json

# 3. Application sur une COPIE du PCB (Python embarque KiCad)
python tools/pcb_optimize_placement.py apply <proj.kicad_pcb> resultats/best_solution.json \
    <proj_optimise.kicad_pcb> --kicad-python "C:\Users\quent\.venvs\kicad-mcp\Scripts\python.exe"
```

Sorties de l'etape 2, dans `--out-dir` : `best_solution.json` (positions + metriques),
`toutes_les_strategies.json` (comparaison, pour reprendre/comparer, section 9 de la
mission), `comparaison.png` (avant/apres), `rapport.md` (metriques lisibles).

`proj_optimise.kicad_pcb` est un nouveau fichier : ouvrir ce fichier dans KiCad pour relire
visuellement le resultat AVANT de l'adopter (verification visuelle obligatoire du projet,
cf. `framework/kicad-mcp-notes.md`) ; rien n'est ecrase automatiquement.
