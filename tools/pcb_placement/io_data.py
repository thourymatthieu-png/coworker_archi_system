"""Chargement du JSON d'extraction (tools/kicad_tetris_extract.py) vers le modele interne,
et sauvegarde/relecture des solutions de placement (positions/rotations)."""
from __future__ import annotations

import json
from typing import Dict

from .model import Board, Component, Net, Pad


def auto_overhang(board: Board) -> None:
    """Un composant FIXE (verrouille dans KiCad) qui depasse du contour est un debord mecanique
    deja decide par l'utilisateur : on l'exempte de la contrainte de contour (ajout a
    board.overhang_refs, en plus de ceux deja listes). Sans effet si aucun contour n'est impose."""
    if board.outline is None:
        return
    ox0, oy0, ox1, oy1 = board.outline
    extra = set()
    for ref, c in board.components.items():
        if not c.fixed:
            continue
        x0, y0, x1, y1 = c.world_bbox()
        if x0 < ox0 or y0 < oy0 or x1 > ox1 or y1 > oy1:
            extra.add(ref)
    board.overhang_refs = frozenset(set(board.overhang_refs) | extra)


def split_blocks_by_anchor(board: Board, max_pins: int = 8) -> dict:
    """Un bloc qui contient PLUSIEURS pieces verrouillees (ex. DES-007 : un connecteur moteur
    par coin, M1 a M4) est decoupe en autant de sous-blocs que d'ancres : chaque composant libre
    est rattache a l'ancre la plus proche dans le schema (distance en nombre de reseaux de
    <= `max_pins` pastilles, les gros reseaux d'alimentation/masse ne comptent pas), en
    partant des ancres. Un composant sans lien est rattache a l'ancre la plus proche
    geometriquement. Nom des sous-blocs : '<bloc>-<ancre>'. Renvoie {bloc: [sous-blocs]}."""
    from collections import deque
    result = {}
    for block in board.blocks():
        refs = board.refs_in_block(block)
        anchors = [r for r in refs if board.components[r].fixed]
        if len(anchors) < 2:
            continue
        in_block = set(refs)
        adj = {r: set() for r in refs}
        for net in board.nets.values():
            if len(net.pins) > max_pins:
                continue
            members = {r for r, _p in net.pins if r in in_block}
            for a in members:
                adj[a] |= members - {a}
        owner = {a: a for a in anchors}
        queue = deque(anchors)
        while queue:
            r = queue.popleft()
            for n in sorted(adj[r]):
                if n not in owner and not board.components[n].fixed:
                    owner[n] = owner[r]
                    queue.append(n)
        for r in refs:
            if r not in owner:
                cx, cy = board.components[r].world_center()
                owner[r] = min(anchors, key=lambda a: (board.components[a].x - cx) ** 2 + (board.components[a].y - cy) ** 2)
        for r in refs:
            board.components[r].block = f"{block}-{owner[r]}"
            board.block_parent[f"{block}-{owner[r]}"] = block
        result[block] = sorted({f"{block}-{a}" for a in anchors})
    return result


