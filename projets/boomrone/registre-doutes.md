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

### DOU-050 — Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Le critère de DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » est-il mesurable et réaliste ? Lancé à l'envers depuis 1,5 m, une chute libre dure 0,55 s ; le drone peut toucher le sol avant la fin de la stabilisation, hélices tournantes. À lever avant la porte « exigences », avec DOU-030 « Les valeurs provisoires sont-elles à confirmer avant les exigences ? ». Relevé par la relecture critique. Complément de la relecture de porte (critique) : calcul pour un lancer à l'envers depuis 1,5 m à 0,5 m/s vers le haut : le drone touche le sol en 0,61 s environ ; les moteurs ne démarrent qu'à 0,2 s (DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs ») ; il reste donc environ 0,4 s pour se retourner de 180° et freiner une chute de 1,5 à 5 m/s, avec un capteur de hauteur ToF aveugle tant que le drone est retourné. Le bas de la plage de DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » est très probablement infaisable. Proposition à soumettre à l'utilisateur : écrire dans SCN-001 « Vol nominal : de la batterie au posé » que les limites de la plage sont à confirmer par essais. Depuis : DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences » — la phrase est écrite dans SCN-001 « Vol nominal : de la batterie au posé » : les valeurs, y compris les limites de la plage, sont à confirmer avant la porte « exigences » ; le présent doute reste ouvert pour l'analyse. Le capteur ToF n'est plus qu'une proposition d'architecture (DEC-053 « Solutions techniques déplacées en propositions d'architecture, seule l'intention reste décidée ») : le risque d'une mesure de hauteur aveugle drone retourné vaut pour tout capteur orienté vers le bas. Complément du 2026-10-28 : échéance « avant les besoins » (et non seulement avant les exigences) : on revoit la plage de lancer (hauteur minimale, vitesse) avec une analyse de faisabilité avant de rédiger les besoins ; SCN-001 « Vol nominal : de la batterie au posé » et SCN-002 « Échec : stationnaire non atteint dans le délai » gardent les valeurs de la plage de lancer comme provisoires (DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » ; DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences »). Non bloquant pour la porte « scénarios », mais la phase « besoins » ne s'ouvre pas tant que ce doute est ouvert. Complément du 2026-10-28 (rapport de la 4e relecture de porte) : la faisabilité de la plage de lancer dépend aussi de DOU-010 « Quelle rotation au lancer le drone doit-il rattraper ? » (rotation à rattraper) et de DOU-035 « Quelle hauteur de stationnaire vise-t-on ? » (hauteur de stationnaire), ouverts avec une échéance « avant les exigences » ; le jalon « avant les besoins » de DEC-122 « Jalon avant les besoins : promesse de l'architecte, sans modification de l'outil de porte » n'est pas modifié, mais la plage de lancer ne peut pas être confirmée tant que ces deux valeurs sont inconnues. Complément du 2026-10-29 (5e relecture) : l'échéance « avant les besoins » est abandonnée, validation par essais sur prototype (DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée » et DEC-138 « Tolérance d'immobile et part de DOU-058 liée à la faisabilité : jalon déplacé aux essais »).
**Réponse :** Phase exigences, 2026-10-29 : valeur provisoire écrite dans REQ-006 « Stabilisation après le lancer » (stationnaire en 2,0 s, 90 % de 20 lancers) ; reste ouvert jusqu'aux essais sur prototype, non bloquant. Note du 2026-10-29 (DEC-216 « Fusions de simplicité et sous-tension en échec d'initialisation : retouches finales de la porte exigences ») : REQ-006 « Stabilisation après le lancer » ne porte plus la convergence vers la hauteur visée ; elle relève de REQ-008 « Tenue du vol stationnaire » (3e à 10e seconde), qui laisse environ 1 s après les 2,0 s pour passer de la hauteur du lancer (1,5 m au moins) à la fenêtre de 0,8 à 1,2 m : à vérifier aux essais avec ce doute.
**Décision liée :** DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée » (2026-10-28 : le doute reste ouvert jusqu'aux essais sur prototype, il n'empêche plus la phase « besoins » ; modifie DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » et DEC-122 « Jalon avant les besoins : promesse de l'architecte, sans modification de l'outil de porte »)

### DOU-116 — Échéance et circularité du report aux essais, comportement de SCN-002 sur la partie infaisable de la plage
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé » et SCN-002 « Échec : stationnaire non atteint dans le délai »
**Question :** DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée » et DEC-138 « Tolérance d'immobile et part de DOU-058 liée à la faisabilité : jalon déplacé aux essais » reportent la faisabilité aux essais sur prototype, qui n'existe qu'après l'architecture, alors que le choix des capteurs, des moteurs et de la mesure de vitesse horizontale (DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m ») conditionne cette architecture. Quelle échéance borne l'essai (avant ou pendant l'architecture) ? Sur la partie de la plage où le sol est atteint en environ 0,4 s, SCN-002 « Échec : stationnaire non atteint dans le délai » devient le comportement normal : cela doit-il apparaître dans un scénario ou un risque accepté ? Ouvert le 2026-10-29 (5e relecture de porte, `critique`).
**Réponse :** Phase exigences, 2026-10-29 : REQ-006 « Stabilisation après le lancer » fixe un taux de réussite de 90 % et prévoit la reprise de la plage si l'essai échoue ; reste ouvert jusqu'aux essais, non bloquant.
**Décision liée :**

### DOU-131 — Valeurs provisoires des exigences, à valider aux essais sur prototype
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** « Exigences système » — `projets/boomrone/02-exigences.md`, annexe B
**Question :** Les valeurs chiffrées posées par l'architecte à la phase « exigences » sont provisoires : bouton (anti-rebond, garde, délais), critère de stationnaire, tenue en altitude et dérive, basculement, seuils de batterie et marge de vol, délais de coupure, débits du sans fil, durée d'initialisation, taille et pièce d'essai. Chacune tient-elle aux essais sur prototype ? Échéance : essais sur prototype ; si une valeur ne tient pas, l'exigence concernée est reprise par décision.
**Réponse :** Valeurs provisoires écrites dans REQ-001 « Anti-rebond du bouton » à REQ-034 « Page de consignes d'emploi » et dans l'annexe B de « Exigences système » ; aucune n'est bloquante pour la porte « exigences ».
**Décision liée :** DEC-182 « Valeurs du bouton : 1 s, 2 s, 10 s, anti-rebond, garde, délai des moteurs » ; DEC-183 « Valeurs de départ : immobile, à plat, batterie à l'armement » ; DEC-184 « Valeurs du vol : lancer, stationnaire, hauteur, dérive, atterrissage » ; DEC-185 « Valeurs de coupure : basculement, pas de limite de dérive ni d'altitude » ; DEC-186 « Valeurs de batterie : seuils par élément, confirmation, vol complet » ; DEC-187 « Valeurs du cadre d'emploi : poche, protège-hélices, pièce d'essai »

### DOU-133 — Forme des dix effets locaux : lumière, son, distinction mesurable
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** REQ-018 « Effets locaux par situation » et REQ-019 « Perceptibilité et distinction des effets »
**Question :** Quelle forme (couleur, rythme, tonalité) donne dix effets que l'observateur distingue sans erreur à 1 m, y compris la lumière seule moteurs en marche ? Échéance : architecture, vérifiée aux essais (TS-014 « Perceptibilité et distinction des effets »).
**Réponse :** Phase architecture, 2026-10-29 : forme proposée (voyant RGB couleur et rythme, buzzer actif nombre et durée des bips ; table dans « Architecture », DEC-228 « Effets locaux : table des dix effets, buzzer actif à un seul timbre ») ; reste ouvert jusqu'à la vérification de la distinction à TS-014 « Perceptibilité et distinction des effets » et TI-019 « Effets locaux sur les sorties ».
**Décision liée :** DEC-176 « Simplification n°3 adoptée : dix effets locaux au lieu de dix-sept signaux »

### DOU-135 — Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** REQ-031 « Drone de poche », REQ-013 « Marge de batterie pour un vol complet », REQ-006 « Stabilisation après le lancer » et REQ-044 « Assemblage à la main »
**Question :** Un drone de 100 g au plus, assemblé à la main, avec la batterie réellement choisie et un capteur de hauteur, fournit-il la poussée d'un stationnaire en 2,0 s depuis 1,5 m, tient-il un vol complet de 30 s sans passer sous 3,3 V par élément, et reste-t-il un drone de poche ? Les exigences sont écrites sans choix de composants ; la faisabilité d'ensemble dépend de l'architecture. Ouvert le 2026-10-29 (relecture de la porte « exigences », `critique`). Échéance : architecture (choix des moteurs, de la batterie et du capteur), puis essais sur prototype ; si l'ensemble n'est pas faisable, l'exigence concernée est reprise par décision.
**Réponse :** Phase architecture, 2026-10-29 : bilan chiffré dans « Architecture » (DEC-229 « Faisabilité conjointe : bilan, verdict marginal, mesures au banc avant la commande de la carte ») : masse 65 g (au pire 76,5 g) pour 100 g, hélices de 45 mm (98 × 98 mm), poussée/poids 1,35 (0,8 à 2,2), crête 9,5 A ; chute de tension jusqu'à 3,17 V avec 3,7 V à l'armement, donc marginale à infaisable en tension. Mesures au banc avant la commande de la carte ; repli proposé : armement à 3,9 V et sous-tension à 3,0 V sous charge, ou brushless 1S. Reste ouvert.
**Décision liée :** DEC-209 « Batterie de référence choisie à l'architecture, faisabilité conjointe en doute » ; DEC-229 « Faisabilité conjointe : bilan, verdict marginal, mesures au banc avant la commande de la carte »

