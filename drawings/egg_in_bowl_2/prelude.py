"""Run before every pass, in the same scope: the shapes, the helpers and the plan.

Everything is drawn in pixels of the 1024x768 sheet and handed to the engine as
0..1 units, because one unit number is two distances on a sheet whose sides differ.

The picture: a hen's egg lying in a shallow white bowl on a plain wooden table, the
window to the upper left and a little in front, out of frame. Four masses: the light
(the egg's lit side, the bowl's lit rim and left wall, the near floor of the bowl: paper
never touched, or nearly); the egg's shadow side; the bowl's interior shadow round the
far and right inner wall, with the egg's cast shadow lying in it on the near floor to
the right; and the table, a mid tone lighter toward the window.
"""
import math

from easel import Region, polygon

W, H = 1024.0, 768.0


def U(x, y):
    """A pixel point as a unit point."""
    return (x / W, y / H)


def ell(cx, cy, rx, ry, t0, t1, step=6, rot=0.0):
    """Points of an ellipse arc in pixels, t in degrees (0 at +x, 90 straight down)."""
    c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = []
    n = max(2, int(round(abs(t1 - t0) / step)) + 1)
    for i in range(n):
        t = math.radians(t0 + (t1 - t0) * i / (n - 1))
        u, v = rx * math.cos(t), ry * math.sin(t)
        pts.append(U(cx + u * c - v * s_, cy + u * s_ + v * c))
    return pts


# --- the bowl --------------------------------------------------------------------
BOWL_CX, BOWL_CY = 512.0, 430.0
RIM_RX, RIM_RY = 318.0, 88.0          # the rim, seen from a little above
LOW_RX, LOW_RY = 318.0, 150.0         # the outer wall's lower outline
LIP_RX, LIP_RY = 311.0, 81.0          # the inner edge of the rim: the rim is 7 px of paper
INNER_CX, INNER_CY, INNER_RX, INNER_RY = 500.0, 450.0, 282.0, 66.0   # where the inner
                                      # wall meets the floor


def rim(t0=0, t1=360, step=5, k=1.0):
    return ell(BOWL_CX, BOWL_CY, RIM_RX * k, RIM_RY * k, t0, t1, step)


def lower(t0=0, t1=180, step=5, ry=LOW_RY):
    return ell(BOWL_CX, BOWL_CY, LOW_RX, ry, t0, t1, step)


def lip(t0=180, t1=360, step=5):
    return ell(BOWL_CX, BOWL_CY, LIP_RX, LIP_RY, t0, t1, step)


def inner(t0=180, t1=360, step=5):
    return ell(INNER_CX, INNER_CY, INNER_RX, INNER_RY, t0, t1, step)


def crescent_arc(k, t0=180, t1=360, step=5):
    """An arc between the lip (k=0) and the inner ellipse (k=1), the far inner wall."""
    cx = BOWL_CX + (INNER_CX - BOWL_CX) * k
    cy = BOWL_CY + (INNER_CY - BOWL_CY) * k
    return ell(cx, cy, LIP_RX + (INNER_RX - LIP_RX) * k, LIP_RY + (INNER_RY - LIP_RY) * k,
               t0, t1, step)


# one closed run round both shapes, so the silhouette has no notch where they meet
bowl = polygon(rim(180, 360) + lower(0, 180)[1:-1], name="bowl")
rim_shape = polygon(rim(0, 360), name="rim")
lip_shape = polygon(lip(0, 360), name="lip")
inner_shape = polygon(ell(INNER_CX, INNER_CY, INNER_RX, INNER_RY, 0, 360), name="inner")
# the outer wall below the rim: right half in shade, left half lit
bowl_shade = polygon(lower(0, 90) + rim(90, 0)[1:], name="bowl_shade")
bowl_lit = polygon(lower(90, 180) + rim(180, 90)[1:], name="bowl_lit")
# the far inner wall's shadow, read on its right portion (the left is behind the egg
# and lighter with reflected light)
interior_shade = polygon(lip(-75, 0) + crescent_arc(1.0, 0, -75)[1:], name="interior_shade")
# the near floor, lit, to the left of the egg
floor_lit = polygon([U(280, 445), U(325, 432), U(335, 488), U(285, 474)], name="floor_lit")

