"""Pass 1: the table as rows of broad side strokes at two angles, and the stumps.

Horizontal rows carry the planes: 2H leant on for the far plane (0.68), HB for the
near one (0.55), each row's pressure list lighter toward the window at the left. A
second set at 22 degrees in 2H crosses both. Every row is cut 40 px short of the
bowl's silhouette (half the 72 px stroke and a few pixels); the band beside the bowl
is the bowl pass's. The stumps are rectangles and four polygons hugging the bowl, so
nothing is dragged into the bowl's paper.
"""
WIDTH = 0.07
MARGIN = 40.0
laid = 0
look_n = 0


def row(p0, p1, grade, pressure, note):
    global laid, look_n
    for pts, pl in cut(p0, p1, pressure, in_bowl, MARGIN):
        s.line(pts, grade, pressure=pl, tip="side", width=WIDTH, smooth=False, note=note)
        laid += 1
        if laid % 12 == 0:
            look_n += 1
            print(s.look(path=f"out/p01_look_{look_n:02d}.png"))


# Horizontal rows, alternating direction, no two alike.
rows = [(20, 2, "2H", (0.50, 0.75)), (74, -1, "2H", (0.52, 0.78)), (128, 3, "2H", (0.50, 0.76)),
        (182, 0, "2H", (0.55, 0.80)), (236, -2, "2H", (0.55, 0.82)), (290, 1, "2H", (0.58, 0.85)),
        (344, -3, "2H", (0.62, 0.90)), (398, 2, "HB", (0.50, 0.72)), (452, -1, "HB", (0.55, 0.78)),
        (506, 1, "HB", (0.58, 0.82)), (560, -2, "HB", (0.60, 0.85)), (614, 3, "HB", (0.62, 0.88)),
        (668, 0, "HB", (0.63, 0.88)), (722, -2, "HB", (0.65, 0.90)), (770, 1, "HB", (0.65, 0.90))]
for k, (y, dy, grade, pr) in enumerate(rows):
    p0, p1 = (-24.0, y + dy), (1048.0, y + dy + 2 * dy)
    if k % 2:                                   # right to left: list turned round
        p0, p1, pr = p1, p0, (pr[1], pr[0])
    row(p0, p1, grade, pr, "table rows")

# A second angle: rows rising to the right at 22 degrees in pixels, 2H.
import math
slope = math.tan(math.radians(22))
k = 0
y0 = -430.0
while y0 < 790:
    p0, p1 = (-24.0, y0 + 24 * slope * -1), (1048.0, y0 + 1048 * slope)
    pr = (0.72, 0.92)
    if k % 2:
        p0, p1, pr = p1, p0, (pr[1], pr[0])
    row(p0, p1, "2H", pr, "table rows, second angle")
    y0 += 58.0 + (k % 3) * 2
    k += 1

print("rows laid:", laid)
print(s.look(path="out/p01_rows_before_stump.png"))

# The stumps: rectangles clear of the bowl, and four polygons hugging its silhouette.
for place in (Region(0.0, 0.0, 1.0, 0.42), Region(0.0, 0.75, 1.0, 1.0),
              Region(0.0, 0.42, 0.21, 0.75), Region(0.79, 0.42, 1.0, 0.75)):
    s.stump(place, strength=1.0, note="table stump")
G = 6.0
ul = polygon([N(215, 322), N(512, 322)] + silhouette(270, 180, G) + [N(215, 450)])
ur = polygon([N(512, 322), N(809, 322), N(809, 450)] + silhouette(0, -90, G))
ll = polygon([N(215, 450)] + silhouette(180, 90, G) + [N(512, 576), N(215, 576)])
lr = polygon(silhouette(0, 90, G) + [N(512, 576), N(809, 576), N(809, 450)])
for place in (ul, ur, ll, lr):
    s.stump(place, strength=1.0, note="table stump beside the bowl")
print(s.look(path="out/p01_after_stump.png"))
print(s.look(grid=True, region="C4:G7", scale=None, path="out/p01_after_stump_crop.png"))
