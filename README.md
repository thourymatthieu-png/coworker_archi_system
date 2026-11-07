# coworker_archi_system

Équipe d'agents IA experts (architecte système, exigences, logiciel, hardware, critique, cohérence, vérificateur de sources) pour mener des projets embarqués (électronique et logiciel) en cycle en V.

Point d'entrée : `CLAUDE.md` (charte). Agents : `.claude/agents/`. Méthode : `framework/` (règles, portes, listes de contrôle, gabarits). Savoir-faire optionnel par outil ou fabricant : `modules/`. Projets : `projets/<nom>/`.

## Démarrer un projet

1. **Copier les gabarits** : copier le contenu de `framework/templates/` dans un nouveau dossier `projets/<nom>/`.
2. **Lancer l'architecte** : dans Claude Code ouvert sur ce dépôt, demander « lance l'agent architecte-systeme pour le projet <nom> » (ou parler directement de son projet : l'architecte est l'interlocuteur par défaut).
3. **Décrire ses scénarios** : l'architecte pose les questions (cas nominal, dégradés, d'échec, mise en service) et rédige `00-scenarios.md` avec vous ; il remplit le nom et le but dans `projet.md`. Préparer : ce que l'appareil doit faire, pour qui, dans quelles situations, et ce qui doit se passer quand quelque chose va mal.
4. **Porte « scénarios »** : relectures par `critique` et `coherence-clarte`, synthèse, puis votre accord explicite (`framework/portes.md`). Ensuite seulement viennent les besoins, puis les exigences, l'architecture et la conception détaillée, chacun avec sa porte.
5. **Choix d'outils et de fabricant** (en général en architecture) : l'architecte présente les options ; votre choix est consigné en décision, inscrit dans `projet.md`, et active les modules correspondants (`modules/README.md`).

Vérifier un projet à tout moment : `python tools/check_traceability_V2.py projets/<nom> --phase <phase atteinte>`.
