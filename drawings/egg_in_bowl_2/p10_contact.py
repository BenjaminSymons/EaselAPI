"""Pass 10: the passage I would apologise for. The contact under the egg.

Looked at small (look --scale 256), the 6B contact line of pass 8 reads as a black
outline under the egg: its left third runs against the lit floor, where the occlusion
shadow is a sliver, and the bell of pressure still left 6B at 0.45 there. And the
four 4B arcs of the cast's core stack into a rectangle beside the foot.

(Pass 9, forty horizontal rows of grain over the table, was rehearsed and dropped:
at 0.028 wide and unstumped the side tip's dabs read as brickwork, and the row ends
stood round the bowl as a staircase of blocks. The table stays as it is.)

A mark stays, so the contact's left third is graded away with the kneaded eraser,
twice at falling strength, each held to a place that is the line and a few pixels
either side and nothing else. The bars are softened with one stump along their
outline at half strength. Then the occlusion shadow is rebuilt as arcs of the egg's
own foot grown outward, 4B, tapering to both ends, laid after that stump and left:
darkest under the lowest point of the egg, fading toward the light and into the cast.

Budget for the pass: 10.
"""
before = len(s.history.records)
n = 0


def foot_band(t0, t1, k_in, k_out, step=2):
    """A place along the egg's outline between two scalings, for a lift."""
    return polygon(egg_arc(t0, t1, k_in, step) + egg_arc(t1, t0, k_out, step)[1:])


# the contact's left third, graded away toward the light
# (first rehearsal: kneaded at 0.7 over 56-80 and 0.4 over 76-94 left the end a dark
# grey and the small look a black smile; the plastic takes 0.92 where kneaded 0.7
# takes 0.6, per the calibration)
# (third rehearsal: these were at t 54-76, 74-88, 86-98, which is the egg's lower
# RIGHT, under the cast: the plastic left a white rectangle in the shadow. The egg's
# parameter runs 0 at the narrow end, 90 down, 180 at the blunt end; the lowest point
# of the outline on the sheet is at t 118, pixel (426, 494), and the end toward the
# light is t 125 to 156. EGG_FOOT in the prelude, (470, 486), is 44 px right of the
# true foot; p05's pressures were weighted round it. Left as laid.)
s.plastic(foot_band(140, 158, 0.93, 1.09), note="repair: the contact's end toward the light")
s.kneaded(foot_band(128, 142, 0.93, 1.09), strength=0.6,
          note="repair: the contact's third toward the light, lifted")
s.kneaded(foot_band(118, 130, 0.93, 1.09), strength=0.3,
          note="repair: the contact's third toward the light, lifted a little")
n += 3
# the bars' outline, softened
s.stump(cast_arc(0.92, 60, 136, step=4), strength=0.5, width=0.03,
        note="repair: the cast core's outer edge, softened")
s.stump(cast_arc(0.34, 46, 154, step=4), strength=0.5, width=0.03,
        note="repair: the cast core's inner edge, softened")
n += 2
print(s.look(region="C5:G6", scale=None, path="out/p10_a_lifted.png"))

# the occlusion shadow, as the egg's own foot grown outward, after every stump near it
for k, t0, t1, hi in ((1.03, 62, 132, 1.0), (1.08, 66, 128, 0.9), (1.14, 70, 124, 0.75)):
    pts = egg_arc(t0, t1, k, step=2)
    s.line(pts, "4B", pressure=bell(len(pts), 0.15, hi, peak=0.7, spread=0.45), tip="side",
           width=0.014, smooth=False, note="subject dark, the occlusion under the foot")
    n += 1
# and the crevice itself under the lowest point, 6B on the outline, left
# (one 6B arc 12 px wide read 0.21, 0.78 of the way: the darkest half-percentile is
# about 3,900 px and wants that much at the value, so two arcs, wider)
pts = egg_arc(70, 128, 1.0, step=2)
s.line(pts, "6B", pressure=bell(len(pts), 0.5, 1.0, peak=0.72, spread=0.55), tip="side",
       width=0.018, smooth=False, note="subject dark, the crevice under the egg")
n += 1
# (two crevice arcs over the line read 0.21 still: they overlapped the line they sat
# on. The cast's core beside the foot is the dark that can grow: 6B arcs of the cast's
# shape, each a different length so they fan out rather than stack into a block.)
for k, t0, t1 in ((0.86, 76, 124), (0.70, 64, 136), (0.54, 50, 150), (0.38, 34, 166)):
    pts = cast_arc(k, t0, t1, step=3)
    s.line(pts, "6B", pressure=bell(len(pts), 0.25, 0.85, peak=0.5, spread=0.5), tip="side",
           width=0.016, smooth=False, note="subject dark, the cast's core, 6B")
    n += 1
# the gap between the crevice's right end and the cast's core, bridged
bridge = [U(518, 468), U(540, 472), U(562, 475), U(588, 479)]
s.line(bridge, "6B", pressure=[0.5, 0.9, 0.9, 0.5], tip="side", width=0.016, smooth=False,
       note="subject dark, from the crevice into the cast's core")
n += 1
print("strokes:", n)
print(s.look(region="C5:G6", scale=None, path="out/p10_b_done.png"))
print(s.look(scale=256, sketch=False, path="out/p10_c_small.png"))
print(s.look(sketch=False, path="out/p10_d_whole.png"))
print(s.report(since=before))
print(s.compare(s.plan(), path="out/p10_compare.png"))
print(s.checklist())
