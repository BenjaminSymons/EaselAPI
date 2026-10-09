"""Run before every pass, in the same scope: the shapes, the helpers, and the plan.

The subject: a hen's egg in a shallow white bowl on a wooden table, lit from a window
to the upper left (in front of the subject, high). Everything is built in pixels on
the 1024x768 sheet and converted, because a radius in `0..1` is two distances.

Why this subject (the guide asks for one sentence): a white egg in a white bowl is the
light drawn as paper, and the whole drawing exists to make that paper read as light.
"""
import math
from easel import polygon, ellipse, union, span, Region

W, H = 1024, 768


def N(px, py):
    """A pixel as a place."""
    return (px / W, py / H)


def ell_pts(cx, cy, rx, ry, t0, t1, step=5.0, rot=0.0):
    """Points of an elliptical arc in pixels, angles in degrees clockwise (y down)."""
    n = max(2, int(abs(t1 - t0) / step) + 1)
    pts = []
    for i in range(n):
        t = math.radians(t0 + (t1 - t0) * i / (n - 1))
        x, y = rx * math.cos(t), ry * math.sin(t)
        if rot:
            r = math.radians(rot)
            x, y = x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r)
        pts.append(N(cx + x, cy + y))
    return pts


def egg_pts(cx, cy, a, b, t0, t1, scale=1.0, step=5.0, rot=-18.0, fat=0.18):
    """Points of an egg outline (big end to the left), scaled about its centre."""
    n = max(2, int(abs(t1 - t0) / step) + 1)
    pts = []
    for i in range(n):
        t = math.radians(t0 + (t1 - t0) * i / (n - 1))
        x = a * scale * math.cos(t)
        y = b * scale * math.sin(t) * (1 - fat * math.cos(t))
        r = math.radians(rot)
        x, y = x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r)
        pts.append(N(cx + x, cy + y))
    return pts


# --- the bowl, in pixels -------------------------------------------------------
RIM = (512, 438, 290, 108)        # the rim's outer edge: cx, cy, rx, ry
INNER = (512, 439, 275, 98)       # the rim's inner edge
BELLY = (512, 462, 266, 108)      # the outer wall's lower silhouette
FLOOR = (512, 442, 250, 68)       # where the inner wall meets the floor
# --- the egg ---------------------------------------------------------------------
EGG = (470, 438, 105, 78)         # cx, cy, half-length, half-height; rotated -18 deg

rim = polygon(ell_pts(*RIM, 0, 360), name="rim")
inner = polygon(ell_pts(*INNER, 0, 360), name="inner")
belly = polygon(ell_pts(*BELLY, 0, 360), name="belly")
floor = polygon(ell_pts(*FLOOR, 0, 360), name="floor")
bowl = union(rim, belly, name="bowl")                       # the whole silhouette
egg = polygon(egg_pts(*EGG, 0, 360), name="egg")

# The egg's shadow side: the outline from -40 to 170 degrees (0 is the raised right
# end, 90 the underside) closed by a terminator bowed toward the shade.
egg_shade = polygon(egg_pts(*EGG, -40, 170) + egg_pts(*EGG, 170, -40, scale=0.30),
                    name="egg_shade")                       # back along a small inner egg
egg_lit = polygon(egg_pts(*EGG, 165, 325) + [N(EGG[0], EGG[1])],
                  name="egg_lit")                           # the lit sector, closed at the centre

# The bowl's interior shadow: the near inner wall as a crescent between the inner edge
# and the floor line, joined to the egg's cast shadow lying on the floor to its right.
near_cres = polygon(ell_pts(*INNER, 12, 168) + ell_pts(*FLOOR, 168, 12), name="near_cres")
CAST = (560, 505, 110, 28, -5)    # cx, cy, rx, ry, rot: a flat shadow under and right of the egg
cast_body = polygon(ell_pts(*CAST[:4], 0, 360, rot=CAST[4]), name="cast_body")
bowl_shadow = union(near_cres, cast_body, name="bowl_shadow")
cast_core = polygon(ell_pts(500, 512, 55, 14, 0, 360, rot=-8), name="cast_core")
# The far inner wall, lit: between the inner edge and the floor line, far half.
bowl_lit = polygon(ell_pts(*INNER, 190, 350) + ell_pts(*FLOOR, 350, 190), name="bowl_lit")

# The table: a far plane above the bowl and a near plane below it, and the bowl's own
# shadow thrown to the lower right.
table_far = polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 0.40), (0.0, 0.40)], name="table_far")
table_near = polygon([(0.0, 0.78), (1.0, 0.78), (1.0, 1.0), (0.0, 1.0)], name="table_near")
cast_table = polygon(ell_pts(530, 470, 345, 160, -15, 100) + ell_pts(*BELLY, 100, 40)
                     + ell_pts(*RIM, 40, -15), name="cast_table")


