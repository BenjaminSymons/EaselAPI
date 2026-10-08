"""Pass 9: the passage I would apologise for. The table.

Two angles of rows and two stumps made the table read as cloud: a mottle with no
surface and no direction, and the zone round the bowl, stumped smooth, a different
texture from the rows beside it. A wooden table has a grain. A third set of rows,
horizontal, narrower, a hard grade leant on and left unstumped, cut round the bowl and
the egg, so that the marks stay as marks and run the same way everywhere, across the
smooth zone and the mottle alike. The two table places stay inside the plan: the rows
are light enough that the medians move by a few hundredths.

No stump in this pass, and nothing near the darks.

Budget for the pass: 30.
"""
before = len(s.history.records)
standing = [bowl, egg]
n = 0
ys = [0.02 + 0.034 * i for i in range(29)]
for k, y in enumerate(ys):
    row = [(-0.03, y), (1.03, y)]
    if y < 0.5:
        grade, pr = "2H", [0.72 + 0.3 * y, 0.84 + 0.3 * y]
    else:
        grade, pr = "HB", [0.48 + 0.16 * (y - 0.5), 0.58 + 0.16 * (y - 0.5)]
    n += lay_rows([row], grade, pr, 0.028, note="table grain", avoid=standing,
                  margin=0.016, flip_odd=(k % 2 == 1))
    if k in (9, 19):
        print(s.look(path=f"out/p09_rows_{k}.png"))
print("strokes:", n)
print(s.look(path="out/p09_a_whole.png"))
print(s.look(region="A1:D4", scale=None, path="out/p09_b_table_full.png"))
print(s.report(since=before))
print(s.compare(s.plan(), path="out/p09_compare.png"))
print(s.checklist())
