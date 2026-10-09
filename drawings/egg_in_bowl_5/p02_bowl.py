"""Pass 2: the bowl. The band beside it, its shadow on the table, its walls, its
interior shadow with the egg's cast shadow lying in it, and a stump along each.

The band fills the 40 px of paper the rows stopped short of, as arcs along the
silhouette: an outer layer at width 0.07 and an inner one at 0.03, in the table's own
grade and pressure on each side, and in the cast shadow's where the bowl's shadow
falls on the table (angles -15 to 100 about the bowl's centre; 270 is the top).

Rehearsed three times: the first laid nothing inside the bowl (arc_cut took normalised
points as pixels); the second read the interior shadow 0.60-0.66 against 0.45, the
table shadow 0.49 against 0.34, and left a hole in the cast body; this one lays the
cast shadow under the egg in 2B leant on, the table shadow's inner layers in 2B, and
stumps the interior at 0.6 along its arcs.
"""
laid = 0


def arc(pts, grade, pressure, width=0.024, note=""):
    global laid
    s.line(pts, grade, pressure=pressure, tip="side", width=width, smooth=False, note=note)
    laid += 1


def arcs_cut(pts_px, grade, pressure, width, note, margin):
    global laid
    for pts, pl in cut_arc(pts_px, pressure, in_egg, margin):
        s.line(pts, grade, pressure=pl, tip="side", width=width, smooth=False, note=note)
        laid += 1


# --- the band beside the bowl: the table's own value, two layers ----------------
arc(silhouette(170, 372, 44), "2H", [0.4, 0.55, 0.72, 0.68, 0.45], width=0.07, note="band far")
arc(silhouette(170, 372, 15), "2H", [0.5, 0.80, 1.00, 0.95, 0.55], width=0.03, note="band far")
arc(silhouette(180, 98, 44), "HB", [0.4, 0.70, 0.75, 0.5], width=0.07, note="band near")
arc(silhouette(180, 98, 15), "HB", [0.4, 0.75, 0.80, 0.5], width=0.03, note="band near")
# the bowl's shadow on the table, lower right: 2B leant on inside, HB outside
arc(silhouette(104, -18, 15), "2B", [0.5, 0.9, 0.9, 0.85, 0.5], width=0.03, note="bowl cast")
arc(silhouette(104, -18, 44), "2B", [0.5, 0.85, 0.85, 0.8, 0.5], width=0.07, note="bowl cast")
arc(silhouette(100, -12, 88), "HB", [0.3, 0.8, 0.8, 0.7, 0.3], width=0.06, note="bowl cast")
print(s.look(path="out/p02_look_01.png"))

# --- the outer wall below the rim, lit at the left and turning away to the right ---
arc(ell_pts(512, 462, 256, 97, 160, 20), "2H", [0.35, 0.75, 1.0, 1.0], note="outer wall")
# --- the left inner wall, facing away from the window: a half-tone -----------------
arc(ell_pts(512, 439, 262, 86, 148, 218), "2H", [0.4, 0.85, 0.85, 0.4], note="left wall")

# --- the interior shadow: the near crescent, then the cast shadow, cut round the egg
M = 15.0
arcs_cut(ell_px(512, 439, 262, 86, 168, 14, step=3), "HB", [0.3, 0.9, 1.0, 1.0, 0.9],
         0.024, "near crescent", M)
arcs_cut(ell_px(512, 439, 246, 70, 160, 22, step=3), "HB", [0.3, 0.9, 1.0, 1.0, 0.9],
         0.024, "near crescent", M)
cx, cy, rx, ry, rot = CAST
for k, pk in ((0.95, 0.75), (0.72, 0.85), (0.5, 0.85), (0.26, 0.8)):
    arcs_cut(ell_px(cx, cy, rx * k, ry * k, 200, 560, step=4, rot=rot), "2B",
             [0.45, pk, pk, pk, 0.45], 0.024, "cast shadow", M)
print("laid so far:", laid)
print(s.look(path="out/p02_look_02.png"))
print(s.look(region="C4:G7", scale=None, path="out/p02_look_02_crop.png"))

# --- the stumps: along the band, held off the bowl's paper by half their width -----
s.stump(silhouette(170, 372, 52), strength=1.0, width=0.09, note="band stump")
s.stump(silhouette(180, 98, 52), strength=1.0, width=0.09, note="band stump")
s.stump(silhouette(104, -18, 60), strength=1.0, width=0.11, note="bowl cast stump")
s.stump(ell_pts(512, 462, 256, 97, 160, 20), strength=0.8, width=0.03, note="outer wall stump")
s.stump(ell_pts(512, 439, 262, 86, 148, 218), strength=0.8, width=0.03, note="left wall stump")
s.stump(ell_pts(512, 439, 254, 78, 168, 14), strength=0.6, width=0.05, note="near crescent stump")
s.stump(cast_body, strength=0.6, note="cast shadow stump")
print(s.look(path="out/p02_look_03.png"))
print(s.look(region="C4:G7", scale=None, path="out/p02_look_03_crop.png"))

# Read the band and the walls by their medians, against my own values (not the plan).
band_far_probe = polygon(silhouette(215, 325, 8) + silhouette(325, 215, 70), name="band_far_probe")
band_near_probe = polygon(silhouette(110, 170, 8) + silhouette(170, 110, 70), name="band_near_probe")
outer_wall_probe = polygon(ell_pts(512, 462, 266, 108, 60, 120) + ell_pts(512, 438, 290, 108, 120, 60),
                           name="outer_wall_probe")
print(s.compare({band_far_probe: 0.68, band_near_probe: 0.55, outer_wall_probe: 0.72,
                 cast_table: 0.34, bowl_shadow: 0.45, near_cres: 0.45, cast_body: 0.45},
                path="out/p02_compare.png"))
