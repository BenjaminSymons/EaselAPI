"""Exercise 6: what the stump does to the number. Tone a cell, read, stump, read."""
from easel import Session, cell

s = Session(900, 450, medium="graphite", seed=6, out_dir="ex_out")
s.plan(why="one patch", values={cell("D4"): 0.45})
s.tone(cell("D4"), 0.45, grade="2B")
print("--- before the stump ---")
print(s.report(since=0))                 # the plan line: inside 0.10
print(s.look(region="C3:E5", scale=None, path="ex_out/ex_06_before.png"))
s.stump(cell("D4"), strength=1.0)
print("--- after the stump ---")
print(s.report())                        # and now it reads lighter, by a tenth or more
print(s.look(region="C3:E5", scale=None, path="ex_out/ex_06_after.png"))
