"""Pass 1: the table. Rows of broad side strokes by hand at two angles, a 2H leant on,
lighter toward the window at the upper left; the rows cut round the bowl and the egg;
one stump over the table and not over the bowl."""


def pressure_at(x, y):
    x, y = max(0.0, min(1.0, x)), max(0.0, min(1.0, y))
    return min(1.0, 0.74 + 0.26 * (0.6 * x + 0.4 * y))


PADX, PADY = 12 * PX, 35 * PY        # a run ends a sixth short; one passing beside keeps half clear


def blocked(x, y):
    return in_thing(x, y, PADX, PADY)


rows = []
k, y = 0, -0.03
while y < 1.04:                       # the first angle: horizontal, 60 px apart, 72 px wide
    for run in runs((-0.03, y), (1.03, y), blocked):
        rows.append(run[::-1] if k % 2 else run)
    k += 1
    y += 0.078

c = -0.56
while c < 1.06:                       # the second angle: y = x / 2 + c, about 20 degrees
    x0 = max(-0.03, (-0.03 - c) / 0.5)
    x1 = min(1.03, (1.03 - c) / 0.5)
    if x1 - x0 > 0.05:
        for run in runs((x0, 0.5 * x0 + c), (x1, 0.5 * x1 + c), blocked):
            rows.append(run[::-1] if k % 2 else run)
    k += 1
    c += 0.087

print(f"{len(rows)} runs")
for i, run in enumerate(rows):
    s.line(run, "2H", pressure=[pressure_at(*run[0]), pressure_at(*run[1])], tip="side",
           width=0.07, smooth=False, note="table")
    if i % 12 == 11:
        print(s.look())
print(s.look())
table = table_ring(15 * PX, 15 * PY)
s.stump(table, strength=1.0)
print(s.look())
s.stump(table, strength=1.0)          # the second covers exactly what the first did
print(s.look())
