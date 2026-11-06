# Piste moteur_maison : moteur de placement du dépôt (copie de travail du dépôt principal, 2026-11-06)

Variantes : `moteur_maison` (config_parallele.json, 10 stratégies) et `moteur_maison_qualite` (config_qualite.json, 2 stratégies, 3 cycles max).
**Meilleure variante au juge : `moteur_maison_qualite`** (routage 81,6 % contre 76,7 %), bien que son coût interne soit similaire.

## Ce qui a été fait (commandes exactes, depuis le worktree)
Fichiers copiés depuis le dépôt principal (copie de travail non commitée) : `tools/pcb_placement/` (sans `__pycache__`), `tools/pcb_optimize_placement.py`, `tools/kicad_tetris_extract.py`, `tools/kicad_apply_placement.py`. Moteur non modifié.
```
python tools/pcb_optimize_placement.py extract resultats/moteur_maison/depart.kicad_pcb --out-dir resultats/moteur_maison/_travail --kicad-python C:/Users/quent/.venvs/kicad-mcp/Scripts/python.exe
python tools/pcb_optimize_placement.py optimize .../_travail/extract.json --out-dir .../_travail --config tools/pcb_placement/examples/config_parallele.json --decoupling entree/decouplage.json --rules entree/regles_actives.json
python tools/pcb_optimize_placement.py apply .../depart.kicad_pcb .../_travail/best_solution.json .../placee.kicad_pcb --kicad-python ...
python eval/bench_eval.py statique|routage .../placee.kicad_pcb --piste moteur_maison
```
Variante qualité : identique avec `config_qualite.json` (même extract.json), piste `moteur_maison_qualite`.

## Versions et temps
Python 3.13.17 (système, numpy/matplotlib), pcbnew via venv kicad-mcp (KiCad 10). Aucune installation. Extraction : quelques secondes. Calcul : **454 s** (config_parallele, rapport interne) ; **410 s** (qualité) ; lancés en parallèle d'autres pistes, donc indicatif. Apply : quelques secondes. Routage juge : 463 s (principal, atteint le plafond 480 s) et 187 s (qualité).

## Résultat interne du moteur
Principal (graine 0 retenue) : surface 3142 mm2, HPWL 1449,9 mm, croisements 365, vias 182, recouvrement 0, hors contour 0, « dépassement des règles de proximité » 39,8 mm, coût 4694,5, faisable OK.
Qualité : HPWL 1565,0, croisements 409, dépassement proximité 16,6 mm, coût 4558,1.
Note : la surface « occupée » est la boîte englobante, égale au contour 50x50 moins marge dans les deux cas (3142 mm2) : ce terme ne discrimine rien ici. L'avertissement « DES-011-voyant-buzzer et DES-005-flux-optique ne tiennent pas comme rectangle rigide » apparaît à chaque cycle.

