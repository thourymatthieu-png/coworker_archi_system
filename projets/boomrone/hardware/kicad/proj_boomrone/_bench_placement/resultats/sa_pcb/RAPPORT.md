# Piste `sa_pcb` (OpenROAD SA-PCB, recuit simule C++) : ECHEC DOCUMENTE (binaire bloque par Smart App Control)

Statut : **echec**. Le code a ete lu, adapte, converti et compile, mais l'executable produit est refuse par Windows
(Smart App Control). Aucune carte `placee.kicad_pcb` n'a ete produite, le juge commun n'a donc pas ete lance
(pas de `metrics.md`). Par regle, je n'ai pas contourne le blocage (voir plus bas).

## Ce qui a ete fait (et marche)
| Etape | Resultat | Temps |
|---|---|---|
| `git clone https://github.com/The-OpenROAD-Project-Attic/SA-PCB` dans `_outils/src` (commit `ca962f5`) | OK | secondes |
| MinGW-w64 winlibs GCC 16.2.0 UCRT x86_64 posix-seh (release GitHub `16.2.0posix-23.1.3-14.0.0-ucrt-r3`, zip sans LLVM, 276 Mo) ; sha256 verifie = celui publie (`3c693050...d4b6a1`) | OK | 55 s telechargement, 19 s extraction |
| Boost 1.87.0 (zip officiel `archives.boost.io`, 226 Mo, sha256 calcule `f367a218...0828`, non compare : pas de somme publiee consultee) ; seuls les en-tetes sont extraits | OK | 42 s + 19 s |
| Extraction KiCad 10 -> format texte (`tools/bench_sa_pcb/extract.py`, pcbnew) : 107 noeuds (courtyard F.Cu + rotation), 56 reseaux, pieces verrouillees marquees fixes, contour ; variante avec 23 liens de decouplage triples | OK | < 5 s |
| Adaptation Windows du code SA-PCB (`patch_src.py`) + pilote CLI (`sa_main.cpp`) + compilation (`build.ps1`) | **compile et lie** (`_outils/build/sa_main.exe`) | ~30 s par compilation |
| Execution de `sa_main.exe` | **BLOQUE** | - |

Commandes exactes : `powershell tools/bench_sa_pcb/build.ps1` (patch + g++ `-std=gnu++17 -O2 -w -fpermissive`) ;
extraction : `C:\Users\quent\.venvs\kicad-mcp\Scripts\python.exe tools/bench_sa_pcb/extract.py <entree.kicad_pcb> base.txt meta.json [--decoup decouplage.json --decoup-poids 3]`.
CMake/Ninja n'ont pas ete necessaires : je compile directement les 8 `.cpp` utiles (le `CMakeLists.txt` du depot depend de SWIG, de Python et d'un sous-module absent).

## Le blocage
Lancement de `sa_main.exe` : « Une strategie de controle d'application a bloque ce fichier ». Le registre indique
`VerifiedAndReputablePolicyState = 1` (Smart App Control en application) et le journal CodeIntegrity
(Microsoft-Windows-CodeIntegrity/Operational, ev. 3077/3033) montre le refus de charger l'exe depuis `_outils/build`.
Smart App Control bloque tout binaire non signe sans reputation : **tout** executable ou DLL compile localement sera
refuse (g++ passe car les binaires winlibs sont connus). Le contourner (desactiver SAC, signer avec un certificat
auto-signe, charger la DLL via un interpreteur autorise) releve de la modification de reglages de securite : interdit,
je m'arrete. Desactiver SAC est en outre irreversible sans reinstallation de Windows ; c'est a l'utilisateur d'en decider.

Consequence pour le banc : tout outil C/C++ compile sur ce poste sera dans le meme cas. Les outils Python/Java deja connus passent.

## Ce que l'analyse du code dit de l'outil pour notre cas (sans l'avoir execute)
- **Etat du depot** : archive 2020, depot incoherent. `main.cpp` est un stub, le `Makefile` de `src/` reference un `main.hpp` absent,
  le vrai point d'entree est un pilote Python SWIG (`PcbPlacer.py`) qui exige le sous-module `KicadParser` (vide ici, KiCad 5 seulement),
  SWIG, Python-dev, Boost, cpp-taskflow. J'ai extrait le noyau `GridBasedPlacer::annealer`. Le code est POSIX (`sys/resource.h`,
  `mkdir(path, mode)`) : adapte par des shims.
- **Modele** : composants = rectangles (courtyard), pastilles = decalages au centre, face F/B, rotations 0/90/180/270 (ou 45 degres).
  Pieces fixes supportees (non deplacees, peuvent deborder du contour).
- **Cout** : HPWL + recouvrement des polygones (terme quadratique **mou**, aucune garantie de zero recouvrement ; `project_soln()` n'est jamais appelee).
  Pas de decouplage, pas de regles d'isolement, pas de zone interdite, poids de reseau non fonctionnels (README : « Broken support for weighted modules/nets »).
  Contournement prevu : dupliquer des reseaux condensateur -> broche CI (`--decoup-poids`), simple approximation du critere 5 mm.
- **Defauts reperes** : `sigma` plancher a 2 mm en Lam modifie (pas fin impossible sur des 0402/0603), poids de longueur `l1` decroissant a chaque
  iteration externe, meilleur etat echantillonne toutes les 100 iterations (patche a 10), recouvrement en O(n^2) intersections Boost.Geometry,
  ecritures de debug dans `./cache`.
- **Pronostic** (hypothese, non mesuree) : sur une carte a 61 % de courtyards, un placement presque valide mais avec recouvrements residuels ;
  legalisation externe necessaire.

## Effort
- Installation et plomberie : ~1 h effectif. Piege : cc1plus echoue sur `bits/c++config.h` quand le chemin du toolchain depasse MAX_PATH ;
  toolchain et Boost deplaces dans `C:\Users\quent\satc` (1,07 Go, supprimable). `_outils/mingw` est donc vide.
- Qualite du placement : non evaluable.

## Avis franc
SA-PCB n'est pas une option pour ce projet : depot casse et non maintenu, ni decouplage ni regles, recouvrement non garanti ; et sur ce poste
le binaire doit en plus passer Smart App Control. Le recuit simule peut etre bon sur petite carte (article Cypress), mais ce serait plutot a
faire avec le moteur maison existant (qui a deja un recuit) qu'avec cet outil archive.

## Pour reprendre (blocage leve ou autre machine)
`_outils/build/sa_main.exe _travail/base.txt sortie.txt -i 100 -j 25` (ou `decoup.txt`). Sortie : `ref cx cy orient fixe`. Il reste a ecrire la reinjection
pcbnew (origine empreinte = centre - R(offset courtyard) ; `_travail/meta.json` contient les decalages) puis a lancer le juge. Metriques du juge : aucune.

## Fichiers
`tools/bench_sa_pcb/{extract.py,patch_src.py,sa_main.cpp,build.ps1}` (worktree, non commites) ; ici : `_outils/src`, `_outils/build`, `_travail/`.
