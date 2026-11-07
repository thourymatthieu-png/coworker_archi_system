# coworker_archi_system

Équipe d'agents IA experts (architecte système, exigences, logiciel, hardware, critique, cohérence, vérificateur de sources) pour mener des projets embarqués (électronique et logiciel) en cycle en V.

Point d'entrée : `CLAUDE.md` (charte). Agents : `.claude/agents/`. Procédures (skills) : `.claude/skills/`. Méthode : `framework/` (règles, portes, listes de contrôle, gabarits). Savoir-faire optionnel par outil ou fabricant : `modules/`. Projets : `projets/<nom>/`.

## Démarrer un projet

1. **Ouvrir Claude Code sur ce dépôt** (branche `main`, nouvelle session pour que les agents et les skills soient chargés). La session principale tient le rôle d'architecte : c'est à elle que vous parlez.
2. **Créer le projet** : taper `/nouveau-projet <nom>`. Les gabarits sont copiés dans `projets/<nom>/` et l'architecte remplit le profil (`projet.md`).
3. **Décrire ses scénarios** : l'architecte pose les questions (cas nominal, dégradés, d'échec, mise en service) et rédige `00-scenarios.md` avec vous. Préparer : ce que l'appareil doit faire, pour qui, dans quelles situations, et ce qui doit se passer quand quelque chose va mal.
4. **Porte « scénarios »** : `/porte scenarios` (l'architecte la lance lui-même quand la phase est prête). Relectures indépendantes, synthèse, puis votre accord explicite. Ensuite viennent les besoins, les exigences, l'architecture et la conception détaillée, chacun fermé par `/porte <phase>`.
5. **Changer un élément déjà validé** : `/modification <ID>`, jamais une retouche directe.
6. **Choix d'outils et de fabricant** (en général en architecture) : l'architecte présente les options ; votre choix est consigné en décision, inscrit dans `projet.md`, et active les modules correspondants (`modules/README.md`).

Vérifier un projet à tout moment : `python tools/check_traceability_V2.py projets/<nom> --phase <phase atteinte>`.
