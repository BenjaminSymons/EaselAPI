"""Pass 2: a repair. The table's band along the far rim ran over the egg's crown where it
stands above the rim, and the lit side of the egg is meant to be paper never touched.
A plastic eraser twice over the sliver of egg above the rim, and nothing else under the
place: the crown lifts to within a few hundredths of the paper, and its clean edge
draws the egg's top against the table.

Budget for the pass: 2.
"""
before = len(s.history.records)


def rim_far_y(x):
    """The far rim's edge at pixel x, in pixels; None outside the rim."""
    dx = (x - BOWL_CX) / RIM_RX
    if abs(dx) >= 1.0:
        return None
    return BOWL_CY - RIM_RY * math.sqrt(1.0 - dx * dx)


# the egg's outline above the rim's far edge, with a pixel of grace
above = []
for t in range(0, 360):
    x, y = egg_pt(t)
    px, py = x * W, y * H
    ry = rim_far_y(px)
    if ry is not None and py < ry - 1.0:
        above.append((t, (x, y)))
ts = [t for t, _ in above]
ts = _run(ts)
crown_outline = [egg_pt(t) for t in ts]
# close it along the rim's far edge, from the last point back to the first
x_last, x_first = crown_outline[-1][0] * W, crown_outline[0][0] * W
n = 24
closing = []
for i in range(n + 1):
    px = x_last + (x_first - x_last) * i / n
    closing.append(U(px, rim_far_y(px) - 1.0))
crown = polygon(crown_outline + closing, name="egg_crown")
print("crown box:", crown.box)

s.plastic(crown, note="lift the table off the egg's crown")
s.plastic(crown, note="lift the table off the egg's crown, second pass")
print(s.look(region="C4:F5", scale=None, path="out/p02_crown.png"))
print(s.report(since=before))
print(s.compare(s.plan(), path="out/p02_compare.png"))
