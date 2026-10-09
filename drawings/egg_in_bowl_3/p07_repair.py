"""Pass 7: the passage I would apologise for, and the budget's remainder. Without the
envelope the egg's lit side dissolves into the lit floor and its left end has no edge
at all. Three marks: a 2H half-tone along the egg's lower-left outline just inside it,
and the floor's occlusion against the egg's lower-left just outside it, both fading to
nothing, so the egg's left end is found by a half-tone and not an outline. Then the
second stump the guide allows over a large plane's mottle, in pieces that avoid the
bowl and the darks."""
since = len(s.history.records)

# the egg's lower-left: a half-tone inside the outline, the occlusion outside it
pts = egg_arc(0.95, 95, 172, step=4)
s.line(pts, "2H", pressure=bell(len(pts), 0.80, ends=0.0, power=0.8), tip="side", width=0.012,
       smooth=False, note="subject egg half-tone")
pts = ell_pts(EGG_C, EGG_RX + 0.007, EGG_RY + 0.009, 100, 185, step=4, rot=EGG_ROT, egg=EGG_E)
s.line(pts, "2H", pressure=bell(len(pts), 0.95, ends=0.0, power=0.8), tip="side", width=0.012,
       smooth=False, note="subject floor against egg")
pts = ell_pts(EGG_C, EGG_RX + 0.018, EGG_RY + 0.024, 105, 180, step=4, rot=EGG_ROT, egg=EGG_E)
s.line(pts, "2H", pressure=bell(len(pts), 0.70, ends=0.0, power=0.8), tip="side", width=0.016,
       smooth=False, note="subject floor against egg")
print(s.look(region="C4:F6", scale=None, path="out/p07_egg_left.png"))

# the second stump over the table, in pieces: the far plane to the bowl's top, the left
# column, the near-left, the strip below the cast shadow, the right column above it
for name, box in (("far", (0.0, 0.0, 1.0, 0.40)), ("left", (0.0, 0.40, 0.185, 1.0)),
                  ("near-left", (0.185, 0.785, 0.56, 1.0)), ("below cast", (0.56, 0.84, 1.0, 1.0)),
                  ("right", (0.825, 0.40, 1.0, 0.59))):
    x0, y0, x1, y1 = box
    s.stump(polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]), strength=0.6,
            note=f"table second stump, {name}")
print(s.look(path="out/p07_whole.png"))
print(s.look(scale=256, sketch=False, path="out/p07_small.png"))
print(s.compare(s.plan(), path="out/p07_compare.png"))
print(s.budget_line())
