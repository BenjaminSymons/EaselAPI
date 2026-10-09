"""Run before every pass, in the same scope: the shapes, the helpers, and the plan.

The subject: a hen's egg in a shallow white bowl on a wooden table, lit from a window to
the upper left, out of frame. My decisions (reasoned, not measured):

- The window is upper left and a little *behind* the subject, so the bowl's interior
  shadow is a crescent along its far and right wall (the wall that faces the viewer and
  away from the window), and the near-left interior is lit through the open front. That
  is what lets the egg's shadow side (lower right) melt into the bowl's shadow behind it.
- The egg lies on its side, pointy end up toward the light, in the right-of-centre of the
  bowl. Its lit side is paper never touched. Its cast shadow falls to the lower right.
- The bowl's rim is paper. The bowl's outer wall faces the viewer: half-shadow, darker
  to the right. The bowl's cast shadow lies on the table to the lower right; its core
  under the bowl is the drawing's dark.
- The table is lighter far (near the window) and darker near.

Values are what the check should read by the median *after* the stumps.
"""
import math

W, H = 1024, 768


# ----------------------------------------------------------------------------- helpers
def ell_pts(c, rx, ry, t0, t1, step=6, rot=0.0, k=1.0, egg=0.0):
    """Points along an ellipse (or an egg, `egg` > 0 fattens the +x end) from angle t0
    to t1 in degrees, scaled by k about its centre, rotated `rot` degrees in *pixel*
    space so the rotation is true on a 4:3 sheet. Angles run clockwise on screen
    (y down): 0 is the right end, 90 the bottom, -90 the top, 180 the left end."""
    cx, cy = c
    n = max(2, int(round(abs(t1 - t0) / step)) + 1)
    out = []
    r = math.radians(rot)
    for i in range(n):
        t = math.radians(t0 + (t1 - t0) * i / (n - 1))
        x = rx * k * math.cos(t)
        y = ry * k * math.sin(t) * (1.0 + egg * math.cos(t))
        px, py = x * W, y * H
        if rot:
            px, py = px * math.cos(r) - py * math.sin(r), px * math.sin(r) + py * math.cos(r)
        out.append((cx + px / W, cy + py / H))
    return out


def bell(n, top, ends=0.0, power=1.0):
    """A pressure list of n values rising from `ends` to `top` in the middle and back."""
    if n < 2:
        return [top]
    return [ends + (top - ends) * (max(0.0, math.sin(math.pi * i / (n - 1))) ** power)
            for i in range(n)]


def ramp(n, a, b):
    """A pressure list of n values from a to b along the stroke."""
    if n < 2:
        return [b]
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def runs_outside(pts, shape, least=3):
    """Cut a run of points into the runs that lie outside `shape` (a thing standing in
    the passage); runs shorter than `least` points are dropped."""
    runs, cur = [], []
    for (x, y) in pts:
        if shape.contains(x, y):
            if len(cur) >= least:
                runs.append(cur)
            cur = []
        else:
            cur.append((x, y))
    if len(cur) >= least:
        runs.append(cur)
    return runs


def runs_inside(pts, shape, least=3):
    """The runs of a point list that lie inside `shape`."""
    runs, cur = [], []
    for (x, y) in pts:
        if shape.contains(x, y):
            cur.append((x, y))
        else:
            if len(cur) >= least:
                runs.append(cur)
            cur = []
    if len(cur) >= least:
        runs.append(cur)
    return runs


def diag_row(x0, y0, dx, dy, step=0.02):
    """A straight row from (x0, y0) to (x0 + dx, y0 + dy) as a list of points, so it can
    be cut round a shape."""
    n = max(2, int(round(math.hypot(dx * W, dy * H) / (step * W))) + 1)
    return [(x0 + dx * i / (n - 1), y0 + dy * i / (n - 1)) for i in range(n)]


