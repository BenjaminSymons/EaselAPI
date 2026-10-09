"""Pass 6: darks last, unstumped. The egg's cast shadow inside the bowl.

The first rehearsal laid the shadow as concentric arcs of the shifted shape, and their
ends in the open stepped down the right side as a staircase: a wedge, not a shadow.
So now each arc is attached to the egg: it starts and ends on the egg's lower-right
outline and bulges out toward the shadow's outer line in the middle, `u` saying how far.
The ends land inside the egg's keep-out and are cut there, 2B leant on for the outer
arcs and 4B at full pressure for the core next to the egg; one 4B arc along the
contact under the egg; and one stump along the outer edge alone, so the penumbra is
soft and the core is left as laid."""

T0, T1 = 8, 147


def shadow_arc(u, step=3.0):
    pts = []
    t = T0
    while t <= T1 + 1e-9:
        e = eggpt(t, 1.0)
        c = ept(CX2, CY2, CRX2, CRY2, t, CROT2, 1.0)
        w = math.sin(math.pi * (t - T0) / (T1 - T0))
        pts.append((e[0] + u * w * (c[0] - e[0]), e[1] + u * w * (c[1] - e[1])))
        t += step
    return pts


within = interior_inset(6)
# Seven arcs at width 0.028: the second rehearsal's five at 0.022 only touched, and
# showed as ribs.
for u, grade, peak in ((0.97, "2B", 0.80), (0.86, "2B", 1.00), (0.74, "2B", 1.00),
                       (0.62, "4B", 0.95), (0.50, "4B", 1.00), (0.38, "4B", 1.00),
                       (0.27, "4B", 1.00)):
    pts = shadow_arc(u)
    for run_pts, run_prs in cut(pts, bell(len(pts), peak, 0.5), [egg_keepout_20],
                                within=within, min_px=30):
        s.line(run_pts, grade, pressure=run_prs, tip="side", width=0.028, smooth=False,
               note="subject: cast shadow")
s.look(path="out/p06_look_01_cast.png")

core = arc(EX, EY, ERX + 12 / W, ERY + 12 / H, 22, 128, EROT)
s.line(core, "4B", pressure=bell(len(core), 1.0, 0.5), tip="side", width=0.024,
       smooth=False, note="subject: cast shadow core, under the egg")
edge = shadow_arc(1.04)                 # the stump's ends held off the egg's outline
for run_pts, _ in cut(edge, [1.0] * len(edge), [egg_keepout_20], min_px=30):
    s.stump(run_pts, strength=0.8, width=0.03, note="subject: the shadow's outer edge, soft")
print(s.look(path="out/p06_after.png"))
print(s.look(region="B5:G7", scale=None, path="out/p06_after_crop.png"))
print(s.budget_line())
print(s.compare(s.plan()))
