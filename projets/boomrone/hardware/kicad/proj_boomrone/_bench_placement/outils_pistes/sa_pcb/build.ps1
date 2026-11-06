# Compile sa_main.exe (SA-PCB patche) avec MinGW-w64 winlibs (gcc 16.2.0) et Boost 1.87 (en-tetes).
# Le toolchain et Boost sont dans C:\Users\quent\satc (chemin court : MAX_PATH de cc1plus, voir RAPPORT.md).
param([string]$Outils = "C:\Users\quent\Documents\codes\coworker_archi_system\projets\boomrone\hardware\kicad\proj_boomrone\_bench_placement\resultats\sa_pcb\_outils")
$W = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$W\patch_src.py" "$Outils\src\src" "$Outils\build"
$env:PATH = "C:\Users\quent\satc\mingw64\bin;$env:PATH"
Set-Location "$Outils\build"
g++ -std=gnu++17 -O2 -w -fpermissive -I shim -I . -I C:/Users/quent/satc/boost -o sa_main.exe sa_main.cpp GridBasedPlacer.cpp readFiles.cpp Node.cpp globalParam.cpp Hierarchy.cpp Module.cpp linreg.cpp 2>&1 | Select-Object -First 40 | ForEach-Object { "$_" }
Test-Path "$Outils\build\sa_main.exe"
