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

Les doutes levés sont déplacés dans l'archive en bas de ce fichier : on ne les supprime jamais, car les décisions les citent.

## Doutes ouverts

### DOU-009 — Quelle tolérance d'altitude pendant les 10 secondes de stationnaire ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « Il maintient son altitude » pendant 10 s : quelle variation d'altitude est acceptable (par exemple ± 10 cm) ? À lever avant la porte « exigences », car l'exigence doit être chiffrée. Voir aussi DOU-002 « Que veut dire ne pas dériver horizontalement ? » pour la dérive horizontale.
**Réponse :**
**Décision liée :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs »

### DOU-010 — Quelle rotation au lancer le drone doit-il rattraper ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Un lancer à la main fait souvent tourner le drone sur lui-même. Jusqu'à quelle rotation (en tours par seconde) l'utilisateur s'attend-il à ce que le vol réussisse ? À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :** DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol »

### DOU-011 — Quelle dérive horizontale reste acceptable si 30 cm n'est pas tenu ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** L'objectif de 30 cm sur 10 s n'est pas garanti. Si les essais montrent une dérive plus grande, jusqu'où l'utilisateur l'accepte-t-il dans une pièce d'appartement (par exemple 1 m, 2 m) ? Au-delà, revoit-on l'objectif ou le produit ?
**Réponse :**
**Décision liée :** DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais »

### DOU-012 — Quel angle limite et quelles autres valeurs de coupure retenir ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Question :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » retient 60° à titre provisoire. Quel angle, et quelle durée au-delà de laquelle on coupe (pour éviter une coupure sur une perturbation brève) ? À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »

### DOU-013 — Quelle durée de vol garantit-on après un armement accepté ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-003 « Échec : batterie faible à l'armement »
**Question :** Après un armement accepté, le vol (jusqu'à environ 27 s : 2 s de stabilisation, 10 s de stationnaire, 15 s de descente au plus) doit aller à son terme sans contrôle de la batterie en vol. Quelle marge de durée attend-on (par exemple deux fois la durée du vol) ? À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :** DEC-013 « Pas de contrôle de la batterie en vol »

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

### DOU-035 — Quelle hauteur de stationnaire vise-t-on ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Aucun scénario ne fixe la hauteur du stationnaire, en vol normal comme en vol de réglage. Elle dépend de la hauteur de lancer, et elle fixe la durée de la descente à 0,5 m/s (DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »). Quelle hauteur vise-t-on, ou quelle plage ? À lever avant la porte « exigences ».
**Réponse :**
**Décision liée :**

### DOU-050 — Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Le critère de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » est-il mesurable et réaliste ? Lancé à l'envers depuis 1,5 m, une chute libre dure 0,55 s ; le drone peut toucher le sol avant la fin de la stabilisation, hélices tournantes. À lever avant la porte « exigences », avec DOU-030 « Les valeurs provisoires sont-elles à confirmer avant les exigences ? ». Relevé par la relecture critique. Complément de la relecture de porte (critique) : calcul pour un lancer à l'envers depuis 1,5 m à 0,5 m/s vers le haut : le drone touche le sol en 0,61 s environ ; les moteurs ne démarrent qu'à 0,2 s (DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs ») ; il reste donc environ 0,4 s pour se retourner de 180° et freiner une chute de 1,5 à 5 m/s, avec un capteur de hauteur ToF aveugle tant que le drone est retourné. Le bas de la plage de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » est très probablement infaisable. Proposition à soumettre à l'utilisateur : écrire dans SCN-001 « Vol nominal : de la batterie au posé » que les limites de la plage sont à confirmer par essais. Depuis : DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences » — la phrase est écrite dans SCN-001 « Vol nominal : de la batterie au posé » : les valeurs, y compris les limites de la plage, sont à confirmer avant la porte « exigences » ; le présent doute reste ouvert pour l'analyse. Le capteur ToF n'est plus qu'une proposition d'architecture (DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée ») : le risque d'une mesure de hauteur aveugle drone retourné vaut pour tout capteur orienté vers le bas. Complément du 2026-10-28 : échéance « avant les besoins » (et non seulement avant les exigences) : on revoit la plage de lancer (hauteur minimale, vitesse) avec une analyse de faisabilité avant de rédiger les besoins ; SCN-001 « Vol nominal : de la batterie au posé » et SCN-002 « Échec : stationnaire non atteint dans le délai » gardent les valeurs de la plage de lancer comme provisoires (DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » ; DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences »). Non bloquant pour la porte « scénarios », mais la phase « besoins » ne s'ouvre pas tant que ce doute est ouvert.
**Réponse :**
**Décision liée :** DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » (jalon, doute non levé)

### DOU-058 — Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Les valeurs d'origine du drone neuf (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ») et d'éventuelles bornes numériques sont renvoyées à l'architecture par DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ». Les fixer en phase architecture, avec les essais. Complément de la relecture de porte (critique) : « bornes numériques » contredit en apparence DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » (« aucune borne ») et DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » (bornes écartées). Lecture proposée, à faire confirmer par l'utilisateur : il s'agit seulement des limites de représentation (type de donnée, par exemple un entier sur 16 bits), et non de bornes de sécurité. Complément du 2026-10-28 (fusion) : la tolérance de mouvement (vitesse, rotation) de « immobile » pour l'armement, le mode réglage et le redémarrage (reste de DOU-073 « Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ? », DEC-110 « Armement refusé à 2 secondes d'appui : tous les tests faits, un seul signal Refus, sans attente de l'immobilité ») ; la durée de conservation du statut de refus sur le sans fil, et son extension éventuelle aux refus d'armement et de mode réglage (DEC-102 « Décollage de réglage refusé : signal Refus, statut de refus lisible jusqu'à la commande suivante ») ; la durée perceptible de l'effet local de la cause d'une coupure avant le relais de « Allumé » (DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil ») ; le seuil de batterie du décollage de réglage (DEC-108 « Vols de réglage répétés : aucune limite de nombre ni contrôle de chauffe, risque accepté ») ; la durée de la garde du bouton et la durée maximale de la phase « Lancé » (notes d'architecture) ; dire si le délai de 15 secondes après le décollage de réglage est le délai de descente réglable (DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement »). Complément du 2026-10-28 (extraction) : la tolérance de « immobile » pour l'armement sur un drone tenu en main (faisabilité du cas nominal) est extraite dans DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal », avec une échéance avant la phase « besoins » ; la tolérance pour le mode réglage et le redémarrage reste ici. Complément du 2026-10-28 (réponses de l'utilisateur) : (1) échéance « avant les besoins » pour la part qui conditionne la faisabilité des scénarios, c'est-à-dire la tolérance de « immobile » et la plage de lancer ; le reste (valeurs d'origine, bornes numériques, durées de garde, de refus, seuils) reste à fixer en architecture ; portée exacte de l'échéance à confirmer (DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir ») ; (2) la durée perceptible de l'effet local de la cause d'une coupure avant le relais d'« Allumé » est supprimée de ce doute : aucune durée minimale (DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté »).
**Réponse :** Partielle, le doute reste ouvert. 2026-10-27 : DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » rend les bornes des seuils de sécurité obligatoires (délai de 2 s, angle limite, délai de descente de 15 s, seuil de batterie, hauteur minimale dont la borne est strictement supérieure à 0) ; leurs valeurs sont à fixer ici, en architecture. La contradiction relevée par la critique est résolue pour les seuils de sécurité : ils sont bornés. Pour les autres réglages, qui restent sans borne (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal »), il ne s'agit que de limites de représentation. Restent à fixer : les valeurs d'origine et les valeurs numériques des bornes.
**Décision liée :**

### DOU-059 — Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Sauvegarde des réglages (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage ») : la commande de sauvegarde est-elle acceptée en vol ? Que se passe-t-il si la batterie est coupée pendant l'écriture ? Comment détecter une mémoire « jamais écrite » (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ») sans contrôle d'intégrité, alors que DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » écarte la détection de corruption ? Complément de la relecture de porte (critique) : « Sauvegarder » est acceptée à l'état « Armé, avant le lancer » (DEC-043 « Commandes sans fil acceptées selon l'état du drone ») ; une écriture en mémoire non volatile en cours peut-elle retarder le démarrage des moteurs au lancer, prévu 200 ms après le relâchement (DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs ») ? Complément du 2026-10-28 : « Sauvegarder » est désormais ignorée à l'état « Armé, avant le lancer » (DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer », qui modifie DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque » et DEC-043 « Commandes sans fil acceptées selon l'état du drone ») ; reste à traiter en architecture une écriture commencée avant l'armement (état « Allumé ») et encore en cours au relâchement du bouton, qui pourrait dépasser la durée maximale de la phase « Lancé ». Précision du 2026-10-28 (3e relecture de porte) : la fenêtre d'écriture dangereuse inclut l'état « Premier appui validé », seul état d'où l'armement est possible (DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série ») : « Sauvegarder » y est acceptée (état inclus dans « Allumé, en attente d'un appui », tableau de DEC-043 « Commandes sans fil acceptées selon l'état du drone »). Question complémentaire : « Sauvegarder » doit-elle aussi être ignorée dans l'état « Premier appui validé », comme à l'état armé (DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer »), ou l'écriture en cours à l'armement est-elle traitée autrement en architecture ?
**Réponse :**
**Décision liée :**

### DOU-060 — Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol »
**Question :** Reste après DEC-097 « Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé » : que se passe-t-il si la batterie est coupée dans chacun des états du drone (allumé, série d'appuis, armé, lancé, en vol, mode réglage, vol de réglage, échec d'initialisation) ? Lecture implicite des réponses du 2026-10-28, à confirmer : toute coupure mène à « Éteint, moteurs arrêtés », puis au redémarrage selon DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation » (le mode réglage est perdu : sortie uniquement en enlevant la batterie, DEC-079 « Sortie du mode réglage : uniquement en enlevant la batterie »). Hypothèse à valider par l'architecture matérielle : l'alimentation des moteurs garantit leur arrêt lors d'un redémarrage ou d'une chute de tension. Précise SCN-011 « Dégradé : coupure d'alimentation en vol ».
Complément du 2026-10-28 (fusion du point « coupure d'alimentation en phase Lancé », qui complète aussi DOU-075 « Le chien de garde couvre-t-il la phase Lancé, et cette phase a-t-elle une durée maximale ? ») : que fait le drone si l'alimentation est coupée en phase « Lancé », entre le relâchement du bouton et le démarrage des moteurs, 200 ms plus tard (DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard ») ? Hypothèse à confirmer : comme en vol (DEC-061 « Redémarrage immobile au sol : allumé mais jamais armé » ; DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie »), le drone redémarre, n'est jamais armé, donne « Échec d'initialisation » s'il est en mouvement et « Allumé » s'il est immobile, et ne démarre pas les moteurs seul. Une fois la réponse écrite, supprimer l'état « À définir : coupure en phase Lancé » du diagramme b et le renvoi « Coupure en phase Lancé » du diagramme a dans « Scénarios d'utilisation » — `projets/boomrone/00-scenarios.md`.
Échéance : porte « architecture » (pas d'échéance « avant les besoins »).
**Réponse :** Partielle, le doute reste ouvert. 2026-10-28 : pendant un redémarrage ou une chute de tension, y compris en phase « Lancé », les moteurs s'arrêtent et le drone est verrouillé (même état que « Allumé, en attente d'un appui »), puis redémarre selon la règle immobile et à plat ; hypothèse à valider par l'architecture matérielle (alimentation des moteurs). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-097 « Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé »

### DOU-062 — Où l'utilisateur est-il informé des limites d'emploi ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Où l'utilisateur est-il informé des limites d'emploi : plage de lancer (DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol »), lieu (DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires », DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur », DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu ») ? Notice, étiquette, ou rien ? Complément du 2026-10-28 (réponses de la dernière série de décisions) : cinq risques acceptés s'ajoutent à la liste de `reprise.md` : écriture de réglages sur un drone non initialisé (DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées ») ; pas de limite du nombre de vols de réglage ni de contrôle de chauffe (DEC-108 « Vols de réglage répétés : aucune limite de nombre ni contrôle de chauffe, risque accepté ») ; lancer hors plage ou hauteur impossible à mesurer = échec de stabilisation (DEC-109 « Lancer hors plage ou hauteur non mesurable : échec de stabilisation, limite d'emploi ») ; pas d'action particulière si le lien sans fil est perdu en vol de réglage, l'arrêt sans fil n'atteignant plus le drone (DEC-106 « Lien sans fil perdu en vol de réglage : aucune action particulière ») ; cause d'une chute non conservée en local, lisible seulement sur le statut sans fil (DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil »). Complément du 2026-10-28 (réponses de l'utilisateur) : s'ajoutent à la liste de `reprise.md` : (a) batterie lithium : charge et stockage hors périmètre, à la charge de l'utilisateur ; (b) drone laissé allumé : décharge de la batterie, risque de décharge profonde ; (c) programmation : hélices à démonter, programmation interrompue et essai des moteurs avant le premier vol non couverts (DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter ») ; (d) la commande « Sauvegarder » ignorée à l'état armé ne donne aucun signal local, l'acquittement se lit sur le statut sans fil (DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer ») ; (e) cause d'une coupure : l'utilisateur sans appareil de suivi n'est pas informé de la cause, risque confirmé (DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté »). La reprogrammation et le contrôle de version sont à confirmer comme hors périmètre.
**Réponse :**
**Décision liée :**


### DOU-080 — Seuils de temps du bouton : 1 s, 2 s, 10 s et délai entre appuis
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Valeurs provisoires à fixer en architecture et à confirmer avant la porte « exigences » (DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences ») : 1 s pour l'appui validé (DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court »), 2 s pour l'armement (DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone »), 10 s pour le désarmement (DEC-054 « Chrono de 10 secondes compté depuis l'appui initial »), et le délai d'environ 2 s entre appuis d'affilée (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »), avec sa tolérance et son origine (fin du relâchement ou début du nouvel appui). Depuis DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série », le délai d'environ 2 s fixe aussi la durée pendant laquelle l'armement est impossible après un appui validé relâché.
**Réponse :**
**Décision liée :** DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences »

<!-- Ajouter les nouveaux doutes ci-dessus, avant ce marqueur, au même format, en dehors des blocs de code. -->

### DOU-097 — Bouton encore maintenu à l'entrée en mode réglage (3e appui)
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Le 3e appui est validé après 1 s d'appui : le bouton peut encore être enfoncé à l'entrée en mode réglage (DEC-085 « Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé »). Est-il ignoré jusqu'au relâchement, ou pris en compte tout de suite (en mode réglage, le bouton n'arme jamais : DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage » ; aucun appui de la série ne peut armer : DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série ») ? Cas à relier à DEC-094 « Bouton appuyé après un décollage de réglage : pris en compte tout de suite, sans garde » (bouton pris en compte tout de suite après un décollage de réglage, sans garde) : une commande Décoller reçue pendant que le bouton est encore maintenu coupe-t-elle les moteurs aussitôt ? Cas voisin traité pour un refus : DEC-093 « Mode réglage refusé : retour à l'attente, compteur à zéro, bouton encore enfoncé ignoré ».
**Réponse :**
**Décision liée :**

### DOU-098 — Commande Sauvegarder pendant l'initialisation ou après un échec d'initialisation : réglages enregistrés écrasés
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage »
**Question :** DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » accepte Modifier et Sauvegarder pendant l'initialisation en cours et après un échec d'initialisation. Si les réglages enregistrés ne sont pas encore chargés, Sauvegarder écrase-t-elle les réglages enregistrés par des valeurs d'origine ou incomplètes (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée ») ? Un tiers à portée peut envoyer cette commande (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »). Le risque est une perte persistante des réglages, et non seulement une incomplétude. Accepté tel quel ?
**Réponse :**
**Décision liée :**

### DOU-099 — Paramètres de vol sans borne : modification en vol et sauvegarde par un tiers
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Les paramètres de vol n'ont aucune borne et sont modifiables aussi en vol normal (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ») ; sans appairage, un tiers à portée peut les modifier (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »), sans contrôle d'intégrité des commandes (DEC-066 « Commande sans fil corrompue : aucun contrôle d'intégrité »), puis les sauvegarder (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » : pas de retour aux valeurs d'origine). Précision à confirmer : d'après le tableau des commandes (DEC-043 « Commandes sans fil acceptées selon l'état du drone »), Modifier est acceptée en vol, Sauvegarder est ignorée en vol et acceptée au sol. Faut-il lister ce risque dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »), le limiter, ou les deux ?
Complément du 2026-10-28 (3e relecture de porte) : des paramètres de vol aberrants, sauvegardés par un tiers, sont rechargés à chaque démarrage (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage ») sans retour aux valeurs d'origine (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »), sans borne (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal »), sans contrôle d'intégrité (DEC-066 « Commande sans fil corrompue : aucun contrôle d'intégrité ») et sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »). Comment le propriétaire récupère-t-il un drone dont les réglages sauvegardés l'empêchent de voler normalement : par la reprogrammation seule (SCN-008 « Mise en service : programmation du drone »), ou autrement ? Ce risque est-il à inscrire dans la liste des risques acceptés de `reprise.md` (voir DOU-102 « Registre consolidé des risques acceptés ») ?
**Réponse :**
**Décision liée :**

### DOU-100 — Appui bref pendant la garde du bouton, relâché avant la fin, hélices tournantes en main
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-002 « Échec : stationnaire non atteint dans le délai »
**Question :** Pendant la garde qui suit le lancer, la garde ignore les fronts et prend en compte le niveau à sa fin (DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement »). Un utilisateur qui a relâché le bouton sans lancer, hélices tournantes en main (DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer »), appuie brièvement puis relâche avant la fin de la garde : l'appui n'a aucun effet et les hélices continuent de tourner. Ce cas est-il accepté ?
**Réponse :**
**Décision liée :**

### DOU-101 — Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Extrait de DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » pour lui donner une échéance : avant la phase « besoins ». L'armement exige un drone immobile et à plat, au sol ou dans la main (DEC-056 « Armement : drone immobile, sans autotest »), tous les tests étant faits à 2 s d'appui (DEC-110 « Armement refusé à 2 secondes d'appui : tous les tests faits, un seul signal Refus, sans attente de l'immobilité »). Un drone tenu en main n'est jamais parfaitement immobile : quelle tolérance de mouvement rend le cas nominal (armement dans la main, SCN-001 « Vol nominal : de la batterie au posé ») réalisable sans refus répétés ? Le critère doit être fixé avant les besoins, car il détermine ce qu'un besoin d'armement peut exiger. Complément du 2026-10-28 : l'échéance « avant les besoins » est confirmée et liée au jalon DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir ».
**Réponse :**
**Décision liée :** DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » (jalon, doute non levé)

### DOU-102 — Registre consolidé des risques acceptés
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Les quinze risques acceptés de `reprise.md` (dont trois ajoutés le 2026-10-28 : batterie lithium, drone laissé allumé, programmation) ne couvrent pas : DEC-057 « Pas de détection dédiée d'un drone attrapé ou posé sur un obstacle », DEC-060 « Défaillance d'un capteur ou d'un moteur en vol : hors périmètre », DEC-063 « Choc contre un obstacle ou un plafond : aucune réaction dédiée », DEC-013 « Pas de contrôle de la batterie en vol », DEC-014 « Pas de coupure sur choc en vol », DEC-066 « Commande sans fil corrompue : aucun contrôle d'intégrité », DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur » et DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu ». Autres décisions à examiner pour le registre : DEC-032 « Vol libre : le drone vole sans appareil de suivi », DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée », DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal », DEC-056 « Armement : drone immobile, sans autotest », DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » et DEC-045 « Seuils de sécurité réglables comme le reste, sans borne ». Où tient le registre consolidé des risques acceptés, avec quel périmètre (toutes les décisions « risque accepté ») et quel lien avec DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? » (où l'utilisateur est informé des limites d'emploi) ?
**Réponse :**
**Décision liée :**

### DOU-103 — Signal Allumé après Posé, Refus et Désarmement : donné au retour à l'attente ou silencieux ?
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Question :** Le signal « Allumé » est défini à la mise sous tension et comme relais après une coupure en vol (DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil »). Après un « Posé » (DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler »), un « Refus » (DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté ») et un « Désarmement » (DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté »), le drone revient à « Allumé, en attente d'un appui » (DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui », DEC-082 « Retours à l'attente après le posé ou une coupure des moteurs : compteur à zéro, appui en cours ni pris en compte ni compté ») : le signal « Allumé » est-il donné à ce retour à l'attente, ou le drone reste-t-il silencieux ?
**Réponse :**
**Décision liée :**

