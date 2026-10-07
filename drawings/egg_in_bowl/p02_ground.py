# Pass 2: the two big planes, the wall and the table, as broad side strokes laid in
# rows at two angles, then stumped to close the tooth. The rows stop short of the
# bowl by half a stroke; the band round the bowl is laid in the bowl's own pass.
#
# Second version. The first (rehearsed, never committed) used HB/2B at p=0.35-0.6 and
# came back as holes: the probe showed that a hard grade leant on fills the tooth
# where a soft one held lightly rides its peaks. 2H at p=1.0 reads 0.56, HB at 0.9
# reads 0.40, and the stump closes what is left.
EDGE = 0.045          # half a wide stroke, in y: the broad rows keep this far from the table line


def table_line(x):
    return TABLE_Y_L + (TABLE_Y_R - TABLE_Y_L) * x


def in_wall_core(x, y):
    return y < table_line(x) - EDGE


def in_wall_band(x, y):
    return table_line(x) - EDGE - 0.01 <= y < table_line(x) - 0.004


def in_table_core(x, y):
    return y > table_line(x) + EDGE and not in_bowl_grown(x, y)


def in_table_band(x, y):
    return table_line(x) + 0.004 < y <= table_line(x) + EDGE + 0.01 and not in_bowl_grown(x, y)


wall_read = polygon([(0.05, 0.03), (0.95, 0.03), (0.95, 0.27), (0.05, 0.27)])
table_front_read = polygon([(0.05, 0.85), (0.95, 0.85), (0.95, 0.98), (0.05, 0.98)])
table_left_read = polygon([(0.05, 0.40), (0.15, 0.40), (0.15, 0.80), (0.05, 0.80)])
table_right_read = polygon([(0.88, 0.40), (0.98, 0.40), (0.98, 0.80), (0.88, 0.80)])

before = s.stroke_count
# The wall: lighter on the left, by the window; two angles so it is not a comb.
lay_rows(rows(in_wall_core, 0, 0.040, phase=0.5), "2H", [0.55, 0.80], 0.07, note="wall")
lay_rows(rows(in_wall_core, 9, 0.046), "2H", [0.50, 0.72], 0.07, note="wall")
lay_rows(rows(in_wall_band, 0, 0.013), "2H", [0.55, 0.78], 0.026, note="wall")
print(f"wall: {s.stroke_count - before} strokes")

# The table: darker to the right and toward the front.
before = s.stroke_count
lay_rows(rows(in_table_core, 0, 0.042), "HB", [0.55, 0.72], 0.07, note="table")
lay_rows(rows(in_table_core, -7, 0.048), "HB", 0.60, 0.07, note="table")
lay_rows(rows(lambda x, y: in_table_core(x, y) and y > 0.74, 4, 0.05), "HB", 0.55, 0.07,
         note="table")
lay_rows(rows(in_table_band, 0, 0.013), "HB", [0.55, 0.70], 0.026, note="table")
print(f"table: {s.stroke_count - before} strokes")

read(wall_read, "wall before stump")
read(table_front_read, "table front before stump")
read(table_left_read, "table left before stump")
read(table_right_read, "table right before stump")

before = s.stroke_count
s.stump(wall, strength=1.0, note="wall")
s.stump(table, strength=1.0, note="table")
print(f"stumps: {s.stroke_count - before} strokes")

read(wall_read, "wall after stump")
read(table_front_read, "table front after stump")
read(table_left_read, "table left after stump")
read(table_right_read, "table right after stump")
read(rim, "rim (should still be paper)")
print(s.compare(s.plan()))
print(s.look(grid=True))
