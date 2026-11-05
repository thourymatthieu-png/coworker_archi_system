#!/usr/bin/env python3
"""Crée une feuille KiCad 10 contenant une image PNG (ex. synoptique) et ajoute sa case
à la page racine du projet hiérarchique.

Usage :
    python tools/kicad_add_image_sheet.py <dossier_projet_kicad> <image.png> \
        --file synoptique.kicad_sch --name "Synoptique de la carte" --title "Synoptique" [--paper A3]

- L'image est ré-encodée à 300 ppp (échelle KiCad prévisible) puis mise à l'échelle pour
  remplir la feuille avec une marge ; elle est centrée sous le cartouche.
- Idempotent : si la feuille existe déjà, seule l'image est remplacée.
- Après l'appel, lancer `python tools/kicad_build_root.py <dossier>` (aligne la case sur la grille).
"""
import argparse
import base64
import glob
import os
import re
import struct
import uuid
import zlib

PAPERS = {"A4": (297.0, 210.0), "A3": (420.0, 297.0)}
MARGIN = 12.0       # mm autour de l'image
TITLE_H = 22.0      # mm réservés en bas pour le cartouche


def uid():
    return str(uuid.uuid4())


def set_dpi(png, dpi=300):
    """Remplace/ajoute le bloc pHYs du PNG ; renvoie (octets, largeur px, hauteur px)."""
    assert png[:8] == b"\x89PNG\r\n\x1a\n", "ce n'est pas un PNG"
    w, h = struct.unpack(">II", png[16:24])
    out, i = [png[:8]], 8
    ppm = int(dpi / 0.0254)
    phys = struct.pack(">IIB", ppm, ppm, 1)
    done = False
    while i < len(png):
        n = struct.unpack(">I", png[i:i + 4])[0]
        typ = png[i + 4:i + 8]
        chunk = png[i:i + 12 + n]
        i += 12 + n
        if typ == b"pHYs":
            continue
        out.append(chunk)
        if typ == b"IHDR" and not done:
            out.append(struct.pack(">I", 9) + b"pHYs" + phys + struct.pack(">I", zlib.crc32(b"pHYs" + phys)))
            done = True
    return b"".join(out), w, h


def image_block(png_path, paper, dpi=300):
    data, w, h = set_dpi(open(png_path, "rb").read(), dpi)
    pw, ph = PAPERS[paper]
    nat_w, nat_h = w / dpi * 25.4, h / dpi * 25.4
    scale = min((pw - 2 * MARGIN) / nat_w, (ph - 2 * MARGIN - TITLE_H) / nat_h)
    cx, cy = pw / 2, MARGIN + (ph - 2 * MARGIN - TITLE_H) / 2
    b64 = base64.b64encode(data).decode()
    lines = "\n".join('\t\t\t"%s"' % b64[k:k + 76] for k in range(0, len(b64), 76))
    return ("\t(image\n\t\t(at %.2f %.2f)\n\t\t(scale %.4f)\n\t\t(uuid \"%s\")\n\t\t(data\n%s\n\t\t)\n\t)\n"
            % (cx, cy, scale, uid(), lines)), scale


def sheet_file(png_path, paper, title):
    img, scale = image_block(png_path, paper)
    return ('(kicad_sch\n\t(version 20260306)\n\t(generator "eeschema")\n\t(generator_version "10.0")\n'
            '\t(uuid "%s")\n\t(paper "%s")\n\t(title_block\n\t\t(title "%s")\n\t)\n\t(lib_symbols)\n%s'
            '\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n)\n' % (uid(), paper, title, img)), scale


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("projet")
    ap.add_argument("png")
    ap.add_argument("--file", default="synoptique.kicad_sch")
    ap.add_argument("--name", default="Synoptique de la carte")
    ap.add_argument("--title", default="Synoptique de la carte")
    ap.add_argument("--paper", default="A3", choices=PAPERS)
    a = ap.parse_args()

    path = os.path.join(a.projet, a.file)
    txt, scale = sheet_file(a.png, a.paper, a.title)
    existed = os.path.exists(path)
    open(path, "w", encoding="utf8", newline="\n").write(txt)
    print("feuille %s %s (échelle %.3f)" % (a.file, "mise à jour" if existed else "créée", scale))

    pro = glob.glob(os.path.join(a.projet, "*.kicad_pro"))[0]
    pname = os.path.splitext(os.path.basename(pro))[0]
    root_path = os.path.join(a.projet, pname + ".kicad_sch")
    t = open(root_path, encoding="utf8").read()
    if 'Sheetfile" "%s"' % a.file in t:
        print("case déjà présente à la racine")
        return
    root_uuid = re.search(r'\(uuid "([^"]+)"\)', t).group(1)
    page = len(re.findall(r'\(property "Sheetfile"', t)) + 2
    blk = ('\t(sheet\n\t\t(at 241.3 167.64)\n\t\t(size 38.1 15.24)\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n'
           '\t\t(on_board yes)\n\t\t(dnp no)\n\t\t(fields_autoplaced yes)\n\t\t(stroke\n\t\t\t(width 0.0006)\n\t\t\t(type solid)\n\t\t)\n'
           '\t\t(fill\n\t\t\t(color 0 0 0 0)\n\t\t)\n\t\t(uuid "%s")\n'
           '\t\t(property "Sheetname" "%s"\n\t\t\t(at 243.84 166.37 0)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify left bottom)\n\t\t\t)\n\t\t)\n'
           '\t\t(property "Sheetfile" "%s"\n\t\t\t(at 243.84 184.15 0)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify left top)\n\t\t\t)\n\t\t)\n'
           '\t\t(instances\n\t\t\t(project "%s"\n\t\t\t\t(path "/%s"\n\t\t\t\t\t(page "%d")\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n'
           % (uid(), a.name, a.file, pname, root_uuid, page))
    k = re.search(r"\n\t\(sheet_instances", t).start() + 1
    open(root_path, "w", encoding="utf8", newline="\n").write(t[:k] + blk + t[k:])
    print("case ajoutée à la racine (page %d) ; lancer ensuite kicad_build_root.py" % page)


if __name__ == "__main__":
    main()
