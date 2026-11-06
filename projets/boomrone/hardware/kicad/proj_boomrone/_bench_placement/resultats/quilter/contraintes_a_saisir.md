# Contraintes à saisir dans Quilter (carte Boomrone)

Essai non décisionnel. Source : `entree/decouplage.json` et `entree/regles_actives.json` du banc.
Interface Quilter : étape de « Circuit Comprehension » (section *Bypass Capacitors*) puis « Define your own constraints »
(*Custom Component Proximity*, changelog du 1er mai 2026 : composant restreint, composant parent, broche cible, distance maximale).
Les libellés exacts de l'interface n'ont pas pu être vérifiés (compte non créé) : à ajuster à l'écran.

## 0. Ce qui est déjà acquis par le fichier (rien à saisir)
| Besoin | Mécanisme Quilter | État |
|---|---|---|
| Pièces fixes J1, M1, M2, M3, M4, U2, U7 | Tout composant dont l'empreinte est **dans le contour** est « pré-placé » et n'est jamais déplacé (doc *Pre-placed components*). | Dans la carte d'entrée : exactement ces 7 empreintes sont dans le contour, les 100 autres sont hors carte. Rien à faire. |
| U2 à 0° | Orientation pré-placée conservée (même doc). | Acquis. |
| U2 au centre (3 mm près) | Découle de la position de U2, fixe. | Acquis, rien à saisir (non vérifiable par Quilter, vérifié par le juge). |
| Contour, un seul | Edge.Cuts unique fermé. | Présent. |
| Face unique (avant) | Voir § 3. | À régler. |

## 1. Découplage : tableau à recopier (distance max 5 mm)
Colonne « Broche » = broche proposée pour l'essai ; les lignes marquées (libre) ont une broche non imposée par le schéma
(`appariement_libre_dans_groupe`) : laisser d'abord la détection automatique de Quilter (« Bypass Capacitors ») faire son
appariement, puis corriger seulement si elle est incohérente. Pour les lignes marquées (indice), l'appariement vient de l'ordre
d'implantation du schéma, **sans source** : c'est un choix d'essai, pas une exigence.

| Condensateur | Valeur | Circuit intégré (parent) | Broche cible | Distance max |
|---|---|---|---|---|
| C27 | 100nF | U1 | 48 (VDD) (libre : 24, 36, 48, 20) | 5 mm |
| C32 | 100nF | U1 | 36 (VDD) (libre) | 5 mm |
| C33 | 100nF | U1 | 24 (VDD) (libre) | 5 mm |
| C34 | 100nF | U1 | 20 (VREF+) (libre) | 5 mm |
| C28 | 4.7uF | U1 | 24, 36 ou 48 (VDD commun, libre) | 5 mm |
| C29 | 10nF | U1 | 21 (VDDA) (sûr, fil direct) | 5 mm |
| C30 | 1uF | U1 | 21 (VDDA) (libre : 21 ou 20) | 5 mm |
| C35 | 1uF | U1 | 20 (VREF+) (libre : 21 ou 20) | 5 mm |
| C19 | 100nF | U2 | 8 (libre : 8 ou 5) | 5 mm |
| C20 | 100nF | U2 | 5 (libre : 8 ou 5) | 5 mm |
| C22 | 4.7uF | U3 | 1 (AVDDVCSEL) (sûr) | 5 mm |
| C23 | 100nF | U3 | 1 (libre : 1 ou 11) | 5 mm |
| C24 | 100nF | U3 | 11 (libre : 1 ou 11) | 5 mm |
| C11 | 4.7uF | U5 | 2 (VOUT) (sûr) | 5 mm |
| C10 | 1uF | U5 | 3 (VIN) (fil direct, réseau /VBATL) | 5 mm |
| C13 | 1uF | U6 | 3 (VIN) (sûr) | 5 mm |
| C14 | 2.2uF | U6 | 2 (VOUT) (douteux : U6 ou U4, voir DOU du banc, question Q4) | 5 mm |
| C15 | 1uF | U4 | 2 (VDD) | 5 mm |
| C16 | 100nF | U4 | 2 (VDD) | 5 mm |
| C17 | 100nF | U4 | 3 (VDDIO) (fil direct) | 5 mm |
| C18 | 2.2uF | U4 | 4 (VREG) (fil direct) | 5 mm |
| C36 | 10uF | U7 | 8 (VDD) (fil direct) | 5 mm |
| C37 | 100nF | U7 | 8 (VDD) (fil direct) | 5 mm |

Remarques :
- Quilter mesure la distance euclidienne entre les **bords les plus proches** des deux pastilles, en cm (doc *Pin Distance*) ;
  le juge du banc mesure pastille → broche. Pour garder de la marge, on peut saisir 4,5 mm au lieu de 5 mm (option, non retenue ici).
- Quilter dit placer les plus petits condensateurs au plus près de la broche et laisse un même condensateur servir plusieurs broches.
- 23 lignes de découplage (C14 comprise) ; les condensateurs « hors découplage » (C1 à C9, C12, C21, C31, etc.,
  voir `hors_decouplage_proximite`) n'ont pas de contrainte de distance.

## 2. Règles actives : exprimables ou non
| Règle | Exprimable dans Quilter ? |
|---|---|
| U2 au centre ± 3 mm | Oui, indirectement : U2 est pré-placé (fixe). |
| I-01 (8 mm), I-02 (6 mm), I-03 (8 mm) : éloignement entre groupes | **Non.** Seule la contrainte « maximum » (composant près d'une broche) existe ; pas de distance **minimale** entre groupes. Seul contournement partiel : *Rule Areas* (zones de placement), pas de distance garantie. Ces règles ne seront donc pas imposées ; le juge les mesurera. |
| Rotation imposée U2 | Acquise (pré-placé). |

## 3. Face unique
Quilter bascule les composants entre dessus et dessous **sauf** s'ils sont liés à une zone de placement (*placement region*) sur une couche donnée.
Deux options (doc *Single-sided placement*) :
1. Préférence : cocher « Show single-sided layouts only » (filtre à l'affichage des candidats ; Quilter essaie de produire des candidats mono-face à chaque job, sans garantie).
2. Exigence : une *Rule Area* KiCad sur F.Cu englobant les 100 composants à placer, associée un par un par référence dans l'interface.
Recommandation : option 1 pour le premier essai. Si les candidats sont double face, le juge les refusera (contrainte « tout sur la face avant ») : il faudra alors l'option 2 (variante à demander).

## 4. Réglages du job (hors contraintes)
- Pile : 2 couches (cuivre), choisir un empilement à 2 couches dans « Select your stackup ».
- Contraintes fabricant : valeurs du fichier `.kicad_pro` (vérifier à l'écran).
- Le job produit placement **et routage** ; le routage de Quilter ne sert pas à la comparaison de placement (le juge reroute avec Freerouting) mais le fichier retourné contient ses pistes : le juge doit recevoir la carte telle quelle, aucune retouche.
