"""Pass 5: the egg's cast shadow on the near floor, laid as arcs of its own shape.

Concentric arcs of the cast ellipse scaled inward; the pressure along every arc is a
function of the distance from the egg's foot, so the shadow is darkest where it comes
out from under the egg and lighter toward the wall, whatever the arc. Nothing is cut
round the egg: the arcs that pass under it lay the join, which is the lost edge the
plan names. Then the inner wall's shade is carried down its right end to meet the
cast, so the two are one mass. One stump along the outer arc for the penumbra, one
along the middle. The occlusion dark under the egg is for the darks pass.

First version (rehearsed, not committed): a shorter ellipse to the egg's right, cut
round the egg, pressure heavier per arc toward the ellipse's centre. It read cast
+0.03 and looked like a dark puddle beside the egg with a gap of paper at the foot.

Planned: cast 0.33. Budget for the pass: 30.
"""
before = len(s.history.records)
n = 0


def foot_pressure(pts, near=0.95, far=0.60, reach=170.0):
    # far was 0.45 in the second rehearsal: a 2B held that lightly left the far end
    # a speckle the stump did not close
    out = []
    for x, y in pts:
        d = math.hypot(x * W - EGG_FOOT[0], y * H - EGG_FOOT[1])
        out.append(far + (near - far) * math.exp(-(d / reach) ** 2))
    return out


ks = (0.97, 0.86, 0.75, 0.64, 0.53, 0.42, 0.30)
grades = ("HB", "2B", "2B", "2B", "2B", "2B", "2B")
for k, grade in zip(ks, grades):
    pts = cast_arc(k, 0, 360, step=5)
    s.line(pts, grade, pressure=foot_pressure(pts), tip="side", width=0.02, smooth=False,
           note=f"subject cast shadow k={k}")
    n += 1
print(s.look(region="D5:H6", scale=None, path="out/p05_a_arcs.png"))

# the inner wall's shade carried down its right end, to meet the cast
for k, grade, p in ((0.2, "HB", 0.9), (0.5, "2B", 0.7), (0.8, "2B", 0.6)):
    pts = crescent_arc(k, 330, 384, step=3)
    s.line(pts, grade, pressure=[p * 0.8, p, p * 0.7], tip="side", width=0.016,
           smooth=False, note="subject inner wall shade, down to the cast")
    n += 1

s.stump(cast_arc(0.98, 0, 360, step=8), strength=0.7, width=0.04,
        note="cast penumbra stump along")
s.stump(cast_arc(0.6, 0, 360, step=8), strength=0.6, width=0.05,
        note="cast stump along the middle")
s.stump(crescent_arc(0.5, 330, 384, step=4), strength=0.6, width=0.035,
        note="inner wall stump, right end")
n += 3
print("strokes:", n)
print(s.look(region="D5:H6", scale=None, path="out/p05_b_stumped.png"))
print(s.look(path="out/p05_c_whole.png"))
print(s.report(since=before))
print(s.compare(s.plan(), path="out/p05_compare.png"))
