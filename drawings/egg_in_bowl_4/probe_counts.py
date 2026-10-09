"""A probe, charged nothing: read the finished session file and count what the notes
need. Marks per pass by the script that laid them, the looks and rehearsals captured,
the longest run of marks with no look or rehearsal between them, and the grades used."""
from collections import Counter

from easel import Session

s = Session.load("drawing.easel")
recs = s.history.records
print("records:", len(recs), " charged:", s.stroke_count, " spent:", s.spent, " budget left:", s.remaining)

kinds = Counter(getattr(r, "kind", type(r).__name__) for r in recs)
print("kinds:", dict(kinds))

grades = Counter()
for r in recs:
    g = getattr(r, "grade", None)
    if g is None and isinstance(getattr(r, "params", None), dict):
        g = r.params.get("grade")
    if g:
        grades[g] += 1
print("grades:", dict(grades))

# what the capture kept
caps = getattr(s, "captures", None)
if caps is not None:
    ck = Counter()
    for c in caps:
        ck[getattr(c, "kind", type(c).__name__)] += 1
    print("captures:", len(caps), dict(ck))
passes = getattr(s, "passes", None)
if passes is not None:
    print("passes kept:", len(passes))
    for p in passes:
        if isinstance(p, dict):
            print("  ", {k: v for k, v in p.items() if k not in ("sources", "lines", "report")})
        else:
            print("  ", getattr(p, "scripts", None), getattr(p, "mode", None),
                  getattr(p, "at", None), getattr(p, "until", None))

# the looks, as the check counts them
looked = getattr(s, "_looked", None)
if looked is not None:
    looked = sorted(set(looked))
    print("look indices:", looked)
    marks_idx = [i for i, r in enumerate(recs) if getattr(r, "charged", True)]
    gaps, last = [], 0
    for L in looked + [len(recs)]:
        gaps.append(L - last)
        last = L
    print("longest run of records between looks:", max(gaps))

print(s.reports()[-1] if s.reports() else "no reports")
