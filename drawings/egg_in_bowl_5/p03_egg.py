"""Pass 3: the egg. Its shadow side as arcs of its own outline scaled inward, each
shorter than the one before so that their ends trace the terminator; the outermost
lighter than the core (reflected light from the bowl), the innermost a 2H half-tone
turning into the light. One stump held to the shade polygon and one along the
terminator. Then the far inner wall, two 2H arcs held off, so the egg's paper crown
stands against something.

Rehearsed twice: the first read egg_shade 0.67 against 0.45 (the arcs narrowed faster
than the place, the stump lifted the rest) and took 18% of the light's paper with two
half-tone arcs laid inside egg_lit as it was then drawn.
"""
laid = 0
cx, cy, a, b = EGG


def egg_arc(scale, t0, t1, grade, pressure, width=0.024, note="subject egg"):
    global laid
    s.line(egg_pts(cx, cy, a, b, t0, t1, scale=scale, step=4), grade, pressure=pressure,
           tip="side", width=width, smooth=False, note=note)
    laid += 1


egg_arc(0.85, -40, 170, "HB", [0.35, 0.7, 0.85, 0.75, 0.35], width=0.02)  # the turn, reflected light
egg_arc(0.73, -34, 162, "2B", [0.35, 0.8, 0.9, 0.8, 0.35])               # the core
egg_arc(0.60, -26, 150, "2B", [0.35, 0.8, 0.9, 0.8, 0.35])
egg_arc(0.47, -14, 134, "HB", [0.35, 0.85, 1.0, 0.9, 0.35])
egg_arc(0.36, 0, 116, "2H", [0.4, 0.9, 1.0, 0.9, 0.4])                   # the half-tone
egg_arc(0.28, 14, 100, "2H", [0.4, 0.75, 0.75, 0.4])
# the core again, since the stump will lift it: a 2B twice is the darkest half-tone
egg_arc(0.73, -30, 158, "2B", [0.35, 0.85, 0.9, 0.85, 0.35])
egg_arc(0.60, -22, 146, "2B", [0.35, 0.85, 0.9, 0.85, 0.35])
print(s.look(region="C4:G7", scale=None, path="out/p03_look_01_crop.png"))
s.stump(egg_shade, strength=0.6, note="egg stump")
s.stump(egg_pts(cx, cy, a, b, -10, 126, scale=0.36, step=4), strength=0.6, width=0.035,
        note="terminator stump")

# the far inner wall, lit but not paper: 2H held off, two arcs, stumped twice
for k, pr in ((0.94, [0.3, 0.5, 0.55, 0.5, 0.3]), (0.87, [0.3, 0.45, 0.5, 0.45, 0.3])):
    s.line(ell_pts(512, 439, 275 * k, 98 * k, 192, 348), "2H", pressure=pr, tip="side",
           width=0.03, smooth=False, note="far wall")
    laid += 1
s.stump(ell_pts(512, 439, 250, 88, 192, 348), strength=1.0, width=0.05, note="far wall stump")
s.stump(ell_pts(512, 439, 250, 88, 192, 348), strength=1.0, width=0.05, note="far wall stump")
print("laid:", laid)
print(s.look(region="C4:G7", scale=None, path="out/p03_look_02_crop.png"))
print(s.look(path="out/p03_look_02.png"))
print(s.compare({egg_shade: 0.45, egg_lit: 0.93, bowl_lit: 0.90, bowl_shadow: 0.45},
                path="out/p03_compare.png"))
