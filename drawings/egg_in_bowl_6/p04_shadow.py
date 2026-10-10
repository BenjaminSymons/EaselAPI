"""Pass 4: the bowl's interior shadow, right of and behind the egg, and the lost edge. Two
arcs run round the inside of the interior; three more hug the egg's right outline, the
first with its inner edge on the line, so the egg's shade and the bowl's shadow are two
tones of one value butting there. One stump over the shadow, then one stump dragged across
the join. The lit floor at the left gets its tone again: the first pass's 2H at 0.7
measured as paper."""

SW = 0.025                                 # 26 px arcs

# --- round the inside of the interior, the right half ------------------------------------
egg_clear = lambda x, y: in_egg(x, y, 18 * PX, 18 * PY)
for k in (0.5, 1.5):
    dx, dy = k * SW, k * SW * W / H
    for piece in cut_arc(interior(-75, 95, dx=dx, dy=dy, n=36), egg_clear, min_pts=5):
        s.line(piece, "2B", pressure=[0.12, 0.60, 0.75, 0.80, 0.80, 0.75, 0.12], tip="side",
               width=SW, smooth=False, note="subject")
# --- hugging the egg's right side: the first butts the outline -------------------------
int_clear = lambda x, y: not in_ellipse(x, y, IC, IR[0] - 10 * PX, IR[1] - 10 * PY)
for d, peak in ((6, 0.85), (32, 0.85), (58, 0.85), (84, 0.72), (110, 0.68)):
    # the first overlaps the outline by 7 px: the egg's own arc leaves a 5 px fringe of
    # paper inside it; the last two fill the middle, which the first rehearsal left light
    for piece in cut_arc(egg_arc(-60, 125, dx=-d * PX, dy=-d * PY, n=30), int_clear, min_pts=5):
        s.line(piece, "2B", pressure=[0.12, peak - 0.05, peak, peak, peak - 0.05, 0.12], tip="side",
               width=SW, smooth=False, note="subject")
print(s.look())
shadow_stump = polygon(interior(-72, 92, dx=0.004, dy=0.005, n=24)
                       + egg_arc(118, -48, dx=-0.004, dy=-0.005, n=24), name="shadow_stump")
s.stump(shadow_stump, strength=1.0)
# the lost edge: one stump dragged across the join, where the egg's shade meets the shadow
j0, j1 = egg_pt(35, dx=0.045, dy=0.040), egg_pt(35, dx=-0.045, dy=-0.040)
s.stump([j0, j1], strength=0.8, width=0.05)
print(s.look())

# --- the lit floor, again, leant on this time -------------------------------------------
floor_clear = lambda x, y: in_egg(x, y, 28 * PX, 28 * PY)
for k in (0.5, 1.3):
    dx, dy = k * 0.030, k * 0.040
    for piece in cut_arc(interior(95, 285, dx=dx, dy=dy, n=36), floor_clear, min_pts=5):
        s.line(piece, "2H", pressure=[0.2, 0.9, 0.9, 0.6, 0.9, 0.9, 0.2], tip="side",
               width=0.03, smooth=False, note="subject")
floor_stump = polygon(interior(92, 288, dx=0.004, dy=0.005, n=30)
                      + egg_arc(255, 115, dx=-0.016, dy=-0.021, n=20), name="floor_stump")
s.stump(floor_stump, strength=1.0)
print(s.look())
