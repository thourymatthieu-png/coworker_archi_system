# Registre de doutes — Boomrone

> **Aperçu** : tout doute, ambiguïté ou hypothèse est inscrit ici. Un doute **bloquant ouvert** empêche de franchir la porte de validation.
> **État** : 9 doutes levés, 8 ouverts (dont 1 bloquant : DOU-007 « Que fait le drone si ça se passe mal ? »).

### DOU-001 — Que veut dire se rétablir en vol stationnaire ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** BES-002 « Se rétablir rapidement en vol stationnaire »
**Question :** À partir de quand considère-t-on le drone « en stationnaire » ?
**Réponse :** Vitesse et inclinaison sous des seuils, tenus brièvement (seuils provisoires, voir DOU-016 « Quels seuils chiffrés retenir pour le rétablissement, le stationnaire et l'atterrissage ? »).
**Décision liée :** DEC-001 « Critère de rétablissement : vitesse et inclinaison »

### DOU-002 — Que veut dire au plus vite ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** BES-002 « Se rétablir rapidement en vol stationnaire »
**Question :** Y a-t-il un temps maximal visé, ou un simple score ?
**Réponse :** Le temps de rétablissement est un score de jeu, sans seuil de réussite.
**Décision liée :** DEC-002 « La rapidité de rétablissement sert de score de jeu »

### DOU-003 — À quelle altitude et sur quoi se stabilise-t-on ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** BES-003 « Tenir le vol stationnaire 10 secondes »
**Question :** Le stationnaire se fait-il à l'altitude atteinte ou à une altitude cible ?
**Réponse :** À l'altitude atteinte au rétablissement. Tolérance à chiffrer (voir DOU-016 « Quels seuils chiffrés retenir pour le rétablissement, le stationnaire et l'atterrissage ? »).
**Décision liée :** DEC-003 « Stationnaire à l'altitude atteinte »

### DOU-004 — Qu'est-ce qu'un atterrissage doux ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** BES-004 « Se poser doucement »
**Question :** Quel critère pour un atterrissage doux ?
**Réponse :** Vitesse verticale au contact sous un seuil, moteurs coupés après le contact, sol plat, n'importe où (seuil provisoire, voir DOU-016 « Quels seuils chiffrés retenir pour le rétablissement, le stationnaire et l'atterrissage ? »).
**Décision liée :** DEC-004 « Atterrissage doux : vitesse maximale au contact »

### DOU-005 — Comment le drone sait-il qu'il est lancé, et quand les moteurs démarrent-ils ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** BES-001 « Lancer à la main »
**Question :** Comment détecte-t-on le lancer ?
**Réponse :** Bouton-poussoir maintenu pour armer ; son relâchement signale le lancer ; les moteurs démarrent 200 ms après.
**Décision liée :** DEC-005 « Armement par bouton-poussoir maintenu, lancer détecté au relâchement »

### DOU-006 — Quelle exigence de sécurité pour les personnes ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** BES-001 « Lancer à la main »
**Question :** Qui joue, et quelles protections ?
**Réponse :** Adultes seulement, coupure des moteurs obligatoire en cas d'anomalie, protections d'hélices optionnelles, pas de norme jouet.
**Décision liée :** DEC-006 « Public : adultes seulement »

### DOU-007 — Que fait le drone si ça se passe mal ?
**Statut :** Ouvert
**Bloquant :** Oui
**Concerne :** BES-011 « Couper les moteurs en cas d'échec »
**Question :** Principe retenu : couper les moteurs. Cas retenus : absence de rétablissement dans un délai, batterie faible (DEC-013 « Cas de coupure des moteurs »). Reste à préciser : (a) le délai maximal de rétablissement ; (b) le seuil de batterie faible ; (c) retournement et choc : l'utilisateur ne les a pas retenus alors que DEC-006 « Public : adultes seulement » impose la coupure en cas d'anomalie — faut-il les ajouter ? (d) perte du lien radio : le drone continue-t-il normalement, puisque le réglage est possible en vol ? (e) le bouton rappuyé en vol doit-il couper les moteurs ?
**Réponse :** Partielle : voir DEC-013 « Cas de coupure des moteurs ».
**Décision liée :** DEC-007 « En cas d'échec, couper les moteurs »

### DOU-008 — Que doit-on régler et lire sans fil, et avec quoi ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-005 « Régler le drone sans fil »
**Question :** Quels outils et à quel moment ?
**Réponse :** Réglage des paramètres (par exemple PID) et visualisation des variables depuis un ordinateur et/ou un téléphone, en temps réel, y compris en vol.
**Décision liée :** DEC-008 « Réglage et visualisation sans fil, y compris en vol, temps réel »

