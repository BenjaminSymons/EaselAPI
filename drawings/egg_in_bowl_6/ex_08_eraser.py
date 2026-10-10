"""Exercise 8: the eraser and its ghost. A toned strip with a dark line, lifted two ways."""
from easel import Session, Region

s = Session(900, 300, medium="graphite", seed=8, out_dir="ex_out")
strip = Region(0.15, 0.38, 0.85, 0.62)
s.tone(strip, 0.55, grade="HB")
s.line([(0.2, 0.39), (0.8, 0.61)], "6B", pressure=0.9, tip="point", width=0.01)
print(s.look(path="ex_out/ex_08_before.png"))              # before the lifts
s.kneaded(Region(0.35, 0.33, 0.55, 0.67), strength=0.5)
s.plastic(Region(0.65, 0.33, 0.80, 0.67))
print(s.look(scale=None, path="ex_out/ex_08_after.png"))
print(s.report())                        # the paper line: never touched, and lifted
