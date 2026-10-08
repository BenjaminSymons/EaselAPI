"""Exercise 9: draw, rehearse, draw. The whole loop on an abstract shape."""
from easel import Session, cell, polygon

s = Session(900, 600, medium="graphite", seed=9)
s.mark("a", *cell("C3").point(0.5, 0.5))
s.mark("b", *cell("F3").point(0.5, 0.5))
s.mark("c", *cell("D6").point(0.5, 0.5))
shape = polygon([s.pt("a"), s.pt("b"), s.pt("c")])
s.pencil(shape, pressure=0.6)
print(s.look(path="ex_out/ex_09_envelope.png"))
plan = [{"hatch": shape, "grade": "2B", "tip": "side", "pressure": 0.8, "angle": 20}]
print(s.cost(plan))
print(s.rehearse(plan, path="ex_out/ex_09_rehearse.png"))
s.hatch(shape, angle=20, grade="2B", tip="side", pressure=0.8)
print(s.look(sketch=False, path="ex_out/ex_09_done.png"))
print(s.report())
