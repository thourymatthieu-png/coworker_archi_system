"""Placement par forces dirigees (attraction par reseau, repulsion anti-recouvrement) et
legalisation (resorption des chevauchements residuels par poussee geometrique). Opere
directement sur les Component d'un Board (mutation des positions en place) pour un
sous-ensemble de references donne ; le reste de la carte (autres composants non inclus dans
`refs`) reste fixe et sert d'obstacle pour la repulsion/legalisation si `obstacles` est passe."""
from __future__ import annotations

import math
import random
from typing import Dict, List, Optional, Tuple

from . import live
from .model import ALLOWED_ROTATIONS, Board
from .partition import build_weight_matrix


def force_directed_layout(
    board: Board,
    refs: List[str],
    iterations: int = 200,
    area_hint: Optional[float] = None,
    seed: int = 0,
    try_rotations: bool = True,
) -> None:
    """Dispose `refs` par forces dirigees (style Fruchterman-Reingold adapte) : attraction
    le long des reseaux partages (poids = expansion en clique, cf. partition.build_weight_matrix),
    repulsion proportionnelle a l'encombrement reel (demi-extensions + marge) pour que le
    refroidissement separe deja grossierement les boitiers avant la legalisation stricte."""
    rng = random.Random(seed)
    movable = [r for r in refs if not board.components[r].fixed]
    if not movable:
        return
    w = build_weight_matrix(refs, board.nets)
    idx = {r: i for i, r in enumerate(refs)}

    # Rayon caracteristique : aire visee (ou somme des aires composants * 2 par defaut),
    # sert a calibrer les constantes d'attraction/repulsion comme pour FR classique.
    if area_hint is None:
        # Aire des SEULS composants places par cet appel (jamais celle de toute la carte :
        # un petit groupe ne doit pas heriter d'une echelle calculee sur les 100+ composants
        # du PCB entier, sinon le rayon de depart explose - bug constate le 2026-11-05).
        area_hint = sum(board.components[r].courtyard_w * board.components[r].courtyard_h for r in refs) * 2.5
    k = math.sqrt(max(area_hint, 1.0) / max(len(refs), 1))

    # Position initiale : cercle (eviter la degenerescence toutes-positions-egales de FR).
    for i, r in enumerate(refs):
        if r in movable:
            angle = 2 * math.pi * i / len(refs)
            jitter = rng.uniform(-0.5, 0.5)
            board.components[r].x = k * len(refs) ** 0.5 * math.cos(angle) + jitter
            board.components[r].y = k * len(refs) ** 0.5 * math.sin(angle) + jitter

    temp = k * 2.0
    cooling = temp / iterations
    gravity = 0.03  # rappel doux vers le centre : sans lui, un composant peu connecte
    # (poids d'attraction faible) derive indefiniment car la repulsion (~1/dist) decroit
    # plus lentement que l'attraction ne peut le retenir a grande distance - defaut classique
    # du placement par forces dirigees, constate le 2026-11-05 (composants pousses a des
    # dizaines de mm des ancres alors que la carte fait quelques cm).

    for it in range(iterations):
        live.tick(board)
        disp: Dict[str, List[float]] = {r: [0.0, 0.0] for r in movable}
        center_x = sum(board.components[r].x for r in refs) / len(refs)
        center_y = sum(board.components[r].y for r in refs) / len(refs)
        for r in movable:
            disp[r][0] -= gravity * (board.components[r].x - center_x)
            disp[r][1] -= gravity * (board.components[r].y - center_y)
        # Repulsion (toutes paires de refs, y compris fixes comme obstacles immobiles).
        for a_idx, ra in enumerate(refs):
            ca = board.components[ra]
            for rb in refs[a_idx + 1:]:
                cb = board.components[rb]
                dx = ca.x - cb.x
                dy = ca.y - cb.y
                dist = math.hypot(dx, dy) or 0.01
                hw_a, hh_a = ca.world_half_extents()
                hw_b, hh_b = cb.world_half_extents()
                min_sep = (hw_a + hw_b + hh_a + hh_b) / 2.0 + 0.3
                # Repulsion a PORTEE LIMITEE (coupee au-dela de quelques fois min_sep) : deux
                # composants non/peu connectes n'ont aucune raison de se repousser a grande
                # distance (un champ a decroissance en 1/dist reste non negligeable sur toute
                # la carte) - seule la gravite (vers le centre du groupe) et l'attraction par
                # reseau doivent gouverner l'espacement au-dela du contact. Defaut constate le
                # 2026-11-05 : composants pousses a des dizaines de mm sans raison avec une
                # repulsion a portee illimitee.
                if dist < min_sep * 4.0:
                    force = (k * k) / dist * max(min_sep / dist, 1.0)
                    fx, fy = dx / dist * force, dy / dist * force
                    if ra in disp:
                        disp[ra][0] += fx
                        disp[ra][1] += fy
                    if rb in disp:
                        disp[rb][0] -= fx
                        disp[rb][1] -= fy

        # Attraction (ressort le long des reseaux partages, pondere par le poids de clique).
        for a_idx, ra in enumerate(refs):
            ca = board.components[ra]
            ia = idx[ra]
            row = w[ia]
            for b_idx in range(a_idx + 1, len(refs)):
                # float(...) : sortir du type numpy.float64 des maintenant, sinon il
                # contamine ensuite Component.x/y (numpy.bool_ refuse par json.dump plus loin).
                weight = float(row[b_idx])
                if weight <= 0:
                    continue
                rb = refs[b_idx]
                cb = board.components[rb]
                dx = ca.x - cb.x
                dy = ca.y - cb.y
                dist = math.hypot(dx, dy) or 0.01
                force = weight * (dist * dist) / k
                fx, fy = dx / dist * force, dy / dist * force
                if ra in disp:
                    disp[ra][0] -= fx
                    disp[ra][1] -= fy
                if rb in disp:
                    disp[rb][0] += fx
                    disp[rb][1] += fy

        for r in movable:
            dx, dy = disp[r]
            dist = math.hypot(dx, dy) or 0.01
            capped = min(dist, temp)
            board.components[r].x = float(board.components[r].x + dx / dist * capped)
            board.components[r].y = float(board.components[r].y + dy / dist * capped)

        if try_rotations and it % 20 == 19:
            for r in movable:
                if not board.components[r].rotation_locked:
                    _try_best_rotation(board, r)

        temp = max(temp - cooling, 0.01)


