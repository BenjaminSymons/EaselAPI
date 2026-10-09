"""Pass 4: the edges. The hard edge is the bowl's rim against the table: a narrow side
stroke along the silhouette, laid after every stump near it, its centre two pixels
outside the line (in the table), in the table's own value on each side and in the
cast shadow's where the bowl's shadow falls. The lost edge is the egg's shadow side
into the bowl's shadow behind it: the two tones already butt on the line, and one
stump is worked across the join, held to a band straddling it.

The first rehearsal laid the narrow edge alone and left the 10-15 px fringe of paper
speckle the band's inner layer had ridden over; this one closes the fringe first with
a 20 px stroke at 8 px out and a stump along it, and lays the narrow edge last.
"""
EDGE = 0.013
SIDES = (((172, 370), "2H", [0.55, 0.85, 0.9, 0.85, 0.55]),      # far: the table at 0.69
         ((178, 100), "HB", [0.5, 0.75, 0.8, 0.5]),               # near-left: 0.56
         ((106, -16), "2B", [0.5, 0.85, 0.9, 0.85, 0.5]))         # the cast shadow: 0.38
for (t0, t1), grade, pr in SIDES:
    s.line(silhouette(t0, t1, 8.0, step=3), grade, pressure=pr, tip="side", width=0.02,
           smooth=False, note="edge band")
for (t0, t1), grade, pr in SIDES:
    s.stump(silhouette(t0, t1, 14.0, step=3), strength=0.8, width=0.03, note="edge stump")
print(s.look(region="C4:G7", scale=None, path="out/p04_look_01_crop.png"))
for (t0, t1), grade, pr in SIDES:
    s.line(silhouette(t0, t1, 2.0, step=3), grade, pressure=pr, tip="side", width=EDGE,
           smooth=False, note="hard edge")

# the lost edge: a band straddling the egg's lower-right outline, stumped once
cx, cy, a, b = EGG
join = polygon(egg_pts(cx, cy, a, b, 45, 150, scale=0.86, step=4)
               + egg_pts(cx, cy, a, b, 150, 45, scale=1.16, step=4), name="join")
s.stump(join, strength=0.8, note="lost edge stump")
print(s.look(region="C4:G7", scale=None, path="out/p04_look_02_crop.png"))
print(s.look(path="out/p04_look_02.png"))
