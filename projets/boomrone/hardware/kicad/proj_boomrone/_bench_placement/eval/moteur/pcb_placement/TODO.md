# A faire - moteur de placement PCB et regles de placement

Notes de travail (mises a jour le 2026-11-05, soir). Ce n'est pas un document de methode : aucune
decision ici (les decisions vont dans `journal-decisions.md`, apres accord de l'utilisateur).

## Repris le 2026-11-06 : methode de placement des condensateurs de decouplage reprise a zero
Le code de `place_active_and_decoupling` (position1/position2 dans `placement.py`) ecrit plus
tot le 2026-11-06 est remis en cause par l'utilisateur (resultats incoherents sur le groupe
encombre DES-002/U1) : on reprend cas par cas, en ecrivant la methode au fur et a mesure dans
`tools/pcb_placement/regle_decouplage.md` AVANT de la coder. Premier cas traite (condensateur
unitaire, cf. ce fichier) : deux bugs trouves et corriges en route (recouvrement du composant
actif quand la broche est en retrait du bord ; alignement sur le centre du condensateur au lieu
de sa pastille). Le code existant de `placement.py` n'est PAS encore remis a jour avec cette
regle - a faire une fois tous les cas types traites et valides.

Cas 2 (plusieurs condensateurs sur la meme broche / des broches voisines, cf. C28+C34 sur
U1/broche 36) : EN COURS, reouvert le 2026-11-06 apres un premier jet automatique juge
insuffisant (voir le detail et les constats utiles dans `regle_decouplage.md`, section Cas 2).

**Regles de travail actees le 2026-11-06, a appliquer pour la suite de ce cas (et des suivants) :**
1. **"C'est le script qui place, jamais toi [l'assistant] directement."** Toute position doit
   venir d'une fonction de `tools/pcb_placement/exploration_decouplage.py`, execute tel quel
   (`python tools/pcb_placement/exploration_decouplage.py`) - plus de calcul en Python a la volee
   via Bash. Si une nouvelle etape est demandee, on AJOUTE/MODIFIE une fonction dans ce script
   plutot que d'ecrire du code ailleurs.
2. **Ouvrir chaque image generee dans Chrome** (mcp__claude-in-chrome), dans son propre onglet si
   plusieurs images doivent rester visibles en meme temps (ne pas ecraser un onglet qui sert
   encore) - serveur local `python -m http.server 8899` depuis `<TEMP>/resultats_placement`
   (a relancer si la session a change : le process ne survit pas a un effacement du contexte).
3. **But revise le 2026-11-06 (en cours de session) : catalogue, pas choix manuel immediat.**
   Apres plusieurs allers-retours (construction pas a pas rejetee, puis essais de filtrage
   automatique d'une "meilleure" position), l'utilisateur a tranche : "on en choisira jamais une
   position, je veux generer tous les cas pour les avoir a disposition plus tard dans le process".
   Le script ne sert donc plus a choisir UNE position a la fois, mais a produire un CATALOGUE
   complet (image + JSON) de tous les cas valides, reutilisable plus tard par le pipeline de
   production. Regle de filtrage retenue pour ne pas noyer le catalogue de cas trivialement
   mauvais : dans un groupe de combinaisons comparables (meme position du condensateur fixe),
   ne garder que le sous-groupe de distances le plus proche, coupe au plus grand saut entre deux
   valeurs triees (fonction `_filter_largest_gap`) - PAS un seuil fixe (essaye et abandonne).

**Script d'exploration : `tools/pcb_placement/exploration_decouplage.py`** (ajoute le
2026-11-06). Ce n'est PAS le moteur de production (`hierarchy.py`) : juste l'outil qui genere les
images/catalogues pour `regle_decouplage.md`, ecrit dans `<TEMP>/resultats_placement/exploration/`.