def _boxes_overlap(a: tuple, b: tuple, margin_mm: float) -> bool:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    return ax0 - margin_mm < bx1 and bx0 - margin_mm < ax1 and ay0 - margin_mm < by1 and by0 - margin_mm < ay1


def compute_decoupling_assignment(rules: List[dict]) -> Dict[str, tuple]:
    """Calcule, de facon deterministe et SANS toucher au board (fonction pure, reutilisee par
    `place_active_and_decoupling` ET par l'affichage dans groupes_view.py pour rester
    coherents), la broche choisie pour chaque condensateur `rules[i]["cap"]` : traitement par
    ordre alphabetique de reference, en equilibrant la charge entre les broches CANDIDATES de
    CHAQUE regle (qui peuvent differer d'un condensateur a l'autre - cf.
    `appariement_libre_dans_groupe` du fichier `decouplage.json`, aucune des deux n'est "la
    bonne" broche au sens strict, seulement un choix parmi les candidates). Renvoie
    {cap: (ic, broche ou None si la regle n'a aucune candidate)}."""
    by_ic: Dict[str, List[dict]] = {}
    for r in rules:
        by_ic.setdefault(r["ic"], []).append(r)
    out: Dict[str, tuple] = {}
    for ic, ic_rules in by_ic.items():
        pin_usage: Dict[str, int] = {}
        for r in sorted(ic_rules, key=lambda r: r["cap"]):
            candidates = r.get("pins") or []
            pin = min(candidates, key=lambda p: pin_usage.get(p, 0)) if candidates else None
            if pin is not None:
                pin_usage[pin] = pin_usage.get(pin, 0) + 1
            out[r["cap"]] = (ic, pin)
    return out


_CARDINALS: Tuple[Tuple[float, float], ...] = ((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0))


