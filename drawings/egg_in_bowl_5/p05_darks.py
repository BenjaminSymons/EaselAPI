"""Pass 5: the darks, last and unstumped. The egg's contact shadow on the bowl's floor:
6B arcs along the egg's underside just outside its outline, at a bell, laid after
every stump near them (the egg's, the lost edge's) and left alone.

The first rehearsal's bells fell to 0.4 and a 6B at 0.4 is still a dark block at both
ends of each arc; these fall to 0.15 and the arcs are shorter.
"""
cx, cy, a, b = EGG
for scale, (t0, t1), pr in ((1.05, (54, 124), [0.15, 0.6, 0.95, 0.6, 0.15]),
                            (1.13, (60, 118), [0.15, 0.55, 0.9, 0.55, 0.15]),
                            (1.21, (68, 110), [0.1, 0.45, 0.75, 0.45, 0.1])):
    s.line(egg_pts(cx, cy, a, b, t0, t1, scale=scale, step=3), "6B", pressure=pr,
           tip="side", width=0.02, smooth=False, note="subject darks")
print(s.look(region="C4:G7", scale=None, path="out/p05_look_01_crop.png"))
print(s.look(path="out/p05_look_01.png"))
print(s.look(scale=256, path="out/p05_look_small.png"))
