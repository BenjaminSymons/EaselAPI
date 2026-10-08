"""Pass 8: repairs the stump can make, then the darks last, unstumped.

What the first rehearsal of this pass showed, beyond its own numbers: a side stroke
laid at a constant pressure starts and ends in a hard block, and over a lighter tone
a short one reads as a rectangle. Pass 7 left four of them: the crown-gap arc's left
run on the far-left inner wall, the far-rim hard-edge runs' ends either side of the
egg's crown, and the hard-edge band's outer side, which sits unstumped on a stumped
table and reads as an outline round the bowl. Stumps first, small and along the
strokes, so that the darks come after every stump near them.

Then the darks. The acceptance criterion is a darkest half-percentile 0.80 of the way
from the paper to black: value 0.19 on this paper, over about 3,900 px. The first
rehearsal's darks (a tapered 4B point line of 11 px and three short side arcs) read
0.24, 0.75 of the way. This version: the contact line at 13 px and held near full
pressure along its middle, a second under it, and four 4B arcs of the cast's own shape
beside the foot with their pressure tapering to the ends so that they do not block.

Budget for the pass: 16.
"""
before = len(s.history.records)
n = 0

# --- repairs: the blocks, stumped along their own strokes ------------------------------
s.stump(crescent_arc(0.3, 226, 242, step=2), strength=0.7, width=0.028,
        note="repair: the crown-gap arc's left run, blocked at its start")
# the crown spans t 248 to 273 on the rim; the runs end 8 px either side of it. The
# second rehearsal had these at 226-246 and 296-318, and the first reached the crown.
for t0, t1 in ((230, 243), (278, 292)):
    s.stump(ell(BOWL_CX, BOWL_CY, RIM_RX + 7, RIM_RY + 7, t0, t1, step=2), strength=0.6,
            width=0.022, note="repair: the far-rim edge run's end at the crown")
# the band's outer side, blended into the table; its inner edge on the bowl untouched
s.stump(ell(BOWL_CX, BOWL_CY, RIM_RX + 16, RIM_RY + 16, 178, 362, step=4), strength=0.5,
        width=0.018, note="repair: the far-rim edge band's outer side")
s.stump(ell(BOWL_CX, BOWL_CY, LOW_RX + 20, LOW_RY + 20, -2, 182, step=4), strength=0.5,
        width=0.02, note="repair: the near-wall edge band's outer side")
n += 5
print(s.look(region="B4:G6", scale=None, path="out/p08_0_repairs.png"))

# --- the darks ----------------------------------------------------------------------
contact = [egg_pt(t, 0.985) for t in range(58, 156, 3)]
# 6B: with 4B the darkest half-percentile read 0.20, 0.79 of the way, a hair under
s.line(contact, "6B", pressure=bell(len(contact), 0.45, 1.0, peak=0.5, spread=0.7),
       tip="point", width=0.013, smooth=False, note="subject dark, the contact under the egg")
contact2 = [egg_pt(t, 1.03) for t in range(66, 146, 3)]
s.line(contact2, "4B", pressure=bell(len(contact2), 0.35, 1.0, peak=0.5, spread=0.6),
       tip="side", width=0.014, smooth=False, note="subject dark, under the foot")
n += 2
# the cast's core beside the foot, where it comes out from under the egg: arcs of the
# cast's shape, each tapering to its ends
for k, t0, t1 in ((0.88, 70, 126), (0.72, 66, 130), (0.56, 60, 136), (0.40, 50, 150)):
    pts = cast_arc(k, t0, t1, step=3)
    s.line(pts, "4B", pressure=bell(len(pts), 0.25, 1.0, peak=0.5, spread=0.5), tip="side",
           width=0.016, smooth=False, note="subject dark, the cast's core")
    n += 1
# the egg's core, an accent
core = [egg_pt(t, 0.73) for t in range(4, 84, 3)]
s.line(core, "4B", pressure=bell(len(core), 0.2, 0.6, peak=0.5, spread=0.4), tip="side",
       width=0.011, smooth=False, note="subject dark, the core of the egg's shade")
n += 1
print("strokes:", n)
print(s.look(region="C4:G6", scale=None, path="out/p08_a_darks.png"))
print(s.look(path="out/p08_b_whole.png"))
print(s.report(since=before))
print(s.compare(s.plan(), path="out/p08_compare.png"))
print(s.checklist())