## Juge : métriques statiques
| Métrique | moteur_maison | moteur_maison_qualite |
|---|---|---|
| valide | True | True |
| recouvrement / hors contour (mm2) | 0 / 0 | 0 / 0 |
| HPWL (mm) | 1535,2 | 1679,4 |
| arbre couvrant (mm) | 1683,1 | 1769,4 |
| croisements du chevelu | 448 | 501 |
| découplage hors 5 mm (sur 23) | 10 | 10 |
| excès découplage total / moyen (mm) | 47,37 / 6,19 | 30,15 / 5,54 |
| règles : U2 centre / I-01 / I-02 / I-03 (excès mm) | 0 / 5,19 / 0 / 11,31 | 0 / 10,03 / 0,47 / 5,71 |
| drc_courtyard (voir note) | 103 | 100 |
Intégrité : aucune ancre bougée, U2 à 0°, faces inchangées, rien de manquant (7 pièces verrouillées ignorées à l'apply, 100 positions appliquées).

## Juge : routage (Freerouting)
| | moteur_maison | moteur_maison_qualite |
|---|---|---|
| connexions manquantes avant → après | 227 → 53 | 228 → 42 |
| proportion routée | 0,767 | 0,816 |
| longueur pistes (mm) | 1484 | 2169 |
| vias | 118 | 124 |
| durée Freerouting (s) | 462,6 | 186,9 |
| erreurs DRC après routage | via_dangling 43, copper_edge_clearance 31, clearance 19, shorting 8 | copper_edge 25, clearance 16, shorting 11, via_dangling 6 |

## Les contraintes sont-elles vraiment respectées ?
- Courtyards : OUI pour les deux variantes, 0 mm2 de recouvrement selon le moteur du juge ; le DRC KiCad ne signale aucun `courtyards_overlap`. La métrique `drc_courtyard` (103 / 100) est trompeuse : elle compte les erreurs `silk_overlap` (sérigraphie), pas les courtyards.
- Contour : OUI, 0 mm2 hors carte.
- Mais le DRC KiCad de la carte placée (avant routage) montre : principal 19 `clearance` (isolement pastille-pastille), 8 `shorting_items`, 7 `copper_edge_clearance`, 10 `silk_edge_clearance`. Exemple : R13 (GND) à 0,7 mm de la pastille 6 de U7 (pièce fixe) : les courtyards ne se chevauchent pas, mais des pastilles de réseaux différents se touchent. Ces courts-circuits/isolements persistent après routage (8 et 11) : le moteur ne modélise que les courtyards (marge min_clearance 0,3 mm), pas les pastilles ni les pastilles débordant du courtyard. Il faudra les corriger à la main.
- Découplage : non respecté pour 10 condensateurs sur 23 dans les deux variantes (moyenne 6,2 / 5,5 mm contre 5 mm demandé), alors que le moteur a une pénalité de proximité. Règle I-01 et I-03 dépassées de 5 à 11 mm ; U2 au centre OK.

## Ce que l'outil sait / ne sait pas faire pour notre cas
Sait : pièces fixes (ancres), rotation verrouillée de U2, règles de découplage et règles actives (proximité/éloignement) lues en JSON, contour lu sur Edge.Cuts, pas de dépendance externe, pur Python, intégré au flux KiCad (extract/apply sans ouvrir l'interface). Ne sait pas : modéliser les pastilles/isolements cuivre réels, le débord de pastilles hors courtyard, la sérigraphie ; garantir le découplage (pénalité molle, pas de contrainte dure) ; il n'y a pas de table de blocs générique : `kicad_tetris_extract.py` embarque une table `REF_TO_BLOCK` écrite en dur pour Boomrone (extraction OK ici, « Sans bloc identifié : [] »). Aucune sortie de flux de routage dans le moteur (il ne route pas).

## Avis franc
Le moteur est le seul de la liste fiable sur la validité géométrique (0 recouvrement, 0 débord, pièces fixes respectées) et il tourne sans rien installer, mais il laisse 10/23 découplages hors tolérance et des conflits de pastilles que ses courtyards ne voient pas. Le gain de la config « parallèle » (10 stratégies) sur la config « qualité » (2 stratégies) est nul au juge : meilleure HPWL en parallèle, meilleur routage et meilleur découplage en qualité ; le coût interne n'est donc pas un bon prédicteur du routage (HPWL +9 % mais 5 points de routage en plus). 7 min de calcul pour 107 pièces est correct. Résultat à retenir comme référence honnête : ~77 à 82 % routé par Freerouting, non finissable sans reprise manuelle.

## Métriques du juge (copie de metrics.md, moteur_maison)
valide True ; recouvrement 0.0 ; hors_contour 0.0 ; hpwl 1535.2 ; arbre_couvrant 1683.1 ; croisements 448 ; découplage hors 5 mm : 10 ; excès 47.37 ; distance moyenne 6.19 ; règles {proximité U2 0.0, I-01 5.19, I-02 0.0, I-03 11.31} ; drc_courtyard 103 (voir note).