**METHODE RETENUE EN FIN DE SESSION (2026-11-06 soir) : methode EN CHAINE.** Apres un episode de
chevauchements constates (l'ancienne approche "groupes de condensateurs calcules independamment
+ condensateurs par defaut en arriere-plan" pouvait superposer un condensateur par defaut avec un
cas en cours d'exploration - corrige une premiere fois en retirant au vol le condensateur en
conflit, mais juge "tres mauvais" par l'utilisateur), la methode a ete reecrite pour etre
correcte PAR CONSTRUCTION : "on pose la 1ere capa (x combinaison), on pose la 2eme capa a cote
des x combinaison ce qui donne Y nouvelle combinaison, on pose la x eme capa a cote ... etc,
toujours en minimisant les distances des pin actives et en ignorant dans le nouveau lot de
combinaison les 'saut' de distance." Implementee dans `_chain_cap_cases(ic, pin, caps_chain)` :
- Le 1er condensateur de la chaine utilise le cas 1 (3 positions, `_single_cap_cases`).
- Chaque condensateur suivant est colle contre N'IMPORTE LEQUEL des condensateurs DEJA POSES DANS
  CETTE BRANCHE (jamais contre un condensateur d'une autre branche - c'est ce qui garantit
  l'absence de chevauchement), teste sur 3 bords x 2 styles par reference possible, filtre par
  recouvrement (IC + tous les condensateurs deja poses dans la branche), puis par le plus grand
  saut entre deux distances triees (`_filter_largest_gap` - distance = la plus courte vers un
  condensateur deja pose dans la branche).
- Chaque combinaison finale est une branche complete et auto-coherente (jamais de recomposition
  apres coup entre branches independantes) : `{"snaps": [(cap, snap), ...], "label": str,
  "links": [(a, b), ...]}`.
Fonctions cles actuelles : `_single_cap_cases`, `_chain_cap_cases`, `_filter_largest_gap`,
`_draw_panel_full` (dessine TOUS les condensateurs de la combinaison + traits rouges fins
broche<->pastille et pastille<->pastille, SANS la valeur chiffree dessus - demande utilisateur :
le trait seul suffit), `scenario_page_complete` (assemble tout - image `page_complete.png` +
catalogue `page_complete_cas.json`). Anciennes fonctions (`scenario_cap_seul`,
`scenario_une_capa_seule`, `scenario_c34_contre_c28`, `scenario_c34_au_plus_pres`,
`scenario_c34_toutes_options`, `_pair_cap_cases`) gardees dans le fichier a titre d'historique
mais plus appelees depuis `main()`.

**Etat exact en fin de session (2026-11-06 soir), point de reprise :** `main()` appelle
`scenario_page_complete(board)`, perimetre **U1/broche 36, chaine C28 -> C34 -> C33 -> C27**
(C33 et C27 choisis arbitrairement comme 3e/4e condensateurs d'exemple pour exercer la methode -
AUCUNE decision reelle sur quel condensateur va sur quelle broche : "c'est l'agent hardware qui
donne les recommandations, mais pour notre cas on apprend juste a placer des capa de decouplage").
Avec 4 condensateurs dans la chaine : **166 combinaisons finales**, image 1764x18522 px (2,4 Mo) -
l'utilisateur a choisi explicitement de TOUT garder plutot que de limiter ("Garder tout"), malgre
la taille illisible d'un coup d'oeil. Catalogue JSON a jour avec les 166 cas (positions x/y/
rotation de chaque condensateur par combinaison).

**Prochaines etapes possibles (aucune choisie, a discuter avec l'utilisateur a la reprise) :**
- Elargir a une 5e broche ou a une 5e capacite dans la meme chaine.
- Elargir aux broches restantes du MCU (24, 20/VREF+, 21/VDDA avec C29/C30/C32/C35 - PAS encore
  traitees avec la methode en chaine : l'episode de chevauchement avait eu lieu avec l'ancienne
  methode "groupes + defauts" sur ces broches-la, donc a refaire en chaine si repris).
- Rendre l'image plus lisible pour un grand nombre de cas (166+) : vignettes plus grandes/
  espacees, ou un decoupage en plusieurs fichiers - propose par l'assistant, pas encore demande
  par l'utilisateur.
- Decider, une fois la methode stabilisee, comment reinjecter ce catalogue dans le moteur de
  production (`hierarchy.py` / `placement.py`), qui n'est pas encore mis a jour avec cette regle.

## Frictions et points d'attention pour la suite (session du 2026-11-06, a lire avant de reprendre)
Cette session a beaucoup tatonne sur LA METHODE plutot que sur le resultat final - resume des
allers-retours pour ne pas les refaire :
1. **Construction pas a pas (un condensateur a la fois, l'utilisateur dit ou mettre le suivant)
   a ete essayee en premier, puis ABANDONNEE** : l'utilisateur a explicitement dit "on en
   choisira jamais une position, je veux generer tous les cas pour les avoir a disposition plus
   tard dans le process" - ne pas revenir a un mode de choix interactif un cas a la fois.
2. **Un balayage complet (12 combinaisons) montre d'un coup a ete REJETE une premiere fois**
   ("pour les 2 capa c'est mauvais") avant que la demande finale "montrer TOUS les cas" ne revienne
   - la encore, accepter que la demande finale de l'utilisateur peut sembler contredire une
   reponse plus ancienne : ce n'est pas une contradiction, c'est une methode qui s'est precisee
   (voir le detail distance-min vs saut de distance au point 4).
3. **Toute tentative de choisir automatiquement UNE "meilleure" position (distance minimale
   stricte, puis tolerance relative fixe de 20 %) a ete rejetee** ("il y a des cas en trop", "le
   script devrait retourner 4 cas pas 2") : le bon critere, valide par l'utilisateur, est le PLUS
   GRAND SAUT entre deux distances triees (`_filter_largest_gap`), pas un seuil absolu ou relatif
   fixe a l'avance.
4. **Erreur structurelle a eviter si on reprend l'ancienne approche "groupes + condensateur par
   defaut en arriere-plan"** : elle produit des chevauchements des qu'un groupe en cours
   d'exploration et un groupe "par defaut" (fige sur son 1er cas) occupent le meme espace dans
   certaines combinaisons. Preferer TOUJOURS la methode en chaine (point de reprise ci-dessus),
   qui est correcte par construction (chaque combinaison est une branche complete, jamais de
   recomposition de morceaux calcules separement).
5. **Toujours passer par le script, jamais de calcul a la volee** ("c'est le script qui place,
   jamais toi [l'assistant] directement") - verifie plusieurs fois par l'utilisateur ("tu utilise
   toujours bien que le script... ?"). Toute nouvelle regle discutee doit etre codee dans
   `exploration_decouplage.py` (nouvelle fonction ou modification) puis le script relance, jamais
   de position injectee a la main.
6. **Toujours ouvrir l'image dans Chrome** (onglet dedie), jamais seulement affichee en ligne a
   l'assistant - meme si l'assistant la regarde aussi pour verifier avant de la montrer.
7. **Affichage** : tous les condensateurs de la combinaison affiches ensemble (pas un seul a la
   fois), point rouge sur chaque broche ciblee, trait rouge fin broche<->pastille et
   pastille<->pastille SANS texte de distance dessus (demande explicitement retiree apres un
   premier essai avec le chiffre affiche).

## Fait le 2026-11-05
- Contour lu sur *Edge.Cuts*, ancres = empreintes verrouillees, debords exemptes automatiquement.
- Cout incremental (`incremental.py`), parite 0 ecart, x45 par pas.
- Regle de decouplage a 5 mm (`--decoupling`), fichier `decouplage.json` (agent hardware).
- Suivi en direct (`--live`, `viewer/index.html`), couleurs par bloc, chevelu, paires de decouplage.
- Decoupe automatique d'un bloc a plusieurs ancres (DES-007 en 4 blocs moteur).
- Pose des blocs en rectangles rigides (`assemble_blocks`), recuit global plus doux.
- Remise en etat faisable par relaxation locale (`spread_resolve`) au lieu d'un repavage complet.
- Meilleur resultat (10 strategies) : cout 4327, cablage 1250 mm, 340 croisements, 15 mm de
  depassement de decouplage (le meme test sans regle : 5014, 2275 mm, 830, 371 mm).

## A verifier / en cours
- Test des 10 strategies avec la relaxation locale (`spread_resolve`) : comparer a 4327.
- `DES-002 microcontroleur` et `DES-005 flux optique` ne tiennent pas comme rectangles rigides
  (laisses a la relaxation et au recuit) : essayer de les poser par groupes, ou accepter.
- La remise en etat faisable avant le recuit global degrade encore le decouplage (80 -> 268 mm)
  parce que l'etat de depart a ~93 mm2 de recouvrement et ~102 mm2 hors contour. Piste :
  penalite progressive (poids de la contrainte croissant pendant le recuit) au lieu d'une remise
  en etat brutale ; ou meilleure pose des blocs pour partir presque faisable.

## Fait le 2026-11-06
- Regles `eloigner` et `bord` ajoutees au moteur (`--rules`), test de parite dans `tests/`. Non
  lancees sur la carte : aucune distance sourcee dans le projet (isolements a `null`, reponse 5 ;
  pas de bord impose, reponse 6 ; U7 et J1 sont deja des ancres).

## Fait le 2026-11-06 (reprise des essais)
- Retour utilisateur : les "tas" du placement par forces dirigees sont desordonnes (aucun
  alignement horizontal/vertical). Ajout de `placement.align_rows` : range chaque petit
  groupe (sans ancre) en rangees alignees apres son placement (force dirigee + recuit +
  legalisation), appele dans `hierarchy.optimize_group` (`HierarchyConfig.align_rows`,
  `EngineConfig.align_rows`, defaut `True`, desactivable pour comparer a l'ancien aspect).
  Non encore relance sur la carte (a verifier en direct, phase 1, avant de rejuger la phase 2).

## Etat au 2026-11-06 (soir) : placement par etapes, a reprendre

Methode de travail retenue avec l'utilisateur : on valide **une etape a la fois sur image**, avant la suivante.
1. **Phase 1, petits groupes par bloc** (VALIDEE par l'utilisateur, a garder telle quelle).
2. **Phase 2, un rectangle rigide par groupe, poses sur la carte** (en cours, image a critiquer).
3. **Phase 3, ajustement** (recuit : composants et groupes un par un) : pas encore refaite dans cette methode.

Commandes (extraction d'abord, Python embarque KiCad, voir README) :
```bash
python tools/pcb_optimize_placement.py extract projets/boomrone/hardware/kicad/proj_boomrone/proj_boomrone.kicad_pcb --out-dir <dossier>
python tools/pcb_optimize_placement.py groupes    <dossier>/extract.json --out-dir <dossier>/g  --config tools/pcb_placement/examples/config_parallele.json --decoupling projets/boomrone/hardware/kicad/proj_boomrone/decouplage.json --rules projets/boomrone/hardware/kicad/proj_boomrone/regles_actives.json   # phase 1 : une image par bloc
python tools/pcb_optimize_placement.py rectangles <dossier>/extract.json --out-dir <dossier>/p2 --config ... --decoupling ... --rules ...                                                                                                    # phases 1 + 2 : phase2_rectangles.png
```
Code : `groupes_view.py` (phase 1 et 2, trous libres, refonte d'un groupe dans une boite), `hierarchy.py`.

Fait aujourd'hui :
- Regles `eloigner` et `bord` (voir README) ; `regles_actives.json` : U2 rotation 0 et centre (3 mm), isolements
  I-01 (8 mm), I-02 (6 mm), I-03 (8 mm) en valeurs d'essai ; proximite C6/C7/C9-J1 retiree (choix de l'utilisateur).
- Phase 1 corrigee : un groupe ne subit que les regles dont tous les composants sont dans le groupe
  (`rules_within`, aussi pour le recuit de bloc) ; liens condensateur-circuit au partitionnement
  (`decoupling_link_weight`, 2.0) ; `group_restarts` (6 essais par groupe dans la commande `groupes`, 1 par defaut
  dans le pipeline complet). Constat : sans ces regles croisees, DES-009 passe de 92 a 47 mm2 d'emprise.
- Phase 2 : 20 ordres de pose (`assemble_blocks(..., order_noise)`, retourne les groupes sans place) ; pour un
  groupe sans place, recherche des plus grands trous libres (`free_rectangles`) et phase 1 refaite avec un but de
  forme (`optimize_group_in_box`).

Resultat de la phase 2 (carte 50 x 50 mm) : 15 groupes sur 16 poses ; **DES-011 g2** (Q5, Q6, Q7, R9 a R14, 65 mm2 de
composants) ne tient pas : le seul trou assez grand fait 9,5 x 7,5 mm (71 mm2) et 30 essais n'ont pas donne de
disposition sans recouvrement. Recouvrement residuel 63 mm2. La carte est remplie a 61 % par les composants.

A faire ensuite (l'utilisateur doit choisir) :
- DES-011 g2 : le couper en deux sous-groupes (Q5, Q6, Q7 / R9 a R14) et reessayer, ou passer a l'ajustement.
- Critiquer l'image de la phase 2 (emplacement des groupes par rapport aux reseaux et aux regles ; `regles` = 119 mm de
  depassement dans la meilleure disposition, plus que le plein pipeline : les groupes sont poses avant que les
  regles de proximite globales agissent).
- Phase 3 d'ajustement, puis `apply` sur une copie du PCB, relue dans KiCad.
- Valider le plein pipeline avec les corrections de phase 1 (`rules_within` etc.) : comparer au dernier essai (cout
  4694 ; meilleur precedent 4327), non refait.
- Etat du PCB dans le depot : U2 verrouille en (25 ; 25) (fait par l'utilisateur), U4 deplace.

## Suggestions a faire (par priorite)
1. **Autres regles de placement, cas par cas** (fichier `regles_placement.json` par projet, une
   regle = un terme de cout, mise a jour incrementale) :
   - `reseau_critique` : poids multiplicateur et longueur maximale (retour d'un DC/DC, horloge,
     SPI rapide, mesure analogique) ;
   - `boucle` : minimiser l'encombrement d'une boucle de courant (inductance, diode,
     interrupteur d'un hacheur) ;
   - `eloigner` : distance minimale entre un groupe bruyant et un groupe sensible ;
   - `proximite` : deux composants a rapprocher (quartz et microcontroleur) ;
   - `bord` : composant impose sur un bord (antenne, connecteur).
   Chaque regle porte sa source (fiche, page) et sa certitude ; les regles viennent de l'agent
   `electronique-hardware` (voir « Informations de placement » dans sa fiche), validees par
   l'utilisateur.
2. **Cohesion des blocs** : terme de regroupement par bloc (dispersion encore ~10 mm).
3. **Vides** (~33 % de la carte libre) : poser les gros composants d'abord, puis remplir les
   trous ; eventuellement un terme de remplissage faible.
4. **Vitesse** : moins d'iterations aux niveaux groupe et bloc ; ou compiler les boucles chaudes
   (Numba, non installe). 10 strategies : ~517 s.
5. **Verifications a l'`apply`** : ouvrir une copie du PCB dans KiCad et juger visuellement ;
   verifier R1 (deborde un peu a droite sur un essai).
6. **Tests dans le depot** : le test de parite cout incremental / `total_cost` (300 deplacements
   aleatoires) est dans un fichier temporaire ; le ranger dans `tools/pcb_placement/tests/`.
7. **Suivi en direct** : accessible depuis le PC seulement ; une option pour l'ouvrir au reseau
   local (a decider : exposition d'un serveur) ou pour exporter des images regulieres.
8. **Limites connues du moteur** : rotations multiples de 90 deg seulement ; pas de couches ;
   congestion sur grille uniforme (voir le README).

## Points ouverts cote utilisateur
- Taille de la carte : 50x50 mm (essai) contre 40x35 mm (ARC-013 « Carte electronique JLCPCB,
  cablage et assemblage »), DOU-162 « Implantation mecanique de la carte, du connecteur et de la
  batterie » reste ouvert ; ne pas ecrire de DEC avant confirmation.
- Fiches en **anglais** a deposer : PMW3901MB (U4) et PB-03F (U7) ; 16 appariements de decouplage
  « a verifier » en dependent.
- Distance de decouplage : 5 mm = valeur d'essai, aucune fiche ne donne de mm.
- Questions de l'agent : C8 pres de FB1 ou de l'entree de U5 ? Penalite de proximite pour C12
  (PA0) et C31 (NRST) ?
- `min_clearance_mm` = 0,3 mm : a confirmer avec les regles de fabrication JLCPCB avant de le
  reduire.
