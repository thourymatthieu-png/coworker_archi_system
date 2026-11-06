# Piste `quilter` : préparation de la soumission (2026-11-06)

Essai non décisionnel. Rien n'a été envoyé à Quilter (pas de compte, pas de téléversement). Les pages publiques ont été lues le 2026-11-06 ;
le contenu web est traité comme donnée. Les libellés d'interface ne sont pas vérifiés (pas de compte).

## 1. Résumé de la documentation
| Sujet | Ce que dit la source | Source |
|---|---|---|
| Fichiers KiCad | Carte `.kicad_pcb` **et** schéma correspondant ; fichier projet facultatif mais utile ; fichiers envoyés **directement** (« does not currently support uploading .zip files or nested directories, except for Xpedition »). Contour unique fermé sur Edge.Cuts, empreintes chargées, netlist cohérente avec le schéma. | [KiCAD](https://docs.quilter.ai/cad-compatibility/kicad.md), [Prepare your input board file](https://docs.quilter.ai/using-quilter/prepare-your-input-board-file.md), [Upload](https://docs.quilter.ai/using-quilter/upload-your-design-files.md) |
| Version KiCad | **Non précisée** : la doc ne cite aucune version, KiCad 10 non confirmé. Le projet est au format 20260206 (KiCad 10.0). Risque d'échec à l'import. | idem |
| Pièces pré-placées | Tout composant dans le contour au téléversement est traité comme pré-placé ; position et orientation jamais modifiées, même si cela bloque le job. Ce qui est hors contour est placé et routé. | [Pre-placed components](https://docs.quilter.ai/design-parameters/pre-placed-components.md) |
| Zones de placement | KiCad : *Rule Area* en « Keepout », tous les éléments de keepout décochés ; extraite comme placement region ; composants à associer **à la main par référence**. | [Placement regions](https://docs.quilter.ai/design-parameters/placement-regions.md) |
| Keepouts | Respectés (composants, pistes, vias, zones). | [Keepouts](https://docs.quilter.ai/design-parameters/keepouts.md) |
| Condensateurs de découplage | Détection automatique des condensateurs entre un composant et la masse ; priorité : fil de schéma, puis noms de broches « tension », puis répartition égale. Plus petits condensateurs placés au plus près. | [Bypass Capacitors](https://docs.quilter.ai/physics-constraints/bypass-capacitors.md) |
| Distance composant vers broche | Contrainte *Custom Component Proximity* (1er mai 2026) : composant restreint, parent, broche cible, distance max ; appliquée au placement et vérifiée par le contrôle Pin Distance (écart entre bords, en cm). | [Changelog](https://www.quilter.ai/changelog), [Pin Distance](https://docs.quilter.ai/physics-rule-checks-prcs/pin-distance.md) |
| Simple face | Quilter bascule les composants entre faces sauf si liés à une zone ; filtre « Show single-sided layouts only » (préférence) ou zones englobant tout, liées à la couche dessus (exigence). | [Single-sided placement](https://docs.quilter.ai/design-parameters/single-sided-placement.md) |
| Limites | Pas de limite de composants ni de densité publiée (la FAQ renvoie vers support@quilter.ai). Nouvelle stratégie de routage (alpha) : cartes de moins de 400 broches. Seulement des vias traversants. | [FAQ](https://docs.quilter.ai/about-quilter/faq.md), [Changelog](https://www.quilter.ai/changelog) |
| Durée | « from 15 minutes to 24 hours », premiers résultats typiquement sous une heure ; courriels au premier placement réussi et à la fin. Témoignage tiers : 1 h 10 de calcul. | [Submit your layout job](https://docs.quilter.ai/using-quilter/submit-your-layout-job.md), [article tinycomputers](https://tinycomputers.io/posts/what-a-commercial-pcb-placer-does-that-my-open-source-one-cant.html) |
| Retour | Candidats renvoyés dans le format natif, bouton Download en bas à droite de l'aperçu. Quilter fait placement **et** routage. | [Downloading candidates](https://docs.quilter.ai/downloading-candidates.md) |

## 2. Gratuité, propriété, confidentialité
- **Le « gratuit en bêta » n'est pas confirmé.** Les pages lues décrivent un *Free Tier* : « Academic, personal, and eligible professional use » ; éligibilité : moins de 10 personnes et moins de 50 000 USD de revenu ; usage commercial/entreprise = Enterprise ([page gratuite](https://www.quilter.ai/free-ai-pcb-design)). La page tarifs n'en donne pas les conditions. Usage d'essai personnel : vraisemblablement éligible, **à confirmer à l'inscription**.
- **Entraînement (point sensible).** Offre gratuite : métadonnées (contour, empreintes, contraintes) et/ou fichiers d'entrée servent à générer des puzzles d'entraînement (même page). FAQ : les conditions du palier gratuit « permit training on both users' direct inputs and synthetic training data ». Conditions d'utilisation (§5.2) : licence « perpetual, worldwide, royalty-free and sublicensable » sur l'entrée, incluant le droit d'entraîner les modèles ; §4 : Quilter ne revendique pas la propriété de l'entrée ni de la sortie. Politique de confidentialité (datée du 14 août 2025) : pas d'entraînement direct sur l'entrée, seulement sur des « Synthetic Training Data ». Les textes sont partiellement en tension : prudence. ([Terms](https://www.quilter.ai/terms), [Privacy](https://www.quilter.ai/privacy), [FAQ](https://docs.quilter.ai/about-quilter/faq.md))
- **Conservation** : aucune durée pour les fichiers ; suppression de compte « up to 7 business days », irréversible (FAQ). Partage possible avec des prestataires (paiement, CRM) et des services d'IA tiers pour le support (Privacy).
- **Conséquence** : le projet complet (schéma, empreintes, noms de nets) sort de la machine, sans garantie de non-réutilisation sur l'offre gratuite. À valider par l'utilisateur avant envoi ; si Boomrone est sensible, ne pas soumettre.

## 3. Risques
1. **Densité** : environ 61 % de la surface par les courtyards, 2 couches. Les chiffres « ~10 % de densité et ~100 composants en 2024 » de l'article Cypress n'ont **pas pu être retrouvés** dans les pages lues (l'article tinycomputers du 2026-04-24 ne les mentionne pas) ; aucune limite officielle publiée. Probable : candidats incomplets ou aucun candidat. 107 empreintes, 100 à placer.
2. **KiCad 10 non confirmé** : l'import peut échouer. Si oui, noter le message et arrêter (pas de rétrogradation sans accord).
3. **Pièces pré-placées** : seules 7 sont dans le contour (bon) ; Quilter échouera plutôt que de les déplacer.
4. **Pas de distance minimale entre groupes** : I-01, I-02, I-03 non exprimables ; U2 « au centre » acquis par sa position fixe.
5. **Face unique non garantie** (préférence seulement, voir `contraintes_a_saisir.md` § 3).
6. **Routage par Quilter** : le fichier retourné contient ses pistes.
7. Confidentialité : voir § 2.

## 4. Dossier préparé
- `paquet/proj_boomrone/` : `.kicad_pro`, `.kicad_sch` racine, `synoptique.kicad_sch`, 10 sous-feuilles `des-0xx-*.kicad_sch`, `sym-lib-table`, `fp-lib-table` (chemins `${KIPRJMOD}/...`, aucun chemin absolu), `lib_boomrone.kicad_sym`, `lib_boomrone.pretty`, `lib_boomrone.3dshapes`, et `proj_boomrone.kicad_pcb` = copie identique de `entree/proj_boomrone.kicad_pcb`.
- `paquet/proj_boomrone_quilter.zip` (1,7 Mo) : transport seulement. **Quilter n'accepte pas le zip** pour KiCad : téléverser les fichiers un par un.
- Vérification : `kicad-cli pcb drc` sur la copie : 0 violation, 228 connexions non routées (normal) ; rapport `drc_copie.txt`. L'import dans Quilter n'a pas pu être testé.
- `contraintes_a_saisir.md` : 23 contraintes de découplage, pièces fixes, règles exprimables ou non, face unique.
- **Rule Areas : pas de variante créée.** Raisons : (a) les 7 pièces fixes sont déjà verrouillées par la règle « dans le contour » ; (b) Quilter regroupe déjà par schéma ; (c) l'association des composants aux zones se fait à la main dans l'interface (100 références) ; (d) dessiner des zones reviendrait à décider d'un plan de masse (choix de conception) ; (e) elles n'apportent pas les isolements. À reconsidérer seulement pour imposer la face unique (une zone F.Cu englobante). Composants par bloc, si besoin : DES-002 (U1, C27 à C35, R31, J2), DES-003 (U2, C19 à C21, R24), DES-004 (U3, C22 à C24, R25 à R28), DES-005 (U4, U6, C13 à C18, R22, R23, TP1 à TP6), DES-007 (Q1 à Q4, D1 à D4, C2 à C7, C9, R3 à R8, R29, R30, TP11, M1 à M4), DES-008 (J1, FB1, C8), DES-009 (U5, C10 à C12, R20, R21), DES-010 (SW1, C1, R1, R2), DES-011 (BZ1, LED1, D5, Q5 à Q8, R9 à R19), DES-012 (U7, C36, C37, TP7 à TP10).

## 5. Guide pas à pas pour l'utilisateur
1. Lire les § 2 et 3 ; décider d'envoyer ou non (confidentialité).
2. Créer un compte sur [app.quilter.ai](https://app.quilter.ai) (offre gratuite ; confirmer l'éligibilité).
3. Créer un projet puis un job ; téléverser les fichiers de `paquet/proj_boomrone/`, à plat : `proj_boomrone.kicad_pcb`, `proj_boomrone.kicad_sch`, toutes les `des-0*.kicad_sch` et `synoptique.kicad_sch`, `proj_boomrone.kicad_pro` (pas le zip, pas de sous-dossier).
4. Pile : 2 couches. Fabricant : valeurs par défaut ou celles du `.kicad_pro`.
5. Circuit Comprehension : vérifier les condensateurs détectés (*Bypass Capacitors*) ; recopier le tableau de `contraintes_a_saisir.md` (5 mm). Cocher « Show single-sided layouts only ».
6. Soumettre ; attendre de 15 min à 24 h. Si l'import échoue ou si aucun candidat n'aboutit, copier le message (console) et arrêter.
7. Télécharger un candidat (le mieux classé, mono-face) ; l'enregistrer en `resultats/quilter/placee.kicad_pcb` (sans l'ouvrir ni le modifier). Noter la durée, le nombre de candidats, les avertissements du contrôle physique.
8. Lancer l'évaluation (§ 6).

## 6. Commandes d'évaluation (depuis le dossier du banc)
```bash
python eval/bench_eval.py statique resultats/quilter/placee.kicad_pcb --piste quilter
python eval/bench_eval.py routage  resultats/quilter/placee.kicad_pcb --piste quilter
```
Attention : le fichier de Quilter contiendra ses pistes ; vérifier si le juge `routage` les retire avant de comparer (sinon la mesure est celle du routage de Quilter, à signaler).

## 7. DeepPCB (InstaDeep), pages publiques seulement
- Essai gratuit : 30 minutes, une carte, 4 couches, 150 airwires, 100 composants, 2 200 broches ; au-delà, prépayé (1 h 30 USD, 10 h 280 USD, 30 h 800 USD) ([pricing](https://deeppcb.ai/pricing), [aide](https://deeppcb.ai/help/)).
- Placement : des articles décrivent un placement par apprentissage par renforcement, mais ni la page tarifs ni l'aide ne disent s'il est inclus dans l'essai ; le plugin KiCad documenté fait du **routage**. Une source tierce évoque 2 h de placement jusqu'à 100 composants (non officiel, peut-être périmé).
- Conclusion : gratuit seulement en essai limité ; la carte Boomrone (107 empreintes) dépasse la limite de 100 composants de l'essai ; **placement non confirmé comme utilisable gratuitement** aujourd'hui. Non testé (aucun compte).
