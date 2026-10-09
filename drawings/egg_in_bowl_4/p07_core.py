"""Pass 7: the core of the dark, once more. The closing check read the darkest
half-percentile at 0.22, 0.78 of the way from paper to black, under the 0.80 the
criterion asks for: the 4B arcs with their pressure falling to the ends did not reach
it. Two 6B arcs along the contact under the egg, leant on, laid over the 4B and left
unstumped; nothing else is touched."""

# (The first rehearsal ran these from 25 to 125 with the ends at half pressure, and a
# 6B at half pressure is still black: the ends stood out of the shadow as a slab under
# the egg's lower left. Shorter, and the ends let fall to near nothing.)
for d in (12.0, 34.0):
    core = arc(EX, EY, ERX + d / W, ERY + d / H, 32, 112, EROT)
    s.line(core, "6B", pressure=bell(len(core), 0.9, 0.12), tip="side", width=0.03,
           smooth=False, note="subject: cast shadow core, 6B")
# And the sliver of bare floor at the interior's left end, between the lit arcs and the
# egg's band, which read as a sharp bright notch at full size: one 2H arc held light,
# and a stump along it, cut round the egg.
sl = intarc_px(130, 232, 84)
for run_pts, run_prs in cut(sl, bell(len(sl), 0.85, 0.4), [egg_keepout_30]):
    s.line(run_pts, "2H", pressure=run_prs, tip="side", width=0.035, smooth=False,
           note="bowl lit, the floor's last sliver")
for run_pts, _ in cut(sl, [1.0] * len(sl), [egg_keepout_45], min_px=40):
    s.stump(run_pts, strength=1.0, width=0.045, note="bowl lit closed, the sliver")
print(s.look(path="out/p07_after.png"))
print(s.look(region="C5:F7", scale=None, path="out/p07_after_crop.png"))
print(s.budget_line())
print(s.checklist())
