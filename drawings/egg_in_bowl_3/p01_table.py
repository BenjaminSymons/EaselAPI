"""Pass 1: the table, as rows of broad side strokes by hand, at two angles, one stump
over each plane. The far plane 2H leant on (plan 0.70), the near plane HB (0.54); the
rows stop half a stroke short of the bowl, whose band comes in the edges pass. The
pressure is a function of where the row is, so the table grades from the window at the
far left to the near edge with no seam."""
since = len(s.history.records)
WIDTH = 0.07


def p_far(x, y):
    return min(1.0, 0.50 + 0.15 * max(0.0, min(1.0, x)) + 1.15 * max(0.0, y))


def p_near(x, y):
    return min(1.0, 0.52 + 0.06 * max(0.0, min(1.0, x)) + 0.16 * max(0.0, (y - 0.45)) / 0.55)


def lay(run, grade, fn, flip):
    plist = [fn(x, y) for (x, y) in run]
    if flip:
        run, plist = run[::-1], plist[::-1]
    s.line(run, grade, pressure=plist, tip="side", width=WIDTH, smooth=False,
           note="table far" if grade == "2H" else "table near")


# --- the far plane: level rows, lighter toward the window at the left
for k, y in enumerate((0.035, 0.095, 0.155, 0.215, 0.275, 0.335)):
    lay([(-0.02, y), (0.25, y), (0.50, y), (0.75, y), (1.02, y)], "2H", p_far, k % 2)
print(s.look(path="out/p01_far_level.png"))
# ...and a second angle, 25 degrees on screen, cut short of the bowl's margin
for k, x0 in enumerate([-0.50, -0.38, -0.26, -0.14, -0.02, 0.10, 0.22, 0.34, 0.46, 0.58,
                        0.70, 0.82, 0.94]):
    pts = diag_row(x0, 0.37, 0.60, -0.375)
    for run in runs_outside(pts, bowl_margin):
        run = [p for p in run if -0.02 <= p[0] <= 1.02 and p[1] >= -0.02]
        if len(run) >= 3:
            lay(run, "2H", p_far, k % 2)
print(s.look(path="out/p01_far_rows.png"))
s.stump(table_far, strength=1.0, note="table far")
s.stump(polygon([(0.0, 0.33), (1.0, 0.33), (1.0, 0.41), (0.0, 0.41)]), strength=1.0, note="table far")
print(s.look(path="out/p01_far_stumped.png"))
print(s.compare(s.plan(), path="out/p01_compare_far.png"))

# --- the near plane and the table beside the bowl: rows cut round the bowl's margin.
# The first two rows are 2H leant on, the step between the planes.
near_rows = [(0.39, "2H", p_far), (0.45, "2H", p_far), (0.51, "HB", p_near), (0.57, "HB", p_near),
             (0.63, "HB", p_near), (0.69, "HB", p_near), (0.75, "HB", p_near), (0.81, "HB", p_near),
             (0.87, "HB", p_near), (0.93, "HB", p_near), (0.99, "HB", p_near), (1.03, "HB", p_near)]
laid = 0
for k, (y, grade, fn) in enumerate(near_rows):
    pts = diag_row(-0.02, y, 1.04, 0.0)
    for run in runs_outside(pts, bowl_margin):
        lay(run, grade, fn, k % 2)
        laid += 1
        if laid % 10 == 0:
            print(s.look(path=f"out/p01_near_rows_{laid}.png"))
for k, x0 in enumerate([-0.70, -0.58, -0.46, -0.34, -0.22, -0.10, 0.02, 0.14, 0.26, 0.38,
                        0.50, 0.62, 0.74, 0.86, 0.98]):
    pts = diag_row(x0, 1.02, 1.00, -0.625)
    for run in runs_outside(pts, bowl_margin):
        run = [p for p in run if -0.02 <= p[0] <= 1.02 and p[1] >= 0.40]
        if len(run) < 3:
            continue
        lay(run, "2H" if run[0][1] < 0.47 and run[-1][1] < 0.47 else "HB", p_near, k % 2)
        laid += 1
        if laid % 10 == 0:
            print(s.look(path=f"out/p01_near_rows_{laid}.png"))
print(s.look(path="out/p01_near_rows.png"))
near_all = polygon([(0.0, 0.355), (1.0, 0.355), (1.0, 1.0), (0.0, 1.0)])
s.stump(near_all, strength=1.0, note="table near")
s.stump(table_near, strength=0.7, note="table near")
print(s.look(path="out/p01_near_stumped.png"))
print(s.compare(s.plan(), path="out/p01_compare.png"))
print(s.budget_line())
