# Piste `regles_simples` — flux « industriel » automatisé

Statut : **réussi** (carte valide, 0 recouvrement, 23/23 découplages à moins de 5 mm, 97,4 % routé). Non décisionnel.

## Ce qui a été fait
Un placeur de 279 lignes, sans optimiseur global : `tools/bench_regles_simples/place.py` (dans le worktree
`.claude/worktrees/agent-a4d6e4555712692d8`, non commité). Il réutilise tel quel `kicad_tetris_extract.py`,
`kicad_apply_placement.py` et le moteur `pcb_placement` (copies du dépôt principal, dans `tools/bench_regles_simples/`),
seulement pour lire la carte (`io_data.load_board`, `apply_decoupling`, `apply_active_rules`), les formes (`world_bbox`,
`pad_world_pos`) et les mesures (`cost`). Aucun recuit.

Règles, dans l'ordre :
1. Pièces verrouillées (J1, M1 à M4, U2, U7) = fixes, marquées dans une grille d'occupation (pas 0,05 mm, marge 0,3 mm).
2. Pièces principales (U*, Q*, D*, J*, SW1, BZ1, LED1, FB1, C6, C7, C8 : 29 pièces mobiles), une à une, la plus liée aux
   pièces déjà posées d'abord. Grille de 1 mm sur toute la carte x 4 rotations, puis affinage à 0,25 mm. Score = distance
   pastille -> pastille voisine la plus proche (réseaux de 8 pastilles ou moins, hors GND) + 30 x manque d'isolement
   (I-01 à I-03). Chaque pièce laisse un « halo » libre (2,2 mm pour les circuits, 0,6 à 1 mm pour Q/D/J) pour ses futurs
   satellites. Une pièce principale hérite des groupes d'isolement de ses satellites (ex. U5 à cause de R20, R21, C12).
3. Condensateurs de decouplage.json : pour chaque broche candidate, spirale à 0,25 mm autour de la broche, 4 rotations,
   score = distance pastille d'alimentation -> broche + 1,2 mm par condensateur déjà affecté à cette broche (répartition).
   Les condensateurs à une seule broche candidate passent en premier.
4. Autres passifs et points de test : le plus lié d'abord (ceux qui sont dans une règle d'isolement avant les autres),
   spirale autour de la pastille voisine du réseau ; sans lien, près du centre de leur bloc.
Pas de polissage final.

