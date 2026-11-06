# Banc de comparaison des outils de placement — protocole

Essai d'outils, **non décisionnel** (aucun DEC/DOU). Lancé le 2026-11-06 à la demande de l'utilisateur :
comparer les solutions de placement automatique gratuites sur la carte Boomrone.

## Entrée figée (`entree/`)
- `proj_boomrone.kicad_pcb` : copie de la carte du dépôt au commit `c888873` (2 couches, 107 empreintes,
  contour 50 x 50 mm, pièces verrouillées = fixes : J1, M1 à M4, U2, U7).
- `decouplage.json`, `regles_actives.json`, `regles_placement.json` : règles d'essai du projet.

## Contraintes communes
1. Tout dans le contour *Edge.Cuts* (débords des pièces fixes exemptés), aucun recouvrement de courtyard.
2. Pièces verrouillées immobiles, U2 à 0°, toutes les empreintes sur leur face d'origine.
3. Objectifs : validité, puis routabilité, découplage (pastille à 5 mm au plus de sa broche), règles actives
   (U2 au centre à 3 mm près, isolements I-01 à I-03), longueur de câblage.

## Juge commun (`eval/`, figé, identique pour toutes les pistes)
```bash
python eval/bench_eval.py statique resultats/<piste>/placee.kicad_pcb --piste <piste>
python eval/bench_eval.py routage  resultats/<piste>/placee.kicad_pcb --piste <piste>
```
- Statique : intégrité, recouvrement et débord (moteur maison figé dans `eval/moteur`), HPWL, arbre couvrant,
  croisements du chevelu, découplage pastille → broche, règles actives, DRC KiCad.
- Routage : Freerouting 2.5.0 (Java 25 portable), 25 passes max, 480 s max, optimiseur désactivé ;
  proportion routée = 1 − connexions manquantes après / avant (DRC KiCad), longueur, vias, erreurs DRC.
- Un seul routage à la fois (verrou `routage`) ; les temps de calcul des pistes, lancées en parallèle,
  restent indicatifs.
- Correction du 2026-11-06 en cours d'essai : `drc_courtyard` comptait aussi la sérigraphie (`silk_overlap`) ;
  le juge compte désormais `courtyards_overlap` et les défauts de cuivre créés par le placement
  (`drc_defauts_placement`, au-delà de la carte d'entrée). Toutes les cartes ont été rejugées.
- Moteur maison : variantes `_rotfix` = même solution réécrite avec l'angle corrigé (bug de
  `tools/kicad_apply_placement.py`, sens de rotation inversé), via `outils_pistes/moteur_maison/apply_rotfix.py` (angle écrit =
  `(2 × angle lu − angle du modèle) mod 360`).

### Rejouer le juge sur un autre poste
Java et Freerouting ne sont pas dans le dépôt (ils étaient dans un dossier temporaire de session) :
télécharger `freerouting-2.5.0.jar` (github.com/freerouting/freerouting, il exige Java 25) et un JRE 25
portable (Adoptium Temurin), puis définir `BANC_JAVA` (chemin de `java.exe`) et `BANC_FREEROUTING`
(chemin du `.jar`). `KICAD_PYTHON` et `KICAD_CLI` se règlent de la même façon si les chemins diffèrent.
Les outils installés par les agents (`resultats/*/_outils/`) et la copie du projet pour Quilter ne sont
pas versionnés (voir `.gitignore`).

## Verrous (`eval/verrou.py`, dossier `verrous/`)
- `mcp_kicad` : obligatoire avant tout appel au serveur MCP KiCad (serveur unique partagé).
- `routage` : pris par le juge.

## Pistes
| Dossier | Piste |
|---|---|
| `etat_actuel` | Point de départ : carte du dépôt telle quelle (composants hors carte) |
| `moteur_maison` | Moteur `tools/pcb_placement` actuel (10 stratégies) |
| `regles_simples` | Flux « industriel » automatisé : pièces principales, puis satellites posés par règle |
| `kicad_tools` | kicad-tools (rjwalters, PyPI), optimiseurs de placement |
| `sa_pcb` | SA-PCB (OpenROAD, recuit simulé C++), compilé localement |
| `mcp_kicad` | Serveur MCP KiCad (mixelpixx) : outils de placement du serveur et agent LLM |
| `quilter` | Quilter (cloud) : préparation du dossier, soumission par l'utilisateur |

Non testables sur ce poste (pas de Linux/WSL/Docker, pas de GPU NVIDIA) : Cypress (NVlabs), RL_PCB.
