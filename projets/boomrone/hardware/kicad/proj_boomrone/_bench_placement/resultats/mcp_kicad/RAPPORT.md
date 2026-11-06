# Piste mcp_kicad : ARRET DE SECURITE (aucun placement effectue)

Statut : echec documente (volontaire). Aucune variante (mcp_kicad_outils, mcp_kicad_agent) n'a ete jugee.

## Constat
- `get_backend_state` : backend `ipc`, `realtime: true`, `ipcConnected: true`, aucune carte chargee cote serveur.
- `check_kicad_ui` : kicad.exe en cours d'execution (PID 10944), `realtime_sync: true`.
- Le serveur est donc connecte par l'API IPC a l'instance KiCad de l'utilisateur. Les outils d'edition
  (move_component, rotate_component, suggest_placement apply=true, etc.) en mode IPC temps reel agissent sur la
  carte ouverte dans l'interface, c'est-a-dire potentiellement sur la carte source de l'utilisateur, et non sur
  la copie `resultats/mcp_kicad/placee.kicad_pcb`. Rien ne permet de garantir que `open_board` redirige vers un
  fichier distinct sans toucher la carte ouverte dans l'UI.
- Consigne du banc : arreter des que le serveur travaille via IPC sur l'interface de l'utilisateur.

## Actions
- Seuls appels MCP : `get_backend_state` et `check_kicad_ui` (lecture seule). Aucun `open_board`, aucun deplacement.
- Verrou `mcp_kicad` pris puis rendu. Carte du depot et entree du banc non modifiees.
- `resultats/mcp_kicad/placee.kicad_pcb` = copie intacte de l'entree (non placee, non jugee).

## Pour reprendre
Fermer KiCad (ou lancer le serveur en backend `swig`/fichier, sans IPC), puis relancer la piste. Le caractere
temps reel IPC rend aussi la comparaison peu reproductible avec l'UI ouverte.

## Avis
Un serveur MCP qui pilote en temps reel l'UI de l'utilisateur est dangereux pour un banc automatique : il faut
un mode fichier isole. Rien n'a pu etre mesure sur les outils de placement ni sur le placement par LLM.
