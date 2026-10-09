"""Pass 8: sign it and export it. A mark, not a name: two short ticks in the bottom
right corner, HB on the near table, close in value to what they sit on; free, as the
guide says, under note="signature". Then the drawing without its envelope."""
s.line([(0.935, 0.955), (0.948, 0.935)], "HB", pressure=0.6, tip="point", note="signature")
s.line([(0.948, 0.935), (0.958, 0.952)], "HB", pressure=0.6, tip="point", note="signature")
print(s.look(region="H8", scale=None, path="out/p08_signature.png"))
s.export("drawing.png", sketch=False)
print("exported drawing.png")
print(s.budget_line())
