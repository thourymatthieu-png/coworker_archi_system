# Registre de doutes

> **Aperçu** : tout doute, ambiguïté ou hypothèse est inscrit ici. Un doute **bloquant ouvert** empêche de franchir la porte de validation.

Format (exemple, non analysé) :

```
### DOU-001 — Titre court du doute
**Statut :** Ouvert | Levé
**Bloquant :** Oui | Non
**Concerne :** REQ-001 « Titre de l'exigence »
**Question :** ce qu'on ne sait pas.
**Réponse :** (à remplir, avec la source)
**Décision liée :** DEC-001 « Titre de la décision »
```

### DOU-001 — Comment le drone informe-t-il l'utilisateur ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Le drone « informe » à 7 moments (initialisé, prêt, lancé, stabilisation, stationnaire, atterrissage, posé). Par LED, buzzer, vibration, ou sans fil (téléphone) ? Combien de signaux distincts, sachant que le drone vole (la LED est-elle visible, le buzzer audible) ?
**Réponse :** LED RGB, buzzer et communication sans fil, combinés. Motifs précis à définir en architecture ; contenu de la liaison sans fil : voir DOU-008 « Que transmet la liaison sans fil, et vers quoi ? ».
**Décision liée :** DEC-001 « Information de l'utilisateur par LED RGB, buzzer et liaison sans fil »

### DOU-002 — Que veut dire ne pas dériver horizontalement ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « Ne dérive pas horizontalement » exige de mesurer la position ou la vitesse horizontale (capteur de flux optique, par exemple). Veux-tu une dérive maximale chiffrée (en cm sur les 10 s), ou seulement une vitesse horizontale proche de zéro ? Le capteur de position est un surcoût en masse et en complexité pour un drone de poche.
**Réponse :** Centrale inertielle seule ; dérive maximale de 30 cm sur 10 s en objectif à valider par essais (non garanti).
**Décision liée :** DEC-011 « Centrale inertielle seule, dérive de 30 cm sur 10 s en objectif à valider par essais »

### DOU-003 — Quel délai pour atteindre le stationnaire ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « 2 secondes plus tard il doit être en vol stationnaire » : 2 s après le démarrage des moteurs ou après le lancer ? Est-ce un maximum (exigence) ou un objectif ? Quels seuils précis de vitesse et d'inclinaison pour dire « stationnaire » ?
**Réponse :** 2 s après le démarrage des moteurs, limite stricte ; stationnaire = vitesse < 0,3 m/s, inclinaison < 10°, tenues 0,5 s (provisoire, à confirmer par essais).
**Décision liée :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs »

### DOU-004 — Quelle plage de lancer et quelle orientation initiale ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « Dans n'importe quel sens » : le drone peut-il être lancé dans n'importe quelle orientation (à l'envers, de côté) ? Quelle plage de vitesse et d'angle de lancer le drone doit-il rattraper ? Quelle altitude minimale à la sortie de la main pour avoir le temps de se rétablir ?
**Réponse :** Toute orientation, y compris à l'envers ; vitesse de lancer 0,5 à 4 m/s vers le haut et l'avant ; hauteur d'au moins 1,5 m du sol (valeurs provisoires, à confirmer par essais).
**Décision liée :** DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol »

