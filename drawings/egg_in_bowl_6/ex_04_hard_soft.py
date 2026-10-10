"""Exercise 4: a hard grade leant on beside a soft grade held lightly."""
from easel import Session, cell

s = Session(900, 450, medium="graphite", seed=4, out_dir="ex_out")
s.hatch(cell("C4"), angle=0, grade="HB", pressure=0.5, tip="side", note="soft, light")
s.hatch(cell("F4"), angle=90, grade="2H", pressure=1.0, tip="side", note="hard, leant on")
print(s.look(scale=None, path="ex_out/ex_04_hard_soft.png"))
print(s.report())                        # the values line, and the paper line
