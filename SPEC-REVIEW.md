# SPEC.md against the engine

Checked against `main` at `1ed1f69` (the commit that added `SPEC.md`). `src/` is
`v0.8.0`'s: `pyproject.toml` and `easel.__version__` both say 0.8.0, `CHANGELOG.md`
dates 0.8.0 to 2026-10-01 and its *Unreleased* section is empty. `PLAN-0.9.0.md` and
`NOTES-step1.md` are in the checkout: upstream's next round is planned, step 1 is done,
nothing under `src/` has changed since `dcdfc94`, and none of its workstreams A to J
touches the pencil or the `sketch` channel.

Each section below follows the section of `SPEC.md` with the same name. A line marked
**Sibling, not promotion** is a place where the spec assumes `sketch` can become the
graphite channel and the code says it cannot. Numbers given as *measured* were measured
on this checkout with the probe described beside them; everything else is read from
the source, with the file and line it was read from.

---

## Purpose and scope

**The value convention is inverted.** The engine's value is sRGB-encoded luminance, 0
black and 1 white: `REFERENCE.md` *Units*, `palette.value_of`, `look(values=True)`,
`compare()`, `plan(values=)` and the `values:` line all read it that way. The spec's
grade table, `tone(place, value)`, the acceptance criterion *darkest value at or above
0.80* and the seven report rules all use 0 white and 1 black. Every number the agent
plans with and every number `compare()` prints would be inverted against the spec.
Correct approach: state the spec in the engine's convention. Paper white (`GROUNDS
["white"]`, `#F6F4F0` shaded by the tooth in `Canvas.bare`) reads 0.956 *measured*.

**The darkest mark the `sketch` channel can make is value 0.229.** `Canvas.composite`
(`canvas.py:831-835`) draws the channel as `rgb * (1 - g) + GRAPHITE * g`, where
`GRAPHITE = "#3A3A40"` is one constant colour whose value is 0.229 *measured*. A
full-pressure pencil line 0.05 wide on rough paper bottoms out at sRGB 58, value 0.227
*measured*. In the spec's own convention that is a darkness of 0.77, under the 6B's
0.96 and under the acceptance criterion of 0.80. No number of passes changes it: `rub`
accumulates by maximum and the composite is a lerp to one colour. **Sibling, not
promotion:** a channel that has to reach black needs its own composite, and changing
`sketch`'s composite moves the `drawing` golden and every painting with an
underdrawing showing.

**The channel's unit has to be the value the view reports.** `GRAPHITE` is specified in
sRGB and composited in linear light; a linear multiply `rgb * (1 - g)` at `g = 0.96`
on paper at linear 0.90 lands at sRGB value 0.21, not 0.04. `LESSONS.md` *The
measurement can be right and the instrument still wrong* records the last time a
linear number was shown beside an sRGB view. Define the graphite channel in the unit
`compare()` reads (sRGB value darkness on white paper) or convert at the composite, and
write the grade table in that unit.

**No merge upstream is the right call for the first cut, and it costs nothing to keep
the option open.** `LESSONS.md` *Engine decisions that are load-bearing*: *Add
capability beside the old path, never through it*, with `block_in`'s frozen named
directions as the precedent that let a change land mid-milestone with every golden
unchanged. A sibling channel and new record kinds leave every existing golden
byte-identical, which is also the shape an upstream PR would need.

---

## What easel-paint already gives us

Row by row, against the code.

### Canvas

What `sketch` actually is: a float32 plane 0..1 of *coverage of one colour*, plus a
`has_sketch` flag that keeps the hot loop free for a painting that never draws
(`canvas.py:287-290`). It is coupled to paint in nine places:

| Where | Coupling |
|---|---|
| `Canvas.stamp` (`canvas.py:515-521`) | paint buries it: `sketch *= 1 - effective`, the same per-dab alpha the colour blend uses. `LESSONS.md` calls this contract load-bearing |
| `Canvas.composite` (`:831-835`) | drawn as the flat `GRAPHITE` colour over the paint, after the relief so it is never embossed |
| `Canvas.values`, `thumbnail_srgb8`, `to_srgb8` | all go through `composite`, so the greyscale view, the time-lapse frame and the export agree |
| `Canvas.snapshot`/`restore` (`:884-948`) | `sketch: None` means *no drawing yet*, distinct from *leave it alone*; a boxed snapshot copies the box of it |
| `Canvas.trial_copy` (`:950-968`) | copies it explicitly; what `rehearse()` paints on |
| `Session.save`/`load` (`session.py:5330`, `:5479-5485`) | written only when `has_sketch`, read with `if "sketch" in data.files` (format 1 files have none) |
| `Canvas.ground_showing` (`:332-373`) | ignores it on purpose: *a drawing over the ground is still ground showing through* |
| `Session._canvas_lines` (`:4874-4915`) | `values:` and `edges:` read `values(sketch=False)`; `pencil:` is the difference between with and without |
| `look(sketch=)`, `export(sketch=)` | one flag hides the channel *and* the `guide()` overlay (`look.py:154-157`) |

Three more things carry the name: `Session.sketch()` (`session.py:4043`) is the
assisted mode that lays prepared outlines as pencil and notes itself in `assisted`;
`sketch_lines()` is derived from the log; `has_sketch` is a meta key in every saved
file. Promoting the channel means flipping the burial rule, the flat composite, the
report's exclusion, `UNPAINTED_KINDS` and the `drawing` golden, each of which has a
test in `tests/test_precision.py:70-245`.

**Sibling, not promotion.** Add a second plane (`Canvas.graphite`, darkness in value
units, with its own `has_graphite`), composited after the paint and the relief in
`composite()` so `values()`, `thumbnail_srgb8`, `to_srgb8`, `_value_view` and
`compare()` all see it for free, never touched by `stamp`, and added to `snapshot`,
`restore`, `trial_copy`, `save` and `load` beside `sketch`. The `sketch` channel then
stays available to a graphite session as the free underdrawing it already is, which
the spec's *envelope in 2H* step wants anyway.

