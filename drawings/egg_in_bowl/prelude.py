"""Run before every pass, in the same scope: helpers, shapes, and the plan.

A hen's egg in a shallow white bowl on a wooden table, lit from a window to the
upper left, out of frame. 1024x768, cartridge, white paper, graphite.
"""
import math

W, H = 1024, 768
ASPECT = W / H


def arc(c, rx, ry, t0, t1, n=24):
    """Points along an ellipse from angle t0 to t1 (degrees, clockwise from the
    horizontal, y down), both included."""
    cx, cy = c
    pts = []
    for i in range(n + 1):
        t = math.radians(t0 + (t1 - t0) * i / n)
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    return pts


def push_out(shape, p, c, step=1.03):
    """Move p radially away from c until it is outside the shape."""
    x, y = p
    cx, cy = c
    for _ in range(60):
        if not shape.contains(x, y):
            break
        x, y = cx + (x - cx) * step, cy + (y - cy) * step
    return (x, y)


# --- the arrangement -------------------------------------------------------

# The table's back edge, almost level, a touch higher on the left.
TABLE_Y_L, TABLE_Y_R = 0.335, 0.325
wall = polygon([(0.0, 0.0), (1.0, 0.0), (1.0, TABLE_Y_R), (0.0, TABLE_Y_L)], name="wall")
table = polygon([(0.0, TABLE_Y_L), (1.0, TABLE_Y_R), (1.0, 1.0), (0.0, 1.0)], name="table")

# The bowl: the rim's outer ellipse, the inner lip, and the belly below the rim.
RIM_C, RIM_RX, RIM_RY = (0.52, 0.60), 0.30, 0.12
INNER_C, INNER_RX, INNER_RY = (0.52, 0.607), 0.282, 0.102
BELLY_C, BELLY_RX, BELLY_RY = (0.52, 0.645), 0.29, 0.155
rim = ellipse(RIM_C, RIM_RX, RIM_RY, name="rim")
inner = ellipse(INNER_C, INNER_RX, INNER_RY, name="inner")
belly = ellipse(BELLY_C, BELLY_RX, BELLY_RY, name="belly")
bowl = union(rim, belly, name="bowl")
# The exterior wall seen below the rim: the belly's lower arc, back along the rim's.
bowl_wall = polygon(arc(BELLY_C, BELLY_RX, BELLY_RY, 2, 178, 30)
                    + arc(RIM_C, RIM_RX, RIM_RY, 178, 2, 30), name="bowl_wall")
# The right two thirds of that wall, which turns away from the light.
bowl_wall_shade = polygon(arc(BELLY_C, BELLY_RX, BELLY_RY, 2, 110, 20)
                          + arc(RIM_C, RIM_RX, RIM_RY, 110, 2, 20), name="bowl_wall_shade")

# The egg, lying a little left of the bowl's centre, its long axis tilted up to the
# right, the narrow end to the right. An egg curve, not an ellipse.
EGG_C, EGG_RX, EGG_RY, EGG_ROT, EGG_TAPER = (0.47, 0.607), 0.100, 0.082, -14, 0.16


def egg_pt(t):
    """A point on the egg's outline at parameter t (degrees), rotation included.
    t=0 is the narrow end (right), 90 the bottom, 180 the broad end, 270 the top."""
    a = math.radians(t)
    r = math.radians(EGG_ROT)
    x = EGG_RX * math.cos(a)
    y = EGG_RY * math.sin(a) * (1.0 - EGG_TAPER * math.cos(a))
    # rotate in pixel space so the tilt is what it looks like
    px, py = x * W, y * H
    qx, qy = px * math.cos(r) - py * math.sin(r), px * math.sin(r) + py * math.cos(r)
    return (EGG_C[0] + qx / W, EGG_C[1] + qy / H)


egg = polygon([egg_pt(t) for t in range(0, 360, 6)], name="egg")


# The egg's shadow side: the lower-right arc of the outline, and a terminator
# bowed toward the shadow side, so the shade is a little under half the egg.
def egg_shade_poly(bow=0.30, t_from=-70, t_to=126):
    outer = [egg_pt(t) for t in range(t_from, t_to + 1, 8)]
    a, b = egg_pt(t_to), egg_pt(t_from)
    inner_pts = []
    for i in range(1, 16):
        u = i / 16
        x = a[0] + (b[0] - a[0]) * u
        y = a[1] + (b[1] - a[1]) * u
        k = bow * math.sin(math.pi * u)
        # bow toward the lower right (the shadow side) in canvas units
        x += k * EGG_RX * 0.7071
        y += k * EGG_RY * 0.7071
        inner_pts.append((x, y))
    return polygon(outer + inner_pts, name="egg_shade")


egg_shade = egg_shade_poly()

