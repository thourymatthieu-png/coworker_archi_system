# Simulation SPICE de Boomrone — installation sur un nouveau poste

> **Aperçu** : les scripts de ce dossier simulent l'alimentation de la carte dans **ngspice** et **LTspice**, puis tracent les courbes et écrivent le rapport. Les deux simulateurs ne sont **pas** dans le dépôt : il faut les installer sur chaque poste. Rapport : `rapport-simulation-spice.html` (lecture depuis GitHub : voir son en-tête).

## À installer

| Quoi | Comment (Windows) |
|---|---|
| Python 3.12 | déjà requis par le dépôt |
| Paquets Python | `pip install --user numpy scipy matplotlib spicelib` |
| LTspice 26.1 | `winget install AnalogDevices.LTspice --source winget --scope user` (installe dans `%LOCALAPPDATA%\Programs\ADI\LTspice\LTspice.exe`) |
| ngspice 47 | voir ci-dessous |

### ngspice (installation manuelle)

Le téléchargement par script depuis SourceForge est bloqué (protection Cloudflare) et `choco` demande les droits administrateur. Deux voies :

1. **Navigateur (le plus simple)** : télécharger `ngspice-47_64.7z` sur <https://sourceforge.net/projects/ngspice/files/ng-spice-rework/47/>, l'extraire (7-Zip) dans `C:\Users\<vous>\tools\ngspice`, puis régler `NGSPICE_EXE` sur `...\Spice64\bin\ngspice_con.exe`.
2. **Paquets MSYS2** (méthode utilisée sur le premier poste) : télécharger sur <https://repo.msys2.org/mingw/mingw64/> les fichiers `.pkg.tar.zst` de `mingw-w64-x86_64-` suivi de `ngspice`, `fftw`, `readline`, `termcap`, `libwinpthread`, `libgcc`, `libgomp`, `libsystre`, `libtre`, les extraire (`pip install zstandard`, module `tarfile`) dans un même dossier ; l'exécutable est alors `mingw64\bin\ngspice_con.exe`. `ngspice_con.exe -v` doit répondre sans erreur de bibliothèque manquante.

## Régler les chemins

Par défaut `sim_boomrone.py` cherche les outils dans les emplacements du premier poste. Sur un autre poste, définir avant de lancer :

```powershell
$env:NGSPICE_EXE = "C:\chemin\vers\ngspice_con.exe"
$env:LTSPICE_EXE = "$env:LOCALAPPDATA\Programs\ADI\LTspice\LTspice.exe"
```

## Lancer

Depuis ce dossier (environ une minute) :

```bash
python sim_boomrone.py all     # calibre, simule (ngspice + LTspice), vérifie, trace
python build_report.py         # régénère rapport-simulation-spice.html
```

Les sorties brutes vont dans `resultats/` (environ 900 Mo, exclu de git). `sim_boomrone.py run`, `extras` ou `plot` lancent une étape seule.

## Contenu

- `sim_boomrone.py` : paramètres (chaque valeur avec sa source ou « HYP »), netlists, lancement, calibration.
- `analyse_boomrone.py` : lecture des deux formats de sortie, mesures, figures.
- `build_report.py` : rapport HTML autonome.
- `netlists/`, `figures/`, `metriques.json`, `timing.json`, `emf_calibree.json` : résultats conservés.
- Doutes liés : DOU-208 à DOU-212 dans `projets/boomrone/registre-doutes.md`.
