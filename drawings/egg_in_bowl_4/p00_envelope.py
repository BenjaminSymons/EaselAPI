"""Pass 0: the envelope, in pencil, free. The arrangement and every round thing's
terminator, looked at with the grid, and the masses flat and small."""

s.pencil(silhouette, pressure=0.6)
s.pencil(rim_line, pressure=0.4)
s.pencil(interior, pressure=0.5)
s.pencil(egg, pressure=0.6)
s.pencil(eggarc(-60, 128, k=0.5), pressure=0.4)          # the egg's terminator
s.pencil(castarc(15, 140), pressure=0.4)                  # the cast shadow's outer line
print(s.look(grid=True, path="out/p00_envelope_grid.png"))
print(s.thumbnail({region("all"): 0.54, silhouette: 0.93, interior: 0.85, wall: 0.72,
                   bowl_lit: 0.80, bowl_shade: 0.56, egg: 0.75, egg_lit: 0.92,
                   egg_shade: 0.56, cast: 0.26}, size=256, path="out/p00_thumbnail.png"))
print(s.budget_line())