# The bowl's interior shadow: a crescent along the far inner wall, thin on the
# left where the light comes in, thickest on the upper right, cut round the egg.
# ``shrink`` pulls its outer arc off the lip by that much in y (3/4 of it in x), so
# a side stroke's half-width does not cover the lip.
def crescent_poly(shrink=0.0):
    t0, t1 = 200, 372
    outer = arc(INNER_C, INNER_RX - shrink * 0.75, INNER_RY - shrink, t0, t1, 30)
    inner_pts = []
    for i in range(30, -1, -1):
        t = t0 + (t1 - t0) * i / 30
        u = (t - t0) / (t1 - t0)
        d = 0.70 * math.sin(math.pi * u) ** 0.9 * (0.55 + 0.45 * u)
        k = 1.0 - d
        a = math.radians(t)
        p = (INNER_C[0] + INNER_RX * k * math.cos(a), INNER_C[1] + INNER_RY * k * math.sin(a))
        inner_pts.append(push_out(egg, p, EGG_C))
    return polygon(outer + inner_pts, name="bowl_shadow")


bowl_shadow = crescent_poly()

# The egg's cast shadow on the bowl's floor, to the lower right of it.
egg_cast = ellipse((0.548, 0.668), 0.085, 0.030, rotate=-8, name="egg_cast")

# The bowl's cast shadow on the table: from under the belly out to the lower right.
bowl_cast = polygon(arc(BELLY_C, BELLY_RX, BELLY_RY, 172, 8, 30)
                    + arc((0.60, 0.725), 0.31, 0.105, 8, 172, 30), name="bowl_cast")

# The lit floor of the bowl, lower left, around the egg: where the paper shows.
def floor_poly(shrink=0.0):
    return polygon(arc(INNER_C, INNER_RX - shrink * 0.75, INNER_RY - shrink, 20, 200, 30)
                   + [push_out(egg, p, EGG_C) for p in reversed(
                       arc((0.50, 0.60), 0.20, 0.05, 20, 200, 20))], name="floor_lit")


floor_lit = floor_poly()


def egg_arc(k, t0, t1, step=5):
    """The egg's outline scaled by k about its centre, from t0 to t1: a cross-contour."""
    pts = []
    for t in range(t0, t1 + 1, step):
        x, y = egg_pt(t)
        pts.append((EGG_C[0] + (x - EGG_C[0]) * k, EGG_C[1] + (y - EGG_C[1]) * k))
    return pts


def bowl_outline_arc(t0, t1, dx=0.0, dy=0.0, n=30):
    """The bowl's silhouette grown by (dx, dy): the rim's arc over the top half
    (180..360), the belly's over the bottom (0..180). t0..t1 within one half."""
    if t0 >= 180 or t1 >= 180:
        return arc(RIM_C, RIM_RX + dx, RIM_RY + dy, t0, t1, n)
    return arc(BELLY_C, BELLY_RX + dx, BELLY_RY + dy, t0, t1, n)


def _ray_hit(p0, d, c, rx, ry):
    """How far along the ray p0 + t d the ellipse (c, rx, ry) is crossed outward."""
    ox, oy = (p0[0] - c[0]) / rx, (p0[1] - c[1]) / ry
    dx, dy = d[0] / rx, d[1] / ry
    a, b, cc = dx * dx + dy * dy, 2 * (ox * dx + oy * dy), ox * ox + oy * oy - 1.0
    disc = b * b - 4 * a * cc
    if disc < 0:
        return 0.0
    return (-b + math.sqrt(disc)) / (2 * a)


def silhouette(dx=0.0, dy=0.0, start_deg=60, n=120):
    """The bowl's whole silhouette -- the rim where it is outside, the belly where it
    is -- grown by (dx, dy), as one closed run of points starting at start_deg
    (screen angle from the bowl's middle, clockwise, 90 straight down)."""
    p0 = (0.52, 0.635)
    pts = []
    for i in range(n + 1):
        th = math.radians(start_deg + 360.0 * i / n)
        d = (math.cos(th), math.sin(th))
        t = max(_ray_hit(p0, d, RIM_C, RIM_RX + dx, RIM_RY + dy),
                _ray_hit(p0, d, BELLY_C, BELLY_RX + dx, BELLY_RY + dy))
        pts.append((p0[0] + t * d[0], p0[1] + t * d[1]))
    return pts


def cut_runs(points, blocked, shape=None, centre=None, min_pts=3):
    """Split a run of points into the runs where ``blocked(x, y)`` is false. Where a
    run meets a blocked stretch, its end is pushed out of ``shape`` from ``centre`` so
    the stroke butts against the outline rather than stopping a step short."""
    runs, run = [], []
    for i, (x, y) in enumerate(points):
        if not blocked(x, y):
            run.append((x, y))
        else:
            if run:
                if shape is not None:
                    run.append(push_out(shape, (x, y), centre, step=1.02))
                runs.append(run)
                run = []
            elif shape is not None and i + 1 < len(points) and not blocked(*points[i + 1]):
                run.append(push_out(shape, (x, y), centre, step=1.02))
    if run:
        runs.append(run)
    return [r for r in runs if len(r) >= min_pts]


