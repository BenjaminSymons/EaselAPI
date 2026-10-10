"""Pass 6: the edges, last but one. The one hard edge is the bowl's far rim against the
table, laid as the guide's three strokes where the band beside it is speckled: a 20 px
stroke 8 px out, a stump along it, and the 13 px edge last with its centre 2 px outside
the line, in the table's own value (a 2H held to the pressure that reads as the table, not
leant on). The egg's crown against the table gets the 13 px stroke alone, lighter."""

crown_clear = lambda x, y: in_egg(x, y, 10 * PX, 10 * PY)
FAR = (185, 355)
for piece in cut_arc(rim(*FAR, dx=-8 * PX, dy=-8 * PY, n=60), crown_clear, min_pts=4):
    s.line(piece, "2H", pressure=[0.2, 0.78, 0.78, 0.78, 0.2], tip="side", width=0.02,
           smooth=False, note="edge")
for piece in cut_arc(rim(*FAR, dx=-10 * PX, dy=-10 * PY, n=60), crown_clear, min_pts=4):
    s.stump(piece, strength=0.8, width=0.03)
print(s.look())
for piece in cut_arc(rim(*FAR, dx=-2 * PX, dy=-2 * PY, n=60), crown_clear, min_pts=4):
    s.line(piece, "2H", pressure=[0.3, 0.8, 0.8, 0.8, 0.3], tip="side", width=0.013,
           smooth=False, note="edge")
# the egg's crown against the table: the narrow stroke alone, held off
bowl_clear = lambda x, y: in_bowl(x, y, 6 * PX, 6 * PY)
for piece in cut_arc(egg_arc(200, 340, dx=-2 * PX, dy=-2 * PY, n=40), bowl_clear, min_pts=4):
    s.line(piece, "2H", pressure=[0.25, 0.7, 0.7, 0.7, 0.25], tip="side", width=0.013,
           smooth=False, note="edge")
print(s.look())

# the lost edge, behind the egg: the egg's outline arc and the shadow's first hugging arc
# overlap into a darker line (seen in the no-sketch rehearsal), so three more stumps are
# dragged across the join where the bowl's shadow stands behind the egg
for t in (-30, -5, 20):
    s.stump([egg_pt(t, dx=0.045, dy=0.040), egg_pt(t, dx=-0.045, dy=-0.040)], strength=0.8, width=0.05)
# the lighter wedge in the interior shadow, between the arcs round the inside and the arcs
# hugging the egg: two short strokes along the inside, and one small stump
s.line(interior(-45, 45, dx=0.035, dy=0.048, n=16), "2B", pressure=[0.15, 0.7, 0.7, 0.15],
       tip="side", width=0.03, smooth=False, note="subject")
s.line(interior(-30, 30, dx=0.060, dy=0.075, n=12), "2B", pressure=[0.15, 0.65, 0.65, 0.15],
       tip="side", width=0.03, smooth=False, note="subject")
s.stump(polygon(interior(-50, 50, dx=0.02, dy=0.028, n=16) + [(0.655, 0.605), (0.655, 0.550)],
                name="wedge_stump"), strength=0.8)
print(s.look())
print(s.look(sketch=False))
