"""Pass 1: the table. Rows of broad side strokes by hand at two angles twenty degrees
apart, cut round the bowl half a stroke and a few pixels short of it, a hard grade
leant on, lighter toward the window on the left; then one stump over the far plane
and one over the near. A look every twelve rows."""

WIDTH = 0.07
LOOK_EVERY = 12
_count = [0]


def row_points(y0, slope):
    a = (-0.03, y0 - 0.03 * slope)
    b = (1.03, y0 + 1.03 * slope)
    return dense(a, b, 8.0)


def grade_and_pressures(ymid):
    if ymid < 0.42:
        return "2H", (0.80, 1.00)          # far: 2H leant on reads about 0.58
    if ymid < 0.74:
        return "HB", (0.55, 0.70)          # beside the bowl
    return "HB", (0.62, 0.80)              # near: HB reads about 0.50 after the stump


def lay_rows(y0s, slope, note):
    for y0 in y0s:
        pts = row_points(y0, slope)
        grade, (pa, pb) = grade_and_pressures(y0 + 0.5 * slope)
        prs = ramp(len(pts), pa, pb)       # lighter at the left, toward the window
        for run_pts, run_prs in cut(pts, prs, [bowl_keepout_rows]):
            if _count[0] % 2:
                run_pts, run_prs = run_pts[::-1], run_prs[::-1]
            s.line(run_pts, grade, pressure=run_prs, tip="side", width=WIDTH,
                   smooth=False, note=note)
            _count[0] += 1
            if _count[0] % LOOK_EVERY == 0:
                s.look(path=f"out/p01_look_{_count[0]:03d}.png")


# First angle: five degrees up to the right. Second: fifteen degrees down to the right.
lay_rows([0.05 + 0.065 * i for i in range(18)], -0.117, "table rows, -5 deg")
lay_rows([-0.33 + 0.085 * i for i in range(17)], 0.357, "table rows, +15 deg")
print("rows laid:", _count[0])
s.look(path="out/p01_rows_before_stump.png")
s.stump(Region(0.0, 0.0, 1.0, 0.44), strength=1.0, note="far plane closed")
s.stump(Region(0.0, 0.44, 1.0, 1.0), strength=1.0, note="near plane closed")
print(s.look(path="out/p01_after_stump.png"))
print(s.budget_line())
print(s.compare(s.plan()))
