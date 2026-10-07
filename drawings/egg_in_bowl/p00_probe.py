# Probe, rehearsed only, never committed: what do wide side strokes read, and what
# does each cost? Swatches in the top row's cells, read back by sample(rendered=True).
def swatch(name, fn):
    before = s.stroke_count
    fn()
    v = s.palette.value_of(s.sample(cell(name), rendered=True))
    print(f"{name}: reads {v:.3f}, cost {s.stroke_count - before}")


swatch("A1", lambda: s.hatch(cell("A1"), angle=0, spacing=0.04, grade="2H", pressure=0.6,
                            tip="side", width=0.07))
swatch("B1", lambda: s.hatch(cell("B1"), angle=0, spacing=0.04, grade="HB", pressure=0.5,
                            tip="side", width=0.07))
swatch("C1", lambda: s.hatch(cell("C1"), angle=[0, 90], spacing=0.04, grade="HB", pressure=0.5,
                            tip="side", width=0.07))
swatch("D1", lambda: s.hatch(cell("D1"), angle=0, spacing=0.04, grade="2B", pressure=0.4,
                            tip="side", width=0.07))
swatch("E1", lambda: s.hatch(cell("E1"), angle=[0, 90], spacing=0.04, grade="2B", pressure=0.5,
                            tip="side", width=0.07))
swatch("F1", lambda: s.tone(cell("F1"), 0.52, grade="HB"))
swatch("G1", lambda: s.hatch(cell("G1"), angle=0, spacing=0.03, grade="4B", pressure=0.5,
                            tip="side", width=0.05))
swatch("H1", lambda: s.hatch(cell("H1"), angle=[0, 90], spacing=0.03, grade="2B", pressure=0.6,
                            tip="side", width=0.05))
swatch("A2", lambda: s.hatch(cell("A2"), angle=[20, 110], spacing=0.045, grade="HB", pressure=0.7,
                            tip="side", width=0.08))
swatch("B2", lambda: s.hatch(cell("B2"), angle=0, spacing=0.04, grade="2H", pressure=1.0,
                            tip="side", width=0.07))
swatch("C2", lambda: s.hatch(cell("C2"), angle=0, spacing=0.02, grade="HB", pressure=0.5,
                            tip="side", width=0.04))
swatch("D2", lambda: s.hatch(cell("D2"), angle=0, spacing=0.012, grade="HB", pressure=0.5,
                            tip="side"))
swatch("E2", lambda: s.tone(cell("E2"), 0.36, grade="2B"))
swatch("F2", lambda: s.tone(cell("F2"), 0.24, grade="4B"))
swatch("G2", lambda: s.hatch(cell("G2"), angle=0, spacing=0.05, grade="2B", pressure=0.5,
                            tip="side", width=0.10))
swatch("H2", lambda: s.hatch(cell("H2"), angle=0, spacing=0.04, grade="HB", pressure=0.5,
                            tip="point", width=0.07))
print(s.thumbnail({wall: 0.70, table: 0.52, bowl: 0.93, bowl_wall_shade: 0.66,
                   bowl_cast: 0.36, bowl_shadow: 0.36, egg: 0.90, egg_shade: 0.42,
                   egg_cast: 0.24}, size=768))
print(s.look(grid=True))