def crescent(c, rx, ry, shift, step=4, name=""):
    """The part of an ellipse a copy of itself shifted by `shift` leaves uncovered: one
    closed run, the ellipse's own arc between the two crossings and the copy's arc back.
    `shift` points toward the covered side; the crescent lies opposite it."""
    sx, sy = shift[0] / rx, shift[1] / ry            # the shift in the ellipse's own units
    L = math.hypot(sx, sy)
    phi = math.atan2(sy, sx)
    d = math.acos(min(1.0, L / 2))
    a1, a2 = phi + d, phi - d + 2 * math.pi           # the crossings; a1 -> a2 passes phi+pi
    n = max(3, int(round(math.degrees(a2 - a1) / step)) + 1)
    first = [(c[0] + rx * math.cos(a1 + (a2 - a1) * i / (n - 1)),
              c[1] + ry * math.sin(a1 + (a2 - a1) * i / (n - 1))) for i in range(n)]
    c2 = (c[0] + shift[0], c[1] + shift[1])
    b2 = math.atan2(math.sin(a2) - sy, math.cos(a2) - sx)
    b1 = math.atan2(math.sin(a1) - sy, math.cos(a1) - sx)
    mid = phi + math.pi
    # go from b2 to b1 the way that passes mid (angles reduced modulo 2 pi)
    def ccw_span(x, y):
        return (y - x) % (2 * math.pi)
    if ccw_span(b2, mid) < ccw_span(b2, b1):
        e1, e2 = b2, b2 + ccw_span(b2, b1)
    else:
        e1, e2 = b2, b2 - ((b2 - b1) % (2 * math.pi))
    m = max(3, int(round(abs(math.degrees(e2 - e1)) / step)) + 1)
    second = [(c2[0] + rx * math.cos(e1 + (e2 - e1) * i / (m - 1)),
               c2[1] + ry * math.sin(e1 + (e2 - e1) * i / (m - 1))) for i in range(1, m - 1)]
    return polygon(first + second, name=name)


# ----------------------------------------------------------------------------- geometry
# The bowl: a shallow ellipse for the rim, an inner ellipse for the lip, an outer
# ellipse hanging below it for the outer wall.
BOWL_C = (0.50, 0.55)
RIM_RX, RIM_RY = 0.31, 0.14
INNER_C = (0.50, 0.554)
INNER_RX, INNER_RY = 0.29, 0.125
OUTER_C = (0.50, 0.57)
OUTER_RX, OUTER_RY = 0.31, 0.18

rim = polygon(ell_pts(BOWL_C, RIM_RX, RIM_RY, 0, 360, step=5), name="rim")
inner = polygon(ell_pts(INNER_C, INNER_RX, INNER_RY, 0, 360, step=5), name="inner")


def bowl_sil(grow_x=0.0, grow_y=0.0, name="bowl"):
    """The bowl's silhouette against the table: the rim's top half over the outer
    wall's bottom half, one closed run; grown by (grow_x, grow_y) for a margin."""
    top = ell_pts(BOWL_C, RIM_RX + grow_x, RIM_RY + grow_y, 180, 360, step=4)
    bottom = ell_pts(OUTER_C, OUTER_RX + grow_x, OUTER_RY + grow_y, 0, 180, step=4)
    return polygon(top + bottom, name=name)


bowl = bowl_sil()
HALF = 0.035                                         # half of a width=0.07 row, in x
bowl_margin = bowl_sil(HALF, HALF * W / H, name="bowl_margin")   # where rows stop

# The outer wall: the crescent between the rim's lower arc and the outer's lower arc.
wall = polygon(ell_pts(OUTER_C, OUTER_RX, OUTER_RY, 0, 180, step=4)
               + ell_pts(BOWL_C, RIM_RX, RIM_RY, 180, 0, step=4), name="wall")

# The egg: lying, fat end lower right, pointy end up toward the light.
EGG_C = (0.545, 0.556)
EGG_RX, EGG_RY = 100 / W, 70 / H
EGG_ROT, EGG_E = 10.0, 0.18


def egg_arc(k, t0, t1, step=6):
    return ell_pts(EGG_C, EGG_RX, EGG_RY, t0, t1, step=step, rot=EGG_ROT, k=k, egg=EGG_E)


egg = polygon(egg_arc(1.0, 0, 360, step=5), name="egg")
# ...grown by 14 px in x and 18 in y: a side stroke's end block overruns its last point
# by half a width, so a run cut here at width 0.02 stops short of the egg itself.
egg_grown = polygon(ell_pts(EGG_C, EGG_RX + 0.014, EGG_RY + 0.019, 0, 360, step=5,
                            rot=EGG_ROT, egg=EGG_E), name="egg_grown")

# The egg's lit side, the plan's light: the upper-left half of the egg, a place no
# line crosses. The shade side: the lower-right.
egg_lit = polygon(egg_arc(0.94, 150, 295, step=5) + egg_arc(0.52, 295, 150, step=5),
                  name="egg_lit")
egg_shade = polygon(egg_arc(1.0, -45, 140, step=5) + egg_arc(0.60, 140, -45, step=5),
                    name="egg_shade")

# The bowl's interior shadow: the crescent the inner ellipse leaves uncovered when a
# copy of it is shifted toward the lower left; it runs along the far and right wall.
SHIFT = (-0.04, 0.07)                                # toward the lit, lower-left side
int_shade = crescent(INNER_C, INNER_RX, INNER_RY, SHIFT, name="int_shade")
# The lit interior: the lower-left of the inner ellipse, left of the egg.
int_lit = polygon(ell_pts(INNER_C, INNER_RX, INNER_RY, 100, 250, step=4)
                  + [(0.40, 0.46), (0.40, 0.64)], name="int_lit")

