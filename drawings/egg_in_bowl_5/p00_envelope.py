"""The envelope, free: the bowl, the egg, the terminator, the shadows, and a thumbnail.

Second arrangement: the first (env_01) had the egg too small against the bowl and a
twisted egg_lit polygon; erase() takes the free pencil out before anything is charged.
"""
s.erase()
s.pencil(rim, pressure=0.6)
s.pencil(inner, pressure=0.4)
s.pencil(belly, pressure=0.6)
s.pencil(floor, pressure=0.3)
s.pencil(egg, pressure=0.6)
s.pencil(egg_shade, pressure=0.35)
s.pencil(bowl_shadow, pressure=0.35)
s.pencil(cast_core, pressure=0.35)
s.pencil(cast_table, pressure=0.3)
print(s.look(grid=True, path="out/env_02_grid.png"))
print(s.thumbnail({table_far: 0.68, table_near: 0.55, cast_table: 0.34, bowl: 0.92,
                   bowl_lit: 0.90, bowl_shadow: 0.45, egg_lit: 0.93, egg_shade: 0.45,
                   cast_core: 0.26}, size=256, path="out/env_02_thumb.png"))
