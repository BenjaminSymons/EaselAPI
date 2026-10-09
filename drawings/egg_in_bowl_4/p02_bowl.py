"""Pass 2: the bowl's interior, and the table's band round the bowl.

First the band the rows stopped short of, laid along the silhouette in the table's own
value as one layer: two arcs round the far half in 2H leant on, two round the near
half in HB, and a stump along each half to close them (the first rehearsal showed the
band as a ring of white speckle). Then the interior shadow: arcs of the interior's own
outline inset by pixels, from the back-left round the right, fading at both ends, cut
round the egg; and arcs of the egg's own shape grown outward, for the floor beside it.
Then the lit end of the interior, three 2H arcs held light. Stumps along the arcs, not
over a polygon: the first rehearsal's polygon stump left a hard chord where it stopped."""

LOOK = [0]


def look(tag):
    LOOK[0] += 1
    s.look(path=f"out/p02_look_{LOOK[0]:02d}_{tag}.png")


def lay(pts, prs, grade, width, note, keepouts=(), within=None):
    """Lay a run, cut round the keepouts, as one line per run."""
    n = 0
    for run_pts, run_prs in cut(pts, prs, list(keepouts), within=within):
        s.line(run_pts, grade, pressure=run_prs, tip="side", width=width,
               smooth=False, note=note)
        n += 1
    return n


# --- the table's band round the bowl --------------------------------------------------
far1 = silarc(170, 370, grow_px=20)
far2 = silarc(170, 370, grow_px=52)
near1 = silarc(-10, 190, grow_px=20)
near2 = silarc(-10, 190, grow_px=52)
lay(far1, bell(len(far1), 1.00, 0.75), "2H", 0.040, "table band, far")
lay(far2, bell(len(far2), 1.00, 0.75), "2H", 0.045, "table band, far")
lay(near1, bell(len(near1), 0.85, 0.65), "HB", 0.040, "table band, near")
lay(near2, bell(len(near2), 0.85, 0.65), "HB", 0.045, "table band, near")
s.stump(silarc(165, 375, grow_px=40), strength=1.0, width=0.07, note="table band closed, far")
s.stump(silarc(-15, 195, grow_px=40), strength=1.0, width=0.07, note="table band closed, near")
look("band")

# --- the interior shadow: along the rim's inside, then round the egg -------------------
shade_within = interior_inset(16)
for inset in (18, 38, 58, 78):
    pts = intarc_px(-135, 108, inset)
    lay(pts, bell(len(pts), 0.95, 0.35), "HB", 0.030, "subject: bowl shade",
        keepouts=[egg_keepout_30])
for k in (1.22, 1.46, 1.70, 1.94, 2.18):
    pts = eggarc(-110, 118, k=k)
    lay(pts, bell(len(pts), 0.95, 0.40), "HB", 0.030, "subject: bowl shade, round the egg",
        keepouts=[egg_keepout_30], within=shade_within)
look("shade_arcs")

# --- the lit end of the interior -------------------------------------------------------
for inset in (18, 40, 62):
    pts = intarc_px(112, 248, inset)
    lay(pts, bell(len(pts), 0.90, 0.40), "2H", 0.035, "bowl lit", keepouts=[egg_keepout_30])

# --- the stumps, along the arcs, cut round the egg so that none crosses its top --------
def stump_along(path, width, strength, note, keepouts=()):
    for run_pts, _ in cut(path, [1.0] * len(path), list(keepouts), min_px=40):
        s.stump(run_pts, strength=strength, width=width, note=note)


stump_along(intarc_px(-135, 108, 40), 0.06, 1.0, "subject: bowl shade closed", [egg_keepout_60])
stump_along(intarc_px(-125, 100, 84), 0.06, 1.0, "subject: bowl shade closed", [egg_keepout_60])
s.stump(eggarc(-105, 115, k=1.7), strength=1.0, width=0.07, note="subject: bowl shade closed")
stump_along(intarc_px(112, 248, 40), 0.05, 0.7, "bowl lit closed", [egg_keepout_60])
print(s.look(path="out/p02_after.png"))
print(s.budget_line())
print(s.compare(s.plan()))
