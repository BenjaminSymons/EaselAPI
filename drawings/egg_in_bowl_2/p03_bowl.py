"""Pass 3: the bowl, every passage laid along its own shape.

- the outer wall's shade (right half, below the rim): arcs between the rim's lower half
  and the wall's lower outline, 2H leant on, heavier toward the right, a stump over
- the lit outer wall (left half): one faint 2H arc at the bottom where the form turns
- the bowl's cast shadow on the table, to its right: arcs offset outward from the
  wall's lower outline, HB, a stump along
- the inner wall's shade: arcs between the lip and the inner ellipse round the far
  side, cut round the egg, heavier toward the right where the egg's shade and the
  cast will meet it; HB, then 2B over the right portion; stumps along the arcs
- the floor: two faint 2H arcs along the inner ellipse's near half
- the lip's near edge: one HB point contour

Planned: bowl_shade 0.74, bowl_lit 0.92, interior_shade 0.44, floor_lit 0.90.
Budget for the pass: 35.
"""
before = len(s.history.records)
n = 0

# --- the outer wall's shade ----------------------------------------------------------
# each arc runs from the right end round past the bottom and fades into the lit half,
# heaviest a third of the way round, where the wall faces away from the window
for ry in (97, 109, 121, 133, 144):
    pts = ell(BOWL_CX, BOWL_CY, RIM_RX, ry, -4, 150, step=4)
    s.line(pts, "2H", pressure=bell(len(pts), 0.12, 0.9, peak=0.22, spread=0.45),
           tip="side", width=0.018, smooth=False, note="subject bowl wall shade")
    n += 1
for ry in (106, 134):
    s.stump(ell(BOWL_CX, BOWL_CY, RIM_RX, ry, -4, 150, step=6), strength=0.8, width=0.05,
            note="bowl wall stump along")
    n += 1
print(s.look(region="A5:H8", path="out/p03_a_wall.png"))

# --- the bowl's cast shadow on the table, under and to the right of the wall ----------
for grow_x, grow_y in ((3, 8), (8, 20), (14, 32)):
    pts = ell(BOWL_CX, BOWL_CY, LOW_RX + grow_x, LOW_RY + grow_y, 10, 115, step=4)
    s.line(pts, "2B", pressure=bell(len(pts), 0.15, 0.65, peak=0.35, spread=0.4),
           tip="side", width=0.022, smooth=False, note="bowl cast shadow on the table")
    n += 1
s.stump(ell(BOWL_CX, BOWL_CY, LOW_RX + 8, LOW_RY + 20, 10, 115, step=6),
        strength=0.8, width=0.055, note="bowl cast shadow stump")
n += 1
print(s.look(region="D5:H8", path="out/p03_b_cast.png"))

# --- the inner wall's shade ------------------------------------------------------------
for k in (0.12, 0.36, 0.60, 0.84):
    pts = crescent_arc(k, 182, 358, step=3)
    for run, u0, u1 in cut(pts, egg, margin=0.008):
        pr = ramp(0.55, 1.0, u0, u1, len(run))
        s.line(run, "HB", pressure=pr, tip="side", width=0.016, smooth=False,
               note="subject inner wall shade")
        n += 1
print(s.look(region="B4:H6", path="out/p03_c_inner_hb.png"))
# the right portion again, in 2B, toward the lost edge
for k in (0.25, 0.62):
    pts = crescent_arc(k, 285, 358, step=3)
    for run, u0, u1 in cut(pts, egg, margin=0.008):
        pr = ramp(0.45, 0.8, u0, u1, len(run))
        s.line(run, "2B", pressure=pr, tip="side", width=0.016, smooth=False,
               note="subject inner wall shade, right")
        n += 1
for k in (0.3, 0.7):
    for run, u0, u1 in cut(crescent_arc(k, 182, 358, step=4), egg, margin=0.012):
        s.stump(run, strength=0.7, width=0.03, note="inner wall stump along")
        n += 1
print(s.look(region="B4:H6", path="out/p03_d_inner.png"))

# --- the floor, and the lip's near edge ------------------------------------------------
# (two 2H arcs at 0.35 to 0.55 along the inner ellipse's near half were rehearsed here
# and dropped: a hard grade held lightly, they read as a speckled band along the near
# rim and moved floor_lit not at all. The floor is paper.)
s.line(lip(2, 178, step=3), "HB", pressure=[0.3, 0.5, 0.3], tip="point", width=0.003,
       note="subject lip near edge")
n += 1
print("strokes:", n)
print(s.look(path="out/p03_e_done.png"))
print(s.report(since=before))
print(s.compare(s.plan(), path="out/p03_compare.png"))
