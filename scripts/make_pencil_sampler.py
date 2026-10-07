"""Generate ``samples/pencils.png`` -- every grade at three pressures, point and side,
on every paper, plus a hatched patch and a side-built patch per grade.

The graphite medium's primary test artefact, as ``samples/brushes.png`` is the
paint's. Regenerate it after any change to the grade table, the gate, the deposit
or the papers, and then *look at it*: the question it answers is whether a 2H looks
like a 2H and a 6B like a 6B, and no number answers that.

    python scripts/make_pencil_sampler.py

Each panel is one paper, drawn as **one canvas** at the panel's size rather than a
cell at a time, so the tooth is at the scale a drawing is made at; the marks are
drawn at the width they would have on a canvas :data:`SCALE` pixels wide. Things to
look for:

* a hard grade that fills the tooth under a light hand, or a soft one that speckles
  under a heavy one (the bite is wrong);
* a grade whose three pressures look alike (the gamma is wrong), or whose heaviest
  line is lighter than the next grade's lightest (the ceilings overlap);
* a hatched patch that is one grey bar (the stroke's own dabs are adding, which is the
  rule the engine was built to avoid), or a crossed patch no darker than a single
  layer (strokes are not adding);
* a side mark with no tooth in it, or one that reads as a ruled rectangle.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from easel.canvas import Canvas  # noqa: E402
from easel.graphite import GRADES, SIDE_WIDTH  # noqa: E402
from easel.stroke import draw_graphite  # noqa: E402
from easel.texture import TEXTURES  # noqa: E402

#: The marks are drawn at the width they would have on a canvas this many pixels
#: wide, whatever the panel's own size: a pencil line is a fraction of the long side,
#: and a sampler that drew an HB at a 190-pixel cell's fraction would draw it under a
#: pixel wide.
SCALE = 1024
PRESSURES = [0.25, 0.5, 1.0]
#: The columns: the point at three pressures, the side at three, a hatched patch
#: (one layer on the left, a second crossing it on the right), and the side laid
#: three times over itself.
COLUMNS = ([("point", p) for p in PRESSURES] + [("side", p) for p in PRESSURES]
           + [("hatch", 0.6), ("side x3", 0.5)])
#: The papers, the medium's own first.
PAPERS = ("cartridge",) + tuple(t for t in TEXTURES if t != "cartridge")

CELL_W, CELL_H = 190, 120
LABEL_W = 70
HEADER_H = 26
TITLE_H = 30
GROUND = "white"


def _cell_rng(seed: int, row: int, col: int) -> np.random.Generator:
    return np.random.default_rng([seed, row, col])


def _path(rng: np.random.Generator, at, inset: float = 0.08) -> list[tuple[float, float]]:
    """A gently curved line across a cell, with a little variation per mark."""
    wob = rng.uniform(-0.05, 0.05, size=4)
    us = (inset, 0.36, 0.64, 1.0 - inset)
    vs = (0.5 + wob[0], 0.42 + wob[1], 0.58 + wob[2], 0.48 + wob[3])
    return [at(u, v) for u, v in zip(us, vs, strict=True)]


def draw_panel(canvas: Canvas, seed: int) -> None:
    """Every grade and column onto one canvas: rows are grades, columns are
    :data:`COLUMNS`. The canvas is the panel, so cell ``(r, c)`` is the rectangle
    ``[c * CELL_W, r * CELL_H]`` in pixels."""
    w, h = canvas.width, canvas.height
    scale = SCALE / canvas.long_side

    for r, grade in enumerate(GRADES.values()):
        for c, (what, pressure) in enumerate(COLUMNS):
            x0, y0 = c * CELL_W, r * CELL_H

            def at(u: float, v: float, x0=x0, y0=y0) -> tuple[float, float]:
                return ((x0 + u * CELL_W) / (w - 1), (y0 + v * CELL_H) / (h - 1))

            rng = _cell_rng(seed, r, c)
            point_w = grade.width * scale
            side_w = SIDE_WIDTH * scale
            if what == "point":
                draw_graphite(canvas, _path(rng, at), grade, pressure, "point", point_w,
                              rng=_cell_rng(seed, r, c + 100))
            elif what == "side":
                draw_graphite(canvas, _path(rng, at), grade, pressure, "side", side_w,
                              rng=_cell_rng(seed, r, c + 100))
            elif what == "hatch":
                # Eight lines one way across the patch; eight more across the right
                # two thirds of it, so one layer and two sit side by side.
                for k in range(8):
                    t = 0.14 + 0.72 * k / 7.0
                    pts = [at(0.10 + 0.05 * t, t + 0.06), at(0.92 - 0.05 * t, t - 0.06)]
                    draw_graphite(canvas, pts, grade, pressure, "point", point_w,
                                  rng=_cell_rng(seed, r, c + 200 + k), smooth=False)
                for k in range(8):
                    u = 0.36 + 0.56 * k / 7.0
                    pts = [at(u - 0.04, 0.10), at(u + 0.04, 0.90)]
                    draw_graphite(canvas, pts, grade, pressure, "point", point_w,
                                  rng=_cell_rng(seed, r, c + 300 + k), smooth=False)
            else:  # side x3
                for k in range(3):
                    dv = (k - 1) * 0.04
                    pts = [at(0.08, 0.50 + dv), at(0.50, 0.46 + dv), at(0.92, 0.52 + dv)]
                    draw_graphite(canvas, pts, grade, pressure, "side", side_w,
                                  rng=_cell_rng(seed, r, c + 400 + k))


def build_panel_array(texture: str, seed: int) -> np.ndarray:
    """One paper's panel as 8-bit sRGB, no labels: what the golden test hashes."""
    canvas = Canvas(len(COLUMNS) * CELL_W, len(GRADES) * CELL_H, texture=texture,
                    ground=GROUND, seed=seed)
    draw_panel(canvas, seed)
    return canvas.to_srgb8()