def _snap_cardinal(dx: float, dy: float) -> tuple:
    """Direction brute (IC -> broche) ramenee a l'une des 4 directions cardinales (une broche
    de boitier QFP est, au pas pres, sur UN cote du boitier - la direction exacte flotte peu
    autour de l'axe de ce cote)."""
    if dx == 0.0 and dy == 0.0:
        return (1.0, 0.0)
    return max(_CARDINALS, key=lambda d: d[0] * dx + d[1] * dy)


def _rotate_xy(lx: float, ly: float, deg: float) -> tuple:
    a = math.radians(deg)
    cos_a, sin_a = math.cos(a), math.sin(a)
    return lx * cos_a - ly * sin_a, lx * sin_a + ly * cos_a


def _isotonic_nondecreasing(values: List[float]) -> List[float]:
    """Regression isotone (Pool Adjacent Violators) : la suite non DEcroissante la plus proche
    de `values` au sens des moindres carres. Utilisee pour le pavage 1D d'une rangee de
    condensateurs (cf. _pack_1d_balanced) - preferee a un simple "pousse vers l'avant" qui
    accumule tout le decalage d'un seul cote (retour utilisateur du 2026-11-06 : C27/C33 trop
    loin de leur broche alors que C30 l'etait aussi, dans l'autre sens)."""
    blocks: List[List[float]] = []   # [valeur moyenne, poids]
    for v in values:
        blocks.append([v, 1.0])
        while len(blocks) >= 2 and blocks[-2][0] > blocks[-1][0]:
            v2, w2 = blocks.pop()
            v1, w1 = blocks.pop()
            blocks.append([(v1 * w1 + v2 * w2) / (w1 + w2), w1 + w2])
    out: List[float] = []
    for v, w in blocks:
        out.extend([v] * int(w))
    return out


def _pack_1d_balanced(natives: List[float], halves: List[float], margin_mm: float) -> List[float]:
    """Positions 1D pour des elements DEJA TRIES par `natives` croissant, respectant un
    espacement minimal `halves[i-1] + halves[i] + margin_mm` entre voisins, aussi proches que
    possible de leur position native `natives[i]` - pas seulement un "pousse vers l'avant"
    depuis le premier (qui cascaderait tout le monde d'un seul cote), une regression isotone
    REPARTIT l'ecart necessaire entre les elements qui se disputent la meme place."""
    n = len(natives)
    offsets = [0.0] * n
    for i in range(1, n):
        offsets[i] = offsets[i - 1] + halves[i - 1] + halves[i] + margin_mm
    d = [natives[i] - offsets[i] for i in range(n)]
    z = _isotonic_nondecreasing(d)
    return [z[i] + offsets[i] for i in range(n)]


