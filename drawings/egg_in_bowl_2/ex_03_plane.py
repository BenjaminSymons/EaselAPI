"""Exercise 3: a plane, laid as rows by hand at two angles, read before and after the stump."""
from easel import Session, span

s = Session(900, 600, medium="graphite", seed=3)
plane = span("B2", "G7")
s.plan(why="a plane that reads as one tone", values={plane: 0.60})
for k, (y, x0, x1) in enumerate(((0.16, 0.12, 0.88), (0.24, 0.10, 0.80), (0.33, 0.16, 0.90),
                                 (0.41, 0.11, 0.84), (0.50, 0.12, 0.89), (0.58, 0.10, 0.78),
                                 (0.67, 0.15, 0.88), (0.75, 0.12, 0.82))):
    row = [(x0, y), (x1, y)]
    s.line(row if k % 2 == 0 else row[::-1], "HB", pressure=0.9, tip="side", width=0.06,
           smooth=False)
for k, (x, y0, y1) in enumerate(((-0.05, 0.14, 0.80), (0.10, 0.30, 0.76), (0.29, 0.14, 0.74),
                                 (0.43, 0.40, 0.80), (0.63, 0.14, 0.70), (0.78, 0.26, 0.80))):
    row = [(x, y0), (x + 0.36 * (y1 - y0) / 0.66, y1)]
    s.line(row if k % 2 == 0 else row[::-1], "2H", pressure=1.0, tip="side", width=0.06,
           smooth=False)
print("--- before the stump")
print(s.report(since=0))
print(s.look(path="ex_out/ex_03_plane_before.png"))
s.stump(plane, strength=1.0)
print("--- after the stump")
print(s.report())
print(s.look(path="ex_out/ex_03_plane_after.png"))
