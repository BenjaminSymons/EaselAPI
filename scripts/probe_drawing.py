"""Measure a test drawing against `SPEC.md`'s pass criteria, off its session file.

    python scripts/probe_drawing.py drawings/<name>/drawing.easel [drawing.png]

Reads the log, the captures and the canvas, and prints one line per criterion with the
number it was read from: the longest run of marks between looks (the loop), the grades
and tips used, the darkest and lightest values on the canvas and whether paper white
survives inside the subject's planned places, the plan's places as the check reads
them, and whether a replay of the log lands on the export within one level a pixel.
Nothing here is a judgement; the picture is.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from easel import Session  # noqa: E402
from easel.history import History  # noqa: E402
from easel.session import _values_of  # noqa: E402


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    s = Session.load(argv[0])
    records = s.history.records
    paid = History.paid_marks(records)
    print(f"{argv[0]}: {len(records)} records, {len(paid)} marks charged of "
          f"{s.budget}, medium {s.medium}, {s.canvas.texture_name}, seed {s.seed}")

    # The loop: looks (captures of kind look) against the marks laid between them.
    looks = sorted(c["at"] for c in s.captures if c.get("kind") == "look")
    rehearsals = sum(1 for c in s.captures if c.get("kind") == "rehearse")
    gaps = []
    last = 0
    for at in [*looks, len(records)]:
        gaps.append(sum(1 for r in records[last:at] if r.kind not in History.UNPAINTED_KINDS))
        last = at
    print(f"looks: {len(looks)} captured, {rehearsals} rehearsals; longest run of marks "
          f"between looks {max(gaps) if gaps else 0} (criterion: at most 15)")

    # Grades and tips.
    grades = Counter(r.params.get("grade") for r in records if r.kind == "graphite")
    tips = Counter(r.params.get("tip") for r in records if r.kind == "graphite")
    kinds = Counter(r.kind for r in records)
    vias = Counter(r.params.get("via") or "hand" for r in records if r.kind == "graphite")
    print(f"grades: {dict(grades)} (criterion: three or more)")
    print(f"tips: {dict(tips)} (criterion: side used for the masses); kinds: {dict(kinds)}; "
          f"laid through: {dict(vias)}")

    # Values on the canvas, in the engine's convention.
    view = _values_of(s.canvas.to_srgb8(impasto=False))
    bare = Session(s.canvas.width, s.canvas.height, texture=s.canvas.texture_name,
                   ground=s.canvas.ground_spec, seed=s.seed, timelapse=False,
                   medium=s.medium).canvas
    paper = float(np.median(_values_of(bare.to_srgb8(impasto=False))))
    darkest = float(np.percentile(view, 0.5))
    print(f"values: darkest half-percentile {darkest:.3f} (criterion: at most "
          f"{paper * 0.20:.3f}, which is 0.80 of the way from paper {paper:.3f} to black); "
          f"paper never touched: {float((s.canvas.graphite <= 1e-6).mean()):.1%} of the canvas")

    plan = s._plan
    if plan.values:
        print("the plan's places, as the check reads them (median value; criterion: within "
              "0.10 of what was planned):")
        for place, value in plan.values.items():
            mask = s._place_mask(place)
            read = float(np.median(view[mask])) if mask.any() else float("nan")
            untouched = float((s.canvas.graphite[mask] <= 1e-6).mean()) if mask.any() else 0.0
            flag = "" if abs(read - value) <= 0.10 else "  <-- off"
            print(f"  {str(place):28s} planned {value:.2f}  reads {read:.2f}  "
                  f"paper untouched {untouched:.0%}{flag}")
        if plan.lightest is not None:
            mask = s._place_mask(plan.lightest)
            print(f"  lightest planned at {plan.lightest}: reads {float(np.median(view[mask])):.2f}, "
                  f"paper untouched {float((s.canvas.graphite[mask] <= 1e-6).mean()):.0%}")
    else:
        print("no plan declared")

    # The replay against the canvas, and against the export if one is given.
    again = s.replay()
    off = int((np.abs(again.canvas.to_srgb8().astype(int) - s.canvas.to_srgb8().astype(int))
               .max(axis=2) > 1).sum())
    print(f"replay: {off} pixels more than one level off the saved canvas "
          f"(criterion: 0)")
    if len(argv) > 1 and Path(argv[1]).exists():
        from PIL import Image
        exported = np.asarray(Image.open(argv[1]).convert("RGB"), dtype=int)
        if exported.shape == again.canvas.to_srgb8().shape:
            off = int((np.abs(again.canvas.to_srgb8().astype(int) - exported).max(axis=2) > 1).sum())
            print(f"export: {off} pixels more than one level off the replay")
    print(s.checklist())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
