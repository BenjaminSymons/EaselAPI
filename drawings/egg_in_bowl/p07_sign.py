# Pass 7: the signature. Three marks in the lower right corner, close in value to
# the table they sit on: a small oval, the egg again, lying on a short line, and a
# dot inside it where its light would be. Free, as marks noted "signature" are.
sx, sy = 0.925, 0.950
oval = [(sx + 0.012 * math.cos(math.radians(t)), sy + 0.010 * math.sin(math.radians(t)) * 0.95)
        for t in range(0, 361, 20)]
s.line(oval, grade="HB", pressure=0.5, tip="point", width=0.004, smooth=True, note="signature: egg")
s.line([(sx - 0.02, sy + 0.013), (sx + 0.022, sy + 0.012)], grade="HB", pressure=[0.3, 0.55, 0.3],
       tip="point", width=0.004, smooth=True, note="signature: line")
s.line([(sx - 0.004, sy - 0.003)], grade="HB", pressure=0.45, tip="point", width=0.004,
       note="signature: dot")
print(s.look(region="G8", grid=True, sketch=False))
