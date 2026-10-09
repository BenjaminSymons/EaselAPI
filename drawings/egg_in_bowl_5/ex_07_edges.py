"""Exercise 7: three edges, hard, soft and lost."""
from easel import Session, Region

s = Session(900, 300, medium="graphite", seed=7, out_dir="ex_out")
for i, (left, right, angle) in enumerate(((0.40, None, 20), (0.40, None, 110),
                                          (0.50, 0.56, 65))):
    x0 = 0.05 + i * 0.31
    s.tone(Region(x0, 0.2, x0 + 0.14, 0.8), left, grade="2B", angle=angle)
    if right is not None:
        s.tone(Region(x0 + 0.14, 0.2, x0 + 0.28, 0.8), right, grade="HB", angle=angle + 90)
    print(s.look(region=Region(x0 - 0.02, 0.1, x0 + 0.3, 0.9), path=f"ex_out/ex_07_panel_{i+1}.png"))
edge = 0.05 + 0.14
s.line([(edge - 0.004, 0.2), (edge - 0.004, 0.8)], "2B", pressure=0.9, tip="side",
       width=0.013, smooth=False)
edge = 0.36 + 0.14
s.stump([(edge, 0.2), (edge, 0.8)], strength=0.8, width=0.03)
edge = 0.67 + 0.14
s.stump([(edge - 0.03, 0.5), (edge + 0.03, 0.5)], strength=0.8, width=0.05)
print(s.look(path="ex_out/ex_07_edges.png"))
print(s.look(scale=None, path="ex_out/ex_07_edges_full.png"))
print(s.report())
