"""Run before every pass, in the same scope: the shapes, the helpers and the plan.

Why this subject: one white thing holding one pale thing on a darker ground, so the
whole drawing is the paper left alone where the light falls and tone laid everywhere
else to make that paper read as light.

The arrangement. A shallow white bowl, seen from a little above and in front, centred
on the sheet and a little low; the egg sits in it left of centre, its crown rising just
above the far rim. The window is upper left and out of frame: the far rim and the
egg's upper-left are paper; the egg's lower-right turns into the bowl's interior
shadow behind it (the lost edge); the egg's cast shadow lies on the bowl's floor at its
lower right, and is the darkest thing in the picture. The bowl's rim against the table
is the hard edge. The table is the whole ground, lighter toward the window.

Masses and the values they are to read, by median after their stump:
  table_far 0.68, table_near 0.63 (one mass, lighter at the top left)
  bowl_wall 0.74 (lit left, turning at right), rim_light 0.94 (paper), floor_lit 0.73
  egg_light 0.83 (floor), with a highlight of paper never touched
  egg_shade 0.46 and bowl_shadow 0.44 (the lost edge pair), cast 0.20 (the dark)
  bowl_cast 0.46 (the bowl's shadow on the table)
"""
import math
from easel import polygon

W, H = 1024, 768
PX, PY = 1.0 / W, 1.0 / H          # one pixel, in sheet units, in each axis


def arc(c, rx, ry, t0, t1, n=24):
    """Points along an ellipse arc, angles in degrees, screen sense (y down)."""
    return [(c[0] + rx * math.cos(math.radians(t0 + (t1 - t0) * i / n)),
             c[1] + ry * math.sin(math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]


# --- the bowl ------------------------------------------------------------------------
BC = (0.50, 0.570)                 # the rim's centre
RIM = (0.300, 0.125)               # the outer rim's radii
IC, IR = (0.50, 0.580), (0.272, 0.100)   # the interior ellipse: far rim 27 px, near rim 12 px
BODY = (0.300, 0.230)              # the outer wall: this ellipse's lower half, bottom at 0.80


def rim(t0, t1, dx=0.0, dy=0.0, n=24):
    return arc(BC, RIM[0] - dx, RIM[1] - dy, t0, t1, n)


def body(t0, t1, dx=0.0, dy=0.0, n=24):
    return arc(BC, BODY[0] - dx, BODY[1] - dy, t0, t1, n)


def interior(t0, t1, dx=0.0, dy=0.0, n=24):
    return arc(IC, IR[0] - dx, IR[1] - dy, t0, t1, n)


# --- the egg -------------------------------------------------------------------------
EC = (0.440, 0.530)                # centre
ER = (0.120, 0.112)                # radii (246 x 177 px); the left end is the blunt one
EK = 0.15                          # how much blunter the left end is than the right


def egg_pt(t, dx=0.0, dy=0.0):
    """A point of the egg's outline at angle t, offset inward by dx, dy (negative: outward)."""
    r = math.radians(t)
    return (EC[0] + (ER[0] - dx) * math.cos(r),
            EC[1] + (ER[1] - dy) * (1.0 - EK * math.cos(r)) * math.sin(r))


def egg_arc(t0, t1, dx=0.0, dy=0.0, n=24):
    return [egg_pt(t0 + (t1 - t0) * i / n, dx, dy) for i in range(n + 1)]


def egg_scaled(t0, t1, scale, n=24):
    """An arc of the egg's outline scaled toward its centre: a cross-contour on a round form."""
    return [(EC[0] + scale * (x - EC[0]), EC[1] + scale * (y - EC[1])) for (x, y) in egg_arc(t0, t1, n=n)]


# --- tests used to cut the rows round the bowl and the egg ----------------------------
def in_ellipse(x, y, c, rx, ry):
    return ((x - c[0]) / rx) ** 2 + ((y - c[1]) / ry) ** 2 <= 1.0


def in_bowl(x, y, padx=0.0, pady=0.0):
    """Inside the bowl's silhouette (rim ellipse plus the wall below it), padded."""
    if in_ellipse(x, y, BC, RIM[0] + padx, RIM[1] + pady):
        return True
    return y >= BC[1] and in_ellipse(x, y, BC, BODY[0] + padx, BODY[1] + pady)


def in_egg(x, y, padx=0.0, pady=0.0):
    return in_ellipse(x, y, EC, ER[0] + padx, ER[1] * 1.15 + pady)


def in_thing(x, y, padx=0.0, pady=0.0):
    return in_bowl(x, y, padx, pady) or in_egg(x, y, padx, pady)


def runs(p0, p1, blocked, min_len=0.05, n=600):
    """Cut a straight row into the runs that stay clear of `blocked`; each run is two points."""
    pts = [(p0[0] + (p1[0] - p0[0]) * i / n, p0[1] + (p1[1] - p0[1]) * i / n) for i in range(n + 1)]
    out, cur = [], []
    for p in pts:
        if blocked(*p):
            if cur:
                out.append(cur)
            cur = []
        else:
            cur.append(p)
    if cur:
        out.append(cur)
    result = []
    for c in out:
        a, b = c[0], c[-1]
        if math.hypot(b[0] - a[0], b[1] - a[1]) >= min_len:
            result.append([a, b])
    return result


def cut_arc(points, blocked, min_pts=3):
    """Cut a polyline into the pieces that stay clear of `blocked`."""
    out, cur = [], []
    for p in points:
        if blocked(*p):
            if len(cur) >= min_pts:
                out.append(cur)
            cur = []
        else:
            cur.append(p)
    if len(cur) >= min_pts:
        out.append(cur)
    return out


def bell(peak, ends=0.1, n=5):
    """A pressure list that rises to `peak` in the middle and falls to `ends`."""
    return [ends + (peak - ends) * math.sin(math.pi * i / (n - 1)) for i in range(n)]


# --- the places the plan reads -------------------------------------------------------
bowl = polygon(rim(180, 360) + body(0, 180), name="bowl")
egg = polygon(egg_arc(0, 360, n=72), name="egg")
rim_light = polygon(rim(185, 300, n=20) + interior(300, 185, n=20), name="rim_light")
egg_light = polygon(egg_arc(135, 315, n=36), name="egg_light")
egg_shade = polygon(egg_arc(-35, 125, n=32) + egg_arc(125, -35, dx=0.060, dy=0.050, n=32),
                    name="egg_shade")
bowl_shadow = polygon(interior(-75, 95, n=24) + egg_arc(120, -50, dx=-0.004, dy=-0.004, n=24),
                      name="bowl_shadow")
floor_lit = polygon(interior(95, 285, n=24) + egg_arc(250, 120, dx=-0.004, dy=-0.004, n=20),
                    name="floor_lit")
cast = polygon(egg_arc(15, 115, dx=-0.004, dy=-0.004, n=20)
               + egg_arc(115, 15, dx=-0.080, dy=-0.035, n=20), name="cast")
bowl_wall = polygon(rim(0, 180) + body(180, 0), name="bowl_wall")
bowl_cast = polygon([(0.81, 0.62), (0.87, 0.68), (0.90, 0.74), (0.89, 0.80), (0.83, 0.845),
                     (0.70, 0.865), (0.55, 0.855), (0.44, 0.825), (0.38, 0.79)]
                    + body(110, 15, n=24), name="bowl_cast")
table_far = polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 0.40), (0.0, 0.40)], name="table_far")
table_near = polygon([(0.0, 0.62), (0.17, 0.62), (0.22, 0.72), (0.30, 0.80), (0.34, 0.88),
                      (0.34, 1.0), (0.0, 1.0)], name="table_near")

# the egg's highlight: paper never touched, a little inside the outline toward the window
HL_C = (0.393, 0.482)
HL_R = (0.032, 0.026)
highlight = polygon(arc(HL_C, HL_R[0], HL_R[1], 0, 360, n=24), name="highlight")


def in_highlight(x, y, padx=0.0, pady=0.0):
    return in_ellipse(x, y, HL_C, HL_R[0] + padx, HL_R[1] + pady)


# the silhouette of bowl and egg together, offset outward by a pad, from the left point
# clockwise over the top (the egg's crown breaking the rim) and back under the bowl
def silhouette(padx, pady, n=36):
    top = rim(180, 360, dx=-padx, dy=-pady, n=n)
    out = [p for p in top if not (in_egg(*p, padx, pady) and p[1] < EC[1])]
    crown = [p for p in egg_arc(180, 360, dx=-padx, dy=-pady, n=n) if not in_bowl(*p, padx, pady)]
    k = next(i for i, (x, y) in enumerate(out) if x > EC[0] - ER[0]) if crown else 0
    return out[:k] + crown + out[k:] + body(0, 180, dx=-padx, dy=-pady, n=n)


def slit_polygon(outer, inner, name):
    """A polygon with a hole: outer boundary, a zero-width slit, the hole's boundary reversed."""
    lx, ly = inner[0]
    ly = round(ly * H) / H          # the slit sits on a pixel boundary, so no row is missed
    ox, oy = outer[0]
    return polygon([(ox, ly)] + outer[1:] + [(ox, ly), (lx, ly)] + inner[::-1] + [(lx, ly)],
                   name=name)


def holed_polygon(outer, inner, name):
    """A polygon with a hole anywhere inside it: the slit runs from the outer vertex nearest
    the hole's first point."""
    hx, hy = inner[0]
    j = min(range(len(outer)), key=lambda i: (outer[i][0] - hx) ** 2 + (outer[i][1] - hy) ** 2)
    rot = outer[j:] + outer[:j]
    return polygon(rot + [rot[0], (hx, hy)] + inner[::-1] + [(hx, hy)], name=name)


# the table minus the bowl and the egg, as one polygon with a slit, for the stump
def table_ring(padx, pady):
    return slit_polygon([(0.0, 0.0), (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)],
                        silhouette(padx, pady), "table")


# the band of table beside the bowl, between two pads, for the band's own stump
def band_ring(outer_px, inner_px):
    return slit_polygon(silhouette(outer_px * PX, outer_px * PY), silhouette(inner_px * PX, inner_px * PY),
                        "band")


# --- the plan ------------------------------------------------------------------------
s.plan(why="one white thing holding one pale thing on a darker ground: the paper left alone "
           "where the window falls, and tone laid everywhere else to make it read as light",
       values={table_far: 0.68, table_near: 0.63, bowl_wall: 0.74, rim_light: 0.94,
               floor_lit: 0.73, egg_light: 0.83, egg_shade: 0.46, bowl_shadow: 0.44,
               cast: 0.20, bowl_cast: 0.46},
       lightest=rim_light, subject_share=0.55)
