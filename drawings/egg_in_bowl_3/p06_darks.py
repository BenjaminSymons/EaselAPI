"""Pass 6: darks last, unstumped. The core of the bowl's cast shadow under its
lower-right wall (6B, plan 0.18, the drawing's dark); the egg's contact shadow (4B); the
egg's cast core (4B); the bowl's bottom-left contact with the table (HB)."""
since = len(s.history.records)

# the bowl's cast core: three overlapping 6B strokes along the outer wall's lower-right
# arc, 14 px apart at 41 px wide so they close into one dark, their ends fading to
# nothing; the first sits 20 px out so its half-width stays off the wall
for gx, gy, top, t0, t1 in ((0.020, 0.027, 0.72, 16, 80), (0.034, 0.045, 0.72, 18, 76),
                            (0.048, 0.064, 0.60, 22, 70)):
    pts = ell_pts(OUTER_C, OUTER_RX + gx, OUTER_RY + gy, t0, t1, step=3)
    s.line(pts, "6B", pressure=bell(len(pts), top, ends=0.0, power=0.8), tip="side",
           width=0.04, smooth=False, note="bowl cast core")
print(s.look(region="E6:H8", scale=None, path="out/p06_core.png"))

# the egg's contact shadow: a 4B along its lower outline, centre 5 px below it, thin
pts = ell_pts(EGG_C, EGG_RX + 0.005, EGG_RY + 0.007, 35, 112, step=4, rot=EGG_ROT, egg=EGG_E)
s.line(pts, "4B", pressure=bell(len(pts), 0.85, ends=0.0, power=0.8), tip="side", width=0.009,
       smooth=False, note="subject egg contact")
# the egg's cast core, along the cast's lower arc, outside the egg
pts = ell_pts(CAST_C, CAST_RX, CAST_RY, 20, 125, step=4, rot=CAST_ROT, k=0.66)
for run in runs_outside(pts, egg_tight):
    s.line(run, "4B", pressure=bell(len(run), 0.8, ends=0.0, power=0.8), tip="side",
           width=0.014, smooth=False, note="subject egg cast core")
# the bowl's bottom-left contact with the table
pts = ell_pts(OUTER_C, OUTER_RX + 0.005, OUTER_RY + 0.007, 100, 172, step=3)
s.line(pts, "HB", pressure=bell(len(pts), 0.9, ends=0.0, power=0.8), tip="side", width=0.012,
       smooth=False, note="bowl contact")
print(s.look(region="D4:G7", scale=None, path="out/p06_egg_darks.png"))
print(s.look(path="out/p06_whole.png"))
print(s.look(scale=256, path="out/p06_small.png"))
print(s.compare(s.plan(), path="out/p06_compare.png"))
print(s.budget_line())
