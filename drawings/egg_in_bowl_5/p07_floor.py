"""Pass 7: the bowl's floor. The export without the envelope showed the egg's lit side
vanishing into the bowl's paper floor: paper against paper, no edge at all. A white
bowl's floor in light is not paper. Rings of its own ellipse offset inward 24 px (not
scaled: a scaled copy of so flat an ellipse overlaps four deep at the top and leaves
gaps at the sides, which the first rehearsal showed as swirls), a row across the
middle, 2H held off, lighter toward the window, cut 8 px short of the egg, stumped
twice along the same paths (cut round the egg and the cast shadow, so neither is
lifted). Then a second stump over the table, rectangles and hugging polygons both:
the first rehearsal stumped the rectangles alone and left a faint rectangle.
"""
fx, fy, frx, fry = FLOOR
ccx, ccy, crx, cry, crot = CAST


def in_cast(px, py, grow):
    r = math.radians(-crot)
    x, y = px - ccx, py - ccy
    x, y = x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r)
    return (x / (crx + grow)) ** 2 + (y / (cry + grow)) ** 2 <= 1.0


def in_egg_or_cast(px, py, grow):
    return in_egg(px, py, grow) or in_cast(px, py, grow)


laid = 0
paths = [ell_px(fx, fy, frx - 13 - 24 * k, fry - 13 - 24 * k, 100, 460, step=3) for k in range(3)]
row = [(fx - 190 + 4 * i, fy + 1) for i in range(0, 96)]       # the middle, left to right
paths.append(row)
for pts_px in paths:
    for pts, pl in cut_arc(pts_px, [0.7, 0.55, 0.6, 0.78, 0.7] if pts_px is not row
                           else [0.55, 0.65, 0.78], in_egg, 8.0):
        s.line(pts, "2H", pressure=pl, tip="side", width=0.03, smooth=False, note="floor")
        laid += 1
print("floor laid:", laid)
print(s.look(region="C4:G7", scale=None, path="out/p07_look_01_crop.png"))
for n in range(2):
    for pts_px in paths:
        for pts, pl in cut_arc(pts_px, [1.0, 1.0], in_egg_or_cast, 14.0):
            s.stump(pts, strength=1.0, width=0.045, note="floor stump")
            laid += 1
    # a look between the two rounds: the rehearsal's check found 16 stumps with none
    print(s.look(region="C4:G7", scale=None, path=f"out/p07_look_stump_{n + 1}_crop.png"))
print("with stumps:", laid)
print(s.look(region="C4:G7", scale=None, path="out/p07_look_02_crop.png"))
# the table's second stump, to even the mottle one stump left over a large place
G = 6.0
ul = polygon([N(215, 322), N(512, 322)] + silhouette(270, 180, G) + [N(215, 450)])
ur = polygon([N(512, 322), N(809, 322), N(809, 450)] + silhouette(0, -90, G))
ll = polygon([N(215, 450)] + silhouette(180, 90, G) + [N(512, 576), N(215, 576)])
lr = polygon(silhouette(0, 90, G) + [N(512, 576), N(809, 576), N(809, 450)])
for place in (Region(0.0, 0.0, 1.0, 0.42), Region(0.0, 0.75, 1.0, 1.0),
              Region(0.0, 0.42, 0.21, 0.75), Region(0.79, 0.42, 1.0, 0.75), ul, ur, ll, lr):
    s.stump(place, strength=1.0, note="table second stump")
print(s.look(path="out/p07_look_03.png"))
print(s.look(sketch=False, path="out/p07_look_03_nosketch.png"))
floor_probe = polygon([N(270, 400), N(360, 400), N(360, 480), N(270, 480)], name="floor_probe")
floor_right = polygon([N(640, 400), N(740, 400), N(740, 470), N(640, 470)], name="floor_right")
print(s.compare({floor_probe: 0.84, floor_right: 0.82, egg_lit: 0.93, bowl_lit: 0.88,
                 egg_shade: 0.45, bowl_shadow: 0.40, table_far: 0.68, table_near: 0.55},
                path="out/p07_compare.png"))
