"""Verrous partages entre les agents du banc de placement (Python systeme, sans dependance).

Un verrou = un dossier `verrous/<nom>.lock` cree de facon atomique (os.mkdir). Le detenteur y
ecrit `detenteur.json` (qui, depuis). Verrous utilises :
  - `mcp_kicad` : obligatoire avant TOUT appel d'outil mcp__kicad__* (le serveur MCP KiCad est
    unique et partage : un seul agent a la fois peut ouvrir une carte et la manipuler) ;
  - `routage`   : pris automatiquement par `bench_eval.py routage` (un seul Freerouting a la
    fois, pour des temps comparables et pour ne pas saturer la memoire).

Usage :
  python verrou.py prendre <nom> --qui <piste> [--attente 540] [--perime 5400]
  python verrou.py rendre  <nom> --qui <piste>
  python verrou.py attendre <nom> [--attente 540]      # attend qu'il soit libre, sans le prendre
  python verrou.py etat

Codes de sortie : 0 = fait ; 2 = encore occupe a la fin de l'attente (relancer la commande) ;
1 = erreur (ex. rendre un verrou detenu par un autre).
Un verrou plus vieux que --perime secondes (defaut 90 min) est considere comme abandonne et repris
(avec un message). L'attente maximale par appel reste sous les 10 min d'un appel d'outil Bash.
"""
import argparse
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DOSSIER = os.path.join(os.path.dirname(HERE), "verrous")


def _chemin(nom):
    return os.path.join(DOSSIER, f"{nom}.lock")


def lire(nom):
    try:
        with open(os.path.join(_chemin(nom), "detenteur.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None if not os.path.isdir(_chemin(nom)) else {"qui": "?", "depuis": 0}


def essayer(nom, qui, perime=5400):
    os.makedirs(DOSSIER, exist_ok=True)
    try:
        os.mkdir(_chemin(nom))
    except FileExistsError:
        d = lire(nom) or {}
        if d.get("qui") == qui:
            return True  # deja detenu par le meme agent : reentrant
        age = time.time() - float(d.get("depuis", 0) or 0)
        if d.get("depuis") and age > perime:
            print(f"[verrou] {nom} detenu par {d.get('qui')} depuis {age:.0f} s : repute abandonne, repris.")
            shutil.rmtree(_chemin(nom), ignore_errors=True)
            return essayer(nom, qui, perime)
        return False
    with open(os.path.join(_chemin(nom), "detenteur.json"), "w", encoding="utf-8") as f:
        json.dump({"qui": qui, "depuis": time.time(), "depuis_txt": time.strftime("%H:%M:%S")}, f)
    return True


def prendre(nom, qui, attente=540, perime=5400, pas=5):
    t0 = time.time()
    annonce = False
    while True:
        if essayer(nom, qui, perime):
            print(f"[verrou] {nom} pris par {qui}.")
            return True
        if not annonce:
            print(f"[verrou] {nom} occupe par {(lire(nom) or {}).get('qui')} : attente (max {attente} s)...", flush=True)
            annonce = True
        if time.time() - t0 > attente:
            print(f"[verrou] {nom} toujours occupe apres {attente} s : relancer la commande.")
            return False
        time.sleep(pas)


def rendre(nom, qui):
    d = lire(nom)
    if d is None:
        print(f"[verrou] {nom} deja libre.")
        return True
    if d.get("qui") != qui:
        print(f"[verrou] refus : {nom} est detenu par {d.get('qui')}, pas par {qui}.")
        return False
    shutil.rmtree(_chemin(nom), ignore_errors=True)
    print(f"[verrou] {nom} rendu par {qui}.")
    return True


def attendre(nom, attente=540, pas=5):
    t0 = time.time()
    while os.path.isdir(_chemin(nom)):
        if time.time() - t0 > attente:
            print(f"[verrou] {nom} toujours occupe par {(lire(nom) or {}).get('qui')}.")
            return False
        time.sleep(pas)
    print(f"[verrou] {nom} libre.")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["prendre", "rendre", "attendre", "etat"])
    ap.add_argument("nom", nargs="?")
    ap.add_argument("--qui")
    ap.add_argument("--attente", type=float, default=540)
    ap.add_argument("--perime", type=float, default=5400)
    a = ap.parse_args()
    if a.action == "etat":
        os.makedirs(DOSSIER, exist_ok=True)
        locks = [n[:-5] for n in os.listdir(DOSSIER) if n.endswith(".lock")]
        print({n: lire(n) for n in locks} or "aucun verrou")
        return 0
    if not a.nom:
        ap.error("nom du verrou manquant")
    if a.action in ("prendre", "rendre") and not a.qui:
        ap.error("--qui <piste> obligatoire")
    if a.action == "prendre":
        return 0 if prendre(a.nom, a.qui, a.attente, a.perime) else 2
    if a.action == "rendre":
        return 0 if rendre(a.nom, a.qui) else 1
    return 0 if attendre(a.nom, a.attente) else 2


if __name__ == "__main__":
    sys.exit(main())
