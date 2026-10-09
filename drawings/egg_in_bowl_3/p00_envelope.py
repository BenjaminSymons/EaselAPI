"""Pass 0: the envelope, in pencil. Free. The arrangement, looked at with the grid, and
the masses flat and small."""
# Why this subject: a white egg in a white bowl is one light with two shapes in it.
s.erase()                                              # free: the envelope moved, redraw it
s.pencil(bowl, pressure=0.6)
s.pencil(inner, pressure=0.4)
s.pencil(egg, pressure=0.6)
s.pencil(egg_arc(0.62, -45, 140), pressure=0.4)        # the egg's terminator, decided now
s.pencil(int_shade, pressure=0.35)
s.pencil(egg_cast_seen, pressure=0.35)
s.pencil(bowl_cast_seen, pressure=0.35)
s.pencil(bowl_cast_core, pressure=0.35)
print(s.look(grid=True, path="out/p00_envelope_grid.png"))
print(s.thumbnail({table_far: 0.70, table_near: 0.56, table_left: 0.62, bowl: 0.93,
                   wall: 0.56, int_lit: 0.82, int_shade: 0.46, bowl_cast_seen: 0.30,
                   bowl_cast_core: 0.18, egg: 0.95, egg_shade: 0.44, egg_cast_seen: 0.36},
                  size=256, path="out/p00_thumbnail.png"))
print(s.look(scale=256, path="out/p00_envelope_small.png"))
