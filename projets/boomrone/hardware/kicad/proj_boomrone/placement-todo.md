# A faire - placement de la carte Boomrone

Notes de travail (mises a jour le 2026-11-05, soir). Ce n'est pas un document de methode : aucune
decision ici (les decisions vont dans `journal-decisions.md`, apres accord de l'utilisateur).

## 2026-11-06 (apres-midi) : banc comparatif des outils de placement - A LIRE EN PREMIER
Veille en ligne puis banc de 6 pistes (un agent par piste), juge commun et resultats dans
`projets/boomrone/hardware/kicad/proj_boomrone/_bench_placement/` (versionne en partie, ajoute avec `git add -f` :
juge, entree, cartes placees et routees, metriques, rapports, scripts ; `PROTOCOLE.md`, `resultats/<piste>/RAPPORT.md`). Conclusions publiees en artefact (claude.ai/artifact/Qr6qJDKjEH11h5tco5z3Eh).
Points cles, non decisionnels (aucune DEC) :
- **Bug** : `tools/kicad_apply_placement.py` ecrit l'angle du modele tel quel ; le modele tourne en sens horaire,
  KiCad en sens inverse -> toute piece tournee de 90 deg est retournee de 180 deg dans KiCad. Angle a ecrire :
  `(2 * angle_lu_a_l_extraction - angle_modele) % 360`. NON corrige dans le depot (attente accord utilisateur).
- Un placeur a regles de 279 lignes (`_bench_placement/outils_pistes/regles_simples/place.py`) bat le moteur :
  valide, 23/23 decouplages < 5 mm, 97,4 % route (moteur corrige : 85,5 %), 17 s.
- 4 empreintes ont des pastilles hors courtyard (BZ1 1,66 mm, U7 0,70, J1 0,24, LED1 0,11) : cause des
  courts-circuits apres placement.
- Le serveur MCP KiCad est en backend IPC : il agit sur la carte OUVERTE dans KiCad (piste MCP non mesuree).
- Smart App Control bloque tout executable non signe compile sur ce poste (SA-PCB).
- A trancher par l'utilisateur : geler moteur global + catalogue de decouplage ? (contredit le choix du 2026-11-06).

## Fait le 2026-11-05
- Contour lu sur *Edge.Cuts*, ancres = empreintes verrouillees, debords exemptes automatiquement.
- Cout incremental (`incremental.py`), parite 0 ecart, x45 par pas.
- Regle de decouplage a 5 mm (`--decoupling`), fichier `decouplage.json` (agent hardware).
- Suivi en direct (`--live`, `viewer/index.html`), couleurs par bloc, chevelu, paires de decouplage.
- Decoupe automatique d'un bloc a plusieurs ancres (DES-007 « Circuit de puissance des moteurs » en 4 blocs moteur).
- Pose des blocs en rectangles rigides (`assemble_blocks`), recuit global plus doux.
- Remise en etat faisable par relaxation locale (`spread_resolve`) au lieu d'un repavage complet.
- Meilleur resultat (10 strategies) : cout 4327, cablage 1250 mm, 340 croisements, 15 mm de
  depassement de decouplage (le meme test sans regle : 5014, 2275 mm, 830, 371 mm).

## A verifier / en cours
- Test des 10 strategies avec la relaxation locale (`spread_resolve`) : comparer a 4327.
- DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option » et DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V » ne tiennent pas comme rectangles rigides
  (laisses a la relaxation et au recuit) : essayer de les poser par groupes, ou accepter.
- La remise en etat faisable avant le recuit global degrade encore le decouplage (80 -> 268 mm)
  parce que l'etat de depart a ~93 mm2 de recouvrement et ~102 mm2 hors contour. Piste :
  penalite progressive (poids de la contrainte croissant pendant le recuit) au lieu d'une remise
  en etat brutale ; ou meilleure pose des blocs pour partir presque faisable.

## Fait le 2026-11-06
- Regles `eloigner` et `bord` ajoutees au moteur (`--rules`), test de parite dans `tests/`. Non
  lancees sur la carte : aucune distance sourcee dans le projet (isolements a `null`, reponse 5 ;
  pas de bord impose, reponse 6 ; U7 et J1 sont deja des ancres).

## Etat au 2026-11-06 (soir) : placement par etapes, a reprendre

Methode de travail retenue avec l'utilisateur : on valide **une etape a la fois sur image**, avant la suivante.
1. **Phase 1, petits groupes par bloc** (VALIDEE par l'utilisateur, a garder telle quelle).
2. **Phase 2, un rectangle rigide par groupe, poses sur la carte** (en cours, image a critiquer).
3. **Phase 3, ajustement** (recuit : composants et groupes un par un) : pas encore refaite dans cette methode.

Commandes (extraction d'abord, Python embarque KiCad, voir README) :
```bash
python modules/kicad/tools/pcb_optimize_placement.py extract projets/boomrone/hardware/kicad/proj_boomrone/proj_boomrone.kicad_pcb --out-dir <dossier>
python modules/kicad/tools/pcb_optimize_placement.py groupes    <dossier>/extract.json --out-dir <dossier>/g  --config modules/kicad/tools/pcb_placement/examples/config_parallele.json --decoupling projets/boomrone/hardware/kicad/proj_boomrone/decouplage.json --rules projets/boomrone/hardware/kicad/proj_boomrone/regles_actives.json   # phase 1 : une image par bloc
python modules/kicad/tools/pcb_optimize_placement.py rectangles <dossier>/extract.json --out-dir <dossier>/p2 --config ... --decoupling ... --rules ...                                                                                                    # phases 1 + 2 : phase2_rectangles.png
```
Code : `groupes_view.py` (phase 1 et 2, trous libres, refonte d'un groupe dans une boite), `hierarchy.py`.

Fait aujourd'hui :
- Regles `eloigner` et `bord` (voir README) ; `regles_actives.json` : U2 rotation 0 et centre (3 mm), isolements
  I-01 (8 mm), I-02 (6 mm), I-03 (8 mm) en valeurs d'essai ; proximite C6/C7/C9-J1 retiree (choix de l'utilisateur).
- Phase 1 corrigee : un groupe ne subit que les regles dont tous les composants sont dans le groupe
  (`rules_within`, aussi pour le recuit de bloc) ; liens condensateur-circuit au partitionnement
  (`decoupling_link_weight`, 2.0) ; `group_restarts` (6 essais par groupe dans la commande `groupes`, 1 par defaut
  dans le pipeline complet). Constat : sans ces regles croisees, DES-009 « Régulateur de 3,0 V et pont de mesure de la tension » passe de 92 a 47 mm2 d'emprise.
- Phase 2 : 20 ordres de pose (`assemble_blocks(..., order_noise)`, retourne les groupes sans place) ; pour un
  groupe sans place, recherche des plus grands trous libres (`free_rectangles`) et phase 1 refaite avec un but de
  forme (`optimize_group_in_box`).

Resultat de la phase 2 (carte 50 x 50 mm) : 15 groupes sur 16 poses ; **groupe g2 de DES-011 « Circuit du voyant RGB et du buzzer »** (Q5, Q6, Q7, R9 a R14, 65 mm2 de
composants) ne tient pas : le seul trou assez grand fait 9,5 x 7,5 mm (71 mm2) et 30 essais n'ont pas donne de
disposition sans recouvrement. Recouvrement residuel 63 mm2. La carte est remplie a 61 % par les composants.

A faire ensuite (l'utilisateur doit choisir) :
- Groupe g2 de DES-011 « Circuit du voyant RGB et du buzzer » : le couper en deux sous-groupes (Q5, Q6, Q7 / R9 a R14) et reessayer, ou passer a l'ajustement.
- Critiquer l'image de la phase 2 (emplacement des groupes par rapport aux reseaux et aux regles ; `regles` = 119 mm de
  depassement dans la meilleure disposition, plus que le plein pipeline : les groupes sont poses avant que les
  regles de proximite globales agissent).
- Phase 3 d'ajustement, puis `apply` sur une copie du PCB, relue dans KiCad.
- Valider le plein pipeline avec les corrections de phase 1 (`rules_within` etc.) : comparer au dernier essai (cout
  4694 ; meilleur precedent 4327), non refait.
- Etat du PCB dans le depot : U2 verrouille en (25 ; 25) (fait par l'utilisateur), U4 deplace.

Ameliorations du moteur (generiques) : `modules/kicad/tools/pcb_placement/TODO.md`.

## Points ouverts cote utilisateur
- Taille de la carte : 50x50 mm (essai) contre 40x35 mm (ARC-013 « Carte électronique JLCPCB, câblage et assemblage »),
  DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie » reste ouvert ; ne pas ecrire de DEC avant confirmation.
- Fiches en **anglais** a deposer : PMW3901MB (U4) et PB-03F (U7) ; 16 appariements de decouplage
  « a verifier » en dependent.
- Distance de decouplage : 5 mm = valeur d'essai, aucune fiche ne donne de mm.
- Questions de l'agent : C8 pres de FB1 ou de l'entree de U5 ? Penalite de proximite pour C12
  (PA0) et C31 (NRST) ?
- `min_clearance_mm` = 0,3 mm : a confirmer avec les regles de fabrication JLCPCB avant de le
  reduire.