def place_active_and_decoupling(board: Board, refs: List[str], rules: List[dict], margin_mm: float = 0.3,
                                 seed: int = 0, mode: str = "position1", mirror_alt: bool = False,
                                 order_seed: int = 0) -> set:
    """Mise en place dirigee par le decouplage (demande utilisateur du 2026-11-06, affinee le
    meme jour avec deux positions - cf. retour utilisateur) : 1) le(s) composant(s) actif(s) du
    groupe sont poses d'abord, cote a cote ; 2) chaque condensateur de decouplage est tourne
    (0/90/180/270) et pose pres de la broche d'alimentation qu'il decouple (choisie par
    `compute_decoupling_assignment`) :

    - `mode="position1"` : le PETIT cote du condensateur (celui qui porte la broche posee sur
      le reseau decouple) touche la broche, le corps s'etend vers l'exterieur de l'IC ;
      plusieurs condensateurs sur la MEME broche sont ranges cote a cote sur leur GRAND cote
      (paralleles, perpendiculaires a l'IC).
    - `mode="position2"` : le GRAND cote du condensateur est colle contre le boitier de l'IC
      (axe des pastilles parallele au bord de l'IC). Les condensateurs sont regroupes par
      ARETE (bord de l'IC), pas par broche exacte - des broches voisines sur le meme bord sont
      traitees comme une seule rangee (retour utilisateur du 2026-11-06) - puis ranges cote a
      cote dans une seule rangee flush contre l'IC, chacun le plus pres possible de SA propre
      broche (pavage 1D, repousse seulement en cas de chevauchement avec le voisin precedent).

    `mirror_alt` : un condensateur sur deux de chaque groupe de broche est tourne de 180 deg
    de plus ("tete-beche") - piste a essayer parmi d'autres pour les broches encombrees, cf.
    retour utilisateur du 2026-11-06 ("pourquoi pas tete-beche"). `order_seed` : ordre de
    traitement des groupes de broches melange (graine) - deux broches voisines qui se disputent
    le meme espace restreint peuvent donner un meilleur resultat dans un ordre different ;
    `compute_decoupling_assignment` reste toujours le meme (l'affectation capa -> broche ne
    change pas, seul l'ORDRE de pose change). Repli (position generique, centree sur la broche)
    si la polarite d'un condensateur ne peut pas etre lue (pas exactement 2 pastilles, ou la
    broche d'alimentation n'est pas identifiee). Les "autres composants" (etape 3) ne sont PAS
    touches ici. Renvoie l'ensemble des references posees (IC + condensateurs) ; vide si aucune
    regle ne concerne ce groupe."""
    refs_set = set(refs)
    local_rules = [r for r in rules if r.get("ic") in refs_set and r.get("cap") in refs_set]
    if not local_rules:
        return set()
    assignment = compute_decoupling_assignment(local_rules)
    ics = sorted({r["ic"] for r in local_rules}, key=lambda ic: (-sum(1 for r in local_rules if r["ic"] == ic), ic))
    handled: set = set()
    placed_boxes: List[tuple] = []
    cursor_x = 0.0
    for ic in ics:
        comp = board.components[ic]
        if not comp.fixed:
            cur_cx, cur_cy = comp.world_center()
            hw, _hh = comp.world_half_extents()
            comp.x += (cursor_x + hw) - cur_cx
            comp.y += 0.0 - cur_cy
        handled.add(ic)
        placed_boxes.append(comp.world_bbox())
        ic_cx, ic_cy = comp.world_center()
        cap_rules = sorted((r for r in local_rules if r["ic"] == ic), key=lambda r: r["cap"])

        def _pin_point(rule: dict) -> tuple:
            _ic2, pin = assignment[rule["cap"]]
            pad = next((p for p in comp.pads if p.name == pin), None) if pin else None
            return comp.pad_world_pos(pad) if pad is not None else (ic_cx, ic_cy)

        if mode == "position2":
            # Regroupe par ARETE (direction cardinale IC -> broche), pas par broche exacte :
            # des broches VOISINES sur le meme bord (ex. VREF+ et VDDA, cote a cote sur le
            # boitier) partagent une seule rangee plutot que des piles separees qui se genent
            # (retour utilisateur du 2026-11-06 : "on fait comme si c'etait la meme pin").
            edge_groups: Dict[tuple, List[tuple]] = {}
            for rule in cap_rules:
                if rule["cap"] in handled:
                    continue
                px, py = _pin_point(rule)
                dirc = _snap_cardinal(px - ic_cx, py - ic_cy)
                latc = (-dirc[1], dirc[0])
                lateral = (px - ic_cx) * latc[0] + (py - ic_cy) * latc[1]
                edge_groups.setdefault(dirc, []).append((rule, lateral))

            ic_hw, ic_hh = comp.world_half_extents()
            for dirc, items in sorted(edge_groups.items()):
                dirx, diry = dirc
                latx, laty = -diry, dirx
                # Point de depart = le BORD de l'IC dans la direction `dir` (pas son centre).
                edge_depth = (ic_hw if abs(dirx) >= abs(diry) else ic_hh) + margin_mm
                items.sort(key=lambda it: it[1])   # ordre le long du bord, broches voisines regroupees
                # Tete-beche seulement si CE bord fusionne plusieurs broches DIFFERENTES (cf.
                # retour utilisateur du 2026-11-06 : utile pour desserrer un coin encombre,
                # mais casse inutilement une paire propre sur une seule et meme broche comme
                # C28/C34 - la tournerait sans raison, pour rien gagner).
                apply_mirror = mirror_alt and len({round(lat, 3) for _r, lat in items}) > 1

                # Passe 1 : polarite, rotation (et donc demi-largeur laterale) de chaque element ;
                # repli immediat (position generique) pour celui dont la polarite n'est pas lisible.
                placeable: List[tuple] = []   # (cap_comp, rule, lateral, off_x, off_y, half_lat, half_depth)
                for cidx, (rule, lateral) in enumerate(items):
                    cap = rule["cap"]
                    cap_comp = board.components[cap]
                    power_pad = next((p for p in cap_comp.pads if p.net == rule.get("net")), None) if rule.get("net") else None
                    other_pad = next((p for p in cap_comp.pads if p is not power_pad), None) if power_pad else None
                    if power_pad is None or other_pad is None or len(cap_comp.pads) != 2:
                        px, py = _pin_point(rule)
                        chw, chh = cap_comp.world_half_extents()
                        gap = max(chw, chh) + margin_mm
                        box = None
                        for step in range(20):
                            ox, oy = px + dirx * (gap + step * 0.4), py + diry * (gap + step * 0.4)
                            cur_cx, cur_cy = cap_comp.world_center()
                            cap_comp.x += ox - cur_cx
                            cap_comp.y += oy - cur_cy
                            candidate_box = cap_comp.world_bbox()
                            if not any(_boxes_overlap(candidate_box, b, margin_mm) for b in placed_boxes):
                                box = candidate_box
                                break
                        placed_boxes.append(box or cap_comp.world_bbox())
                        handled.add(cap)
                        continue

                    if not cap_comp.rotation_locked:
                        # Axe des pastilles le plus ALIGNE sur le bord de l'IC (perpendiculaire
                        # a `dir`) : le grand cote fait face a l'IC.
                        def _score(rot: float) -> float:
                            pox, poy = _rotate_xy(power_pad.local_x, power_pad.local_y, rot)
                            oox, ooy = _rotate_xy(other_pad.local_x, other_pad.local_y, rot)
                            return abs((oox - pox) * latx + (ooy - poy) * laty)
                        base_rot = max(ALLOWED_ROTATIONS, key=_score)
                        cap_comp.rotation = (base_rot + 180) % 360 if (apply_mirror and cidx % 2 == 1) else base_rot
                    # Decalage (constant, ne depend pas de x/y) entre l'origine du composant et
                    # le CENTRE de son rectangle d'encombrement a cette rotation - sert a placer
                    # le CENTRE sur la grille 1D (pas une pastille precise, cf. bug du
                    # 2026-11-06 : ancrer la broche d'alimentation cassait l'espacement anti-
                    # recouvrement, qui suppose des centres regulierement espaces).
                    off_x = cap_comp.world_center()[0] - cap_comp.x
                    off_y = cap_comp.world_center()[1] - cap_comp.y
                    hw, hh = cap_comp.world_half_extents()
                    half_lat = hw if abs(latx) >= abs(laty) else hh
                    half_depth = hw if abs(dirx) >= abs(diry) else hh
                    placeable.append((cap_comp, lateral, off_x, off_y, half_lat, half_depth))

                # Passe 2 : pavage 1D EQUILIBRE (regression isotone, cf. _pack_1d_balanced) -
                # chaque element reste le plus pres possible de SA broche, l'ecart necessaire est
                # REPARTI entre les elements voisins au lieu d'etre cumule d'un seul cote (retour
                # utilisateur du 2026-11-06 : C27/C33 trop loin de leur broche, C30 idem).
                if placeable:
                    natives = [p[1] for p in placeable]
                    halves = [p[4] for p in placeable]
                    lat_positions = _pack_1d_balanced(natives, halves, margin_mm)
                    for (cap_comp, _lateral, off_x, off_y, _half_lat, half_depth), lat_pos in zip(placeable, lat_positions):
                        depth = edge_depth + half_depth
                        center_x = ic_cx + dirx * depth + latx * lat_pos
                        center_y = ic_cy + diry * depth + laty * lat_pos
                        cap_comp.x = center_x - off_x
                        cap_comp.y = center_y - off_y
                        placed_boxes.append(cap_comp.world_bbox())
                        handled.add(cap_comp.ref)
            cursor_x = max(b[2] for b in placed_boxes) + margin_mm * 2.0
            continue

        # "Position 1" (defaut) : le PETIT cote touche SA broche exacte, groupes par broche.
        pin_groups: Dict[Optional[str], List[dict]] = {}
        for rule in cap_rules:
            if rule["cap"] in handled:
                continue
            _ic2, pin = assignment[rule["cap"]]
            pin_groups.setdefault(pin, []).append(rule)

        ordered_groups = sorted(pin_groups.items(), key=lambda kv: "" if kv[0] is None else kv[0])
        if order_seed:
            random.Random(order_seed).shuffle(ordered_groups)

        for pin, group_rules in ordered_groups:
            pad = next((p for p in comp.pads if p.name == pin), None) if pin else None
            px, py = comp.pad_world_pos(pad) if pad is not None else (ic_cx, ic_cy)
            dirx, diry = _snap_cardinal(px - ic_cx, py - ic_cy)
            latx, laty = -diry, dirx   # axe perpendiculaire a `dir`
            lateral_cursor = 0.0
            depth_cursor = margin_mm
            for cidx, rule in enumerate(group_rules):
                cap = rule["cap"]
                cap_comp = board.components[cap]
                power_pad = next((p for p in cap_comp.pads if p.net == rule.get("net")), None) if rule.get("net") else None
                other_pad = next((p for p in cap_comp.pads if p is not power_pad), None) if power_pad else None
                if power_pad is None or other_pad is None or len(cap_comp.pads) != 2:
                    # Repli : polarite non lisible - position generique (centre colle a la
                    # broche, spirale anti-recouvrement).
                    chw, chh = cap_comp.world_half_extents()
                    gap = max(chw, chh) + margin_mm
                    box = None
                    for step in range(20):
                        ox, oy = px + dirx * (gap + step * 0.4), py + diry * (gap + step * 0.4)
                        cur_cx, cur_cy = cap_comp.world_center()
                        cap_comp.x += ox - cur_cx
                        cap_comp.y += oy - cur_cy
                        candidate_box = cap_comp.world_bbox()
                        if not any(_boxes_overlap(candidate_box, b, margin_mm) for b in placed_boxes):
                            box = candidate_box
                            break
                    placed_boxes.append(box or cap_comp.world_bbox())
                    handled.add(cap)
                    continue

                if not cap_comp.rotation_locked:
                    # L'autre pastille la plus ELOIGNEE de la broche dans la direction `dir` (le
                    # petit cote qui porte `power_pad` reste du cote de la broche, le corps
                    # s'etend vers l'exterieur du boitier).
                    def _score(rot: float) -> float:
                        pox, poy = _rotate_xy(power_pad.local_x, power_pad.local_y, rot)
                        oox, ooy = _rotate_xy(other_pad.local_x, other_pad.local_y, rot)
                        return (oox - pox) * dirx + (ooy - poy) * diry
                    base_rot = max(ALLOWED_ROTATIONS, key=_score)
                    cap_comp.rotation = (base_rot + 180) % 360 if (mirror_alt and cidx % 2 == 1) else base_rot
                pox, poy = _rotate_xy(power_pad.local_x, power_pad.local_y, cap_comp.rotation)

                for attempt in range(20):
                    target_x = px + dirx * depth_cursor + latx * lateral_cursor
                    target_y = py + diry * depth_cursor + laty * lateral_cursor
                    cap_comp.x = target_x - pox
                    cap_comp.y = target_y - poy
                    box = cap_comp.world_bbox()
                    if not any(_boxes_overlap(box, b, margin_mm) for b in placed_boxes):
                        break
                    depth_cursor += 0.4   # deja occupe : s'eloigne un peu plus dans `dir`
                placed_boxes.append(cap_comp.world_bbox())
                handled.add(cap)
                chw, chh = cap_comp.world_half_extents()
                # demi-largeur dans l'axe LATERAL (grand cote) : le petit cote est dans `dir`
                lateral_cursor += 2.0 * (chh if abs(dirx) >= abs(diry) else chw) + margin_mm
        cursor_x = max(b[2] for b in placed_boxes) + margin_mm * 2.0
    return handled