### DOU-104 — Jalon avant les besoins non contrôlé par l'outil de porte
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » et DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal »
**Question :** DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » et DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal » doivent être levés avant la phase « besoins », mais restent non bloquants pour la porte « scénarios » (DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir »). L'outil `tools/check_traceability.py --gate` ne bloque que sur « Bloquant : Oui » : rien n'empêche donc techniquement d'ouvrir les besoins. Comment tenir ce jalon : marquer ces doutes bloquants, ajouter à l'outil une option de phase (échéance par doute), ou accepter la promesse de l'architecte sans contrôle outillé ?
**Réponse :**
**Décision liée :** DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » (jalon, doute non levé)

### DOU-105 — Bouton en mode réglage, moteurs coupés : comportement autre que ne jamais armer
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Seul « le bouton n'arme jamais en mode réglage » est écrit (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »). Dans l'état « Mode réglage, moteurs coupés », que fait le bouton : un appui est-il validé à 1 s avec le signal « Appui validé » ? un signal est-il donné à 2 s, ou à 10 s ? un 4e appui d'affilée compte-t-il ? un appui maintenu est-il ignoré ou sans effet ? Complète DOU-097 « Bouton encore maintenu à l'entrée en mode réglage (3e appui) » (qui ne traite que l'entrée) sans le fusionner.
**Réponse :**
**Décision liée :** DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »

### DOU-106 — Bouton en échec d'initialisation après un premier relâchement
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-011 « Dégradé : coupure d'alimentation en vol »
**Question :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-011 « Dégradé : coupure d'alimentation en vol » disent que le drone en échec d'initialisation ignore le bouton, alors que la note du diagramme a et DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement » l'ignorent seulement jusqu'au premier relâchement. Après ce premier relâchement, le bouton reste-t-il ignoré pour toujours (échec définitif jusqu'au débranchement : DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie ») ou seulement jusqu'au premier relâchement ? Un appui de 2 s en échec d'initialisation donne-t-il le signal « Refus », ou rien ?
**Réponse :**
**Décision liée :** DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement »

### DOU-107 — Exigences sans scénario amont : protections de la batterie, sous-tension, brown-out, CEM
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol »
**Question :** La batterie est hors périmètre des scénarios (DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter ») et la règle de la phase 0 impose qu'un besoin cite au moins un scénario. Des exigences que l'architecture matérielle peut imposer (protections matérielles de la batterie, détection de sous-tension, brown-out du microcontrôleur, CEM) n'auraient alors aucun scénario amont. Comment les tracer : par un scénario, par une contrainte, ou par une exception de méthode consignée ? Voir DEC-097 « Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé » et DOU-060 « Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle ».
**Réponse :**
**Décision liée :** DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter »

## Archive — doutes levés

### DOU-001 — Comment le drone informe-t-il l'utilisateur ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Le drone « informe » à 7 moments (allumé, prêt, lancé, stabilisation, stationnaire, atterrissage, posé). Par LED, buzzer, vibration, ou sans fil (téléphone) ? Combien de signaux distincts, sachant que le drone vole (la LED est-elle visible, le buzzer audible) ?
**Réponse :** LED RGB, buzzer et communication sans fil, combinés. Motifs précis à définir en architecture ; contenu de la liaison sans fil : voir DOU-008 « L'utilisateur veut-il suivre le vol depuis un autre appareil ? ». Depuis : DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée » — LED RGB et buzzer ne sont plus qu'une proposition d'architecture ; seule l'intention (signaux lumineux, sonores et suivi sur un autre appareil) reste décidée.
**Décision liée :** DEC-001 « Information de l'utilisateur par signaux lumineux, sonores et suivi sur un autre appareil »

### DOU-002 — Que veut dire ne pas dériver horizontalement ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « Ne dérive pas horizontalement » exige de mesurer la position ou la vitesse horizontale (capteur de flux optique, par exemple). Veux-tu une dérive maximale chiffrée (en cm sur les 10 s), ou seulement une vitesse horizontale proche de zéro ? Le capteur de position est un surcoût en masse et en complexité pour un drone de poche.
**Réponse :** Centrale inertielle seule ; dérive maximale de 30 cm sur 10 s en objectif à valider par essais (non garanti). Depuis : DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée » — la centrale inertielle seule n'est plus qu'une proposition d'architecture ; seul l'objectif de dérive reste décidé.
**Décision liée :** DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais »

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
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Atterrissage « doux » : quelle vitesse maximale au contact ? Le drone se pose-t-il à l'endroit où il est (sol plat) ou revient-il vers le point de lancer ? Quelle durée de descente ?
**Réponse :** Le drone se pose sur place ; vitesse au contact de 0,5 m/s au plus ; descente de 15 s au plus, après quoi les moteurs sont coupés.
**Décision liée :** DEC-020 « Atterrissage sur place », DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »

### DOU-008 — L'utilisateur veut-il suivre le vol depuis un autre appareil ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Veut-il voir les états du vol sur un téléphone ou un ordinateur, en plus de ce que le drone signale lui-même ? Faut-il un geste préalable avant le vol ? Le vol doit-il fonctionner sans cet appareil (par défaut oui) ?
**Réponse :** Oui : le drone retourne à un appareil de suivi les variables du vol (commandes des moteurs, hauteur, autres données de position). L'appareil n'est pas précisé à ce stade ; la technologie relève de l'architecture.
**Décision liée :** DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol »

### DOU-014 — Quel scénario de mise en service faut-il écrire ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Question :** Premier montage : flash du micrologiciel avec le ST-LINK, première mise sous tension, calibrage de la centrale inertielle, test des moteurs hélices démontées, sens de rotation, réglage des seuils (batterie, angle). Que doit pouvoir faire l'utilisateur, dans quel ordre, et que se passe-t-il si le calibrage échoue ? Relevé par la relecture du critique à la porte « scénarios ».
**Réponse :** La mise en service est la programmation du ou des microcontrôleurs avec un programmateur ST-LINK (seul outil de programmation disponible), via JTAG ou SWD ; scénario SCN-008 « Mise en service : programmation du drone » écrit. Les opérations suivantes (calibrage, essais des moteurs) font l'objet de DOU-031 « Quelles opérations suivent la programmation à la mise en service ? ». Depuis : DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée » — le programmateur ST-LINK n'est plus qu'une proposition d'architecture ; seule la programmation du drone à la mise en service reste décidée.
**Décision liée :** DEC-024 « Mise en service par programmation avec un programmateur ST-LINK »

### DOU-015 — Que se passe-t-il si l'initialisation échoue ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Si le drone n'est pas en état de voler au démarrage (mesure absente, drone déplacé au démarrage), annonce-t-il « allumé » à tort ? Faut-il exiger un drone immobile à la mise sous tension et un signal distinct d'échec ?
**Réponse :** L'utilisateur pose le drone immobile avant de brancher la batterie. Si le drone n'est pas en état de voler au démarrage, il refuse de s'armer, ignore le bouton et donne un signal d'échec d'initialisation distinct ; on en sort en débranchant puis rebranchant la batterie. Durée d'immobilité : à fixer en exigences.
**Décision liée :** DEC-030 « Drone posé immobile à la mise sous tension ; refus de s'armer si l'initialisation échoue »

### DOU-016 — Comment limiter le risque d'hélices en rotation sans lancer ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » accepte le risque sans le borner : relâchement en main, drone posé, doigt qui glisse. Faut-il, au minimum, une coupure rapide des moteurs si aucun lancer n'est détecté, ou reconsidérer la confirmation par la centrale inertielle (écartée par DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs ») ? À arbitrer par l'utilisateur.
**Réponse :** Statu quo : aucune coupure ni confirmation ; risque accepté, limité par les protège-hélices obligatoires.
**Décision liée :** DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer »

### DOU-017 — Que se passe-t-il si l'alimentation est coupée ou chute en vol ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Un lancer vigoureux peut débrancher la batterie ou faire chuter la tension, et le microcontrôleur peut redémarrer en vol. Le drone peut-il alors se réarmer seul, notamment si le bouton est appuyé ? Décision attendue : jamais de réarmement automatique. La batterie est-elle mesurée à vide ou sous charge à l'armement (voir DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? ») ?
**Réponse :** Jamais de réarmement automatique après un redémarrage ; batterie mesurée à vide à l'armement, avec un seuil à marge large (valeur à fixer en DOU-013 « Quelle durée de vol garantit-on après un armement accepté ? »).
**Décision liée :** DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement »

### DOU-018 — Quel est le comportement à l'atterrissage et après le posé ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Quel critère détecte « posé » (arrêt de la descente, choc) sans capteur supplémentaire ? Que se passe-t-il en cas de rebond, d'atterrissage de travers ou sur sol incliné ? La détection de basculement de DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » est-elle désactivée une fois posé ? Quel est l'état du drone après un posé ou une coupure (verrouillé, initialisé), et comment le réarme-t-on, jamais automatiquement ? À traiter avec DOU-007 « Quelles contraintes d'atterrissage ? ».
**Réponse :** Le drone se déclare posé et coupe ses moteurs à moins de 2 à 3 cm du sol (rebond couvert). Après le posé ou toute coupure, il est verrouillé ; un nouvel appui de 2 secondes sur le bouton le réarme, jamais automatiquement.
**Décision liée :** DEC-022 « Moteurs coupés à moins de 2 à 3 cm du sol », DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler »

### DOU-019 — Quel capteur donne l'altitude et la vitesse verticale ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » repose sur un capteur de hauteur, alors que DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais » retient une centrale inertielle seule. Sans capteur d'altitude, l'altitude se calcule par intégration et diverge. Faut-il un baromètre ou un capteur de distance ? À trancher avant les exigences, car cela change la carte.
**Réponse :** Capteur de distance de type ToF, orienté vers le bas, pour la hauteur et la vitesse verticale. Depuis : DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée » — le capteur ToF n'est plus qu'une proposition d'architecture ; seule la mesure de la hauteur au-dessus du sol en vol reste décidée.
**Décision liée :** DEC-019 « Hauteur au-dessus du sol mesurée en vol »

### DOU-020 — Quel est le public visé et quel risque pour les personnes est acceptable ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Adulte seulement, ou enfant aussi ? Sans cette réponse, les risques de DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » et de DEC-014 « Pas de coupure sur choc en vol » (hélices nues qui continuent après un choc) ne peuvent pas être jugés. Protège-hélices obligatoires ou optionnels ? Norme jouet visée ou non ?
**Réponse :** Public adulte uniquement, pas de norme jouet ; protège-hélices obligatoires.
**Décision liée :** DEC-016 « Public adulte, protège-hélices obligatoires »

### DOU-024 — Comment arrêter un drone en vol sans le saisir ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Atteindre le bouton d'un drone en vol revient à l'attraper, hélices tournantes. Faut-il un arrêt d'urgence par le sans fil (voir DOU-008 « L'utilisateur veut-il suivre le vol depuis un autre appareil ? »), des protège-hélices, ou accepte-t-on que seul le bouton existe ?
**Réponse :** Deux moyens coexistent une fois le drone lancé : le bouton (DEC-015 « Bouton appuyé en vol : arrêt d'urgence ») et une commande d'arrêt sans fil, en vol normal comme en vol de réglage. Sans appareil de suivi, seul le bouton reste. Suites : DOU-025 « Le drone vole-t-il sans appareil de suivi ? », DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? », DOU-047 « Appareil de suivi : appairage, absence, plusieurs drones ».
**Décision liée :** DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil »

### DOU-025 — Le drone vole-t-il sans appareil de suivi ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Le drone arme-t-il et vole-t-il sans téléphone ni ordinateur ? Perdre le suivi en vol change-t-il quelque chose ? Lié à DOU-008 « L'utilisateur veut-il suivre le vol depuis un autre appareil ? ».
**Réponse :** Vol libre : le drone arme et vole sans appareil de suivi ; un appareil présent est un plus, pas une nécessité. La perte du lien en vol normal ne change rien. Les moyens d'arrêt sans fil et de suivi ne sont disponibles que si un appareil est relié (voir DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil »). Suites : DOU-037 « Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ? », DOU-047 « Appareil de suivi : appairage, absence, plusieurs drones ».
**Décision liée :** DEC-032 « Vol libre : le drone vole sans appareil de suivi »

### DOU-026 — L'utilisateur veut-il régler le drone depuis un autre appareil ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Veut-il seulement être informé, ou aussi régler le drone (seuils, valeurs) ? Si oui, dans quels états (au sol, désarmé seulement) ? Les réglages sont-ils conservés après coupure ?
**Réponse :** Oui : le drone doit être paramétrable sans fil, y compris en vol. États autorisés, entrée dans le mode réglage et conservation des réglages : voir DOU-032 « Comment entre-t-on dans le mode réglage et comment en sort-on ? », DOU-033 « Que fait le drone pendant les vols de réglage répétés ? » et DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? ».
**Décision liée :** DEC-025 « Suivi et réglage du drone par le sans fil, y compris en vol »

### DOU-031 — Quelles opérations suivent la programmation à la mise en service ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Question :** Après la programmation, l'utilisateur doit-il faire d'autres opérations avant le premier vol : calibrage des mesures du drone (drone immobile, à plat), essai des moteurs hélices démontées, vérification du sens de rotation, réglage de valeurs (seuil de batterie, angle de coupure) ? Dans quel ordre, et que se passe-t-il si la programmation ou le calibrage échoue ? Voir aussi DOU-015 « Que se passe-t-il si l'initialisation échoue ? ».
**Réponse :** Aucune opération imposée après la programmation à ce stade : un éventuel calibrage dépend des solutions techniques et sera défini en architecture. L'utilisateur règle ensuite le vol (SCN-009 « Réglage et suivi du drone par le sans fil »).
**Décision liée :** DEC-026 « Mise en service : calibrage éventuel renvoyé à l'architecture, réglage du vol par un scénario dédié »

### DOU-032 — Comment entre-t-on dans le mode réglage et comment en sort-on ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** L'utilisateur pense à trois appuis sur le bouton pour entrer dans le mode réglage, sans certitude. Faut-il ce geste, une commande sans fil, ou les deux ? Comment sort-on du mode (appui, commande, fin du délai, coupure de la batterie) ? Le drone signale-t-il l'entrée et la sortie ? Le mode réglage peut-il être déclenché par erreur pendant un vol normal ?
**Réponse :** Entrée par trois appuis sur le bouton, drone au sol et non armé ; le drone signale l'entrée. Sortie seulement par coupure de la batterie : après un redémarrage, le drone est en mode normal.
**Décision liée :** DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie »

### DOU-033 — Que fait le drone pendant les vols de réglage répétés ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** En mode réglage, le drone décolle, se pose, décolle, se pose, un certain nombre de fois sur un temps bref. Combien de cycles, quelle durée, quelle hauteur ? Décolle-t-il seul depuis le sol (exception au lancer à la main de DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs ») ou sur commande de l'utilisateur à chaque fois ? Que se passe-t-il si le lien sans fil est perdu, si l'utilisateur appuie sur le bouton (DEC-015 « Bouton appuyé en vol : arrêt d'urgence ») ou si les réglages rendent le vol instable ?
**Réponse :** Sur commande sans fil, le drone décolle depuis le sol, reste 3 secondes en stationnaire, puis se pose ; il coupe ses moteurs 15 secondes au plus après le décollage, stationnaire de 3 secondes fixe (voir DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu »). Si le lien sans fil est perdu en vol, il atterrit doucement sur place. Le bouton appuyé en vol reste un arrêt d'urgence. Hauteur et délai de lien perdu : DOU-035 « Quelle hauteur de stationnaire vise-t-on ? » et DOU-036 « Après quel délai le lien sans fil est-il considéré comme perdu ? ».
**Décision liée :** DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu »

### DOU-034 — Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Un mauvais réglage peut rendre le drone instable. Existe-t-il un retour aux valeurs d'origine ? Les réglages sont-ils conservés après coupure de la batterie, et que fait le drone au démarrage s'il n'a jamais été réglé ?
**Réponse :** Conservation : une commande sans fil sauvegarde les réglages, le drone charge au démarrage ses dernières valeurs depuis sa mémoire non volatile, sans configuration poussée par l'appareil de suivi (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage »). Retour à des réglages sûrs : pas de commande de retour aux valeurs d'origine (reprogrammation comme seul recours), mémoire corrompue non traitée, risques acceptés (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »). Drone neuf, mémoire jamais écrite : valeurs d'origine fixes du logiciel, sans signal particulier (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal »). Valeurs d'origine et bornes à fixer : DOU-038 « Réglages en vol : valeurs d'origine, bornes, coupures en vol de réglage ? ».
**Décision liée :** DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage », DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée », DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal »

### DOU-037 — Faut-il un arrêt d'urgence sans fil et un décollage protégé en mode réglage ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Une commande d'arrêt d'urgence sans fil existe-t-elle ? La commande « Décoller » exige-t-elle un appairage, une confirmation, ou la vérification que le drone est posé, immobile et à plat ? Que fait le drone s'il est tenu en main ? Le seul arrêt est aujourd'hui le bouton (DEC-015 « Bouton appuyé en vol : arrêt d'urgence »), donc il faut attraper le drone hélices tournantes. Complète DOU-024 « Comment arrêter un drone en vol sans le saisir ? », levé par DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ». Impact de DEC-032 « Vol libre : le drone vole sans appareil de suivi » : la commande d'arrêt sans fil n'est disponible que si un appareil est relié, donc elle n'est pas une condition de sécurité du vol normal. Reste ouvert après cette commande d'arrêt : la commande d'arrêt sans fil existe, mais il faut encore trancher le décollage protégé en mode réglage (appairage, confirmation, drone posé, immobile et à plat, drone tenu en main). Impact de DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée » : sans appairage, le risque d'une commande « Décoller » parasite (tiers, autre drone) n'est plus couvert ailleurs, ce qui renforce la question de la protection du décollage. Relevé par la relecture critique.
**Réponse :** Pas de protection supplémentaire du décollage en mode réglage (interprétation de la réponse de l'utilisateur : « pour le moment il n'y a qu'un drone, il n'y a pas lieu de faire quelque chose de compliqué, lourd »), donc pas de 17e signal « Décollage refusé ». La commande d'arrêt d'urgence sans fil est couverte par DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ». Risque accepté : une commande « Décoller » parasite est possible, sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »).
**Décision liée :** DEC-038 « Mode réglage : décollage sans protection supplémentaire »

### DOU-038 — Réglages en vol : valeurs d'origine, bornes, coupures en vol de réglage ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Que fait un drone neuf non réglé ? (Répondu par DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal » : il utilise des valeurs d'origine fixes. Reste à fixer ces valeurs d'origine et leurs bornes.) Les coupures de stabilisation et de basculement (DEC-002 « Couper les moteurs si le stationnaire n'est pas atteint dans le délai », DEC-012 « Couper les moteurs si le drone bascule après le stationnaire ») valent-elles en vol de réglage ? Le réglage est-il limité au mode réglage ? Une valeur hors plage est-elle refusée ? Complète DOU-034 « Comment revenir à des réglages sûrs, et les réglages sont-ils conservés ? ». Relevé par la relecture critique.
**Réponse :** Drone neuf : valeurs d'origine fixes (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal »). Les coupures de stabilisation et de basculement valent aussi en vol de réglage ; aucune borne sur les valeurs de réglage ; réglage possible aussi en vol normal, sans entrer dans le mode réglage (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal »). Les valeurs d'origine et les bornes numériques éventuelles sont renvoyées à l'architecture.
**Décision liée :** DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal », DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal »

### DOU-040 — Quel périmètre d'emploi et quelle zone libre minimale ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Intérieur seulement, ou jardin, avec quelles conditions (soleil, sol, herbe) ? Quelle zone libre minimale et quelle distance aux personnes pour un lancer à 4 m/s ? Un lancer à 4 m/s parcourt jusqu'à 8 m en 2 s, ce qui est incompatible avec une pièce d'appartement et avec la dérive de DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais ». Réponse partielle de l'utilisateur, consignée par DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires » : périmètre visé = appartement, gymnase et jardin en essais complémentaires. Lancer trop rapide pour la zone : hors plage, responsabilité de l'utilisateur (DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur »). Reste à trancher : zone libre minimale, distance aux personnes, plage de lancer à garder ou à restreindre en appartement; ancien libellé : lancer trop rapide pour la zone (hors plage ou plage de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » à restreindre). Relevé par la relecture critique.
**Réponse :** Périmètre visé : l'appartement, gymnase et jardin en essais complémentaires (DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires »). Lancer trop rapide pour le lieu : responsabilité de l'utilisateur (DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur »). Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu, incompatibilité appartement / 4 m/s acceptée (DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu »).
**Décision liée :** DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires », DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur », DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu »

### DOU-043 — Quel signal et quel état pour un délai de descente dépassé ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Si les 15 secondes de descente s'écoulent sans être à moins de 2 à 3 cm du sol, les moteurs sont coupés (DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs ») et SCN-001 « Vol nominal : de la batterie au posé » dit que le drone informe qu'il est posé, alors qu'il peut être en l'air. Même signal « Posé », signal d'échec distinct (DEC-005 « Un signal distinct pour chaque information »), ou cas impossible ? Relevé par les deux relectures.
**Réponse :** Signal distinct « Délai de descente dépassé » (17e signal), moteurs coupés, drone verrouillé selon DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler » (DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé »).
**Décision liée :** DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé »

### DOU-047 — Appareil de suivi : appairage, absence, plusieurs drones
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Comment l'appareil de suivi est-il relié au drone ? Le vol normal fonctionne-t-il sans lui ? Une perte de lien en vol normal change-t-elle quelque chose ? (Répondu par DEC-032 « Vol libre : le drone vole sans appareil de suivi » : oui, vol libre, la perte de lien ne change rien en vol normal.) Reste à trancher : appairage, présence de l'appareil, plusieurs drones. Que se passe-t-il avec deux drones dans la même salle ? Recoupe DOU-025 « Le drone vole-t-il sans appareil de suivi ? ». Impact de DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » : la commande d'arrêt sans fil impose un appairage sûr (pas d'arrêt par l'appareil d'un autre drone ou d'un tiers). Scénario manquant proposé : appareil de suivi absent ou lien perdu hors mode réglage. Relevé par la relecture critique.
**Réponse :** Pas d'appairage : le drone obéit à tout appareil de suivi à portée (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »). Le vol normal fonctionne sans appareil de suivi et la perte de lien ne change rien en vol normal (DEC-032 « Vol libre : le drone vole sans appareil de suivi »). Question sur le nombre d'appareils appairés : sans objet sans appairage. Conséquences résiduelles : un tiers ou l'appareil d'un autre drone peut envoyer arrêt, décollage de réglage ou sauvegarde ; une commande peut atteindre plusieurs drones à portée ; le suivi peut être mélangé si plusieurs drones sont à portée. À traiter en architecture si besoin.
**Décision liée :** DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée », DEC-032 « Vol libre : le drone vole sans appareil de suivi »

### DOU-051 — L'état verrouillé est-il le même que l'état allumé, en attente d'un appui ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Après un posé ou une coupure, DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler » prévoit un nouvel appui de 2 s sans débrancher la batterie. Cet état « verrouillé » est-il le même que « Allumé, en attente d'un appui » (mêmes vérifications, mêmes signaux) ? Dans le diagramme d'états, « Posé » et « Moteurs coupés en vol » n'ont aujourd'hui aucune sortie. Relevé par la relecture de cohérence.
**Réponse :** Oui : l'état verrouillé est le même que « Allumé, en attente d'un appui » (DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »). Risque accepté : aucune vérification après une chute ; voir DOU-042 « Quel autotest avant réarmement après un vol raté ? » et DOU-052 « Que fait le drone qui redémarre immobile au sol après une coupure en vol ? ».
**Décision liée :** DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »

### DOU-055 — Le signal Arrêt sans fil (16e signal) est-il validé ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Pour respecter DEC-005 « Un signal distinct pour chaque information », l'architecte a ajouté un 16e signal « Arrêt sans fil » après DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ». Garde-t-on un signal distinct pour l'arrêt sans fil, ou le même signal que « Arrêt par le bouton » ? Voir aussi DOU-027 « Un signal distinct par information, ou par catégorie ? ».
**Réponse :** Le 16e signal est validé et reste distinct du signal n° 14 « Arrêt par le bouton ».
**Décision liée :** DEC-033 « Signal Arrêt sans fil distinct du signal Arrêt par le bouton »

### DOU-056 — Commande sans fil et état du drone : que fait chaque commande dans chaque état ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Partie levée par DEC-043 « Commandes sans fil acceptées selon l'état du drone » : table des commandes sans fil (Décoller, Arrêt, Modifier, Sauvegarder) selon l'état. **Reste ouvert :** après un vol de réglage terminé normalement, ou après un arrêt (bouton, sans fil, échec, basculement) en vol de réglage, le drone est-il verrouillé (DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler ») ou revient-il au mode réglage au sol, prêt à une nouvelle commande « Décoller » ? Tient compte de DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement », DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée », DEC-028 « Mode réglage : décollage depuis le sol sur commande sans fil » et DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu ». Relevé par les relectures de la porte « scénarios ».
**Réponse :** Table des commandes sans fil selon l'état : DEC-043 « Commandes sans fil acceptées selon l'état du drone ». État après un vol de réglage : le drone reste en mode réglage, posé, prêt à une nouvelle commande « Décoller », sans verrouillage (DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage », interprétation de la réponse de l'utilisateur). Le cas d'un arrêt ou d'un échec en vol de réglage était une lecture de l'architecte ; depuis : confirmé par l'utilisateur le 2026-10-27 (DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage », DOU-065 « Quelles décisions relayées ou interprétées sont à confirmer explicitement à la porte ? »).
**Décision liée :** DEC-043 « Commandes sans fil acceptées selon l'état du drone », DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage »

### DOU-057 — Les seuils de sécurité sont-ils des paramètres réglables sans borne ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Les seuils de sécurité (délai de 2 s de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs », angle limite de DEC-012 « Couper les moteurs si le drone bascule après le stationnaire », délai de 15 s de DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs », seuil de batterie) sont-ils des paramètres réglables ? DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » dit que les coupures valent en vol de réglage (Q1) mais qu'aucune borne ne limite les valeurs (Q2) : un réglage sans borne peut désactiver une coupure. Contradiction à lever. Relevé par les relectures de la porte « scénarios ».
**Réponse :** Les seuils de sécurité sont réglables comme le reste, sans borne (DEC-045 « Seuils de sécurité réglables comme le reste, sans borne »). Conséquence acceptée : une valeur peut désactiver une coupure, y compris par un tiers sans appairage. Depuis : réponse révisée par DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » le 2026-10-27 : les seuils de sécurité restent réglables, mais seulement dans des bornes fixées par le logiciel ; une valeur hors bornes est refusée ; aucune valeur réglable ne supprime une coupure.
**Décision liée :** DEC-045 « Seuils de sécurité réglables comme le reste, sans borne », DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel »

### DOU-066 — Le critère de stationnaire peut-il être rempli au sol ou dans la main ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-002 « Échec : stationnaire non atteint dans le délai »
**Question :** Le critère de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » (vitesse < 0,3 m/s, inclinaison < 10°, tenues 0,5 s) n'exige pas que le drone soit en l'air. Un drone armé puis relâché sans lancer, posé à plat ou tenu immobile en main, se déclare « En vol stationnaire » au bout de 0,5 s ; selon la consigne de hauteur (DOU-035 « Quelle hauteur de stationnaire vise-t-on ? »), il peut décoller seul de la table ou de la main. Même cas après une chute à plat au sol pendant la stabilisation : le drone peut alors redécoller seul, contraire à l'esprit de DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement ». La prémisse de DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer » (cas « couvert par SCN-002 « Échec : stationnaire non atteint dans le délai » ») est fausse : SCN-002 « Échec : stationnaire non atteint dans le délai » ne se déclenche pas si le critère est rempli au sol. Questions : (1) le critère de stationnaire doit-il exiger que le drone soit en l'air (hauteur minimale) ? (2) L'utilisateur maintient-il l'acceptation du risque de DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer » en connaissant ce comportement ? (3) Que fait un drone qui touche le sol pendant la stabilisation : contact au sol, moteurs tournant jusqu'à 2 s, ou plus si le délai est réglé (DEC-003 « Drone retourné ou très incliné : normal tant que la stabilisation n'est pas finie », DEC-014 « Pas de coupure sur choc en vol », DEC-045 « Seuils de sécurité réglables comme le reste, sans borne ») ? Options notées, non tranchées : (a) ajouter une condition « en l'air » au critère de stationnaire ; (b) réaccepter explicitement le risque. Selon la réponse, ajouter à SCN-002 « Échec : stationnaire non atteint dans le délai » les cas « drone non lancé » et « contact au sol pendant la stabilisation ». Relevé par la relecture critique de la porte « scénarios ».
**Réponse :** Option (a) : le critère de stationnaire de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » exige en plus que le drone soit en l'air, au-dessus d'une hauteur minimale mesurée sous lui (valeur à fixer en architecture). (1) Oui, condition « en l'air » ajoutée. (2) DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer » reste valable et retrouve sa justification : un drone relâché sans lancer, posé ou tenu immobile en main, n'est jamais déclaré en stationnaire et coupe ses moteurs au bout du délai de 2 s (SCN-002 « Échec : stationnaire non atteint dans le délai »). (3) Un drone en contact avec le sol pendant la stabilisation n'atteint pas non plus le stationnaire : coupure au bout du délai, tant que ce délai n'est pas modifié (DEC-045 « Seuils de sécurité réglables comme le reste, sans borne »). Depuis : DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » — le délai et la hauteur minimale restent dans leurs bornes ; la coupure vaut pour toute valeur réglable. Alternative (b) écartée. Source : décision de l'utilisateur en chat, au sujet de DOU-066 « Le critère de stationnaire peut-il être rempli au sol ou dans la main ? » : « option (a), condition « en l'air » ajoutée au critère de stationnaire. »
**Décision liée :** DEC-049 « Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale », DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs », DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer »

### DOU-067 — L'appui qui arrête le drone peut-il le réarmer ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Après une coupure des moteurs (arrêt par le bouton de SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol », basculement, échec de stabilisation), le drone revient à l'état « Allumé, en attente d'un appui » (DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »). Si l'appui qui a provoqué l'arrêt reste maintenu 2 s (utilisateur qui tient le drone saisi), le drone s'arme ; au relâchement, les moteurs redémarrent dans la main (DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs »). DOU-045 « Que fait un bouton enfoncé au branchement ou maintenu après désarmement ? » et DOU-023 « Quel appui sur le bouton juste après le lancer est ignoré ? » ne couvrent pas ce cas. Question : un appui déjà en cours au moment d'une coupure des moteurs est-il ignoré jusqu'au relâchement ? Relevé par la relecture critique de la porte « scénarios ».
**Réponse :** Oui : un appui sur le bouton déjà en cours au moment d'une coupure des moteurs (arrêt par le bouton, basculement, échec de stabilisation, et toute autre coupure des moteurs) est ignoré jusqu'au relâchement ; il faut un nouvel appui distinct pour armer. Alternative écartée : compter cet appui pour l'armement (aucun bénéfice d'usage, risque de redémarrage des moteurs dans la main). Source : décision de l'utilisateur en chat, au sujet de DOU-067 « L'appui qui arrête le drone peut-il le réarmer ? » : « appui en cours ignoré jusqu'au relâchement. »
**Décision liée :** DEC-050 « Appui en cours lors d'une coupure des moteurs ignoré jusqu'au relâchement », DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »

### DOU-065 — Quelles décisions relayées ou interprétées sont à confirmer explicitement à la porte ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Les décisions relayées à l'architecte ou interprétées (DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » à DEC-048 « Renommage de SCN-009 ») sont-elles confirmées explicitement par l'utilisateur à la porte « scénarios » ? DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » et DEC-038 « Mode réglage : décollage sans protection supplémentaire » portent la mention « à confirmer à la porte ». À confirmer aussi : DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage » (après un arrêt, un échec ou un basculement en vol de réglage, le drone reste en mode réglage, ce que l'utilisateur n'a pas dit explicitement). À confirmer aussi : DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » (seuils de sécurité réglables sans borne, y compris par un tiers sans appairage). Reclassé bloquant par la relecture critique de la porte « scénarios » : la question porte sur la porte « scénarios » elle-même. Ce doute se lève par la confirmation écrite de l'utilisateur dans l'accord de porte.
**Réponse :** 2026-10-27 : DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage » confirmée par l'utilisateur, y compris après un arrêt, un échec ou un basculement en vol de réglage (« il faut garder Prêt à redécoller tout de suite via une commande sans fils » ; options B et D écartées). 2026-10-27 : DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » revue par l'utilisateur et remplacée par DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » (« C. Réglables mais bornés »). 2026-10-27 : DEC-038 « Mode réglage : décollage sans protection supplémentaire » confirmée par l'utilisateur (« A. Aucune protection, le regleur est experimenté »). 2026-10-27 : DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil » confirmée par l'utilisateur (« B. Bouton + coupure sans fil »). 2026-10-27 : confirmation en bloc par l'utilisateur, telles qu'écrites (réponse de l'utilisateur en chat : confirmation en bloc des décisions ci-après): DEC-032 « Vol libre : le drone vole sans appareil de suivi », DEC-033 « Signal Arrêt sans fil distinct du signal Arrêt par le bouton », DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage », DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée », DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal », DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée », DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal », DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires », DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur », DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu », DEC-043 « Commandes sans fil acceptées selon l'état du drone », DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé », DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui », DEC-048 « Renommage de SCN-009 ». Toutes les décisions de la plage sont donc confirmées ou remplacées : le doute est levé.
**Décision liée :** DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil », DEC-038 « Mode réglage : décollage sans protection supplémentaire », DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage », DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel »

### DOU-030 — Les valeurs provisoires sont-elles à confirmer avant les exigences ?
**Statut :** Levé
**Bloquant :** Oui
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs », DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » et DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » portent des valeurs provisoires, à confirmer par essais, alors que leurs doutes sont « Levé ». Les considère-t-on comme levées pour la porte « scénarios », avec confirmation par essais avant la porte « exigences » ? Reclassé bloquant par la relecture critique de la porte « scénarios » : la question porte sur la porte « scénarios » elle-même, elle doit donc être tranchée avant de la franchir.
**Réponse :** Option (a) : les scénarios sont validés avec les valeurs de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » (2 s), DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » (0,5 à 4 m/s, au moins 1,5 m) et DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » (60°), marquées provisoires, à confirmer par analyse ou par essais avant la porte « exigences », y compris les limites de la plage de lancer (lien avec DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m »). Une phrase de SCN-001 « Vol nominal : de la batterie au posé » le dit. Alternatives écartées : (b) confirmer maintenant (bloque la porte sans architecture ni prototype) ; (c) tenir les valeurs pour définitives (faux, voir DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m »). Source : décision de l'utilisateur en chat, au sujet de DOU-030 « Les valeurs provisoires sont-elles à confirmer avant les exigences ? » : « option (a), valeurs provisoires pour cette porte, à confirmer avant la porte exigences, mention dans SCN-001 « Vol nominal : de la batterie au posé » [titre ajouté] ».
**Décision liée :** DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences »

### DOU-054 — Les décisions de solution technique restent-elles dans le journal ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-001 « Information de l'utilisateur par signaux lumineux, sonores et suivi sur un autre appareil », DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais », DEC-019 « Hauteur au-dessus du sol mesurée en vol » et DEC-024 « Mise en service par programmation avec un programmateur ST-LINK » fixent des solutions (LED et buzzer, centrale inertielle seule, capteur de distance, programmateur ST-LINK), alors que les scénarios ne doivent pas en décrire. Deux options : (a) les garder avec le statut « contrainte posée par l'utilisateur, à confirmer en architecture » ; (b) ne garder dans le journal que l'intention et déplacer la solution dans `notes-architecture.md`. Relevé par la relecture de cohérence.
**Réponse :** Option (b) : le journal ne garde que l'intention ; la solution (LED et buzzer de DEC-001 « Information de l'utilisateur par signaux lumineux, sonores et suivi sur un autre appareil », centrale inertielle seule de DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais », capteur de distance de type ToF de DEC-019 « Hauteur au-dessus du sol mesurée en vol », programmateur ST-LINK de DEC-024 « Mise en service par programmation avec un programmateur ST-LINK ») est déplacée comme proposition dans « Notes pour l'architecture » — `notes-architecture.md`, à arbitrer en architecture. Aucune n'est une contrainte imposée par l'utilisateur. Les quatre décisions portent une mention « Depuis » ; les scénarios ne nomment plus que l'intention. Alternative écartée : (a) les garder comme contraintes. Source : décision de l'utilisateur en chat, au sujet de DOU-054 « Les décisions de solution technique restent-elles dans le journal ? » : « option (b), aucune contrainte imposée. »
**Décision liée :** DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée »

### DOU-022 — À partir de quand compte le chrono des 10 secondes, et que fait un lancer avec le bouton encore appuyé ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Question :** Les 10 secondes de DEC-008 « Désarmement si le bouton reste appuyé plus de 10 secondes » courent-elles depuis l'appui initial ou depuis l'armement (2 s plus tard) ? L'utilisateur qui lance à 9,9 s et relâche à 10,1 s désarme-t-il le drone ?
**Réponse :** Depuis l'appui initial. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-054 « Chrono de 10 secondes compté depuis l'appui initial »

### DOU-023 — Quel appui sur le bouton juste après le lancer est ignoré ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Un appui ou un relâchement parasite juste après le lancer ne doit pas déclencher l'arrêt d'urgence de DEC-015 « Bouton appuyé en vol : arrêt d'urgence » avec un signal trompeur. Pendant combien de temps après le lancer le bouton est-il ignoré, et quel appui volontaire reste pris en compte ?
**Réponse :** Appui et relâchement ignorés pendant une courte garde après le lancer (durée à fixer en architecture), puis arrêt d'urgence. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-055 « Bouton ignoré pendant une courte garde après le lancer »

### DOU-042 — Quel autotest avant réarmement après un vol raté ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** L'armement exige-t-il l'immobilité du drone ou un autotest (hélices, mesures) ? DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement » dit « drone au sol et immobile » alors que SCN-001 « Vol nominal : de la batterie au posé » arme le drone dans la main. Après un vol raté, un drone abîmé peut être réarmé sans vérification. Relevé par la relecture critique. Complément de la relecture de la porte : DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement » parle d'un drone « au sol et immobile », alors que SCN-001 « Vol nominal : de la batterie au posé » arme le drone dans la main : quelle condition vaut vraiment ?
**Réponse :** Armement exigeant un drone immobile (au sol ou dans la main), sans autotest. Source : choix de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-056 « Armement : drone immobile, sans autotest »

### DOU-041 — Que fait le drone si on l'attrape ou s'il descend sur un obstacle ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Coupure, poursuite, signal ? Une main, une table ou une personne sous le drone en descente : que se passe-t-il ? Qui peut arrêter le drone sans saisir les hélices ? Scénario manquant proposé : drone récupéré à la main ou posé sur un obstacle. Relevé par la relecture critique.
**Réponse :** Aucune détection dédiée ; seules les coupures existantes s'appliquent, risque résiduel accepté. Source : choix de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-057 « Pas de détection dédiée d'un drone attrapé ou posé sur un obstacle »

### DOU-044 — Séquence de trois appuis : fenêtre et signal ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Les deux premiers appuis des trois donnent-ils le signal « Appui trop court » (SCN-004 « Appui normal : bouton relâché avant 2 secondes ») ? Quel délai entre appuis ? Que fait un appui long en mode réglage ? Le drone peut-il être tenu en main (DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie » impose un drone posé) ? Relevé par les deux relectures.
**Réponse :** Fenêtre courte (durée en architecture), sans signal « Appui trop court » sur les deux premiers appuis, appui long inchangé. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-058 « Trois appuis : fenêtre courte, sans signal parasite »
**Depuis :** DEC-058 « Trois appuis : fenêtre courte, sans signal parasite » est remplacée par DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage » (le signal « Appui trop court » n'existe plus). La réponse ci-dessus est conservée pour l'historique.

### DOU-045 — Que fait un bouton enfoncé au branchement ou maintenu après désarmement ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Question :** Après le désarmement à 10 s, l'appui en cours est-il ignoré jusqu'au relâchement ? Que fait un bouton déjà enfoncé à la mise sous tension (poche, sac) ou pendant l'initialisation ? Précise DOU-022 « À partir de quand compte le chrono des 10 secondes, et que fait un lancer avec le bouton encore appuyé ? ». Relevé par la relecture critique.
**Réponse :** Ignoré jusqu'au premier relâchement. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement »

### DOU-046 — Capteur ou moteur défaillant en vol : quel comportement ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Mesure de hauteur perdue (sol non réfléchissant, escalier, vitre), hélice bloquée, protège-hélice détaché, moteur qui chauffe : quelle coupure, quel signal ? Scénario manquant proposé : mesure ou moteur défaillant en vol. Relevé par la relecture critique.
**Réponse :** Hors périmètre : aucune détection dédiée, risque résiduel accepté. Source : choix de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-060 « Défaillance d'un capteur ou d'un moteur en vol : hors périmètre »

### DOU-052 — Que fait le drone qui redémarre immobile au sol après une coupure en vol ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol »
**Question :** SCN-011 « Dégradé : coupure d'alimentation en vol » suppose que le drone redémarre en mouvement et donne l'échec d'initialisation. Si l'alimentation revient quand le drone est déjà immobile au sol, l'initialisation réussit : annonce-t-il « Allumé » sans que l'utilisateur ait touché la batterie ? Faut-il toujours rebrancher la batterie ? Harmoniser DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement » et DEC-030 « Drone posé immobile à la mise sous tension ; refus de s'armer si l'initialisation échoue ». Relevé par les deux relectures.
**Réponse :** Le drone annonce « Allumé », sans armement automatique, sans débranchement obligatoire. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-061 « Redémarrage immobile au sol : allumé mais jamais armé »

### DOU-061 — Quelle priorité entre le bouton et l'arrêt sans fil, et l'arrêt est-il pris en compte pendant la phase Lancé ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Quelle priorité entre le bouton et l'arrêt sans fil si les deux arrivent ensemble ? L'arrêt (bouton ou sans fil) est-il pris en compte pendant la phase « Lancé » avant le démarrage des moteurs (voir DOU-023 « Quel appui sur le bouton juste après le lancer est ignoré ? ») ? Complément de la relecture de porte (critique) : la table de DEC-043 « Commandes sans fil acceptées selon l'état du drone » n'a pas de ligne « Lancé, avant démarrage des moteurs » (200 ms, DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs ») ; le sort des commandes Décoller, Modifier et Sauvegarder dans cet intervalle n'est pas dit non plus.
**Réponse :** Arrêt (bouton ou sans fil) ignoré pendant Lancé, avant le démarrage des moteurs ; priorité bouton / sans fil sans objet (même effet). Sort des autres commandes : DOU-072 « Commandes sans fil reçues pendant la phase Lancé : ignorées ou refusées ? ». Source : choix de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-062 « Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs »

### DOU-063 — Que se passe-t-il lors d'un choc contre un obstacle ou un plafond à 4 m/s ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Que se passe-t-il lors d'un choc contre un obstacle ou un plafond en vol, notamment à 4 m/s (DEC-014 « Pas de coupure sur choc en vol ») ? Étend DOU-041 « Que fait le drone si on l'attrape ou s'il descend sur un obstacle ? » et se rattache à DOU-029 « Quelle altitude maximale et quel plafond le drone doit-il tolérer ? ».
**Réponse :** Aucune réaction dédiée, dans la ligne de DEC-014 « Pas de coupure sur choc en vol ». Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-063 « Choc contre un obstacle ou un plafond : aucune réaction dédiée »

### DOU-064 — Drone tenu en main, trois appuis et commande Décoller : quel risque pour la main ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Drone tenu en main, trois appuis puis commande « Décoller » : le drone décolle (DEC-038 « Mode réglage : décollage sans protection supplémentaire ») alors que la main est proche des hélices. Quel risque accepte-t-on ? Voir DOU-044 « Séquence de trois appuis : fenêtre et signal ? ».
**Réponse :** Risque accepté et documenté dans les limites d'emploi. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-064 « Main près des hélices en mode réglage : risque accepté et documenté »

### DOU-068 — Que se passe-t-il si le logiciel se bloque en vol ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Le bouton (DEC-015 « Bouton appuyé en vol : arrêt d'urgence »), l'arrêt sans fil (DEC-031 « Arrêt du drone lancé : bouton et commande d'arrêt sans fil ») et toutes les coupures dépendent du même logiciel. Si le logiciel se bloque avec des commandes des moteurs figées, le drone monte ou dérive ; le seul recours est d'arracher la batterie, hélices tournantes. Quel comportement attend-on (par exemple moteurs coupés en cas de blocage), et quel signal ? Non couvert par DOU-046 « Capteur ou moteur défaillant en vol : quel comportement ? » ni par DOU-060 « Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle ». À lever avant la porte « exigences ». Relevé par la relecture critique de la porte « scénarios ».
**Réponse :** Coupure des moteurs par un mécanisme indépendant du logiciel. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-065 « Logiciel bloqué en vol : coupure des moteurs par un chien de garde »

### DOU-069 — Une commande sans fil corrompue est-elle rejetée ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Une trame sans fil tronquée ou bruitée peut produire une commande « Modifier » à valeur aberrante, appliquée sans borne (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal », DEC-045 « Seuils de sécurité réglables comme le reste, sans borne ») puis rendue permanente par « Sauvegarder » (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »). Le drone rejette-t-il une commande corrompue ? Ce risque technique est distinct du risque « commandes d'un tiers » déjà accepté par DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée ». À lever avant la porte « exigences ». Relevé par la relecture critique de la porte « scénarios ». Note du 2026-10-27 : avec DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel », une valeur aberrante sur un seuil de sécurité est refusée si elle sort des bornes ; le risque reste entier pour les autres réglages et pour les valeurs aberrantes situées dans les bornes.
**Réponse :** Aucun contrôle d'intégrité, risque résiduel accepté. Source : choix de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-066 « Commande sans fil corrompue : aucun contrôle d'intégrité »

### DOU-070 — Le drone doit-il démarrer posé à plat, ou tolérer une surface inclinée ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-010 « Échec : initialisation impossible au démarrage »
**Question :** DEC-030 « Drone posé immobile à la mise sous tension ; refus de s'armer si l'initialisation échoue » et SCN-001 « Vol nominal : de la batterie au posé » demandent un drone « posé immobile », jamais « à plat ». Démarré à 8° sur un accoudoir, le drone peut prendre une horizontale de référence faussée : dérive, ou critère d'inclinaison < 10° de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » jamais rempli. Le scénario doit-il exiger un drone à plat, ou le drone doit-il tolérer une surface inclinée ? Le choix technique (calibrage, référence) est renvoyé à l'architecture (DEC-026 « Mise en service : calibrage éventuel renvoyé à l'architecture, réglage du vol par un scénario dédié »). À lever avant la porte « exigences ». Relevé par la relecture critique de la porte « scénarios ».
**Réponse :** Drone posé à plat exigé ; au-delà d'une inclinaison limite, échec de l'initialisation. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-067 « Démarrage à plat exigé, sinon échec de l'initialisation avec signal »

### DOU-071 — Que fait le drone quand il reçoit une valeur de seuil hors bornes ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » décide qu'une valeur de seuil de sécurité hors bornes est refusée, sans dire comment. Le refus est-il silencieux, donne-t-il un signal sur le drone, ou un retour vers l'appareil de suivi ? La valeur précédente est-elle conservée ? Lien avec DOU-027 « Un signal distinct par information, ou par catégorie ? » (nombre de signaux) et DOU-053 « Vols de réglage : signaux des phases, signal du lien perdu, acquittement des commandes » (acquittement des commandes sans fil). À lever avant la porte « exigences ».
**Réponse :** Refus silencieux, valeur précédente conservée, valeur relue sur l'appareil de suivi. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-068 « Seuil hors bornes : refus silencieux, valeur relue sur l'appareil de suivi »

### DOU-072 — Commandes sans fil reçues pendant la phase Lancé : ignorées ou refusées ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** DEC-062 « Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs » ne dit rien des commandes Décoller, Modifier et Sauvegarder reçues pendant cet intervalle de 200 ms. La table de DEC-043 « Commandes sans fil acceptées selon l'état du drone » n'a pas de ligne « Lancé ». Sont-elles ignorées, refusées avec retour vers l'appareil de suivi, ou prises en compte à la fin de l'intervalle ? Issu de DOU-061 « Quelle priorité entre le bouton et l'arrêt sans fil, et l'arrêt est-il pris en compte pendant la phase Lancé ? ».
**Réponse :** Ignorées, comme l'arrêt. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-069 « Commandes sans fil reçues pendant la phase Lancé : ignorées »

### DOU-077 — Séquence de trois appuis : cas incomplets et ambigus
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** DEC-058 « Trois appuis : fenêtre courte, sans signal parasite » ne traite pas : (a) deux appuis seulement, puis rien (le signal « Appui trop court » est-il donné après coup, sinon l'utilisateur n'a aucun retour) ; (b) un troisième appui maintenu 2 s (mode réglage ou armement) ; (c) le signal « Mode réglage » donné au troisième appui ou à son relâchement. Relevé par la relecture critique du 2026-10-28.
**Réponse :** Plus de signal « Appui trop court » : chaque appui validé (1 s) a son signal « Appui validé » (cas a). Le 3e appui d'affilée entre en mode réglage dès sa validation, sans armement même maintenu (cas b), avec le signal « Mode réglage » (cas c). Source : réponse de l'utilisateur en chat, 2026-10-28. Cas limites restants dans DOU-079 « Compteur d'appuis validés : remise à zéro par un appui de moins de 1 s, cas limites ».
**Décision liée :** DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »

### DOU-081 — Bouton appuyé en vol de réglage : arrêt d'urgence ou non ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** En mode réglage, le bouton n'arme jamais (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »). Pendant un vol de réglage, un appui sur le bouton est-il toujours un arrêt d'urgence ? Non tranché à la demande de l'utilisateur le 2026-10-28. En attendant, DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu » et DEC-015 « Bouton appuyé en vol : arrêt d'urgence » restent écrites et les scénarios les reprennent telles quelles.
**Réponse :** Oui : le bouton appuyé en vol de réglage est un arrêt d'urgence, les moteurs sont coupés et le drone reste en mode réglage. Source : réponse de l'utilisateur en chat, 2026-10-28. Reste le signal donné (DOU-053 « Vols de réglage : signaux des phases, signal du lien perdu, acquittement des commandes ») et l'éventuelle garde après le décollage de réglage (DOU-084 « Garde du bouton après le décollage de réglage ? »).
**Décision liée :** DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage »

### DOU-082 — Sortie du mode réglage : coupure de la batterie seulement, non rediscutée
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** La sortie du mode réglage reste la coupure de la batterie (DEC-027 « Mode réglage : trois appuis sur le bouton au sol, sortie par coupure de la batterie »), laissée telle quelle le 2026-10-28 et non rediscutée avec le nouveau modèle du bouton. À confirmer à la porte « scénarios » : aucune sortie par le bouton ou par le sans fil.
**Réponse :** Confirmé : la seule façon de sortir du mode réglage est d'enlever la batterie. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-079 « Sortie du mode réglage : uniquement en enlevant la batterie »

### DOU-085 — Entrée en mode réglage : exiger drone immobile seulement, ou aussi à plat ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** L'entrée en mode réglage exige un drone « posé et immobile » (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »). Or le drone ne sait pas s'il est posé : il n'y a pas de détection dédiée d'un drone posé, attrapé ou tenu en main (DEC-057 « Pas de détection dédiée d'un drone attrapé ou posé sur un obstacle »). Il ne peut mesurer que son mouvement et son inclinaison. Faut-il donc exiger seulement « immobile », ou « immobile et à plat » comme pour l'armement (DEC-056 « Armement : drone immobile, sans autotest »), le mot « posé » ne gardant que son sens d'intention ? Un drone tenu en main, immobile et à plat, entre alors en mode réglage, et la commande « Décoller » démarre les moteurs dans la main (DEC-064 « Main près des hélices en mode réglage : risque accepté et documenté » ; DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre »). Voir aussi DOU-073 « Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ? » pour la tolérance d'« immobile ».
**Réponse :** Immobile et à plat, non armé ; le mot « posé » n'est plus une condition. Source : réponse de l'utilisateur en chat, 2026-10-28. Reste la tolérance d'« immobile » (DOU-073 « Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ? »).
**Décision liée :** DEC-085 « Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé »

### DOU-086 — Décollage de réglage commandé par un tiers, drone en main ou retourné : risque cumulé accepté ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Trois décisions se cumulent : le drone obéit à tout appareil de suivi à portée (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »), il reste en mode réglage après un vol de réglage, quelle qu'en soit l'issue, prêt à redécoller tout de suite (DEC-044 « Mode réglage persistant : retour au mode réglage après un vol de réglage, sans verrouillage »), et le décollage ne vérifie que la batterie (DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre »). Conséquence : un tiers à portée peut commander « Décoller » alors que l'utilisateur tient le drone en main, ou l'a ramassé retourné ou incliné après un échec ou un basculement en vol de réglage, et les hélices démarrent. Le risque pour une main proche des hélices est accepté pour l'entrée en mode réglage (DEC-064 « Main près des hélices en mode réglage : risque accepté et documenté »), mais pas explicitement dans ce cas cumulé. L'utilisateur accepte-t-il explicitement ce risque cumulé, ou veut-il une condition de plus (par exemple drone à plat ou immobile, délai après un arrêt) ?
**Réponse :** Risque cumulé explicitement accepté : la commande Décoller ne vérifie que la batterie, un appareil à portée peut faire décoller un drone retourné ou tenu en main en mode réglage. À documenter dans les limites d'emploi. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-086 « Décollage de réglage : batterie seulement, risque cumulé avec les décisions sans appairage et sans verrouillage accepté »

### DOU-087 — Appui ignoré en silence pendant une série d'appuis : faut-il un signal ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Question :** Pendant une série d'appuis, le maintien du 2e appui au-delà de 2 s ne fait ni armement, ni signal, ni annulation (DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série »). L'utilisateur qui veut armer, mais dont le premier appui a été relâché trop tôt, maintient le bouton sans rien percevoir de plus que le signal « Appui validé » : il ne sait pas pourquoi le drone ne s'arme pas. Inversement, trois appuis validés accidentels (poche, sac) entrent en mode réglage (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »), seul le signal « Mode réglage » l'indique, et la sortie exige d'enlever la batterie (DEC-079 « Sortie du mode réglage : uniquement en enlevant la batterie »). Faut-il un signal pour l'appui ignoré dans la série, ou le comportement silencieux est-il accepté ? Voir DEC-005 « Un signal distinct pour chaque information » et DOU-027 « Un signal distinct par information, ou par catégorie ? ».
**Réponse :** Aucun signal, comme aujourd'hui ; risque accepté (utilisateur perplexe, mode réglage entré par erreur) et à documenter dans les limites d'emploi. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-084 « Appui ignoré pendant une série d'appuis : aucun signal, risque accepté et documenté »

### DOU-088 — Annulation d'un armement : comment renoncer après le signal Prêt ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes » et SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Une fois le signal « Prêt » donné à 2 s d'appui, le relâchement du bouton démarre les moteurs, même sans lancer (DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs » ; DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard »). Le seul moyen de renoncer sans démarrer les moteurs est de maintenir le bouton jusqu'à 10 s d'appui (DEC-054 « Chrono de 10 secondes compté depuis l'appui initial »), soit 8 s de plus après le signal « Prêt ». Un utilisateur qui change d'avis, ou qui a armé par erreur, n'a pas de geste plus rapide, et les hélices en rotation sans lancer n'ont pas de protection supplémentaire (DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer »). Faut-il un autre moyen d'annuler (autre geste, commande sans fil, délai plus court), ou le maintien de 8 s est-il accepté ?
**Réponse :** On garde le maintien jusqu'au désarmement à 10 s comme seule annulation ; risque accepté et à documenter dans les limites d'emploi. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-083 « Annulation d'un armement : le maintien jusqu'au désarmement à 10 s reste la seule annulation »

### DOU-089 — Arrêt d'urgence par le bouton en vol : filtrage du rebond et des parasites
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Au sol, un appui n'est validé qu'après 1 s de maintien (DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court »). En vol, tout appui sur le bouton est un arrêt d'urgence immédiat (DEC-015 « Bouton appuyé en vol : arrêt d'urgence »). Quel filtrage s'applique à cet appui : aucun, une durée minimale très courte (rebond du contact), ou la même validation de 1 s ? Sans filtrage, un rebond, un parasite électrique ou une vibration coupent les moteurs et le drone tombe ; avec une validation de 1 s, l'arrêt d'urgence arrive trop tard. Le compromis entre coupure intempestive et délai d'arrêt est à décider, avec la valeur du filtrage (voir DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences »). Voir aussi DOU-076 « Garde du bouton après le lancer : front ou niveau, et quelle origine par rapport à la phase Lancé ? ».
**Réponse :** Anti-rebond très court seulement (quelques millisecondes, valeur à fixer en architecture), arrêt quasi immédiat ; ni durée minimale de 100 ms, ni validation de 1 s. Risque connu : un parasite plus long que l'anti-rebond peut couper les moteurs ; à documenter dans les limites d'emploi. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-087 « Arrêt d'urgence par le bouton en vol : anti-rebond très court seulement, arrêt quasi immédiat »

### DOU-090 — Bouton coincé ou maintenu en permanence au démarrage : faut-il un signal ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-010 « Échec : initialisation impossible au démarrage »
**Question :** Un bouton déjà enfoncé à la mise sous tension, pendant l'initialisation ou après un désarmement est ignoré jusqu'à son premier relâchement (DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement »). Si le bouton est coincé (mécanique, saleté, court-circuit) ou maintenu en permanence, le drone ne peut jamais être armé et n'en dit rien : il donne le signal « Allumé » et reste sourd au bouton. L'utilisateur ne sait pas pourquoi. Le drone doit-il signaler cet état (signal existant, nouveau signal, statut sans fil) après un délai donné, ou le silence est-il accepté ? Voir DEC-005 « Un signal distinct pour chaque information » et DOU-027 « Un signal distinct par information, ou par catégorie ? ».
**Réponse :** Statut sans fil seulement : l'appareil de suivi indique « bouton maintenu » ; aucun nouveau signal local, le drone reste silencieux au bouton. Risque accepté pour l'utilisateur sans appareil de suivi, à documenter dans les limites d'emploi. Reste à fixer en architecture : moment et contenu exact du statut. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-088 « Bouton coincé ou maintenu en permanence au démarrage : statut sans fil seulement, aucun signal local »

### DOU-076 — Garde du bouton après le lancer : front ou niveau, et quelle origine par rapport à la phase Lancé ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** DEC-055 « Bouton ignoré pendant une courte garde après le lancer » ignore « tout appui ou relâchement » pendant la garde. Si l'utilisateur appuie pendant la garde et maintient le bouton après sa fin, l'arrêt d'urgence de DEC-015 « Bouton appuyé en vol : arrêt d'urgence » est-il déclenché, tardivement au relâchement, ou jamais ? La garde (de l'ordre de 0,5 s) est plus longue que la phase « Lancé » (200 ms) : son origine (le relâchement du lancer ?) et sa durée minimale par rapport à « Lancé » sont à écrire. Dans SCN-002 « Échec : stationnaire non atteint dans le délai » (relâché sans lancer, hélices tournantes), le réflexe de ré-appuyer tombe dans la garde. Relevé par la relecture critique du 2026-10-28. À lever avant la porte « exigences ». Note du 2026-10-28 : réflexe de ré-appui dans la garde après un relâchement sans lancer. L'utilisateur qui relâche le bouton sur un drone tenu en main voit les hélices démarrer et ré-appuie aussitôt pour les arrêter : cet appui tombe dans la garde et est ignoré. Le cas est le plus probable de ceux qui exposent la main (DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer »). Que doit faire ce ré-appui : rien jusqu'à la fin de la garde, un arrêt différé à la fin de la garde s'il est maintenu, ou un arrêt immédiat ? Voir aussi DOU-089 « Arrêt d'urgence par le bouton en vol : filtrage du rebond et des parasites ».
**Réponse :** La garde ignore les fronts (appuis et relâchements) mais pas le niveau : si le bouton est encore enfoncé à la fin de la garde, arrêt d'urgence à ce moment. La garde commence au relâchement du bouton (geste du lancer), couvre la phase « Lancé » de 200 ms puis le démarrage des moteurs ; durée de l'ordre de 0,5 s à fixer en architecture. Le réflexe de ré-appui reste efficace, avec au plus la durée de la garde de retard. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement »

### DOU-079 — Compteur d'appuis validés : remise à zéro par un appui de moins de 1 s, cas limites
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Question :** Hypothèse de l'architecte, à confirmer : un appui de moins de 1 s n'est pas compté et laisse le compteur d'appuis d'affilée inchangé ou le remet à zéro (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »). Cas voisins non tranchés : (a) le 3e appui validé d'un drone en mouvement ou tenu en main (pas posé et immobile) est-il un appui comme les autres, ignoré, refusé, ou entre-t-il quand même en mode réglage, et avec quel signal ? (b) le signal « Appui validé » est-il remplacé par « Mode réglage » à la 3e validation ? L'appui long qui suit un armement refusé ou un désarmement n'est pas compté : décidé par DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté ».
**Réponse :** (a) Un appui de moins de 1 s au milieu d'une série remet le compteur à zéro (hypothèse confirmée). (b) 3e appui validé sur un drone non immobile ou pas à plat : mode réglage refusé, signal « Refus ». (c) Le signal à la 3e validation est « Mode réglage » (déjà décidé par DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »), « Appui validé » n'étant donné qu'aux deux premières validations. Les retours à l'attente après refus, désarmement, posé ou coupure étaient déjà décidés par DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série », DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté » et DEC-082 « Retours à l'attente après le posé ou une coupure des moteurs : compteur à zéro, appui en cours ni pris en compte ni compté ». Hors de ce doute, en déduction de l'architecte : le compteur après un mode réglage refusé (DOU-091 « Compteur d'appuis après un mode réglage refusé : retour à l'attente, compteur à zéro ? »). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-089 « Appui de moins de 1 s au milieu d'une série d'appuis : compteur remis à zéro » ; DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus » ; DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage » ; DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série » ; DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté » ; DEC-082 « Retours à l'attente après le posé ou une coupure des moteurs : compteur à zéro, appui en cours ni pris en compte ni compté »


### DOU-091 — Compteur d'appuis après un mode réglage refusé : retour à l'attente, compteur à zéro ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-004 « Appui normal : bouton relâché avant 2 secondes »
**Question :** Quand le 3e appui validé est refusé parce que le drone n'est pas immobile et à plat (DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus »), que devient le compteur d'appuis ? DÉDUCTION DE L'ARCHITECTE, non confirmée par l'utilisateur : par analogie avec DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté » et DEC-081 « Bouton encore enfoncé après un refus ou un désarmement : ignoré jusqu'au premier relâchement, puis nouvel appui possible tout de suite », le drone revient à « Allumé, en attente d'un appui », compteur à zéro, le 3e appui n'est pas compté, et le bouton encore enfoncé est ignoré jusqu'au premier relâchement. Alternative : compteur laissé à 3 ou à 2, le prochain appui validé retentant l'entrée en mode réglage. 
**Réponse :** Retour à l'attente, compteur à zéro, le 3e appui n'est pas compté, le bouton encore enfoncé est ignoré jusqu'au premier relâchement, nouvel essai possible tout de suite (déduction de l'architecte, confirmée par l'utilisateur en chat, 2026-10-28).
**Décision liée :** DEC-093 « Mode réglage refusé : retour à l'attente, compteur à zéro, bouton encore enfoncé ignoré » ; DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus »

### DOU-084 — Garde du bouton après le décollage de réglage ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** La garde pendant laquelle le bouton est ignoré ne s'applique qu'après un lancer au relâchement (DEC-078 « Garde du bouton après le lancer : attachée au lancer au relâchement, pas décidée pour le décollage de réglage »). Après un décollage de réglage sur commande sans fil, le bouton appuyé est un arrêt d'urgence (DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage ») : est-il pris en compte dès le décollage, ou une garde existe-t-elle aussi après ce décollage ? Aucun geste de lancer n'y produit d'appui parasite, mais une main proche du bouton peut déclencher un arrêt involontaire. Posé le 2026-10-28 à la demande de l'utilisateur, rien ne le couvrant.
**Réponse :** Après un décollage de réglage sur commande sans fil, le bouton est pris en compte tout de suite comme arrêt d'urgence ; pas de garde, car aucun geste de lancer ne produit d'appui parasite. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-094 « Bouton appuyé après un décollage de réglage : pris en compte tout de suite, sans garde »

### DOU-075 — Le chien de garde couvre-t-il la phase Lancé, et cette phase a-t-elle une durée maximale ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** DEC-065 « Logiciel bloqué en vol : coupure des moteurs par un chien de garde » n'est représenté dans le diagramme que pour « En vol » et « Vol de réglage ». Pendant « Lancé » (DEC-062 « Arrêt ignoré pendant la phase Lancé, avant le démarrage des moteurs »), le bouton, l'arrêt sans fil et les commandes sont ignorés : si le démarrage des moteurs ne se termine pas, le drone reste sourd à tout. Le chien de garde couvre-t-il tout état où les moteurs peuvent être alimentés ? La phase « Lancé » a-t-elle une durée maximale ? Relevé par la relecture critique du 2026-10-28. Complément du 2026-10-28 : le comportement exact en cas de coupure d'alimentation pendant « Lancé » et la suppression de l'état « À définir » des diagrammes sont traités dans DOU-060 « Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle ».
**Réponse :** Le chien de garde couvre tout état où les moteurs peuvent être alimentés, donc aussi la phase « Lancé » ; cette phase a une durée maximale, de l'ordre de quelques centaines de millisecondes, à fixer en architecture et provisoire. Le comportement au dépassement de cette durée n'est pas répondu : voir DOU-093 « Dépassement de la durée maximale de la phase Lancé : que fait le drone ? ». La coupure d'alimentation en phase « Lancé » est traitée par DEC-097 « Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé ». Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale » ; DEC-097 « Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé »

### DOU-074 — Une initialisation en échec est-elle définitive jusqu'au débranchement, et la condition à plat vaut-elle aussi après une coupure en vol ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol » et SCN-010 « Échec : initialisation impossible au démarrage »
**Question :** DEC-061 « Redémarrage immobile au sol : allumé mais jamais armé » dit que le drone qui revient immobile au sol s'initialise, sans la condition « à plat » de DEC-067 « Démarrage à plat exigé, sinon échec de l'initialisation avec signal » : un drone tombé sur la tranche ou retourné est immobile mais pas à plat. Le diagramme d'états fait de « Échec d'initialisation » un état dont on ne sort que par débranchement : or un redémarrage en l'air échoue, puis le drone se pose, et l'utilisateur voit « Échec d'initialisation » sur un drone déjà au sol. L'initialisation est-elle refaite en continu, ou définitive jusqu'au débranchement ? Relevé par la relecture critique du 2026-10-28. À lever avant la porte « exigences ».
**Réponse :** Une fois l'échec d'initialisation établi, il est définitif jusqu'au débranchement (première réponse, DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie »). Après une coupure d'alimentation en vol, le drone redémarre « Allumé, en attente d'un appui » seulement s'il est immobile et à plat ; sinon, échec d'initialisation, définitif jusqu'au débranchement. L'utilisateur avait d'abord répondu « Échec d'initialisation » à l'option sur la tranche, puis confirmé « immobile et à plat » après rappel de la précision de DEC-061 « Redémarrage immobile au sol : allumé mais jamais armé ». Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation » ; DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie »

### DOU-027 — Un signal distinct par information, ou par catégorie ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-005 « Un signal distinct pour chaque information » conduit à 17 signaux, alors qu'en vol l'utilisateur ne perçoit pas toujours les signaux (bruit des moteurs, drone qui s'éloigne). Faut-il un signal par catégorie (prêt, lancé, échec, posé), avec le détail réservé au suivi sur un autre appareil ? Complément de la relecture de porte (critique) : à l'entrée dans l'état verrouillé (DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »), le signal « Allumé » écrase-t-il le signal de la cause (Basculement, Délai de descente dépassé, Échec de stabilisation…) ? Combien de temps le signal de la cause persiste-t-il, pour qu'un utilisateur qui ramasse le drone sache encore pourquoi il est tombé ?
**Réponse :** Chaque état reste distinct et chaque état a un statut sans fil distinct ; les effets visuels et sonores locaux peuvent être regroupés par catégorie pour la praticité, la liste des effets étant à définir en architecture. Le tableau garde 17 événements. Non répondu : combien de temps le signal de la cause persiste à l'entrée dans l'état verrouillé, repris dans DOU-094 « Signal de la cause d'une coupure : combien de temps persiste-t-il après le retour à l'attente ? ». Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie » ; DEC-005 « Un signal distinct pour chaque information »

### DOU-083 — Contenu du statut sans fil d'un armement ou d'un décollage refusé
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-003 « Échec : batterie faible à l'armement »
**Question :** Le signal « Armement refusé » est unique ; la cause est transmise par le statut sans fil, différent selon la cause (DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone »). Quel contenu exact (batterie faible, drone en mouvement, drone pas à plat, combinaison de causes) ? Combien de temps le statut est-il conservé ? Un décollage de réglage refusé pour batterie insuffisante (DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre ») donne-t-il le même signal et le même statut ? Sans appareil de suivi, l'utilisateur ne connaît pas la cause (risque accepté avec DEC-032 « Vol libre : le drone vole sans appareil de suivi »). Complément du 2026-10-28 : le signal est renommé « Refus » (DEC-091 « Un seul signal Refus pour tout refus, armement ou mode réglage ») et vaut aussi pour le mode réglage refusé au 3e appui validé (DEC-090 « Troisième appui validé sur un drone non immobile ou pas à plat : mode réglage refusé avec le signal Refus ») ; le statut doit donc dire aussi si la cause est un mode réglage refusé, et un bouton maintenu (DEC-088 « Bouton coincé ou maintenu en permanence au démarrage : statut sans fil seulement, aucun signal local »).
**Réponse :** Le statut sans fil donne la cause précise du refus (batterie faible, drone en mouvement, drone pas à plat, bouton maintenu au démarrage, etc.) pour l'armement, le mode réglage et le décollage de réglage refusés ; la liste exacte des causes est à fixer en architecture. Non répondu : le signal local du décollage de réglage refusé et la durée de conservation du statut, repris dans DOU-092 « Décollage de réglage refusé : quel signal local, et combien de temps le statut de refus est-il conservé ? ». Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-101 « Statut sans fil d'un refus : cause précise, liste exacte à fixer en architecture »

### DOU-021 — Que se passe-t-il pour un lancer hors plage ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-002 « Échec : stationnaire non atteint dans le délai »
**Question :** Lancer trop bas, trop faible, trop fort ou sous un plafond bas : le drone le distingue-t-il d'un défaut du drone, et quel signal l'utilisateur reçoit-il (le même que l'échec de stabilisation ?) ? Voir DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol ». Que fait le drone s'il ne peut pas évaluer sa hauteur (sol non réfléchissant, vitre, escalier) ?
Complément du 2026-10-28 (fusion du point « perte de la mesure de hauteur par l'environnement », vérifié : aucun autre doute ne le couvre) : la perte de la mesure de hauteur vaut aussi en stationnaire et à l'atterrissage, pas seulement au lancer. Sans hauteur mesurée au-dessus de la hauteur minimale, le stationnaire n'est jamais déclaré (DEC-049 « Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale ») : échec de stabilisation et chute au-dessus d'un sol non réfléchissant ou d'une vitre. À l'atterrissage, le passage sous 2 à 3 cm n'est pas détecté (DEC-022 « Moteurs coupés à moins de 2 à 3 cm du sol »), d'où un signal « Délai de descente dépassé » après 15 s (DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs » ; DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé »), et au-dessus d'un escalier la hauteur réelle est plus grande que celle mesurée. Ces cas relèvent-ils de l'environnement d'emploi (limites d'emploi : DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? ») ou du comportement du drone, et sont-ils couverts par DEC-060 « Défaillance d'un capteur ou d'un moteur en vol : hors périmètre » ? Voir aussi DEC-019 « Hauteur au-dessus du sol mesurée en vol ».
**Réponse :** Un lancer hors plage ou une hauteur impossible à mesurer (sol non réfléchissant, vitre, escalier) donne un échec de stabilisation : même signal « Échec de stabilisation » et même coupure que dans SCN-002 « Échec : stationnaire non atteint dans le délai » ; pas de signal ni de comportement propre ; limite d'emploi à documenter (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-109 « Lancer hors plage ou hauteur non mesurable : échec de stabilisation, limite d'emploi »

### DOU-036 — Après quel délai le lien sans fil est-il considéré comme perdu ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** En vol de réglage, le drone atterrit sur place si le lien est perdu. Après combien de temps sans nouvelle de l'appareil de suivi le considère-t-on perdu, pour éviter un atterrissage sur une coupure brève ? À lever avant la porte « exigences ». Complément de la relecture de la porte : sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »), qu'appelle-t-on « le lien sans fil » ? Réception d'un appareil de suivi quelconque à portée ? À fusionner avec la définition du délai.
**Réponse :** Sans objet le 2026-10-28 : en vol de réglage, aucune action particulière n'est prévue si le lien sans fil est perdu ; il n'y a donc plus de délai de perte du lien à définir (DEC-106 « Lien sans fil perdu en vol de réglage : aucune action particulière »). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-106 « Lien sans fil perdu en vol de réglage : aucune action particulière »

### DOU-039 — La batterie est-elle vérifiée à chaque décollage de réglage ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Quel contrôle de batterie et de chauffe entre deux vols de réglage ? Y a-t-il une limite du nombre de vols ? DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » ne couvre que l'armement. Relevé par la relecture critique. Complément de la relecture de la porte : la batterie est-elle aussi vérifiée avant chaque vol de réglage, compte tenu de DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » ?
**Réponse :** La batterie est vérifiée à chaque décollage de réglage (DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre »). Aucune limite du nombre de vols ni contrôle de chauffe entre deux vols de réglage ; risque accepté et documenté dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »). Le seuil de batterie est fixé en architecture avec les autres seuils (DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture »). Source : réponse de l'utilisateur en chat, 2026-10-28. Historique des réponses partielles : Partielle, le doute reste ouvert. 2026-10-28 : la batterie est vérifiée à chaque décollage de réglage, et seulement elle (DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre »). Restent à décider : le seuil de batterie (le même qu'à l'armement ?), la chauffe, la limite éventuelle du nombre de vols, le signal et le statut sans fil envoyé en cas de refus (DOU-083 « Contenu du statut sans fil d'un armement ou d'un décollage refusé »).
**Décision liée :** DEC-108 « Vols de réglage répétés : aucune limite de nombre ni contrôle de chauffe, risque accepté »

### DOU-053 — Vols de réglage : signaux des phases, signal du lien perdu, acquittement des commandes
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Reste après DEC-100 « Issues du vol de réglage : signaux du vol normal réutilisés, signal du lien perdu à définir » : (a) les signaux des phases du vol de réglage (décollage, stabilisation, stationnaire de 3 secondes) sont-ils ceux du vol normal ? (b) quel signal pour le lien perdu, propre ou via le statut sans fil, et après quel délai (DOU-036 « Après quel délai le lien sans fil est-il considéré comme perdu ? ») ? (c) le drone acquitte-t-il les commandes sans fil reçues (Décoller, Arrêt, Modifier, Sauvegarder), et par quel signal ? (d) quelle relation entre l'atterrissage sur lien perdu et le délai de 15 secondes après le décollage (DEC-029 « Vol de réglage : stationnaire de 3 secondes, atterrissage sur place si le lien est perdu »), et ce délai est-il le délai de descente réglable de DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » (depuis : réglable dans ses bornes, DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel ») ? (e) dans quel état et avec quel signal finit le drone après un atterrissage sur lien perdu ?
**Réponse :** (a) Les signaux des phases du vol de réglage sont ceux du vol normal ; (c) l'acquittement des commandes sans fil (Décoller, Arrêt, Modifier, Sauvegarder) se fait par le statut sans fil seulement (état et valeur relue, comme DEC-068 « Seuil hors bornes : refus silencieux, valeur relue sur l'appareil de suivi »), sans signal local supplémentaire ; (b), (d) et (e) sans objet, le lien perdu n'ayant plus d'effet (DEC-106 « Lien sans fil perdu en vol de réglage : aucune action particulière »). Seul reste, reporté dans DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » : dire si le délai de 15 secondes après le décollage est le délai de descente réglable de DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel ». Source : réponse de l'utilisateur en chat, 2026-10-28. Historique des réponses partielles : Partielle, le doute reste ouvert. 2026-10-28 : les issues du vol de réglage (posé, arrêt par le bouton, arrêt sans fil, échec de stabilisation, basculement, délai de 15 s) réutilisent les signaux du vol normal ; le lien perdu a un signal propre ou passe par le statut sans fil, à définir en architecture. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement » et DEC-106 « Lien sans fil perdu en vol de réglage : aucune action particulière »

### DOU-073 — Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-056 « Armement : drone immobile, sans autotest » exige un drone immobile, au sol ou dans la main. Un drone tenu en main n'est jamais strictement immobile : quelle tolérance de mouvement (vitesse, rotation) l'armement accepte-t-il ? Si l'appui de 2 s a lieu sur un drone en mouvement, quel signal et quel comportement (armement refusé comme dans SCN-003 « Échec : batterie faible à l'armement », ou attente de l'immobilité) ? Relevé en alignant les scénarios sur DEC-056 « Armement : drone immobile, sans autotest ». À lever avant la porte « exigences ». Compléments de la relecture critique du 2026-10-28 : dans quel ordre le drone teste-t-il l'immobilité et la batterie (SCN-003 « Échec : batterie faible à l'armement ») ? Si l'appui dépasse 10 s sans armement, y a-t-il un signal de désarmement (SCN-005 « Dégradé : bouton maintenu plus de 10 secondes » ne traite que le drone armé) ? Après un refus, le bouton est-il ignoré jusqu'au relâchement ?
**Réponse :** Si l'appui de 2 s a lieu sur un drone en mouvement, pas à plat ou à batterie faible, tous les tests sont faits à 2 s et le drone donne un seul signal « Refus » ; le statut sans fil liste les causes (DEC-101 « Statut sans fil d'un refus : cause précise, liste exacte à fixer en architecture ») ; l'ordre des tests n'a pas d'importance pour l'utilisateur ; le drone n'attend pas l'immobilité. Levé pour ce qui est répondu. Reste, fusionné dans DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » : la tolérance de mouvement (vitesse, rotation) de « immobile », à fixer en architecture. Source : réponse de l'utilisateur en chat, 2026-10-28. Historique des réponses partielles : Partielle, le doute reste ouvert. 2026-10-28 : si l'armement est refusé (batterie faible, drone en mouvement ou pas à plat), un seul signal « Armement refusé » est donné, la cause étant transmise par le statut sans fil (DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone ») ; le drone n'attend pas l'immobilité. Restent à fixer : la tolérance de mouvement d'un drone tenu en main (vitesse, rotation) et l'ordre des tests. Complément 2026-10-28 : après un refus, le drone revient à l'attente et le bouton est ignoré jusqu'au relâchement (DEC-081 « Bouton encore enfoncé après un refus ou un désarmement : ignoré jusqu'au premier relâchement, puis nouvel appui possible tout de suite »), ce qui répond au bouton après refus et, par conséquence, à l'appui de plus de 10 s sans armement (sans effet ni signal).
**Décision liée :** DEC-110 « Armement refusé à 2 secondes d'appui : tous les tests faits, un seul signal Refus, sans attente de l'immobilité »

### DOU-078 — Initialisation en cours et échec d'initialisation : quelles commandes sans fil sont acceptées ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Reste après DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque » : la table de DEC-043 « Commandes sans fil acceptées selon l'état du drone » n'a pas de ligne pour l'initialisation en cours ni pour l'échec d'initialisation, désormais définitif jusqu'au débranchement (DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie »). Toutes les commandes (Décoller, Arrêt, Modifier, Sauvegarder) y sont-elles ignorées ? Modifier et Sauvegarder y sont-elles acceptées, et l'état est-il visible sur l'appareil de suivi ? Historique : la question de « Sauvegarder » à l'état armé (relevée par la relecture critique du 2026-10-28) est répondue.
**Réponse :** Pendant l'initialisation et après un échec d'initialisation, Modifier et Sauvegarder sont acceptées ; Décoller et Arrêt sont ignorées (commandes de vol). Deux lignes ajoutées à la table de DEC-043 « Commandes sans fil acceptées selon l'état du drone ». Risque accepté, à documenter (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? ») et à traiter en architecture : écrire des réglages sur un drone non initialisé. Source : réponse de l'utilisateur en chat, 2026-10-28. Historique des réponses partielles : Partielle, le doute reste ouvert. 2026-10-28 : la commande « Sauvegarder » reste acceptée à l'état « Armé, avant le lancer » ; risque accepté, une écriture en mémoire non volatile peut retarder le lancer, à traiter en architecture et à documenter comme limite d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »). Reste non répondu : l'initialisation en cours et l'échec d'initialisation. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées »

### DOU-092 — Décollage de réglage refusé : quel signal local, et combien de temps le statut de refus est-il conservé ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** DEC-101 « Statut sans fil d'un refus : cause précise, liste exacte à fixer en architecture » donne la cause précise du refus dans le statut sans fil pour l'armement, le mode réglage et le décollage de réglage. Mais le signal local d'un décollage de réglage refusé (batterie insuffisante, DEC-074 « Décollage en mode réglage : la batterie est vérifiée, rien d'autre ») n'a pas été répondu : le signal « Refus » de DEC-091 « Un seul signal Refus pour tout refus, armement ou mode réglage » ne cite que l'armement et le mode réglage. Faut-il le même signal « Refus », un autre, ou aucun signal local ? Combien de temps le statut de refus est-il conservé sur le sans fil ? Posé le 2026-10-28 : lacune de la réponse sur DOU-083 « Contenu du statut sans fil d'un armement ou d'un décollage refusé », laissée dans le diagramme c comme « Décollage refusé » sans signal local.
**Réponse :** Un décollage de réglage refusé (batterie insuffisante) donne le même signal « Refus » (DEC-091 « Un seul signal Refus pour tout refus, armement ou mode réglage »). Le statut de refus reste lisible sur le sans fil jusqu'à la commande suivante ; la durée exacte est à fixer en architecture (DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture »). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-102 « Décollage de réglage refusé : signal Refus, statut de refus lisible jusqu'à la commande suivante »

### DOU-093 — Dépassement de la durée maximale de la phase Lancé : que fait le drone ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale » fixe une durée maximale de la phase « Lancé », de l'ordre de quelques centaines de millisecondes. Que se passe-t-il si elle est dépassée sans démarrage des moteurs : le chien de garde coupe et redémarre le drone comme pour un logiciel bloqué (DEC-065 « Logiciel bloqué en vol : coupure des moteurs par un chien de garde »), ou le drone revient à l'attente, et avec quel signal ? Posé le 2026-10-28 : la réponse sur DOU-075 « Le chien de garde couvre-t-il la phase Lancé, et cette phase a-t-elle une durée maximale ? » ne le dit pas.
**Réponse :** Si la phase « Lancé » dépasse sa durée maximale sans démarrage des moteurs, le chien de garde coupe et redémarre le drone comme pour un logiciel bloqué (DEC-065 « Logiciel bloqué en vol : coupure des moteurs par un chien de garde »), puis le redémarrage suit DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation » ; aucun nouvel état ni signal. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-103 « Phase Lancé trop longue : coupure et redémarrage par le chien de garde, sans nouvel état ni signal »

### DOU-094 — Signal de la cause d'une coupure : combien de temps persiste-t-il après le retour à l'attente ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Reprise du complément de la relecture de porte (critique) à DOU-027 « Un signal distinct par information, ou par catégorie ? », resté sans réponse. À l'entrée dans l'état verrouillé, qui est le même que « Allumé, en attente d'un appui » (DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui »), l'effet local de la cause (Basculement, Délai de descente dépassé, Échec de stabilisation, arrêt) persiste-t-il, combien de temps, ou le signal « Allumé » l'écrase-t-il ? Un utilisateur qui ramasse le drone doit pouvoir savoir pourquoi il est tombé. Le statut sans fil distinct par état (DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie ») conserve la cause sur l'appareil de suivi, pas en local.
**Réponse :** Après une coupure en vol, le signal local de la cause ne persiste pas : « Allumé » prend le relais tout de suite à l'entrée dans l'état verrouillé ; la cause est conservée dans le statut sans fil distinct (DEC-099 « Un statut sans fil distinct par état, effets locaux regroupables par catégorie »). La tension avec DEC-033 « Signal Arrêt sans fil distinct du signal Arrêt par le bouton » et DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé » (signaux distincts) est nommée sans être tranchée (DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil »). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil »

### DOU-048 — Batterie : charge, remplacement, drone laissé allumé
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Question :** Comment la batterie est-elle chargée, remplacée, rangée ? Que fait un drone « allumé, en attente d'un appui » laissé branché des heures ? Y a-t-il un signal de batterie faible hors armement ? Scénario manquant proposé : maintenance de la batterie. Relevé par la relecture critique. Note de priorité du 2026-10-28 (relectures de porte) : priorité élevée proposée, car il manque un scénario de la batterie (charge, remplacement, stockage, drone laissé allumé) et que la sécurité en dépend ; non bloquant pour la porte « scénarios » tel que l'utilisateur l'a demandé, à traiter avant la porte « exigences ». Le niveau de priorité et le moment sont à fixer par l'utilisateur.
**Réponse :** Hors périmètre des scénarios, traitée comme limite d'emploi (notice) : le drone ne gère rien de la batterie (charge, remplacement, stockage, drone laissé allumé) ; pas de scénario dédié à la batterie. Limites d'emploi reportées dans DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? ». Aucun besoin ne pourra porter sur la gestion de la batterie. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter »

### DOU-049 — Programmation : cas d'échec, hélices démontées, essai des moteurs avant le premier vol
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-008 « Mise en service : programmation du drone »
**Question :** Que se passe-t-il si la programmation échoue ? La batterie est-elle branchée pendant la programmation, les hélices démontées (consigne de sécurité) ? Faut-il un essai des moteurs avant le premier vol ? Y a-t-il une reprogrammation ou un contrôle de version ? Reprend la partie oubliée de DOU-031 « Quelles opérations suivent la programmation à la mise en service ? ». Relevé par la relecture critique. Note de priorité du 2026-10-28 (relectures de porte) : même priorité que DOU-048 « Batterie : charge, remplacement, drone laissé allumé » pour l'essai des moteurs avant le premier vol (hélices démontées ou non, sens de rotation), à traiter avant la porte « exigences » ; le niveau de priorité et le moment sont à fixer par l'utilisateur.
**Réponse :** Hors périmètre des scénarios, traitée comme limite d'emploi (notice) : le drone ne gère aucun cas d'échec de la programmation (programmation interrompue, hélices démontées, essai des moteurs avant le premier vol) ; aucun cas n'est ajouté à SCN-008 « Mise en service : programmation du drone ». Reprogrammation et contrôle de version : non nommés dans la réponse, lecture de l'architecte (hors périmètre), à confirmer à la porte « scénarios ». Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter »

### DOU-095 — Commande Sauvegarder à l'état armé : écriture en mémoire non volatile et durée maximale de la phase Lancé
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque » accepte la commande Sauvegarder à l'état armé. Une écriture en mémoire non volatile peut-elle dépasser la durée maximale de la phase « Lancé » (DEC-096 « Chien de garde sur tout état où les moteurs peuvent être alimentés, phase Lancé de durée maximale ») et provoquer, par le chien de garde, une coupure puis un redémarrage au moment du lancer (DEC-103 « Phase Lancé trop longue : coupure et redémarrage par le chien de garde, sans nouvel état ni signal ») ? Un appareil de suivi tiers à portée peut déclencher cette commande (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »). Ce cas est-il accepté tel quel ? Complète DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite » (retard du lancer), qui ne traite pas le chien de garde.
**Réponse :** La commande « Sauvegarder » est ignorée à l'état « Armé, avant le lancer » : plus d'écriture en mémoire non volatile pendant l'armement, donc plus de dépassement de la phase « Lancé » par une écriture déclenchée à l'état armé. L'écriture commencée avant l'armement et encore en cours au lancer est reportée dans DOU-059 « Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite ». Source : réponse de l'utilisateur en chat, 2026-10-28 (elle avait d'abord répondu « acceptée comme aujourd'hui », DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque », puis a changé sa réponse après rappel de l'interaction avec le chien de garde).
**Décision liée :** DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer »

### DOU-096 — Durée minimale perceptible du signal de cause d'une coupure en vol
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** Après une coupure en vol, le signal local de la cause (signaux 13 à 17 : Échec de stabilisation, Arrêt par le bouton, Basculement, Arrêt sans fil, Délai de descente dépassé) est remplacé tout de suite par « Allumé » (DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil »). Sans durée minimale perceptible, l'information de l'utilisateur sans appareil de suivi (DEC-005 « Un signal distinct pour chaque information », DEC-033 « Signal Arrêt sans fil distinct du signal Arrêt par le bouton », DEC-046 « Délai de descente dépassé : signal distinct, moteurs coupés, drone verrouillé ») n'est pas vérifiable en test. Faut-il une durée minimale perceptible, et sous quelle forme (exigence, valeur) ? Vérification faite dans l'archive : DOU-094 « Signal de la cause d'une coupure : combien de temps persiste-t-il après le retour à l'attente ? » est levé par DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil » (« Allumé » prend le relais tout de suite) et ne peut pas être rouvert ; la valeur de la durée est déjà listée dans DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture ». Ce doute porte sur le principe d'une durée minimale vérifiable, pas sur sa valeur ; fusion avec DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » non faite, à confirmer.
**Réponse :** Aucune durée minimale perceptible : « Allumé » prend le relais tout de suite après une coupure en vol, la cause ne se lit que sur le statut sans fil ; DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil » est confirmée telle quelle. Risque accepté : un utilisateur sans appareil de suivi n'est pas informé de la cause (limite d'emploi, DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »). La durée perceptible n'est plus à fixer dans DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture ». Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté »
