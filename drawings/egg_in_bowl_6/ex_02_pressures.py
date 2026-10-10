"""Exercise 2: one line, six pressures, on the point and on the side."""
from easel import Session

s = Session(900, 500, medium="graphite", seed=2, out_dir="ex_out")
for i, p in enumerate(["taper", "press_in", "lift_off", "even", "swell", [0.1, 1.0]]):
    y = 0.12 + i * 0.15
    s.line([(0.08, y), (0.46, y)], "2B", pressure=p, tip="point", width=0.012, note=str(p))
    s.line([(0.54, y), (0.92, y)], "2B", pressure=p, tip="side", note=str(p))
print(s.look(path="ex_out/ex_02_pressures.png"))