def score_decoupling_placement(board: Board, rules: List[dict]) -> dict:
    """Note un placement de condensateurs de decouplage DEJA pose sur `board` (fonction pure,
    ne modifie rien) : plus petit = mieux. Compromis demande par l'utilisateur le 2026-11-06
    ("il faut avoir des capacites globalement toutes proches et non pas des tres proches et
    des tres loin") - somme des distances condensateur -> broche + un terme d'ecart-type (penalise
    une distribution inegale, pas seulement la moyenne) + une grosse penalite par paire de
    condensateurs qui se recouvrent (ne devrait jamais arriver, sert de garde-fou)."""
    assignment = compute_decoupling_assignment(rules)
    dists: List[float] = []
    boxes: List[tuple] = []
    for r in rules:
        cap, ic = r["cap"], r["ic"]
        _ic2, pin = assignment.get(cap, (ic, None))
        ic_comp = board.components.get(ic)
        cap_comp = board.components.get(cap)
        if ic_comp is None or cap_comp is None:
            continue
        boxes.append(cap_comp.world_bbox())
        if pin is None:
            continue
        pad = next((p for p in ic_comp.pads if p.name == pin), None)
        if pad is None:
            continue
        pin_pos = ic_comp.pad_world_pos(pad)
        power_pad = next((p for p in cap_comp.pads if p.net == r.get("net")), None) if r.get("net") else None
        cap_pos = cap_comp.pad_world_pos(power_pad) if power_pad is not None else cap_comp.world_center()
        dists.append(math.hypot(cap_pos[0] - pin_pos[0], cap_pos[1] - pin_pos[1]))
    overlaps = sum(1 for i in range(len(boxes)) for j in range(i + 1, len(boxes))
                   if _boxes_overlap(boxes[i], boxes[j], 0.0))
    total = sum(dists)
    mean = total / len(dists) if dists else 0.0
    spread = (sum((d - mean) ** 2 for d in dists) / len(dists)) ** 0.5 if dists else 0.0
    return {"score": total + 2.0 * spread + 50.0 * overlaps, "total_dist": total,
            "max_dist": max(dists) if dists else 0.0, "spread": spread, "overlaps": overlaps}


