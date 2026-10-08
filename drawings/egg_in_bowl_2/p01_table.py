"""Pass 1: the table, the big plane. Rows of broad side strokes by hand at two angles,
a hard grade leant on, cut round the bowl and the egg, lighter toward the window at
the upper left; a band along the bowl's silhouette for what the rows stop short of;
one stump over the table alone (the bowl is cut out of the stump's place).

Planned: table_far 0.66, table_near 0.56. Budget for the pass: 45.
"""
before = len(s.history.records)
standing = [bowl, egg]
MARGIN = 0.035                      # half a 0.07 stroke

# rows at the first angle: horizontal, heavier lower down and toward the right
rows = []
pressures = []
ys = [0.04 + 0.085 * i for i in range(12)]
for y in ys:
    rows.append([(-0.03, y), (1.03, y)])
def grade_and_pressure(y):
    """The far table is 2H leant on; the near table, past the bowl's middle, is HB,
    since a 2H's ceiling reads 0.53 and the near plane wants 0.56 after its stump."""
    if y < 0.5:
        base = 0.70 + 0.50 * y                       # 0.70 at the top, 0.95 at the middle
        return "2H", [base, min(1.0, base + 0.12)]
    base = 0.55 + 0.24 * (y - 0.5)                   # 0.55 at the middle, 0.67 at the bottom
    return "HB", [base, min(1.0, base + 0.12)]


n1 = 0
for k, (y, row) in enumerate(zip(ys, rows)):
    grade, pr = grade_and_pressure(y)
    n1 += lay_rows([row], grade, pr, 0.07, note="table rows",
                   avoid=standing, margin=MARGIN, flip_odd=(k % 2 == 1))
print("first angle:", n1)
print(s.look(path="out/p01_a_rows1.png"))

# rows at the second angle, 22 degrees off
import math
slope = math.tan(math.radians(22))
rows2 = []
y0s = [-0.42 + 0.092 * i for i in range(16)]
n2 = 0
for k, y0 in enumerate(y0s):
    row = [(-0.03, y0), (1.03, y0 + 1.06 * slope)]
    mid = max(0.0, min(1.0, y0 + 0.53 * slope))
    grade, pr = grade_and_pressure(mid)
    n2 += lay_rows([row], grade, pr, 0.07, note="table rows 2",
                   avoid=standing, margin=MARGIN, flip_odd=(k % 2 == 1))
print("second angle:", n2)
print(s.look(path="out/p01_b_rows2.png"))

# the band beside the bowl, along its silhouette, where the rows stopped short
# in the grade of the table it sits in: 2H over the far rim, HB under the near wall
for g in (14, 38, 62):
    s.line(ell(BOWL_CX, BOWL_CY, RIM_RX + g, RIM_RY + g, 185, 355), "2H",
           pressure=[0.95, 0.9, 1.0], tip="side", width=0.03, smooth=False,
           note="table band along the far rim")
    s.line(ell(BOWL_CX, BOWL_CY, LOW_RX + g, LOW_RY + g, -5, 185), "HB",
           pressure=[0.62, 0.6, 0.58], tip="side", width=0.03, smooth=False,
           note="table band along the near wall")
s.stump(table, strength=1.0, note="table stump")
s.stump(table, strength=1.0, note="table stump, second, for the mottle")
print(s.look(path="out/p01_c_stumped.png"))
print(s.report(since=before))
print(s.compare(s.plan(), path="out/p01_compare.png"))
