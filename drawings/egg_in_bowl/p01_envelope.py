# Pass 1: the arrangement, in free pencil. Nothing here is charged.
s.pencil(wall, pressure=0.5)
s.pencil(rim, pressure=0.6)
s.pencil(inner, pressure=0.5)
s.pencil(belly, pressure=0.5)
s.pencil(egg, pressure=0.7)
s.pencil(egg_shade, pressure=0.4)
s.pencil(bowl_shadow, pressure=0.4)
s.pencil(egg_cast, pressure=0.4)
s.pencil(bowl_cast, pressure=0.4)
s.pencil(bowl_wall_shade, pressure=0.3)
s.pencil(floor_lit, pressure=0.3)
print(s.thumbnail({wall: 0.70, table: 0.52, bowl: 0.93, bowl_wall_shade: 0.66,
                   bowl_cast: 0.36, bowl_shadow: 0.36, egg: 0.90, egg_shade: 0.42,
                   egg_cast: 0.24}))
print(s.look(grid=True))
