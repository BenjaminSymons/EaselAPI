"""Exercise 9: draw, rehearse, draw. The whole loop on an abstract shape."""
from easel import Session, cell, polygon

s = Session(900, 600, medium="graphite", seed=9, out_dir="ex_out")
s.mark("a", *cell("C3").point(0.5, 0.5))
s.mark("b", *cell("F3").point(0.5, 0.5))
s.mark("c", *cell("D6").point(0.5, 0.5))
shape = polygon([s.pt("a"), s.pt("b"), s.pt("c")])
s.pencil(shape, pressure=0.6)            # the envelope, free
print(s.look(path="ex_out/ex09_envelope.png"))
plan = [{"hatch": shape, "grade": "2B", "tip": "side", "pressure": 0.8, "angle": 20}]
print("cost:", s.cost(plan))
print(s.rehearse(plan, path="ex_out/ex09_rehearsal.png"))   # what the pass would look like
s.hatch(shape, angle=20, grade="2B", tip="side", pressure=0.8)
print(s.look(sketch=False, path="ex_out/ex09_no_envelope.png"))   # the drawing without its envelope
print(s.budget_line())
print(s.report())
