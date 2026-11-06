# Piste kicad_tools (rjwalters/kicad-tools 0.27.0, MIT) - RAPPORT

Statut : **échec de validité** (aucune variante valide). L'outil fonctionne mais ne produit pas de placement légal sur cette carte dense (61 % d'occupation).

## Installation
- `python -m venv resultats\kicad_tools\_outils\venv` puis `pip install "kicad-tools[placement]==0.27.0"` : 48 s, aucun échec de dépendance sous Windows / Python 3.13.
- Backend C++ (`kct build-native`) non installable : pas de compilateur (cl, g++, cmake absents). Tout tourne en Python pur, lent (environ 0,5 s/itération en seed force-directed, jusqu'à 11 s/itération en seed `current`).

## Fonctionnalités pertinentes
- `kct optimize-placement` : stratégies `cmaes` (défaut) et `bayesian` (extra non installé, non testé). Les forces dirigées ne servent que de graine (`--seed force-directed|random|current`).
- Pièces verrouillées respectées (attribut locked ; `--anchor-weight` pondère les réseaux qui les touchent). Le juge confirme : 0 ancre bougée, U2 à 0°, aucune face changée.
- Contour lu dans Edge.Cuts (`--require-outline`).
- Découplage : détection automatique (24 condensateurs vers 16 broches sur 3 rails), terme de coût `decoupling` + passe « snap » finale. Ne lit PAS notre `decouplage.json` ni `regles_actives.json` (pas d'isolements I-01..I-03).
- Autres : `--route-check` (routeur A* intégré), `--hv-domains` (creepage), non utilisés.

## Commandes (lanceur Python : copie de l'entrée dans chaque dossier, sortie placee.kicad_pcb, `--allow-infeasible --require-outline`)
- `kicad_tools_cmaes_fd` : `--seed force-directed --max-iterations 300 --time-budget 400 --anchor-weight 3 --pad-anchored-wirelength` (435 s)
- `kicad_tools_cmaes_current` : idem avec `--seed current` (428 s ; départ = carte actuelle, composants hors carte, 5050 conflits, seulement 37 itérations)
- `kicad_tools_cmaes_fd_long` : `--seed force-directed --max-iterations 2000 --time-budget 850 --weights '{"overlap":1e9,"drc":1e6,"boundary":1e6,"decoupling":4.0}'` (866 s, 1753 itérations)
Logs dans `resultats\kicad_tools_<variante>\log.txt`.

## Juge statique
| Variante | valide | recouvrement mm2 | hors contour mm2 | HPWL mm | découplage hors 5 mm (sur 23) | excès I-01 / I-02 / I-03 mm | DRC courtyard |
|---|---|---|---|---|---|---|---|
| cmaes_fd | non | 117,5 | 3,9 | 2636 | 18 | 71,0 / 51,4 / 28,5 | 107 |
| cmaes_current | non | non relevé (404 DRC) | 19,4 | 1778 | 21 | 97,2 / 69,0 / 2,6 | 404 |
| **cmaes_fd_long (meilleure)** | non | 94,4 | 2,1 | 2567 | 22 | 46,4 / 28,2 / 18,6 | 104 |

Routage (Freerouting) lancé sur cmaes_fd seulement : coupé à 480 s, pas de .ses, donc aucune métrique. Non lancé sur les autres (invalides). Routeur A* de kicad-tools non mesuré (budget, placement invalide). Métriques détaillées : `metrics.md` de chaque dossier de variante.

## Constat
- Écart d'évaluation : le moteur interne annonce un recouvrement final de 1,03 mm2 (fd) et 0 (long, restent drc=1 et boundary=3.00), le juge en mesure 94 à 117 (courtyards KiCad). Son « faisable » ne signifie pas valide chez nous.
- Le snap de découplage ne déplace qu'une partie des condensateurs et crée de nouveaux conflits.
- Aucune règle d'isolement du projet prise en compte.

## Avis
- Maturité : installation triviale, énorme CLI, documentation abondante, mais optimiseur CMA-ES générique en Python pur, lent, sans backend natif ici, et échec sur carte dense.
- Intégration : facile (fichiers KiCad lus/écrits sans KiCad, pièces verrouillées respectées), mais il faudrait un adaptateur pour nos règles.
- Architecture « LLM pour la stratégie, outils pour la géométrie » : principe à reprendre (idées utiles : seed `current`, `--route-check`, snap des condensateurs), pas l'outil de placement tel quel.
