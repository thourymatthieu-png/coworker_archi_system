"""Prepare une copie compilable de SA-PCB sous Windows/MinGW dans <build> (la copie source reste intacte).

  patch_src.py <SA-PCB/src/src> <build_dir>

Modifications (toutes minimes, aucune ne touche l'algorithme) :
  - util.h : mkdir(x, 0777) -> mkdir(x) (MinGW), commandes shell `whoami` retirees
  - GridBasedPlacer.hpp : plus de dependance au sous-module KicadParser (ctor sans base), membres prives -> publics
  - GridBasedPlacer.cpp : test_placer_flow() (qui lit une base KicadParser) supprime ; echantillonnage du
    meilleur etat toutes les 10 iterations externes au lieu de 100 ; ecritures de debug ./cache/*.pl|*.rad supprimees
  - shims : sys/resource.h (getrusage), kicadPcbDataBase.h (classe vide)
"""
import os
import re
import shutil
import sys

src, dst = sys.argv[1:3]
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("py_utils", "*.py", "PcbPlacer_wrapper.cpp", "*.i"))


def edit(name, fn):
    p = os.path.join(dst, name)
    t = open(p, encoding="utf-8", errors="replace").read()
    t2 = fn(t)
    assert t2 != t, name
    open(p, "w", encoding="utf-8").write(t2)


edit("util.h", lambda t: t.replace("mkdir(dirName.c_str(), 0777)", "mkdir(dirName.c_str())"))

def hpp(t):
    t = t.replace("GridBasedPlacer(kicadPcbDataBase &db) : mDb(db) {}", "GridBasedPlacer() {}")
    t = t.replace("kicadPcbDataBase &getDb() { return mDb; }", "")
    t = t.replace("kicadPcbDataBase &mDb;", "")
    t = t.replace("private:", "public:")
    t = t.replace("class GridBasedPlacer {", "namespace bgi = boost::geometry::index;\nclass GridBasedPlacer {", 1)
    return t
edit("GridBasedPlacer.hpp", hpp)

def cpp(t):
    # supprime test_placer_flow (de "double GridBasedPlacer::test_placer_flow() {" jusqu'au commentaire suivant "initialize_params")
    a = t.index("//kicadPcbDataBase &GridBasedPlacer::test_placer_flow() {")
    b = t.index("/**\ninitialize_params")
    t = t[:a] + t[b:]
    t = t.replace("if (ii % 100 == 0) {", "if (ii % 10 == 0) {")
    t = t.replace('writePlFile("./cache/"+std::to_string( ii )+".pl");', "")
    t = t.replace('writeRadFile("./cache/"+std::to_string( ii )+".rad");', "")
    t = t.replace('writeNodesFile("./cache/nodes.nodes");', "")
    t = t.replace('writePlFile("initial_pl.pl");', "")
    return t
edit("GridBasedPlacer.cpp", cpp)

os.makedirs(os.path.join(dst, "shim", "sys"), exist_ok=True)
open(os.path.join(dst, "shim", "sys", "resource.h"), "w").write(
    "#pragma once\n#include <sys/time.h>\n#include <time.h>\n"
    "struct rusage { struct timeval ru_utime, ru_stime; };\n#define RUSAGE_SELF 0\n"
    "static inline int getrusage(int, struct rusage* r){ r->ru_utime.tv_sec = clock()/CLOCKS_PER_SEC;"
    " r->ru_utime.tv_usec = 0; r->ru_stime = r->ru_utime; return 0; }\n")
open(os.path.join(dst, "shim", "kicadPcbDataBase.h"), "w").write("#pragma once\nclass kicadPcbDataBase {};\n")
shutil.copy(os.path.join(os.path.dirname(__file__), "sa_main.cpp"), os.path.join(dst, "sa_main.cpp"))
print("ok")