### DOU-009 — Quelle taille, masse et forme de drone ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-012 « Rester sous 100 g »
**Question :** Quelle classe de drone ?
**Réponse :** Quadricoptère de moins de 100 g.
**Décision liée :** DEC-009 « Quadricoptère de moins de 100 g »

### DOU-010 — Quelle famille de STM32, et quels outils de programmation exactement ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-007 « Programmer le drone par câble avec l'outillage STMicroelectronics »
**Question :** Quel outillage, quel microcontrôleur ?
**Réponse :** ST-LINK disponible ; choix du STM32 laissé à l'architecture selon le besoin et le stock JLCPCB.
**Décision liée :** DEC-010 « ST-LINK disponible, microcontrôleur libre »

### DOU-011 — Quel budget, quelle quantité, quel délai ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-010 « Fabriquer avec JLCPCB en composants en stock »
**Question :** Quelle ambition de production ?
**Réponse :** Prototypes, quelques exemplaires. Budget et délai : voir DOU-015 « Quel budget et quelle échéance ? ».
**Décision liée :** DEC-011 « Prototypes, quelques exemplaires »

### DOU-012 — Que se passe-t-il si le bouton est relâché sans vrai lancer ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** BES-001 « Lancer à la main »
**Question :** Si l'utilisateur lâche le bouton alors que le drone est posé ou tenu en main, les moteurs démarrent 200 ms après. Comment éviter un démarrage dangereux ?
**Réponse :** Le relâchement seul suffit, mais le drone n'est armé qu'après 2 s de maintien du bouton, et se désarme si le bouton reste appuyé plus de 10 s. Risque résiduel accepté par l'utilisateur : un relâchement volontaire après 2 s démarre les moteurs, même si le drone n'est pas lancé. Retour visuel/sonore de l'armement : voir DOU-017 « Comment l'utilisateur sait-il que le drone est armé ? »
**Décision liée :** DEC-012 « Armement par maintien du bouton de 2 à 10 secondes »

### DOU-013 — Le délai de 200 ms est-il compatible avec le rétablissement ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** BES-002 « Se rétablir rapidement en vol stationnaire »
**Question :** Pendant 200 ms, le drone est en vol libre sans moteurs (environ 0,2 m de chute et 2 m/s de vitesse verticale supplémentaire). Ce délai est-il imposé (sécurité, dégagement de la main) ou ajustable après essais ? Comptabilise-t-on ces 200 ms dans le score ?
**Réponse :**
**Décision liée :**

### DOU-014 — Quels paramètres, quelle portée et quelle cadence de visualisation ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** BES-005 « Régler le drone sans fil »
**Question :** Quels paramètres modifiables (PID, durée du stationnaire, seuils…) ? Portée utile (ordre de grandeur de la pièce) ? Quelles variables visualiser et à quelle cadence ? Un paramètre modifié en vol peut faire chuter le drone : faut-il des bornes de sécurité ?
**Réponse :**
**Décision liée :**

### DOU-015 — Quel budget et quelle échéance ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** BES-010 « Fabriquer avec JLCPCB en composants en stock »
**Question :** Budget cible pour les prototypes et date visée pour les premiers essais ?
**Réponse :**
**Décision liée :**

### DOU-016 — Quels seuils chiffrés retenir pour le rétablissement, le stationnaire et l'atterrissage ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** BES-003 « Tenir le vol stationnaire 10 secondes »
**Question :** Les seuils proposés (vitesse < 0,3 m/s, inclinaison < 10°, tenue 0,5 s, vitesse au contact < 0,5 m/s) sont provisoires. Quelle tolérance d'altitude pendant les 10 s ? À lever avant la porte « exigences », car les exigences doivent être chiffrées.
**Réponse :**
**Décision liée :** DEC-001 « Critère de rétablissement : vitesse et inclinaison »

### DOU-017 — Comment l'utilisateur sait-il que le drone est armé ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** BES-001 « Lancer à la main »
**Question :** Après 2 s de maintien, l'utilisateur doit savoir que le drone est armé (LED, buzzer, vibration des moteurs ?). Même question pour le désarmement après 10 s. Le drone peut-il être réarmé sans relâcher puis rappuyer ?
**Réponse :**
**Décision liée :** DEC-012 « Armement par maintien du bouton de 2 à 10 secondes »

<!-- Ajouter les doutes ci-dessous, au même format, en dehors des blocs de code. -->
