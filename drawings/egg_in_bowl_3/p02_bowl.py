"""Pass 2: the bowl. Each curved passage along its own shape: the lit interior as arcs
of the inner ellipse scaled inward (2H, plan 0.82), the interior shadow crescent as the
same arcs over the far and right wall (HB leant on, plan 0.46), the outer wall as arcs
between the rim's and the outer's lower arcs (HB, plan 0.58), the right of the lip a
single faint 2H. Every arc is cut round the egg. Stumps: over the lit floor, along the
crescent, along the wall; the crescent's inner boundary softened once."""
since = len(s.history.records)
ARC_W = 0.02


def lay_arc(pts, grade, top, ends=0.25, width=ARC_W, note="", ramp_to=None):
    n = len(pts)
    if ramp_to is None:
        plist = bell(n, top, ends=ends, power=0.6)
    else:                                   # along the arc from `top` to `ramp_to`, faded ends
        fade = bell(n, 1.0, ends=0.35, power=0.5)
        base = ramp(n, top, ramp_to)
        plist = [b * f for b, f in zip(base, fade)]
    s.line(pts, grade, pressure=plist, tip="side", width=width, smooth=False, note=note)


# --- the lit interior: lower-left arcs, outside the crescent and round the egg, and
# two level strokes along the flat of the floor left of the egg
laid = 0
for k in (0.97, 0.87, 0.77, 0.67):
    pts = ell_pts(INNER_C, INNER_RX, INNER_RY, 35, 255, step=4, k=k)
    for run in runs_outside(pts, int_shade):
        for r2 in runs_outside(run, egg_grown):
            lay_arc(r2, "2H", 0.70, ends=0.35, note="interior lit")
            laid += 1
for y in (0.535, 0.575):
    pts = [(0.27 + 0.16 * i / 8, y) for i in range(9)]
    for run in runs_outside(pts, egg_grown):
        lay_arc(run, "2H", 0.65, ends=0.3, width=0.03, note="interior lit")
        laid += 1
print(s.look(path="out/p02_int_lit.png"))
s.stump(polygon(ell_pts(INNER_C, INNER_RX, INNER_RY, 95, 265, step=4)
                + [(0.43, 0.45), (0.43, 0.66)]), strength=1.0, note="interior lit")
s.stump(polygon(ell_pts(INNER_C, INNER_RX, INNER_RY, 15, 140, step=4, k=0.99)
                + ell_pts(INNER_C, INNER_RX, INNER_RY, 140, 15, step=4, k=0.45)),
        strength=0.8, note="interior lit, the near floor")
print(s.look(path="out/p02_int_lit_stumped.png"))

# --- the interior shadow: arcs over the far and right wall, their reach shrinking
# with the crescent's own thickness, cut round the egg
THICK = 0.64                                  # the crescent's thickness at its thickest, of the radius
for k in (0.97, 0.89, 0.81, 0.73, 0.65, 0.57, 0.49, 0.42):
    reach = math.degrees(math.acos(min(1.0, (1 - k) / THICK)))
    t0, t1 = -75 - reach, -75 + reach
    pts = ell_pts(INNER_C, INNER_RX, INNER_RY, t0, t1, step=4, k=k)
    for run in runs_outside(pts, egg_grown):
        n = len(run)
        s.line(run, "2B", pressure=bell(n, 0.78, ends=0.12, power=0.35), tip="side",
               width=ARC_W, smooth=False, note="interior shade")
        laid += 1
        if laid % 8 == 0:
            print(s.look(path=f"out/p02_arcs_{laid}.png"))
print(s.look(path="out/p02_int_shade.png"))
for run in runs_outside(ell_pts(INNER_C, INNER_RX, INNER_RY, -160, 10, step=4, k=0.78), egg_grown):
    s.stump(run, strength=0.9, width=0.06, note="interior shade")
# the crescent's inner boundary, softened once: a stump along it
inner_edge = ell_pts((INNER_C[0] + SHIFT[0], INNER_C[1] + SHIFT[1]), INNER_RX, INNER_RY,
                     -115, -5, step=4, k=1.0)
for run in runs_outside(inner_edge, egg_grown):
    s.stump(run, strength=0.6, width=0.035, note="interior shade edge")
print(s.look(path="out/p02_int_shade_stumped.png"))

# --- the outer wall: arcs between the rim's lower arc and the outer's, lit at the
# left and dark at the right
for f in (0.10, 0.30, 0.50, 0.70, 0.90):
    c = (BOWL_C[0] + (OUTER_C[0] - BOWL_C[0]) * f, BOWL_C[1] + (OUTER_C[1] - BOWL_C[1]) * f)
    ry = RIM_RY + (OUTER_RY - RIM_RY) * f
    pts = ell_pts(c, RIM_RX - 0.004, ry - 0.004, 172, 8, step=4)       # left to right
    lay_arc(pts, "HB", 0.60, width=0.016, ramp_to=1.0, note="wall")
# the lip's right quarter, faintly
lay_arc(ell_pts(BOWL_C, RIM_RX, RIM_RY, -50, 50, step=4, k=0.975), "2H", 0.55, ends=0.2,
        width=0.012, note="lip")
print(s.look(path="out/p02_wall.png"))
s.stump(wall, strength=1.0, note="wall")
print(s.look(path="out/p02_wall_stumped.png"))
print(s.compare(s.plan(), path="out/p02_compare.png"))
print(s.budget_line())