def align_rows(board: Board, refs: List[str], margin_mm: float = 0.3, origin: tuple = (0.0, 0.0)) -> bool:
    """Range `refs` en rangees bien alignees (demande utilisateur du 2026-11-06 : les "tas"
    issus du seul placement par forces dirigees sont desordonnes). Rangees formees par
    proximite en y (cf. le classement issu du recuit, qui a deja regroupe les composants
    lies), puis chaque rangee posee cote a cote de gauche a droite ; les rangees sont
    empilees de haut en bas. Les centres d'une meme rangee partagent alors la meme ordonnee
    (alignement horizontal) et les rangees successives sont alignees sur le meme depart en x
    (alignement vertical du bord gauche). `origin` : coin haut-gauche de la grille resultante -
    permet de poser ce rangement a cote d'un autre groupe deja pose (ex. le bloc IC +
    decouplage de `place_active_and_decoupling`) sans le recouvrir. Ignore (renvoie False) un
    groupe qui contient une piece verrouillee : sa position est deja dictee par l'ancre, un
    realignement rigide la deplacerait a tort (cf. hierarchy.optimize_group) - et un groupe de
    moins de 2 composants (rien a aligner)."""
    movable = [r for r in refs if not board.components[r].fixed]
    if len(movable) != len(refs) or len(movable) < 2:
        return False
    ordered = sorted(movable, key=lambda r: board.components[r].world_center()[1])
    rows: List[List[str]] = []
    row_cy: List[float] = []
    for r in ordered:
        _, hh = board.components[r].world_half_extents()
        cy = board.components[r].world_center()[1]
        if rows and abs(cy - row_cy[-1]) < hh + margin_mm * 3.0:
            rows[-1].append(r)
            row_cy[-1] = sum(board.components[rr].world_center()[1] for rr in rows[-1]) / len(rows[-1])
        else:
            rows.append([r])
            row_cy.append(cy)
    for row in rows:
        row.sort(key=lambda r: board.components[r].world_center()[0])

    ox, oy = origin
    cursor_y = oy
    for row in rows:
        row_h = max(board.components[r].world_half_extents()[1] * 2.0 for r in row)
        row_center_y = cursor_y + row_h / 2.0
        cursor_x = ox
        for r in row:
            comp = board.components[r]
            hw, _hh = comp.world_half_extents()
            target_cx, target_cy = cursor_x + hw, row_center_y
            cur_cx, cur_cy = comp.world_center()
            comp.x += target_cx - cur_cx
            comp.y += target_cy - cur_cy
            cursor_x += hw * 2.0 + margin_mm
        cursor_y += row_h + margin_mm
    return True