# --- the egg -----------------------------------------------------------------------
EGG_CX, EGG_CY = 470.0, 408.0
EGG_A, EGG_B = 120.0, 78.0            # half length, half width
EGG_ROT = -12.0                       # the narrow end up and to the right
EGG_E = 0.22                          # how much narrower the narrow end is
# the light: from the upper left, and a little in front (elevation 20 degrees)
LIGHT = (-0.6, -0.8)
LIGHT_EL = 20.0


def egg_local(t, k=1.0):
    """The egg's outline in its own frame, t in degrees, 0 at the narrow end."""
    tr = math.radians(t)
    u = EGG_A * k * math.cos(tr)
    v = EGG_B * k * math.sin(tr) * (1 - EGG_E * math.cos(tr))
    return u, v


def egg_pt(t, k=1.0):
    u, v = egg_local(t, k)
    c, s_ = math.cos(math.radians(EGG_ROT)), math.sin(math.radians(EGG_ROT))
    return U(EGG_CX + u * c - v * s_, EGG_CY + u * s_ + v * c)


def egg_arc(t0, t1, k=1.0, step=5):
    n = max(2, int(round(abs(t1 - t0) / step)) + 1)
    return [egg_pt(t0 + (t1 - t0) * i / (n - 1), k) for i in range(n)]


def shade_depth(t):
    """Along the egg's outline direction t: how far in from the outline the shade
    reaches (as a share of the radius, 0..1), from a sphere lit at LIGHT_EL. 0 means
    the direction is lit."""
    # the direction of the point in picture space, normalised by the egg's radii
    u, v = egg_local(t)
    c, s_ = math.cos(math.radians(EGG_ROT)), math.sin(math.radians(EGG_ROT))
    dx, dy = (u * c - v * s_) / EGG_A, (u * s_ + v * c) / EGG_A
    norm = math.hypot(dx, dy) or 1.0
    dx, dy = dx / norm, dy / norm
    d = -(dx * LIGHT[0] + dy * LIGHT[1])        # 1 facing straight away from the light
    if d <= 0:
        return 0.0
    tan = math.tan(math.radians(LIGHT_EL))
    # r cos(delta) = tan(el) sqrt(1 - r^2), cos(delta) = d
    r = tan / math.sqrt(d * d + tan * tan)
    return max(0.0, 1.0 - r)


# the egg's masses: the lit side toward the light, the shade beyond the terminator
_lit_ts = [t for t in range(0, 360, 4) if shade_depth(t) == 0.0]
_shade_ts = [t for t in range(0, 360, 4) if shade_depth(t) > 0.18]
egg = polygon(egg_arc(0, 360), name="egg")


def _run(ts):
    """Order a set of outline angles as one contiguous run round the outline."""
    ts = sorted(ts)
    # find the gap and start after it
    gaps = [(ts[(i + 1) % len(ts)] - ts[i]) % 360 for i in range(len(ts))]
    i0 = (gaps.index(max(gaps)) + 1) % len(ts)
    return ts[i0:] + ts[:i0]


egg_light = polygon([egg_pt(t, 0.97) for t in _run(_lit_ts)], name="egg_light")
egg_shade = polygon([egg_pt(t) for t in _run(_shade_ts)]
                    + [egg_pt(t, 1.0 - shade_depth(t)) for t in reversed(_run(_shade_ts))],
                    name="egg_shade")
terminator_pts = [egg_pt(t, 1.0 - shade_depth(t)) for t in _run(_shade_ts)]

# --- the cast shadow, on the near floor to the lower right of the egg ---------------
# from under the egg's foot (its bottom is at about (470, 486)) to the right inner wall
CAST_CX, CAST_CY, CAST_RX, CAST_RY, CAST_ROT = 640.0, 472.0, 172.0, 31.0, 3.0
EGG_FOOT = (470.0, 486.0)


def cast_arc(k=1.0, t0=0, t1=360, step=6):
    return ell(CAST_CX, CAST_CY, CAST_RX * k, CAST_RY * k, t0, t1, step, CAST_ROT)