**Dropping wetness and thickness is unnecessary.** Both are allocated unconditionally
(`canvas.py:285-286`); `stamp` is their only writer; `composite` skips the relief when
`thickness.max() <= 1e-3`. A session that never calls `stroke()` leaves them at zero.
The real cost is elsewhere: `pencil()` and `erase()` snapshot the *whole* canvas
(`_snapshot()` with no box, `session.py:2102`, `:2147`, `:5780-5790`), four planes
of 3.1 MB each at 1024x768, and `MAX_SNAPSHOTS = 24` keeps 24 of them. A 400-record
drawing made of nothing but full snapshots holds about 450 MB resident, which is the
problem `_stroke_box` was built to end (`session.py:5934-5960`). A graphite verb has
to snapshot by box, and only the planes it touches.

### `pencil()`

`History.UNPAINTED_KINDS = ("dry", "look", "pencil", "erase")` (`history.py:105`) is a
class constant read by `paid_marks` (the budget), by `report()` at `session.py:4393`,
`:4398`, `:4641`, `:4753`, by `_buried` at `:8651` and `:8669`, and asserted by
`tests/test_reference.py:126-130` to appear in `REFERENCE.md`'s *free* column. A pencil
record carries `brush="pencil"`, `pressure=<float>` and `params={"width", "smooth",
"rng"}` (`session.py:2110-2122`); every rule in `report()` reads a mark's brush fields
off `params` (`size` at `:8302`, `:8388`, `:8473`, `:8561`, `:8853`; `tip` and `load`
at `:8712-8714`; `tip_wobble` at `:8735`) and would read defaults off a pencil record.
`notices._PAINTED = ("stroke", "glaze", "smudge")` (`notices.py:239`) is the set a
rebuild notice counts. `History.summary` prints *NOTHING DREW* for a pencil under one
unit of graphite (`history.py:185-186`).

Correct approach: a new record kind (`"graphite"`, say) that is not in
`UNPAINTED_KINDS` and so is charged by `paid_marks` with no change to the budget code,
carrying its own params (grade, tip, width, the pressure spec as `stroke` records
carry it, `rng`, `via`). `_replay_records` (`session.py:5591-5644`) dispatches on
`kind` and needs a branch for it; `pencil` stays exactly as it is. The ten `report()`
rules then skip or crash on the new kind depending on which fields it carries, so the
rules need a kind filter or graphite rules of their own (see *report()* below).

### Stroke renderer

The spec's sentence *the tooth gate is exactly what pencil on paper needs* conflates
two gates.

- `Canvas.stamp` (`canvas.py:480-502`) gates on **load**, not pressure: `need =
  min((1 - load) * texture_sensitivity, tooth_ceiling)`, a smoothstep over `_GATE_BAND
  = 0.18`, and since 0.7.0 a *drag* that reads the tooth along the stroke's travel
  (`tooth_along`) once load falls under `_DRY_FROM = 0.9`, plus per-bristle run-out
  for the comb. Load is a per-dab exponential run-out over ten diameters
  (`stroke.py:242-245`). Pressure never enters this gate; it scales `strength` (alpha)
  and, on round tips only, the radius (`stroke.py:415-422`). `stamp` also blends
  `rgb`, writes wetness and thickness and buries `sketch`: it lays paint and cannot be
  reused for graphite.
- `Canvas.rub` (`canvas.py:699-744`) is the pencil's gate and the one the spec
  describes: `need = min((1 - bite) * 0.62, tooth_ceiling)` over `_GRAPHITE_BAND =
  0.13`, where `draw_pencil` passes `pressure` as both `bite` and `strength`
  (`stroke.py:597-624`). It has no travel drag and no comb.

What the gate does at pencil bites, *measured* at 1024x768, seed 7, as the share of
pixels fully open and the mean gate:

| bite | smooth | linen | rough |
|---|---|---|---|
| 0.25 | 22% open, mean 0.41 | 21%, 0.38 | 19%, 0.35 |
| 0.55 | 79%, 0.92 | 75%, 0.88 | 69%, 0.83 |
| 0.75 | 99%, 1.00 | 97%, 0.99 | 93%, 0.98 |
| 1.00 | 100% | 100% | 100% |

So a 4H's speckle and a 6B's fill are not reachable from `pressure` alone; the gate
needs a hardness term per grade (bite decoupled from darkness) and its two constants
retuned, and the `tooth_ceiling` cap has to stay (`LESSONS.md`: uncapped, a starving
mark laid *nothing* on smooth and linen).

What is reusable as-is: `catmull_rom`, `_resample`, `_dabs` (spacing along travel,
`stroke.py:217-239`), `pressure_curve`, `press_width`, `_wander`, and the tip masks
(`brush.py:268-416`, angle quantised to 10 degrees, radius to a quarter pixel,
sub-pixel phase in the key). The right shape is a `draw_graphite()` in `stroke.py`
built the way `draw_pencil` is but on `_dabs` and `pressure_curve`, calling a new
`Canvas` deposit method; `tooth_along(travel)` is available if a side-of-pencil mark
should drag along its travel the way a dry brush does.

### Pressure

`pressure_curve` already takes a name, a scalar or a list (`stroke.py:144-183`). Width
follows pressure only on `_ROUND_TIPS` (`0.35 + 0.65 * p` of the radius, floor 0.75 px,
`stroke.py:44-49`, `:415-422`); oriented tips keep their width, and a hand-laid
pressure list on one is a notice (`chisel-pressure`). `draw_pencil` takes a *scalar*
pressure only and a fixed width of 0.0026 with a `round_hard` mask at hardness 0.75:
pressure to value exists for the pencil, pressure to width does not. Building the
graphite stroke on `_dabs` plus `pressure_curve` gets profiles and lists for nothing;
the round-tip width rule applies to `point`, and `side` keeps its width as `flat` does.

### Regions and shapes

Reuse is right, and more is reusable than the row says. `_block_in_paths(fill, b,
direction, density, overhang)` (`session.py:1176`) yields `(pass_dir, path, flipped)`
for parallel passes across a place at any angle, cut against a `Polygon`'s outline by
`_shape_paths` (`:1200`), spaced `size * (1 - 0.45 * density)` apart, alternating
direction, with `_canvas_order_pressure` keeping an asymmetric profile in canvas order
(`:7461`). That is `hatch`. `_clean_contour` and `sweep` along `shape.inset()` are
`contour`. `Polygon.mask`, `coverage`, `inside` and `_clip_cover` (`:5739`) are the
clip for anything held inside a shape.