Commandes exactes (X = dossier `resultats\regles_simples`, kicad-venv = `C:\Users\quent\.venvs\kicad-mcp\Scripts\python.exe`) :
```
kicad-venv tools\bench_regles_simples\kicad_tetris_extract.py X\depart.kicad_pcb X\extract_in.json
python tools\bench_regles_simples\place.py X\extract_in.json entree\decouplage.json entree\regles_actives.json X\solution.json
kicad-venv tools\bench_regles_simples\kicad_apply_placement.py entree\proj_boomrone.kicad_pcb X\solution.json X\placee.kicad_pcb
python eval\bench_eval.py statique X\placee.kicad_pcb --piste regles_simples
python eval\bench_eval.py routage  X\placee.kicad_pcb --piste regles_simples
```
(`depart.kicad_pcb` = copie de l'entrée.) Versions : Python 3.13 + numpy, KiCad 10.0.6 (pcbnew), juge et Freerouting 2.5.0
du banc. Installation : aucune. Temps de calcul du placeur : **15 à 35 s** (17 s pour la version finale), un seul coeur.
Temps de travail effectif : environ 1 h, dont une bonne part à comprendre le piège de rotation ci-dessous. Le routage a
attendu plusieurs fois le verrou (autres pistes), mais a duré 134 s une fois lancé.

## Piège important découvert (concerne tout le banc)
Le moteur (`model.py`) tourne avec `x' = x cos - y sin` (horaire à l'écran, y vers le bas), alors que KiCad compte les
angles dans l'autre sens. L'extracteur ne le voit pas sur les pièces à 0 degré, mais `kicad_apply_placement.py` écrit
l'angle du modèle tel quel : une pièce « tournée de 90 degrés » dans le modèle est tournée de 270 degrés dans KiCad (et
inversement), donc pastilles et courtyards (J2 a un courtyard décentré) ne sont plus où le modèle croit. Premier essai :
29 mm2 de recouvrement vus par le juge alors que mon modèle disait 0. Correction dans `place.py` : écrire `(-rot) % 360`
pour les pièces mobiles (toutes à 0 degré au départ). Les autres pistes qui passent par le moteur et ce script
d'application ont probablement le même défaut sur les rotations de 90/270 : à vérifier.
Aussi : le juge compte `silk_overlap` dans `drc_courtyard` (81 ici : recouvrements de sérigraphie, pas de courtyard) ;
le recouvrement de courtyard réel est de 0 (moteur et DRC).

## Résultats et variantes
| Variante | Principe | Décou. hors 5 mm | I-01 / I-02 / I-03 (mm) | HPWL |
|---|---|---|---|---|
| **`regles_simples`** (meilleure, routée) | halos x 1,0 | 0 | 0,33 / 3,96 / 14,88 | 1265 |
| `regles_simples_h05` (statique seul) | halos x 0,5 | 5 (8,7 mm) | 0,0 / 5,9 / 8,34 | 1142 |
| `regles_simples_h15` (statique seul) | halos x 1,5 | 0 | 13,6 / 17,5 / 15,2 | 1290 |

Halo trop petit : plus de place pour les condensateurs (découplage rompu) ; trop grand : les satellites partent loin et
violent les isolements. Variantes non routées (non meilleures). Ce réglage a été fait à la main, sur cette carte seulement.

Reste de I-03 : environ 6,7 mm de M1 et M2 (fixes) à U7, inévitables. Le reste vient de condensateurs moteur (C3, C5, C9...)
rangés au centre bas faute de place près des transistors.

## Métriques du juge (copie de metrics.md)
| Metrique | Valeur |
|---|---|
| valide | True |
| recouvrement_mm2 | 0.0 |
| hors_contour_mm2 | 0.0 |
| hpwl_mm | 1265.0 |
| arbre_couvrant_mm | 1355.9 |
| croisements_chevelu | 385 |
| decouplage_hors_5mm | 0 |
| decouplage_excès_total_mm | 0.0 |
| decouplage_distance_moy_mm | 2.82 |
| regles_excès_mm | proximite U2 0.0 ; I-01 0.33 ; I-02 3.96 ; I-03 14.88 |
| drc_courtyard | 81 (en réalité silk_overlap) |
| routage.proportion_routee | 0.974 |
| routage.non_connectes_avant / apres | 227 / 6 |
| routage.longueur_pistes_mm | 1977.34 |
| routage.vias | 115 |
| routage.erreurs_drc_routage | copper_edge_clearance 29, clearance 18, via_dangling 7, shorting_items 1 |
| routage.duree_s | 134.4 (statut termine) |

Pour mémoire, `etat_actuel` : 3917 mm de pistes, 133 vias, 95,6 % routé (mais hors contour).

## Ce que l'outil sait et ne sait pas faire pour notre cas
- Découplage : bien, c'est son point fort. Pastille d'alimentation (jamais le centre), corps hors du circuit (grille
  d'occupation), répartition entre broches candidates. Distance moyenne 2,8 mm. Le choix de la broche est glouton.
- Pièces fixes : respectées. Règles : isolements pris en compte à chaque pose, mais sans retour arrière : le premier qui
  prend la place gagne ; les violations restantes viennent de l'ordre de pose.
- Ne sait pas : arbitrer globalement (un satellite posé tôt peut bloquer un autre), regrouper les chaînes de signal,
  orienter les connecteurs, limiter les croisements du chevelu (385, contre 452 à l'état actuel : pas d'objectif dédié),
  tenir une distance au bord pour le routage (29 erreurs `copper_edge_clearance` : marge de 0,3 mm au contour seulement).

## Avis franc
Pour 280 lignes et 20 s de calcul, c'est bon : valide du premier coup, découplage parfait, longueur de pistes divisée
par deux par rapport à l'état actuel. Mais c'est un placement correct, pas optimisé : isolements pas tous respectés, pas
de vision d'ensemble, réglages (halo, poids) tâtonnés pour cette carte. À 61 % d'occupation, la difficulté tient dans
quelques pièces que la règle gloutonne place selon l'ordre de pose. Bon point de départ pour un humain ou pour
initialiser un optimiseur ; pas une solution finale.

## Ce qu'apporterait un humain fixant ~15 pièces critiques avant le script
Probablement le meilleur gain : U1, U4, U3, J2, U5, U6, BZ1, Q1 à Q4, D1 à D4 et le côté batterie (C6, C7, C8, FB1).
Un humain mettrait d'emblée les 4 groupes moteur dans leurs coins avec leurs condensateurs de découplage moteur (ce que
le script rate : C2 à C5, C9 loin des Q), éloignerait U1 et la chaîne de mesure batterie (U5, R20, R21) des moteurs avant
tout, orienterait J2 (SWD) et U4 (capteur de flux) vers un bord, et garderait des couloirs de routage. Le script n'aurait
plus qu'à poser les ~70 satellites, ce qu'il fait bien. Coût humain estimé : 15 à 20 min dans KiCad (estimation, non
mesurée).
