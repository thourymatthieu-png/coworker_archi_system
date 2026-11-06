import sys, pcbnew
b = pcbnew.LoadBoard(sys.argv[1]); out = []
for fp in b.GetFootprints():
    cy = fp.GetCourtyard(pcbnew.F_CrtYd)
    if cy.OutlineCount() == 0:
        out.append((fp.GetReference(), "sans courtyard")); continue
    bb = cy.BBox()
    worst = 0
    for p in fp.Pads():
        pb = p.GetBoundingBox()
        d = max(bb.GetLeft() - pb.GetLeft(), pb.GetRight() - bb.GetRight(), bb.GetTop() - pb.GetTop(), pb.GetBottom() - bb.GetBottom())
        worst = max(worst, pcbnew.ToMM(d))
    if worst > 0.01:
        out.append((fp.GetReference(), f"pastille hors courtyard de {worst:.2f} mm"))
for r in out: print(*r)
print(len(out), "empreintes concernees")
