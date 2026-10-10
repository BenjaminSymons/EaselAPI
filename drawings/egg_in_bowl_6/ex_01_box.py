"""Exercise 1: the box of pencils. Every grade at three pressures, on the side."""
from easel import Session, GRADES

s = Session(900, 450, medium="graphite", seed=1, out_dir="ex_out")
for i, grade in enumerate(GRADES):
    y = 0.1 + i * 0.15
    for j, p in enumerate((0.3, 0.6, 1.0)):
        x = 0.06 + j * 0.31
        s.line([(x, y), (x + 0.25, y)], grade, pressure=p, tip="side", width=0.05,
               note=f"{grade} at {p}")
print(s.look(scale=None, path="ex_out/ex_01_box.png"))
print(s.report())
