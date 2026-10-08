"""The signature's third tick, HB at 0.45 on the point, landed nothing (the check's
`landed nothing:` line, record 147). A fourth tick at 0.55, which the first two landed
at. Free, noted "signature". Then the export again, without the envelope.
"""
s.line([(0.929, 0.950), (0.941, 0.950)], "HB", pressure=0.55, tip="point", note="signature")
print(s.look(region="G8:H8", scale=None, path="out/p12_signature.png"))
print(s.export("drawing.png", sketch=False))