### `look()`, `preview()`, `rehearse()`, `cost()`

Not untouched. A plan entry is dispatched by key in `_plan_specs` (`session.py:3497-
3553`): `points` is a stroke, `shape`/`region` a mass, `edge` a sweep, `band` a
scumble, `cover` a burial. `_lay` (`:3067`) maps those five to `block_in`, `sweep`,
`scumble`, `cover` and `stroke`; `_plan_price` and `_preview_entry` do the same for
`cost` and `preview`. `_check_plan_keys` holds an entry's keys to `PLAN_ACCEPTS`,
built from the five signatures (`:5869`), and `stroke()`'s `**brush_overrides` are
checked by `_check_brush_overrides` (`:7423`) against `Brush`'s fields, so
`s.stroke(..., grade="HB")` raises `TypeError` and `{"points": ..., "grade": "HB"}`
is refused as a plan. `tests/test_reference.py:304-324` holds `PLAN_KIND_KEYS` to
`PLAN_ACCEPTS` and to the grammar paragraph in `REFERENCE.md`. A graphite mark is a
sixth plan kind: register it in `_plan_specs`, `_lay`, `_plan_price`,
`_preview_entry`, `PLAN_ACCEPTS`, the test's `PLAN_KIND_KEYS`, and the reference's
grammar, and the four verbs read it unchanged thereafter. `look()` itself needs no
change for a sibling channel composited in `composite()`; `values=True` as a default
is a `Session` default, not a `look` change.

### History

The row is right about the mechanism and incomplete about three things.

- Seeding is per **record index**, not per stroke: `_stroke_rng(index)` with `index =
  _index_base + len(history.records)` (`session.py:483`, `:5519-5527`). A `pencil`,
  `dry` or `erase` record shifts the seed of every mark after it (`CALIBRATION.md`,
  *the planning verbs leave nothing behind, and three free verbs do*). Nothing new may
  take a log index unless it is a mark: notices, pass reports and the plan live beside
  the log for exactly this reason (`REFERENCE.md`, *What the tool will tell you*).
- Masses also draw from the running stream `self.rng`, and every record carries the
  stream state at the start of its call as `params["rng"]` (`_one_call`, `:5659-5714`);
  `replay()` restores it from the first record not replayed (`:5584-5588`), `undo()`
  from the first undone record (`:2466`). A graphite helper that draws wander from the
  stream has to run inside `_one_call(verb, place, mass=)`, which also stamps `via`
  on every record (what lets the check tell a pass from a hand-laid mark) and the
  painter's script line (`_call_site`, read by the dearest-calls line).
- `undo(n)` counts records, restores boxed snapshots newest first, and past
  `MAX_SNAPSHOTS` or on a loaded file rebuilds by `replay(upto=)` (`:2437-2489`). A
  verb must push its snapshot immediately before touching the canvas, in the same
  method (`LESSONS.md` trap 6, and the comment at `:2422-2424`).

### `easel timelapse`

The film is not a per-stroke record. `History.add_frame` thins the sequence by halves
past `MAX_FRAMES = 200` and doubles `_frame_stride` so the dropped frames are never
built (`history.py:247-279`); `save_gif(every=, scale=)` decimates on top (`:296-344`);
`timelapse_gif(from_log=True)` goes through `replay(frames=px)`, which constructs a
fresh `Session(timelapse=px)` whose `__init__` captures frame 0 and whose `_auto_frame`
captures after every mark, so the rebuilt film is thinned the same way (`session.py:
4139-4142`, `:5542-5552`, `:324-325`). A 400-record drawing rebuilt from the log has
at most 200 frames at stride 2 before `--every` is applied. *Extend, not replace* is
right about the command and wrong about the source: a frame per stroke has to walk the
records one at a time on one fresh session (`_one_call("replay")` around
`_replay_records([record])`, then `canvas.to_srgb8()` or `thumbnail_srgb8(px)`) and
write each frame to disk, never through `History._frames`. The pre-0.7.0 memory
problem this would otherwise bring back is in `CALIBRATION.md` B15.

### `report()` / `checklist()`

The mechanism to keep is in three parts, and each has a cost the row leaves out.

- The ten rules are `_pass_findings` over `records[since:]` (`session.py:8807`), and
  they read stroke records' brush fields (above). Each rule that is a *check* fires
  through `_notify(code, text)`, and `tests/test_notices.py` holds every code to a row
  of `notices.NOTICES`, a row of `REFERENCE.md`'s code table, and a heading in the
  document the row names. So each graphite warning is a `NOTICES` entry, a
  `REFERENCE.md` row and a `CALIBRATION.md` heading, not a string.
- The standing lines read the canvas **without** graphite (`values(sketch=False)`,
  `:4901-4902`), `values:` against the paint box (`palette.darkest_value` 0.128 to
  `lightest_value`, `:4904`), `ground:` by `ground_showing`, which treats graphite as
  ground by design, and `pencil:` as graphite still showing. Under a sibling channel
  composited as paint is, `values:` and `edges:` read it; `reach` has to become the
  grade box and the paper; `ground:` has to mean *paper never touched*; `pencil:` is
  the underdrawing still showing, which in a graphite drawing is a different question.
- `LESSONS.md`: *a check earns its line by firing on a real pass of a real painting,
  and the cheapest way to find out is to measure the condition before writing the
  rule*; *a warning that cannot fire is worse than no warning*. The spec's seven
  graphite warnings are written before any drawing exists. They are candidates, to be
  measured on the first drawing's log before any is built, which is what the spec's
  own step 5 ordering already implies.

### Palette and pigment mixing

`Session.__init__` builds a `Palette()` unconditionally and nothing breaks if it stays.
What reads it and would be wrong for graphite: the `values:` line's `reach`
(`:4904`), `compare()`'s *unreachable* split (`~`), which compares reference cells
against the palette floor, and `plan(values=)`'s pairing. Those take the grade box
instead; the palette itself needs no change.

### MCP server