### DOU-005 — Que se passe-t-il si le drone n'y arrive pas ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Principe retenu : stationnaire non atteint dans le délai → moteurs coupés (DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai »). Retournement normal pendant la stabilisation (DEC-003 « Drone retourné ou très incliné : normal tant que la stabilisation n'est pas finie »). Batterie vérifiée à l'armement (DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible »). Reste à préciser : (a) une fois le stationnaire atteint, une inclinaison excessive ou un retournement doit-il couper les moteurs ? (b) la batterie peut-elle tomber en vol malgré la vérification à l'armement (seuil et marge) ? (c) un choc en vol (mur, plafond) coupe-t-il les moteurs ? (d) que fait le bouton appuyé en vol ?
**Réponse :** Stationnaire non atteint dans le délai : moteurs coupés (DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai »). Retournement normal pendant la stabilisation (DEC-003 « Drone retourné ou très incliné : normal tant que la stabilisation n'est pas finie »), mais moteurs coupés si le drone bascule après le stationnaire (DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »). Batterie vérifiée à l'armement seulement (DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » et DEC-013 « Pas de contrôle de la batterie en vol »). Pas de coupure sur choc (DEC-014 « Pas de coupure sur choc en vol »). Bouton appuyé en vol : moteurs coupés (DEC-015 « Bouton appuyé en vol : arrêt d'urgence »). Chaque cas a un signal distinct (DEC-005 « Un signal distinct pour chaque information »).
**Décision liée :** DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai », DEC-012 « Couper les moteurs si le drone bascule après le stationnaire », DEC-015 « Bouton appuyé en vol : arrêt d'urgence »

### DOU-006 — Comment éviter un départ des moteurs sans vrai lancer ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Les moteurs démarrent 200 ms après le relâchement du bouton. Si l'utilisateur relâche le bouton sans lancer (drone posé ou tenu en main), les hélices tournent. Que doit faire le drone (exigence de sécurité) ? Que se passe-t-il si le bouton est relâché avant 2 s ou maintenu très longtemps ?
**Réponse :** Le relâchement seul suffit (risque accepté : relâcher sans lancer démarre les moteurs). Relâché avant 2 s : retour en attente avec signal. Maintenu plus de 10 s : désarmement avec signal.
**Décision liée :** DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs », DEC-007 « Bouton relâché avant 2 secondes : retour en attente », DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes »

### DOU-007 — Quelles contraintes d'atterrissage ?
**Statut :** Ouvert
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Atterrissage « doux » : quelle vitesse maximale au contact ? Le drone se pose-t-il à l'endroit où il est (sol plat) ou revient-il vers le point de lancer ? Quelle durée de descente ?
**Réponse :**
**Décision liée :**

### DOU-008 — Que transmet la liaison sans fil, et vers quoi ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Vers quel appareil (téléphone, ordinateur, les deux) et par quelle technologie (Bluetooth, Wi-Fi) ? Le sans fil transmet-il seulement les 7 états du vol, ou aussi des mesures en temps réel et des réglages ? Faut-il un appairage avant le vol ? Le vol dépend-il de la liaison (non, par défaut) ?
**Réponse :**
**Décision liée :** DEC-001 « Information de l'utilisateur par LED RGB, buzzer et liaison sans fil »

### DOU-009 — Quelle tolérance d'altitude pendant les 10 secondes de stationnaire ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « Il maintient son altitude » pendant 10 s : quelle variation d'altitude est acceptable (par exemple ± 10 cm) ? À lever avant la porte « exigences », car l'exigence doit être chiffrée. Voir aussi DOU-002 « Que veut dire ne pas dériver horizontalement ? » pour la dérive horizontale.
**Réponse :**
**Décision liée :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs »

### DOU-010 — Quelle rotation du drone au lancer doit-il rattraper ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Un lancer à la main fait souvent tourner le drone sur lui-même. Quelle vitesse de rotation maximale doit-il rattraper (en degrés par seconde) ? Elle dimensionne le gyroscope. À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :** DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol »

### DOU-011 — Que fait-on si l'objectif de 30 cm de dérive n'est pas tenu aux essais ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-011 « Centrale inertielle seule, dérive de 30 cm sur 10 s en objectif à valider par essais » accepte le risque. Si les essais montrent une dérive plus grande : ajouter un capteur de flux optique, ou relâcher l'objectif ? Faut-il prévoir dès la carte JLCPCB un emplacement (connecteur ou empreinte) pour un capteur de flux optique, afin d'éviter une nouvelle carte ? À trancher en architecture.
**Réponse :**
**Décision liée :** DEC-011 « Centrale inertielle seule, dérive de 30 cm sur 10 s en objectif à valider par essais »

### DOU-012 — Quel angle limite et quelles autres valeurs de coupure retenir ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Question :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » retient 60° à titre provisoire. Quel angle, et quelle durée au-delà de laquelle on coupe (pour éviter une coupure sur une perturbation brève) ? À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »

### DOU-013 — Quel seuil de batterie à l'armement garantit un vol complet ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-003 « Échec : batterie faible à l'armement »
**Question :** Sans contrôle en vol (DEC-013 « Pas de contrôle de la batterie en vol »), le seuil d'armement doit garantir un vol complet (environ 15 s, moteurs sollicités). Quelle tension ou quel niveau de charge, avec quelle marge, et pour quelle batterie ? Dépend de la batterie choisie en architecture. À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :** DEC-013 « Pas de contrôle de la batterie en vol »

### DOU-014 — Quel scénario de mise en service faut-il écrire ?
**Statut :** Ouvert
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Premier montage : flash du micrologiciel avec le ST-LINK, première mise sous tension, calibrage de la centrale inertielle, test des moteurs hélices démontées, sens de rotation, réglage des seuils (batterie, angle). Que doit pouvoir faire l'utilisateur, dans quel ordre, et que se passe-t-il si le calibrage échoue ? Relevé par la relecture du critique à la porte « scénarios ».
**Réponse :**
**Décision liée :**

### DOU-015 — Que se passe-t-il si l'initialisation échoue ?
**Statut :** Ouvert
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Capteur absent, centrale inertielle muette, drone en mouvement pendant le calibrage des gyroscopes : le drone annonce-t-il « initialisé » à tort ? Faut-il exiger un drone immobile à l'initialisation, avec une durée définie, et un signal distinct d'échec d'initialisation ?
**Réponse :**
**Décision liée :**

### DOU-016 — Comment limiter le risque d'hélices en rotation sans lancer ?
**Statut :** Ouvert
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » accepte le risque sans le borner : relâchement en main, drone posé, doigt qui glisse. Faut-il, au minimum, une coupure rapide des moteurs si aucun lancer n'est détecté, ou reconsidérer la confirmation par la centrale inertielle (écartée par DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs ») ? À arbitrer par l'utilisateur.
**Réponse :**
**Décision liée :** DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs »

### DOU-017 — Que se passe-t-il si l'alimentation est coupée ou chute en vol ?
**Statut :** Ouvert
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Un lancer vigoureux peut débrancher la batterie ou faire chuter la tension, et le microcontrôleur peut redémarrer en vol. Le drone peut-il alors se réarmer seul, notamment si le bouton est appuyé ? Décision attendue : jamais de réarmement automatique. La batterie est-elle mesurée à vide ou sous charge à l'armement (voir DOU-013 « Quel seuil de batterie à l'armement garantit un vol complet ? ») ?
**Réponse :**
**Décision liée :** DEC-013 « Pas de contrôle de la batterie en vol »

### DOU-018 — Quel est le comportement à l'atterrissage et après le posé ?
**Statut :** Ouvert
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Quel critère détecte « posé » (arrêt de la descente, choc) avec une centrale inertielle seule ? Que se passe-t-il en cas de rebond, d'atterrissage de travers ou sur sol incliné ? La détection de basculement de DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » est-elle désactivée une fois posé ? Quel est l'état du drone après un posé ou une coupure (verrouillé, initialisé), et comment le réarme-t-on, jamais automatiquement ? À traiter avec DOU-007 « Quelles contraintes d'atterrissage ? ».
**Réponse :**
**Décision liée :**

### DOU-019 — Quel capteur donne l'altitude et la vitesse verticale ?
**Statut :** Ouvert
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » repose sur un capteur de hauteur, alors que DEC-011 « Centrale inertielle seule, dérive de 30 cm sur 10 s en objectif à valider par essais » retient une centrale inertielle seule. Sans capteur d'altitude, l'altitude se calcule par intégration et diverge. Faut-il un baromètre ou un capteur de distance ? À trancher avant les exigences, car cela change la carte.
**Réponse :**
**Décision liée :** DEC-011 « Centrale inertielle seule, dérive de 30 cm sur 10 s en objectif à valider par essais »

### DOU-020 — Quel est le public visé et quel risque pour les personnes est acceptable ?
**Statut :** Ouvert
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Adulte seulement, ou enfant aussi ? Sans cette réponse, les risques de DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » et de DEC-014 « Pas de coupure sur choc en vol » (hélices nues qui continuent après un choc) ne peuvent pas être jugés. Protège-hélices obligatoires ou optionnels ? Norme jouet visée ou non ?
**Réponse :**
**Décision liée :**

### DOU-021 — Que se passe-t-il pour un lancer hors plage ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-002 « Échec : stationnaire non atteint dans le délai »
**Question :** Lancer trop bas, trop faible, trop fort ou sous un plafond bas : le drone le distingue-t-il d'un défaut du drone, et quel signal l'utilisateur reçoit-il (le même que l'échec de stabilisation ?) ? Voir DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol ».
**Réponse :**
**Décision liée :**

### DOU-022 — À partir de quand compte le chrono des 10 secondes, et que fait un lancer avec le bouton encore appuyé ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Question :** Les 10 secondes de DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes » courent-elles depuis l'appui initial ou depuis l'armement (2 s plus tard) ? L'utilisateur qui lance à 9,9 s et relâche à 10,1 s désarme-t-il le drone ?
**Réponse :**
**Décision liée :** DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes »

### DOU-023 — Quel filtrage du bouton et quelle fenêtre de garde après le lancer ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Quel antirebond, et quelle fenêtre de garde juste après le lancer, évitent qu'un relâchement ou un appui parasite déclenche l'arrêt d'urgence de DEC-015 « Bouton appuyé en vol : arrêt d'urgence » avec un signal trompeur ?
**Réponse :**
**Décision liée :** DEC-015 « Bouton appuyé en vol : arrêt d'urgence »

### DOU-024 — Comment arrêter un drone en vol sans le saisir ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Atteindre le bouton d'un drone en vol revient à l'attraper, hélices tournantes. Faut-il un arrêt d'urgence par le sans fil (voir DOU-008 « Que transmet la liaison sans fil, et vers quoi ? »), des protège-hélices, ou accepte-t-on que seul le bouton existe ?
**Réponse :**
**Décision liée :** DEC-015 « Bouton appuyé en vol : arrêt d'urgence »

### DOU-025 — Que fait le vol si le lien sans fil est absent, jamais appairé ou perdu ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Le vol dépend-il du lien sans fil (par défaut non) ? Le drone arme-t-il et vole-t-il sans téléphone ? Un lien perdu en vol change-t-il quelque chose ? Lié à DOU-008 « Que transmet la liaison sans fil, et vers quoi ? ».
**Réponse :**
**Décision liée :** DEC-001 « Information de l'utilisateur par LED RGB, buzzer et liaison sans fil »

### DOU-026 — Les réglages par le sans fil sont-ils dans le périmètre, et dans quels états ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Le sans fil sert-il aussi à régler (seuils, gains) ou seulement à informer ? Si oui, dans quels états du drone est-ce autorisé (au sol, désarmé seulement) ? Les réglages sont-ils conservés après coupure ?
**Réponse :**
**Décision liée :**

### DOU-027 — Combien de signaux distincts la LED RGB et le buzzer peuvent-ils porter ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-005 « Un signal distinct pour chaque information » conduit à 13 signaux et plus, pour une LED et un buzzer dont le son est couvert par les moteurs en vol. Faut-il « un signal distinct par catégorie » (prêt, lancé, échec, posé), avec le détail réservé au sans fil ? À valider par l'utilisateur.
**Réponse :**
**Décision liée :** DEC-005 « Un signal distinct pour chaque information »

### DOU-028 — Faut-il une limite de dérive avant la coupure, entre 10° et 60° d'inclinaison ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Question :** Entre le stationnaire (< 10°) et la coupure à 60° (DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »), un drone à 45° peut dériver de plusieurs mètres vers un mur ou une personne sans coupure. Faut-il une distance ou une durée maximale ? Élargit DOU-012 « Quel angle limite et quelles autres valeurs de coupure retenir ? ».
**Réponse :**
**Décision liée :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »

### DOU-029 — Quelle altitude maximale et quel plafond le drone doit-il tolérer ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** À 4 m/s vers le haut, le drone peut atteindre un plafond en 0,5 s. Quelle altitude maximale vise-t-on, et que se passe-t-il en cas de contact avec le plafond (DEC-014 « Pas de coupure sur choc en vol ») ? Voir DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol ».
**Réponse :**
**Décision liée :** DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol »

### DOU-030 — Les valeurs provisoires sont-elles à confirmer avant les exigences ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs », DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » et DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » portent des valeurs provisoires, à confirmer par essais, alors que leurs doutes sont « Levé ». Les considère-t-on comme levées pour la porte « scénarios », avec confirmation par essais avant la porte « exigences » ?
**Réponse :**
**Décision liée :**

<!-- Ajouter les doutes ci-dessous, au même format, en dehors des blocs de code. -->
