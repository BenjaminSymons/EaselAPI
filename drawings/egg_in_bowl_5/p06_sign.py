"""Sign it: one tick in the lower right corner, leant on since it sits on a stumped
HB tone, free under note="signature"; then export without the envelope."""
s.line([(0.905, 0.955), (0.935, 0.947)], "HB", pressure=0.9, tip="point", width=0.004,
       note="signature")
print(s.look(region="G8:H8", scale=None, path="out/p06_signature_crop.png"))
s.export("drawing.png", sketch=False)
print(s.look(sketch=False, path="out/p06_final.png"))
print(s.look(sketch=False, scale=256, path="out/p06_final_small.png"))
