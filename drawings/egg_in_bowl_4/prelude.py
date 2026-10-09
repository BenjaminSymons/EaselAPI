"""Run before every pass, in the same scope: the shapes, the helpers, and the plan.

The picture: a hen's egg lying in a shallow white bowl on a wooden table, the window
to the upper left out of frame. The bowl sits a little below the middle of the sheet,
seen from a little above, so its rim is an ellipse and a sliver of its near wall shows
under the rim. The egg lies in the bowl's floor left of centre, lit on its upper-left,
its cast shadow running to the lower right inside the bowl. The bowl's interior shadow
is the right and back of the interior; the egg's shadow side is lost into it.

Why this subject: one light, one egg, and everything else in the picture is laid darker
so that the egg's lit side and the rim read as the light that was left alone.
"""
import math

W, H = 1024, 768
LONG = float(max(W, H))


# ----- geometry helpers ---------------------------------------------------------------

def ept(cx, cy, rx, ry, t, rot=0.0, k=1.0):
    """A point on an ellipse at angle t (degrees, clockwise from the right, y down),
    the ellipse rotated by rot degrees in pixel space and scaled by k about its centre."""
    a = math.radians(t)
    r = math.radians(rot)
    xp, yp = rx * k * math.cos(a) * W, ry * k * math.sin(a) * H
    xr = xp * math.cos(r) - yp * math.sin(r)
    yr = xp * math.sin(r) + yp * math.cos(r)
    return (cx + xr / W, cy + yr / H)


def arc(cx, cy, rx, ry, t0, t1, rot=0.0, k=1.0, step=3.0):
    """Points along an ellipse from t0 to t1, every `step` degrees."""
    n = max(2, int(round(abs(t1 - t0) / step)) + 1)
    return [ept(cx, cy, rx, ry, t0 + (t1 - t0) * i / (n - 1), rot, k) for i in range(n)]


def px_len(a, b):
    return math.hypot((b[0] - a[0]) * W, (b[1] - a[1]) * H)


def dense(a, b, every_px=8.0):
    """A straight run from a to b as points every `every_px` pixels."""
    n = max(2, int(px_len(a, b) / every_px) + 1)
    return [(a[0] + (b[0] - a[0]) * i / (n - 1), a[1] + (b[1] - a[1]) * i / (n - 1))
            for i in range(n)]


def bell(n, peak, ends=0.35):
    """A pressure list that rises to `peak` in the middle and falls to `ends`."""
    if n < 2:
        return [peak]
    return [ends + (peak - ends) * math.sin(math.pi * i / (n - 1)) for i in range(n)]


def ramp(n, a, b):
    return [a + (b - a) * i / max(1, n - 1) for i in range(n)]


def cut(points, pressures, keepouts, fade_px=30.0, floor=0.3, min_px=40.0, within=None):
    """Split a polyline into the runs that lie outside every keepout shape (and inside
    `within`, if given). Each run keeps its own pressures; at a cut end the pressure
    fades to `floor` of itself over the last `fade_px` pixels. Runs shorter than
    `min_px` are dropped."""
    runs, cur, curp = [], [], []
    for p, pr in zip(points, pressures):
        inside = any(s.contains(p[0], p[1]) for s in keepouts) if keepouts else False
        if within is not None and not within.contains(p[0], p[1]):
            inside = True
        if inside:
            if cur:
                runs.append((cur, curp, True))
            cur, curp = [], []
        else:
            cur.append(p)
            curp.append(pr)
    if cur:
        runs.append((cur, curp, False))
    out = []
    for i, (pts, prs, cut_end) in enumerate(runs):
        cut_start = i > 0
        length = sum(px_len(pts[j], pts[j + 1]) for j in range(len(pts) - 1))
        if length < min_px:
            continue
        d_from_start = [0.0]
        for j in range(1, len(pts)):
            d_from_start.append(d_from_start[-1] + px_len(pts[j - 1], pts[j]))
        faded = []
        for j, pr in enumerate(prs):
            f = 1.0
            if cut_start:
                f = min(f, floor + (1 - floor) * min(1.0, d_from_start[j] / fade_px))
            if cut_end:
                f = min(f, floor + (1 - floor) * min(1.0, (length - d_from_start[j]) / fade_px))
            faded.append(pr * f)
        out.append((pts, faded))
    return out


# ----- the arrangement ----------------------------------------------------------------

# The bowl: its outer silhouette, its rim (the ellipse the far rim's top surface draws),
# and its interior (the rim's inner edge). All share a centre in x.
BX, BY = 0.50, 0.615
SIL = (BX, BY, 0.310, 0.175)            # outer silhouette: top 0.44, bottom 0.79
RIM = (BX, 0.595, 0.300, 0.150)         # the rim's outer line: top 0.445, bottom 0.745
INT = (BX, 0.600, 0.285, 0.135)         # the interior: top 0.465, bottom 0.735

# The egg, lying in the bowl left of centre, tilted a little.
EX, EY, ERX, ERY, EROT = 0.455, 0.615, 0.105, 0.085, -8.0
EGG = (EX, EY, ERX, ERY)

