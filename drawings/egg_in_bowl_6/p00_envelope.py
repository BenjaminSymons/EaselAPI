"""Pass 0: the envelope, in pencil, free. Moved until it is right; nothing charged."""
# the bowl's silhouette, its interior, and the egg
s.pencil(bowl, pressure=0.6)
s.pencil(polygon(interior(0, 360, n=48), name="interior_line"), pressure=0.5)
s.pencil(egg, pressure=0.6)
# the terminator on the egg: the shade side is the outline from -45 to 135 degrees
s.pencil(polygon(egg_arc(-45, 135, n=24) + egg_arc(135, -45, dx=0.06, dy=0.05, n=24),
                 name="terminator"), pressure=0.4)
# the cast shadow on the bowl's floor, the bowl's shadow on the table, the highlight
s.pencil(cast, pressure=0.5)
s.pencil(bowl_cast, pressure=0.4)
s.pencil(highlight, pressure=0.4)
print(s.thumbnail({table_far: 0.68, table_near: 0.63, bowl_wall: 0.74, rim_light: 0.94,
                   floor_lit: 0.73, egg_light: 0.83, egg_shade: 0.46, bowl_shadow: 0.44,
                   cast: 0.20, bowl_cast: 0.46}))
print(s.look())
