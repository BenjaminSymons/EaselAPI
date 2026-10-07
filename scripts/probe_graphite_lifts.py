"""The stump and the erasers, measured: what each keeps, moves and leaves.

    python scripts/probe_graphite_lifts.py

A patch ``0.40 x 0.40`` at the centre of a ``1024x768`` cartridge canvas is toned to a
value with ``tone()``, then stumped at four strengths, or lifted once with each eraser
at each strength -- and read three ways: the share of its graphite kept, its spread
(the standard deviation of the channel over its middle), and what ``compare()`` would
read, the median of the values view. The table is what ``CALIBRATION.md`` *The stump
and the erasers* quotes; rerun it after moving a constant.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from easel import Session  # noqa: E402
from easel.regions import Region  # noqa: E402

W, H = 1024, 768
PATCH = Region(0.3, 0.3, 0.7, 0.7)
INNER = (slice(int(0.33 * H), int(0.67 * H)), slice(int(0.33 * W), int(0.67 * W)))


def toned(value: float, grade: str = "2B") -> Session:
    s = Session(W, H, medium="graphite", seed=7, timelapse=False, out_dir="out")
    s.tone(PATCH, value, grade=grade)
    return s


def read(s: Session) -> float:
    return s._median_value(s.canvas, s._place_mask(PATCH))


def main() -> int:
    print(f"a {PATCH.width:.2f} x {PATCH.height:.2f} patch at the centre of {W}x{H} cartridge, "
          f"toned with tone(); read over its middle")
    print("\nstump over a 2B tone at 0.45, worked every way:")
    print("  strength  kept   sd before -> after   median value before -> after")
    for strength in (0.3, 0.5, 0.8, 1.0):
        s = toned(0.45)
        g0 = s.canvas.graphite[INNER].copy()
        v0 = read(s)
        s.stump(PATCH, strength=strength)
        g1 = s.canvas.graphite[INNER]
        print(f"  {strength:<8}  {g1.sum() / g0.sum():.3f}  {g0.std():.3f} -> {g1.std():.3f}"
              f"        {v0:.3f} -> {read(s):.3f}")
    print("\nerasers, one pass over the patch:")
    print("  grade  toned to  eraser        graphite left  reads")
    for grade, value in (("HB", 0.60), ("2B", 0.45), ("6B", 0.20)):
        for eraser, strength in (("kneaded", 0.3), ("kneaded", 0.5), ("kneaded", 0.7),
                                 ("plastic", None), ("plastic twice", None)):
            s = toned(value, grade)
            g0 = s.canvas.graphite[INNER].copy()
            if eraser == "kneaded":
                s.kneaded(PATCH, strength=strength)
            else:
                s.plastic(PATCH)
                if eraser.endswith("twice"):
                    s.plastic(PATCH)
            g1 = s.canvas.graphite[INNER]
            label = eraser if strength is None else f"{eraser} {strength}"
            print(f"  {grade:5s}  {value:.2f}      {label:13s} {g1.sum() / g0.sum():.2f}"
                  f"           {read(s):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