def load_board(extract_json_path: str) -> Board:
    with open(extract_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    components: Dict[str, Component] = {}
    nets: Dict[str, Net] = {}

    for c in data["components"]:
        pads = [Pad(name=p["name"], net=p["net"], local_x=p["x"], local_y=p["y"]) for p in c["pads"]]
        comp = Component(
            ref=c["ref"],
            value=c["value"],
            block=c["block"],
            is_anchor=c["is_anchor"],
            courtyard_w=c["courtyard_w_mm"],
            courtyard_h=c["courtyard_h_mm"],
            courtyard_offset_x=c["courtyard_center_offset_x_mm"],
            courtyard_offset_y=c["courtyard_center_offset_y_mm"],
            pads=pads,
            x=c["current_x_mm"],
            y=c["current_y_mm"],
            # Une ancre fixe (is_anchor) n'est JAMAIS tournee par le moteur (cf. ALLOWED_ROTATIONS,
            # limite aux multiples de 90) : son angle reel est donc conserve tel quel (ex. moteurs
            # a 45 degres sur Boomrone), pas arrondi - seuls les composants mobiles sont forces sur
            # la grille 0/90/180/270 que le recuit simule sait explorer.
            rotation=c["current_rotation_deg"] if c["is_anchor"] else _snap_rotation(c["current_rotation_deg"]),
            fixed=c["is_anchor"],
        )
        components[comp.ref] = comp
        for p in pads:
            if not p.net:
                continue
            net = nets.setdefault(p.net, Net(name=p.net))
            net.pins.append((comp.ref, p.name))

    # Les reseaux a une seule pastille ne contraignent rien (pas de paire a relier) : on les
    # garde dans Board.nets pour la tracabilite mais le cout les ignore (cf. cost.py).
    board = Board(
        components=components,
        nets=nets,
        source_pcb=data.get("source_pcb", ""),
        outline_w=data["board_outline_bbox_mm"]["w_mm"],
        outline_h=data["board_outline_bbox_mm"]["h_mm"],
    )
    if data.get("outline_mm"):  # contour Edge.Cuts dessine dans KiCad
        board.outline = tuple(data["outline_mm"])
    auto_overhang(board)
    split_blocks_by_anchor(board)
    return board


def apply_constraints(board: Board, constraints_path: str) -> None:
    """Charge un fichier JSON de contraintes mecaniques specifiques au projet (contour de
    carte fixe, positions d'ancres imposees, references autorisees a deborder) et les
    applique sur `board`. Format :
        {
          "outline_mm": [xmin, ymin, xmax, ymax],
          "overhang_refs": ["J1", "U7"],
          "positions": {
            "M1": {"x_mm": .., "y_mm": .., "rotation_deg": .., "fixed": true}
          },
          "courtyard_overrides": {
            "M1": {"courtyard_w_mm": .., "courtyard_h_mm": ..}
          }
        }
    Toutes les cles sont optionnelles. `positions` ecrase x/y/rotation (et fixed si fourni)
    des references listees - prevu pour des contraintes mecaniques deja decidees (coin de
    carte, bord de connecteur, debord d'antenne), jamais devinees par le moteur lui-meme.
    `courtyard_overrides` corrige la geometrie (empreinte) d'une reference quand celle de
    l'extraction est fausse ou provisoire (ex. empreinte de substitution utilisee le temps
    de choisir le vrai connecteur) - applique AVANT `positions`, pour que les positions de
    coin/bord soient calculees avec la bonne taille."""
    with open(constraints_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "outline_mm" in data:
        board.outline = tuple(data["outline_mm"])
    if "overhang_refs" in data:
        board.overhang_refs = frozenset(data["overhang_refs"])
    for ref, cy in data.get("courtyard_overrides", {}).items():
        if ref not in board.components:
            continue
        c = board.components[ref]
        if "courtyard_w_mm" in cy:
            c.courtyard_w = cy["courtyard_w_mm"]
        if "courtyard_h_mm" in cy:
            c.courtyard_h = cy["courtyard_h_mm"]
        if "courtyard_offset_x_mm" in cy:
            c.courtyard_offset_x = cy["courtyard_offset_x_mm"]
        if "courtyard_offset_y_mm" in cy:
            c.courtyard_offset_y = cy["courtyard_offset_y_mm"]
    for ref, pos in data.get("positions", {}).items():
        if ref not in board.components:
            continue
        c = board.components[ref]
        if "x_mm" in pos:
            c.x = pos["x_mm"]
        if "y_mm" in pos:
            c.y = pos["y_mm"]
        if "rotation_deg" in pos:
            c.rotation = pos["rotation_deg"]
        if "fixed" in pos:
            c.fixed = pos["fixed"]
    auto_overhang(board)


def _snap_rotation(angle_deg: float) -> int:
    a = round(angle_deg / 90.0) * 90 % 360
    return int(a)


def save_solution(board: Board, path: str, extra: dict | None = None) -> None:
    sol = {
        "source_pcb": board.source_pcb,
        "positions": {
            r: {"x_mm": round(c.x, 4), "y_mm": round(c.y, 4), "rotation_deg": c.rotation}
            for r, c in board.components.items()
        },
    }
    if extra:
        sol["metrics"] = extra
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sol, f, indent=2)


def load_solution_into(board: Board, path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        sol = json.load(f)
    for ref, pos in sol["positions"].items():
        if ref not in board.components:
            continue
        c = board.components[ref]
        c.x = pos["x_mm"]
        c.y = pos["y_mm"]
        c.rotation = int(pos["rotation_deg"])


def apply_decoupling(board: Board, path: str, default_mm: float = 5.0) -> dict:
    """Charge les regles de decouplage d'un fichier `decouplage.json` (tableau
    `decouplage_proximite` : condensateur, circuit integre, broche(s) d'alimentation,
    `distance_max_mm`). Une regle sans distance prend `default_mm` (la fiche ne donne que
    « as close as possible », la valeur est une valeur de projet, pas une valeur de fiche).
    Les references absentes de la carte sont ignorees et listees. Renvoie un resume."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    rules, skipped = [], []
    for e in data.get("decouplage_proximite", []):
        cap, ic = e.get("condensateur"), e.get("circuit_integre")
        pins = [c["num"] for c in e.get("broches_candidates", []) if c.get("num")]
        if e.get("broche_alimentation_num"):
            pins.append(str(e["broche_alimentation_num"]))
        if cap not in board.components or ic not in board.components or not pins:
            skipped.append(cap)
            continue
        dmax = e.get("distance_max_mm")
        rules.append({"cap": cap, "ic": ic, "pins": pins,
                      "dmax": float(dmax) if dmax is not None else float(default_mm)})
    board.decoupling_rules = rules
    return {"rules": len(rules), "skipped": skipped}