### DOU-101 — Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Extrait de DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » pour lui donner une échéance : avant la phase « besoins ». L'armement exige un drone immobile et à plat, au sol ou dans la main (DEC-056 « Armement : drone immobile, sans autotest »), tous les tests étant faits à 2 s d'appui (DEC-110 « Armement refusé à 2 secondes d'appui : tous les tests faits, un seul signal Refus, sans attente de l'immobilité »). Un drone tenu en main n'est jamais parfaitement immobile : quelle tolérance de mouvement rend le cas nominal (armement dans la main, SCN-001 « Vol nominal : de la batterie au posé ») réalisable sans refus répétés ? Le critère doit être fixé avant les besoins, car il détermine ce qu'un besoin d'armement peut exiger. Complément du 2026-10-28 : l'échéance « avant les besoins » est confirmée et liée au jalon DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir ». Complément du 2026-10-28 (rapport de la 4e relecture de porte) : la faisabilité du cas nominal dépend aussi de DOU-010 « Quelle rotation au lancer le drone doit-il rattraper ? » (rotation à rattraper) et de DOU-035 « Quelle hauteur de stationnaire vise-t-on ? » (hauteur de stationnaire), ouverts avec une échéance « avant les exigences » ; le jalon de DEC-122 « Jalon avant les besoins : promesse de l'architecte, sans modification de l'outil de porte » n'est pas modifié. Complément du 2026-10-29 (5e relecture) : l'échéance « avant les besoins » est abandonnée, validation par essais sur prototype (DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée » et DEC-138 « Tolérance d'immobile et part de DOU-058 liée à la faisabilité : jalon déplacé aux essais »).
**Réponse :** Phase exigences, 2026-10-29 : tolérance provisoire écrite dans REQ-003 « Conditions de départ du drone » (30 °/s, variation d'accélération de ±0,5 m/s² sur 0,5 s ; mesure relative depuis la relecture de porte, DEC-206 « Conditions de départ : immobilité mesurée en relatif, cas Décoller séparé »). Le calibrage de l'accéléromètre (biais, échelle) reste à traiter en architecture ; reste ouvert jusqu'aux essais sur prototype, non bloquant.
**Décision liée :** DEC-138 « Tolérance d'immobile et part de DOU-058 liée à la faisabilité : jalon déplacé aux essais » (2026-10-28 : le doute reste ouvert jusqu'aux essais sur prototype, il n'empêche plus la phase « besoins »)

### DOU-137 — Latence de bout en bout de l'arrêt sans fil sur Bluetooth
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** REQ-022 « Arrêt sans fil » et ARC-025 « Protocole et service du statut sans fil »
**Question :** la commande Arrêt est exécutée 2 ms après la fin de la trame côté drone, mais la latence Bluetooth (intervalle de connexion du module et de l'ordinateur, retransmission) peut dépasser les 200 ms de {REQ-022 « Arrêt sans fil »}. Où commencent les 200 ms (envoi ou fin de trame) ? Ouvert le 2026-10-29 (architecture logicielle).
**Réponse :** mesure de bout en bout à {TS-016 « Arrêt sans fil »} et à {TI-010 « Liaison Bluetooth à basse consommation »} ; si la valeur de 200 ms ne tient pas, l'architecte proposera de préciser le point de départ ou de relever la valeur de {REQ-022 « Arrêt sans fil »}. Échéance : essais sur prototype, non bloquant.
**Décision liée :** {DEC-232 « Nouveaux doutes d'architecture ouverts »}

### DOU-138 — Interprétations de l'architecture logicielle : priorité de l'initialisation, causes de refus, sauvegarde et statut
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** REQ-017 « Initialisation en 3 secondes », REQ-027 « Sauvegarde et chargement des réglages », REQ-038 « Causes et paramètres dans le statut sans fil » et ARC-023 « Initialisation et échec d'initialisation »
**Question :** l'architecture a tranché sans que les exigences le disent : (a) à la fin de l'initialisation, l'échec prime sur le mode réglage, qui prime sur Allumé ({REQ-017 « Initialisation en 3 secondes »}, {REQ-024 « Entrée en mode réglage par le bouton »}) ; (b) un refus d'armement porte une seule cause, dans l'ordre batterie, mouvement, pas à plat ({REQ-038 « Causes et paramètres dans le statut sans fil »}) ; (c) Sauvegarder est ignorée sous 3,5 V ({REQ-027 « Sauvegarde et chargement des réglages »}) ; (d) aucun statut radio n'est émis pendant l'initialisation ({REQ-020 « Statut sans fil »}) ; (e) le retour au sol en mode réglage donne directement l'effet Mode réglage, sans passer par l'effet Posé visible ; (f) le critère de stationnaire exige 10 cycles consécutifs ({REQ-007 « Critère de vol stationnaire »}) ; (g) une norme d'accélération hors de 0,8 à 1,2 g vaut « pas à plat » à l'initialisation (critère absolu ajouté à {REQ-017 « Initialisation en 3 secondes »}) ; (h) un reset du chien de garde en mouvement mène à l'échec d'initialisation définitif plutôt qu'à Allumé ({REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage »}, {REQ-036 « Coupure sur phase Lancé trop longue »}) ; (i) le mode réglage n'est accordé qu'à une mise sous tension, pas après un reset ({REQ-024 « Entrée en mode réglage par le bouton »}). Ouvert le 2026-10-29.
**Réponse :** interprétations consignées dans {DEC-226 « Initialisation : priorités, mode réglage après mise sous tension, causes conservées après reset »} ; à relire et à reprendre dans les exigences à la prochaine révision si l'utilisateur n'est pas d'accord. Non bloquant.
**Décision liée :** {DEC-226 « Initialisation : priorités, mode réglage après mise sous tension, causes conservées après reset »}

### DOU-139 — Capteurs de hauteur et de flux : hauteur de montage et sols sans texture
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** REQ-009 « Atterrissage doux », REQ-008 « Tenue du vol stationnaire » et ARC-004 « Capteur de hauteur à temps de vol »
**Question :** le capteur de hauteur n'est fiable qu'à partir de 40 mm alors que la coupure se fait à 2 à 3 cm du sol ({REQ-009 « Atterrissage doux »}) : le montage à environ 20 mm au-dessus du plan de contact, avec une coupure à une lecture brute d'environ 45 mm, suffit-il ? Le flux optique ne mesure pas la vitesse sur un sol uni ou sombre : la dérive de {REQ-008 « Tenue du vol stationnaire »} est-elle alors tenue ? Ouvert le 2026-10-29.
**Réponse :** mesures à {TI-003 « Hauteur du capteur à temps de vol et position de montage »} et {TI-004 « Flux optique et vitesse horizontale »} (hauteur = lecture moins 20 mm, coupure à une lecture brute d'environ 45 mm) ; à défaut, la coupure à 15 s reste le secours et la limite est à consigner. Échéance : essais sur prototype, non bloquant.
**Décision liée :** {DEC-232 « Nouveaux doutes d'architecture ouverts »}

### DOU-140 — Défaut de capteur en vol : cause et effet rattachés à l'échec de stabilisation
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** REQ-011 « Coupures automatiques en vol », REQ-038 « Causes et paramètres dans le statut sans fil » et ARC-016 « Pilotes des capteurs et des sorties »
**Question :** que fait le drone si la centrale inertielle ou le capteur de hauteur cesse de répondre moteurs en marche (bus bloqué, capteur débranché) ? Aucune cause de {REQ-038 « Causes et paramètres dans le statut sans fil »} ne le couvre. Ouvert le 2026-10-29 (relecture de porte `critique`).
**Réponse :** par décision provisoire de l'architecte, la coupure est rattachée à la cause « échec de stabilisation » (état 13) ; à confirmer à la prochaine révision des exigences. Non bloquant.
**Décision liée :** {DEC-233 « Relecture de porte architecture : corrections décidées par délégation »}

### DOU-142 — Fuite d'entrée de l'ADC et marge de ±50 mV de la mesure de tension
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-009 « Alimentation de la logique et mesure de la tension » et REQ-003 « Conditions de départ du drone »
**Question :** la fuite d'entrée de l'ADC du STM32G431 n'est pas relevée ; avec une source d'environ 60 kΩ, 100 nA de fuite donnent 6 mV à la broche, soit environ 10 mV sur la batterie. Le budget estimé (pont à 0,1 % 3 mV, VREFINT 6 mV, décalage 5 mV, fuite 10 mV, soit environ ±25 mV) tient-il dans les ±50 mV ?
**Réponse :** (aucune) ; à relever dans la fiche DS12589 et à mesurer à TI-008 « Batterie, connecteur, chute de tension et mesure de tension » ; étalonnage de gain au multimètre en repli. Non bloquant. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-281 « Puissance et alimentation : AO3400A, MCP1700, source de l'ADC et étalonnage ») : DS12589 limite RAIN à 50 kΩ (tableau 60) et à 39 kΩ à 640,5 cycles à 60 MHz sur voie rapide (tableau 61) ; le pont fait 60 kΩ ; le pont est conservé et le condensateur de 100 nF sur PA0 est obligatoire (CADC au plus 5 pF : écart de partage de charge au plus 0,13 mV) ; la fuite d'entrée de l'ADC n'est toujours pas relevée : le doute reste ouvert, la mesure de TI-008 « Batterie, connecteur, chute de tension et mesure de tension » reste la preuve.
**Décision liée :** {DEC-242 « Alimentation de la logique à 130 mA et masse recalculée à 62 g »}

### DOU-143 — Tensions d'alimentation acceptées par les capteurs et le module à 3,0 V
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-009 « Alimentation de la logique et mesure de la tension », ARC-004 « Capteur de hauteur à temps de vol », ARC-005 « Capteur de flux optique » et ARC-012 « Module radio Bluetooth à basse consommation »
**Question :** le rail descend à environ 2,9 V (2,82 V avec une batterie à 3,0 V). Le capteur de hauteur (2,6 V minimum), le module E104-BT02 (2,5 V minimum), la centrale (1,71 V) conviennent d'après le catalogue ; le flux optique (puce PMW3901MB posée par JLCPCB) n'est plus sur le rail de 3,0 V pour VDD : la fiche PixArt, lue le 2026-10-29, donne VDD de 1,8 à 2,1 V (alimenté en 2,0 V par un régulateur dédié, DEC-247 « Flux optique : alimentation en 2,0 V par un régulateur dédié, signaux en 3,0 V ») et VDDIO de 1,8 à 3,6 V (au rail de 3,0 V), tolérée. Les autres plages viennent du catalogue, pas des fiches.
**Réponse :** (aucune) ; relever les plages dans les fiches avant la commande de la carte. Non bloquant.
**Décision liée :** {DEC-242 « Alimentation de la logique à 130 mA et masse recalculée à 62 g »} ; {DEC-247 « Flux optique : alimentation en 2,0 V par un régulateur dédié, signaux en 3,0 V »}

### DOU-144 — Courant du buzzer, diode et tensions directes du voyant RGB
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-011 « Voyant RGB et avertisseur sonore »
**Question :** le buzzer actif tire environ 30 mA à 3,3 V (plus sous 4,2 V, non vérifié) et le niveau sonore à 1 m (environ 60 dB estimé) est inférieur à l'ancienne estimation de 65 dB ; une diode de précaution est prévue. Les tensions directes du voyant (rouge 2,4 V, vert et bleu 3,4 V selon le catalogue) sont à confirmer : le vert et le bleu peuvent s'éteindre vers 3,3 à 3,4 V de batterie.
**Réponse :** (aucune) ; mesure à TI-009 « Bouton, voyant RGB et avertisseur » et TS-014 « Perceptibilité et distinction des effets ». Non bloquant.
**Décision liée :** {DEC-235 « Catalogue JLCPCB/LCSC vérifié : composants retenus »}

### DOU-145 — Vol entre la dernière mesure de hauteur et la coupure à 200 ms
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-004 « Capteur de hauteur à temps de vol », ARC-016 « Pilotes des capteurs et des sorties » et REQ-011 « Coupures automatiques en vol »
**Question :** que fait la commande de hauteur entre la dernière mesure valide et la coupure à 200 ms ? Tenir la dernière poussée peut faire monter ou descendre le drone pendant 0,2 s.
**Réponse :** (aucune) ; décision provisoire : la hauteur est extrapolée par l'observateur de ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse » (accélération verticale) sans recalage ; à confirmer en conception détaillée et à TI-028 « Pilote du capteur de hauteur : durée d'appel, bus bloqué, capteur muet ». Non bloquant.
**Décision liée :** {DEC-239 « Capteur de hauteur : pilote non bloquant, reprise, échec d'initialisation, mesure horodatée »}

### DOU-146 — Broches d'état du module Bluetooth et de mouvement du capteur de flux
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-012 « Module radio Bluetooth à basse consommation » et ARC-005 « Capteur de flux optique »
**Question :** la broche d'état (connexion) du module Bluetooth et la broche de mouvement (MOTION) du capteur de flux ne sont pas câblées au microcontrôleur : choix de simplicité (le statut radio est lu par trames, le flux par interrogation). À reconsidérer si l'essai montre un besoin.
**Réponse :** (aucune) ; décision provisoire : non câblées, plots de test seulement. Non bloquant. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-277 « Module radio : 19200 bauds, réveil par PA1, broches du module et boîtier ») : la fiche d'Ebyte montre que WKP (P06, broche 9) n'est pas optionnel : le module est en veille par défaut et l'UART ne reçoit plus en veille ; WKP est relié à PA1 ; MOD laissée libre, RESET_H à la masse, STA non câblée ; la broche MOTION du PMW3901MB reste non câblée, la fiche de la puce étant absente (DOU-185 « Fiche du capteur de flux PMW3901MB absente du dossier des fiches »). Ouvert : niveau actif de WKP à confirmer (DOU-195 « Module E104-BT02 : niveau de WKP, état à la mise sous tension et mot de passe aérien »). Complément du 2026-10-30 : niveau confirmé par la fiche anglaise (bas = éveillé) ; STA reste non câblée ; WKP est relié directement à PA1 (DEC-286 « WKP : PA1 directe, emplacements de 0 Ω supprimés », qui remplace DEC-285 « WKP : PA1 conservée, résistance série de 0 Ω et emplacement de 0 Ω vers la masse non posé » : les emplacements de 0 ohm sont supprimés), sans effet sur ce doute.
**Décision liée :** {DEC-240 « Brochage, timers, voyant et bouton »}

### DOU-147 — Compatibilité de l'empreinte avec le STM32G474
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-002 « Microcontrôleur et programmation par liaison SWD »
**Question :** le STM32G474CBT6 (LQFP-48, C730123, en stock) peut servir de repli : les deux tableaux de brochage doivent être comparés (PA11 et PA12 sont l'USB sur le G474, non utilisées).
**Réponse :** (aucune) ; comparaison à faire dans les fiches avant le routage. Non bloquant.
**Décision liée :** {DEC-240 « Brochage, timers, voyant et bouton »}

### DOU-149 — Valeurs de registres du VL53L1X à vérifier dans la bibliothèque ST (ULD)
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-004 « Capteur de hauteur à temps de vol »
**Question :** les registres de lecture du résultat, d'acquittement de l'interruption, de polarité de GPIO1 et de budget de mesure sont donnés de mémoire dans les notes d'architecture.
**Réponse :** (aucune) ; à vérifier dans l'ULD de ST et la fiche DS12093 en conception détaillée. Non bloquant. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-280 « Capteurs : VL53L1X sans broche IOVDD, LSM6DSO et délai de mise en route ») : la fiche déposée est DS12385 Rev 8 (et non DS12093) ; elle ne donne pas les registres (renvoi à la note UM2356), seuls l'identifiant 0x010F = 0xEA, le type de module 0x0110 = 0xCC et la révision 0x0111 = 0x10 sont donnés (p. 16) ; le mode d'E/S par défaut du pilote est 1V8, le mode 2V8 (niveaux de 2,6 à 3,5 V, tableau 13 p. 18) est à régler : vérifier dans l'ULD que l'initialisation le fait (DES-019 « Pilote du capteur de hauteur non bloquant »). Reste ouvert.
**Décision liée :** {DEC-239 « Capteur de hauteur : pilote non bloquant, reprise, échec d'initialisation, mesure horodatée »}

### DOU-153 — Carte double face, assemblage Standard, frais d'extension et délais
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-013 « Carte électronique JLCPCB, câblage et assemblage »
**Question :** l'assemblage « Standard » (double face, panneau de 70 × 70 mm, fiduciaires) coûte plus cher que « Économique » (simple face) ; les frais d'extension de chaque référence « expand » (environ 9 à 11 références), le cuivre de 2 oz, la distance composant-bord et le délai de fabrication du circuit n'ont pas été vérifiés.
**Réponse :** (aucune) ; à lire sur le devis de JLCPCB avant la commande. Non bloquant ; repli : carte simple face « Économique ».
**Décision liée :** {DEC-236 « Assemblage par JLCPCB : puces nues, carte double face, flux acheté »}

### DOU-154 — Vibrations des moteurs sur la centrale inertielle posée sur la carte rigide
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-003 « Centrale inertielle »
**Question :** la centrale n'est plus sur une petite carte collée sur de la mousse : elle est sur la carte principale, fixée au cadre. Les vibrations des moteurs à balais peuvent bruiter les mesures.
**Réponse :** (aucune) ; fixer la carte sur de la mousse ou des plots souples et mesurer le bruit à TI-013 « Boucle de contrôle sur potence ». Non bloquant.
**Décision liée :** {DEC-236 « Assemblage par JLCPCB : puces nues, carte double face, flux acheté »}

### DOU-155 — Connecteur XT30 : genre côté carte et surtension à la connexion
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-008 « Batterie et connecteur débranchable » et ARC-009 « Alimentation de la logique et mesure de la tension »
**Question :** le XT30PW retenu est mâle (C431092) ; la batterie achetée peut avoir un connecteur du même genre. De plus, la mise sous tension de la batterie peut produire un dépassement de tension sur l'entrée du régulateur (maximum absolu d'environ 6 V, dépassement calculé d'environ 4,7 V, valeurs à vérifier).
**Réponse :** (aucune) ; choisir le genre à l'achat de la batterie ; mesure du dépassement à TI-008 « Batterie, connecteur, chute de tension et mesure de tension ». Non bloquant ; à lever avant la commande de la carte. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-282 « Voyant RGB, XC6206 et connecteur XT30 : valeurs de fiche ») : genre mâle confirmé pour le XT30PW (fiche Amass p. 1 et 2) ; désignation de la fiche XT30PW30-M.G.Y, différente de la nomenclature (DOU-198 « Écarts avec l'architecture à reporter à la prochaine révision : débit, réveil du module, boîtier, désignation du XT30 ») ; le genre de la batterie achetée reste à relever (fiche absente : DOU-191 « Fiche de la batterie absente du dossier des fiches ») ; MCP1700 : maximum absolu 6,5 V, fonctionnement 2,3 à 6,0 V (dépassement calculé de 4,7 V, marge de 1,8 V), la mesure de TI-008 « Batterie, connecteur, chute de tension et mesure de tension » reste nécessaire. Reste ouvert.
**Décision liée :** {DEC-243 « Latence de l'arrêt sans fil et module Bluetooth : mesure avant la commande de la carte »}

### DOU-156 — Vérifications avant la commande de la carte
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-013 « Carte électronique JLCPCB, câblage et assemblage », ARC-012 « Module radio Bluetooth à basse consommation » et ARC-002 « Microcontrôleur et programmation par liaison SWD »
**Question :** les essais TI-001 « Alimentation, programmation SWD et octets d'option », TI-008 « Batterie, connecteur, chute de tension et mesure de tension » et TI-013 « Boucle de contrôle sur potence » demandent la carte livrée : ils ne peuvent pas précéder la commande. Quelles vérifications se font avant ?
**Réponse :** décision provisoire : avant la commande, tester le module BLE seul (TI-010 « Liaison Bluetooth à basse consommation »), le brochage, les fonctions alternatives et les registres sur une carte Nucleo STM32G431 et dans les fiches, la poussée et la résistance interne au banc (TI-007 « Moteurs, poussée, masse et dimensions »), le genre du XT30 et le devis ; le dépassement de tension, les vibrations et la consommation restent mesurés sur la première carte (5 cartes commandées, risque accepté). Non bloquant.
**Décision liée :** {DEC-244 « Relecture de porte de la révision JLCPCB : corrections décidées par délégation »}

### DOU-157 — VL53L1CX contre VL53L1X : identifiant, bibliothèque et registres
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-004 « Capteur de hauteur à temps de vol »
**Question :** la référence en stock VL53L1CXV0FY/1 est présentée comme la référence ST du VL53L1X ; elle pourrait être une variante (VL53L1CX) avec un identifiant et une bibliothèque différents de ceux supposés (0xEACC, ULD du VL53L1X).
**Réponse :** (aucune) ; vérifier dans la fiche ST avant la commande, sinon changer de référence ; essai possible sur une carte du commerce. Non bloquant, à lever avant la commande de la carte. Complément du 2026-11-04 : la fiche déposée sous le nom `DS_vl53l1.pdf` est DS11786 rév. 16 (janvier 2026), celle du **VL53L1** (référence de commande VL53L1CBV0FY/1, multizone), et non celle du VL53L1X ni du VL53L1CX ; elle donne les mêmes identifiants (0x010F = 0xEA et 0x0110 = 0xCC) et une alimentation AVDD de 2,6 à 3,5 V, compatible avec le rail de 3,0 V. La référence CX en stock n'y figure pas : le doute reste ouvert, la fiche et la bibliothèque du VL53L1CX restent à vérifier.
**Décision liée :** {DEC-244 « Relecture de porte de la révision JLCPCB : corrections décidées par délégation »} ; DEC-289 « Fiches du 2026-11-04 : PMW3901MB, ferrite, diode SS34, buzzer et VL53L1 »

### DOU-158 — Initialisation du capteur de hauteur plus longue que le chien de garde
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-023 « Initialisation et échec d'initialisation », ARC-022 « Chien de garde » et ARC-004 « Capteur de hauteur à temps de vol »
**Question :** le chien de garde matériel dure 100 ms dès le reset alors que l'initialisation par la bibliothèque ST est estimée à 110 à 170 ms avec ses attentes.
**Réponse :** décision provisoire : les attentes de la bibliothèque sont découpées ou rappellent la fonction unique de rafraîchissement ; à vérifier à TI-018 « Initialisation et échec d'initialisation » et TI-028 « Pilote du capteur de hauteur : durée d'appel, bus bloqué, capteur muet ». Non bloquant.
**Décision liée :** {DEC-244 « Relecture de porte de la révision JLCPCB : corrections décidées par délégation »}

### DOU-159 — Ordonnancement des tâches de fond : flux à 100 Hz, pilote de hauteur et latence de l'arrêt sans fil
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-015 « Structure logicielle et ordonnancement », ARC-005 « Capteur de flux optique » et ARC-025 « Protocole et service du statut sans fil »
**Question :** avec une seule tâche de fond par cycle, le flux à 100 Hz en plusieurs pas, le pilote de hauteur et le traitement de l'arrêt sans fil peuvent se gêner ; le pire cas (300 µs + 200 µs) égale l'ancien seuil d'alarme de 500 µs.
**Réponse :** décision provisoire : tâches choisies par priorité (arrêt radio, hauteur, flux, statut, effets), seuil d'alarme porté à 800 µs ; à confirmer par la mesure du temps de calcul à TI-011 « Cadence du cycle et temps de réponse de l'arrêt d'urgence ». Non bloquant.
**Décision liée :** {DEC-244 « Relecture de porte de la révision JLCPCB : corrections décidées par délégation »}

### DOU-160 — Mesure de hauteur valide et sols sombres ou brillants
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-016 « Pilotes des capteurs et des sorties », ARC-021 « Surveillance et coupures automatiques » et ARC-004 « Capteur de hauteur à temps de vol »
**Question :** la coupure à 200 ms sans mesure de hauteur valide ne dit pas ce qu'est une mesure valide ; un sol noir mat ou brillant, une vitre ou le soleil peuvent invalider la mesure plus de 200 ms.
**Réponse :** décision provisoire : valide = statut de portée sans erreur et taux de signal au-dessus du seuil de la bibliothèque ; sinon la coupure à 200 ms intervient (choix prudent) ; sols difficiles essayés à TI-028 « Pilote du capteur de hauteur : durée d'appel, bus bloqué, capteur muet ». Non bloquant.
**Décision liée :** {DEC-244 « Relecture de porte de la révision JLCPCB : corrections décidées par délégation »}

### DOU-161 — Tensions directes du voyant RGB : visibilité du vert et du bleu entre 3,4 et 3,7 V
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-011 « Voyant RGB et avertisseur sonore » et REQ-019 « Perceptibilité et distinction des effets »
**Question :** si le vert et le bleu ont 3,4 V de tension directe, ils sont très faibles autour de 3,7 V (environ 4 mA) et éteints sous 3,4 V, alors que l'effet 1 « Allumé » est vert et l'effet 4 « Lancé et vol » est blanc.
**Réponse :** (aucune) ; mesurer la LED retenue, changer de LED ou de résistances avant la commande si besoin. Non bloquant. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-282 « Voyant RGB, XC6206 et connecteur XT30 : valeurs de fiche ») : fiche SZYY1615RGB-B : tension directe du vert et du bleu de 2,8 à 3,4 V à 20 mA, courbe typique d'environ 3,1 V et 3,2 V ; la décision sur la LED ou les résistances dépend d'un échantillon mesuré à TI-009 « Bouton, voyant RGB et avertisseur ». Rouge : 37 mW pour 40 mW permis, courant admis réduit vers 45 à 50 °C : marge faible acceptée pour la première version. Reste ouvert.
**Décision liée :** {DEC-244 « Relecture de porte de la révision JLCPCB : corrections décidées par délégation »}

### DOU-162 — Implantation mécanique de la carte, du connecteur et de la batterie
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-013 « Carte électronique JLCPCB, câblage et assemblage », ARC-008 « Batterie et connecteur débranchable » et ARC-004 « Capteur de hauteur à temps de vol »
**Question :** la carte de 40 × 35 mm est au centre, entre des moteurs à 49 mm d'entraxe ; l'accès au connecteur au bord, la place de la batterie, le cône du capteur de hauteur avec la puce et la lentille du flux optique sur la même face basse (cônes de 27° et de 42°) et le flux d'air des hélices ne sont pas dessinés.
**Réponse :** (aucune) ; croquis coté (dessus et côté) avant le routage. Non bloquant. Complément du 2026-11-05 (essai du moteur de placement PCB, DEC-292 « Moteur autonome d'optimisation du placement PCB (hors KiCad) ») : pour tester le placement, l'utilisateur a donné en chat un contour cible de **50 x 50 mm** et des connecteurs M1-M4 (header 2 broches, pas 5,08 mm, ~8 x 3 mm) aux 4 coins (M1 nord-ouest, M2 nord-est, M3 sud-est, M4 sud-ouest), J1 débordant le bord sud, U7 (module radio) débordant entièrement le bord ouest — voir `projets/boomrone/hardware/kicad/proj_boomrone/placement_constraints.json`. **Ceci contredit la carte de 40 x 35 mm donnée plus haut dans ce doute et dans DOU-204 « PB-03F : empreinte de 24 x 16 mm, antenne et masse »** (ARC-013 « Carte électronique JLCPCB, câblage et assemblage ») : à confirmer explicitement avec l'utilisateur avant d'écrire une décision (DEC) qui tranche ce doute - pour l'instant ces valeurs ne servent qu'à l'essai du moteur de placement, pas encore une cote officielle de la carte. Reste ouvert.
**Décision liée :** {DEC-244 « Relecture de porte de la révision JLCPCB : corrections décidées par délégation »}

### DOU-163 — Valeurs de fiche à relever : rappel de GPIO1, résistance de l'AO3400A, USB du G431
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-004 « Capteur de hauteur à temps de vol », ARC-007 « Étage de puissance des moteurs coupés par défaut » et ARC-002 « Microcontrôleur et programmation par liaison SWD »
**Question :** GPIO1 serait en drain ouvert (rappel externe prévu) ; la résistance de l'AO3400A à 2,5 V est peut-être plus élevée que 33 mΩ (pertes de 0,2 W optimistes) ; la fonction USB de PA11 sur le G431 est incertaine ; le courant de calage d'un moteur 8520 bloqué n'est pas écrit.
**Réponse :** (aucune) ; relever dans les fiches avant le routage. Non bloquant. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-281 « Puissance et alimentation : AO3400A, MCP1700, source de l'ADC et étalonnage ») : GPIO1 du VL53L1X en drain ouvert avec rappel de 10 kΩ (DS12385 p. 5 et 6) ; AO3400A 24 mΩ typique et 48 mΩ au maximum à VGS = 2,5 V (p. 2), la valeur à 3,0 V n'étant pas trouvée (DOU-199 « AO3400A : résistance à 3,0 V et capacité d'entrée maximale non trouvées dans la fiche ») ; PA11 en AF11 (TIM1_CH4), USB_DM sans effet (DS12589 tableau 13) ; le courant de calage du moteur 8520 est détaché dans DOU-190 « Fiche du moteur 8520 absente du dossier des fiches : courant de calage ». Reste ouvert tant que les deux points non trouvés ne sont pas tranchés.
**Décision liée :** {DEC-244 « Relecture de porte de la révision JLCPCB : corrections décidées par délégation »}

### DOU-164 — PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-005 « Capteur de flux optique », ARC-013 « Carte électronique JLCPCB, câblage et assemblage » et REQ-044 « Assemblage à la main »
**Question :** (1) JLCPCB assemble-t-il la puce COB-28 C43496881 (« expand », 182 en stock le 2026-10-29, lot de 80 par tube) ? Le catalogue ne l'indique pas ; l'empreinte du catalogue est « COB-28_6.0X6.0X0.65P ». (2) La lentille LN03-ZSZ, pièce séparée d'après la fiche, est-elle fournie avec la puce ? La photo du catalogue montre une puce et une petite lentille, le nom interne est « lot de 2 pièces », le poids du lot est de 0,357 g ; la lentille n'est pas commandable seule chez JLCPCB (recherche du 2026-10-29). JLCPCB ne la pose probablement pas : collage à la main, colle et alignement non définis. (3) Profil de refusion de la puce : non indiqué dans la fiche lue (soudure sans plomb 260 °C au plus, seule donnée), niveau de sensibilité à l'humidité non connu. (4) Le stock de 182 suffit pour 5 cartes, mais baisse chaque jour ; l'unité du stock et du prix (pièce ou lot de 2), le minimum de commande et les frais d'extension sont à lire sur le devis. (5) Ordre des faces et nombre de passages au four de la carte double face : la puce est sur la face basse, qui peut subir deux refusions ; sensibilité à l'humidité non connue. (6) Collage de la lentille : colle sans effet sur l'optique, alignement, propreté, critère d'acceptation à définir (TA-015 « Inspection de la fabrication à la main »).
**Réponse :** (aucune) ; avant la commande de la carte : relire le devis et l'aperçu de fabrication (DFM) de JLCPCB avec la référence C43496881, et demander au service client si la lentille est dans le lot, si la puce est posée au four standard et comment est livrée la lentille. Repli décidé : carte achetée Pimoroni PMW3901 soudée par 6 fils si JLCPCB refuse la puce ou si la lentille manque (DEC-248 « Flux optique : lentille collée à la main et repli sur carte achetée »). Non bloquant.
**Décision liée :** {DEC-246 « Flux optique : puce PMW3901MB-TXQT achetée et posée par JLCPCB »} ; {DEC-248 « Flux optique : lentille collée à la main et repli sur carte achetée »}

### DOU-165 — Flux optique : alimentation en 2,0 V, valeurs de fiche et mise sous tension
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-009 « Alimentation de la logique et mesure de la tension », ARC-005 « Capteur de flux optique » et ARC-002 « Microcontrôleur et programmation par liaison SWD »
**Question :** le XC6206P202MR-G (2,0 V fixe, C2891260) n'a pas été lu dans sa fiche : tolérance de la sortie (la puce n'accepte que 1,8 à 2,1 V, bruit compris), chute de tension à 9 mA (le catalogue donne 780 mV à 100 mA), capacité de sortie pour la stabilité et réponse à la pointe de 70 mA de la mise sous tension. Valeurs des condensateurs et des résistances de la figure 8 de la fiche de la puce (texte extrait ambigu). Niveau d'entrée haut du STM32G431 face à la sortie MISO de la puce (au moins VDDIO − 0,45 V, soit 2,55 V à 1 mA), à relever dans DS12589 (à lire dans DS12589, hors du périmètre de DOU-148 « Numéros de broches physiques du LQFP-48 à relever dans la fiche DS12589 »). Ordre de mise sous tension : VDDIO (rail de 3,0 V) est présent avant VDD (2,0 V), conforme à VDDIO ≥ VDD de la fiche, séquence non écrite dans la fiche lue : hypothèse, non démontrée ; à l'extinction VDDIO peut tomber avant VDD (capacité de sortie du régulateur) et un creux du rail en vol peut faire décrocher la puce sans reset du microcontrôleur, NRESET n'étant pas câblée : prévoir la détection logicielle d'une puce muette ou figée et sa ré-initialisation par registre (au sol), et l'essai de coupure rapide de TI-001 « Alimentation, programmation SWD et octets d'option ». La tolérance totale du XC6206 (tension, température, charge) doit tenir dans 1,8 à 2,1 V avant la commande : sinon régulateur de précision ±1 %. À lever avant le gel de la nomenclature.
**Réponse :** (aucune) ; relever dans les fiches avant le routage ; mesurer à TI-001 « Alimentation, programmation SWD et octets d'option » (rail de 2,0 V entre 1,8 et 2,1 V) et TI-002 « Bus SPI, I2C et capteurs ». Non bloquant. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-282 « Voyant RGB, XC6206 et connecteur XT30 : valeurs de fiche ») : XC6206P202MR-G (fiche Torex ETR0305_004b) : sortie 1,96 à 2,04 V, chute à 100 mA de 350 mV typique et 780 mV au maximum (valeur à 70 mA non donnée), 120 mA minimum, CIN = 1,0 µF et CL = 1,0 µF (2,2 µF compatible), SOT-23 1 VSS, 2 VOUT, 3 VIN ; VIH du STM32 = 0,7 × VDD = 2,1 V pour une sortie MISO d'au moins 2,55 V (marge de 0,45 V). Manquent toujours la fiche de la puce (figure 8, ordre de mise sous tension, réponse à la pointe de 70 mA, NRESET : DOU-185 « Fiche du capteur de flux PMW3901MB absente du dossier des fiches »). Reste ouvert. Complément du 2026-11-04 : fiche de la puce lue : VDD de 1,8 à 2,1 V, maximum absolu de 2,1 V bruit compris (bruit sinusoïdal toléré de 100 mV crête à crête de 10 kHz à 75 MHz) : la sortie du XC6206 de 1,96 à 2,04 V laisse 60 mV de marge avant ce maximum, faible, à confirmer par la mesure à TI-001 « Alimentation, programmation SWD et octets d'option » avec le bruit réel ; VDDIO de 1,8 à 3,6 V avec VDDIO ≥ VDD, donc 3,0 V convient ; VIH du STM32 de 2,1 V face à une sortie MISO d'au moins VDDIO − 0,45 V = 2,55 V (marge confirmée) ; pointe de 70 mA à la montée de l'alimentation, confirmée. Reste ouvert (condensateurs : DOU-205 « PMW3901MB : condensateurs du schéma de référence de la fiche et valeur illisible de R1 »).
**Décision liée :** {DEC-247 « Flux optique : alimentation en 2,0 V par un régulateur dédié, signaux en 3,0 V »} ; DEC-289 « Fiches du 2026-11-04 : PMW3901MB, ferrite, diode SS34, buzzer et VL53L1 »

### DOU-166 — PMW3901MB : plage de température de 0 à 40 °C et hauteur de montage avec la lentille
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-005 « Capteur de flux optique » et ARC-013 « Carte électronique JLCPCB, câblage et assemblage »
**Question :** la fiche donne une température de fonctionnement de 0 à 40 °C : la face basse de la carte, proche des moteurs, de la batterie et du régulateur MCP1700T-3002E/TT (échauffement estimé de 40 à 55 °C en SOT-23, ARC-009 « Alimentation de la logique et mesure de la tension »), et un vol dans un gymnase ou un jardin chaud, restent-ils dans cette plage ? Le boîtier fait 2,28 mm de haut, sans doute lentille comprise (non confirmé) : la hauteur de la lentille au-dessus de la carte, la distance au sol avec le capteur de hauteur monté à 20 mm du plan de contact (DOU-139 « Capteurs de hauteur et de flux : hauteur de montage et sols sans texture ») et les cônes de 42° et 27° sont à dessiner (DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie »).
**Réponse :** (aucune) ; mesure de la température de la puce à TI-004 « Flux optique et vitesse horizontale » (moteurs en marche 30 s) ; hauteur à dessiner avec le croquis coté avant le routage. Aucune exigence ne fixe la température ambiante de vol : à demander à l'utilisateur avant la commande (jardin d'été). Distance entre le régulateur et la puce, cuivre et comportement du logiciel si la qualité du flux chute (vitesse déclarée invalide) à fixer au routage. Non bloquant. Complément du 2026-11-04 : la fiche déposée (PMW3901MB v1.5) donne une température de fonctionnement de **0 à 60 °C** (et non 0 à 40 °C : valeur de la première lecture, d'une source non retrouvée) et un boîtier de **6 x 6 x 3,08 mm avec l'ensemble de lentille L214-ZSZ** (et non 2,28 mm) ; la plage de travail commence à 80 mm (le flux est donc invalide sur le sol et au début de la montée, le capteur étant à environ 20 mm du plan de contact : à traiter avec DOU-139 « Capteurs de hauteur et de flux : hauteur de montage et sols sans texture » et dans la logique d'armement et de décollage). Le risque de température est beaucoup plus faible (marge de la fiche de 60 °C contre un échauffement estimé de 40 à 55 °C), la mesure à TI-004 « Flux optique et vitesse horizontale » reste utile. La hauteur de 3,08 mm entre dans le croquis coté de DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie ». Le titre de ce doute garde l'ancienne plage de 0 à 40 °C pour rester identique dans les documents qui le citent. Reste ouvert.
**Décision liée :** {DEC-246 « Flux optique : puce PMW3901MB-TXQT achetée et posée par JLCPCB »} ; DEC-289 « Fiches du 2026-11-04 : PMW3901MB, ferrite, diode SS34, buzzer et VL53L1 »

### DOU-167 — Orientation des axes de la centrale et sens de rotation des moteurs
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-003 « Centrale inertielle », ARC-006 « Moteurs, hélices et protège-hélices », ARC-018 « Boucle de contrôle du vol », DES-003 « Raccordement de la centrale inertielle LSM6DSO », DES-006 « Cadre, anneaux, moteurs et hélices », DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique »
**Question :** la matrice d'axes de la centrale (puce sur la face basse) et la table de signes du mixeur supposent un repère x avant, y gauche, z haut et des moteurs 1 et 3 horaires. Ces choix ne sont connus qu'après le routage (sens de la puce) et l'essai des hélices.
**Réponse :** décision provisoire de DEC-259 « Contrôle : poussée linéarisée, mixeur en X et priorité à l'attitude » : matrice par défaut de 180° autour de x, table de signes de DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique » ; vérifier sur la potence (TI-013 « Boucle de contrôle sur potence ») et corriger les constantes (une seule table, `config_fixed.h` et `ctl_mixer.c`). Non bloquant.
**Décision liée :** DEC-259 « Contrôle : poussée linéarisée, mixeur en X et priorité à l'attitude »

### DOU-168 — Centrale inertielle ou flux optique absent à l'initialisation
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-023 « Initialisation et échec d'initialisation », REQ-017 « Initialisation en 3 secondes », REQ-037 « Comportement en échec d'initialisation », DES-031 « Séquence d'initialisation et échec d'initialisation »
**Question :** REQ-017 « Initialisation en 3 secondes » ne cite que le mouvement et le défaut de platitude comme causes d'échec d'initialisation, et ARC-023 « Initialisation et échec d'initialisation » y ajoute le capteur de hauteur absent. L'absence de la centrale inertielle ou du flux optique n'est prévue nulle part.
**Réponse :** décision provisoire de DEC-264 « Initialisation : centrale inertielle ou flux optique absent vaut échec d'initialisation » : ces absences valent échec d'initialisation, comme le capteur de hauteur. À confirmer à la porte (une ligne à ajouter à REQ-017 « Initialisation en 3 secondes » si l'utilisateur le souhaite ; ARC-023 « Initialisation et échec d'initialisation » et REQ-017 « Initialisation en 3 secondes » ne sont pas modifiées par cette phase). Non bloquant.
**Décision liée :** DEC-264 « Initialisation : centrale inertielle ou flux optique absent vaut échec d'initialisation »

### DOU-169 — Matière, masse, délai et cotes verticales des pièces imprimées
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-006 « Moteurs, hélices et protège-hélices », ARC-014 « Bilan de masse, de poussée et d'autonomie », DES-006 « Cadre, anneaux, moteurs et hélices »
**Question :** la matière du cadre (résine ou autre), son prix, son délai, sa masse réelle (9 g estimés) et la tenue de parois de 1,0 mm ne sont pas établis ; les cotes verticales dépendent du croquis de DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie ».
**Réponse :** décision provisoire de DEC-268 « Mécanique : anneaux tangents, modèle OpenSCAD et impression en ligne » : résine par un service en ligne ; devis et masse à relever avant la commande de la pièce ; repli sur une autre technique si les parois ne tiennent pas. Non bloquant.
**Décision liée :** DEC-268 « Mécanique : anneaux tangents, modèle OpenSCAD et impression en ligne »

### DOU-170 — Constantes de capteurs de départ : échelle du flux, retard du capteur de hauteur, filtres
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-005 « Capteur de flux optique », ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse », DES-024 « Observateur de hauteur et de vitesse verticale », DES-025 « Vitesse horizontale et critères d'immobilité, de platitude et de stationnaire »
**Question :** l'échelle du flux (0,0021 rad par pas, reprise de mémoire d'un pilote publié), le retard effectif du capteur de hauteur (33 ms), les seuils de qualité du flux (30) et du taux de signal sont des valeurs de départ non vérifiées.
**Réponse :** décision provisoire de DEC-260 « Gains de référence et constantes de départ provisoires » et DEC-261 « Estimation : filtre de Mahony, observateur de hauteur et compensation du retard » : valeurs de départ dans `config_fixed.h`, étalonnées à TI-004 « Flux optique et vitesse horizontale », TI-003 « Hauteur du capteur à temps de vol et position de montage » et TI-012 « Chaîne capteurs vers estimation ». Non bloquant.
**Décision liée :** DEC-260 « Gains de référence et constantes de départ provisoires »

### DOU-171 — Gains de référence, poussée de sustentation et linéarisation de la poussée
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-018 « Boucle de contrôle du vol », REQ-006 « Stabilisation après le lancer », REQ-008 « Tenue du vol stationnaire », DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique »
**Question :** les gains de DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique », la poussée de sustentation de 0,69 (rapport poussée/poids de 1,44) et l'hypothèse « poussée proportionnelle au carré de la tension » ne reposent sur aucune mesure (pas de mesures au banc : DEC-252 « Phase conception détaillée ouverte avant les mesures au banc »). Le stationnaire en 2 s depuis 1,5 m n'est pas démontré (DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m »).
**Réponse :** décision provisoire de DEC-259 « Contrôle : poussée linéarisée, mixeur en X et priorité à l'attitude » et DEC-260 « Gains de référence et constantes de départ provisoires » ; réglage sur la potence (TI-013 « Boucle de contrôle sur potence ») puis en vol. Non bloquant.
**Décision liée :** DEC-260 « Gains de référence et constantes de départ provisoires »

### DOU-172 — Valeurs de configuration des périphériques à vérifier dans le manuel de référence
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-002 « Microcontrôleur et programmation par liaison SWD », DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option », DES-022 « Pilote de la mesure de tension de la batterie »
**Question :** états d'attente de la flash à 170 MHz et mode « boost », registre de timing de l'I2C à 400 kHz, horloge de l'ADC, adresse de VREFINT_CAL (0x1FFF75AA), valeur nominale de VREFINT et canal 18 de l'ADC1 sont repris de mémoire.
**Réponse :** à relever dans le manuel de référence RM0440 et la fiche DS12589, y compris la fonction alternative de chaque broche moteur (PA11 est TIM1_CH4 en AF11 de mémoire, pas AF6) à l'écriture du code, avant le premier essai sur la carte ; une carte Nucleo STM32G431 permet l'essai avant la commande de la carte (DOU-156 « Vérifications avant la commande de la carte »). Non bloquant. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-278 « Microcontrôleur : états d'attente de la flash, séquence boost, USART2 et I2C1 d'après les fiches ») : confirmés dans DS12589 et RM0440 : PA11 en AF11, mode boost (R1MODE), PLL (M = 4, N = 85, R = 2), adresse 0x1FFF75AA de VREFINT_CAL à 3,0 V, VREFINT nominale, canal 18, horloge de l'ADC HCLK/4, déclenchement par TIM6 ; états d'attente corrigés à 4 (et non 8) ; I2C1 sur HSI16 avec TIMINGR = 0x10320309 (exemple à 16 MHz du RM0440, rien pour 170 MHz) ; la durée de démarrage du régulateur de l'ADC (tADCVREG_STUP) est ambiguë dans l'extraction du texte de DS12589 p. 119 (DOU-197 « ADC : attente du régulateur à confirmer et comportement si l'étalonnage échoue »). Reste ouvert tant que ce dernier point et le contrôle du TIMINGR avec l'outil de ST ne sont pas faits.
**Décision liée :** DEC-257 « Valeurs de configuration des horloges, timers, bus et convertisseur »

### DOU-173 — Composants passifs et découplages à relever dans les fiches avant le routage
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-003 « Centrale inertielle », ARC-004 « Capteur de hauteur à temps de vol », ARC-009 « Alimentation de la logique et mesure de la tension », DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option », DES-003 « Raccordement de la centrale inertielle LSM6DSO », DES-004 « Raccordement du capteur de hauteur VL53L1X », DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V », DES-008 « Batterie, connecteur XT30 et entrée de la carte », DES-009 « Régulateur de 3,0 V et pont de mesure de la tension »
**Question :** découplages de la centrale, du capteur de hauteur, du microcontrôleur, condensateurs d'entrée et de sortie du MCP1700 et du XC6206, liaison auxiliaire de la centrale, résistance de la ferrite ne sont pas relevés dans les fiches (seul souvenir ou ordre de grandeur dans DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option » à DES-009 « Régulateur de 3,0 V et pont de mesure de la tension »).
**Réponse :** relever dans les fiches avant le routage ; les valeurs de ce document sont des valeurs usuelles (100 nF par broche, 1 à 10 µF). Non bloquant. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-279 « Microcontrôleur : découplage, BOR et chien de garde d'après les fiches » et DEC-280 « Capteurs : VL53L1X sans broche IOVDD, LSM6DSO et délai de mise en route ») : relevés dans les fiches : microcontrôleur (VDDA 10 nF + 1 µF, VREF+ 100 nF + 1 µF, VBAT, 100 nF par VDD et 4,7 µF, NRST 100 nF), centrale (100 nF sur VDD et VDDIO, liaison auxiliaire, le 10 µF commun est un ajout du projet), capteur de hauteur (4,7 µF + 100 nF sur AVDDVCSEL, le 100 nF sur AVDD est un ajout du projet), MCP1700 (1 µF en entrée et en sortie au minimum), XC6206 (1,0 µF). Manquent la résistance de la ferrite (DOU-186 « Fiche de la ferrite BLM18PG121SN1D absente du dossier des fiches ») et la figure 8 de la puce du flux (DOU-185 « Fiche du capteur de flux PMW3901MB absente du dossier des fiches »). Reste ouvert.
**Décision liée :** DEC-269 « Matériel : ferrite hors du chemin des moteurs, mesure en amont, rappels des sélections de bus »

### DOU-174 — Séquence d'initialisation du flux et bibliothèque ULD : taille, appels bloquants, licence
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-004 « Capteur de hauteur à temps de vol », ARC-005 « Capteur de flux optique », DES-015 « Arborescence du firmware, édition de liens et budget de mémoire », DES-019 « Pilote du capteur de hauteur non bloquant », DES-020 « Pilote du flux optique »
**Question :** la suite d'une cinquantaine d'écritures du PMW3901 vient d'un pilote publié, dont la licence est à vérifier avant d'en recopier le texte ; la bibliothèque ULD de ST a une taille (budget de 50 kio) et des fonctions à attentes bloquantes à découper pour le chien de garde, non mesurées.
**Réponse :** à vérifier à l'écriture du code ; si la licence l'interdit, refaire la suite d'après la fiche de PixArt ; si l'ULD dépasse le budget, ne garder que les fonctions d'initialisation. Non bloquant.
**Décision liée :** DEC-255 « Conception détaillée : chaîne de développement et arborescence des fichiers »

### DOU-175 — Résolution de la vitesse horizontale du flux face au seuil de 0,3 m/s
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** DEC-262 « Vitesse horizontale invalide : stationnaire non déclaré », DOU-139 « Capteurs de hauteur et de flux : hauteur de montage et sols sans texture », REQ-007 « Critère de vol stationnaire », ARC-005 « Capteur de flux optique », DES-025 « Vitesse horizontale et critères d'immobilité, de platitude et de stationnaire »
**Question :** avec l'échelle de départ, un pas du flux correspond à environ 0,21 m/s à 1 m de hauteur et 100 Hz ; le seuil de stationnaire est de 0,3 m/s : sa précision de mesure dépend du filtrage et de la hauteur.
**Réponse :** le filtre du premier ordre à 0,3 lisse les pas ; à confirmer à TI-004 « Flux optique et vitesse horizontale » ; si le critère est trop bruité, revoir le filtre ou le seuil par une demande de modification de REQ-007 « Critère de vol stationnaire ». Non bloquant.
**Décision liée :** DEC-262 « Vitesse horizontale invalide : stationnaire non déclaré »

### DOU-176 — Tests unitaires sur PC : écart entre la maquette de registres et le composant réel
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** DES-015 « Arborescence du firmware, édition de liens et budget de mémoire », DES-016 « Tick de 1 kHz, cycle de contrôle et ordonnanceur de tâches de fond », DES-017 « Coupure des moteurs, démarrage unique et gestionnaires d'exception »
**Question :** les tests des pilotes sur PC utilisent une maquette de registres : ils ne détectent ni une erreur de nom de bit, ni un temps d'attente trop court, ni un conflit de DMA.
**Réponse :** ces risques sont couverts par les tests d'intégration sur la carte (TI-002 « Bus SPI, I2C et capteurs », TI-011 « Cadence du cycle et temps de réponse de l'arrêt d'urgence », TI-029 « Mémoire, écriture de flash pendant une mesure et chronomètres ») ; ne pas considérer un TU de pilote comme preuve du fonctionnement du composant. Non bloquant.
**Décision liée :** DEC-256 « Tests unitaires compilés sur PC avec maquette des registres »

### DOU-177 — Filtre d'attitude : l'accéléromètre en vol mesure la poussée, pas la gravité
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-017 « Estimation de l'attitude, de la hauteur et de la vitesse », DES-023 « Filtre d'attitude de Mahony »
**Question :** moteurs en marche, l'accélération mesurée est la force spécifique (poussée et traînée) : le filtre de Mahony la prend pour la gravité et tire l'inclinaison vers l'horizontale.
**Réponse :** décision provisoire : Kp de 0,3 s⁻¹ moteurs en marche (2,0 s⁻¹ au sol) ; à régler sur la potence (TI-013 « Boucle de contrôle sur potence »). Non bloquant.
**Décision liée :** DEC-260 « Gains de référence et constantes de départ provisoires »

### DOU-178 — Horloge à 16 MHz de l'échec par sous-tension abandonnée
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-023 « Initialisation et échec d'initialisation », DES-031 « Séquence d'initialisation et échec d'initialisation », DOU-118 « Seuil de protection et consommation résiduelle du drone laissé allumé »
**Question :** ARC-023 « Initialisation et échec d'initialisation » prévoit 16 MHz en échec par sous-tension ; la conception garde 170 MHz, la consommation résiduelle et la durée avant 3,0 V (DOU-118 « Seuil de protection et consommation résiduelle du drone laissé allumé ») sont donc moins bonnes que les 12 mA estimés.
**Réponse :** décision provisoire de DEC-274 « Échec par sous-tension : horloge conservée à 170 MHz » ; consigne « débrancher » de ARC-030 « Page de consignes d'emploi » ; à mesurer à TI-008 « Batterie, connecteur, chute de tension et mesure de tension ». Non bloquant ; à présenter à la porte.
**Décision liée :** DEC-274 « Échec par sous-tension : horloge conservée à 170 MHz »

### DOU-179 — Anti-repliement de la centrale : sortie à 3,33 kHz lue à 1 kHz
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-003 « Centrale inertielle », DES-003 « Raccordement de la centrale inertielle LSM6DSO », DES-018 « Pilote de la centrale inertielle », DOU-154 « Vibrations des moteurs sur la centrale inertielle posée sur la carte rigide »
**Question :** la lecture à 1 kHz d'une sortie à 3,33 kHz peut replier les vibrations des moteurs ; aucun filtre passe-bas n'est réglé sur l'accéléromètre.
**Réponse :** à mesurer sur la carte (spectre des vibrations, TI-013 « Boucle de contrôle sur potence ») ; options : filtre numérique de l'accéléromètre, sortie à 1,66 kHz, lecture sur INT1. Non bloquant.
**Décision liée :** DEC-261 « Estimation : filtre de Mahony, observateur de hauteur et compensation du retard »

### DOU-180 — Recouvrement de la carte et des disques d'hélice
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-006 « Moteurs, hélices et protège-hélices », ARC-013 « Carte électronique JLCPCB, câblage et assemblage », ARC-014 « Bilan de masse, de poussée et d'autonomie », DES-006 « Cadre, anneaux, moteurs et hélices », DES-014 « Feuille de calcul du bilan de masse, de poussée et d'autonomie », DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie »
**Question :** la carte de 40 x 35 mm déborde sur les disques des quatre hélices de 45 mm ; la poussée perdue n'est pas dans le bilan.
**Réponse :** à chiffrer sur le croquis coté de DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie » avant le routage ; repli : carte plus étroite. Non bloquant.
**Décision liée :** DEC-268 « Mécanique : anneaux tangents, modèle OpenSCAD et impression en ligne »

### DOU-181 — Bilan d'erreur de la mesure de tension et niveau du BOR
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-009 « Alimentation de la logique et mesure de la tension », DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option », DES-022 « Pilote de la mesure de tension de la batterie », DOU-142 « Fuite d'entrée de l'ADC et marge de ±50 mV de la mesure de tension »
**Question :** l'incertitude de la mesure ne compte pas la tolérance de VREFINT_CAL, le gain de l'ADC, ni l'ondulation à 24 kHz des moteurs ; le niveau 3 du BOR (environ 2,5 V de mémoire) est sous le minimum de 2,6 V du capteur de hauteur.
**Réponse :** budget estimé ±15 mV à confirmer à TI-008 « Batterie, connecteur, chute de tension et mesure de tension » (critère de recette ±30 mV) ; tension du niveau du BOR à relever dans la fiche DS12589. Non bloquant. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-279 « Microcontrôleur : découplage, BOR et chien de garde d'après les fiches ») : niveau 3 du BOR relevé (descendant 2,47 / 2,52 / 2,57 V, montant 2,56 / 2,61 / 2,66 V, DS12589 tableau 19 p. 72), sous le minimum de 2,6 V du VL53L1X : écart accepté (le rail +3V0 reste au-dessus de 2,91 V tant que la batterie dépasse 3,1 V, le drone se coupe sous 3,3 V), niveau 4 écarté ; budget d'erreur : conversion 6,9 LSB au plus, VREFINT_CAL à ±10 mV soit ±12 mV sur 3,7 V, pont ±3,7 mV, somme arithmétique d'environ 24 mV et quadratique d'environ 15 mV, hors dérive et ondulation ; la mesure de TI-008 « Batterie, connecteur, chute de tension et mesure de tension » reste la preuve. Reste ouvert.
**Décision liée :** DEC-258 « Mesure de la tension : séquence de conversion et zone de maintien de la sous-tension »

### DOU-182 — Noms et numéros de broches des circuits intégrés des schémas SVG non relevés dans les fiches
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** DES-003 « Raccordement de la centrale inertielle LSM6DSO », DES-004 « Raccordement du capteur de hauteur VL53L1X », DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V », DES-009 « Régulateur de 3,0 V et pont de mesure de la tension », DES-012 « Raccordement du module Bluetooth PB-03F », DOU-148 « Numéros de broches physiques du LQFP-48 à relever dans la fiche DS12589 »
**Question :** les schémas SVG de la conception détaillée (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée ») nomment des broches que le texte des DES ne donne pas : SCL (SCK), SDA/SDI (MOSI), SDO/SA0 (MISO), INT2, VDDIO de la centrale ; SCL, SDA, GPIO1, XSHUT, AVDD, AVDDVCSEL, IOVDD du capteur de hauteur ; VDD, VDDIO, VREG, NRESET, MOTION, MOSI, MISO, SCK, CS du flux optique ; RXD, TXD, VCC du module radio ; VIN, VOUT, GND des régulateurs. Ces noms sont de mémoire, aucune fiche n'a été lue. Les numéros de broches ne sont affichés que pour les régulateurs MCP1700 et XC6206 (SOT-23 : 1 à 3, en orange, de mémoire) ; ils sont omis pour la centrale (LGA-14), le capteur de hauteur (LGA-12), la puce du flux (COB-28), le module radio et le microcontrôleur (DOU-148 « Numéros de broches physiques du LQFP-48 à relever dans la fiche DS12589 »).
**Réponse :** (à remplir) relever noms et numéros dans les fiches avant le routage, puis corriger les schémas SVG ; ne bloque ni la porte ni la commande de la carte si les schémas KiCad sont saisis depuis les fiches. Complément du 2026-10-30 (relevé des fiches, instruction de l'utilisateur « Oui, appliquer » ; DEC-280 « Capteurs : VL53L1X sans broche IOVDD, LSM6DSO et délai de mise en route ») : noms et numéros de broches relevés dans les fiches pour le STM32 (DOU-148 « Numéros de broches physiques du LQFP-48 à relever dans la fiche DS12589 » levé), la centrale, le capteur de hauteur, les deux régulateurs (brochage confirmé) et le module radio, et reportés dans les schémas SVG et les DES ; manquent les broches de la puce du flux (DOU-185 « Fiche du capteur de flux PMW3901MB absente du dossier des fiches »). Reste ouvert.
**Décision liée :** DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »

### DOU-183 — Repères de composants provisoires des schémas SVG de la conception détaillée
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** DES-001 « Schéma par blocs, réseaux et domaines de tension de la carte », DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option », DES-007 « Circuit de puissance des moteurs », DES-008 « Batterie, connecteur XT30 et entrée de la carte », DES-011 « Circuit du voyant RGB et du buzzer »
**Question :** le texte des DES ne donne aucun repère de composant (R1, C3, U2…) : il décrit les composants par leur fonction et leur valeur. Les schémas SVG (DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée ») attribuent des repères provisoires, uniques sur toute la carte : U1 microcontrôleur, U2 centrale, U3 capteur de hauteur, U4 flux optique, U5 MCP1700, U6 XC6206, U7 module radio ; Q1 à Q4 moteurs, Q5 à Q7 voyant, Q8 buzzer ; D1 à D4 et D5 SS34 ; M1 à M4 ; R1 à R4 grilles de 47 ohms, R5 à R8 rappels des moteurs ; R9 à R11 et R12 à R14 grille et rappel du voyant, R15 à R17 résistances du voyant ; R18 et R19 grille et rappel du buzzer ; R20 et R21 pont de mesure ; R22 à R31 rappels et résistances diverses ; C1 à C33 (C9 non attribué) ; J1 XT30, J2 SWD, FB1 ferrite, SW1 bouton, LED1, BZ1. L'annotation de KiCad les remplacera sans doute. Quels repères retenir, ceux des schémas SVG (au risque de les voir changer à l'annotation) ou ceux de KiCad (à reporter alors dans les SVG et dans le texte des DES) ?
**Réponse :** (à remplir) proposition : garder les repères provisoires jusqu'à la saisie du schéma KiCad, puis reporter les repères définitifs dans les SVG et dans le texte des DES ; ne bloque pas. Complément du 2026-10-30 : deux repères provisoires de plus dans le schéma SVG de DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option » : C34 (100 nF) et C35 (1 µF) sur VREF+ ; le repère C9 reste non attribué ; le total passe de C1 à C35 (DEC-279 « Microcontrôleur : découplage, BOR et chien de garde d'après les fiches »). Complément du 2026-10-30 : les repères R32 et R33 attribués un temps à DES-012 « Raccordement du module Bluetooth PB-03F » (DEC-285 « WKP : PA1 conservée, résistance série de 0 Ω et emplacement de 0 Ω vers la masse non posé ») sont supprimés (DEC-286 « WKP : PA1 directe, emplacements de 0 Ω supprimés ») et libérés ; la suite des repères provisoires est inchangée.
**Décision liée :** DEC-275 « Schémas SVG des circuits de la carte dans la conception détaillée »

### DOU-185 — Fiche du capteur de flux PMW3901MB absente du dossier des fiches
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-005 « Capteur de flux optique », DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V », DES-020 « Pilote du flux optique »
**Question :** la fiche de la puce n'est pas dans `projets/boomrone/Datasheets/` : brochage de la puce COB-28, figure 8 (valeurs des condensateurs et résistances), ordre de mise sous tension, niveau d'entrée bas VIL, réponse à la pointe de 70 mA, NRESET, fréquence maximale de SPI2 (2 MHz de mémoire), valeurs d'identité 0x49 et 0x5F : non trouvés, aucune valeur inventée.
**Réponse :** (à remplir) déposer la fiche et refaire le relevé ; à lever avant le gel de la nomenclature et le routage. Non bloquant. Complément du 2026-11-04 : fiche déposée (`projets/boomrone/Datasheets/PMW3901MB.pdf`, PixArt v1.5 du 21 novembre 2022, EA003EN) : brochage relevé (VDD 2, VDDIO 3, VREG 4, NRESET 7, MOTION 15, MOSI 16, SCLK 17, MISO 18, NCS 19, LED_N 20, masses 1 et 21, plot central 29 à la masse, autres broches non connectées) ; SPI à 2 MHz au plus ; VIL 0,3 x VDDIO et VIH 0,7 x VDDIO ; sorties MISO et MOTION : VOL 0,45 V à 1 mA ; 6 mA typique en marche, 12 µA à l'arrêt ; montée de l'alimentation de 0,15 à 20 ms avec 70 mA au plus ; 50 ms entre la remise à zéro et un mouvement valide ; une remise à zéro est obligatoire après une mise à l'arrêt ; schéma de référence (figure 7, et non figure 8) : voir DOU-205 « PMW3901MB : condensateurs du schéma de référence de la fiche et valeur illisible de R1 ». Toujours non trouvés dans cette fiche : les valeurs d'identité 0x49 et 0x5F (fiche générale, les registres sont dans une note d'application PixArt) et l'ordre de mise sous tension au-delà de VDDIO ≥ VDD. Reste ouvert.
**Décision liée :** DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour » ; DEC-289 « Fiches du 2026-11-04 : PMW3901MB, ferrite, diode SS34, buzzer et VL53L1 »

### DOU-186 — Fiche de la ferrite BLM18PG121SN1D absente du dossier des fiches
**Statut :** Levé
**Bloquant :** Non
**Concerne :** ARC-008 « Batterie et connecteur débranchable », DES-008 « Batterie, connecteur XT30 et entrée de la carte »
**Question :** la résistance continue de la ferrite (0,1 ohm de mémoire, 13 mV à 130 mA) et son courant nominal (1 A de mémoire) ne sont pas relevés : fiche absente du dossier.
**Réponse :** Levé le 2026-11-04 (fiche Murata JENF243A déposée dans `projets/boomrone/Datasheets/BLM18PG121SN1D.pdf`) : 120 ohms à 100 MHz (±25 %), courant nominal 2 000 mA à 85 °C et 1 000 mA à 125 °C, résistance continue 0,05 ohm initiale et 0,10 ohm au maximum après essais. Chute au pire de 13 mV à 130 mA (et 0,2 V à 2 A) : le calcul de DES-008 « Batterie, connecteur XT30 et entrée de la carte » est confirmé (la mémoire annonçait 0,1 ohm et 1 A).
**Décision liée :** DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour » ; DEC-289 « Fiches du 2026-11-04 : PMW3901MB, ferrite, diode SS34, buzzer et VL53L1 »

### DOU-187 — Fiche de la diode SS34 absente du dossier des fiches
**Statut :** Levé
**Bloquant :** Non
**Concerne :** ARC-007 « Étage de puissance des moteurs coupés par défaut », DES-007 « Circuit de puissance des moteurs », DES-011 « Circuit du voyant RGB et du buzzer »
**Question :** la tension directe, le courant admissible et le temps de recouvrement de la diode SS34 (roue libre des moteurs et du buzzer) ne sont pas relevés : fiche absente du dossier.
**Réponse :** Levé le 2026-11-04 (fiche onsemi SS32 à S310, `projets/boomrone/Datasheets/SS39-D.PDF`, rév. 5) : SS34 : 40 V de tenue inverse, 3,0 A en moyenne, 100 A en pointe non répétitive, tension directe de 0,5 V à 3,0 A (colonne commune SS32 à SS34), courant inverse de 0,5 mA à 25 °C, diode Schottky (conduction par porteurs majoritaires). Le courant de crête de 2,4 A par moteur est sous 3,0 A. Le temps de recouvrement n'est pas donné : sans objet pour une Schottky de roue libre.
**Décision liée :** DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour » ; DEC-289 « Fiches du 2026-11-04 : PMW3901MB, ferrite, diode SS34, buzzer et VL53L1 »

### DOU-188 — Fiche du buzzer SMD-9650-3327 absente du dossier des fiches
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-011 « Voyant RGB et avertisseur sonore », DES-011 « Circuit du voyant RGB et du buzzer »
**Question :** le courant (30 mA de mémoire), la fréquence propre (2,7 kHz de mémoire), la tension nominale et le niveau sonore du buzzer ne sont pas relevés : fiche absente du dossier.
**Réponse :** (à remplir) déposer la fiche ; la perceptibilité reste à vérifier à TS-014 « Perceptibilité et distinction des effets ». Non bloquant. Complément du 2026-11-04 : fiche du fabricant déposée (`projets/boomrone/Datasheets/SMD-9650-3327.pdf`) : tension nominale 3,3 V, courant 30 mA, niveau sonore 80 dB à 10 cm, fréquence propre 2 700 Hz, température de fonctionnement de -20 à 80 °C : les valeurs de mémoire sont confirmées. Restent illisibles dans l'extraction du texte : la tension de fonctionnement (indiquée « 25 », sans doute une plage) et le type du buzzer (la fiche parle de fréquence d'oscillation mesurée, ce qui suggère un buzzer actif à oscillateur intégré, à confirmer sur la page). Le niveau sonore à 3,0 V (au lieu de 3,3 V) est à vérifier à TS-014 « Perceptibilité et distinction des effets ». Reste ouvert.
**Décision liée :** DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour » ; DEC-289 « Fiches du 2026-11-04 : PMW3901MB, ferrite, diode SS34, buzzer et VL53L1 »

### DOU-189 — Fiche du bouton TS-1088-AR02016 absente du dossier des fiches
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-010 « Bouton », DES-010 « Circuit du bouton »
**Question :** le courant et la tension de contact, la durée des rebonds et l'empreinte du poussoir ne sont pas relevés : fiche absente du dossier (courant dans le contact de 0,27 mA calculé).
**Réponse :** (à remplir) déposer la fiche ; les rebonds sont absorbés par l'antirebond logiciel de 10 ms de DES-028 « Gestion logicielle du bouton ». Non bloquant.
**Décision liée :** DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour »

### DOU-190 — Fiche du moteur 8520 absente du dossier des fiches : courant de calage
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-006 « Moteurs, hélices et protège-hélices », ARC-007 « Étage de puissance des moteurs coupés par défaut », DES-007 « Circuit de puissance des moteurs »
**Question :** le courant de calage d'un moteur 8520 bloqué, son courant à vide et sa résistance de bobinage ne sont pas relevés : fiche absente du dossier ; le calcul de DES-007 « Circuit de puissance des moteurs » repose sur 2,4 A par moteur (9,5 A en crête). Point détaché de DOU-163 « Valeurs de fiche à relever : rappel de GPIO1, résistance de l'AO3400A, USB du G431 ».
**Réponse :** (à remplir) déposer la fiche ou mesurer le courant de calage au banc (TI-007 « Moteurs, poussée, masse et dimensions »). Non bloquant.
**Décision liée :** DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour »

### DOU-191 — Fiche de la batterie absente du dossier des fiches
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-008 « Batterie et connecteur débranchable », DES-008 « Batterie, connecteur XT30 et entrée de la carte »
**Question :** la fiche de la batterie 1S 850 mAh (décharge continue, résistance interne de 40 mohms estimée, genre et désignation du connecteur, tension maximale) n'est pas dans le dossier.
**Réponse :** (à remplir) déposer la fiche, mesurer la résistance interne à TI-008 « Batterie, connecteur, chute de tension et mesure de tension ». Non bloquant.
**Décision liée :** DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour »

### DOU-192 — Fiche du VL53L1CX absente du dossier des fiches
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-004 « Capteur de hauteur à temps de vol », DES-004 « Raccordement du capteur de hauteur VL53L1X », DOU-157 « VL53L1CX contre VL53L1X : identifiant, bibliothèque et registres »
**Question :** la fiche déposée est celle du VL53L1X : l'identifiant du VL53L1CX (composant de la nomenclature, VL53L1CXV0FY/1), ses registres et sa bibliothèque ne sont pas dans le dossier.
**Réponse :** (à remplir) déposer la fiche du VL53L1CX ; à traiter avec DOU-157 « VL53L1CX contre VL53L1X : identifiant, bibliothèque et registres ». Non bloquant. Complément du 2026-11-04 : la fiche déposée aujourd'hui est celle du VL53L1 (DS11786 rév. 16, référence VL53L1CBV0FY/1), pas celle du VL53L1CX : le doute reste ouvert (voir DOU-157 « VL53L1CX contre VL53L1X : identifiant, bibliothèque et registres »).
**Décision liée :** DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour » ; DEC-289 « Fiches du 2026-11-04 : PMW3901MB, ferrite, diode SS34, buzzer et VL53L1 »

### DOU-193 — Fiche du VL53L1X déposée sous la référence DS12385 au lieu de DS12093
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-004 « Capteur de hauteur à temps de vol », DES-004 « Raccordement du capteur de hauteur VL53L1X »
**Question :** le texte de DES-004 « Raccordement du capteur de hauteur VL53L1X » citait la fiche DS12093 de mémoire ; le fichier déposé porte DS12385 Rev 8 en pied de page. La référence est corrigée dans le DES et dans son schéma SVG. Cette fiche couvre-t-elle le VL53L1CX commandé, ou seulement le VL53L1X ?
**Réponse :** (à remplir) confirmer la référence de la fiche du composant commandé avec DOU-192 « Fiche du VL53L1CX absente du dossier des fiches ». Non bloquant. Complément du 2026-11-04 : le dossier contient aujourd'hui `DS_vl53l1.pdf` (DS11786 rév. 16, VL53L1) ; la fiche DS12385 rév. 8 du VL53L1X relevée le 2026-10-30 n'y est plus. Le doute reste ouvert.
**Décision liée :** DEC-280 « Capteurs : VL53L1X sans broche IOVDD, LSM6DSO et délai de mise en route » ; DEC-289 « Fiches du 2026-11-04 : PMW3901MB, ferrite, diode SS34, buzzer et VL53L1 »

### DOU-196 — LSM6DSO : durée du reset logiciel et départ du temps de mise en route non trouvés
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-003 « Centrale inertielle », DES-003 « Raccordement de la centrale inertielle LSM6DSO », DES-018 « Pilote de la centrale inertielle »
**Question :** la fiche DS12140 Rev 3 donne un temps de mise en route de 35 ms typique (tableau 3 p. 11) sans dire s'il court depuis la mise sous tension ou depuis un changement de débit de sortie, et ne donne pas la durée du reset logiciel (SW_RESET) : DES-018 « Pilote de la centrale inertielle » attend 40 ms après le reset du microcontrôleur puis au plus 20 ms après le reset logiciel (valeur du projet, non relevée).
**Réponse :** (à remplir) mesurer sur la première carte (premier accès SPI possible, durée de SW_RESET) ; garder les marges tant que non mesuré. Non bloquant.
**Décision liée :** DEC-280 « Capteurs : VL53L1X sans broche IOVDD, LSM6DSO et délai de mise en route »

### DOU-197 — ADC : attente du régulateur à confirmer et comportement si l'étalonnage échoue
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-009 « Alimentation de la logique et mesure de la tension », DES-022 « Pilote de la mesure de tension de la batterie », DES-031 « Séquence d'initialisation et échec d'initialisation »
**Question :** (1) la durée de démarrage du régulateur de l'ADC (tADCVREG_STUP, DS12589 p. 119) est ambiguë dans l'extraction du texte (2,0 ou 20 µs) ; DES-022 « Pilote de la mesure de tension de la batterie » attend 100 µs, au-dessus des deux ; (2) si l'étalonnage ne se termine pas en 1 ms, `vbat_valid` reste faux et `adc_cal_failed` est compté : l'effet sur l'initialisation (échec d'initialisation ou non) n'est pas défini par DES-031 « Séquence d'initialisation et échec d'initialisation ».
**Réponse :** (à remplir) lire la valeur sur le PDF ; décision de l'utilisateur sur le comportement en cas d'échec d'étalonnage (proposition : échec d'initialisation, comme une tension invalide). Non bloquant. Complément (relectures) : si `vbat_valid` reste faux de façon permanente, DES-029 « Surveillance et coupures automatiques » n'active pas la sous-tension et DES-031 « Séquence d'initialisation et échec d'initialisation » ne teste pas `vbat_valid` à l'étape 10 : le drone pourrait décoller sans protection de tension ; décision de l'utilisateur attendue avant l'implémentation de `app_init`.
**Décision liée :** DEC-281 « Puissance et alimentation : AO3400A, MCP1700, source de l'ADC et étalonnage »

### DOU-198 — Écarts avec l'architecture à reporter à la prochaine révision : débit, réveil du module, boîtier, désignation du XT30
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-002 « Microcontrôleur et programmation par liaison SWD », ARC-008 « Batterie et connecteur débranchable », ARC-012 « Module radio Bluetooth à basse consommation », ARC-016 « Pilotes des capteurs et des sorties », TI-010 « Liaison Bluetooth à basse consommation »
**Question :** l'architecture validée n'est pas modifiée, mais la conception détaillée s'en écarte sur quatre points : (1) ARC-012 « Module radio Bluetooth à basse consommation » et ARC-016 « Pilotes des capteurs et des sorties » parlent de 9600 bauds visés, le débit retenu est 19200 bauds ; (2) ARC-012 « Module radio Bluetooth à basse consommation » donne un boîtier de 22,3 x 14 mm (fiche : 14,6 x 21,9 mm) et dit que la broche d'état n'est pas utilisée sans traiter WKP, relié à PA1 ; ARC-002 « Microcontrôleur et programmation par liaison SWD » ne cite pas PA1 ; (3) ARC-008 « Batterie et connecteur débranchable » écrit XT30PW-M30.G.Y (fiche : XT30PW30-M.G.Y) ; (4) TI-010 « Liaison Bluetooth à basse consommation » est à compléter (WKP, 19200 bauds, rail de 3,0 V sous les 3,3 V de puissance garantie, mot de passe aérien) ; (5) sans objet : DEC-285 « WKP : PA1 conservée, résistance série de 0 Ω et emplacement de 0 Ω vers la masse non posé » (deux emplacements de 0 ohm sur WKP) est remplacée par DEC-286 « WKP : PA1 directe, emplacements de 0 Ω supprimés », PA1 est reliée directement à WKP, aucun composant de plus que l'architecture.
**Réponse :** (à remplir) reporter ces points dans l'architecture et dans TI-010 « Liaison Bluetooth à basse consommation » à la prochaine révision ; sans effet sur les REQ et les BES. Non bloquant. Complément (relectures) : ajouter aussi le diagramme d'ensemble de « Architecture » — `projets/boomrone/03-architecture.md` (UART 9600 à confirmer), ARC-025 « Protocole et service du statut sans fil » (9600 bauds visés), ARC-023 « Initialisation et échec d'initialisation » (reconnaissance de la mise sous tension par le marqueur seul, alors que DES-031 « Séquence d'initialisation et échec d'initialisation » ajoute BORRSTF ; 2,2 s contre 2,3 s) et ARC-009 « Alimentation de la logique et mesure de la tension » (repli à 3,0 V sous charge, lié à l'acceptation du BOR). Complément 2026-11-02 : le débit de 19200 bauds et le réveil du module (points 1 et 2) sont caducs depuis DEC-288 « Module radio : PB-03F à la place du E104-BT02 indisponible chez JLCPCB » (PB-03F : 115200 bauds, aucune broche de réveil) ; le boîtier et la désignation du XT30 restent à reporter.
**Décision liée :** DEC-277 « Module radio : 19200 bauds, réveil par PA1, broches du module et boîtier » ; DEC-282 « Voyant RGB, XC6206 et connecteur XT30 : valeurs de fiche »

### DOU-199 — AO3400A : résistance à 3,0 V et capacité d'entrée maximale non trouvées dans la fiche
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-007 « Étage de puissance des moteurs coupés par défaut », DES-007 « Circuit de puissance des moteurs »
**Question :** la fiche donne la résistance à VGS = 2,5 V et 4,5 V mais pas à 3,0 V (tension de grille réelle), la charge de grille à 3,0 V ni de valeur maximale de Ciss (630 pF typique seulement) : DES-007 « Circuit de puissance des moteurs » majore avec les valeurs à 2,5 V et le double du Ciss typique.
**Réponse :** (à remplir) mesure de l'échauffement des MOSFET à TI-005 « Moteurs coupés par le matériel » ou au banc ; aucune valeur inventée. Non bloquant.
**Décision liée :** DEC-281 « Puissance et alimentation : AO3400A, MCP1700, source de l'ADC et étalonnage »

### DOU-200 — PB-03F : mode transparent sans commande, microprogramme d'origine, débit et service Bluetooth
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-012 « Module radio Bluetooth à basse consommation », DES-012 « Raccordement du module Bluetooth PB-03F », DES-033 « Trames du statut sans fil, automate de réception et file d'émission », DES-036 « Logiciel de suivi en Python », TI-010 « Liaison Bluetooth à basse consommation »
**Question :** la fiche du PB-03F ne dit pas ce que fait le microprogramme livré : elle annonce des « commandes AT universelles » et un débit par défaut de 115 200 bauds. Un guide d'Ai-Thinker dit qu'après une connexion Bluetooth le mode transparent est actif par défaut (non vérifié pour le PB-03F). Le module est-il livré avec le microprogramme « combo AT » ? Transmet-il l'UART tel quel sans aucune commande ? Quels sont le format (8N1), le service et la caractéristique Bluetooth, et faut-il envoyer une commande à chaque démarrage (ce que ARC-012 « Module radio Bluetooth à basse consommation » refuse) ? Le service 0xFFF0 du E104-BT02 ne vaut plus.
**Réponse :** (à remplir) essai d'un module seul avec un adaptateur USB-UART en 3,3 V avant la commande de la carte (TI-010 « Liaison Bluetooth à basse consommation ») ; sources : fiche « PB-03F Specification V1.0.1 » et microprogramme « combo AT » de la page de la série PB d'Ai-Thinker. Si une configuration est nécessaire, décision à prendre (repli : E104-BT5010A, `AT+TRANMD=1`). Non bloquant.
**Décision liée :** DEC-288 « Module radio : PB-03F à la place du E104-BT02 indisponible chez JLCPCB »

### DOU-201 — PB-03F : source de plus de 200 mA en crête et rail de 3,0 V
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-012 « Module radio Bluetooth à basse consommation », ARC-009 « Alimentation de la logique et mesure de la tension », DES-009 « Régulateur de 3,0 V et pont de mesure de la tension »
**Question :** la fiche demande une alimentation d'au moins 200 mA, de préférence un régulateur linéaire ou un convertisseur indépendant, avec 3,3 V recommandé (plage 2,7 à 3,6 V). Le MCP1700 de DES-009 « Régulateur de 3,0 V et pont de mesure de la tension » fournit 250 mA avec 130 mA budgétés pour la logique ; le module consomme environ 12 mA en émission selon la fiche. La puissance d'émission est garantie à 3,3 V : à 3,0 V la portée change-t-elle ?
**Réponse :** (à remplir) mesure du courant de crête du module et de la portée à 3,0 V à TI-010 « Liaison Bluetooth à basse consommation ». Non bloquant.
**Décision liée :** DEC-288 « Module radio : PB-03F à la place du E104-BT02 indisponible chez JLCPCB »

### DOU-202 — PB-03F : circuit d'application, programmation du module et plots de test
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-012 « Module radio Bluetooth à basse consommation », DES-012 « Raccordement du module Bluetooth PB-03F », DES-013 « Implantation, routage et fichiers de fabrication pour JLCPCB »
**Question :** le circuit d'application de la fiche (p. 15) montre 10 µF + 100 nF sur l'alimentation, une diode de protection, deux résistances en série et deux rappels de 4,7 kΩ sur TX et RX, une broche de reset (P15, broche 1) avec un PMOS, et des plots pour une mise à jour par liaison série (P9, P10). Lesquels reprendre ? Faut-il des plots de test (3,0 V, masse, TX, RX, reset) pour mettre à jour le module hors du STM32 ? Le programmateur ST-LINK sait-il graver la puce PHY6252 par SWD (P2, P3) ? Rien n'est supposé.
**Réponse :** (à remplir) relecture de la figure 10 de la fiche et essai à TI-010 « Liaison Bluetooth à basse consommation » ; choix des composants à la phase de schéma KiCad. Non bloquant.
**Décision liée :** DEC-288 « Module radio : PB-03F à la place du E104-BT02 indisponible chez JLCPCB »

### DOU-203 — PB-03F sans broche de réveil : veille, reset en vol et état à la mise sous tension
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-012 « Module radio Bluetooth à basse consommation », DES-012 « Raccordement du module Bluetooth PB-03F », DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option »
**Question :** le PB-03F n'a pas de broche équivalente à WKP : le module reste-t-il éveillé en permanence, et avec quelle consommation ? Comment se comporte sa liaison série pendant un reset du microcontrôleur (broches analogiques) et à la mise sous tension (les rappels de 4,7 kΩ de la fiche aident-ils) ? Un reset en vol coupe-t-il toujours la connexion Bluetooth ? PA1 reste libre.
**Réponse :** (à remplir) essai du module seul et du module câblé (TI-010 « Liaison Bluetooth à basse consommation »). Non bloquant.
**Décision liée :** DEC-288 « Module radio : PB-03F à la place du E104-BT02 indisponible chez JLCPCB » ; DEC-286 « WKP : PA1 directe, emplacements de 0 Ω supprimés » (sans objet)

### DOU-204 — PB-03F : empreinte de 24 x 16 mm, antenne et masse
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-012 « Module radio Bluetooth à basse consommation », ARC-013 « Carte électronique JLCPCB, câblage et assemblage », ARC-014 « Bilan de masse, de poussée et d'autonomie », DES-013 « Implantation, routage et fichiers de fabrication pour JLCPCB »
**Question :** le module mesure 24,0 x 16,0 x 3,1 mm, 22 plots, antenne sur le module (fiche p. 5 et 10), contre 14,6 x 21,9 mm pour le E104-BT02. Tient-il en face haute de la carte de 40 x 35 mm avec l'antenne en dépassement de bord et sans métal autour (fiche p. 16) ? Sa masse n'est pas dans la fiche : le bilan de masse garde 1,0 g, valeur du E104-BT02, à peser.
**Réponse :** (à remplir) dessin de l'implantation (DES-013 « Implantation, routage et fichiers de fabrication pour JLCPCB ») et pesée du module reçu. Non bloquant. Complément du 2026-11-05 (essai du moteur de placement PCB) : l'utilisateur a précisé en chat que le module U7 entier (pas seulement l'antenne) déborde du bord ouest du contour testé (50 x 50 mm, voir DOU-162 « Implantation mécanique de la carte, du connecteur et de la batterie » pour la contradiction avec les 40 x 35 mm d'ARC-013 « Carte électronique JLCPCB, câblage et assemblage », à confirmer). Reste ouvert.
**Décision liée :** DEC-288 « Module radio : PB-03F à la place du E104-BT02 indisponible chez JLCPCB »

### DOU-208 — Phase des quatre sorties PWM de TIM1 : en phase ou décalées de 90°
**Statut :** Ouvert
**Bloquant :** Non
**Échéance :** implémentation
**Concerne :** ARC-007 « Étage de puissance des moteurs coupés par défaut », DES-007 « Circuit de puissance des moteurs », DES-021 « Pilotes des moteurs, du voyant, du buzzer et de la liaison série »
**Question :** la conception ne dit pas la phase relative des quatre sorties de TIM1 ; sur un même compteur elles sont en phase par défaut. La simulation SPICE (« Rapport de simulation SPICE » — `projets/boomrone/simulation/rapport-simulation-spice.html`, cas 1) donne sur la ligne moteurs VBATM 0,51 V crête-à-crête d'ondulation à 24 kHz en stationnaire avec des PWM en phase, contre 0,06 V avec un décalage de 90° entre voies ; le courant de la batterie passe de 10,5 à 2,5 A crête-à-crête. L'ondulation ne gêne pas l'ADC (filtre de 6 ms du pont de mesure, DES-009 « Régulateur de 3,0 V et pont de mesure de la tension »), mais elle sollicite les condensateurs de la ligne et le régulateur de 3,0 V. Faut-il décaler les phases, et TIM1 le permet-il (décalage des comparaisons ou mode centré) sans perdre la résolution du rapport cyclique de DES-026 « Contrôle de l'attitude et de la hauteur, mixeur et conversion en rapport cyclique » ?
**Réponse :** (à remplir) ondulation chiffrée avec un modèle de moteur en hypothèse (1 Ω, 25 µH, voir DOU-211 « Paramètres et modèles de la simulation SPICE : moteur, diode, ferrite et boucle des régulateurs ») : à confirmer par la mesure au banc ; le choix, s'il modifie DES-021 « Pilotes des moteurs, du voyant, du buzzer et de la liaison série », est une décision D2 de l'utilisateur après exposé des options.
**Décision liée :**

### DOU-209 — Marge de décrochage du régulateur de 3,0 V en crête et effondrement de +3V0 dans le cas pessimiste
**Statut :** Ouvert
**Bloquant :** Non
**Échéance :** essais sur prototype
**Concerne :** ARC-009 « Alimentation de la logique et mesure de la tension », DES-009 « Régulateur de 3,0 V et pont de mesure de la tension », REQ-012 « Coupure sur sous-tension de la batterie », DOU-135 « Faisabilité conjointe de la poussée, de la masse de 100 g, du capteur de hauteur, de la fabrication à la main et de la batterie »
**Question :** la simulation (« Rapport de simulation SPICE » — `projets/boomrone/simulation/rapport-simulation-spice.html`, cas 2) montre, avec les chiffres du bilan de « Architecture » : (1) à la crête de 9,5 A, VBATL descend à 3,12 V et, avec le décrochage maximal garanti du MCP1700 (350 mV à 250 mA, fiche DS20001826C p. 3), +3V0 tombe à 2,97 V en moyenne et 2,95 V au creux, soit environ 60 mV de marge sur les 2,91 V visés par DES-009 « Régulateur de 3,0 V et pont de mesure de la tension » ; (2) dans le cas pessimiste du bilan (7,5 A, 110 mΩ), VBATL descend à 2,68 V, le régulateur décroche et +3V0 vaut 2,77 V en moyenne avec un creux à 2,62 V et 0,33 V d'ondulation : le microcontrôleur serait en réinitialisation en vol. Les seuils d'armement et de coupure restent ceux de DEC-253 « Seuils de batterie conservés, sans mesures au banc pour la première version ». Le régulateur de repli ME6211C30M5G-N (décrochage à relever dans sa fiche) est-il à préférer, et le repli R1 + R2 de DEC-229 « Faisabilité conjointe : bilan, verdict marginal, mesures au banc avant la commande de la carte » est-il à déclencher ?
**Réponse :** (à remplir) mesure de la résistance interne de la batterie, du courant de crête et du creux de VBATL au banc avant la commande de la carte ; relever le décrochage du ME6211 dans sa fiche. Non bloquant seulement parce que DEC-253 « Seuils de batterie conservés, sans mesures au banc pour la première version » a déjà accepté ce risque pour la première version ; à reclasser bloquant si le banc donne plus de 60 mΩ.
**Décision liée :** DEC-253 « Seuils de batterie conservés, sans mesures au banc pour la première version »

### DOU-210 — Creux de +2V0 à l'impulsion de 70 mA de la mise sous tension du capteur de flux
**Statut :** Ouvert
**Bloquant :** Non
**Échéance :** essais sur prototype
**Concerne :** DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V », DOU-165 « Flux optique : alimentation en 2,0 V, valeurs de fiche et mise sous tension »
**Question :** la simulation (« Rapport de simulation SPICE » — `projets/boomrone/simulation/rapport-simulation-spice.html`, cas 3) donne, pour l'impulsion de 70 mA pendant 100 µs de DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V », un creux de +2V0 de 2,000 V à 1,952 V (−2,4 %), hors des 1,96 à 2,04 V de précision du XC6206P202MR-G. Ce creux dépend d'un modèle de boucle en hypothèse (DOU-211 « Paramètres et modèles de la simulation SPICE : moteur, diode, ferrite et boucle des régulateurs ») et la fiche du PMW3901MB (alimentation minimale à la mise sous tension) n'est pas dans le dossier (DOU-185 « Fiche du capteur de flux PMW3901MB absente du dossier des fiches »). Le capteur supporte-t-il ce creux, et la capacité de sortie de 2,2 µF suffit-elle ?
**Réponse :** (à remplir) mesure de +2V0 à l'oscilloscope sur prototype à la mise sous tension du capteur ; lire l'alimentation minimale du PMW3901MB dans sa fiche ; modèle SPICE ou courbe de charge dynamique du XC6206 si disponible. Non bloquant.
**Décision liée :**

### DOU-211 — Paramètres et modèles de la simulation SPICE : moteur, diode, ferrite et boucle des régulateurs
**Statut :** Ouvert
**Bloquant :** Non
**Échéance :** essais sur prototype
**Concerne :** DES-007 « Circuit de puissance des moteurs », DES-008 « Batterie, connecteur XT30 et entrée de la carte », DES-009 « Régulateur de 3,0 V et pont de mesure de la tension », DES-014 « Feuille de calcul du bilan de masse, de poussée et d'autonomie »
**Question :** le « Rapport de simulation SPICE » — `projets/boomrone/simulation/rapport-simulation-spice.html`, § 6, liste les valeurs d'entrée sans source (« HYP ») : résistance et inductance du moteur 8520 (1 Ω et 25 µH, DOU-190 « Fiche du moteur 8520 absente du dossier des fiches : courant de calage »), diode SS34 (Is, N, Rs, Cj), résistance de la ferrite (DOU-186 « Fiche de la ferrite BLM18PG121SN1D absente du dossier des fiches »), front de grille de 65 ns, ESR des condensateurs, et la dynamique de boucle des deux régulateurs au-delà de 100 Hz (gain de boucle 1,26 S, pôles à 1 et 3 MHz). Les chiffres du rapport ne valent que pour ces hypothèses ; les écarts entre cas sont plus fiables que les valeurs absolues. Aucune valeur ne doit entrer dans un élément « Validé » tant qu'elle n'est pas remplacée par une valeur sourcée.
**Réponse :** (à remplir) remplacer chaque hypothèse par une valeur de fiche, un modèle SPICE du fabricant (Microchip pour le MCP1700, Torex pour le XC6206, à chercher) ou une mesure au banc, puis relancer `projets/boomrone/simulation/sim_boomrone.py`. Non bloquant : la simulation est un contrôle, aucune exigence ni aucun élément de conception n'en dépend.
**Décision liée :**

### DOU-212 — Outil de simulation SPICE à retenir pour le cadre : ngspice, LTspice ou les deux
**Statut :** Ouvert
**Bloquant :** Non
**Échéance :** implémentation
**Concerne :** `modules/README.md` (liste des modules), « Rapport de simulation SPICE » — `projets/boomrone/simulation/rapport-simulation-spice.html`
**Question :** les deux outils donnent le même résultat sur les trois cas (rapport, § 1) : ondulation lissée de 0,509 V dans chacun, rejet d'ondulation identique à 10⁻⁵ dB près. LTspice est plus rapide (environ 1,5 fois) et s'installe en une commande ; ngspice est libre, portable (Linux, intégration continue) mais s'installe à la main sur ce poste sans droits administrateur (paquets MSYS2). Les scripts du projet sont dans `projets/boomrone/simulation/`. Faut-il en faire un module `modules/spice/` du cadre (rendu générique, sans donnée du projet écrite en dur), avec quel outil par défaut ?
**Réponse :** (à remplir) choix d'outil et de périmètre : décision D2 de l'utilisateur après exposé des options (jamais déléguée), à consigner en `DEC-xxx` ; les règles du cadre veulent qu'un script ne rejoigne un module que s'il est rendu générique.
**Décision liée :**

<!-- Ajouter les nouveaux doutes ci-dessus, avant ce marqueur, au même format, en dehors des blocs de code. -->

## Archive — doutes levés

### DOU-195 — Module E104-BT02 : niveau de WKP, état à la mise sous tension et mot de passe aérien
**Statut :** Levé
**Bloquant :** Non
**Concerne :** ARC-012 « Module radio Bluetooth à basse consommation », DES-012 « Raccordement du module Bluetooth PB-03F », DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option »
**Question :** (1) niveau « éveillé » de WKP (P06, broche 9) : présumé bas (rappel interne haut = veille par défaut selon le relevé), non démontré ; (2) comportement d'un WKP tenu bas dès la mise sous tension (non décrit) et valeur de PA1 pendant le reset du microcontrôleur (broche analogique, module en veille) ; (3) mot de passe aérien par défaut 123456 : toute personne à portée peut reconfigurer le module (le relevé propose la commande <UPDPWDxxx> au premier essai) ; (4) consommation en veille et éveillé.
**Réponse :** Sans objet depuis DEC-288 « Module radio : PB-03F à la place du E104-BT02 indisponible chez JLCPCB » : le PB-03F n'a pas de broche WKP ; son état à la mise sous tension et sa veille sont suivis par DOU-203 « PB-03F sans broche de réveil : veille, reset en vol et état à la mise sous tension ».
**Décision liée :** DEC-277 « Module radio : 19200 bauds, réveil par PA1, broches du module et boîtier » ; DEC-286 « WKP : PA1 directe, emplacements de 0 Ω supprimés »
 ; DEC-288 « Module radio : PB-03F à la place du E104-BT02 indisponible chez JLCPCB »



### DOU-194 — Fiche chinoise du E104-BT02 : relecture, tolérance d'horloge et niveaux d'entrée
**Statut :** Levé
**Bloquant :** Non
**Concerne :** ARC-012 « Module radio Bluetooth à basse consommation », DES-012 « Raccordement du module Bluetooth PB-03F »
**Question :** la fiche d'Ebyte est en chinois : le relevé a été fait par lecture des tableaux, sans relecture par une personne qui lit le chinois (points concernés : veille et WKP, commandes, débit, service). Non trouvés de façon sûre : tolérance de l'horloge du module (donc l'erreur de débit totale avec les ±1,75 % de la HSI16) et niveaux d'entrée VIL et VIH.
**Réponse :** Sans objet depuis DEC-288 « Module radio : PB-03F à la place du E104-BT02 indisponible chez JLCPCB » : le E104-BT02 (C411314) est remplacé par le PB-03F, dont la fiche est en anglais ; les points de la fiche du PB-03F sont suivis par DOU-200 « PB-03F : mode transparent sans commande, microprogramme d'origine, débit et service Bluetooth ».
**Décision liée :** DEC-277 « Module radio : 19200 bauds, réveil par PA1, broches du module et boîtier »
 ; DEC-288 « Module radio : PB-03F à la place du E104-BT02 indisponible chez JLCPCB »



### DOU-060 — Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol »
**Question :** Reste après DEC-097 « Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé » : que se passe-t-il si la batterie est coupée dans chacun des états du drone (allumé, série d'appuis, armé, lancé, en vol, mode réglage, vol de réglage, échec d'initialisation) ? Lecture implicite des réponses du 2026-10-28, à confirmer : toute coupure mène à « Éteint, moteurs arrêtés », puis au redémarrage selon DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation » (le mode réglage est perdu : sortie uniquement en enlevant la batterie, DEC-079 « Sortie du mode réglage : uniquement en enlevant la batterie »). Hypothèse à valider par l'architecture matérielle : l'alimentation des moteurs garantit leur arrêt lors d'un redémarrage ou d'une chute de tension. Précise SCN-011 « Dégradé : coupure d'alimentation en vol ».
Complément du 2026-10-28 (fusion du point « coupure d'alimentation en phase Lancé », qui complète aussi DOU-075 « Le chien de garde couvre-t-il la phase Lancé, et cette phase a-t-elle une durée maximale ? ») : que fait le drone si l'alimentation est coupée en phase « Lancé », entre le relâchement du bouton et le démarrage des moteurs, 200 ms plus tard (DEC-073 « Armé entre 2 et 10 secondes d'appui : le relâchement donne le signal Lancé, les moteurs démarrent 200 ms plus tard ») ? Hypothèse à confirmer : comme en vol (DEC-061 « Redémarrage immobile au sol : allumé mais jamais armé » ; DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie »), le drone redémarre, n'est jamais armé, donne « Échec d'initialisation » s'il est en mouvement et « Allumé » s'il est immobile, et ne démarre pas les moteurs seul. Une fois la réponse écrite, supprimer l'état « À définir : coupure en phase Lancé » du diagramme b et le renvoi « Coupure en phase Lancé » du diagramme a dans « Scénarios d'utilisation » — `projets/boomrone/00-scenarios.md`.
Complément du 2026-10-28 (rapport de la 4e relecture de porte, rattaché ici) : la condition « au sol » de DEC-061 « Redémarrage immobile au sol : allumé mais jamais armé » n'est pas reprise par DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation » (« immobile et à plat ») : un drone qui redémarre encore en l'air, en chute libre ou en train de tomber, est en mouvement et mène à « Échec d'initialisation », mais la durée d'initialisation, la lecture des capteurs en chute libre et un redémarrage répété en l'air ne sont pas décrits. Question : que fait le drone qui redémarre en l'air (chute libre, rebond, drone suspendu) ?
Échéance : porte « architecture » (pas d'échéance « avant les besoins »).
**Réponse :** Partielle, le doute reste ouvert. 2026-10-28 : pendant un redémarrage ou une chute de tension, y compris en phase « Lancé », les moteurs s'arrêtent et le drone est verrouillé (même état que « Allumé, en attente d'un appui »), puis redémarre selon la règle immobile et à plat ; hypothèse à valider par l'architecture matérielle (alimentation des moteurs). Source : réponse de l'utilisateur en chat, 2026-10-28. Phase exigences, 2026-10-29 : REQ-005 « Démarrage des moteurs sur geste volontaire seulement » et REQ-010 « Verrouillage après un posé, une coupure ou un redémarrage » exigent l'arrêt des moteurs et le verrouillage après toute coupure ; la façon de le garantir reste à valider à l'architecture matérielle. Échéance : architecture, non bloquant. Phase architecture, 2026-10-29 : garantie matérielle de l'arrêt des moteurs à tout reset, brown-out ou débranchement (rappel de grille de 100 kΩ, ARC-007 « Étage de puissance des moteurs coupés par défaut »), chien de garde matériel en cas de blocage (ARC-022 « Chien de garde »), redémarrage en l'air ou en chute libre = échec d'initialisation (ARC-023 « Initialisation et échec d'initialisation »). Hypothèse de l'alimentation des moteurs validée sur le papier ; vérifiée à TI-005 « Moteurs coupés par le matériel » et TI-006 « Coupures par chien de garde et par sous-tension du microcontrôleur ». Le mode réglage est perdu à la coupure (sortie seulement en débranchant).
**Décision liée :** DEC-231 « Garanties d'arrêt, batterie basse et consommation résiduelle : doutes levés »

### DOU-109 — Batterie déjà déchargée : redémarrages répétés, décharge profonde et état après une coupure logicielle
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-012 « Dégradé : sous-tension de la batterie »
**Question :** (1) Après une coupure sur sous-tension, la tension de la batterie remonte à vide : le drone redémarre-t-il alors avec une batterie encore déchargée (redémarrages répétés, décharge profonde : DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre », DEC-098 « Redémarrage après une coupure en vol : Allumé seulement si immobile et à plat, sinon échec d'initialisation ») ? (2) Que fait le drone quand on branche une batterie déjà sous le seuil de sous-tension (mise sous tension avec une batterie basse) : initialisation, « Allumé », coupure immédiate ? (3) Depuis DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension », la coupure est faite par le logiciel et laisse le microcontrôleur alimenté : le drone reste-t-il sous tension, verrouillé, ou s'éteint-il (état « Éteint » des diagrammes, DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre ») ? Quelle consommation résiduelle après la coupure ? (4) L'état « Échec d'initialisation » n'est pas listé parmi les états couverts par DEC-133 « SCN-012 inclut le drone laissé allumé en attente d'un appui : sous-tension dans le périmètre » : la sous-tension y est-elle couverte ?
**Réponse :** Phase exigences, 2026-10-29 : REQ-012 « Coupure sur sous-tension de la batterie » couvre la coupure sous le seuil sans hystérésis ; redémarrages répétés et décharge profonde restent à traiter. Échéance : architecture, non bloquant. Phase architecture, 2026-10-29 : après une sous-tension, état absorbant sans hystérésis, donc ni remontée de tension ni redémarrage répété ; une batterie déjà sous 3,3 V au branchement finit en échec d'initialisation ; le drone reste sous tension en échec (consommation : DOU-118 « Seuil de protection et consommation résiduelle du drone laissé allumé ») ; BOR niveau 3 (environ 2,5 V) pour ne pas bloquer le microcontrôleur en reset permanent.
**Décision liée :** DEC-231 « Garanties d'arrêt, batterie basse et consommation résiduelle : doutes levés »

### DOU-115 — Contenu et interruption de la réécriture de la zone des réglages par la reprogrammation
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-008 « Mise en service : programmation du drone » et SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Que contient la zone des réglages sauvegardés : seulement des réglages de vol, ou aussi une calibration propre à chaque drone (décalages de capteurs), qui serait effacée à chaque reprogrammation ? Que devient le cas « mémoire jamais écrite » (DEC-130 « Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté ») après DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine » ? Que se passe-t-il si la programmation ou la réécriture de la zone est interrompue, et reste-t-elle rejouable ? La reprogrammation est le recours de quatre risques acceptés de `projets/boomrone/risques-acceptes.md`. Ouvert le 2026-10-29 (5e relecture de porte, `critique`).
**Réponse :** Phase exigences, 2026-10-29 : REQ-028 « Valeurs d'origine après la programmation » exige les valeurs d'origine après programmation ; le contenu de la zone et l'interruption de la programmation restent à traiter. Échéance : architecture, non bloquant. Phase architecture, 2026-10-29 : la zone des réglages contient seulement les 4 paramètres de vol (un mot de 64 bits dans la dernière page de flash) ; aucune calibration par drone, le biais du gyroscope est mesuré à chaque initialisation. Les valeurs d'origine font partie de l'image programmée : toute programmation les réécrit ; une programmation interrompue se rejoue ; une valeur hors bornes revient à la valeur d'origine du paramètre. Vérifié à TI-024 « Paramètres, flash et programmation ».
**Décision liée :** DEC-227 « Réglages : page de flash de l'image, valeurs hors bornes, sauvegarde au sol »

### DOU-118 — Seuil de protection et consommation résiduelle du drone laissé allumé
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-012 « Dégradé : sous-tension de la batterie »
**Question :** Le drone laissé allumé en attente d'un appui est dans le périmètre (DEC-133 « SCN-012 inclut le drone laissé allumé en attente d'un appui : sous-tension dans le périmètre »). Faut-il un seuil de protection de la batterie distinct du seuil de vol pour éviter la décharge profonde ? Après une coupure logicielle, le microcontrôleur et la radio continuent de consommer : quelle borne de décharge ? Complète DOU-109 « Batterie déjà déchargée : redémarrages répétés, décharge profonde et état après une coupure logicielle ». Ouvert le 2026-10-29 (5e relecture de porte, `critique`).
**Réponse :** Phase exigences, 2026-10-29 : aucune exigence de seuil de protection distinct n'est posée (simplicité, risque de la ligne 17 de « Risques acceptés ») ; la consommation résiduelle reste à traiter. Échéance : architecture, non bloquant. Note du 2026-10-29 (DEC-216 « Fusions de simplicité et sous-tension en échec d'initialisation : retouches finales de la porte exigences ») : après une sous-tension, le drone encore alimenté reste en échec d'initialisation (effet lumineux ou sonore, radio) et continue de consommer jusqu'au débranchement ; consommation à traiter en architecture avec ce doute. Phase architecture, 2026-10-29 : pas de seuil de protection distinct (simplicité, risque de la ligne 17 de « Risques acceptés »). En échec d'initialisation par sous-tension : capteurs en veille, horloge à 16 MHz, voyant faible, radio active, environ 12 mA (estimation), soit 1,4 à 2,8 h avant 3,0 V par élément ; la page de consignes dit de débrancher. Consommation à mesurer sur prototype ; risque accepté.
**Décision liée :** DEC-231 « Garanties d'arrêt, batterie basse et consommation résiduelle : doutes levés »

### DOU-120 — Écriture en mémoire sous tension basse ou pendant une phase de vol
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-012 « Dégradé : sous-tension de la batterie »
**Question :** Sous le seuil de sous-tension, le microcontrôleur peut rester alimenté à l'état Allumé, où Sauvegarder est acceptée : une écriture à tension limite risque de corrompre la mémoire (DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension » avec DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture »). Une écriture déjà en cours au franchissement du seuil, ou au relâchement du lancer (DEC-136 « Écriture de réglages commencée à l'état Allumé et encore en cours au relâchement du lancer : risque accepté »), est-elle évitée par une règle d'architecture (garde de tension avant toute écriture, verrou d'appui tant qu'une écriture est en cours) ? Ouvert le 2026-10-29 (5e relecture de porte, `critique`).
**Réponse :** Phase exigences, 2026-10-29 : réduit par DEC-177 « Simplification n°4 adoptée : commandes sans fil acceptées seulement en mode réglage » (Sauvegarder n'est acceptée qu'en mode réglage au sol, jamais en vol) ; reste à décider une garde de tension avant écriture. Relecture de porte, 2026-10-29 : une écriture en mémoire plus longue que la durée de blocage du logiciel de 200 ms (REQ-014 « Coupure sur logiciel bloqué ») risquerait de déclencher la coupure ; l'architecture doit découper l'écriture ou la protéger de cette coupure, sans changer la valeur de 200 ms. Échéance : architecture, non bloquant. Phase architecture, 2026-10-29 : Sauvegarder n'est acceptée qu'en mode réglage au sol, moteurs coupés, batterie d'au moins 3,5 V ; l'écriture (effacement de page 22 à 40 ms) dure environ 45 ms, sous les 100 ms du chien de garde (rafraîchi avant et après), donc sans conflit avec les 200 ms de REQ-014 « Coupure sur logiciel bloqué » ; la réception radio continue en DMA. Aucune écriture en vol.
**Décision liée :** DEC-227 « Réglages : page de flash de l'image, valeurs hors bornes, sauvegarde au sol »

### DOU-136 — Ordre de livraison : exigence essentielle dépendant du mode réglage souhaitable
**Statut :** Levé
**Bloquant :** Non
**Concerne :** REQ-005 « Démarrage des moteurs sur geste volontaire seulement » et REQ-041 « Conditions d'acceptation de la commande Décoller »
**Question :** REQ-005 « Démarrage des moteurs sur geste volontaire seulement » (Essentiel) cite le démarrage des moteurs sur une commande Décoller acceptée, qui appartient au mode réglage (REQ-041 « Conditions d'acceptation de la commande Décoller », Souhaitable). Le plan de livraison doit-il livrer le mode réglage avec le vol normal, ou la règle reste-t-elle vraie avec le seul premier cas, le mode réglage venant après ? Ouvert le 2026-10-29 (relecture de la porte « exigences »). Échéance : architecture (plan de livraison).
**Réponse :** Note de livraison écrite dans REQ-005 « Démarrage des moteurs sur geste volontaire seulement » : la règle reste vraie avec le seul premier cas ; à confirmer au plan de livraison. Phase architecture, 2026-10-29 : plan de livraison en trois jalons (ARC-029 « Plan de livraison par jalons ») ; REQ-005 « Démarrage des moteurs sur geste volontaire seulement » est vraie avec son seul premier cas jusqu'à la livraison du mode réglage (J3), les valeurs fixes de REQ-026 « Paramètres de vol réglables » sont des constantes dès J1.
**Décision liée :** DEC-230 « Plan de livraison par jalons, ordre de livraison levé »


### DOU-127 — Couverture ligne à ligne des risques acceptés par les consignes d'emploi
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-012 « Disposer d'une page de consignes d'emploi »
**Question :** BES-012 « Disposer d'une page de consignes d'emploi » exige que la page rappelle chacun des risques de la liste « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (35 risques), alors que la page « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md` est courte (une consigne par ligne, regroupée par moment). La vérification par inspection ligne à ligne reste à faire ; tout risque sans consigne est à ajouter ou à retirer du besoin. Échéance : phase « exigences » (exigence et recette de BES-012 « Disposer d'une page de consignes d'emploi »). Ouvert le 2026-10-29 (reformulation de BES-012 « Disposer d'une page de consignes d'emploi », DEC-158 « Énoncés des besoins resserrés : une intention, testable, sans solution »).
**Réponse :** La page n'a pas à reprendre chaque ligne : elle rappelle les risques majeurs et ceux qui demandent un geste de l'utilisateur, l'inspection est un contrôle croisé avec la liste des risques acceptés. Décidé par l'architecte par délégation explicite de l'utilisateur, 2026-10-29.
**Décision liée :** DEC-167 « BES-012 : contrôle croisé, consignes complétées, DOU-127 levé » ; DEC-162 « Consignes d'emploi : une consigne par ligne, les dangers en tête »

### DOU-132 — Liste des paramètres de vol réglables et leurs valeurs d'origine
**Statut :** Levé
**Bloquant :** Non
**Concerne :** REQ-026 « Paramètres de vol réglables » et REQ-028 « Valeurs d'origine après la programmation »
**Question :** Quels paramètres de vol sont réglables par la commande Modifier (au moins un), et quelle est la valeur d'origine de chacun ? La liste dépend des choix de commande du vol, donc de l'architecture. Échéance : architecture.
**Réponse :** Liste fixée à quatre paramètres (gain d'inclinaison 1,0 ; gain de hauteur 1,0 ; hauteur visée du stationnaire 1,0 m ; vitesse de descente 0,2 m/s), valeurs d'origine provisoires à valider aux essais (REQ-026 « Paramètres de vol réglables »). Décidé par l'architecte par délégation explicite de l'utilisateur, 2026-10-29.
**Décision liée :** DEC-201 « Quatre paramètres de vol réglables, valeurs d'origine provisoires : DOU-132 levé » ; DEC-180 « Simplification n°7 adoptée : valeurs de sécurité fixes dans le logiciel »

### DOU-134 — Drone tenu en main au-dessus de la hauteur minimale et critère de stationnaire
**Statut :** Levé
**Bloquant :** Non
**Concerne :** REQ-007 « Critère de vol stationnaire » et SCN-002 « Échec : stationnaire non atteint dans le délai »
**Question :** SCN-002 « Échec : stationnaire non atteint dans le délai » dit qu'un drone tenu immobile en main n'atteint pas le stationnaire. Or le critère de REQ-007 « Critère de vol stationnaire » (inclinaison, vitesse, hauteur d'au moins 0,3 m) est vrai pour un drone tenu à la main à hauteur de poitrine, immobile et à plat. Faut-il une condition de plus (par exemple poussée des moteurs trop faible pour le poids, ou hauteur qui ne change pas malgré la poussée), ou accepte-t-on qu'un drone tenu en main soit déclaré en stationnaire (risque de la ligne 26 de « Risques acceptés ») ? Échéance : architecture et essais.
**Réponse :** Limite assumée : un drone tenu en main à plus de 0,3 m, immobile et à plat, peut se croire en vol stationnaire ; le critère de REQ-007 « Critère de vol stationnaire » est inchangé, la limite est dans « Risques acceptés » et « Consignes d'emploi ». Décidé par l'architecte par délégation explicite de l'utilisateur, 2026-10-29.
**Décision liée :** DEC-196 « Drone tenu en main à plus de 0,3 m : limite assumée, DOU-134 levé » ; DEC-049 « Stationnaire déclaré seulement en l'air, au-dessus d'une hauteur minimale »

### DOU-009 — Quelle tolérance d'altitude pendant les 10 secondes de stationnaire ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** « Il maintient son altitude » pendant 10 s : quelle variation d'altitude est acceptable (par exemple ± 10 cm) ? À lever avant la porte « exigences », car l'exigence doit être chiffrée. Voir aussi DOU-002 « Que veut dire ne pas dériver horizontalement ? » pour la dérive horizontale.
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Hauteur tenue pendant les 10 s : 1,0 m, tolérance ±0,2 m, de la 3e à la 10e seconde (provisoire, à valider aux essais).
**Décision liée :** DEC-009 « Stationnaire atteint en 2 secondes maximum après le démarrage des moteurs » ; DEC-184 « Valeurs du vol : lancer, stationnaire, hauteur, dérive, atterrissage »

### DOU-010 — Quelle rotation au lancer le drone doit-il rattraper ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Un lancer à la main fait souvent tourner le drone sur lui-même. Jusqu'à quelle rotation (en tours par seconde) l'utilisateur s'attend-il à ce que le vol réussisse ? À lever avant la porte « exigences ».
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Rotation à rattraper au lancer : jusqu'à 1 tour par seconde (360 °/s) au relâchement (provisoire, à valider aux essais).
**Décision liée :** DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » ; DEC-184 « Valeurs du vol : lancer, stationnaire, hauteur, dérive, atterrissage »

### DOU-011 — Quelle dérive horizontale reste acceptable si 30 cm n'est pas tenu ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** L'objectif de 30 cm sur 10 s n'est pas garanti. Si les essais montrent une dérive plus grande, jusqu'où l'utilisateur l'accepte-t-il dans une pièce d'appartement (par exemple 1 m, 2 m) ? Au-delà, revoit-on l'objectif ou le produit ?
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Dérive exigée : 1,0 m sur 10 s ; l'objectif de 30 cm est mesuré et consigné sans valeur d'acceptation (provisoire).
**Décision liée :** DEC-011 « Dérive de 30 cm sur 10 s en objectif à valider par essais » ; DEC-184 « Valeurs du vol : lancer, stationnaire, hauteur, dérive, atterrissage »

### DOU-012 — Quel angle limite et quelles autres valeurs de coupure retenir ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Question :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » retient 60° à titre provisoire. Quel angle, et quelle durée au-delà de laquelle on coupe (pour éviter une coupure sur une perturbation brève) ? À lever avant la porte « exigences ».
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Angle limite 60° (±5°) pendant plus de 0,1 s après le stationnaire, coupure 100 ms au plus après la détection ; valeurs fixes dans le logiciel (provisoire).
**Décision liée :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » ; DEC-185 « Valeurs de coupure : basculement, pas de limite de dérive ni d'altitude »

### DOU-013 — Quelle durée de vol garantit-on après un armement accepté ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-003 « Échec : batterie faible à l'armement » et SCN-012 « Dégradé : sous-tension de la batterie »
**Question :** Après un armement accepté, le vol (jusqu'à environ 27 s : 2 s de stabilisation, 10 s de stationnaire, 15 s de descente au plus) doit aller à son terme sans contrôle de la batterie en vol. Quelle marge de durée attend-on (par exemple deux fois la durée du vol) ? À lever avant la porte « exigences ». Complément du 2026-10-28 : la durée de vol garantie est reliée à SCN-012 « Dégradé : sous-tension de la batterie » : la coupure sur sous-tension en vol est assumée par le logiciel (DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension », qui modifie DEC-013 « Pas de contrôle de la batterie en vol »), et le seuil d'armement doit rester au-dessus du seuil de sous-tension ; la marge de durée dépend donc de l'écart entre les deux seuils (DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture » ; DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs »).
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Après un armement accepté (3,7 V par élément à vide), un vol complet de 30 s doit aller à son terme sans passer sous 3,3 V par élément (provisoire, à valider aux essais).
**Décision liée :** DEC-013 « Pas de contrôle de la batterie en vol » ; précisé par DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension » ; DEC-186 « Valeurs de batterie : seuils par élément, confirmation, vol complet »

### DOU-028 — Faut-il une limite de dérive avant la coupure, entre 10° et 60° d'inclinaison ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-006 « Échec : inclinaison excessive après le stationnaire »
**Question :** Entre le stationnaire (< 10°) et la coupure à 60° (DEC-012 « Couper les moteurs si le drone bascule après le stationnaire »), un drone à 45° peut dériver de plusieurs mètres vers un mur ou une personne sans coupure. Faut-il une distance ou une durée maximale ? Élargit DOU-012 « Quel angle limite et quelles autres valeurs de coupure retenir ? ».
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Aucune limite de dérive ni coupure entre 15° et 60° : risque accepté, ligne 37 de « Risques acceptés » et consigne.
**Décision liée :** DEC-012 « Couper les moteurs si le drone bascule après le stationnaire » ; DEC-185 « Valeurs de coupure : basculement, pas de limite de dérive ni d'altitude »

### DOU-029 — Quelle altitude maximale et quel plafond le drone doit-il tolérer ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** À 4 m/s vers le haut, le drone peut atteindre un plafond en 0,5 s. Quelle altitude maximale vise-t-on, et que se passe-t-il en cas de contact avec le plafond (DEC-014 « Pas de coupure sur choc en vol ») ? Voir DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol ».
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Aucune limite d'altitude ni réaction au plafond : risque accepté (hauteur de stationnaire 1,0 m ; lancer adapté au lieu par l'utilisateur).
**Décision liée :** DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol » ; DEC-185 « Valeurs de coupure : basculement, pas de limite de dérive ni d'altitude »

### DOU-035 — Quelle hauteur de stationnaire vise-t-on ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Aucun scénario ne fixe la hauteur du stationnaire, en vol normal comme en vol de réglage. Elle dépend de la hauteur de lancer, et elle fixe la durée de la descente à 0,5 m/s (DEC-021 « Atterrissage lent, 15 secondes maximum, puis coupure des moteurs »). Quelle hauteur vise-t-on, ou quelle plage ? À lever avant la porte « exigences ».
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Hauteur de stationnaire visée : 1,0 m (provisoire, à valider aux essais).
**Décision liée :** DEC-184 « Valeurs du vol : lancer, stationnaire, hauteur, dérive, atterrissage »

### DOU-058 — Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Les valeurs d'origine du drone neuf (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ») et d'éventuelles bornes numériques sont renvoyées à l'architecture par DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ». Les fixer en phase architecture, avec les essais. Complément de la relecture de porte (critique) : « bornes numériques » contredit en apparence DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » (« aucune borne ») et DEC-045 « Seuils de sécurité réglables comme le reste, sans borne » (bornes écartées). Lecture proposée, à faire confirmer par l'utilisateur : il s'agit seulement des limites de représentation (type de donnée, par exemple un entier sur 16 bits), et non de bornes de sécurité. Complément du 2026-10-28 (fusion) : la tolérance de mouvement (vitesse, rotation) de « immobile » pour l'armement, le mode réglage et le redémarrage (reste de DOU-073 « Que veut dire immobile pour armer un drone tenu en main, et quel signal si l'armement est refusé ? », DEC-110 « Armement refusé à 2 secondes d'appui : tous les tests faits, un seul signal Refus, sans attente de l'immobilité ») ; la durée de conservation du statut de refus sur le sans fil, et son extension éventuelle aux refus d'armement et de mode réglage (DEC-102 « Décollage de réglage refusé : signal Refus, statut de refus lisible jusqu'à la commande suivante ») ; la durée perceptible de l'effet local de la cause d'une coupure avant le relais de « Allumé » (DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil ») ; le seuil de batterie du décollage de réglage (DEC-108 « Vols de réglage répétés : aucune limite de nombre ni contrôle de chauffe, risque accepté ») ; la durée de la garde du bouton et la durée maximale de la phase « Lancé » (notes d'architecture) ; dire si le délai de 15 secondes après le décollage de réglage est le délai de descente réglable (DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement »). Complément du 2026-10-28 (extraction) : la tolérance de « immobile » pour l'armement sur un drone tenu en main (faisabilité du cas nominal) est extraite dans DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal », avec une échéance avant la phase « besoins » ; la tolérance pour le mode réglage et le redémarrage reste ici. Complément du 2026-10-28 (réponses de l'utilisateur) : (1) échéance « avant les besoins » pour la part qui conditionne la faisabilité des scénarios, c'est-à-dire la tolérance de « immobile » et la plage de lancer ; le reste (valeurs d'origine, bornes numériques, durées de garde, de refus, seuils) reste à fixer en architecture ; portée exacte de l'échéance à confirmer (DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir ») ; (2) la durée perceptible de l'effet local de la cause d'une coupure avant le relais d'« Allumé » est supprimée de ce doute : aucune durée minimale (DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté »). Complément du 2026-10-28 (réponses de l'utilisateur) : s'ajoutent à fixer en architecture le seuil de sous-tension de la batterie (DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre », SCN-012 « Dégradé : sous-tension de la batterie ») et la durée du signal de l'événement (Posé, Refus, Désarmement) avant le relais du signal « Allumé » (DEC-118 « Signal Allumé au retour à l'attente après un posé, un refus ou un désarmement »). Complément du 2026-10-28 (rapport de la 4e relecture de porte, rattaché ici et non ouvert à part) : durée minimale de perception des signaux d'événement (« Refus », « Désarmement », « Posé ») avant le relais du signal « Allumé » (DEC-118 « Signal Allumé au retour à l'attente après un posé, un refus ou un désarmement », SCN-003 « Échec : batterie faible à l'armement », SCN-005 « Dégradé : bouton maintenu plus de 10 secondes », SCN-001 « Vol nominal : de la batterie au posé ») : si le relais est immédiat, le signal de l'événement peut ne pas être perçu ; la cause d'une coupure en vol, elle, n'a aucune durée minimale (DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté ») ; la durée est à fixer en architecture. Complément du 2026-10-28 : le seuil de sous-tension est le seuil de la coupure par le logiciel (DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension ») ; son rapport au seuil d'armement est le sujet de DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs ». Complément du 2026-10-29 (5e relecture) : l'échéance « avant les besoins » est abandonnée, validation par essais sur prototype (DEC-137 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : jalon déplacé aux essais, plage de lancer inchangée » et DEC-138 « Tolérance d'immobile et part de DOU-058 liée à la faisabilité : jalon déplacé aux essais »).
**Réponse :** Partielle, le doute reste ouvert. 2026-10-27 : DEC-051 « Seuils de sécurité réglables dans des bornes fixées par le logiciel » rend les bornes des seuils de sécurité obligatoires (délai de 2 s, angle limite, délai de descente de 15 s, seuil de batterie, hauteur minimale dont la borne est strictement supérieure à 0) ; leurs valeurs sont à fixer ici, en architecture. La contradiction relevée par la critique est résolue pour les seuils de sécurité : ils sont bornés. Pour les autres réglages, qui restent sans borne (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal »), il ne s'agit que de limites de représentation. Restent à fixer : les valeurs d'origine et les valeurs numériques des bornes. Phase exigences, 2026-10-29, par délégation de l'utilisateur : Bornes numériques sans objet (valeurs de sécurité fixes) ; durées et seuils fixés par DEC-182 « Valeurs du bouton : 1 s, 2 s, 10 s, anti-rebond, garde, délai des moteurs », DEC-183 « Valeurs de départ : immobile, à plat, batterie à l'armement », DEC-184 « Valeurs du vol : lancer, stationnaire, hauteur, dérive, atterrissage », DEC-185 « Valeurs de coupure : basculement, pas de limite de dérive ni d'altitude », DEC-186 « Valeurs de batterie : seuils par élément, confirmation, vol complet » et DEC-187 « Valeurs du cadre d'emploi : poche, protège-hélices, pièce d'essai » ; durée perceptible des effets d'événement 0,5 s (DEC-176 « Simplification n°3 adoptée : dix effets locaux au lieu de dix-sept signaux ») ; tolérance d'immobile provisoire écrite, validation par DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal » ; liste et valeurs d'origine des paramètres réglables renvoyées à l'architecture (DOU-132 « Liste des paramètres de vol réglables et leurs valeurs d'origine »).
**Décision liée :** DEC-138 « Tolérance d'immobile et part de DOU-058 liée à la faisabilité : jalon déplacé aux essais » (part liée à DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir » : tolérance de « immobile » et plage de lancer, reportées aux essais ; le reste en architecture) ; DEC-180 « Simplification n°7 adoptée : valeurs de sécurité fixes dans le logiciel »

### DOU-080 — Seuils de temps du bouton : 1 s, 2 s, 10 s et délai entre appuis
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Valeurs provisoires à fixer en architecture et à confirmer avant la porte « exigences » (DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences ») : 1 s pour l'appui validé (DEC-070 « Appui validé : bouton maintenu 1 seconde, rien en dessous, plus de signal Appui trop court »), 2 s pour l'armement (DEC-072 « Armement à 2 secondes d'appui : signal Prêt, ou signal unique Armement refusé selon l'état du drone »), 10 s pour le désarmement (DEC-054 « Chrono de 10 secondes compté depuis l'appui initial »), et le délai d'environ 2 s entre appuis d'affilée (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »), avec sa tolérance et son origine (fin du relâchement ou début du nouvel appui). Depuis DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série », le délai d'environ 2 s fixe aussi la durée pendant laquelle l'armement est impossible après un appui validé relâché.
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Seuils du bouton retenus (provisoires) : 1 s, 2 s, 10 s ; le délai entre appuis est sans objet (série d'appuis supprimée).
**Décision liée :** DEC-052 « Valeurs provisoires retenues pour les scénarios, à confirmer avant les exigences » ; DEC-182 « Valeurs du bouton : 1 s, 2 s, 10 s, anti-rebond, garde, délai des moteurs » ; DEC-175 « Simplification n°2 adoptée : mode réglage par le bouton tenu à la mise sous tension »

### DOU-108 — Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-012 « Dégradé : sous-tension de la batterie » et SCN-003 « Échec : batterie faible à l'armement »
**Question :** DEC-004 « Batterie vérifiée à l'armement : pas d'armement si batterie faible » refuse l'armement sous un seuil mesuré à vide (DEC-018 « Jamais de réarmement automatique ; batterie mesurée à vide à l'armement »), et DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension » coupe les moteurs sous le seuil de sous-tension (voir DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre », DEC-013 « Pas de contrôle de la batterie en vol »). Le seuil d'armement doit rester au-dessus du seuil de sous-tension, mais de combien ? La tension d'une batterie s'affaisse sous la charge du démarrage des moteurs (200 ms après le relâchement) : une batterie acceptée à vide à l'armement peut-elle franchir le seuil de sous-tension dès le démarrage des moteurs, ou en vol ? Les valeurs des deux seuils, la marge et la mesure (à vide, sous charge) sont à fixer en architecture, avec DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture ».
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Seuil d'armement 3,7 V par élément à vide, seuil de sous-tension 3,3 V par élément sous charge, confirmé 100 ms ; marge vérifiée par un vol complet de 30 s sur le banc (provisoire).
**Décision liée :** DEC-186 « Valeurs de batterie : seuils par élément, confirmation, vol complet »

### DOU-111 — Niveau ou front du bouton à l'acceptation de Décoller
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-007 « Dégradé : arrêt d'urgence par le bouton en vol »
**Question :** En vol de réglage le bouton est pris en compte tout de suite, sans garde (DEC-094 « Bouton appuyé après un décollage de réglage : pris en compte tout de suite, sans garde », DEC-077 « Bouton appuyé en vol de réglage : arrêt d'urgence, moteurs coupés, le drone reste en mode réglage »), alors qu'au sol en mode réglage il n'a aucun effet (DEC-116 « Bouton en mode réglage, moteurs coupés : aucun effet et aucun signal, il ne sert qu'en vol de réglage ») et qu'un maintien hérité du 3e appui est ignoré jusqu'au premier relâchement (DEC-115 « Troisième appui encore maintenu à l'entrée en mode réglage : maintien ignoré jusqu'au premier relâchement »). Si le bouton est déjà enfoncé quand le drone accepte Décoller et passe en vol de réglage (appui commencé au sol et maintenu), est-ce un arrêt d'urgence immédiat (niveau), ou faut-il un nouvel appui (front) ? Les règles ne disent pas si le bouton est lu au niveau ou au front à cet instant.
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Un appui commencé avant l'acceptation de Décoller est ignoré jusqu'à son premier relâchement : il faut un nouvel appui (front).
**Décision liée :** DEC-188 « Bouton : un appui commencé avant une coupure ou un décollage est ignoré jusqu'au relâchement »

### DOU-112 — Bouton enfoncé jusqu'à la fin de l'initialisation : état et signal
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-001 « Vol nominal : de la batterie au posé »
**Question :** DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement » fait ignorer un bouton enfoncé à la mise sous tension jusqu'au premier relâchement, et DEC-088 « Bouton coincé ou maintenu en permanence au démarrage : statut sans fil seulement, aucun signal local » ne donne qu'un statut sans fil « bouton maintenu » pour un bouton coincé. Si le bouton est encore enfoncé à la fin d'une initialisation réussie : dans quel état est le drone (sous-état « Bouton à relâcher » de « Allumé, en attente d'un appui » ?) et le signal « Allumé » est-il donné à ce moment ou au relâchement ? Le chemin est une lacune du diagramme a et de SCN-010 « Échec : initialisation impossible au démarrage » ; l'arête « Bouton enfoncé, ignoré jusqu'au relâchement » y a été ajoutée d'après DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement », sans signal précisé.
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Bouton encore enfoncé à la fin d'une initialisation réussie : le drone entre en mode réglage (effet Mode réglage) ; en échec d'initialisation, l'effet Échec d'initialisation.
**Décision liée :** DEC-175 « Simplification n°2 adoptée : mode réglage par le bouton tenu à la mise sous tension »

### DOU-113 — Ordre entre Modifier pendant l'initialisation et chargement des réglages enregistrés
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil » et SCN-010 « Échec : initialisation impossible au démarrage »
**Question :** Modifier est acceptée pendant l'initialisation en cours (DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées », DEC-120 « Sauvegarder ignorée pendant l'initialisation en cours, Modifier acceptée ; cas de l'échec d'initialisation non tranché ») et le drone charge ses réglages enregistrés au démarrage (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage »). Si une valeur modifiée arrive avant la fin du chargement, laquelle l'emporte : la valeur modifiée, ou la valeur enregistrée qui l'écrase ? L'acquittement de la commande par le statut sans fil (DEC-107 « Vol de réglage : signaux des phases du vol normal, acquittement des commandes par le statut sans fil seulement ») ne dit pas si la valeur a été conservée.
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Sans objet : toutes les commandes sans fil sont ignorées pendant l'initialisation.
**Décision liée :** DEC-177 « Simplification n°4 adoptée : commandes sans fil acceptées seulement en mode réglage »

### DOU-114 — Réglages enregistrés chargés ou non à l'état d'échec d'initialisation
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage »
**Question :** À l'état « Échec d'initialisation », Modifier et Sauvegarder sont acceptées (DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté », DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées »). Les réglages enregistrés sont-ils chargés à cet état, ou le drone garde-t-il ses valeurs d'origine ? Question restée hors de la réponse de DOU-098 « Commande Sauvegarder après un échec d'initialisation : acceptée ou ignorée » et seulement notée dans `notes-architecture.md` ; elle détermine ce qu'une commande Sauvegarder écrit (valeurs non chargées, valeurs d'origine) et la portée du risque de la ligne 11 de « Risques acceptés » — `projets/boomrone/risques-acceptes.md`.
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Sans objet : toutes les commandes sans fil sont ignorées en échec d'initialisation ; aucun vol n'est possible.
**Décision liée :** DEC-178 « Simplification n°5 adoptée : échec d'initialisation, toutes les commandes sans fil ignorées »

### DOU-117 — Cause de sous-tension sur le statut sans fil
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-012 « Dégradé : sous-tension de la batterie »
**Question :** SCN-012 « Dégradé : sous-tension de la batterie » dit « aucun signal propre » et ne mentionne pas le statut sans fil. La cause « sous-tension » est-elle conservée sur le statut sans fil comme les autres causes de coupure (DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil »), pour qu'un appareil de suivi la distingue d'un arrêt d'urgence ? Ouvert le 2026-10-29 (5e relecture de porte, `critique`).
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : La cause « sous-tension » fait partie des six valeurs de la dernière cause de coupure du statut sans fil, quand le drone reste alimenté.
**Décision liée :** DEC-179 « Simplification n°6 adoptée : statut sans fil par code d'état et dernières causes »

### DOU-119 — Filtrage, hystérésis et mesure sous charge de la tension
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-012 « Dégradé : sous-tension de la batterie »
**Question :** DEC-134 « Coupure sur sous-tension en vol assumée par le logiciel : le drone surveille la tension » : quelle durée de confirmation avant de couper, quelle hystérésis et quelle mesure sous charge, pour qu'un affaissement bref (pic de courant, bruit de mesure) ne coupe pas un vol sain sans retarder la coupure d'une vraie sous-tension ? Complète DOU-108 « Rapport entre le seuil d'armement et le seuil de sous-tension, affaissement de tension au démarrage des moteurs », à rattacher aux durées de DOU-058 « Valeurs d'origine, bornes numériques, tolérance d'immobile et durées à fixer en architecture ». Ouvert le 2026-10-29 (5e relecture de porte, `critique`).
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Confirmation de 100 ms (±20 ms) avant la coupure, sans hystérésis, tension lue en continu y compris moteurs en marche (provisoire).
**Décision liée :** DEC-186 « Valeurs de batterie : seuils par élément, confirmation, vol complet »

### DOU-126 — Simplifications possibles des scénarios : choix de l'utilisateur
**Statut :** Levé
**Bloquant :** Non
**Concerne :** « Besoins » — `projets/boomrone/01-besoins.md`, section « Annexe B — Simplifications possibles »
**Question :** Six complexités des scénarios validés restent proposées au retrait pour un drone plus simple (n°2 à n°7 de « Annexe B — Simplifications possibles ») : série de trois appuis, dix-sept signaux, états de Sauvegarder, commandes après échec d'initialisation, cause précise sur le sans fil, bornes des seuils. La n°1 (retirer tout le sans fil de réglage et de suivi) est écartée, ce qui rend recommandées les cinq lignes qu'elle aurait fait disparaître. Elles sont toutes recommandées. L'utilisateur en retient-il certaines ? Échéance : avant la porte « exigences » ; chaque retrait passerait par une décision et une modification explicite du scénario concerné.
**Réponse :** partielle, utilisateur, chat, 2026-10-29 : « on garde la communication sans fils » ; simplification n°1 écartée (SCN-009 « Réglage et suivi du drone par le sans fil », BES-008 « Entrer en mode réglage et faire des vols de réglage », BES-009 « Régler et sauvegarder les paramètres de vol », BES-010 « Suivre le drone sur un appareil de suivi » conservés). Les six autres restent à décider. Phase exigences, 2026-10-29, par délégation de l'utilisateur : Les six simplifications (n°2 à n°7) sont adoptées par délégation de l'utilisateur.
**Décision liée :** DEC-155 « Scénarios inchangés : les complexités inutiles sont notées en simplifications possibles » ; DEC-160 « Cadrage des besoins : contraintes du projet et simplification n°1 recommandée » ; DEC-163 « Communication sans fil conservée : simplification n°1 écartée » ; DEC-168 « Annexe B des besoins : quatre colonnes, simplifications n°2 à n°7 recommandées » ; DEC-181 « Simplifications de l'annexe B tranchées : DOU-126 levé »

### DOU-128 — Durée minimale perceptible des signaux
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-007 « Savoir où en est le drone sans autre appareil »
**Question :** BES-007 « Savoir où en est le drone sans autre appareil » exige que chaque signal soit perceptible par l'utilisateur. Sans durée minimale par signal (lumière, son), l'exigence n'est pas testable, d'autant que le signal « Allumé » prend le relais tout de suite après une coupure en vol (DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté »). Quelle durée minimale, pour quels signaux ? Échéance : phase « exigences ». Ouvert le 2026-10-29 (seconde relecture de porte, DEC-164 « Seconde relecture de porte : énoncés des besoins repris »).
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Effets d'événement perceptibles au moins 0,5 s, à 1 m, lumière à environ 300 lux, son moteurs arrêtés ; effets d'état tant que l'état dure.
**Décision liée :** DEC-176 « Simplification n°3 adoptée : dix effets locaux au lieu de dix-sept signaux »

### DOU-129 — Plage de lancer et hauteur d'un appartement (plafond)
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-013 « Voler en appartement avec un drone de poche protégé »
**Question :** La plage de lancer (de 0,5 à 4 m/s depuis au moins 1,5 m du sol) et la hauteur d'un plafond d'appartement sont-elles compatibles, compte tenu de la hauteur de stationnaire visée ? Voir aussi DOU-029 « Quelle altitude maximale et quel plafond le drone doit-il tolérer ? » et DOU-035 « Quelle hauteur de stationnaire vise-t-on ? ». Échéance : phase « exigences » et essais sur prototype. Ouvert le 2026-10-29 (seconde relecture de porte, DEC-164 « Seconde relecture de porte : énoncés des besoins repris »).
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : Pas de limite imposée au drone : l'utilisateur adapte le lancer au lieu ; essai d'appartement en lancer doux dans une pièce de 3 m × 3 m × 2,5 m.
**Décision liée :** DEC-185 « Valeurs de coupure : basculement, pas de limite de dérive ni d'altitude »

### DOU-130 — Arrêt d'un drone en vol par le bouton sans le toucher
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-006 « Arrêter le drone en vol d'un geste » et « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md`
**Question :** Le bouton est sur le drone : l'arrêt en vol par le bouton oblige à toucher un drone aux hélices en rotation. Faut-il une option d'arrêt sans fil (BES-010 « Suivre le drone sur un appareil de suivi ») ? Échéance : exigences. En attendant, la consigne dit d'appuyer avec prudence (DEC-170 « Consigne d'arrêt en vol par le bouton : formulation prudente »).
**Réponse :** Phase exigences, 2026-10-29, par délégation de l'utilisateur : L'arrêt sans fil existe (Souhaitable) ; sans appareil de suivi, seul le bouton arrête, avec prudence ; aucune autre option.
**Décision liée :** DEC-170 « Consigne d'arrêt en vol par le bouton : formulation prudente » ; DEC-189 « Arrêt d'un drone en vol : bouton ou arrêt sans fil, pas d'autre option »

### DOU-110 — La reprogrammation efface-t-elle la zone des réglages sauvegardés ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-008 « Mise en service : programmation du drone » et SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule » et DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » désignent la reprogrammation comme seul recours contre des réglages aberrants, corrompus ou écrasés. La reprogrammation efface-t-elle (ou réécrit-elle avec les valeurs d'origine) la zone des réglages sauvegardés ? Sinon, quatre risques de « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (lignes 20, 24, 33 et 34), dont le seul recours est la reprogrammation, n'ont plus de recours. Échéance : avant la phase « besoins » (demandée à l'architecte le 2026-10-28 ; DEC-122 « Jalon avant les besoins : promesse de l'architecte, sans modification de l'outil de porte » ne nomme pas ce doute, à confirmer à la porte). Voir aussi la vérification demandée en architecture dans `notes-architecture.md`.
**Réponse :** Oui : la reprogrammation réécrit la zone des réglages sauvegardés avec les valeurs d'origine du logiciel (réponse de l'utilisateur en chat, 2026-10-28, option recommandée). Les réglages sauvegardés sont donc perdus à chaque reprogrammation.
**Décision liée :** DEC-139 « Reprogrammation : réécriture de la zone des réglages avec les valeurs d'origine »

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
**Précision postérieure :** le point « drone laissé allumé » n'est plus hors périmètre : sa sous-tension est décrite par SCN-012 « Dégradé : sous-tension de la batterie » (DEC-133 « SCN-012 inclut le drone laissé allumé en attente d'un appui : sous-tension dans le périmètre », le 2026-10-28) ; la charge, le remplacement et le stockage restent hors périmètre.

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

### DOU-062 — Où l'utilisateur est-il informé des limites d'emploi ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Où l'utilisateur est-il informé des limites d'emploi : plage de lancer (DEC-010 « Plage de lancer : toute orientation, 0,5 à 4 m/s, au moins 1,5 m du sol »), lieu (DEC-040 « Périmètre d'emploi visé : l'appartement ; gymnase et jardin en essais complémentaires », DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur », DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu ») ? Notice, étiquette, ou rien ? Complément du 2026-10-28 (réponses de la dernière série de décisions) : cinq risques acceptés s'ajoutent à la liste de `reprise.md` : écriture de réglages sur un drone non initialisé (DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées ») ; pas de limite du nombre de vols de réglage ni de contrôle de chauffe (DEC-108 « Vols de réglage répétés : aucune limite de nombre ni contrôle de chauffe, risque accepté ») ; lancer hors plage ou hauteur impossible à mesurer = échec de stabilisation (DEC-109 « Lancer hors plage ou hauteur non mesurable : échec de stabilisation, limite d'emploi ») ; pas d'action particulière si le lien sans fil est perdu en vol de réglage, l'arrêt sans fil n'atteignant plus le drone (DEC-106 « Lien sans fil perdu en vol de réglage : aucune action particulière ») ; cause d'une chute non conservée en local, lisible seulement sur le statut sans fil (DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil »). Complément du 2026-10-28 (réponses de l'utilisateur) : s'ajoutent à la liste de `reprise.md` : (a) batterie lithium : charge et stockage hors périmètre, à la charge de l'utilisateur ; (b) drone laissé allumé : décharge de la batterie, risque de décharge profonde ; (c) programmation : hélices à démonter, programmation interrompue et essai des moteurs avant le premier vol non couverts (DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter ») ; (d) la commande « Sauvegarder » ignorée à l'état armé ne donne aucun signal local, l'acquittement se lit sur le statut sans fil (DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer ») ; (e) cause d'une coupure : l'utilisateur sans appareil de suivi n'est pas informé de la cause, risque confirmé (DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté »). La reprogrammation et le contrôle de version sont à confirmer comme hors périmètre.
**Réponse :** Les limites d'emploi sont informées par une notice écrite à la phase « besoins », qui reprend `risques-acceptes.md` ; le drone n'affiche rien lui-même, hors statut sans fil. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-125 « Limites d'emploi informées par une notice écrite à la phase besoins, le drone n'affiche rien »

### DOU-097 — Bouton encore maintenu à l'entrée en mode réglage (3e appui)
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Le 3e appui est validé après 1 s d'appui : le bouton peut encore être enfoncé à l'entrée en mode réglage (DEC-085 « Entrée en mode réglage : drone immobile et à plat, non armé, sans condition de posé »). Est-il ignoré jusqu'au relâchement, ou pris en compte tout de suite (en mode réglage, le bouton n'arme jamais : DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage » ; aucun appui de la série ne peut armer : DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série ») ? Cas à relier à DEC-094 « Bouton appuyé après un décollage de réglage : pris en compte tout de suite, sans garde » (bouton pris en compte tout de suite après un décollage de réglage, sans garde) : une commande Décoller reçue pendant que le bouton est encore maintenu coupe-t-elle les moteurs aussitôt ? Cas voisin traité pour un refus : DEC-093 « Mode réglage refusé : retour à l'attente, compteur à zéro, bouton encore enfoncé ignoré ».
**Réponse :** Au 3e appui (entrée en mode réglage) encore maintenu, le maintien est ignoré jusqu'au premier relâchement, comme un bouton déjà enfoncé (DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement ») ; il ne peut ni armer ni déclencher d'arrêt après un Décoller. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-115 « Troisième appui encore maintenu à l'entrée en mode réglage : maintien ignoré jusqu'au premier relâchement »

