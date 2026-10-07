# Pass 5: the egg. Its shade is laid as cross-contours -- the egg's own outline
# scaled inward -- over the lower right, each arc shorter than the last so their
# ends trace the terminator bowing toward the shadow. The core sits a little in from
# the outline, the outline's own arc is lighter (the floor's light bounced back),
# and a hard-grade arc past the terminator is the half-tone into the light. The lit
# side is paper never touched: the highlight is the paper itself. A stump along the
# terminator softens it, a second over the shade evens the arcs, and one 6B line
# under the egg is where it touches the floor.
before = s.stroke_count

# Second version: the first laid the arcs at HB 0.6-0.85 with ends fading hard, and
# the shade read 0.67 where 0.42 was planned; and its terminator ran from the upper
# right to the lower left, so what met the crescent behind the egg was half-tone.
# Now the shade is the egg's right side: the light is from the left, and high.
#
# (k, grade, base pressure, t-range): the outline's arc first, then inward
for k, grade, base, t0, t1 in ((0.96, "HB", 0.72, -72, 128),
                               (0.88, "HB", 0.95, -64, 120),
                               (0.80, "2B", 0.90, -56, 110),
                               (0.72, "2B", 0.80, -46, 100),
                               (0.64, "HB", 0.85, -34, 88),
                               (0.56, "2H", 0.85, -22, 76)):
    pts = egg_arc(k, t0, t1, step=4)
    n = len(pts)
    # a little lighter at both ends of the arc (where it meets the terminator)
    pr = [base * (0.5 + 0.5 * math.sin(math.pi * i / (n - 1)) ** 0.5) for i in range(n)]
    s.line(pts, grade=grade, pressure=pr, tip="side", width=0.014, smooth=False, note="egg shade")

# the lost edge: the egg's outline where it stands against the crescent, taken down
# to the crescent's own value, and a stump dragged across the join
s.line(egg_arc(0.97, -72, -4, step=4), grade="2B", pressure=[0.55, 0.85, 0.85, 0.6], tip="side",
       width=0.012, smooth=False, note="egg shade into the bowl shadow")
s.stump(egg_arc(0.60, -40, 110, step=4), strength=0.7, width=0.035, note="egg terminator")
s.stump(egg_shade_poly(bow=0.22), strength=0.6, note="egg shade")
s.stump(egg_arc(1.0, -66, -8, step=4), strength=0.8, width=0.03, note="lost edge")
# the contact: where the egg meets its own cast shadow
s.line(egg_arc(0.995, 40, 112, step=4), grade="6B", pressure=[0.15, 0.6, 0.9, 0.8, 0.3],
       tip="point", smooth=True, note="egg contact")
print(f"egg: {s.stroke_count - before} strokes")

read(egg_shade, "egg_shade")
read(polygon(egg_arc(0.9, 190, 290) + [EGG_C]), "egg lit side")
read(egg, "egg as a place")
print(s.look(grid=True))
print(s.look(region="C5:F7", grid=True))
