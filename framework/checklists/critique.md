# Liste de contrôle du critique, par phase

> **Aperçu** : questions que l'agent `critique` pose systématiquement à chaque porte. Elles complètent la liste « embarqué » (`framework/checklists/embarque.md`) et les conditions de porte des modules actifs. Chaque question sans réponse satisfaisante devient un constat avec un scénario d'échec concret.

```mermaid
flowchart LR
    P["Pré-mortem"] --> S["Questions de la phase"]
    S --> E["Liste embarqué"]
    E --> M["Règles des modules actifs"]
    M --> R["Constats + doutes à ouvrir"]
```

## Toujours : le pré-mortem
« Le projet a échoué à la recette ou en usage : quelles sont les trois causes les plus probables ? » Chaque cause plausible sans parade écrite est un constat.

## Scénarios
- Chaque fonction a-t-elle un cas nominal, un cas dégradé et un cas d'échec ?
- Mise sous tension, mise hors tension, coupure brutale d'alimentation, batterie faible : décrits ?
- Mise en service, mise à jour du logiciel, maintenance, stockage, fin de vie : décrits ou exclus par décision ?
- Perte d'une liaison (radio, câble), capteur absent ou défaillant, commande reçue dans un mauvais état : décrits ?
- Mauvais usage prévisible par l'utilisateur (geste involontaire, mauvais branchement) ?
- La situation de départ et le résultat attendu sont-ils observables par l'utilisateur, sans connaître la technique ?

## Besoins
- Un besoin décrit-il une solution plutôt qu'un besoin ?
- Un scénario n'est-il couvert par aucun besoin, ou un besoin ne vient-il d'aucun scénario ?
- Les priorités sont-elles cohérentes avec les scénarios (un scénario de sûreté couvert par un besoin « Souhaitable » ?) ?
- Les exclusions de périmètre (sûreté des tiers, réglementation, durée de vie) sont-elles décidées par l'utilisateur, et leurs conséquences écrites ?

## Exigences
- Une exigence est-elle invérifiable, composée, ambiguë, ou sans tolérance (`framework/checklists/exigences.md`) ?
- Le test système prouve-t-il vraiment l'exigence, dans les conditions les plus défavorables, ou seulement le cas facile ?
- Deux exigences se contredisent-elles (délais, seuils, priorités entre coupures) ?
- Les valeurs provisoires ont-elles une échéance et un moyen d'être confirmées ?

## Architecture
- La faisabilité est-elle démontrée par les budgets avec marge, ou seulement affirmée ?
- Chaque composant principal a-t-il une fiche technique lue, une alternative et une disponibilité vérifiée ?
- Un point de défaillance unique peut-il rendre le système dangereux ? L'état de repli est-il sûr sans logiciel (reset, brown-out, alimentation absente) ?
- Les interfaces entre blocs (niveaux logiques, protocoles, temps) sont-elles complètes des deux côtés ?
- L'architecture contient-elle déjà du détail de conception qui y figera des choix trop tôt (règle 9) ?
- Une solution plus simple a-t-elle été écartée sans raison ?

## Conception détaillée
- Chaque valeur a-t-elle sa source, et le rapport de `verificateur-sources` est-il sans écart ouvert ?
- Les calculs de dimensionnement prennent-ils les valeurs maximales de la fiche, et pas seulement les typiques ?
- Les tests unitaires prouvent-ils quelque chose (un TU qui refait le calcul du DES ne prouve rien) ?
- Le comportement au démarrage, au reset, en cas d'erreur de bus, de débordement, de chien de garde est-il défini ?
- Le logiciel et le matériel sont-ils d'accord sur le brochage, les niveaux et les temps ?

## Format
Chaque constat : élément (ID « titre ») · objection · scénario d'échec concret · gravité (bloquant / majeur / mineur) · suggestion. Pas de remarque cosmétique (rôle de `coherence-clarte`).
