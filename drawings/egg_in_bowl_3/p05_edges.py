"""Pass 5: edges. The band beside the bowl, in the table's own value, along the bowl's
silhouette where the rows stopped short; then the one hard edge, the bowl's rim against
the far table: a narrow side stroke in the table's value, its centre two pixels outside
the rim, laid after every stump near it."""
since = len(s.history.records)


def p_far(x, y):
    return min(1.0, 0.50 + 0.15 * max(0.0, min(1.0, x)) + 1.15 * max(0.0, y))


def p_near(x, y):
    return min(1.0, 0.52 + 0.06 * max(0.0, min(1.0, x)) + 0.16 * max(0.0, (y - 0.45)) / 0.55)


# --- the band: two side strokes outside the silhouette, the first 36 px wide centred
# 20 px out, the second 50 px wide centred 44 px out, over the rows' ragged ends; each
# arc runs past the bowl's sides so the two overlap where rim meets outer wall
for width, g, grade_far, grade_near in ((0.035, 20, "2H", "HB"), (0.05, 44, "2H", "HB")):
    gx, gy = g / W, g / H
    far_band = ell_pts(BOWL_C, RIM_RX + gx, RIM_RY + gy, 174, 366, step=3)      # over the top
    s.line(far_band, grade_far, pressure=[p_far(x, y) for x, y in far_band], tip="side",
           width=width, smooth=False, note="table far band")
    near_band = ell_pts(OUTER_C, OUTER_RX + gx, OUTER_RY + gy, -6, 186, step=3)   # under
    for run in runs_outside(near_band, bowl_cast_seen):
        s.line(run, grade_near, pressure=[p_near(x, y) for x, y in run], tip="side",
               width=width, smooth=False, note="table near band")
print(s.look(path="out/p05_band.png"))
gx, gy = 20 / W, 20 / H
s.stump(polygon(ell_pts(BOWL_C, RIM_RX + 4 * gx, RIM_RY + 4 * gy, 176, 364, step=3)
                + ell_pts(BOWL_C, RIM_RX + 0.3 * gx, RIM_RY + 0.3 * gy, 364, 176, step=3)),
        strength=0.8, note="table far band")
s.stump(polygon(ell_pts(OUTER_C, OUTER_RX + 4 * gx, OUTER_RY + 4 * gy, -4, 184, step=3)
                + ell_pts(OUTER_C, OUTER_RX + 0.3 * gx, OUTER_RY + 0.3 * gy, 184, -4, step=3)),
        strength=0.8, note="table near band")
print(s.look(path="out/p05_band_stumped.png"))

# --- the hard edge: the rim against the far table, laid last, centre 2 px outside
ex, ey = 2 / W, 2 / H
edge = ell_pts(BOWL_C, RIM_RX + ex, RIM_RY + ey, 184, 356, step=2)
s.line(edge, "2H", pressure=[min(1.0, p_far(x, y) + 0.05) for x, y in edge], tip="side",
       width=0.013, smooth=False, note="hard edge")
print(s.look(region="B4:G5", scale=None, path="out/p05_hard_edge.png"))
print(s.look(path="out/p05_whole.png"))
print(s.compare(s.plan(), path="out/p05_compare.png"))
print(s.budget_line())
