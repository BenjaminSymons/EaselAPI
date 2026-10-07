# Probe 2, rehearsed only: does a pressure list on line() follow the stroke's own
# direction or canvas order? And what do harder grades at heavy pressure read?
s.line([(0.05, 0.08), (0.95, 0.08)], grade="2B", pressure=[0.1, 1.0], tip="side", width=0.05,
       smooth=False, note="probe L->R, light to heavy")
s.line([(0.95, 0.16), (0.05, 0.16)], grade="2B", pressure=[0.1, 1.0], tip="side", width=0.05,
       smooth=False, note="probe R->L, light to heavy along the stroke")
read(polygon([(0.05, 0.06), (0.25, 0.06), (0.25, 0.10), (0.05, 0.10)]), "row1 left")
read(polygon([(0.75, 0.06), (0.95, 0.06), (0.95, 0.10), (0.75, 0.10)]), "row1 right")
read(polygon([(0.05, 0.14), (0.25, 0.14), (0.25, 0.18), (0.05, 0.18)]), "row2 left")
read(polygon([(0.75, 0.14), (0.95, 0.14), (0.95, 0.18), (0.75, 0.18)]), "row2 right")


def swatch(name, fn):
    before = s.stroke_count
    fn()
    v = s.palette.value_of(s.sample(cell(name), rendered=True))
    print(f"{name}: reads {v:.3f}, cost {s.stroke_count - before}")


swatch("A4", lambda: s.hatch(cell("A4"), angle=[0, 9], spacing=0.04, grade="2H", pressure=0.85,
                            tip="side", width=0.07))
swatch("B4", lambda: s.hatch(cell("B4"), angle=[0, 9], spacing=0.04, grade="2H", pressure=1.0,
                            tip="side", width=0.07))
swatch("C4", lambda: s.hatch(cell("C4"), angle=[0, 9], spacing=0.04, grade="HB", pressure=0.75,
                            tip="side", width=0.07))
swatch("D4", lambda: s.hatch(cell("D4"), angle=[0, 9], spacing=0.04, grade="HB", pressure=0.9,
                            tip="side", width=0.07))
swatch("E4", lambda: s.hatch(cell("E4"), angle=[0, 9], spacing=0.04, grade="4H", pressure=1.0,
                            tip="side", width=0.07))
swatch("F4", lambda: s.hatch(cell("F4"), angle=[0, 9], spacing=0.04, grade="2B", pressure=0.8,
                            tip="side", width=0.07))
swatch("G4", lambda: s.hatch(cell("G4"), angle=[0, 9], spacing=0.04, grade="4B", pressure=0.9,
                            tip="side", width=0.07))
swatch("H4", lambda: s.hatch(cell("H4"), angle=[0, 9], spacing=0.04, grade="6B", pressure=0.9,
                            tip="side", width=0.07))
# the same four, stumped once at full strength
for name in ("A6", "B6", "C6", "D6"):
    grade, pr = {"A6": ("2H", 0.85), "B6": ("2H", 1.0), "C6": ("HB", 0.75), "D6": ("HB", 0.9)}[name]
    swatch(name, lambda: s.hatch(cell(name), angle=[0, 9], spacing=0.04, grade=grade, pressure=pr,
                                tip="side", width=0.07))
    before = s.stroke_count
    s.stump(cell(name), strength=1.0)
    print(f"  stumped: reads {s.palette.value_of(s.sample(cell(name), rendered=True)):.3f}, "
          f"cost {s.stroke_count - before}")
print(s.look(grid=True))
