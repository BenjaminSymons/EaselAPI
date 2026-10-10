"""Pass 7: the darks, last, after every stump near them, and left unstumped. The egg's cast
shadow on the bowl's floor: three 6B arcs hugging the egg's lower right, their lists
falling under 0.15 at the ends; a 6B line where the egg meets the floor; the contact
shadow under the bowl's right foot in 4B."""

int_clear = lambda x, y: not in_ellipse(x, y, IC, IR[0] - 6 * PX, IR[1] - 6 * PY)
for d, t0, t1 in ((6, 15, 115), (20, 22, 112), (34, 30, 108), (48, 40, 103)):
    # 14 px apart at 31 px wide, one mass not stripes; each shorter than the last, so the
    # ends trace a tapering tip instead of stacking as steps
    for piece in cut_arc(egg_arc(t0, t1, dx=-d * PX, dy=-d * PY, n=24), int_clear, min_pts=4):
        s.line(piece, "6B", pressure=[0.05, 0.4, 0.85, 0.9, 0.9, 0.85, 0.4, 0.05], tip="side",
               width=0.03, smooth=False, note="subject")
s.line(egg_arc(60, 125, dx=-3 * PX, dy=-3 * PY, n=16), "6B", pressure=[0.08, 0.8, 0.8, 0.08],
       tip="side", width=0.012, smooth=False, note="subject")
print(s.look())
for d, t0, t1 in ((5, 15, 105), (16, 20, 100)):     # overlapping, one band under the foot
    s.line(body(t0, t1, dx=-d * PX, dy=-d * PY, n=24), "4B",
           pressure=[0.05, 0.4, 0.75, 0.85, 0.75, 0.4, 0.05], tip="side", width=0.025,
           smooth=False, note="bowl shadow on the table")
print(s.look())
print(s.look(sketch=False))