# The egg's cast shadow on the bowl's floor, lower right of the egg.
CAST_C = (EGG_C[0] + 0.05, EGG_C[1] + 0.045)
CAST_RX, CAST_RY, CAST_ROT = 0.12, 0.044, 8
# ...and the egg grown by 4 px, for the cast shadow's arcs to stop at: the shadow must
# touch the egg, and what the stroke's half-width crosses there is the egg's own shade.
egg_tight = polygon(ell_pts(EGG_C, EGG_RX + 0.004, EGG_RY + 0.005, 0, 360, step=5,
                            rot=EGG_ROT, egg=EGG_E), name="egg_tight")
egg_cast = polygon(ell_pts(CAST_C, CAST_RX, CAST_RY, 0, 360, step=5, rot=CAST_ROT), name="egg_cast")
# ...and the part of it the egg does not hide, for the plan.
def egg_angle(p):
    """The egg's own angle, in degrees, of the outline point nearest p."""
    dx, dy = (p[0] - EGG_C[0]) * W, (p[1] - EGG_C[1]) * H
    r = math.radians(-EGG_ROT)
    dx, dy = dx * math.cos(r) - dy * math.sin(r), dx * math.sin(r) + dy * math.cos(r)
    return math.degrees(math.atan2(dy / (EGG_RY * H), dx / (EGG_RX * W)))


_ec_run = max(runs_outside(ell_pts(CAST_C, CAST_RX, CAST_RY, 0, 178, step=3, rot=CAST_ROT),
                           egg_tight), key=len)
# the shadow laid is the lower half of the ellipse, so the place closes along its major
# axis, from where the axis leaves the egg back to the right end
_axis = [ell_pts(CAST_C, CAST_RX * k, CAST_RY * k, 0, 0, rot=CAST_ROT)[0]
         for k in (1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4,
                   0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.0)]
_axis_entry = next((p for p in _axis if egg_tight.contains(*p)), _axis[-1])
egg_cast_seen = polygon(_ec_run
                        + egg_arc(1.03, egg_angle(_ec_run[-1]), egg_angle(_axis_entry), step=4)
                        + [_axis_entry], name="egg_cast_seen")

# The bowl's cast shadow on the table, lower right, and its core under the bowl.
BCAST_C = (0.74, 0.70)
BCAST_RX, BCAST_RY, BCAST_ROT = 0.19, 0.08, 18
bowl_cast = polygon(ell_pts(BCAST_C, BCAST_RX, BCAST_RY, 0, 360, step=5, rot=BCAST_ROT),
                    name="bowl_cast")


def outer_angle(p, grow_x=0.004, grow_y=0.005):
    """The angle, in degrees, of the point on the grown outer ellipse nearest p."""
    return math.degrees(math.atan2((p[1] - OUTER_C[1]) / (OUTER_RY + grow_y),
                                   (p[0] - OUTER_C[0]) / (OUTER_RX + grow_x)))


_bc_run = max(runs_outside(ell_pts(BCAST_C, BCAST_RX, BCAST_RY, -90, 270, step=3, rot=BCAST_ROT),
                           bowl_sil(0.004, 0.005)), key=len)
bowl_cast_seen = polygon(_bc_run + ell_pts(OUTER_C, OUTER_RX + 0.004, OUTER_RY + 0.005,
                                           outer_angle(_bc_run[-1]), outer_angle(_bc_run[0]),
                                           step=4),
                         name="bowl_cast_seen")
bowl_cast_core = polygon(ell_pts(OUTER_C, OUTER_RX + 0.004, OUTER_RY + 0.005, 10, 85, step=4)
                         + ell_pts(OUTER_C, OUTER_RX + 0.03, OUTER_RY + 0.045, 85, 10, step=4),
                         name="bowl_cast_core")

# The table, far and near.
table_far = polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 0.36), (0.0, 0.36)], name="table_far")
table_near = polygon([(0.0, 0.80), (1.0, 0.80), (1.0, 1.0), (0.0, 1.0)], name="table_near")
table_left = polygon([(0.0, 0.42), (0.15, 0.42), (0.15, 0.75), (0.0, 0.75)], name="table_left")

# ----------------------------------------------------------------------------- the plan
s.plan(
    why="a white egg in a white bowl is one light with two shapes in it, and the drawing is "
        "whether the second shape can be found inside the first without an outline",
    values={
        table_far: 0.70,
        table_near: 0.54,
        int_lit: 0.82,
        int_shade: 0.46,
        egg_lit: 0.95,
        egg_shade: 0.46,
        egg_cast_seen: 0.34,
        wall: 0.58,
        bowl_cast_seen: 0.30,
        bowl_cast_core: 0.18,
    },
    lightest=egg_lit,
    subject_share=0.25,
)
