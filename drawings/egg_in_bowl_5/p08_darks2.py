"""Pass 8: more dark, by area. The closing check read darks: 0.26, 0.73 of the way,
under 0.80: the contact shadow under the egg was dark enough (cast_core 0.19) but not
the four thousand pixels the darkest half-percent reads. The darkest place in this
setup is also the crevice where the bowl's belly meets the table under its near rim,
so a 6B goes along that join, and two more arcs widen the egg's contact shadow. All
after every stump near them, and left unstumped.

The first rehearsal reached 0.85 with two crevice strokes and read as two stacked
bars with a block at the left end; this one lays one, its list falling to nothing.
"""
cx, cy, a, b = EGG
# the crevice under the bowl: along the belly's lower silhouette, 7 px outside it
s.line(silhouette(42, 100, 7.0, step=2), "6B", pressure=[0.05, 0.4, 0.9, 0.9, 0.4, 0.05],
       tip="side", width=0.024, smooth=False, note="darks crevice")
# the egg's contact shadow, two arcs further into the cast shadow
for scale, (t0, t1), pr in ((1.29, (62, 118), [0.15, 0.6, 0.85, 0.6, 0.15]),
                            (1.38, (68, 112), [0.1, 0.5, 0.75, 0.5, 0.1])):
    s.line(egg_pts(cx, cy, a, b, t0, t1, scale=scale, step=3), "6B", pressure=pr,
           tip="side", width=0.024, smooth=False, note="subject darks")
print(s.look(region="C4:G7", scale=None, path="out/p08_look_01_crop.png"))
print(s.look(path="out/p08_look_01.png"))
print(s.checklist())
