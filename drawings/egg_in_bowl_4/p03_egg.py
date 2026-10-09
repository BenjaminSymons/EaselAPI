"""Pass 3: the egg. Its shadow side as cross-contours of its own shape scaled inward,
each arc shorter than the one before so that their ends trace the terminator, the
pressure heavier where the form turns from the light; a stump along the terminator;
and the two bands beside the egg that the interior's arcs stopped short of, laid along
its silhouette in the floor's own values: 2H round the lit side, HB round the shade side.
The lit crescent stays paper never touched."""


def lay(pts, prs, grade, width, note, keepouts=()):
    for run_pts, run_prs in cut(pts, prs, list(keepouts)):
        s.line(run_pts, grade, pressure=run_prs, tip="side", width=width,
               smooth=False, note=note)


# --- the shadow side: cross-contours, ends on the terminator ---------------------------
for k, grade, peak, t0, t1 in ((0.96, "HB", 0.75, -62, 128),
                               (0.88, "HB", 0.95, -55, 120),
                               (0.80, "2B", 0.85, -48, 110),
                               (0.72, "HB", 0.95, -40, 100),
                               (0.64, "2H", 1.00, -30, 90),
                               (0.56, "2H", 0.80, -20, 80)):
    pts = eggarc(t0, t1, k=k)
    s.line(pts, grade, pressure=bell(len(pts), peak, 0.3), tip="side", width=0.014,
           smooth=False, note="subject: egg shade")
s.stump(eggarc(-35, 95, k=0.6), strength=0.7, width=0.035, note="subject: egg terminator")
s.stump(eggarc(-50, 118, k=0.86), strength=0.8, width=0.03, note="subject: egg shade closed")
# (the first rehearsal's crop showed the six arcs as rings; a stump along their middle)
s.look(path="out/p03_look_01_shade.png")

# --- the floor's bands beside the egg, along its silhouette ---------------------------
lit_band = arc(EX, EY, ERX + 13 / W, ERY + 13 / H, 125, 305, EROT)
s.line(lit_band, "2H", pressure=bell(len(lit_band), 0.9, 0.5), tip="side", width=0.025,
       smooth=False, note="floor beside the egg, lit")
shade_band = arc(EX, EY, ERX + 12 / W, ERY + 12 / H, -75, 135, EROT)
s.line(shade_band, "HB", pressure=bell(len(shade_band), 0.9, 0.5), tip="side", width=0.025,
       smooth=False, note="subject: floor beside the egg, shade")
print(s.look(path="out/p03_after.png"))
print(s.look(region="C5:F7", scale=None, path="out/p03_after_crop.png"))
print(s.budget_line())
print(s.compare(s.plan()))
