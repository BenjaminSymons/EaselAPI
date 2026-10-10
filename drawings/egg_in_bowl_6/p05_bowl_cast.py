"""Pass 5: the bowl's shadow on the table, to its lower right. Arcs of the shadow's own
outline drawn in toward the bowl's foot, cut where they pass under the bowl, HB over the
2H ground, darker toward the foot and fading at the far edge; one stump over the shadow
and not over the bowl."""

FOCUS = (0.64, 0.76)                       # inside the bowl's foot: the arcs shrink toward it
outer = [(0.81, 0.62), (0.87, 0.68), (0.90, 0.74), (0.89, 0.80), (0.83, 0.845),
         (0.70, 0.865), (0.55, 0.855), (0.44, 0.825), (0.38, 0.79)]


def densify(points, n=6):
    out = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
    return out + [points[-1]]


dense = densify(outer)
bowl_clear = lambda x, y: in_bowl(x, y, 14 * PX, 14 * PY)
for sc, peak in ((0.94, 0.55), (0.84, 0.65), (0.74, 0.75), (0.64, 0.85), (0.54, 0.92),
                 (0.44, 0.95), (0.34, 0.95)):
    ring = [(FOCUS[0] + sc * (x - FOCUS[0]), FOCUS[1] + sc * (y - FOCUS[1])) for (x, y) in dense]
    for piece in cut_arc(ring, bowl_clear, min_pts=4):
        s.line(piece, "HB", pressure=[0.12, peak - 0.05, peak, peak, peak - 0.05, 0.12],
               tip="side", width=0.03, smooth=False, note="bowl shadow on the table")
print(s.look())
cast_stump = polygon(outer + body(110, 15, dx=-15 * PX, dy=-15 * PY, n=24), name="cast_stump")
s.stump(cast_stump, strength=1.0)
print(s.look())