def silhouette_pt(theta_deg, grow=0.0):
    """The bowl's outer silhouette at an angle about (512, 450), grown outward by px."""
    best = None
    for (cx, cy, rx, ry) in (RIM, BELLY):
        t = math.radians(theta_deg)
        x, y = cx + (rx + grow) * math.cos(t), cy + (ry + grow) * math.sin(t)
        d = (x - 512) ** 2 + (y - 450) ** 2
        if best is None or d > best[0]:
            best = (d, x, y)
    return best[1], best[2]


def silhouette(t0, t1, grow=0.0, step=5.0):
    n = max(2, int(abs(t1 - t0) / step) + 1)
    return [N(*silhouette_pt(t0 + (t1 - t0) * i / (n - 1), grow)) for i in range(n)]


def in_bowl(px, py, grow):
    for (cx, cy, rx, ry) in (RIM, BELLY):
        if ((px - cx) / (rx + grow)) ** 2 + ((py - cy) / (ry + grow)) ** 2 <= 1.0:
            return True
    return False


def in_egg(px, py, grow):
    cx, cy, a, b = EGG
    k = 1.0 + grow / b
    r = math.radians(18.0)
    x, y = px - cx, py - cy
    x, y = x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r)
    ct = x / (a * k)
    if abs(ct) > 1.0:
        return False
    t = math.acos(ct)
    yy = b * k * math.sin(t) * (1 - 0.18 * ct)
    return abs(y) <= abs(yy)


def cut(p0, p1, pressure, inside, margin, least=36.0):
    """Cut a straight row (pixels) into runs stopping `margin` px short of `inside`.

    `pressure` is (a, b) along the whole row; each run gets the slice of it, so the
    gradient is continuous across the thing standing in the row.
    """
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    n = int(L / 2) + 1
    runs, cur = [], []
    for i in range(n + 1):
        u = i / n
        x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        if inside(x, y, margin):
            if cur:
                runs.append(cur)
                cur = []
        else:
            cur.append((u, x, y))
    if cur:
        runs.append(cur)
    out = []
    for r in runs:
        ua, xa, ya = r[0]
        ub, xb, yb = r[-1]
        if math.hypot(xb - xa, yb - ya) < least:
            continue
        pa = pressure[0] + (pressure[1] - pressure[0]) * ua
        pb = pressure[0] + (pressure[1] - pressure[0]) * ub
        out.append(([N(xa, ya), N(xb, yb)], [round(pa, 3), round(pb, 3)]))
    return out


# --- the plan ----------------------------------------------------------------------
s.plan(
    why="a white egg in a white bowl is the light drawn as paper, and everything else "
        "is drawn to make that paper read as light",
    values={table_far: 0.68, table_near: 0.55, cast_table: 0.34,
            egg_lit: 0.93, bowl_lit: 0.90, egg_shade: 0.45, bowl_shadow: 0.45,
            cast_core: 0.26},
    lightest=egg_lit,
    subject_share=0.45,
)


def ell_px(cx, cy, rx, ry, t0, t1, step=5.0, rot=0.0):
    """As ell_pts, but the points stay in pixels, for cutting before conversion."""
    return [(x * W, y * H) for x, y in ell_pts(cx, cy, rx, ry, t0, t1, step, rot)]


def egg_px(cx, cy, a, b, t0, t1, scale=1.0, step=5.0, rot=-18.0, fat=0.18):
    return [(x * W, y * H) for x, y in egg_pts(cx, cy, a, b, t0, t1, scale, step, rot, fat)]


def cut_arc(pts_px, pressure, inside, margin, least=3):
    """Cut an arc of pixel points into runs clear of `inside` by `margin` px.

    Returns (points normalised, pressure list) per run, the list sliced from the
    arc's own so the gradient is continuous across the thing standing in it.
    """
    runs, cur = [], []
    for i, (x, y) in enumerate(pts_px):
        if inside(x, y, margin):
            if cur:
                runs.append(cur)
                cur = []
        else:
            cur.append((i, x, y))
    if cur:
        runs.append(cur)
    n = len(pts_px) - 1
    k = len(pressure) - 1

    def at(u):
        f = u * k
        j = min(int(f), k - 1)
        return round(pressure[j] + (pressure[j + 1] - pressure[j]) * (f - j), 3)

    out = []
    for r in runs:
        if len(r) < least:
            continue
        ua, ub = r[0][0] / n, r[-1][0] / n
        pl = [at(ua + (ub - ua) * q / 4) for q in range(5)]
        out.append(([N(x, y) for _, x, y in r], pl))
    return out
