"""Pass 4: the bowl's near wall, the sliver under the rim: three arcs blended between
the rim's lower half and the silhouette's, 2H leant on at the shade end on the right and
held off toward the light on the left, one stump along the middle one. And two stumps
along the lit end of the interior, cut round the egg, to close the 2H arcs' holes that
the egg pass's crop showed as speckle."""


def blend(u, t0=25, t1=155):
    r, sl = rimarc(t0, t1), silarc(t0, t1)
    return [(a[0] * (1 - u) + b[0] * u, a[1] * (1 - u) + b[1] * u) for a, b in zip(r, sl)]


def eased(prs):
    prs = list(prs)
    for i, f in ((0, 0.4), (1, 0.7), (-1, 0.4), (-2, 0.7)):
        prs[i] *= f
    return prs


for u in (0.3, 0.55, 0.8):
    pts = blend(u)
    s.line(pts, "2H", pressure=eased(ramp(len(pts), 1.0, 0.5)), tip="side", width=0.016,
           smooth=False, note="wall")
s.stump(blend(0.55), strength=0.8, width=0.025, note="wall closed")
s.look(path="out/p04_look_01_wall.png")

egg_keepout_45 = grown(EGG, 25.0, EROT)        # a stump at width 0.045: half is 23 px
for inset in (22, 60):
    path = intarc_px(112, 248, inset)
    for run_pts, _ in cut(path, [1.0] * len(path), [egg_keepout_45], min_px=40):
        s.stump(run_pts, strength=1.0, width=0.045, note="bowl lit closed again")

# The two bands beside the egg, closed: the first rehearsal of this pass left the lit
# band as a speckled halo and the shade band as a dark ring where it doubled the arcs.
s.stump(arc(EX, EY, ERX + 20 / W, ERY + 20 / H, 125, 305, EROT), strength=1.0, width=0.03,
        note="floor beside the egg closed, lit")
s.stump(arc(EX, EY, ERX + 12 / W, ERY + 12 / H, -75, 135, EROT), strength=1.0, width=0.035,
        note="subject: floor beside the egg closed, shade")
print(s.look(path="out/p04_after.png"))
print(s.look(region="B5:G7", scale=None, path="out/p04_after_crop.png"))
print(s.budget_line())
print(s.compare(s.plan()))