cast = polygon(cast_arc(1.0), name="cast")

# --- the table ---------------------------------------------------------------------
table_far = Region(0.0, 0.0, 1.0, 0.39)
table_near = Region(0.0, 0.78, 1.0, 1.0)
# the whole sheet with the bowl cut out of it, as one polygon with a slit
_bowl_run = rim(180, 360) + lower(0, 180)
_yl = _bowl_run[0][1]
_outside = [(0.0, _yl - 0.0003), (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0),
            (0.0, _yl + 0.0003)]
table = polygon(_outside + [_bowl_run[0]] + _bowl_run[1:] + [_bowl_run[0]], name="table")


# --- helpers for laying ------------------------------------------------------------
def densify(pts, step=0.008):
    """More points along a polyline, so a cut lands within a few pixels."""
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(1, n + 1):
            out.append((x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n))
    return out


def cut(pts, avoid, margin=0.0, step=0.008):
    """The runs of a polyline that lie outside `avoid` grown by `margin`: a row cut
    round what stands on the plane. Returns a list of (run, u0, u1): the points, and
    where the run starts and ends as a share of the whole line's length."""
    shapes = avoid if isinstance(avoid, (list, tuple)) else [avoid]
    grown = [sh.inset(-margin) if margin else sh for sh in shapes]
    d = densify(pts, step)
    total = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(d, d[1:])) or 1.0
    runs, cur, acc, u_start = [], [], 0.0, 0.0
    prev = d[0]
    for p in d:
        acc += math.hypot(p[0] - prev[0], p[1] - prev[1])
        prev = p
        inside = any(g.contains(p[0], p[1]) for g in grown)
        if inside:
            if len(cur) >= 2:
                runs.append((cur, u_start, acc / total))
            cur = []
        else:
            if not cur:
                u_start = acc / total
            cur.append(p)
    if len(cur) >= 2:
        runs.append((cur, u_start, 1.0))
    return runs


def ramp(p0, p1, u0, u1, n):
    """A pressure list for a run from u0 to u1 of a row whose pressure runs p0 to p1."""
    return [p0 + (p1 - p0) * (u0 + (u1 - u0) * i / max(1, n - 1)) for i in range(n)]


def lay_rows(rows, grade, pressure, width, note="", avoid=None, margin=0.0, flip_odd=True,
             min_len=0.03):
    """Rows by hand: each a line of `tip='side'`, cut round `avoid`, alternating
    direction, the pressure list turned round with the row. Returns the strokes laid."""
    n = 0
    p0, p1 = (pressure if isinstance(pressure, (list, tuple)) else (pressure, pressure))
    for k, row in enumerate(rows):
        runs = cut(row, avoid, margin) if avoid is not None else [(densify(row), 0.0, 1.0)]
        for pts, u0, u1 in runs:
            if math.hypot(pts[-1][0] - pts[0][0], pts[-1][1] - pts[0][1]) < min_len:
                continue
            pr = ramp(p0, p1, u0, u1, len(pts))
            if flip_odd and k % 2 == 1:
                pts, pr = pts[::-1], pr[::-1]
            s.line(pts, grade, pressure=pr, tip="side", width=width, smooth=False, note=note)
            n += 1
    return n


def bell(n, lo, hi, peak=0.5, spread=0.5):
    """A pressure list that rises from lo to hi at `peak` (0..1 along) and falls back."""
    out = []
    for i in range(n):
        u = i / max(1, n - 1)
        w = math.exp(-((u - peak) / spread) ** 2 * 2.0)
        out.append(lo + (hi - lo) * w)
    return out


# --- the plan ----------------------------------------------------------------------
s.plan(
    why="two whites, an egg and a bowl, are one light because everything round them is drawn a step darker",
    values={
        table_far: 0.66, table_near: 0.56,
        bowl_lit: 0.92, bowl_shade: 0.74,
        floor_lit: 0.90, interior_shade: 0.44,
        egg_light: 0.94, egg_shade: 0.47,
        cast: 0.33,
    },
    lightest=egg_light,
    subject_share=0.55,
)
