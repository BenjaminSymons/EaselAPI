"""The signature: three ticks in the lower right corner, HB on the point, close in
value to the near table they sit on. Not charged, each noted "signature". Then the
export without the envelope, and the closing checklist.
"""
s.line([(0.925, 0.955), (0.935, 0.940)], "HB", pressure=0.55, tip="point", note="signature")
s.line([(0.935, 0.940), (0.945, 0.955)], "HB", pressure=0.55, tip="point", note="signature")
s.line([(0.930, 0.950), (0.940, 0.950)], "HB", pressure=0.45, tip="point", note="signature")
print(s.look(region="G8:H8", scale=None, path="out/p11_signature.png"))
print(s.export("drawing.png", sketch=False))
print(s.look(scale=256, sketch=False, path="out/p11_small.png"))
print(s.checklist())
