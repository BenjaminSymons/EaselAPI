"""Pass 4: the egg's shade, laid along its own form.

Arcs of the egg's outline scaled inward, each kept to where it lies beyond the
terminator (shade_depth from the prelude), so the ends of the arcs trace the
terminator and no stroke crosses into the light. The outermost arc is the reflected
light off the bowl's white floor and is held lighter; the core is 2B in the middle of
the crescent; the half-tone that turns into the light is a 2H arc along the terminator
itself. Then stumps along the arcs. The contact shadow under the egg is for the darks
pass, after every stump.

Planned: egg_shade 0.47, egg_light 0.94 untouched. Budget for the pass: 35.
"""
before = len(s.history.records)
n = 0


def shade_arc(k, step=3, grace=0.02):
    """The part of the egg's outline scaled by k that lies beyond the terminator."""
    ts = [t for t in range(0, 360, step) if k > 1.0 - shade_depth(t) + grace]
    if len(ts) < 3:
        return []
    return [egg_pt(t, k) for t in _run(ts)]


# outermost first, in toward the terminator
arcs = (
    (0.995, "HB", 0.35, 0.60),     # the outline itself: the edge against the paper floor
    (0.965, "HB", 0.45, 0.70),     # the reflected light: lighter
    (0.895, "HB", 0.55, 0.90),
    (0.825, "2B", 0.45, 0.80),
    (0.755, "2B", 0.50, 0.88),     # the core
    (0.685, "2B", 0.45, 0.85),
    (0.615, "2B", 0.40, 0.75),
    (0.545, "HB", 0.50, 0.90),
    (0.475, "HB", 0.45, 0.80),
    (0.405, "2H", 0.50, 0.90),
)
for k, grade, lo, hi in arcs:
    pts = shade_arc(k)
    if not pts:
        continue
    s.line(pts, grade, pressure=bell(len(pts), lo, hi, peak=0.5, spread=0.55),
           tip="side", width=0.012 if k > 0.99 else 0.016, smooth=False,
           note=f"subject egg shade k={k}")
    n += 1
print(s.look(region="C4:F6", scale=None, path="out/p04_a_arcs.png"))

# the half-tone along the terminator, a hard grade leant on
term = [egg_pt(t, 1.0 - shade_depth(t) + 0.035) for t in _run(_shade_ts)]
s.line(term, "2H", pressure=bell(len(term), 0.45, 0.9, peak=0.5, spread=0.5), tip="side",
       width=0.02, smooth=False, note="subject egg half-tone along the terminator")
n += 1
# and a lighter one further toward the light, still on the shade side of the chord
term2 = [egg_pt(t, 1.0 - shade_depth(t) + 0.10) for t in _run(_shade_ts)]
s.line(term2, "2H", pressure=bell(len(term2), 0.3, 0.72, peak=0.5, spread=0.45), tip="side",
       width=0.024, smooth=False, note="subject egg half-tone, second")
n += 1

# stumps along the arcs, and one along the terminator for the turn into the light
for k in (0.9, 0.72, 0.54):
    pts = shade_arc(k, step=6)
    if pts:
        s.stump(pts, strength=0.7, width=0.035, note="egg stump along the arcs")
        n += 1
s.stump([egg_pt(t, 1.0 - shade_depth(t) + 0.06) for t in _run(_shade_ts)[::2]],
        strength=0.5, width=0.04, note="egg stump along the terminator")
n += 1
print("strokes:", n)
print(s.look(region="C4:F6", scale=None, path="out/p04_b_stumped.png"))
print(s.look(path="out/p04_c_whole.png"))
print(s.report(since=before))
print(s.compare(s.plan(), path="out/p04_compare.png"))