# The egg's cast shadow's outer boundary: the egg's own shape shifted to the lower right.
CX2, CY2, CRX2, CRY2, CROT2 = 0.545, 0.648, 0.125, 0.082, 10.0
CAST2 = (CX2, CY2, CRX2, CRY2)


def eggpt(t, k=1.0):
    return ept(EX, EY, ERX, ERY, t, EROT, k)


def eggarc(t0, t1, k=1.0, step=3.0):
    return arc(EX, EY, ERX, ERY, t0, t1, EROT, k, step)


def castarc(t0, t1, k=1.0, step=3.0):
    return arc(CX2, CY2, CRX2, CRY2, t0, t1, CROT2, k, step)


def silarc(t0, t1, k=1.0, step=3.0, grow_px=0.0):
    cx, cy, rx, ry = SIL
    return arc(cx, cy, rx * k + grow_px / W, ry * k + grow_px / H, t0, t1, 0.0, 1.0, step)


def rimarc(t0, t1, k=1.0, step=3.0):
    cx, cy, rx, ry = RIM
    return arc(cx, cy, rx, ry, t0, t1, 0.0, k, step)


def intarc(t0, t1, k=1.0, step=3.0):
    cx, cy, rx, ry = INT
    return arc(cx, cy, rx, ry, t0, t1, 0.0, k, step)


def intarc_px(t0, t1, inset_px, step=3.0):
    """An arc of the interior's outline, inset by so many pixels all round."""
    cx, cy, rx, ry = INT
    return arc(cx, cy, rx - inset_px / W, ry - inset_px / H, t0, t1, 0.0, 1.0, step)


def interior_inset(inset_px):
    cx, cy, rx, ry = INT
    return polygon(arc(cx, cy, rx - inset_px / W, ry - inset_px / H, 0, 360, 0.0, 1.0, 4))


# Shapes, named, for the plan and the check. Angles: 0 right, 90 bottom, 180 left, 270 top.
silhouette = polygon(silarc(0, 360, step=4), name="silhouette")
rim_line = polygon(rimarc(0, 360, step=4), name="rim_line")
interior = polygon(intarc(0, 360, step=4), name="interior")
egg = polygon(eggarc(0, 360, step=4), name="egg")

# The far rim: the band between the silhouette and the interior over the back of the
# bowl, from the left round over the top to the right. Paper, the bowl's lit rim.
rim_lit = polygon(silarc(160, 380, step=4) + intarc(380, 160, step=4)[::1], name="rim_lit")

# The near wall: the sliver between the rim's lower half and the silhouette's.
wall = polygon(silarc(20, 160, step=4) + rimarc(160, 20, step=4), name="wall")

# The bowl's interior, lit (left end) and in shadow (right and back), the shadow
# polygon going round the egg so that the egg does not sit inside it.
bowl_lit = polygon(intarc(115, 245, step=4), name="bowl_lit")
bowl_shade = polygon(intarc(-105, 105, step=4) + eggarc(135, -70, k=1.06, step=4),
                     name="bowl_shade")

# The egg's lit side (a crescent on its upper left, paper) and its shadow side.
egg_lit = polygon(eggarc(130, 300, step=4) + eggarc(300, 130, k=0.55, step=4), name="egg_lit")
egg_shade = polygon(eggarc(-55, 125, step=4) + eggarc(125, -55, k=0.5, step=4), name="egg_shade")

# The cast shadow: between the egg's lower-right outline and the shifted shape.
cast = polygon(eggarc(140, 15, k=1.0, step=4) + castarc(15, 140, step=4), name="cast")

# The table, read in two places: the far plane over the top, the near plane below.
table_far = Region(0.0, 0.03, 1.0, 0.40, name="table_far")
table_near = Region(0.0, 0.82, 1.0, 0.99, name="table_near")

# Keep-outs for the row cutter: the bowl grown by a side stroke's half width and a few
# pixels, so that a run stops short of it; and the egg grown the same way for the
# arcs laid round the interior.
def grown(spec, by_px, rot=0.0):
    cx, cy, rx, ry = spec
    return polygon(arc(cx, cy, rx + by_px / W, ry + by_px / H, 0, 360, rot, 1.0, 4))


bowl_keepout_rows = grown(SIL, 40.0)            # rows at width 0.07: half is 36 px
egg_keepout_30 = grown(EGG, 19.0, EROT)          # arcs at width 0.03: half is 15 px
egg_keepout_20 = grown(EGG, 14.0, EROT)          # arcs at width 0.02
egg_keepout_45 = grown(EGG, 25.0, EROT)          # a stump dragged at width 0.045
egg_keepout_60 = grown(EGG, 37.0, EROT)          # a stump dragged at width 0.06


# ----- the plan -----------------------------------------------------------------------

s.plan(
    why="one light left alone: the egg's lit side and the rim are paper, and everything else is laid darker so that they read as the light",
    values={
        table_far: 0.58,
        table_near: 0.50,
        rim_lit: 0.93,
        wall: 0.72,
        bowl_lit: 0.80,
        bowl_shade: 0.56,
        egg_lit: 0.92,
        egg_shade: 0.56,
        cast: 0.26,
    },
    lightest=egg_lit,
    subject_share=0.45,
)
