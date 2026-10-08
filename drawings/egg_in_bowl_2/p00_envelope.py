"""Pass 0: the envelope, in pencil. Free, and not the drawing.

Why this subject: an egg and a white bowl are two whites, and the picture is whether
they read as one light against a mid table with nothing but the paper to say so.
"""
s.pencil(bowl, pressure=0.6, note="bowl silhouette")
s.pencil(rim(0, 360), pressure=0.5, note="rim")
s.pencil(lip(0, 360), pressure=0.4, note="lip")
s.pencil(inner(180, 360), pressure=0.4, note="inner wall meets floor")
s.pencil(egg, pressure=0.6, note="egg")
s.pencil(terminator_pts, pressure=0.5, note="egg terminator")
s.pencil(cast_arc(1.0), pressure=0.5, note="cast shadow")
print(s.thumbnail(path="out/thumb_envelope.png"))
print(s.look(grid=True, path="out/look_envelope_grid.png"))
print(s.cost([{"points": r, "grade": "2H", "tip": "side"} for r in [rim(0, 360)]]))
