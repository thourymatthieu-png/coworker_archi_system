"""Regles `eloigner` et `bord` : valeur du depassement et parite cout incremental / total_cost.
Aucun placement n'est lance (carte synthetique, deplacements aleatoires). Lancer :
    python modules/kicad/tools/pcb_placement/tests/test_regles_eloigner_bord.py"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pcb_placement.cost import CostWeights, eloigner_excess, bord_excess, total_cost  # noqa: E402
from pcb_placement.incremental import IncrementalCost  # noqa: E402
from pcb_placement.model import Board, Component, Net, Pad  # noqa: E402


def comp(ref, x, y, w=2.0, h=2.0):
    return Component(ref=ref, value="", block="B", is_anchor=False, courtyard_w=w, courtyard_h=h,
                     courtyard_offset_x=0, courtyard_offset_y=0,
                     pads=[Pad("1", "N", -0.5, 0), Pad("2", "N", 0.5, 0)], x=x, y=y)


def board():
    cs = {r: comp(r, 10 + 4 * i, 10 + 3 * (i % 3)) for i, r in enumerate(["A1", "A2", "B1", "B2", "C1", "C2"])}
    b = Board(components=cs, nets={"N": Net("N", [(r, "1") for r in cs] + [("C1", "2")])})
    b.outline = (0.0, 0.0, 50.0, 40.0)
    b.decoupling_rules = [
        {"kind": "eloigner", "id": "I-T", "a": ["A1", "A2"], "b": ["B1", "B2"], "dmin": 8.0},
        {"kind": "bord", "ref": "C1", "cote": "ouest", "dmax": 1.0},
        {"kind": "bord", "ref": "C2", "cote": None, "dmax": 0.0},
    ]
    return b


def main():
    b = board()
    # valeurs attendues a la main
    b.components["A1"].x, b.components["A1"].y = 10, 10
    b.components["B1"].x, b.components["B1"].y = 15, 10    # ecart boites = 5 - 2 = 3 mm -> manque 5
    b.components["A2"].x, b.components["A2"].y = 100, 100  # loin de tous les B : 0
    b.components["B2"].x, b.components["B2"].y = -100, -100
    assert abs(eloigner_excess(b, b.decoupling_rules[0]) - 5.0) < 1e-9
    b.components["C1"].x = 4.0                              # bbox x0 = 3 -> ecart 3, dmax 1 -> 2
    assert abs(bord_excess(b, b.decoupling_rules[1]) - 2.0) < 1e-9
    b.components["C1"].x = -0.5                             # deborde a l'ouest : respecte
    assert bord_excess(b, b.decoupling_rules[1]) == 0.0
    b.components["C2"].x, b.components["C2"].y = 25, 20     # ecart min = 19 (nord) -> 19
    assert abs(bord_excess(b, b.decoupling_rules[2]) - 19.0) < 1e-9

    # parite incrementale
    rng = random.Random(1)
    b = board()
    refs = list(b.components)
    w = CostWeights(decoupling=10.0)
    ic = IncrementalCost(b, refs, b.nets, w)
    worst = 0.0
    for _ in range(300):
        moved = rng.sample(refs, rng.choice([1, 1, 2]))
        for r in moved:
            c = b.components[r]
            c.x, c.y = rng.uniform(-2, 52), rng.uniform(-2, 42)
        bd = ic.propose(moved)
        ic.commit()
        ref_cost = total_cost(b, refs, b.nets, w)
        worst = max(worst, abs(bd.decoupling_mm - ref_cost.decoupling_mm))
    print(f"ecart max de depassement incremental / complet : {worst:.2e} mm")
    assert worst < 1e-6
    print("OK")


if __name__ == "__main__":
    main()
