# Historique du framework

> **Aperçu** : évolutions de la méthode, des agents et des outils du framework, avec leur raison et l'accord de l'utilisateur. Les décisions d'un projet restent dans son propre journal ; ici ne figurent que les changements qui s'appliquent à tous les projets.

```mermaid
flowchart LR
    R["Retour d'expérience d'un projet"] --> C["Changement du framework"]
    C --> A["Accord de l'utilisateur"]
    A --> H["Ligne dans cet historique"]
```

## 2026-11-07 — Framework générique et garde-fous renforcés

**Accord de l'utilisateur** : « Oui, restructure, puis vérifie pour te critiquer et corrige » ; « ce que je veux surtout c'est que tu corriges les framework, les agents et les scripts pour que les futurs projets embarqués se passent mieux ».

**Raison** : relecture du premier projet (Boomrone, scénarios à conception détaillée). Constats principaux : phases rédigées par délégation totale (132 décisions prises par l'agent) puis portes accordées en un mot ; porte franchie avec des objections du critique non traitées ; valeurs de conception écrites de mémoire et contredites par les fiches après la porte (16 écarts, dont 3 graves) ; documents amont laissés périmés après des changements en aval ; outil de traçabilité qui ne contrôlait que les liens et les titres ; règles propres à KiCad et à JLCPCB mêlées au noyau.

**Changements** :
- Trois couches : noyau générique, modules optionnels (`modules/kicad/`, `modules/fabrication-jlcpcb/`), profil de projet (`projet.md`) qui déclare les modules actifs.
- Portes : procédure et listes de contrôle (`framework/portes.md`), rapports de relecture écrits par les relecteurs dans `revues/`, un sort par constat, synthèse imposée.
- Doutes : critères de « bloquant », échéance obligatoire pour un doute non bloquant.
- Délégation encadrée en trois niveaux (D0, D1, D2) ; les choix structurants ne sont jamais délégués.
- Sources obligatoires des valeurs techniques, marque `(à vérifier)`, nouvel agent `verificateur-sources`.
- Procédure de modification d'un élément validé (`framework/procedure-modification.md`).
- Listes de contrôle : critique par phase (avec pré-mortem), exigences (9 critères, tournures EARS), embarqué (alimentation, sûreté et AMDEC, matériel, logiciel, réglementation, production).
- Gabarits : champs Échéance, Décidé par, Modifie, Remplace, Sources, Règles d'implantation ; statut « Modifié » ; définition d'un test unitaire matériel ; nouveaux gabarits revue, budgets, risques acceptés.
- Garde-fous communs à tous les agents (`framework/garde-fous-agents.md`) ; agents refondus.
- Outil de traçabilité : champs, statuts, doutes, cohérence exigence/test, priorités, valeurs « (à vérifier) » validées, relectures sans sort, taille et contenu périmé ; tests automatiques.

**Seconde relecture du même jour** (`critique` et `coherence-clarte` sur le framework refondu, avec essai d'un projet sans carte maison) : l'outil laissait passer une porte sans rapport de relecture et ne voyait les valeurs « (à vérifier) » qu'une fois les DES validés. Corrigé : rapports obligatoires par porte, texte du gabarit refusé comme sort, rejet d'un constat grave sans réponse citée refusé, valeurs non vérifiées contrôlées sur tous les DES à la porte, doutes bloquants à partir d'une porte nommée, échéances non reconnues signalées, lien scénario → recette contrôlé, phases d'exécution des tests (implementation, integration, systeme, recette), statut « Validé » pour les tests, recettes définies avec les besoins, sources « page web » et « mesure », budgets sans objet permis, gabarit `reprise.md`, démarrage d'un projet dans `README.md`.

**Règles nouvelles à valider à l'usage** : les règles du module `fabrication-jlcpcb` (relevé de stock avant la porte architecture, règles de fabrication sourcées) et les seuils de taille de l'outil (30 lignes ou 3 000 caractères par élément, 15 lignes ou 1 500 caractères par décision) sont des propositions issues de Boomrone ; à ajuster après le prochain projet.

**Reste ouvert** : l'agent `electronique-hardware` hérite de tous les outils de la session (liste `tools:` retirée pour ne plus nommer les outils KiCad dans le noyau) ; choix à confirmer par l'utilisateur.
