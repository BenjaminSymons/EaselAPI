# Pass 8: the last marks. The wall came back mottled from its one stump; a second
# at full strength evens it, and it touches no edge. The table is left alone: a
# stump over it now would carry its graphite into the rim's white. And the
# signature's dot landed nothing (a one-point line under its width), so a tick
# where it was meant to be, the fourth signature mark.
read(wall, "wall before")
s.stump(wall, strength=1.0, note="wall")
read(wall, "wall after")
sx, sy = 0.925, 0.950
s.line([(sx - 0.006, sy - 0.0045), (sx - 0.001, sy - 0.002)], grade="HB", pressure=0.5, tip="point",
       width=0.004, smooth=False, note="signature: light")
print(s.look(grid=True, sketch=False))