Twenty-one tools, not twenty (`mcp_server.py:630-1429`: `new`, `run`, `look`,
`compare`, `prepare`, `mark`, `undo`, `export`, `timelapse`, `log`, `check`,
`brushes`, `guide`, `diagnose`, `explain`, `demo`, `plan`, `preview`, `rehearse`,
`cost`, `thumbnail`). `new` takes `texture`, `ground`, `seed`, `timelapse`, `budget`
and no medium (`:630-633`); `run` takes the script as text or a path; `--dir` exists
and is an `os.chdir` (`:1473-1483`). `mcpb/manifest.json` has `tools_generated: true`
and a long description naming the tool count; `tests/test_server_json.py` and
`tests/test_mcp.py` cover the registry entry and every tool. A `film` tool and a
`medium` argument on `new` touch all of those.

### Golden-image tests

`tests/golden_cases.py` has eight cases: `marks_<texture>` for each entry of
`texture.TEXTURES`, `drawing` (the pencil on rough: four pressures, two contours, an
opaque mass burying one and a thin glaze leaving the other, an erase), `shapes`,
`sweep`, `edges`, and `sampler` (hash only, pooled PNG), which iterates `TEXTURES` x
`BRUSHES` x sizes x pressures through `scripts/make_brush_sampler.render_cell`. Cases
are 420x300, built twice for determinism, hashed on pixels, with a fallback of one
level on at most 2% of pixels.

Consequences the row does not state:

- Adding `cartridge` to `TEXTURES` adds a `marks_cartridge` case with no stored hash
  (the suite fails until `make_golden.py` runs) and **changes the `sampler` hash**,
  since the strip gains a texture's worth of rows; `samples/brushes.png` regenerates
  with it, and `tests/test_reference.py:80-82` requires the new name in
  `REFERENCE.md`.
- `drawing` is the `sketch` channel's contract in one image. **Sibling, not
  promotion:** it must not move, which is only guaranteed if `sketch`, `rub`,
  `draw_pencil` and the composite of `sketch` are untouched.
- A pencil sampler is a new case plus a new script. `make_brush_sampler.py` drives
  `Canvas` and `paint_stroke` directly, not `Session` (`scripts/make_brush_sampler.py:
  54-64`), so its graphite twin drives `Canvas` and the new `draw_graphite`.
- `LESSONS.md` trap 2: a failing golden is an instruction to look, and `make_golden.py`
  runs only after deciding the new marks are better. Trap 1: the sampler shows
  isolated strokes at full load and was happy with a gate that silkscreened every
  accumulated mass; keep a throwaway script that lays hatching on hatching.

---

## Graphite medium model

