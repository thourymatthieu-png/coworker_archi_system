# A faire - moteur de placement PCB et regles de placement

Notes de travail (mises a jour le 2026-11-05, soir). Ce n'est pas un document de methode : aucune
decision ici (les decisions vont dans `journal-decisions.md`, apres accord de l'utilisateur).

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
