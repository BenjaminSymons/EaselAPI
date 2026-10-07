# Pass 4: inside the bowl. The far wall's shadow crescent, the egg's cast shadow on
# the floor, and a light tone over the lit floor so the egg's paper reads as the
# lightest thing. Every passage is laid as arcs along its own shape, cut into runs
# round the egg so the tone butts against the egg's outline: on its shade side that
# join is the lost edge, on its lit side the egg stays paper. The lips of the rim,
# far and near, are left as paper.
#
# Second version. The first (rehearsed) hatched all three with wide side strokes
# and every curved cut came back as a staircase of stroke ends, the cast shadow a
# hard blob, and the floor at 0.69 where 0.85 was meant. See NOTES.md.
in_egg = egg.contains

# The crescent: arcs from the lip inward, darkest at the lip, lighter toward the
# floor, and light at the left end where the light comes in.
before = s.stroke_count
for u, base in ((0.06, 0.95), (0.24, 0.92), (0.42, 0.88), (0.60, 0.84), (0.78, 0.78),
                (0.94, 0.66)):
    pts = crescent_arc(u)
    def pr(x, y, base=base):
        # along the crescent: faint at the left (x~0.25), full from the top rightward
        w = min(1.0, max(0.0, (x - 0.26) / 0.22))
        return base * (0.40 + 0.60 * w)
    lay_runs(cut_runs(pts, in_egg, egg, EGG_C), "2B", pr, 0.015, note="bowl shadow")
s.stump(crescent_poly(shrink=0.004), strength=0.9, note="bowl shadow")
# and its lower boundary on the right, where the far wall meets the floor, softened
s.stump(crescent_arc(1.0, 292, 368, n=24), strength=0.7, width=0.03, note="bowl shadow foot")
print(f"crescent: {s.stroke_count - before} strokes")

# The egg's cast shadow: loops of its own ellipse, in from the edge, cut round the
# egg. Heavier where it meets the egg (its left), lighter at the far tip.
before = s.stroke_count
cast = ellipse((0.552, 0.669), 0.088, 0.031, rotate=-8)
for k, grade, base in ((0.94, "4B", 0.80), (0.74, "4B", 0.95), (0.52, "6B", 0.85),
                       (0.28, "4B", 0.95)):
    pts = cast.scaled(k).closed
    def pr(x, y, base=base):
        w = min(1.0, max(0.0, (0.64 - x) / 0.14))     # 1 at the egg, 0 at the far tip
        return base * (0.55 + 0.45 * w)
    lay_runs(cut_runs(pts, in_egg, egg, EGG_C), grade, pr, 0.012, note="egg cast shadow")
egg_cast_cut = polygon([push_out(egg, p, EGG_C, step=1.02) for p in cast.closed], name="egg_cast")
s.stump(egg_cast_cut, strength=0.6, note="egg cast shadow")
print(f"egg cast shadow: {s.stroke_count - before} strokes")

# The lit floor: three light arcs of the inner ellipse over its lower half, cut round
# the egg, so the floor reads a step under the egg's paper and the near lip stays white.
before = s.stroke_count
for k, base in ((0.88, 0.50), (0.68, 0.46), (0.46, 0.42)):
    pts = arc(INNER_C, (INNER_RX - 0.012 * 0.75) * k, (INNER_RY - 0.012) * k, 15, 205, 40)
    lay_runs(cut_runs(pts, in_egg, egg, EGG_C), "2H", lambda x, y, b=base: b, 0.030, note="floor")
# the floor right up against the egg's lit side, so no white halo stands round it
lay_runs(cut_runs([(EGG_C[0] + (x - EGG_C[0]) * 1.13, EGG_C[1] + (y - EGG_C[1]) * 1.13)
                   for x, y in egg_arc(1.0, 96, 268, step=4)], in_egg, egg, EGG_C),
         "2H", lambda x, y: 0.5, 0.024, note="floor")
s.stump(floor_poly(shrink=0.014), strength=0.7, note="floor")
print(f"floor: {s.stroke_count - before} strokes")

read(bowl_shadow, "bowl_shadow")
read(egg_cast_cut, "egg_cast (cut round the egg)")
read(floor_poly(shrink=0.012), "floor")
read(egg, "egg (should still be paper)")
print(s.look(grid=True))
print(s.look(region="C5:G7", grid=True))
