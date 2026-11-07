# Notes KiCad propres à Boomrone

> **Aperçu** : constats KiCad qui ne valent que pour la carte Boomrone (`proj_boomrone`). Les constats valables pour tout projet KiCad sont dans « Notes sur le MCP KiCad — bugs connus et méthode » — `modules/kicad/kicad-mcp-notes.md`.

## J1 (XT30PW-M, connecteur batterie) : sens d'enfichage confirmé par l'utilisateur dans KiCad

Un agent avait déduit le sens d'enfichage de J1 par lecture géométrique du footprint seule (position
des pastilles, forme de la sérigraphie) et conclu qu'il fallait une rotation de 180°. **L'utilisateur
a ouvert KiCad, regardé le connecteur réel et corrigé lui-même : la bonne orientation est rotation
0°**, pas 180°. Voir aussi, pour d'autres pièces importées d'EasyEDA : DOU-206 « Buzzer SMD-9650-3327 : empreinte EasyEDA de 9,0 mm contre 9,6 mm de la nomenclature » et DOU-207 « Symboles EasyEDA du PMW3901MB et du PB-03F : brochage à comparer aux fiches ».

**État de référence confirmé (2026-11-05)** : J1
(`lib_boomrone:CONN-TH_XT30PW-M`), position (25, 43,4875) mm, **rotation 0°**, couche F.Cu. Broches 1
(GND) et 2 (VBATM, pastilles traversantes Ø2,5 mm) côté nord (y ≈ 38,49, vers le centre de la carte) ;
broches de maintien 3/4 (sans réseau) côté sud (y ≈ 48,49, vers le bord bas de la carte, où le boîtier
dépasse légèrement du contour — comportement attendu, c'est là que le câble s'enfiche depuis
l'extérieur). **Ne pas retourner ce composant dans une future passe de placement** (le passer en
`locked`) sans revalidation explicite de l'utilisateur.

## Vérification après reprise sur un autre poste

```bash
python tools/check_traceability_V2.py projets/boomrone --phase conception
kicad-cli sch erc projets/boomrone/hardware/kicad/proj_boomrone/proj_boomrone.kicad_sch -o rapport.txt
```
Attendu : OK (au 2026-11-07 : 0 erreur, 66 écarts au standard du framework du 2026-11-07, surtout des doutes sans échéance, qui font échouer `--gate`), et 0 violation ERC. Fiches techniques à recopier à la main (dossier ignoré par Git) ; plusieurs manquent déjà : DOU-185 « Fiche du capteur de flux PMW3901MB absente du dossier des fiches » et le buzzer (DOU-206 « Buzzer SMD-9650-3327 : empreinte EasyEDA de 9,0 mm contre 9,6 mm de la nomenclature »).

## Synoptique
Image dessinée par `projets/boomrone/tools/gen_synoptique_boomrone.py`, importée par `modules/kicad/tools/kicad_add_image_sheet.py` (page 12 de la hiérarchie).
