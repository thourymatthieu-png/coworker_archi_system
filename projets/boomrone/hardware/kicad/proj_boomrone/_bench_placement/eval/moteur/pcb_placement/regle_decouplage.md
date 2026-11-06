# Regle de placement des condensateurs de decouplage

Construite avec l'utilisateur, cas par cas, a partir du 2026-11-06. Ce n'est PAS une decision
de projet (pas de DEC) : une methode d'outil pour `tools/pcb_placement/`, a appliquer partout
une fois stabilisee. Mise a jour a chaque nouveau cas traite.

## Principes generaux (valables pour tous les cas, ne changent pas d'un cas a l'autre)

1. **Pastille, jamais centre.** Toute proximite ou tout alignement avec une broche a decoupler
   se mesure et se cible sur la PASTILLE d'alimentation du condensateur (celle posee sur le
   reseau decouple), jamais sur le centre du composant. Erreur constatee le 2026-11-06 : aligner
   le centre sur la broche degradait la distance reelle pastille -> broche.
2. **Corps hors du composant actif : contrainte dure, separee de la proximite.** Le RECTANGLE
   D'ENCOMBREMENT COMPLET du condensateur (pas seulement sa pastille) ne doit jamais recouvrir
   le boitier du composant actif - meme quand la broche visee est EN RETRAIT du bord du boitier
   (cas constate : U1/broche 48, en retrait de 1 mm du bord). La position qui minimise la
   distance pastille -> broche est cherchee SOUS cette contrainte, jamais apres coup.

## Cas 1 : condensateur UNITAIRE (une seule broche a decoupler sur ce cote de l'IC, aucune
autre a proximite)

Trois positions candidates, departagees par la distance pastille -> broche (la plus petite
gagne, a recouvrement nul) :

- **Position 1** : petit cote du condensateur (celui qui porte la pastille d'alimentation) face
  a la broche, le corps s'etend vers l'exterieur du composant actif.
- **Position 2a** : grand cote du condensateur colle au bord du composant actif, pastille
  alignee LATERALEMENT sur la broche, corps allonge d'un cote.
- **Position 2b** : identique a 2a, corps allonge de l'autre cote (symetrique de 2a - meme
  distance pastille -> broche dans ce cas unitaire, rien ne les depart sans information de
  voisinage).

Valide visuellement le 2026-11-06 sur C32/U1 (broche 48, en retrait du bord) :
`tools/pcb_placement/README.md` ne porte pas cette image (diagramme pedagogique hors moteur,
genere par un script d'essai, non conserve dans le depot) - resultat : 0 recouvrement sur les
3 positions, Position 1 a 1,99 mm, Positions 2a/2b a 2,02 mm chacune.

## Cas 2 : PLUSIEURS condensateurs (jusqu'a 3) visant la meme broche (ou des broches tres
proches, cf. cas 3) - construits en un BLOC FIGE

**EN COURS DE REVISION le 2026-11-06 (reouvert apres un premier jet juge insuffisant) - ce qui
suit n'est PAS encore la regle retenue, seulement l'etat des essais et ce qui a ete ecarte.**

Premier jet (ecarte comme solution automatique, mais les constats restent utiles) :
- **Bloc fige** : les condensateurs (jusqu'a 3) mis en parallele, cote a cote sur leur GRAND
  cote (jamais sur le petit cote), chacun gardant son orientation "petit cote vers l'exterieur"
  (cas 1, position 1). Ce principe de construction (cote a cote sur le grand cote) N'EST PAS
  remis en cause ; ce qui est remis en cause, c'est COMMENT choisir/noter la position du bloc.
- Deux constructions comparees : **A** (tous les condensateurs cote a cote PERPENDICULAIREMENT
  a la broche, meme profondeur) et **B** (un condensateur colle au composant actif, les autres
  empiles DERRIERE lui, vers l'exterieur). Sur C28+C34 (broche 36 de U1) : A donne 2,18 mm
  chacun (total 4,36 mm, equilibre) ; B donne 2,16 et 3,86 mm (total 6,02 mm, desequilibre) -
  B reste moins bon que A dans tous les essais, y compris en essayant de requilibrer B (bloque
  par la contrainte dure du corps hors du composant actif, cf. principes generaux).
- Essai d'un critere "broche de reference" (une seule pastille du bloc prise comme cible
  principale, measuree en priorite) : pour la construction A, prendre une pastille precise comme
  reference lui donne sa meilleure distance individuelle (1,99 mm, identique au cas 1) mais
  degrade le total (4,65 mm) par rapport a la repartition equilibree (4,36 mm) - juge "pas encore
  la bonne approche" par l'utilisateur (2026-11-06).
- Constat utile, a garder : la broche CANDIDATE choisie (parmi plusieurs candidates compatibles)
  ne change PAS le score de distance obtenu - seul l'EMPLACEMENT du bloc sur le boitier change.
  Le choix de la broche candidate doit donc se faire sur un autre critere (place disponible,
  proximite du reste du groupe), pas sur cette distance.

**Nouvelle approche actee (2026-11-06) : construction MANUELLE, pas a pas, un condensateur a la
fois.** Un essai de balayage automatique (12 combinaisons : condensateur colle a l'autre,
2 positions du premier x 3 bords x 2 styles, toujours en contact reel - cf. historique git de
`tools/pcb_placement/exploration_decouplage.py`) a ete REJETE par l'utilisateur ("pour les 2
capa c'est mauvais") malgre une geometrie correcte : montrer trop de combinaisons a la fois n'est
pas la bonne methode. Regle de travail retenue :
1. Poser UN SEUL condensateur (position choisie parmi le cas 1), montrer le resultat, et
   S'ARRETER - la suite (ou mettre le condensateur suivant) vient de l'utilisateur, jamais d'un
   calcul automatique de toutes les possibilites.
2. Toute position vient d'une fonction de `tools/pcb_placement/exploration_decouplage.py`,
   executee telle quelle - jamais de calcul a la volee ailleurs ("c'est le script qui place,
   jamais toi").
3. Chaque image est ouverte dans Chrome (onglet dedie si plusieurs images doivent rester
   visibles en meme temps).

**Point de reprise (2026-11-06) :** C28 seul pose en position 1 sur la broche 36 de U1
(`scenario_une_capa_seule`, 1,99 mm) - en attente de l'instruction de l'utilisateur pour placer
C34 par rapport a ce C28 deja fixe. La regle du cas 2 sera ecrite une fois cette construction
pas a pas validee.

## Cas suivants
A completer au fur et a mesure (broches candidates differentes mais voisines dans un meme bloc,
plus de 3 condensateurs, etc. - cf. `tools/pcb_placement/TODO.md` pour l'etat des essais
precedents, remis en cause le 2026-11-06 : a reprendre une fois cette regle stabilisee sur tous
les cas).
