"""Exercise 5: the same oval hatched across, and laid as arcs of its own outline."""
import math
from easel import Session, ellipse

s = Session(900, 450, medium="graphite", seed=5, out_dir="ex_out")
s.hatch(ellipse((0.27, 0.5), 0.17, 0.32), angle=0, grade="2B", pressure=0.8, tip="side",
        width=0.05)
cx, cy = 0.73, 0.5
for k in (1.0, 0.85, 0.7, 0.55, 0.4):
    arc = [(cx + 0.17 * k * math.cos(math.radians(t)), cy + 0.32 * k * math.sin(math.radians(t)))
           for t in range(-80, 101, 8)]
    s.line(arc, "2B", pressure=[0.4, 0.9, 0.9, 0.4], tip="side", width=0.05, smooth=False)
print(s.look(path="ex_out/ex_05_across_along.png"))
print(s.look(scale=None, path="ex_out/ex_05_across_along_full.png"))