**The per-dab deposit is the additive rule the engine was built to avoid.**
`LESSONS.md`, under the load-bearing decisions: *Graphite accumulates as a maximum,
not a sum. Dabs along a pencil line overlap almost completely and any additive rule
turns the line into a solid bar within a few dabs.* `draw_pencil` resamples at half the
radius (`stroke.py:594`), so every pixel under a line is stamped by four or more
dabs before drift; `Canvas.rub` takes `np.maximum(before, ink)` (`canvas.py:739-741`).
`deposit = rate x pressure^gamma x gate` added per dab, at the HB's rate of 0.10,
saturates at `max_value` inside one line regardless of pressure, and the `(1 - g)^0.5`
layering term only slows the last few dabs. Correct approach: accumulate **within a
stroke** as a maximum (the stroke's own field over its box, `f = max over dabs of mask
x gate x strength`), then combine **strokes** additively with saturation toward the
grade's ceiling. The rate and the layering exponent are then per stroke, and that is
the unit the grade table should be written in and calibrated in.

**The gate's constants are a sketch line's, and bite is not separable from darkness.**
`rub` reads `bite` and `strength` from the one `pressure` (`stroke.py:597-624`), and the
table under *Stroke renderer* above shows what the gate passes per bite on each
surface. A 2H that speckles under heavy pressure and a 6B that fills under light
pressure both need a hardness term that sets bite independently of the darkness laid.

**Grades.** `rate` is written *per dab*; see above. `max_value` is written with 1 as
black; see *Purpose and scope*. Both columns are starting points the spec says to
calibrate, and `LESSONS.md` trap 8 applies: write down the invariant each number holds
(a 6B's ceiling as a fraction of the way from paper to black, not a constant), because
the paper's value moves with the texture's shading and the channel's unit.

**Tip orientation.** `tip_mask("flat", ...)` is a rectangle `aspect` thick along
travel and one diameter wide across it (`brush.py:397-406`; the `flat` preset's aspect
is 0.26), rotated to the travel direction when `angle_follow` is on and pinned to
`angle` when it is off (`brush.py:192`). `_dabs` spaces it at `spacing x diameter x
aspect` along travel so consecutive stamps overlap (`stroke.py:235-236`). That is a
side-of-pencil mark laid broadside, and the mask is reusable. Two facts the spec
leaves out: `size` is a fraction of the long side, so `side` needs a width of its own
rather than a multiple of `point`'s; and an oriented tip's ends are chisel ends
(`PAINTING.md`, *The shape each tool leaves behind*), which the paint check names
(`chisel-staircase`, `chisel-pressure`) from inside `stroke()` and `block_in()` only.
Those checks will not fire on a graphite verb unless it calls them.

**Layering.** Per stroke, as above. The exponent is the one number here that nothing
in the engine constrains, so it is the one to calibrate first on a value scale.

**The `filled` flag is a new saved plane.** The engine has no per-pixel state beyond
the five planes. `height` is read-only after creation and is not saved: tooth and grain
are rebuilt from `(texture, size, seed, strength)` on load (`canvas.py:142-164`,
`session.py:5465-5471`), which `LESSONS.md` lists as load-bearing. A `filled` plane
would be a sixth array in the `.easel` file (read the way `sketch` is, with `in
data.files`, or behind a format bump from `_EASEL_FORMAT = 4`) and a sixth entry in
`snapshot`, `restore`, `trial_copy`, `save` and `load`. Before adding it, measure
whether the graphite channel itself can stand in: where `g` is high the valleys are
full, so lowering the gate's `need` by a term in the local `g` gives *later light
strokes lay flatter where the tooth is filled* with no new plane. The plastic eraser's
burnish is the one case that needs state the channel does not hold, and it can be
measured on a value scale before deciding.

**Stump.** Nothing convolves a channel anywhere in the engine. `smudge` is a dab-based
drag: a `smudge=1.0` brush that samples the canvas under each stamp (`canvas.sample`)
and lays the carried mixture back (`stroke.py:449-461`); it is a stroke in the log
(`kind="smudge"`), charged, previewable, and it works on `rgb` only. Nothing in the
engine conserves anything. `Canvas._read_along` (`canvas.py:639-657`) is a directional
box average per 10-degree bucket and shows the shape a direction-biased kernel would
take. Two ways to build `stump`, with different costs: as a stroke verb (a path and a
width, like `smudge`), it gets `preview`, `rehearse`, `cost`, the plan grammar,
`direction` from the path, `undo` by box and `replay` for free, and the `smudge-*`
notices show what such a verb gets told; as a region operation it has to log the
whole place (`LESSONS.md` trap 7, `_place_params`/`_place_from_params` at
`session.py:9434`, `:9504`) and snapshot the whole plane.

**Erasing.** `Session.erase()` exists and is not what the spec wants: it zeroes
`sketch` inside a place or everywhere, clears the `guide()` overlay with it, is free
(`UNPAINTED_KINDS`), and logs the place whole (`session.py:2132-2169`). `kneaded` and
`plastic` are new, charged kinds and must not reuse `erase`'s name, kind or freedom.
*Taken from the softest grade present in the region* needs grade per pixel, which a
scalar channel does not hold: either a second plane (softest grade seen), or derive
it from the log the way `sketch_lines()` derives the drawing (`:2171-2191`, exact for
rectangles, cut at crossings for shapes, and O(records) per call), or make ghost a
function of local darkness alone. `LESSONS.md`: measure before building; the third is
the one to measure first, on a lifted value scale.

**Paper.** `cartridge` is a branch in `make_texture` (`texture.py:73-130`: each texture
is a height map normalised to 0..1, mean near 0.5, scaled by an amplitude, 0.30 /
0.62 / 0.85), an entry in `TEXTURES`, a divisor in `build_surface`'s grain table
(`canvas.py:161`, unknown names fall to 4), a row in `REFERENCE.md`'s textures list,
and the golden changes under *Golden-image tests* above. `tooth_ceiling` is the 95th
percentile of `0.52 x height + 0.48 x grain` and lands at 0.68 to 0.70 on all three
surfaces *measured*, so a new paper's gate behaves like the others' unless its
amplitude is far from theirs. *Ground is paper white* is `ground="white"`, value 0.956.

---

## API additions

**`Session(medium=, paper=, capture=)` touches four constructors, not one.**
`Session.load` builds the object field by field with `cls.__new__` (`session.py:5372-
5442`), `_trial_session` does the same for a rehearsal copy (`:3390-3462`), and
`replay()` calls `Session(...)` with every argument spelled out (`:5542-5552`). The
comment at `:5436-5438` names the failure: a flag `__init__` sets and `load` does not
is an `AttributeError` on the first film of every pass `easel run` paints from a file.
Every new field goes in `__init__`, `load`, `_trial_session`, `replay` and the `save`
meta. `paper=` is `texture=` by another name: the CLI flag, the MCP argument, the meta
key and `Canvas.texture_name` all say `texture`. Alias it or keep the engine's word.

**Nothing disables a verb.** `_lay`, `paint` and `_plan_specs` dispatch to every
painting verb regardless of state. *Disables paint verbs* is a guard in `stroke`,
`block_in`, `sweep`, `scumble`, `cover`, `glaze` and `smudge`, or it is a default and a
line in the check rather than a refusal. The engine refuses nothing today
(`REFERENCE.md`: *the budget is a plan, not a lock*); a graphite session that can still
`pencil()` an underdrawing for free is the spec's own order of work.

**Stroke verbs.**

- `line`: fits. `pressure=0.5 or [..]` is `pressure_curve`'s contract; a `tip` argument
  that is not a `Brush` field is refused by `_check_brush_overrides` until the verb has
  its own signature.
- `hatch`: `_block_in_paths` with a graphite stroke in place of `stroke()`. Its
  `spacing` is `size x (1 - 0.45 x density)` (`REFERENCE.md`, *density*), its `angle`
  is `direction=` (degrees, a pair of points, `"axis"`, or a sequence priced as the
  sum), and `taper=True` is `pressure="taper"` on every pass with
  `_canvas_order_pressure` applied to the flipped ones. `LESSONS.md` trap 12: the angle
  is in the 0..1 coordinates, so a 45-degree hatch runs at 37 degrees on screen at 4:3,
  and the engine's answer is to hand over two points.
- `crosshatch`: `direction=(a, b)` already lays a full stack per angle.
- `contour`: `_clean_contour` sweeps one pass along `shape.inset(half the brush)`
  (`session.py:1141`); `sweep(edge, closed=True, passes=1)` is the same mark on a
  boundary. A `Polygon`'s outline is `polygon.points`.
- `scribble`: new.
- `tone(place, value)`: *passes until the region reaches `value`* is a search on a
  trial copy. `_glaze_opacity` (`session.py:766-836`) is the existing shape: it lays
  films on `scratch()` copies and halves the bracket up to `_GLAZE_SOLVE_STEPS = 12`
  times to a tolerance of 0.002, then lays the answer once for real. Graphite's
  version measures `canvas.graphite[mask].mean()` on the copy, or the `values()` view
  by median as `plan:` reads a place.
- `stump`, `kneaded`, `plastic`: see the medium model.

**Helpers emitting one kind of record** is how `block_in` already works: every pass is
`self.stroke(...)` inside `with self._one_call("block_in", place, mass=_mass_params
(place, value))` (`session.py:1106-1125`), which stamps `via`, `boxed` and the
stream state on every record and the place and value on the first. `thumbnail()` and
the `boxes:` line are drawn from `params["mass"]` (`:2794`, `_laid_masses`), so `tone`
and `hatch` should pass `mass=` the same way or they will not appear in the notan.

**Look and measure.**

- `look(values=True)` is `Canvas.values()`, the luminance of `composite(sketch=True)`,
  so a sibling channel composited there is in the greyscale view with no change to
  `look`. Making it the default is a `Session`-level default.
- `look(tooth=True)` is a new render. `look()`'s keywords are `render_look`'s
  signature (`look.py:121-134`) and `look_image` pops them by name; a new flag goes
  into both, into the CLI `look` parser and into the MCP `look` tool. What it shows
  depends on the `filled` decision above.
- `compare({place: value})` reads `_value_view` = `to_srgb8(impasto=False)`
  (`session.py:4917-4924`), so it sees whatever `composite` sees. `compare()`'s
  *unreachable* split reads the palette floor and has to read the grade box.
- The standing warnings: see `report()` above, and the `LESSONS.md` rule that a check
  is written after it has been seen to fire.

**CLI.** `easel new` builds `Session(w, h, texture=, ground=, seed=, timelapse=,
out_dir=, budget=)` (`cli.py:534-543`) and writes a `prelude.py` stub holding
`s.plan(...)`. `--paper` is `--texture`. `easel pencils` has a precedent in `easel
brushes` (prints the box) and `scripts/make_brush_sampler.py` (draws it); the CLI
prints and the script draws. `easel film` is a new subcommand beside `timelapse`,
whose `--scale` is the long side in pixels and GIF-only (`cli.py:249-256`).

**MCP.** Twenty-one tools; `run` takes `script` as text; `film` is a new tool and
`new` needs the medium; both reach `server.json`, `mcpb/manifest.json`,
`tests/test_mcp.py` and `tests/test_server_json.py`.

**DRAFTSMAN.md.** The machinery that holds `PAINTER.md` is specific to it:
`docs.DOCUMENTS` maps six names to six files; `FRONT_PAGE_WORDS = 6_700` and
`CARD_WORDS = 1_400` are single constants read for the one file (`docs.py:55-109`);
`tests/test_guide.py` asserts `guide.read("guide")` is under budget, that the card
`## The first hour` is under its own, and that the wheel's `force-include` table in
`pyproject.toml` equals `DOCUMENTS` exactly; `scripts/check_guide_blocks.py` runs
every python block of `("PAINTER.md", "PAINTING.md", "RECIPES.md")` and every demo;
`scripts/check_guide_overlap.py` (run from `test_guide.py`) says when a sentence lives
in two files. A seventh document needs its own `DOCUMENTS` entry, its own budget
constant and test, a `force-include` line, a place in the block checker, and a
decision on the overlap check, which will flag every sentence it shares with
`PAINTER.md`. *Same structure as PAINTER.md* means, today: the card, *Getting
started*, seven workflow steps, *What you are bad at*, ten exercises (not nine), a
closing checklist, *Sign it*, and *Working from a shell*. `PAINTER.md` is at 6,626
words against 6,700, so nothing can be added to it for the graphite medium without
something leaving in the same commit.

The subject leak: `SPEC.md` names the test subject and sits in the repository root.
`LESSONS.md`, *A worked example is an instruction*: a noun in any file the painter
reads is the picture it paints, the grep for the references' nouns has caught its own
author seven times, and the decide-then-read protocol is what dissolves it. Either the
agent chooses its subject before it opens the checkout and the choice is recorded with
the run, or the subject is not written anywhere it can read, `SPEC.md` and
`DRAFTSMAN.md` included.

---

## Frame capture and time-lapse

**The rebuild is exact for the reasons given, plus one.** Per-index seeding covers
marks; masses draw their wander from the running stream, and `params["rng"]` on every
record is what lets `replay()` and `undo()` put the stream back (`CALIBRATION.md`, *The
log, undo, and the stream*: a 1.06% drift until it did). The determinism caveat
matches `LESSONS.md` (729 of 786,432 pixels by one level between two numpy builds) and
the golden tolerance.

**Looks are not in the log, and cannot be.** `look()` writes `out_dir/look_NNN.png`
numbered from what is in the directory (`_next_free_path`, `session.py:2586-2601`),
rehearsals `rehearse_NNN.png`, and `preview`, `compare` and `thumbnail` their own
runs; that half of the capture exists. What does not exist is the link to the log
index: `"look"` is listed in `UNPAINTED_KINDS` but nothing creates a record of that
kind (grep of `session.py` and `history.py`), and `REFERENCE.md`, *What the tool will
tell you*, says why notices, reports and the plan live beside `history.records` and
never in it: *the log indexes the random stream; anything new that took an index
would repaint every painting made before it*. Capture is therefore a sidecar keyed by
`len(history.records)` at the moment of the look, as `PassReport.at` is, saved in the
`.easel` meta the way `reports` and `plan` are (read with `.get`, so an older build
opens the file), and never a record. The pass criterion *a `look()` in the log at least
every 15 strokes* is read off that sidecar or off `reports()`, not off the log.

**Rehearsals.** A rehearsal is a trial session seeded as the painting's next records
(`_trial_session`, `:3381-3462`), and `easel run --rehearse` keeps a `PassReport
(scripts, mode, at, text)` on the painting even though it commits nothing else
(`notices.py:146-175`, `Session._keep_report`). *Whether it was then committed* is a
later report at the same `at` with the committed mode: derivable from what is already
saved, not a new field.

**Pass scripts.** `easel run` copies nothing; the numbered `pNN_name.py` beside a
`prelude.py` is the painters' own convention (`paintings/Claude/uktarl_krannoc/`), and
`PassReport.scripts` holds the names only. The MCP `run` tool receives the script as
**text** (`script=`) and writes it nowhere; the dearest-calls line names it
`<script>:12`. Capturing a pass means saving that text at run time, on both the CLI
and the server path. `s.plan(why=)` is already in the saved `plan` and quoted back by
`checklist()`.

**Film export.** `--fps`, `--every` and `--scale` exist on `timelapse`; MP4 does not,
and the only dependencies are numpy and Pillow. The extras pattern (`mixbox`, `mcp`,
`dev` in `pyproject.toml`) is the place for `film = ["imageio-ffmpeg"]`, with the same
clean-skip test the MCP extra has. The frame source has to be a walk over the records
(see `easel timelapse` above), not `History._frames`.

**Progressive stroke motion needs a hook in the new stroke function, not partial
replay.** `paint_stroke` and `draw_pencil` draw every dab's randomness up front
(`_wander`, `stroke.py:372-373`, `:600-602`) and then stamp in a loop with no callback
(`:411-517`, `:607-624`). Replaying a record *up to dab k* would rerun the stroke per
frame and stamp its first dabs again. A per-dab callback or `upto_dab=` on
`draw_graphite` is the only clean form, and it is new code either way; `paint_stroke`
stays as it is.

**Held looks and captions.** `render_look(canvas, grid=True, values=...)` can be
called on the rebuilt session at any record for a held frame. A record carries
`kind`, `brush`, `pressure`, `note` and `params` for a caption; the pass name comes from
the sidecar, not the record.

**Viewer.** Nothing exists beyond `contact_sheet`. New.

---

## Test drawing

- *A `look()` in the log*: not in the log; see above.
- *`compare()` against the agent's own value plan*: `compare(s.plan())` and
  `compare({place: value})` read places by median through `compare_plan`
  (`REFERENCE.md`, *What the plan changes*), on the composited view, in the engine's
  convention. The criterion is fine once the convention is flipped.
- *Darkest value at or above 0.80*: inverted, and unreachable through `sketch`
  (0.229, above). Reachable only through a channel with its own composite.
- *`replay()` matches the export within one level*: `scripts/probe_cohort_session.py`
  already rebuilds a filed painting from its scripts and counts pixels off
  (`NOTES-step1.md`: 429 records identical, 0 pixels off, 47 s). `LESSONS.md`: *byte
  for byte is a claim about one machine; to the stroke is the one that travels*.
- *MCP server launched with `--dir drawings/`*: exists.
- *Artefacts under `drawings/<name>/`*: `tests/test_paintings.py` scans `paintings/`
  only, and a directory there that holds any of `painting.png`, `painting.gif`,
  `NOTES.md` or `prelude.py` owes all three linked files and a section in
  `PAINTINGS.md`. A `drawings/` tree is outside that test; a drawing filed under
  `paintings/` has to meet it. No filed painting ships its `.easel` file (none under
  `paintings/`); the rebuild is from the scripts.
- *The first run calibrates the grade table*: `LESSONS.md`, *Never change the engine
  while a measurement is running* and *A run measures the guide, not the engine*. The
  grade table is calibrated on samplers and value scales in step 2; the first drawing
  is a shakedown of the guide after which the engine may change; the second is the
  measurement. Keep both, label which is which, and record what the agent read
  (*a painter told where to start reads what it likes, so record what it read*).
- *`NOTES.md` names what went wrong*: `LESSONS.md`, *Check the painters' numbers*:
  ninety-four claims re-measured, twenty-one did not survive, and the ones most
  likely wrong are observed failures with a reasoned cause. Ask the agent to label
  each finding measured or reasoned, and re-measure the measured ones off the PNG.
- The agent must be able to see images (`LESSONS.md`, the cohort's one painter that
  could not; `easel/__init__.py`'s docstring says it as a requirement).

---

## Work plan

**Step 1** is answered by this review. Where things live: `canvas.py` (`Canvas.rub`,
`stamp`, `composite`, `tooth_ceiling`, `_GRAPHITE_BAND`, `snapshot`/`restore`,
`trial_copy`), `stroke.py` (`draw_pencil`, `paint_stroke`, `_dabs`, `pressure_curve`,
`press_width`), `brush.py` (`tip_mask`/`_tip`, `TIPS`, `BRUSHES`), `texture.py`
(`TEXTURES`, `make_texture`), `history.py` (`StrokeRecord`, `UNPAINTED_KINDS`,
`MAX_FRAMES`, `save_gif`), `session.py` (`pencil`, `erase`, `sketch_lines`, `stroke`,
`block_in`, `_block_in_paths`, `_one_call`, `undo`, `replay`, `_replay_records`,
`save`, `load`, `_trial_session`, `_plan_specs`, `_lay`, `_canvas_lines`,
`_pass_findings`), `notices.py` (`NOTICES`, `REBUILDS`, `PassReport`), `look.py`
(`render_look`), `cli.py` (`timelapse`, `new`, `_cmd_run`), `mcp_server.py` (the
tools, `--dir`).

**Step 2**, as a sibling, is this list of touch points, none of which moves a golden
except the two the paper adds: a second plane and its flag in `Canvas.__init__`,
`snapshot`, `restore`, `trial_copy` and `composite`; a deposit method beside `rub`;
`draw_graphite` in `stroke.py`; a charged record kind, a verb that snapshots **by
box** and calls `_auto_frame()`, and a branch in `_replay_records`; the new fields in
`__init__`, `load`, `_trial_session`, `replay` and `save`; `cartridge` in
`texture.py` and `build_surface`; a pencil sampler script and golden case; rows in
`REFERENCE.md` for the texture, the kind in the budget table, and the plan grammar.
`_EASEL_FORMAT` goes to 5 only if the new array is required on load; optional, read
the way `sketch` is, it stays at 4.

**Step 3** reuses `_block_in_paths`, `_shape_paths`, `_angled_paths`,
`_canvas_order_pressure`, `_one_call`, `_mass_params` and `_clip_cover`, and registers
one plan kind in `_plan_specs`, `_lay`, `_plan_price`, `_preview_entry`,
`PLAN_ACCEPTS` and `tests/test_reference.py`'s `PLAN_KIND_KEYS`. Each helper's golden
is a new case in `golden_cases.py`.

**Step 4** is independent of 2 and 3 as the spec says, with one correction: an
upstream painting's log does not exist as a file. Rebuild one from its scripts first
(`probe_cohort_session.py` does this, 47 s for the longest), then walk its records.
`MAX_FRAMES` is the thing to design around, not the thing to extend.

**Step 5**: each report rule is a `NOTICES` entry, a `REFERENCE.md` row and a
`CALIBRATION.md` heading held by `test_notices.py`, and is written only after the
first drawing's log shows it firing. `DRAFTSMAN.md` needs the machinery under *API
additions*. A rule that enters the guide leaves nothing else, so the word budget is
set before the file is written, not after.

**Step 6**: the subject's secrecy and the `paintings/` test, above.

**Step 7**: `CHANGELOG.md`'s own header rule, held by `tests/test_version.py`: nothing
says *shipped* until the tag exists, and `pyproject.toml` is held to the newest
`## [x.y.z]` section, so a fork that adds a section has bumped its version. The
graphite work is a minor release's worth of behaviour; until it is cut it goes under
*Unreleased*.

---

## Risks and open questions

- *Pin to a tag*: `v0.8.0`'s `src/` is `main`'s `src/` today, so forking `main` at
  `1ed1f69` and forking the tag are the same engine. `PLAN-0.9.0.md` names where the
  next round lands: `_clip_cover`, `_as_outlines`, `_pass_findings`,
  `_block_in_paths` with `_check_default_direction`, and `checklist.values_line`. Two
  of those, `_pass_findings` and `values_line`, are exactly where graphite report
  rules go, so that is where forward merges will conflict; the verbs, the channel and
  `stroke.py` will merge clean.
- *Whether `sketch` can be promoted*: settled by the nine couplings under *Canvas*. It
  cannot, without moving the `drawing` golden and the contract `LESSONS.md` lists as
  load-bearing. **Sibling.**
- *No `cover()`*: true, and the erasers the spec proposes lift partially by design, so
  the guide's answer is the order of work, which the spec already states.
- *Value-only medium*: the mitigation exists in part: `look(values=True)` is the
  engine's own view and `compare()` reads it; `look(tooth=True)` is new.
- *`imageio-ffmpeg` as an extra*: matches the existing pattern.
- *Whether the author is already on it*: `PLAN-0.9.0.md`'s workstreams do not touch
  the pencil; the only mention is a request for `--no-sketch` on `easel run
  --rehearse`.

---

## What LESSONS.md constrains

Each of these binds a step above; the step is named.

1. **Add capability beside the old path, never through it.** The sibling channel, the
   new record kinds, and `draw_graphite` beside `draw_pencil` (steps 2, 3). The test of
   compliance is that every stored golden hash is unchanged after step 2 except
   `sampler` and the new cases.
2. **Graphite accumulates as a maximum, not a sum.** The deposit model (medium model).
3. **A golden failing is an instruction to look, not to regenerate.** `make_golden.py`
   only after both images have been opened (steps 2, 3). `drawing` must not move.
4. **Look at the sampler after any engine change, then draw something.** The sampler
   is isolated strokes at full load and missed a gate that silkscreened every
   accumulated mass; keep a throwaway script of hatching over hatching (step 2).
5. **Assert on the canvas, not on the return value.** Diff the graphite plane either
   side of a mark in every engine test (steps 2, 3).
6. **Anything a mask is computed from has to be in its cache key, quantised.** A grade
   or tip parameter that reaches `tip_mask` goes into `_tip`'s key (step 2).
7. **A canvas-mutating method pushes its snapshot immediately before it touches the
   canvas, in the same method.** Every graphite verb; grep for `push_snapshot` first
   (steps 2, 3).
8. **A record that carries a place carries the whole place.** `stump`, `kneaded`,
   `plastic` as region operations (step 3).
9. **A tuned constant encodes a ratio.** Write the invariant each grade number holds
   (step 2, `CALIBRATION.md`).
10. **Normalised space is not isotropic, and `size` is of the long side.** Hatch
    spacing and angle on a 4:3 canvas (step 3).
11. **Nothing new takes a log index unless it is a mark.** Looks, rehearsals and pass
    scripts are captured beside the log (step 4).
12. **Seeding is per record index, and free records shift it.** A graphite drawing's
    `pencil()` envelope moves the seed of every mark after it; replay stays exact
    because the log carries the records (step 4).
13. **A check earns its line by firing on a real pass; measure the condition before
    writing the rule; a warning that cannot fire is worse than none.** The seven
    proposed report rules are candidates until the first drawing's log is measured
    (step 5).
14. **A default is worth more than a warning: measure the curve, then move the
    default, then warn about the far end.** The grade table and the eraser strengths
    are defaults before they are warnings (steps 2, 5).
15. **A new finding never adds a paragraph to the guide; one home per rule; the budget
    is enforced by a test.** `DRAFTSMAN.md` enters `DOCUMENTS`, the budget test, the
    block checker and the overlap check on the day it is written (step 5).
16. **A worked example is an instruction; a list is a ranked list; grep the guide for
    the references' nouns.** No subject noun in `DRAFTSMAN.md`; the test subject in
    no file the agent reads; `SPEC.md` is such a file today (steps 5, 6).
17. **A guide change is a hypothesis until a fresh session paints against it.** The
    second drawing is the only measurement of `DRAFTSMAN.md` (step 6).
18. **Never change the engine while a measurement is running.** Grades are calibrated
    on samplers before run 1; the engine may change between the runs and not during
    one; both runs are kept and labelled (steps 2, 6).
19. **Check the painters' numbers; ask for measured versus reasoned.** The agent's
    `NOTES.md` is re-measured off its PNG before anything is built on it (step 6).
20. **Record what the painter read, and whether it used the index.** Part of each
    run's record (step 6).
21. **Do not write down that something shipped until the thing that ships it has
    run.** `CHANGELOG.md` (step 7).
22. **Vision is a requirement.** The drawing agent must take images back (step 6).

---

## Where the spec says promotion and the code says sibling

1. The darkest mark `sketch` can make is value 0.229, from one constant colour in
   `composite()`; the spec needs black, and changing the composite moves every
   underdrawing ever painted.
2. `stamp()` buries `sketch` by what landed; a channel that is the picture cannot be
   buried by paint, and the burial is listed as load-bearing.
3. `pencil` is free in `UNPAINTED_KINDS`, read by the budget, the report and a
   reference test; a charged mark is a different kind, not a flipped flag.
4. `pencil` records carry `width`, `smooth` and `rng`; the report's rules read brush
   fields a stroke record carries and a pencil record does not.
5. `report()` reads `values:` and `edges:` without `sketch` on purpose and prints
   `pencil:` as the remainder; the picture's values must be read with the graphite in.
6. `ground_showing` treats `sketch` as ground by design; a graphite drawing's paper
   is paper never touched.
7. `look(sketch=False)` and `export(sketch=False)` hide the channel together with
   the `guide()` overlay; the drawing itself cannot sit behind that flag.
8. The `drawing` golden and `tests/test_precision.py:70-245` are the channel's
   contract and must not move.
9. `Session.sketch()` is already a method, the machine-laid outline, and `has_sketch`
   is already a saved key; the new channel needs a name that is not `sketch`.

What a sibling leaves available to a graphite session for free: `pencil()` as a
costless underdrawing that the graphite can be laid over, `erase()` for it,
`sketch_lines()` to sweep a hatch along a drawn line, and `guide()` for scaffolding
that never reaches the export.
