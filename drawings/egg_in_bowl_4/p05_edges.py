"""Pass 5: edges, last but one, after every stump near them.

The hard edge: the bowl's rim against the table, a narrow side stroke along the
silhouette with its centre two pixels outside the line on the table's side, in the
table's own value: 2H leant on round the far half, HB round the near half. The egg's
lit outline against the floor, found: a narrow 2H stroke just outside it in the floor's
value. The rim's inner line against the interior shadow: a narrow HB stroke just inside
it. The lost edge: the egg's shadow side into the bowl's shadow behind it, two tones of
one value butting on the line already, and a stump dragged across the join."""

# First, the one stump the bowl pass could not drag: the arcs stacked behind the egg's
# top were left unstumped by the keep-out and show the side tip's striations.
s.stump(intarc_px(-128, -52, 30), strength=1.0, width=0.035,
        note="subject: shade behind the egg closed")

far = silarc(165, 375, grow_px=2)
s.line(far, "2H", pressure=bell(len(far), 1.0, 0.85), tip="side", width=0.013,
       smooth=False, note="hard edge: rim against the far table")
near = silarc(-15, 195, grow_px=2)
s.line(near, "HB", pressure=bell(len(near), 0.85, 0.70), tip="side", width=0.013,
       smooth=False, note="hard edge: wall against the near table")

lit_edge = arc(EX, EY, ERX + 3 / W, ERY + 3 / H, 140, 290, EROT)
s.line(lit_edge, "2H", pressure=bell(len(lit_edge), 0.7, 0.4), tip="side", width=0.012,
       smooth=False, note="subject: the egg's lit edge, found")

# (A narrow HB stroke along the rim's inner line, inset 7 px, was rehearsed here and
# dropped: at 0.9 it read as a dark ring inside the rim with blocked ends, and the
# paper rim against the stumped shade was already a hard edge without it.)
s.look(path="out/p05_look_01_edges.png")

for t in (-25, 10):                       # the lost edge: across the join, twice
    s.stump([eggpt(t, k=0.80), eggpt(t, k=1.35)], strength=0.8, width=0.05,
            note="subject: lost edge, across the join")
print(s.look(path="out/p05_after.png"))
print(s.look(region="B5:G7", scale=None, path="out/p05_after_crop.png"))
print(s.budget_line())
print(s.compare(s.plan()))
