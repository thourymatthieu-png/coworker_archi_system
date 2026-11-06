"""Extraction KiCad 10 -> format texte simple pour sa_main (SA-PCB).  Python KiCad (pcbnew).

  extract.py <carte.kicad_pcb> <sortie.txt> <sortie_meta.json> [--decoup decouplage.json --decoup-poids N]

Format texte (une ligne par objet, coordonnees mm, y vers le bas comme KiCad) :
  BOARD minx miny maxx maxy
  NODE <ref> <w> <h> <fixe 0|1> <cx> <cy> <orient 0|2|4|6>      w,h = courtyard dans le repere 0 deg
  NET <id> <npins>
  PIN <ref> <dx> <dy>                                          decalage de la pastille / centre du courtyard (repere 0 deg)
La meta JSON garde, par reference, le decalage origine-empreinte -> centre du courtyard (repere 0 deg).
"""
import json
import math
import sys

import pcbnew

MM = pcbnew.ToMM


def rot(x, y, deg):
    """Rotation KiCad (positive = antihoraire a l'ecran, y vers le bas)."""
    t = math.radians(deg)
    return x * math.cos(t) + y * math.sin(t), -x * math.sin(t) + y * math.cos(t)


def main():
    path, out, meta_out = sys.argv[1:4]
    decoup = None
    poids = 3
    if "--decoup" in sys.argv:
        decoup = sys.argv[sys.argv.index("--decoup") + 1]
    if "--decoup-poids" in sys.argv:
        poids = int(sys.argv[sys.argv.index("--decoup-poids") + 1])
    b = pcbnew.LoadBoard(path)
    bb = b.GetBoardEdgesBoundingBox()
    outline = [MM(bb.GetLeft()), MM(bb.GetTop()), MM(bb.GetRight()), MM(bb.GetBottom())]
    nodes, meta = [], {}
    nets = {}
    for fp in b.GetFootprints():
        ref = fp.GetReference()
        ang = fp.GetOrientationDegrees()
        px, py = MM(fp.GetPosition().x), MM(fp.GetPosition().y)
        cy = fp.GetCourtyard(pcbnew.F_CrtYd)
        if cy.OutlineCount() > 0:
            r = cy.BBox()
        else:
            r = fp.GetBoundingBox(False)
        x0, y0, x1, y1 = MM(r.GetLeft()), MM(r.GetTop()), MM(r.GetRight()), MM(r.GetBottom())
        # centre du courtyard en absolu -> repere local 0 deg
        ccx, ccy = (x0 + x1) / 2 - px, (y0 + y1) / 2 - py
        lcx, lcy = rot(ccx, ccy, -ang)          # offset origine -> centre, repere 0 deg
        w0, h0 = (x1 - x0), (y1 - y0)
        if round(ang) % 180 != 0:
            w0, h0 = h0, w0
        k = (int(round(ang / 90.0)) % 4) * 2
        nodes.append((ref, w0, h0, 1 if fp.IsLocked() else 0, px + ccx, py + ccy, k))
        meta[ref] = {"lcx": lcx, "lcy": lcy, "w": w0, "h": h0, "angle0": ang,
                     "x0": px, "y0": py, "locked": bool(fp.IsLocked()),
                     "layer": fp.GetLayerName()}
        for pad in fp.Pads():
            n = pad.GetNetname()
            if not n:
                continue
            ax, ay = MM(pad.GetPosition().x) - px, MM(pad.GetPosition().y) - py
            lx, ly = rot(ax, ay, -ang)          # pastille / origine, repere 0 deg
            nets.setdefault(n, []).append((ref, lx - lcx, ly - lcy, pad.GetNumber()))
    extra = []
    if decoup:
        d = json.load(open(decoup, encoding="utf-8"))
        # appariement: condensateur -> pastille alim du CI sur le meme reseau (si broche precisee)
        for e in d["decouplage_proximite"]:
            c, ic = e["condensateur"], e["circuit_integre"]
            cands = [e.get("broche_alimentation_num")] if e.get("broche_alimentation_num") else \
                [bc["num"] for bc in e.get("broches_candidates", [])]
            cands = [str(x) for x in cands if x is not None]
            # pastille(s) du CI portant le meme reseau que la pastille non-GND du condensateur
            cnets = {n for n, pins in nets.items() for p in pins if p[0] == c and "GND" not in n.upper()}
            pins = []
            for n in cnets:
                for p in nets[n]:
                    if p[0] == ic and (not cands or p[3] in cands):
                        pins.append(p)
            cpins = [p for n in cnets for p in nets[n] if p[0] == c]
            if pins and cpins:
                # un seul lien par condensateur : vers la premiere broche candidate (certitude faible sinon)
                extra.append((c, cpins[0], pins[0]))
    with open(out, "w", encoding="utf-8") as f:
        f.write("BOARD %.3f %.3f %.3f %.3f\n" % tuple(outline))
        for nd in nodes:
            f.write("NODE %s %.4f %.4f %d %.4f %.4f %d\n" % nd)
        nid = 0
        for n, pins in nets.items():
            if len(pins) < 2:
                continue
            f.write("NET %d %d\n" % (nid, len(pins)))
            for p in pins:
                f.write("PIN %s %.4f %.4f\n" % (p[0], p[1], p[2]))
            nid += 1
        for c, cp, ip in extra:
            for _ in range(poids):
                f.write("NET %d 2\n" % nid)
                f.write("PIN %s %.4f %.4f\n" % (c, cp[1], cp[2]))
                f.write("PIN %s %.4f %.4f\n" % (ip[0], ip[1], ip[2]))
                nid += 1
    json.dump({"outline": outline, "fp": meta, "n_decoup_liens": len(extra)},
              open(meta_out, "w", encoding="utf-8"), indent=1)
    print("noeuds", len(nodes), "reseaux", nid, "liens decouplage", len(extra), "contour", outline)


main()
