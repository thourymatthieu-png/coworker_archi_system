# A faire - moteur de placement PCB (generique)

Ameliorations du moteur, valables pour tout projet. L'etat du placement d'un projet donne est dans
son dossier (ex. `placement-todo.md` dans le dossier KiCad du projet Boomrone). Les chiffres
cites viennent de l'essai sur Boomrone (107 composants), a titre d'exemple.

## Suggestions (par priorite)
1. **Autres regles de placement, cas par cas** (fichier `regles_placement.json` par projet, une
   regle = un terme de cout, mise a jour incrementale) :
   - `reseau_critique` : poids multiplicateur et longueur maximale (retour d'un DC/DC, horloge,
     SPI rapide, mesure analogique) ;
   - `boucle` : minimiser l'encombrement d'une boucle de courant (inductance, diode,
     interrupteur d'un hacheur) ;
   - `eloigner` : distance minimale entre un groupe bruyant et un groupe sensible ;
   - `proximite` : deux composants a rapprocher (quartz et microcontroleur) ;
   - `bord` : composant impose sur un bord (antenne, connecteur).
   (`eloigner` et `bord` sont faits, voir le README.)
   Chaque regle porte sa source (fiche, page) et sa certitude ; les regles viennent de l'agent
   `electronique-hardware` (voir « Informations d'implantation » dans sa fiche), validees par
   l'utilisateur.
2. **Cohesion des blocs** : terme de regroupement par bloc (dispersion encore ~10 mm).
3. **Vides** (~33 % de la carte libre) : poser les gros composants d'abord, puis remplir les
   trous ; eventuellement un terme de remplissage faible.
4. **Vitesse** : moins d'iterations aux niveaux groupe et bloc ; ou compiler les boucles chaudes
   (Numba, non installe). 10 strategies : ~517 s.
5. **Verifications a l'`apply`** : ouvrir une copie du PCB dans KiCad et juger visuellement ;
   verifier R1 (deborde un peu a droite sur un essai).
6. **Tests dans le depot** : le test de parite cout incremental / `total_cost` (300 deplacements
   aleatoires) est dans un fichier temporaire ; le ranger dans `modules/kicad/tools/pcb_placement/tests/`.
7. **Suivi en direct** : accessible depuis le PC seulement ; une option pour l'ouvrir au reseau
   local (a decider : exposition d'un serveur) ou pour exporter des images regulieres.
8. **Limites connues du moteur** : rotations multiples de 90 deg seulement ; pas de couches ;
   congestion sur grille uniforme (voir le README).