def _local_wirelength(board: Board, ref: str) -> float:
    comp = board.components[ref]
    total = 0.0
    for pad in comp.pads:
        net = board.nets.get(pad.net)
        if net is None or len(net.pins) < 2:
            continue
        px, py = comp.pad_world_pos(pad)
        for other_ref, other_pad in net.pins:
            if other_ref == ref:
                continue
            pos = board.pad_world_pos(other_ref, other_pad)
            if pos is None:
                continue
            total += math.hypot(px - pos[0], py - pos[1])
    return total


def _try_best_rotation(board: Board, ref: str) -> None:
    comp = board.components[ref]
    if comp.fixed:
        return
    best_rot = comp.rotation
    best_cost = _local_wirelength(board, ref)
    for rot in ALLOWED_ROTATIONS:
        if rot == comp.rotation:
            continue
        comp.rotation = rot
        cost = _local_wirelength(board, ref)
        if cost < best_cost - 1e-6:
            best_cost = cost
            best_rot = rot
    comp.rotation = best_rot


def legalize(board: Board, refs: List[str], min_clearance_mm: float = 0.3, max_iters: int = 800) -> int:
    """Resorbe les chevauchements residuels en poussant chaque paire en recouvrement le long
    de l'axe de moindre penetration (algorithme de separation iteratif, cf. "legalisation +
    spread" de suggest_placement cote MCP KiCad, reimplemente ici pour tourner hors KiCad).
    Retourne le nombre d'iterations effectuees (utile pour diagnostiquer une carte trop
    dense pour converger)."""
    movable = [r for r in refs if not board.components[r].fixed]
    for it in range(max_iters):
        moved = False
        for a_idx, ra in enumerate(refs):
            ca = board.components[ra]
            ax0, ay0, ax1, ay1 = ca.world_bbox()
            for rb in refs[a_idx + 1:]:
                cb = board.components[rb]
                bx0, by0, bx1, by1 = cb.world_bbox()
                ox0, oy0 = max(ax0, bx0) - min_clearance_mm / 2.0, max(ay0, by0) - min_clearance_mm / 2.0
                ox1, oy1 = min(ax1, bx1) + min_clearance_mm / 2.0, min(ay1, by1) + min_clearance_mm / 2.0
                overlap_x = ox1 - ox0
                overlap_y = oy1 - oy0
                if overlap_x <= 0 or overlap_y <= 0:
                    continue
                moved = True
                a_can_move = ra in movable
                b_can_move = rb in movable
                if not a_can_move and not b_can_move:
                    continue
                if overlap_x < overlap_y:
                    push = overlap_x / 2.0 + 0.01
                    direction = 1.0 if ca.x <= cb.x else -1.0
                    if a_can_move and b_can_move:
                        ca.x -= direction * push
                        cb.x += direction * push
                    elif a_can_move:
                        ca.x -= direction * 2 * push
                    else:
                        cb.x += direction * 2 * push
                else:
                    push = overlap_y / 2.0 + 0.01
                    direction = 1.0 if ca.y <= cb.y else -1.0
                    if a_can_move and b_can_move:
                        ca.y -= direction * push
                        cb.y += direction * push
                    elif a_can_move:
                        ca.y -= direction * 2 * push
                    else:
                        cb.y += direction * 2 * push
        if not moved:
            return it
    return max_iters
