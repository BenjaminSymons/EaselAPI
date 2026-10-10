"""Pass 3: the egg. The light side is a floor of 2H, laid as arcs of the egg's own outline
scaled toward its centre (a round form: the guide's offset and scale nearly match, and an
offset deeper than the half-height degenerates), cut round the highlight and stumped
twice; the highlight is paper never touched. The shade side is cross-contour arcs that
shorten toward the terminator, each grade a step softer than the first rehearsal measured
too light: 2B at the outline, a 4B core one stroke in, 2B, HB, then 2H turning into the
light; one stump along them. The egg is the subject."""

AW = 0.02                                  # an arc's width: 20 px
SCALES = (0.92, 0.76, 0.60, 0.44, 0.28)    # about 17 px apart at the egg's shoulder

# --- the light side: the floor round the highlight ---------------------------------------
hl_clear = lambda x, y: in_highlight(x, y, 22 * PX, 22 * PY)
for sc in SCALES[:4]:
    for piece in cut_arc(egg_scaled(135, 315, sc, n=36), hl_clear):
        s.line(piece, "2H", pressure=[0.2, 0.85, 0.85, 0.85, 0.85, 0.2], tip="side", width=AW,
               smooth=False, note="subject")
print(s.look())
light_stump = holed_polygon(egg_arc(135, 315, dx=0.004, dy=0.005, n=36),
                            arc(HL_C, HL_R[0] + 15 * PX, HL_R[1] + 15 * PY, 0, 360, 24),
                            "light_stump")
s.stump(light_stump, strength=1.0)
s.stump(light_stump, strength=1.0)
print(s.look())

# --- the shade side: cross-contours, each shorter than the last --------------------------
shade = (
    (0.92, -45, 135, "2B", [0.12, 0.85, 0.90, 0.85, 0.12]),    # at the outline, the mass's value
    (0.76, -30, 120, "4B", [0.10, 0.70, 0.75, 0.70, 0.10]),    # the core, one stroke in
    (0.60, -15, 105, "2B", [0.12, 0.80, 0.80, 0.80, 0.12]),
    (0.44, 0, 90, "HB", [0.15, 0.90, 0.90, 0.15]),             # the half-tone
    (0.28, 15, 75, "2H", [0.15, 0.90, 0.90, 0.15]),            # turning into the light
)
for sc, t0, t1, grade, pressure in shade:
    s.line(egg_scaled(t0, t1, sc, n=24), grade, pressure=pressure, tip="side", width=AW,
           smooth=False, note="subject")
print(s.look())
shade_stump = polygon(egg_arc(-45, 135, dx=0.004, dy=0.005, n=36) + egg_scaled(135, -45, 0.18, n=24),
                      name="shade_stump")
s.stump(shade_stump, strength=1.0)
print(s.look())
