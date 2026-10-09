"""Exercise 6: what the stump does to the number."""
from easel import Session, cell

s = Session(900, 450, medium="graphite", seed=6, out_dir="ex_out")
s.plan(why="one patch", values={cell("D4"): 0.45})
s.tone(cell("D4"), 0.45, grade="2B")
print("--- before the stump ---")
print(s.report(since=0))
s.stump(cell("D4"), strength=1.0)
print("--- after the stump ---")
print(s.report())
print(s.look(region="C3:E5", scale=None, path="ex_out/ex_06_stump_number.png"))