def crescent_arc(u, t0=200, t1=372, n=48, shrink=0.007):
    """An arc inside the bowl's shadow crescent: u=0 on the lip, u=1 on its inner
    boundary; the same d(t) the polygon is built from."""
    pts = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        v = (t - t0) / (t1 - t0)
        d = 0.70 * math.sin(math.pi * v) ** 0.9 * (0.55 + 0.45 * v)
        k = 1.0 - u * d
        a = math.radians(t)
        pts.append((INNER_C[0] + (INNER_RX - shrink * 0.75) * k * math.cos(a),
                    INNER_C[1] + (INNER_RY - shrink) * k * math.sin(a)))
    return pts


def lay_runs(runs, grade, pressure_fn, width, tip="side", note=""):
    """line() each run with a pressure list from pressure_fn(x, y) at its points."""
    recs = []
    for r in runs:
        pr = [float(pressure_fn(x, y)) for x, y in r]
        recs.append(s.line(r, grade=grade, pressure=pr, tip=tip, width=width, smooth=False,
                           note=note))
    return recs


def wall_arc(f, t0, t1, n=24):
    """An arc on the bowl's exterior wall, f of the way from the rim (0) to the belly (1)."""
    c = (RIM_C[0] + (BELLY_C[0] - RIM_C[0]) * f, RIM_C[1] + (BELLY_C[1] - RIM_C[1]) * f)
    rx = RIM_RX + (BELLY_RX - RIM_RX) * f
    ry = RIM_RY + (BELLY_RY - RIM_RY) * f
    return arc(c, rx, ry, t0, t1, n)

# The bowl grown by half a wide side stroke, so the ground's broad rows stop short of
# the rim and the band beside the bowl is laid by hand, following its silhouette.
GROW_X, GROW_Y = 0.036, 0.048
rim_grown = ellipse(RIM_C, RIM_RX + GROW_X, RIM_RY + GROW_Y, name="rim_grown")
belly_grown = ellipse(BELLY_C, BELLY_RX + GROW_X, BELLY_RY + GROW_Y, name="belly_grown")


def in_bowl_grown(x, y):
    return rim_grown.contains(x, y) or belly_grown.contains(x, y)


def rows(inside, angle_deg, spacing, y0=0.0, y1=1.0, x0=-0.05, x1=1.05, step_px=3,
         min_len=0.02, phase=0.0):
    """Segments of parallel lines across the canvas, kept where ``inside(x, y)``.

    ``angle_deg`` is the screen angle (pixels), clockwise from horizontal; ``spacing``
    a fraction of the long side, measured across the lines. Each row alternates its
    direction, as a hand comes back across the paper. Returns [(points, flipped)]."""
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)          # along the line, in pixels
    nx, ny = -dy, dx                           # across it
    sp = spacing * W
    out = []
    # rows are offsets along the normal, covering the canvas
    corners = [(0, 0), (W, 0), (0, H), (W, H)]
    offs = [cx * nx + cy * ny for cx, cy in corners]
    o, k = min(offs) + phase * sp, 0
    while o <= max(offs):
        # a point on the row, then walk along it
        px0, py0 = o * nx, o * ny
        # parametric extent along the line that stays inside the canvas box
        t_lo, t_hi = -2 * max(W, H), 2 * max(W, H)
        pts = []
        t = t_lo
        run = []
        while t <= t_hi:
            x, y = (px0 + t * dx) / W, (py0 + t * dy) / H
            ok = (x0 <= x <= x1 and y0 <= y <= y1 and 0 <= x <= 1.0 and 0 <= y <= 1.0
                  and inside(x, y))
            if ok:
                run.append((x, y))
            elif run:
                pts.append(run)
                run = []
            t += step_px
        if run:
            pts.append(run)
        for r in pts:
            (ax, ay), (bx, by) = r[0], r[-1]
            if math.hypot((bx - ax) * W, (by - ay) * H) >= min_len * W:
                seg = [(ax, ay), (bx, by)]
                out.append((seg if k % 2 == 0 else seg[::-1], k % 2 == 1))
        o += sp
        k += 1
    return out


def lay_rows(segs, grade, pressure, width, tip="side", note=""):
    """line() each row; a pressure list is read in canvas order on flipped rows."""
    recs = []
    for seg, flipped in segs:
        pr = pressure
        if flipped and isinstance(pressure, (list, tuple)):
            pr = list(pressure)[::-1]
        recs.append(s.line(seg, grade=grade, pressure=pr, tip=tip, width=width,
                           smooth=False, note=note))
    return recs


def read(place, label):
    """Print what a place reads in the values view: its median, as compare() reads it."""
    v = s.palette.value_of(s.sample(place, rendered=True))
    print(f"  {label}: reads {v:.3f} (mean)")
    return v


# --- the plan --------------------------------------------------------------
s.plan(
    why="the egg is the one white thing that is also round: its light is the paper, "
        "and everything else is drawn to make that white read as light",
    values={
        wall: 0.70,
        table: 0.52,
        bowl_shadow: 0.36,
        egg_shade: 0.42,
        egg_cast: 0.24,
        bowl_cast: 0.36,
        bowl_wall_shade: 0.66,
    },
    lightest=egg,
    subject_share=0.45,
    # the two planes are drawn with their rows along them: the wall level, the table
    # along its grain. Declared so the check counts what crosses them (the bowl, the
    # egg's cross-contours) rather than warning about the bars.
    bands="subject",
)
