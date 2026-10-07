"""The graphite medium's value scale: what each grade lays, measured off the view.

    python scripts/probe_graphite_scale.py [paper]

For every grade, a patch is filled with side-of-pencil passes at three pressures and
one, two and four passes deep, and its value is read the way ``compare()`` reads a
place -- the median of ``Canvas.values()`` over the patch, 0 black and 1 white -- on a
1024x768 canvas. Beside it, the share of the patch's pixels the tooth let the first
pass reach at all (``open``), which is the speckle a light hand leaves. The table is
what ``CALIBRATION.md`` *The graphite medium* quotes; rerun it after moving a grade.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from easel.canvas import Canvas  # noqa: E402
from easel.graphite import GRADES  # noqa: E402
from easel.stroke import draw_graphite  # noqa: E402

PRESSURES = (0.25, 0.5, 1.0)
PASSES = (1, 2, 4)
W, H = 1024, 768


def patch_value(paper: str, grade: str, pressure: float, passes: int, tip: str = "side",
                seed: int = 7) -> tuple[float, float]:
    """``(median value of the patch, share of its pixels the first pass reached)``."""
    canvas = Canvas(W, H, texture=paper, ground="white", seed=seed)
    # A patch 0.30 wide and 0.12 tall at the canvas's centre, filled with side passes
    # laid across it, each pass a row of overlapping strokes; later passes cross it.
    x0, x1, y0, y1 = 0.35, 0.65, 0.44, 0.56
    opened = None
    for k in range(passes):
        rng = np.random.default_rng([seed, k])
        if k % 2 == 0:
            rows = np.linspace(y0 + 0.01, y1 - 0.01, 8)
            for r in rows:
                draw_graphite(canvas, [(x0 - 0.02, r), (x1 + 0.02, r)], grade, pressure, tip,
                              rng=rng, smooth=False)
        else:
            cols = np.linspace(x0 + 0.01, x1 - 0.01, 18)
            for c in cols:
                draw_graphite(canvas, [(c, y0 - 0.02), (c, y1 + 0.02)], grade, pressure, tip,
                              rng=rng, smooth=False)
        if opened is None:
            px = canvas.graphite[int(y0 * H) + 4:int(y1 * H) - 4, int(x0 * W) + 4:int(x1 * W) - 4]
            opened = float((px > 0.02).mean())
    view = canvas.values()[int(y0 * H) + 4:int(y1 * H) - 4, int(x0 * W) + 4:int(x1 * W) - 4]
    return float(np.median(view)) / 255.0, opened


def main(argv: list[str]) -> int:
    paper = argv[0] if argv else "cartridge"
    bare = Canvas(W, H, texture=paper, ground="white", seed=7).values()
    print(f"paper {paper}, white ground: value {np.median(bare) / 255.0:.3f} bare")
    print(f"side tip, a 0.30 x 0.12 patch at the centre of a {W}x{H} canvas; median value "
          f"of the view, 0 black 1 white; `open` is the share of pixels the first pass reached")
    head = "grade  ceiling " + "  ".join(f"p={p:<4g} x1    x2    x4   open" for p in PRESSURES)
    print(head)
    for name, g in GRADES.items():
        cells = []
        for p in PRESSURES:
            vals = []
            opened = 0.0
            for n in PASSES:
                v, o = patch_value(paper, name, p, n)
                vals.append(v)
                opened = o
            cells.append("  ".join(f"{v:.2f}" for v in vals) + f"  {opened:.0%}".rjust(6))
        print(f"{name:5s}  {g.ceiling:.2f}    " + "     ".join(cells))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
