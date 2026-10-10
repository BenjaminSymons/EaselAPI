# Graphite fork of easel-paint — project spec

Oct 7, 2026 · @Ben

> **Status, 2026-10-10.** The fork is severed from upstream, so "merge back upstream" and
> "keep the upstream shape" no longer apply, and "nothing refused" is superseded for a
> graphite session, where paint verbs raise. [`CLAUDE.md`](CLAUDE.md) has the current
> rules. [`SPEC-REVIEW.md`](SPEC-REVIEW.md) records where the build differs from this text.

## Purpose and scope

Fork [easel-paint](https://github.com/Gemberkoekje/EaselAPI) (MIT, v0.8.0 at 1 Oct 2026) into a graphite drawing engine for LLM agents, where pencil is the medium rather than a sketch layer under paint. Deliver one test drawing made by an agent from the fork, plus a per-stroke frame capture that plays back as a time-lapse.

In scope:

- A `Session` that draws in graphite only: pencil grades, pressure, tooth, layering, stump blending, erasing
- Drawing helpers an agent can plan with (hatching, contour, scribble masses) that emit ordinary strokes
- A `DRAFTSMAN.md` guide in the same spirit as `PAINTER.md`, held to a word budget
- Frame capture on every stroke, export to GIF and MP4, and a scrubbable HTML viewer
- MCP exposure of the new verbs so Claude Code can drive it

Out of scope for the first cut: coloured pencil, charcoal, ink, paper grain beyond what the existing tooth model gives, reference-photo tracing, and any merge back upstream (open that as a separate conversation with the author once the fork works).

## What easel-paint already gives us

Most of the hard infrastructure exists. The fork changes the medium and adds capture; it does not rebuild the loop.

| Piece | Upstream state | Fork action |
| --- | --- | --- |
| Canvas | Linear-light RGB + wetness, thickness, `sketch` (graphite) and `height` (tooth) channels | Promote `sketch` to the primary channel; drop wetness/thickness from the graphite session |
| `pencil()` | Lays graphite under paint, not counted as a stroke | Rework into the main stroke verb; count it |
| Stroke renderer | Dab-based, spacing along travel, smoothed wobble, tooth gate with aperiodic grain | Reuse as-is; the tooth gate is exactly what pencil on paper needs |
| Pressure | Width follows pressure on round tips; pressure profiles per stroke | Reuse; map pressure to value as well as width |
| Regions and shapes | `cell("D5")`, `blob`, `hull`, `ribbon`, normalised 0–1 coordinates | Reuse untouched |
| `look()`, `preview()`, `rehearse()`, `cost()` | Grid overlay, values view, crop, diff; plan-before-commit | Reuse untouched |
| History | Every stroke logged; seeded per `(seed, stroke index)`; `replay(upto=n)` exact | Reuse; this is the basis of frame capture |
| `easel timelapse` | Rebuilds a GIF from the log with `--every N --scale W` | Extend, not replace (see Frame capture) |
| `report()` / `checklist()` | Reads guide warnings off the log and canvas | Rewrite the rules for graphite; the mechanism stays |
| Palette and pigment mixing | Kubelka-Munk, no black | Not needed; graphite is a single value channel |
| MCP server | 20 tools, `run` takes a script as text | Reuse; register the new verbs |
| Golden-image tests | Hash + PNG per texture and the brush sampler | Add a pencil sampler and goldens for it |

Read `LESSONS.md` before touching the engine. It records which engine decisions are load-bearing and the rules for changing the guide.

## Graphite medium model

Graphite is a deposit of value on paper, gated by tooth and saturating towards the grade's maximum darkness. The model has one channel (`graphite`, 0–1 per pixel) and one surface (`height`, the tooth already in the engine).

**Deposit per dab.** `deposit = grade.rate × pressure^grade.gamma × tooth_gate(height, pressure)`. The gate opens with pressure: light pressure catches only the high points of the tooth (the speckle of a 2H sketch line); heavy pressure fills the valleys. The channel saturates at `grade.max_value`, so a 2H cannot be pushed to a 6B black no matter how many passes.

**Grades.** Ship a fixed set and let the agent name them as a human would.

| Grade | Rate (per dab) | Max value (0 = white, 1 = black) | Gamma | Point behaviour |
| --- | --- | --- | --- | --- |
| 4H | 0.04 | 0.35 | 1.6 | Holds a fine point; width barely responds to pressure |
| 2H | 0.06 | 0.45 | 1.4 | Fine, slightly wider under pressure |
| HB | 0.10 | 0.60 | 1.2 | Default; moderate width response |
| 2B | 0.16 | 0.78 | 1.0 | Wide under pressure; starts to smear |
| 4B | 0.22 | 0.88 | 0.9 | Soft; broad side-of-pencil marks |
| 6B | 0.30 | 0.96 | 0.8 | Near-black; crumbles into the tooth |

The numbers are starting points. Calibrate them the way upstream did: draw a value scale per grade, measure, and record the measurement in `CALIBRATION.md`.

**Tip orientation.** Two tips: `point` (round, width follows pressure) and `side` (a flat oriented tip, like laying the pencil over, 4–8× the point width, low rate, strong tooth texture). `side` reuses the existing `flat` tip geometry.

**Layering.** Graphite on graphite deposits less as the surface fills; apply `(1 - graphite)^0.5` to the deposit so the first pass counts most. This gives the burnished look of repeated HB without needing a separate burnish tool.

**Stump / blending.** `stump(place, strength)` convolves the graphite channel within the shape with a small kernel biased along the stroke direction, and redistributes rather than removes: total graphite in the region is conserved minus a small loss (0.05) to the stump. Blending also fills the tooth valleys, so set a `filled` flag that stops later light strokes from speckling in that region.

**Erasing.** Erasing is a repair with side-effects, not an undo. Two erasers. `kneaded(place, strength)` lifts a fraction of graphite uniformly (0.3–0.7 per pass). `plastic(place)` lifts hard with a clean edge, for pulling highlights. Neither lifts to white: a residue floor of `graphite × grade.ghost` stays on the paper, where `ghost` is per grade (4H 0.03, 2H 0.05, HB 0.08, 2B 0.14, 4B 0.20, 6B 0.28) and is taken from the softest grade present in the region. The plastic eraser also burnishes: it sets the `filled` flag on the region, so later light strokes lay flatter and darker than on fresh tooth, and the speckle of a 2H sketch line is lost there. Kneaded leaves more ghost but does not burnish. Both are strokes in the log and count against budget. Calibrate `ghost` on a lifted value scale and record it in `CALIBRATION.md`; the aim is that the agent erases sparingly, not never.

**Paper.** Reuse the three textures (`smooth`, `linen`, `rough`) and add `cartridge` (medium, random grain) as the default. Ground is paper white; no toned ground in the first cut.

## API additions

Keep the upstream shape: one `Session`, normalised coordinates, every mark logged, nothing refused. New verbs are added beside the old ones rather than replacing them, so a graphite session can still call `look()`, `preview()` and `rehearse()` unchanged.

**Session**

```python
from easel import Session, blob, cell

s = Session(1024, 768, medium="graphite", paper="cartridge", seed=7, budget=400, capture=True)
```

`medium="graphite"` selects the pencil engine and disables paint verbs. `capture=True` turns on frame capture (next section).

**Stroke verbs**

| Verb | Signature | What it does |
| --- | --- | --- |
| `line` | `line(points, grade="HB", pressure=0.5 or [..], tip="point")` | The primitive; one stroke along a polyline with a pressure profile |
| `hatch` | `hatch(place, angle, spacing, grade, pressure, taper=True)` | Parallel strokes filling a shape, each tapered at both ends |
| `crosshatch` | `crosshatch(place, angles=[30, 120], ...)` | Two or more hatch passes |
| `contour` | `contour(place, grade, pressure, closed=True)` | A single stroke around a shape's outline, with pressure varying by a profile |
| `scribble` | `scribble(place, density, grade, pressure)` | Overlapping loose strokes to build a mass fast; the graphite equivalent of `block_in` |
| `tone` | `tone(place, value, grade="2B", tip="side")` | Side-of-pencil passes until the region reaches `value`, measured against the channel |
| `stump` | `stump(place, strength=0.5, direction=None)` | Blend |
| `kneaded`, `plastic` | `(place, strength)` | Erase |

All of them emit `line` records into the log, so replay and capture see only one kind of mark.

**Look and measure**

- `look(values=True)` already returns greyscale; make it the default for graphite
- `look(tooth=True)`: show where the tooth is still open versus filled or burnished, and where ghost residue sits, for deciding whether a light stroke will speckle and whether a highlight is still clean paper
- `compare({place: value})` and `report()` carry over; rewrite the standing warnings for graphite (one grade for the whole drawing, hatching at one angle everywhere, no range of edge hardness, darkest value under 0.7 by the end, a region erased more than twice, ghost residue or burnish inside the lightest planned cell, erasures above 10% of strokes spent)

**CLI**

`easel new drawing.easel --medium graphite --paper cartridge --budget 400 --capture`, then the existing `run`, `look`, `undo`, `export`. Add `easel pencils` (the grade sampler) and `easel film` (see Frame capture).

**MCP**

Register the new verbs in the existing server. No new tools are needed for the stroke verbs because `run` takes a script; add `film` as a tool so the agent can hand back its own time-lapse.

**DRAFTSMAN.md**

The graphite method, same structure as `PAINTER.md` and held to the same word budget by a test: the first hour, the loop (look every 5–15 strokes), order of work (envelope in 2H, placement lines, masses with side 2B, mid-tones, darks last, highlights lifted last), the standing mistakes, nine warm-up exercises, the closing checklist. It states the erasing rule plainly: a ghosted line is fine under a dark mass and ruins a highlight, so erase early and plan highlights as paper never touched. Write it after the first two test drawings, not before, so it records what was measured.

## Frame capture and time-lapse

Upstream already rebuilds a GIF from the log (`easel timelapse --every 3`), and because every stroke is seeded by `(seed, stroke index)` the rebuild is exact. The fork keeps the log as the source of truth and adds three things: capture of the agent's own looks, a proper video export, and a viewer that shows the stroke beside what the agent was thinking.

**What is captured.** With `capture=True` the session writes a `frames/` directory beside the `.easel` file:

| Event | File | Why |
| --- | --- | --- |
| Each stroke committed | nothing extra; the log already holds it | Frames are rebuilt from the log at film time, so capture costs nothing per stroke |
| Each `look()` | `looks/NNNN.png` + the arguments used | Shows what the agent saw before its next decision |
| Each `rehearse()` | `rehearsals/NNNN.png` + whether it was then committed | Shows the paths not taken |
| Each pass (`easel run`) | `passes/NN.py` and the agent's `why` from `s.plan()` | The script that made the next run of strokes |

**Film export.** `easel film drawing.easel out.mp4 --fps 12 --every 1 --scale 720 --hold-looks 1.0`

- Replays the log, rendering a frame every `--every` strokes; a stroke is drawn progressively over 2–4 frames when `--stroke-motion` is set, by replaying its dabs in travel order, so a long contour line visibly travels rather than appearing
- Inserts each captured look as a held frame (`--hold-looks` seconds) with the grid overlay, so the viewer sees the agent stop and check
- Writes MP4 via `imageio-ffmpeg` (bundled binary, no system ffmpeg), GIF via Pillow as upstream does, or a PNG sequence
- Optional caption strip at the foot of each frame: stroke index, grade, pressure, and the pass name

**Viewer.** `easel film --html out/` writes a self-contained page: a scrubber over the stroke index, a play button at a chosen fps, and a side panel showing the pass script line that produced the current stroke and the most recent look. Plain JavaScript, one HTML file plus a frames directory; no framework. Frames load lazily from the PNG sequence so a 400-stroke drawing is not 400 images in memory.

**Determinism caveat.** A frame rebuilt on a different numpy build can differ by one level in a few pixels. That does not matter for a film. If byte-exact matters, store the exported frames rather than relying on rebuild.

## Test drawing

The acceptance test is one drawing made end-to-end by Claude Code from `DRAFTSMAN.md`, with no human mark and no reference photo, plus its film.

**Subject.** Decide before the agent opens the repository (upstream found that any example subject in the docs gets copied). Pick something with a clear light, three or four value masses, one hard edge and one lost edge: a single pear on a table with a window to the left is enough. Record the choice in `drawings/<name>/NOTES.md` before the first stroke.

**Setup.** 1024×768, cartridge paper, seed fixed, budget 400 strokes, capture on, MCP server launched from Claude Code with `--dir drawings/`.

**Pass criteria**

- [ ] The agent follows the loop: a `look()` in the log at least every 15 strokes
- [ ] At least three grades used, and `side` tip used for the masses
- [ ] `compare()` against the agent's own value plan within 0.10 on every cell it planned
- [ ] Darkest value on the canvas at or above 0.80; paper white preserved somewhere in the subject
- [ ] `easel film` produces an MP4 that plays, and the HTML viewer scrubs to any stroke
- [ ] `replay()` of the log matches the export within one level per pixel
- [ ] `NOTES.md` written by the agent names what went wrong, as upstream's painters do

**Artefacts kept.** The `.easel` file, the numbered pass scripts, `prelude.py`, the final PNG, the MP4, the viewer directory and `NOTES.md`, all under `drawings/<name>/`, so the drawing is a worked example in the same form as upstream's `paintings/`.

Run it twice with the same subject and different seeds. The first run calibrates the grade table and finds the gaps in the guide; the second is the one that counts.

## Work plan

Estimates assume Claude Code doing most of the typing with you reviewing output and looking at samplers. Total is roughly four to six working days.

1. **Fork and read** (half a day). Fork the repo, run the suite, run `easel guide`, read `LESSONS.md`, `PAINTING.md` and `src/easel/` to find where `sketch`, the tooth gate and the tip renderer live. Write down what to keep.
2. **Graphite channel and `line`** (1 day). Add `medium="graphite"`, the grade table, the deposit model, `point` and `side` tips, saturation and layering. Produce `samples/pencils.png`: every grade at three pressures on each paper. Look at it; adjust the numbers until a 2H and a 6B look like a 2H and a 6B.
3. **Helpers and tools** (1 day). `hatch`, `crosshatch`, `contour`, `scribble`, `tone`, `stump`, `kneaded`, `plastic`. Each emits `line` records. Golden tests for each.
4. **Capture and film** (1 day). Look and rehearsal capture, `easel film` with MP4 and progressive stroke motion, the HTML viewer. Test on an upstream painting's log first, since those already exist.
5. **DRAFTSMAN.md and report rules** (half a day, after step 6's first run). Write the guide from what the first drawing cost; rewrite the standing warnings in `report()` for graphite.
6. **Test drawings** (1 day). Two runs as described above, the second after the guide exists. Keep both.
7. **MCP and tidy** (half a day). Register `film`, update `server.json`, README section for the graphite medium, changelog.

Step 4 does not depend on steps 2 and 3 and can go first if the film is the part you want to see working soonest.

## Risks and open questions

**Risks**

- Upstream moves fast (nine releases in three weeks, 0.8.0 on 1 Oct 2026). Pin the fork to a tag and decide early whether to track it; a graphite `medium` flag that leaves paint untouched merges forward more easily than a rewrite of `Canvas`.
- The `sketch` channel may be coupled to the paint pipeline in ways the README does not show (it is "covered in proportion to what lands"). Step 1 settles whether it can be promoted or needs a sibling channel.
- Pencil on paper is a less forgiving medium for an LLM than paint. There is no `cover()`; a wrong dark line stays. The guide must push the agent to work light-to-dark, rehearse more and commit less, which costs budget.
- A value-only medium removes the colour cues the agent used to read its own `look()`. Expect the first drawing to be muddy; the `tooth=True` look and a stricter `compare()` are the mitigation.
- `imageio-ffmpeg` adds a 30 MB binary dependency. Make it an extra (`easel-paint[film]`) as upstream did for MCP and Mixbox.

**Decide before starting**

- [ ] Tag to fork from: 0.8.0, or wait for whatever lands next
- [ ] Package name for the fork if it goes to PyPI (`easel-graphite`?) or keep it a private checkout
- [ ] Test subject, chosen and written down before the agent sees the repo
- [ ] Whether the viewer is worth building or whether MP4 plus a contact sheet is enough for the first pass
- [ ] Whether to open an issue upstream describing the graphite medium before building, in case the author is already on it

**Sources**

- [easel-paint on PyPI](https://pypi.org/project/easel-paint/0.7.0/) (0.7.0 page; 0.8.0 released 1 Oct 2026)
- [EaselAPI repository](https://github.com/Gemberkoekje/EaselAPI)
