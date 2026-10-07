# Pass 3: the bowl against the table. The table's tone is brought up to the bowl's
# silhouette with closed loops that follow it and a ring stump to close them; then
# the one hard edge, a narrow stroke whose inner side lands on the silhouette, laid
# last so the stump never touches it. Then the exterior wall turning into shade on
# the right, and the bowl's cast shadow on the table: arcs from the belly outward,
# each lighter than the last, so the shadow is darkest under the bowl and fades.
#
# Third version. The first (rehearsed) laid the band at HB p=0.62-0.74 and came
# back speckled and lighter than the stumped table round it, and hatched the cast
# shadow in 36 strokes with stair-stepped ends. The second laid the band as two
# arcs, the rim's over the top and the belly's under, and left a white notch at each
# side where they did not meet; the wall's three arcs read as stripes. See NOTES.md.
before = s.stroke_count

# The band between the broad rows' ends and the silhouette: closed loops round it,
# each a side stroke, the loop's seam under the cast shadow at lower right. A
# pressure list round a loop: light at the seam, heavier over the top right, so
# the table behind the bowl is a shade darker than beside it.
for dy, width in ((0.074, 0.032), (0.056, 0.030), (0.038, 0.028), (0.022, 0.024)):
    s.line(silhouette(dy * 0.75, dy), grade="HB", pressure=[0.66, 0.66, 0.72, 0.78, 0.72, 0.66],
           tip="side", width=width, smooth=False, note="table round the bowl")

# A ring round the bowl, a hair off the silhouette, stumped to close the loops and
# the broad rows' ends into the table.
ring = polygon(silhouette(0.075, 0.10, n=72) + silhouette(0.0075, 0.010, n=72)[::-1], name="ring")
s.stump(ring, strength=1.0, note="table round the bowl")

# The hard edge: a narrow side stroke whose inner edge lands on the silhouette.
s.line(silhouette(0.0035, 0.0045, n=180), grade="HB", pressure=0.9, tip="side",
       width=0.013, smooth=False, note="table up to the rim: hard edge")
print(f"band round the bowl: {s.stroke_count - before} strokes")

# The exterior wall turning away from the light: arcs between rim and belly, heavy
# on the right and fading out toward the left where the wall is lit; then a stump
# along the wall so the arcs read as one turning plane.
before = s.stroke_count
for f, pr in ((0.30, [0.80, 0.60, 0.15]), (0.55, [0.90, 0.70, 0.2]), (0.80, [0.85, 0.65, 0.15])):
    s.line(wall_arc(f, 8, 125), grade="HB", pressure=pr, tip="side", width=0.020,
           smooth=False, note="bowl wall shade")
s.line(wall_arc(0.75, 30, 100), grade="2B", pressure=[0.2, 0.55, 0.2], tip="side", width=0.016,
       smooth=False, note="bowl wall shade core")
s.stump(wall_arc(0.55, 10, 125), strength=0.8, width=0.045, note="bowl wall shade")
print(f"bowl wall shade: {s.stroke_count - before} strokes")

# The cast shadow on the table: arcs from the belly outward, fading, their right
# ends tapered so the shadow's tip does not end on a line.
before = s.stroke_count
SC, SRX, SRY = (0.60, 0.725), 0.31, 0.105
for f, pr in ((0.0, 0.78), (0.15, 0.72), (0.34, 0.64), (0.50, 0.54), (0.70, 0.42), (0.92, 0.30)):
    c = (BELLY_C[0] + (SC[0] - BELLY_C[0]) * f, BELLY_C[1] + (SC[1] - BELLY_C[1]) * f)
    rx = BELLY_RX + (SRX - BELLY_RX) * f
    ry = BELLY_RY + (SRY - BELLY_RY) * f
    s.line(arc(c, rx, ry, 8, 172 - 40 * f, 30), grade="2B",
           pressure=[pr * 0.35, pr, pr, pr, pr * 0.5], tip="side", width=0.026, smooth=False,
           note="bowl cast shadow")
cast_stump = polygon(arc(BELLY_C, BELLY_RX + 0.005, BELLY_RY + 0.007, 172, 8, 30)
                     + arc(SC, SRX + 0.012, SRY + 0.016, 8, 172, 30), name="cast_stump")
s.stump(cast_stump, strength=0.8, note="bowl cast shadow")
print(f"bowl cast shadow: {s.stroke_count - before} strokes")

read(bowl_cast, "bowl_cast")
read(bowl_wall_shade, "bowl_wall_shade")
read(rim, "rim")
read(polygon([(0.25, 0.44), (0.80, 0.44), (0.80, 0.475), (0.25, 0.475)]), "table just above the rim")
print(s.look(grid=True))
print(s.look(region="B5:D7", grid=True))
