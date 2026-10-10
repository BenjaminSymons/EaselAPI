"""Pass 8: the signature, outside the budget, and the export without the envelope. A mark,
not a name: two short ticks in the lower right corner, over the table's tone, so leant on."""

s.line([(0.905, 0.950), (0.935, 0.942)], "HB", pressure=0.9, tip="point", width=0.004,
       note="signature")
s.line([(0.912, 0.962), (0.928, 0.958)], "HB", pressure=0.9, tip="point", width=0.004,
       note="signature")
print(s.look(sketch=False))
print(s.look(scale=256, sketch=False))
