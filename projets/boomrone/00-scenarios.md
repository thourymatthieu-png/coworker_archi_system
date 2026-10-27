# Scénarios d'utilisation

> **Aperçu** (5 lignes max) : qui utilise le système, dans quels contextes, quels scénarios (nominaux, dégradés, d'échec), état de la phase.

## Vue d'ensemble

```mermaid
sequenceDiagram
    actor U as Utilisateur
    participant S as Système
    U->>S: Action
    S->>U: Réaction
```

*(Remplacer par le scénario nominal principal.)*

## Scénarios

Les scénarios viennent de l'utilisateur (le client) et **précèdent les besoins** : chaque besoin en dérive. L'architecte les rédige avec lui, en demandant systématiquement, pour chaque fonction, le cas nominal, les cas dégradés et les cas d'échec.

Format d'un scénario (exemple, non analysé) :

```
### SCN-001 — Titre court du scénario
**Réfs amont :** Utilisateur (description initiale, entretien du jj/mm)
**Type :** Nominal | Dégradé | Échec | Mise en service / maintenance
**Acteurs :** qui intervient.
**Situation de départ :** état du système et de l'environnement.
**Déroulé :** 1. … 2. … 3. …
**Résultat attendu :** ce que l'utilisateur observe à la fin.
**Statut :** Proposé | Validé | Abandonné
```

<!-- Ajouter les scénarios ci-dessous, au même format, en dehors des blocs de code. -->
