"""Pass 2: the bowl. The band of table beside it, along its silhouette, one layer where the
rows are two, stopping where the egg's crown breaks the silhouette; the outer wall as arcs
of the body's own outline offset inward, lit at the left and turning at the right; the lit
floor as arcs round the inside, a 2H held off and stumped twice."""


def pressure_at(x, y):
    x, y = max(0.0, min(1.0, x)), max(0.0, min(1.0, y))
    return min(1.0, 0.74 + 0.26 * (0.6 * x + 0.4 * y))


OUT = 26                              # the band's centre, outside the silhouette, in pixels:
BAND_W = 0.035                        # a 36 px stroke covering 8 to 44 px out, where the
                                      # rows do not reach; 8 px is left for the splatter

# --- the band beside the bowl, in the table's own value --------------------------------
# Measured in rehearsal: a 2H layer at 0.85 to 1.0 reads 0.60 whatever the pressure, and
# any 2H layer over the rows pushes them from 0.67 toward the grade's floor. So the band
# is narrow, only where the rows do not reach, and held to the pressure that reads as the
# table; and it is stumped by the table's own stump polygon a third time, not a new ring.
band = rim(180, 360, dx=-OUT * PX, dy=-OUT * PY, n=48) + body(0, 180, dx=-OUT * PX, dy=-OUT * PY, n=48)
pieces = cut_arc(band, lambda x, y: in_egg(x, y, 20 * PX, 20 * PY))
crown = cut_arc(egg_arc(195, 345, dx=-OUT * PX, dy=-OUT * PY, n=30),
                lambda x, y: in_bowl(x, y, 16 * PX, 16 * PY))
for piece in pieces + crown:
    s.line(piece, "2H", pressure=[max(0.5, pressure_at(*p) - 0.10) for p in piece], tip="side",
           width=BAND_W, smooth=False, note="table")
s.stump(table_ring(15 * PX, 15 * PY), strength=1.0)
print(s.look())

# --- the outer wall: three arcs along the body, lit left, turning right -----------------
wall_clear = lambda x, y: in_ellipse(x, y, IC, IR[0] + 14 * PX, IR[1] + 14 * PY)
for k, (dx, dy) in enumerate(((0.015, 0.020), (0.0375, 0.050), (0.060, 0.080))):
    for piece in cut_arc(body(0, 180, dx=dx, dy=dy, n=36), wall_clear):
        s.line(piece, "2H", pressure=[0.15, 0.95, 0.95, 0.85, 0.70, 0.55, 0.45, 0.35, 0.12],
               tip="side", width=0.03, smooth=False, note="subject")
wall_stump = polygon(arc(BC, RIM[0] - 0.010, RIM[1] + 0.012, 0, 180, 36)
                     + body(180, 0, dx=0.004, dy=0.005, n=36), name="wall_stump")
s.stump(wall_stump, strength=1.0)
print(s.look())

# --- the lit floor: arcs round the inside of the interior, left of the egg --------------
floor_clear = lambda x, y: in_egg(x, y, 28 * PX, 28 * PY)
for k in (0.5, 1.3):
    dx, dy = k * 0.030, k * 0.040
    for piece in cut_arc(interior(95, 285, dx=dx, dy=dy, n=36), floor_clear, min_pts=5):
        s.line(piece, "2H", pressure=[0.15, 0.7, 0.7, 0.4, 0.7, 0.7, 0.15], tip="side",
               width=0.03, smooth=False, note="subject")   # dips where the arc turns tightest
floor_stump = polygon(interior(92, 288, dx=0.004, dy=0.005, n=30)
                      + egg_arc(255, 115, dx=-0.016, dy=-0.021, n=20), name="floor_stump")
s.stump(floor_stump, strength=1.0)
s.stump(floor_stump, strength=1.0)
print(s.look())
