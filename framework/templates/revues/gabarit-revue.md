# Gabarit de rapport de relecture

> **Aperçu** : format des rapports écrits par les relecteurs dans `projets/<nom>/revues/`, un fichier par relecteur, par porte et par version : `REV-<phase>-<agent>-v<n>.md`, où `<phase>` est l'un de `scenarios`, `besoins`, `exigences`, `architecture`, `conception`, `implementation`, `integration`, `systeme`, `recette` (sans accent, c'est ce que l'outil cherche) ; ex. `REV-architecture-critique-v1.md`. Le relecteur remplit tout sauf la colonne « Sort », que l'architecte remplit avec l'utilisateur. L'outil refuse la porte s'il manque un rapport obligatoire ou si une ligne n'a pas de vrai sort.

Copier le bloc ci-dessous dans un nouveau fichier (sans les balises de code) :

```
# Relecture <phase> — <agent> — v<n>

**Date :** AAAA-MM-JJ
**Porte :** <phase>
**Fichiers relus :** liste des chemins
**Listes de contrôle appliquées :** ex. framework/checklists/critique.md (section de la phase), framework/checklists/embarque.md

| N° | Élément | Constat | Conséquence | Gravité | Proposition | Sort |
|---|---|---|---|---|---|---|
| 1 | | | | bloquant / majeur / mineur | | |

**Doutes à ouvrir :** liste.
**Non vérifié :** ce que le relecteur n'a pas pu lire ou contrôler.
**Synthèse :** nombre de constats par gravité.
```

## Colonnes
| Colonne | Contenu |
|---|---|
| N° | Numéro du constat dans le rapport |
| Élément | ID « titre » ou chemin:ligne |
| Constat | Le problème, en une ou deux phrases |
| Conséquence | Scénario d'échec ou effet concret si rien n'est fait |
| Gravité | bloquant, majeur ou mineur (définitions : `framework/garde-fous-agents.md`) |
| Proposition | Ce qui le résoudrait, sans décider à la place de l'utilisateur |
| Sort | Rempli par l'architecte : « corrigé dans … », « DOU-nnn « titre » », « rejeté : raison », ou « risque accepté : DEC-nnn « titre » » |

Un relecteur peut ajouter des colonnes (ex. `verificateur-sources` : valeur écrite, valeur de la source) ; « Gravité » et « Sort » gardent leur nom exact et « Sort » reste la dernière.

## Règles
- Le relecteur ne reçoit que la liste des fichiers et la porte : il lit les documents lui-même.
- L'architecte ne modifie pas les colonnes du relecteur ; il ne remplit que « Sort ».
- Un constat bloquant ou majeur ne peut être « rejeté » que par l'utilisateur : le sort cite sa réponse entre guillemets.
