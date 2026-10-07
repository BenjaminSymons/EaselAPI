# Pass 6: what the look without the sketch showed weakest. The lit floor left of
# the egg evened; the crescent's left tip lifted where the light comes in; the
# speckle on the bowl's lit exterior stumped; the wall's uncovered top strip; and
# the table given a few grain marks and its back edge, so it reads as wood and as a
# plane with a far edge rather than as grey felt.
in_egg = egg.contains
before = s.stroke_count

# the floor: its arcs read as bands (the first version of this pass added two more
# and made it worse). Lift what is there by half, then one even light hatch of
# narrow side strokes, cut by the floor's own outline round the egg, and a stump.
#
# Third version: the lift was first laid over the whole floor polygon, which holds
# the egg's cast shadow too, and took the drawing's darkest mass up by 0.29 with
# it. The bands were only left of the egg, so the lift is held to there.
floor = floor_poly(shrink=0.012)
floor_left = polygon(arc(INNER_C, INNER_RX - 0.012 * 0.75, INNER_RY - 0.012, 102, 200, 24)
                     + [push_out(egg, p, EGG_C) for p in arc((0.50, 0.60), 0.20, 0.05, 200, 102, 16)],
                     name="floor_left")
s.kneaded(floor_left, strength=0.5, note="floor lifted")
s.hatch(floor, angle=4, spacing=0.011, grade="2H", pressure=0.62, tip="side", width=0.018,
        note="floor")
s.stump(floor_poly(shrink=0.014), strength=0.8, note="floor")

# the crescent's left tip, lifted: the light comes in from there
tip = polygon(arc(INNER_C, INNER_RX, INNER_RY, 196, 226, 12)
              + arc(INNER_C, INNER_RX * 0.86, INNER_RY * 0.86, 226, 196, 12), name="crescent_tip")
s.kneaded(tip, strength=0.55, note="bowl shadow tip")

# the bowl's lit exterior, where the shade arcs faded into speckle
s.stump(wall_arc(0.5, 95, 172), strength=0.7, width=0.04, note="bowl wall lit side")

# the wall's top strip
s.line([(-0.02, 0.012), (1.02, 0.008)], grade="2H", pressure=[0.55, 0.75], tip="side", width=0.05,
       smooth=False, note="wall")
print(f"repairs: {s.stroke_count - before} strokes")

# the table: a few grain marks, each its own length and wander, none parallel to
# the next, stopping at the bowl; and the back edge of the table top
before = s.stroke_count
grain = [
    ([(0.02, 0.43), (0.18, 0.425), (0.31, 0.432), (0.40, 0.428)], 0.34),
    ([(0.55, 0.455), (0.72, 0.452), (0.86, 0.46), (0.99, 0.455)], 0.30),
    ([(0.04, 0.62), (0.12, 0.628), (0.19, 0.622)], 0.36),
    ([(0.03, 0.80), (0.20, 0.806), (0.38, 0.80), (0.52, 0.808), (0.60, 0.804)], 0.36),
    ([(0.70, 0.86), (0.84, 0.866), (0.97, 0.86)], 0.32),
    ([(0.25, 0.93), (0.40, 0.925), (0.58, 0.934), (0.70, 0.93)], 0.34),
    ([(0.86, 0.69), (0.97, 0.695)], 0.30),
]
for pts, pr in grain:
    runs = cut_runs(pts if len(pts) > 2 else pts + [pts[-1]], lambda x, y: bowl.contains(x, y)
                    or rim_grown.contains(x, y) and y < 0.5, min_pts=2)
    for r in runs:
        s.line(r, grade="HB", pressure=[pr * 0.4, pr, pr * 0.8, pr * 0.3], tip="point",
               width=0.0045, smooth=True, note="table grain")
s.line([(-0.02, TABLE_Y_L + 0.004), (0.5, (TABLE_Y_L + TABLE_Y_R) / 2 + 0.004), (1.02, TABLE_Y_R + 0.004)],
       grade="HB", pressure=[0.35, 0.55, 0.42], tip="side", width=0.009, smooth=True, note="table back edge")
print(f"table grain and edge: {s.stroke_count - before} strokes")

read(floor, "floor")
read(tip, "crescent tip")
read(egg, "egg as a place")
print(s.look(grid=True, sketch=False))
print(s.look(region="C5:F7", grid=True, sketch=False))