### DOU-099 — Paramètres de vol sans borne : modification en vol et sauvegarde par un tiers
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Les paramètres de vol n'ont aucune borne et sont modifiables aussi en vol normal (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal ») ; sans appairage, un tiers à portée peut les modifier (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »), sans contrôle d'intégrité des commandes (DEC-066 « Commande sans fil corrompue : aucun contrôle d'intégrité »), puis les sauvegarder (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » : pas de retour aux valeurs d'origine). Précision à confirmer : d'après le tableau des commandes (DEC-043 « Commandes sans fil acceptées selon l'état du drone »), Modifier est acceptée en vol, Sauvegarder est ignorée en vol et acceptée au sol. Faut-il lister ce risque dans les limites d'emploi (DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? »), le limiter, ou les deux ?
Complément du 2026-10-28 (3e relecture de porte) : des paramètres de vol aberrants, sauvegardés par un tiers, sont rechargés à chaque démarrage (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage ») sans retour aux valeurs d'origine (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »), sans borne (DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal »), sans contrôle d'intégrité (DEC-066 « Commande sans fil corrompue : aucun contrôle d'intégrité ») et sans appairage (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée »). Comment le propriétaire récupère-t-il un drone dont les réglages sauvegardés l'empêchent de voler normalement : par la reprogrammation seule (SCN-008 « Mise en service : programmation du drone »), ou autrement ? Ce risque est-il à inscrire dans la liste des risques acceptés de `reprise.md` (voir DOU-102 « Registre consolidé des risques acceptés ») ?
**Réponse :** Risque accepté et documenté : des paramètres de vol aberrants envoyés et sauvegardés par un tiers sont rechargés à chaque démarrage ; seule la reprogrammation du drone rétablit les valeurs. Limite d'emploi à inscrire (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée », DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal », DEC-066 « Commande sans fil corrompue : aucun contrôle d'intégrité », DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-121 « Paramètres de vol aberrants envoyés et sauvegardés par un tiers : risque accepté, reprogrammation seule »

### DOU-100 — Appui bref pendant la garde du bouton, relâché avant la fin, hélices tournantes en main
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-002 « Échec : stationnaire non atteint dans le délai »
**Question :** Pendant la garde qui suit le lancer, la garde ignore les fronts et prend en compte le niveau à sa fin (DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement »). Un utilisateur qui a relâché le bouton sans lancer, hélices tournantes en main (DEC-017 « Pas de protection supplémentaire contre les hélices en rotation sans lancer »), appuie brièvement puis relâche avant la fin de la garde : l'appui n'a aucun effet et les hélices continuent de tourner. Ce cas est-il accepté ?
**Réponse :** Risque accepté et documenté : l'appui bref relâché avant la fin de la garde n'a aucun effet ; DEC-092 « Garde du bouton après le lancer : fronts ignorés, niveau pris en compte, démarrage au relâchement » reste inchangée. Limite d'emploi : tenir le bouton jusqu'à la fin de la garde. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-119 « Appui bref pendant la garde du bouton, relâché avant la fin : risque accepté et documenté »

### DOU-102 — Registre consolidé des risques acceptés
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-001 « Vol nominal : de la batterie au posé »
**Question :** Les quinze risques acceptés de `reprise.md` (dont trois ajoutés le 2026-10-28 : batterie lithium, drone laissé allumé, programmation) ne couvrent pas : DEC-057 « Pas de détection dédiée d'un drone attrapé ou posé sur un obstacle », DEC-060 « Défaillance d'un capteur ou d'un moteur en vol : hors périmètre », DEC-063 « Choc contre un obstacle ou un plafond : aucune réaction dédiée », DEC-013 « Pas de contrôle de la batterie en vol », DEC-014 « Pas de coupure sur choc en vol », DEC-066 « Commande sans fil corrompue : aucun contrôle d'intégrité », DEC-041 « Lancer hors plage ou trop rapide pour la zone : responsabilité de l'utilisateur » et DEC-042 « Plage de lancer inchangée, aucune zone libre ni distance aux personnes, le drone ne connaît pas le lieu ». Autres décisions à examiner pour le registre : DEC-032 « Vol libre : le drone vole sans appareil de suivi », DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée », DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal », DEC-056 « Armement : drone immobile, sans autotest », DEC-039 « Réglages : coupures valables en vol de réglage, aucune borne, modifiables aussi en vol normal » et DEC-045 « Seuils de sécurité réglables comme le reste, sans borne ». Où tient le registre consolidé des risques acceptés, avec quel périmètre (toutes les décisions « risque accepté ») et quel lien avec DOU-062 « Où l'utilisateur est-il informé des limites d'emploi ? » (où l'utilisateur est informé des limites d'emploi) ?
**Réponse :** Un fichier dédié, `projets/boomrone/risques-acceptes.md`, consolide les risques acceptés (les quinze de `reprise.md` et ceux du journal qui n'y figuraient pas) ; `reprise.md` y renvoie. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-124 « Registre consolidé des risques acceptés dans un fichier dédié »

### DOU-103 — Signal Allumé après Posé, Refus et Désarmement : donné au retour à l'attente ou silencieux ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-005 « Dégradé : bouton maintenu plus de 10 secondes »
**Question :** Le signal « Allumé » est défini à la mise sous tension et comme relais après une coupure en vol (DEC-104 « Cause d'une coupure en vol : signal local non conservé, Allumé prend le relais, cause conservée sur le statut sans fil »). Après un « Posé » (DEC-023 « Après le posé ou une coupure : drone verrouillé, nouvel appui pour revoler »), un « Refus » (DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté ») et un « Désarmement » (DEC-080 « Armement refusé ou désarmement : retour à l'attente, compteur à zéro, l'appui long n'est pas compté »), le drone revient à « Allumé, en attente d'un appui » (DEC-047 « L'état verrouillé est le même que l'état allumé, en attente d'un appui », DEC-082 « Retours à l'attente après le posé ou une coupure des moteurs : compteur à zéro, appui en cours ni pris en compte ni compté ») : le signal « Allumé » est-il donné à ce retour à l'attente, ou le drone reste-t-il silencieux ?
**Réponse :** Au retour à l'attente après un posé, un refus ou un désarmement, le signal « Allumé » est donné : il prend le relais après le signal de l'événement, comme après une coupure en vol (DEC-113 « Cause d'une coupure en vol : confirmation, Allumé tout de suite, aucune durée minimale, risque accepté »). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-118 « Signal Allumé au retour à l'attente après un posé, un refus ou un désarmement »

### DOU-104 — Jalon avant les besoins non contrôlé par l'outil de porte
**Statut :** Levé
**Bloquant :** Non
**Concerne :** DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » et DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal »
**Question :** DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » et DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal » doivent être levés avant la phase « besoins », mais restent non bloquants pour la porte « scénarios » (DEC-114 « Faisabilité du stationnaire en 2 secondes depuis 1,5 m : analyse avant les besoins, plage de lancer à revoir »). L'outil `tools/check_traceability.py --gate` ne bloque que sur « Bloquant : Oui » : rien n'empêche donc techniquement d'ouvrir les besoins. Comment tenir ce jalon : marquer ces doutes bloquants, ajouter à l'outil une option de phase (échéance par doute), ou accepter la promesse de l'architecte sans contrôle outillé ?
**Réponse :** Le jalon reste une promesse de l'architecte, inscrite dans une décision : l'architecte n'ouvre pas la phase « besoins » tant que DOU-050 « Mesure de vitesse horizontale et faisabilité du stationnaire en 2 s depuis 1,5 m » et DOU-101 « Tolérance d'immobile à l'armement sur un drone tenu en main : faisabilité du cas nominal » sont ouverts ; l'outil n'est pas modifié. Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-122 « Jalon avant les besoins : promesse de l'architecte, sans modification de l'outil de porte »

### DOU-105 — Bouton en mode réglage, moteurs coupés : comportement autre que ne jamais armer
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Seul « le bouton n'arme jamais en mode réglage » est écrit (DEC-071 « Appuis validés d'affilée : trois appuis entrent en mode réglage sans armer, le bouton n'arme jamais en mode réglage »). Dans l'état « Mode réglage, moteurs coupés », que fait le bouton : un appui est-il validé à 1 s avec le signal « Appui validé » ? un signal est-il donné à 2 s, ou à 10 s ? un 4e appui d'affilée compte-t-il ? un appui maintenu est-il ignoré ou sans effet ? Complète DOU-097 « Bouton encore maintenu à l'entrée en mode réglage (3e appui) » (qui ne traite que l'entrée) sans le fusionner.
**Réponse :** En « Mode réglage, moteurs coupés » (au sol), le bouton n'a aucun effet et ne donne aucun signal ; il ne sert plus qu'en vol de réglage (arrêt d'urgence). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-116 « Bouton en mode réglage, moteurs coupés : aucun effet et aucun signal, il ne sert qu'en vol de réglage »

### DOU-106 — Bouton en échec d'initialisation après un premier relâchement
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-011 « Dégradé : coupure d'alimentation en vol »
**Question :** SCN-010 « Échec : initialisation impossible au démarrage » et SCN-011 « Dégradé : coupure d'alimentation en vol » disent que le drone en échec d'initialisation ignore le bouton, alors que la note du diagramme a et DEC-059 « Bouton déjà enfoncé : ignoré jusqu'au premier relâchement » l'ignorent seulement jusqu'au premier relâchement. Après ce premier relâchement, le bouton reste-t-il ignoré pour toujours (échec définitif jusqu'au débranchement : DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie ») ou seulement jusqu'au premier relâchement ? Un appui de 2 s en échec d'initialisation donne-t-il le signal « Refus », ou rien ?
**Réponse :** En « Échec d'initialisation », après un premier relâchement, le bouton est ignoré pour toujours : aucun effet, aucun signal (échec définitif, DEC-075 « Initialisation en échec : définitive jusqu'au débranchement de la batterie »). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-117 « Bouton en échec d'initialisation : ignoré pour toujours après le premier relâchement, aucun effet ni signal »

### DOU-107 — Exigences sans scénario amont : protections de la batterie, sous-tension, brown-out, CEM
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-011 « Dégradé : coupure d'alimentation en vol »
**Question :** La batterie est hors périmètre des scénarios (DEC-111 « Batterie et programmation : hors périmètre des scénarios, limites d'emploi à documenter ») et la règle de la phase 0 impose qu'un besoin cite au moins un scénario. Des exigences que l'architecture matérielle peut imposer (protections matérielles de la batterie, détection de sous-tension, brown-out du microcontrôleur, CEM) n'auraient alors aucun scénario amont. Comment les tracer : par un scénario, par une contrainte, ou par une exception de méthode consignée ? Voir DEC-097 « Redémarrage ou chute de tension, même en phase Lancé : moteurs arrêtés, drone verrouillé » et DOU-060 « Coupure de la batterie dans chaque état du drone, et alimentation des moteurs à valider en architecture matérielle ».
**Réponse :** Un scénario court de protection de la batterie est créé : SCN-012 « Dégradé : sous-tension de la batterie » (protection de sous-tension seulement ; surintensité, inversion de polarité et surchauffe non retenues, à voir en architecture). L'utilisateur avait d'abord proposé « contraintes hors scénario », puis, après rappel de la règle « chaque besoin cite au moins un scénario », a choisi « Non, un scénario court ». Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-126 « Protection de sous-tension de la batterie : scénario court, coupure sans signal propre »

### DOU-098 — Commande Sauvegarder après un échec d'initialisation : acceptée ou ignorée
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-010 « Échec : initialisation impossible au démarrage »
**Question :** Reste après DEC-120 « Sauvegarder ignorée pendant l'initialisation en cours, Modifier acceptée ; cas de l'échec d'initialisation non tranché » : à l'état « Échec d'initialisation », Sauvegarder reste acceptée à ce jour (DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées », inchangée pour cet état). Les réglages enregistrés sont-ils chargés à cet état ? Si non, Sauvegarder peut écraser des réglages enregistrés par des valeurs d'origine ou incomplètes (DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée »), et un tiers à portée peut envoyer la commande (DEC-037 « Pas d'appairage : le drone obéit à tout appareil de suivi à portée ») : perte persistante des réglages. Sauvegarder est-elle acceptée ou ignorée à cet état ? Seul ce reste est ouvert.
**Réponse :** Acceptée. À l'état « Échec d'initialisation », Sauvegarder reste acceptée (DEC-105 « Initialisation en cours et échec d'initialisation : Modifier et Sauvegarder acceptées, Décoller et Arrêt ignorées » inchangée pour cet état) ; le risque d'écraser les réglages enregistrés par des valeurs non chargées, déclenché par un tiers à portée, est accepté explicitement et documenté dans « Risques acceptés » — `projets/boomrone/risques-acceptes.md` (limite d'emploi). L'utilisateur avait vu l'option « Ignorée (recommandée) » et a choisi « Acceptée ». Reste hors question, laissé à l'architecture : les réglages enregistrés sont-ils chargés à cet état ? Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-127 « Sauvegarder acceptée à l'état Échec d'initialisation : écrasement des réglages par un tiers, risque accepté »

### DOU-059 — Sauvegarde des réglages : écriture en vol, coupure pendant l'écriture, mémoire jamais écrite
**Statut :** Levé
**Bloquant :** Non
**Concerne :** SCN-009 « Réglage et suivi du drone par le sans fil »
**Question :** Sauvegarde des réglages (DEC-034 « Réglages envoyés par le sans fil, sauvegarde sur commande, chargement au démarrage ») : la commande de sauvegarde est-elle acceptée en vol ? Que se passe-t-il si la batterie est coupée pendant l'écriture ? Comment détecter une mémoire « jamais écrite » (DEC-036 « Drone neuf : valeurs d'origine fixes du logiciel, sans signal ») sans contrôle d'intégrité, alors que DEC-035 « Pas de retour aux valeurs d'origine ; mémoire corrompue non traitée » écarte la détection de corruption ? Complément de la relecture de porte (critique) : « Sauvegarder » est acceptée à l'état « Armé, avant le lancer » (DEC-043 « Commandes sans fil acceptées selon l'état du drone ») ; une écriture en mémoire non volatile en cours peut-elle retarder le démarrage des moteurs au lancer, prévu 200 ms après le relâchement (DEC-006 « Le relâchement du bouton armé suffit à démarrer les moteurs ») ? Complément du 2026-10-28 : « Sauvegarder » est désormais ignorée à l'état « Armé, avant le lancer » (DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer », qui modifie DEC-095 « Commande Sauvegarder à l'état armé : acceptée, retard possible du lancer accepté comme risque » et DEC-043 « Commandes sans fil acceptées selon l'état du drone ») ; reste à traiter en architecture une écriture commencée avant l'armement (état « Allumé ») et encore en cours au relâchement du bouton, qui pourrait dépasser la durée maximale de la phase « Lancé ». Précision du 2026-10-28 (3e relecture de porte) : la fenêtre d'écriture dangereuse inclut l'état « Premier appui validé », seul état d'où l'armement est possible (DEC-076 « Armement possible seulement depuis le premier appui d'une série, sans effet du maintien pendant la série ») : « Sauvegarder » y est acceptée (état inclus dans « Allumé, en attente d'un appui », tableau de DEC-043 « Commandes sans fil acceptées selon l'état du drone »). Question complémentaire : « Sauvegarder » doit-elle aussi être ignorée dans l'état « Premier appui validé », comme à l'état armé (DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer »), ou l'écriture en cours à l'armement est-elle traitée autrement en architecture ? Complément du 2026-10-28 (réponse de l'utilisateur) : « Sauvegarder » est aussi ignorée à l'état « Premier appui validé » (fenêtre de maintien de 1 à 2 s) : DEC-123 « Sauvegarder ignorée aussi à l'état Premier appui validé », qui étend DEC-112 « Sauvegarder ignorée à l'état armé, avant le lancer ». Restent ouverts pour ce doute : l'écriture en vol, la coupure pendant l'écriture, la mémoire jamais écrite, une écriture commencée à l'état « Allumé » et encore en cours à l'armement. **Non tranché :** l'état « Série d'appuis en cours » (au moins un appui validé relâché, moins de 2 s écoulées, aucun appui ne peut armer) : Sauvegarder y reste acceptée à ce jour.
**Réponse :** (a) Sauvegarder est aussi ignorée à l'état « Série d'appuis en cours » (comme « Premier appui validé » et « Armé ») ; (b) coupure de la batterie pendant l'écriture : risque accepté, à traiter en architecture (choix de mémoire ou séquence d'écriture), sans contrôle d'intégrité ; (c) mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté ; (d) Sauvegarder ignorée en vol (déjà dans le tableau de DEC-043 « Commandes sans fil acceptées selon l'état du drone », vérifié). Reste à couvrir en architecture (point nommé dans DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture », sans réponse propre de l'utilisateur) : une écriture commencée à l'état « Allumé » et encore en cours à l'armement (voir DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture »). Source : réponse de l'utilisateur en chat, 2026-10-28.
**Décision liée :** DEC-128 « Sauvegarder ignorée aussi à l'état Série d'appuis en cours » ; DEC-129 « Coupure de la batterie pendant l'écriture des réglages : risque accepté, traité en architecture » ; DEC-130 « Mémoire jamais écrite : aucune détection, valeurs d'origine fixes du logiciel, risque accepté » ; DEC-131 « Sauvegarder ignorée en vol : confirmation du tableau des commandes » ; antérieurement DEC-123 « Sauvegarder ignorée aussi à l'état Premier appui validé » (en partie)

### DOU-121 — Le suivi sans fil est-il un besoin à part entière ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-010 « Suivre le drone sur un appareil de suivi » (SCN-009 « Réglage et suivi du drone par le sans fil »)
**Question :** Le suivi sans fil est-il un besoin à part entière ? Doute noté à la rédaction des besoins.
**Réponse :** Oui, un besoin court de priorité Souhaitable : le drone vole sans appareil de suivi. Décidé par l'architecte par délégation explicite de l'utilisateur, 2026-10-29.
**Décision liée :** DEC-150 « Réglage en deux besoins, suivi en un besoin souhaitable »

### DOU-122 — Faut-il un besoin sur le lieu d'emploi et les protège-hélices ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-013 « Voler en appartement avec un drone de poche protégé » (SCN-001 « Vol nominal : de la batterie au posé »)
**Question :** Faut-il un besoin sur le lieu d'emploi et les protège-hélices ? Doute noté à la rédaction des besoins.
**Réponse :** Oui, un besoin court de priorité Important, pour que le cadre d'emploi ait un besoin en aval. Décidé par l'architecte par délégation explicite de l'utilisateur, 2026-10-29.
**Décision liée :** DEC-151 « Un besoin sur le lieu d'emploi et les protège-hélices »

### DOU-123 — Quelle forme donner à la page de consignes d'emploi ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-012 « Disposer d'une page de consignes d'emploi » (SCN-001 « Vol nominal : de la batterie au posé »)
**Question :** Quelle forme donner à la page de consignes d'emploi ? Doute noté à la rédaction des besoins.
**Réponse :** Une seule page, « Consignes d'emploi » — `projets/boomrone/consignes-emploi.md`, sans nouveau registre ; « Risques acceptés » reste la source. Décidé par l'architecte par délégation explicite de l'utilisateur, 2026-10-29.
**Décision liée :** DEC-154 « Notice des limites d'emploi : une page de consignes d'emploi »

### DOU-124 — Les refus d'initialisation et de mode réglage entrent-ils dans le besoin de refus d'armement ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-004 « Ne pas voler quand le drone n'est pas prêt » (SCN-003 « Échec : batterie faible à l'armement »)
**Question :** Les refus d'initialisation et de mode réglage entrent-ils dans le besoin de refus d'armement ? Doute noté à la rédaction des besoins.
**Réponse :** Oui : un seul besoin pour tous les refus et l'échec d'initialisation. Décidé par l'architecte par délégation explicite de l'utilisateur, 2026-10-29.
**Décision liée :** DEC-148 « Un seul besoin pour tous les refus et l'échec d'initialisation »

### DOU-125 — Faut-il des besoins sur la sécurité des tiers, la conformité, la durée de vie ou la gestion de la batterie ?
**Statut :** Levé
**Bloquant :** Non
**Concerne :** BES-005 « Couper les moteurs quand le vol ne peut pas continuer » (SCN-012 « Dégradé : sous-tension de la batterie »)
**Question :** Faut-il des besoins sur la sécurité des tiers, la conformité, la durée de vie ou la gestion de la batterie ? Doute noté à la rédaction des besoins.
**Réponse :** Non : l'utilisateur est seul et accepte les risques ; seule la protection de sous-tension reste un besoin, dans BES-005 « Couper les moteurs quand le vol ne peut pas continuer ». Décidé par l'architecte par délégation explicite de l'utilisateur, 2026-10-29.
**Décision liée :** DEC-153 « Pas de besoin de sécurité des tiers, de conformité, de durée de vie ni de gestion de la batterie »

### DOU-141 — Assemblage de la carte : à la main ou composants posés par JLCPCB, et disponibilité des pièces chez LCSC
**Statut :** Levé
**Bloquant :** Non
**Concerne :** ARC-013 « Carte électronique JLCPCB, câblage et assemblage », REQ-044 « Assemblage à la main » et REQ-029 « Composants disponibles à l'unité »
**Question :** JLCPCB peut souder les composants de la carte à l'usine. REQ-044 « Assemblage à la main » demande un assemblage à la main ; le LQFP-48 à 0,5 mm est le point le plus risqué. Faut-il tout souder à la main, ou faire poser les composants CMS par JLCPCB (capteurs, moteurs et connecteurs restant à la main) ? Et le STM32G431CBT6, l'AO3400A et les autres pièces sont-ils en stock chez JLCPCB (catalogue LCSC), sachant que la contrainte est d'en prendre le plus possible ? Les cartes de capteurs (LSM6DSO, VL53L1X, PMW3901) et le module HM-10 n'y sont probablement pas : faut-il les remplacer par les puces nues en stock, ou les acheter ailleurs ? Ouvert le 2026-10-29.
**Réponse :** composants CMS posés par JLCPCB (assemblage Standard), puces nues pour la centrale et le capteur de hauteur, carte achetée pour le flux optique, module Bluetooth Ebyte E104-BT02 ; stocks relevés le 2026-10-29 (HM-10 à stock 0). Décidé par l'architecte par délégation explicite de l'utilisateur, 2026-10-29. L'écart avec REQ-044 « Assemblage à la main » est suivi par DOU-150 « Écart entre l'exigence d'assemblage à la main et l'assemblage par JLCPCB ».
**Décision liée :** DEC-236 « Assemblage par JLCPCB : puces nues, carte double face, flux acheté » ; DEC-235 « Catalogue JLCPCB/LCSC vérifié : composants retenus » ; DEC-234 « JLCPCB, fabricant de la carte : contrainte de début de projet »

### DOU-150 — Écart entre l'exigence d'assemblage à la main et l'assemblage par JLCPCB
**Statut :** Levé
**Bloquant :** Non
**Concerne :** REQ-044 « Assemblage à la main », REQ-029 « Composants disponibles à l'unité » et ARC-013 « Carte électronique JLCPCB, câblage et assemblage »
**Question :** l'architecture fait poser les composants CMS par JLCPCB, ce qui contredit REQ-044 « Assemblage à la main » telle que rédigée. La nouvelle rédaction proposée est dans DEC-237 « Écart avec REQ-044 : assemblage par JLCPCB, proposition à valider ».
**Réponse :** REQ-044 « Assemblage à la main » réécrite sur accord de l'utilisateur le 2026-10-29 : la carte est fabriquée et assemblée par JLCPCB, les raccordements restent à la main.
**Décision liée :** DEC-245 « REQ-044 réécrite : carte fabriquée et assemblée par JLCPCB, raccordements à la main » ; DEC-237 « Écart avec REQ-044 : assemblage par JLCPCB, proposition à valider »

### DOU-152 — PMW3901 : puce nue ou carte achetée, alimentation et refusion
**Statut :** Levé
**Bloquant :** Non
**Concerne :** ARC-005 « Capteur de flux optique », ARC-013 « Carte électronique JLCPCB, câblage et assemblage », ARC-014 « Bilan de masse, de poussée et d'autonomie » et REQ-044 « Assemblage à la main »
**Question :** la puce nue PMW3901MB-TXQT (C43496881, 182 en stock) annonce une alimentation de 1,8 à 2,1 V, un boîtier COB de 6 × 6 × 2,28 mm et une plage de 0 à 40 °C au catalogue ; son profil de refusion et sa lentille sont inconnus. La carte achetée est retenue pour cette version ; l'alimentation de cette carte est à relever (état avant DEC-246 « Flux optique : puce PMW3901MB-TXQT achetée et posée par JLCPCB »).
**Réponse :** instruction de l'utilisateur en chat, 2026-10-29 : le capteur de flux est acheté et posé par JLCPCB (puce PMW3901MB-TXQT, C43496881, COB-28), tout ce qui peut être pris chez JLCPCB l'est. Fiche PixArt version 1.00 lue : VDD 1,8 à 2,1 V (2,0 V typique), VDDIO 1,8 à 3,6 V ; VDD alimenté en 2,0 V par un régulateur XC6206P202MR-G (C2891260, en stock) depuis le rail de 3,0 V, VDDIO et SPI2 à 3,0 V sans décalage de niveau. Les points restants (lentille, assemblage par JLCPCB, refusion, valeurs de fiche, température, hauteur de montage) sont suivis par DOU-164 « PMW3901MB : lentille, assemblage par JLCPCB et refusion de la puce », DOU-165 « Flux optique : alimentation en 2,0 V, valeurs de fiche et mise sous tension » et DOU-166 « PMW3901MB : plage de température de 0 à 40 °C et hauteur de montage avec la lentille ». Repli : carte achetée Pimoroni (DEC-248 « Flux optique : lentille collée à la main et repli sur carte achetée »).
**Décision liée :** DEC-246 « Flux optique : puce PMW3901MB-TXQT achetée et posée par JLCPCB » ; DEC-247 « Flux optique : alimentation en 2,0 V par un régulateur dédié, signaux en 3,0 V » ; DEC-248 « Flux optique : lentille collée à la main et repli sur carte achetée » ; DEC-236 « Assemblage par JLCPCB : puces nues, carte double face, flux acheté »

### DOU-148 — Numéros de broches physiques du LQFP-48 à relever dans la fiche DS12589
**Statut :** Levé
**Bloquant :** Non
**Concerne :** ARC-002 « Microcontrôleur et programmation par liaison SWD »
**Question :** le brochage de l'architecture est donné par les noms PAx et PBx, sans les numéros de broches physiques ni la vérification des fonctions alternatives (fiche DS12589 non téléchargeable à la rédaction).
**Réponse :** Levé le 2026-10-30 (instruction de l'utilisateur « Oui, appliquer ») : numéros de broches physiques et fonctions alternatives relevés dans DS12589 Rev 6 (figure 8 p. 45, tableaux 12 et 13) et reportés dans DES-002 « Microcontrôleur : brochage, horloges, découplage et octets d'option » ; PA11 en AF11 (TIM1_CH4) confirmé ; reste à les reporter dans KiCad à la saisie du schéma.
**Décision liée :** DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour » ; DEC-278 « Microcontrôleur : états d'attente de la flash, séquence boost, USART2 et I2C1 d'après les fiches »

### DOU-151 — Module E104-BT02 : débit par défaut, service, absence de commande AT
**Statut :** Levé
**Bloquant :** Non
**Concerne :** ARC-012 « Module radio Bluetooth à basse consommation » et ARC-028 « Logiciel d'essai de l'appareil de suivi »
**Question :** le catalogue ne donne ni le débit par défaut, ni l'identifiant du service et de la caractéristique, ni l'absence de commande AT du E104-BT02, ni sa version Bluetooth (4.2 selon Ebyte, 5.1 selon le catalogue).
**Réponse :** Levé le 2026-10-30 (instruction de l'utilisateur « Oui, appliquer », débit 19200 bauds retenu) : fiche d'Ebyte lue (en chinois) : débit par défaut 19200 bauds, 8N1 sans parité ; service 0xFFF0, caractéristique 0xFFF1 (notification) et 0xFFF2 (écriture), 0xFFF3 de configuration ; le module a des commandes entre chevrons, sans préfixe AT, que le projet n'utilise pas ; BLE 5.1 annoncé (le 4.2 cité par le doute n'apparaît pas). Décision : USART2 à 19200 bauds sans commande, WKP relié à PA1. Restent ouverts : niveau de WKP et mot de passe aérien (DOU-195 « Module E104-BT02 : niveau de WKP, état à la mise sous tension et mot de passe aérien »), relecture de la fiche chinoise (DOU-194 « Fiche chinoise du E104-BT02 : relecture, tolérance d'horloge et niveaux d'entrée »), essai du module seul à TI-010 « Liaison Bluetooth à basse consommation ».
**Décision liée :** DEC-277 « Module radio : 19200 bauds, réveil par PA1, broches du module et boîtier » ; DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour » ; DEC-243 « Latence de l'arrêt sans fil et module Bluetooth : mesure avant la commande de la carte »

### DOU-184 — Condensateurs d'entrée du régulateur de 3,0 V : 22 µF sur VBATL et 1 µF sur l'entrée du composant
**Statut :** Levé
**Bloquant :** Non
**Concerne :** DES-008 « Batterie, connecteur XT30 et entrée de la carte », DES-009 « Régulateur de 3,0 V et pont de mesure de la tension »
**Question :** DES-008 « Batterie, connecteur XT30 et entrée de la carte » met 22 µF (1206, 25 V) sur VBATL ; DES-009 « Régulateur de 3,0 V et pont de mesure de la tension » met 1 µF en entrée du MCP1700, sur le même réseau. Les deux schémas SVG dessinent les deux condensateurs (C8 et C10) en parallèle, ce qui est une lecture du texte, non une certitude : s'agit-il de deux condensateurs distincts (un en tête de branche, un au plus près du composant) ou d'une même valeur à corriger ?
**Réponse :** Levé le 2026-10-30 (instruction de l'utilisateur « Oui, appliquer ») : deux condensateurs distincts, valeurs inchangées : 1 µF céramique au plus près du MCP1700 (minimum de la fiche, suffit jusqu'à 100 mA, DS20001826C p. 10 et 12) et 22 µF en tête de VBATL (la charge de 130 mA dépasse 100 mA, la valeur dépend alors de la source et une valeur plus grande est permise) ; les deux schémas SVG les dessinent en parallèle, ce qui est correct.
**Décision liée :** DEC-281 « Puissance et alimentation : AO3400A, MCP1700, source de l'ADC et étalonnage » ; DEC-283 « Relevé des fiches : doutes levés et doutes mis à jour »

### DOU-205 — PMW3901MB : condensateurs du schéma de référence de la fiche et valeur illisible de R1
**Statut :** Ouvert
**Bloquant :** Non
**Concerne :** ARC-005 « Capteur de flux optique », DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V »
**Question :** le schéma de référence de la fiche PMW3901MB v1.5 (figure 7, p. 12) prévoit sur VDD deux condensateurs de 22 µF et un de 100 nF avec une résistance R1, sur VDDIO 10 µF et 100 nF, sur VREG 4,7 µF et 100 nF, et une résistance de 10 kohms (R2), tous au plus près des broches. DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V » prévoit 1 µF et 100 nF sur VDD, 100 nF sur VDDIO et 2,2 µF sur VREG. La valeur et le rôle de R1 (extraction du PDF illisible, page non affichable ici) et la raison des 22 µF (réponse à la pointe de 70 mA ?) ne sont pas lus : adopter les valeurs de la fiche ou justifier un écart est une décision.
**Réponse :** (à remplir) lire R1 et le rôle de R2 sur la page 12 du PDF ; proposition : adopter les valeurs de la fiche sauf manque de place, après avoir vérifié la stabilité du XC6206 avec une capacité de sortie plus grande (fiche Torex : CL de 1 µF, 2,2 µF compatible, au-delà non dit). Non bloquant, à lever avant le routage.
**Décision liée :** DEC-289 « Fiches du 2026-11-04 : PMW3901MB, ferrite, diode SS34, buzzer et VL53L1 »

### DOU-206 — Buzzer SMD-9650-3327 : empreinte EasyEDA de 9,0 mm contre 9,6 mm de la nomenclature
**Statut :** Levé
**Bloquant :** Non
**Concerne :** DES-011 « Circuit du voyant RGB et du buzzer », DES-013 « Implantation, routage et fichiers de fabrication pour JLCPCB »
**Question :** l'empreinte importée d'EasyEDA pour C42420997 s'appelle « BUZ-SMD_L9.0-W9.0_SMD-0955-42-27 » (corps de 9,0 x 9,0 mm, deux pastilles de 2,2 x 4,0 mm), alors que « Architecture » — `projets/boomrone/03-architecture.md` donne 9,6 x 9,6 x 5 mm pour le SMD-9650-3327. Les deux ne sont pas la même pièce ou une des données est fausse.
**Réponse :** Levé le 2026-11-05 sur instruction de l'utilisateur en chat (« fait confiance a easyEDA ») : l'empreinte EasyEDA de 9,0 x 9,0 mm (C42420997) est conservée telle quelle pour le placement et le routage. Reste à reporter l'écart de cote dans la nomenclature de « Architecture » — `projets/boomrone/03-architecture.md` à la prochaine révision.
**Décision liée :** DEC-293 « Composants EasyEDA : confiance accordée aux empreintes et symboles importés » ; DEC-290 « Schéma KiCad proj_boomrone : bibliothèque locale, feuilles hiérarchiques, validation page par page »

### DOU-207 — Symboles EasyEDA du PMW3901MB et du PB-03F : brochage à comparer aux fiches
**Statut :** Levé
**Bloquant :** Non
**Concerne :** DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V », DES-012 « Raccordement du module Bluetooth PB-03F »
**Question :** les symboles du PMW3901MB (29 broches) et du PB-03F (22 broches) viennent d'EasyEDA ; leurs noms de broches concordent avec le texte de DES-005 « Raccordement du flux optique PMW3901MB et régulateur de 2,0 V » et de DES-012 « Raccordement du module Bluetooth PB-03F », mais ils n'ont pas été comparés broche par broche aux fiches (la fiche du PMW3901MB n'est pas dans `projets/boomrone/Datasheets/`, voir DOU-185 « Fiche du capteur de flux PMW3901MB absente du dossier des fiches »). La polarité des plots du XT30PW sur l'empreinte EasyEDA (« - » à gauche, « + » à droite) reste à confirmer : DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion ».
**Réponse :** Levé le 2026-11-05 sur instruction de l'utilisateur en chat (« fait confiance a easyEDA ») : les symboles EasyEDA du PMW3901MB et du PB-03F sont retenus sans comparaison broche par broche. Reste ouvert à part : la polarité des plots du XT30PW, suivie par DOU-155 « Connecteur XT30 : genre côté carte et surtension à la connexion », et la fiche absente, DOU-185 « Fiche du capteur de flux PMW3901MB absente du dossier des fiches ».
**Décision liée :** DEC-293 « Composants EasyEDA : confiance accordée aux empreintes et symboles importés » ; DEC-290 « Schéma KiCad proj_boomrone : bibliothèque locale, feuilles hiérarchiques, validation page par page »

