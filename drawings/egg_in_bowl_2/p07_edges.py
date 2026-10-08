"""Pass 7: edges, last but one. (p06, values read and corrected, was not needed: after
p05 all nine places read inside 0.10, the largest miss floor_lit +0.06.)

Three rehearsals before this one taught the pass:

1. A hard-edge stroke of 2H at 1.0 along the far rim read 0.58 against a table at
   0.67 and drew a dark ring. The stroke has to be the table's value, not the table's
   grade leant on.
2. The band zone round the bowl, where the table's rows stopped short, is one layer
   where the rows are two, and reads lighter: a halo. Laying two more bands and
   stumping along them at 0.9 made the halo lighter still, since the zone had already
   been stumped twice with the table and a stump lightens what the check reads.
3. So the zone is measured here, before and after, by two crescents 12 to 70 px out
   from the bowl (halo_near, halo_far), against the table strips beside them, and the
   bands are laid to the number with no stump.

The lost edge: the egg's shade into the inner wall's shade behind it, at the narrow
end; three stumps dragged across the join. The egg's crown against the inner wall had
a paper gap from the wall's arcs being cut round the egg with a margin; two short arcs
at no margin close it.

Budget for the pass: 15.
"""
before = len(s.history.records)
n = 0

# --- the measuring places -------------------------------------------------------------
halo_near = polygon(lower(15, 165, step=5, ry=LOW_RY + 12)
                    + ell(BOWL_CX, BOWL_CY, LOW_RX + 58, LOW_RY + 70, 165, 15, step=5),
                    name="halo_near")
halo_far = polygon(ell(BOWL_CX, BOWL_CY, RIM_RX + 12, RIM_RY + 12, 195, 345, step=5)
                   + ell(BOWL_CX, BOWL_CY, RIM_RX + 58, RIM_RY + 70, 345, 195, step=5),
                   name="halo_far")
table_beside_near = Region(0.25, 0.79, 0.75, 0.86)
table_beside_far = Region(0.25, 0.30, 0.75, 0.38)
gauge = {halo_near: 0.56, table_beside_near: 0.56, halo_far: 0.66, table_beside_far: 0.66}
print("--- before")
print(s.compare(gauge, path="out/p07_gauge_before.png"))

# The gauge before anything read halo_near -0.03 against the table beside it at -0.02,
# and halo_far -0.04 against -0.02: the zone is at the table's value already, and what
# the eye called a halo is a zone stumped smooth beside mottled rows. Three bands of
# HB at 0.62 and 2H at 0.95 were rehearsed here and read halo_near -0.10 and halo_far
# -0.09: a dark ring. No bands.

# --- the hard edge, in the table's value ----------------------------------------------
OFF = 5.0   # px into the table
# cut round the egg's crown, which stands above the rim: three rehearsals read
# egg_light at 91% paper never touched before this stroke was found to be the cause
for run, u0, u1 in cut(ell(BOWL_CX, BOWL_CY, RIM_RX + OFF, RIM_RY + OFF, 176, 364, step=3),
                       egg, margin=0.008):
    s.line(run, "2H", pressure=0.8, tip="side", width=0.013, smooth=False,
           note="subject hard edge, far rim against the table")
    n += 1
s.line(ell(BOWL_CX, BOWL_CY, LOW_RX + OFF + 2, LOW_RY + OFF + 2, -4, 184, step=3), "HB",
       pressure=[0.72, 0.78, 0.66, 0.6, 0.6], tip="side", width=0.018, smooth=False,
       note="subject hard edge, near wall against the table")
n += 1
print(s.look(region="A4:H8", path="out/p07_a_hard.png"))

# --- the egg's crown against the inner wall: close the paper gap ----------------------
for k, p in ((0.15, 0.9), (0.5, 0.95)):
    # cut at the stroke's half-width, so its body ends on the egg's outline: at a
    # margin of half a pixel the body crossed six pixels into the lit crown
    for run, u0, u1 in cut(crescent_arc(k, 230, 330, step=2), egg, margin=0.008):
        s.line(run, "HB", pressure=p, tip="side", width=0.012, smooth=False,
               note="subject inner wall shade, up to the egg's crown")
        n += 1

# --- the lost edge: across the join ---------------------------------------------------
for t in (-18, -2, 14):
    s.stump([egg_pt(t, 0.9), egg_pt(t, 1.14)], strength=0.8, width=0.02,
            note="lost edge stump across the join")
    n += 1
print("strokes:", n)
print(s.look(region="C4:G6", scale=None, path="out/p07_b_lost.png"))
print(s.look(path="out/p07_c_whole.png"))
print(s.report(since=before))
print(s.compare(s.plan(), path="out/p07_compare.png"))
