"""Pass 8: sign it, and export without the envelope. Two marks, free, each noted
`signature`: a tick in the lower-right corner, HB on the point, close in value to the
near table it sits on.

The first signing laid an HB tick 15 px long at 0.6 and a two-point dot 2 px long; the
check said both landed nothing (under one unit of graphite). Undone with `easel undo 2`,
free, and signed again: two strokes of a tick, each 30 px, HB at 0.9, 4 px wide."""

s.line([(0.918, 0.958), (0.934, 0.944)], "HB", pressure=0.9, tip="point", width=0.004,
       note="signature")
s.line([(0.934, 0.944), (0.950, 0.958)], "HB", pressure=0.9, tip="point", width=0.004,
       note="signature")
print(s.budget_line())
s.export("drawing.png", sketch=False)
print("exported drawing.png")
print(s.look(region="G8:H8", scale=None, path="out/p08_signature_crop.png"))
