"""Pass 4: the two cast shadows, each as arcs of its own shape. The egg's, on the bowl's
floor to its lower right (2B, plan 0.34), cut round the egg; the bowl's, on the table
to its lower right (2B leant on, plan 0.30), cut round the bowl. One stump each. The
cores come in the darks pass, after these stumps."""
since = len(s.history.records)

# --- the egg's cast shadow: the lower arcs of its ellipse, stepped inward unevenly
for k in (1.0, 0.80, 0.56, 0.34):
    pts = ell_pts(CAST_C, CAST_RX, CAST_RY, 5, 175, step=5, rot=CAST_ROT, k=k)
    for run in runs_outside(pts, egg_tight):
        s.line(run, "2B", pressure=bell(len(run), 0.72, ends=0.15, power=0.5), tip="side",
               width=0.016, smooth=False, note="subject egg cast")
print(s.look(region="D4:G7", scale=None, path="out/p04_egg_cast.png"))
s.stump(egg_cast_seen, strength=0.6, note="subject egg cast")
print(s.look(region="D4:G7", scale=None, path="out/p04_egg_cast_stumped.png"))

# --- the bowl's cast shadow: arcs of its ellipse scaled inward, outside the bowl
hold = bowl_sil(0.004, 0.005)
laid = 0
for k in (1.0, 0.86, 0.70, 0.56, 0.40, 0.26):
    pts = ell_pts(BCAST_C, BCAST_RX, BCAST_RY, -100, 260, step=4, rot=BCAST_ROT, k=k)
    for run in runs_outside(pts, hold):
        s.line(run, "2B", pressure=bell(len(run), 0.92, ends=0.2, power=0.5), tip="side",
               width=0.024, smooth=False, note="bowl cast")
        laid += 1
print(s.look(region="E5:H8", scale=None, path="out/p04_bowl_cast.png"))
s.stump(bowl_cast_seen, strength=0.9, note="bowl cast")
print(s.look(region="E5:H8", scale=None, path="out/p04_bowl_cast_stumped.png"))
print(s.look(path="out/p04_whole.png"))
print(s.compare(s.plan(), path="out/p04_compare.png"))
print(s.budget_line())
