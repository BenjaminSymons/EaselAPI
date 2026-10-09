"""Pass 3: the egg. Cross-contour arcs of its own outline scaled inward over the shadow
side, each shorter than the one before so that their ends trace the terminator, grading
from HB leant on at the core out to 2H half-tones toward the light; one stump over the
shade; the core a 2B laid after the stump. The lit side is paper no line crosses. The
lost edge is the egg's upper-right outline into the crescent: the gap the crescent left
round the egg is filled along the outline in the crescent's own value, and one stump
goes across the join."""
since = len(s.history.records)
EGG_W = 0.012

# (k, grade, top pressure, t0, t1): the ends trace the terminator from top-right to
# bottom-left; the core sits just inside the outline, reflected light at the outline
arcs = [(0.97, "HB", 0.70, -65, 125),
        (0.90, "HB", 0.95, -59, 118),
        (0.83, "HB", 1.00, -53, 111),
        (0.76, "HB", 1.00, -47, 104),
        (0.69, "HB", 1.00, -41, 97),
        (0.62, "HB", 0.80, -34, 90),
        (0.55, "2H", 0.85, -27, 82),            # the half-tone that turns into the light
        (0.47, "2H", 0.70, -18, 72)]
laid = 0
for k, grade, top, t0, t1 in arcs:
    pts = egg_arc(k, t0, t1, step=4)
    s.line(pts, grade, pressure=bell(len(pts), top, ends=0.25, power=0.5), tip="side",
           width=EGG_W, smooth=False, note="subject egg shade")
    laid += 1
    if laid == 4:
        print(s.look(region="D4:F6", scale=None, path="out/p03_arcs_4.png"))
print(s.look(region="D4:F6", scale=None, path="out/p03_arcs.png"))

# one stump over the shade, worked every way, and one along the terminator
s.stump(polygon(egg_arc(0.995, -70, 130, step=4) + egg_arc(0.40, 130, -70, step=4)),
        strength=0.8, note="subject egg shade")
term = ([egg_arc(k, t0, t0)[0] for k, _, _, t0, _ in arcs]
        + [egg_arc(k, t1, t1)[0] for k, _, _, _, t1 in reversed(arcs)])
s.stump(term, strength=0.5, width=0.025, note="subject terminator")
print(s.look(region="D4:F6", scale=None, path="out/p03_stumped.png"))

# the core, after the stump, left unstumped
pts = egg_arc(0.84, -50, 108, step=4)
s.line(pts, "2B", pressure=bell(len(pts), 0.80, ends=0.2, power=0.5), tip="side",
       width=0.014, smooth=False, note="subject egg core")

# the lost edge: fill the crescent's gap round the egg's upper right along the outline,
# in the crescent's value, then one stump over a band that straddles the join
for gk, top in ((1.09, 0.70), (1.19, 0.60)):
    pts = ell_pts(EGG_C, EGG_RX * gk, EGG_RY * gk, -62, 2, step=4, rot=EGG_ROT, egg=EGG_E)
    s.line(pts, "2B", pressure=bell(len(pts), top, ends=0.2, power=0.5), tip="side",
           width=0.016, smooth=False, note="subject lost edge")
join = polygon(egg_arc(0.86, -58, 4, step=4)
               + ell_pts(EGG_C, EGG_RX * 1.28, EGG_RY * 1.28, 4, -58, step=4,
                         rot=EGG_ROT, egg=EGG_E), name="join")
s.stump(join, strength=0.8, note="subject lost edge")
print(s.look(region="D4:F6", scale=None, path="out/p03_lost_edge.png"))
print(s.look(path="out/p03_whole.png"))
print(s.compare(s.plan(), path="out/p03_compare.png"))
print(s.budget_line())