def panel_seed(texture: str) -> int:
    return 100 + TEXTURES.index(texture) * 1000


def build_panel(texture: str) -> Image.Image:
    """One paper: grades down the side, tips and pressures across, labelled."""
    arr = build_panel_array(texture, panel_seed(texture))
    width = LABEL_W + arr.shape[1]
    height = TITLE_H + HEADER_H + arr.shape[0]
    panel = Image.new("RGB", (width, height), (22, 22, 24))
    draw = ImageDraw.Draw(panel)
    draw.text((8, 9), f"paper: {texture}   (marks at their width on a {SCALE} px canvas)",
              fill=(255, 235, 190))
    for i, (what, pressure) in enumerate(COLUMNS):
        x = LABEL_W + i * CELL_W
        label = f"{what}  p={pressure:g}" if what in ("point", "side") else what
        draw.text((x + 6, TITLE_H + 7), label, fill=(190, 190, 200))
    panel.paste(Image.fromarray(arr, mode="RGB"), (LABEL_W, TITLE_H + HEADER_H))
    for i in range(1, len(COLUMNS)):
        x = LABEL_W + i * CELL_W
        draw.line([(x, TITLE_H), (x, height)], fill=(70, 70, 78), width=1)
    for r, name in enumerate(GRADES):
        y = TITLE_H + HEADER_H + r * CELL_H
        draw.text((8, y + CELL_H // 2 - 4), name, fill=(235, 235, 240))
        if r:
            draw.line([(LABEL_W, y), (width, y)], fill=(70, 70, 78), width=1)
    return panel


def main() -> int:
    out = Path(__file__).resolve().parents[1] / "samples" / "pencils.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    panels = [build_panel(texture) for texture in PAPERS]
    gap = 10
    width = max(p.size[0] for p in panels)
    height = sum(p.size[1] for p in panels) + gap * (len(panels) - 1)

    sheet = Image.new("RGB", (width, height), (14, 14, 16))
    y = 0
    for p in panels:
        sheet.paste(p, (0, y))
        y += p.size[1] + gap

    sheet.save(out)
    print(f"Wrote {out} ({sheet.size[0]}x{sheet.size[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
