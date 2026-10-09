# A hen's egg in a shallow bowl, drawn a third time

**Run 3 of `SPEC.md`'s test drawing: the guide's candidates, measured.** The same subject
as `drawings/egg_in_bowl/` (run 1, the shakedown) and `drawings/egg_in_bowl_2/` (run 2,
the one that counts), a third seed, drawn by a fresh session against `DRAFTSMAN.md` as
it stands on 2026-10-09, the working tree after `cf116a0`. What changed in the guide and
in the check between run 2 and this run is listed under the re-measurement at the end,
so that the agent's own write-up is not steered by it. Run 2 was the only measurement
of the guide as first written; this run is the only measurement of what was changed
from it (`LESSONS.md`: a guide change is a hypothesis until a fresh session draws
against it).

## The subject, chosen before the agent saw anything

Written here by the person running the round, before the first stroke, as the protocol
asks. The same words as runs 1 and 2, so that the three drawings differ only in the seed
and in what the agent had to read:

> **A single hen's egg in a shallow white bowl on a plain wooden table, lit from a
> window to the upper left, out of frame.** Three or four value masses: the lit side of
> the egg and the bowl's lit rim, the egg's shadow side, the bowl's interior shadow with
> the egg's cast shadow in it, and the table. One hard edge: the bowl's rim against the
> table. One lost edge: the egg's shadow side into the bowl's shadow behind it.

The drawing agent is told this subject in its brief and nothing else about the picture.
It is not the spec's example subject.

## Setup

- `drawing.easel`: 1024x768, `cartridge`, white, **seed 13**, budget 400,
  `medium="graphite"`, `capture=True`, `out_dir` `out/` -- made with `easel new` from
  this folder.
- The agent works through the shell (`easel run`, `easel look`), as runs 1 and 2 did,
  with `py -3.14 -m easel` and `PYTHONPATH` on the checkout's `src/`, because the
  installed wheel is 0.8.0 and has no graphite. The passes are its own numbered scripts
  beside this file.
- A fresh session: the agent has not seen this repository, the spec, the review or the
  earlier runs. It is given `DRAFTSMAN.md` as its guide, the paths of the documents the
  guide points at, and told that what it reads is part of the record. It is told not to
  open `drawings/egg_in_bowl/`, `drawings/egg_in_bowl_2/`, `SPEC.md`, `SPEC-REVIEW.md`
  or `PLAN-0.9.0.md`.

## What the agent read, what it did, what went wrong

*Written by the agent at the end of its run, below this line; re-measured by the person
running the round after it.*

---

## The agent's write-up

**Strokes spent: 140 of 400**, plus two signature ticks that were not charged. Passes in
order, with what each cost (all measured off the budget line `easel run` printed):

| Pass | Script | Cost | Rehearsals before commit | Looks inside the committed run |
|---|---|---|---|---|
| 0 | `p00_envelope.py` | 0 (pencil) | - (run three times, the envelope moved twice) | 2 looks, 1 thumbnail |
| 1 | `p01_table.py` | 61 | 3 | 8 looks, 2 compares |
| 2 | `p02_bowl.py` | 31 | 3 (one raised before laying anything) | 7 looks, 1 compare |
| 3 | `p03_egg.py` | 14 | 2, the second together with pass 4 | 5 looks, 1 compare |
| 4 | `p04_shadows.py` | 11 | 2 (one with pass 3) | 5 looks, 1 compare |
| 5 | `p05_edges.py` | 9 | 3 (two with pass 6) | 4 looks, 1 compare |
| 6 | `p06_darks.py` | 6 | 3 (two with pass 5) | 4 looks, 1 compare |
| 7 | `p07_repair.py` | 8 | 1 | 3 looks, 1 compare |
| 8 | `p08_sign.py` | 0 (2 free) | 0 | 1 look |

Fifteen rehearsal sheets were written in all (`out/rehearse_001..015.png`, counted);
39 looks, 8 compares and one thumbnail were taken inside the committed passes (counted
from the scripts), and every rehearsal ran the same looks on its copy. I opened about
fifty-five of those PNGs with my own eyes, plus the fourteen exercise images.

**The final check** (`check_final.txt`, verbatim):

```
checklist for this painting -- 140 of 400 marks spent
  plan: 9 of 10 places inside 0.10; egg_cast_seen +0.17 (20% of it darker and 26% lighter by more than 0.15)
  lightest: egg_lit reads 0.96 as a place, 0.96 at its brightest twentieth, the lightest of the 10 places planned; 98% of it paper never touched
  subject: 23 of 140 marks so far (16%), against 25% planned -- behind, if the subject is finished
  values: 0.37-0.89 of a box that reaches 0.04-0.96, clusters at 0.46, 0.62, 0.84; a clear light, mid and dark
  edges: 32% of edges are under 2.5 px wide, median 3.7 px
  paper: 2.46% of the canvas is paper never touched
  pencil: the envelope still shows over 1.46% of the canvas -- export(sketch=False) leaves it out
  boxes: no masses laid yet
  darks: the darkest half-percentile reads 0.15, 0.85 of the way from paper to black
  unspent: 260 of 400 unspent (65%) -- name the weakest passage and spend them there
```

**The longest run with no look between marks:** the check printed no such line, in any
committed pass or at the close, so none was over 15. By my own count of the committed
scripts the longest is **13**, the far plane's thirteen diagonal rows in pass 1 between
the look after the level rows and the look after them. The first rehearsal of pass 1
was flagged at **19** (the six level rows and thirteen diagonals with no look between);
I put a look between them before committing.

## What I read, and how far

- **`DRAFTSMAN.md`**: whole, every line, first, before anything else. Its own table of
  files was the only index I used from it. I kept it open and re-read *The workflow* 2,
  3, 6 and 7 and *Sign it* while drawing.
- **`REFERENCE.md`**: I grepped its headings (`^#+ `) as an index, then read in full:
  *Units* and *What counts against the budget* (lines 16-69), *The verbs* and *Which
  verb takes which hold* (71-130), *Places* and *Shapes* (232-349), *The graphite
  medium* (405-508), *Looking, planning, measuring* with *What the plan changes*
  (510-699), and *The session, and the shell* (787-943). Not read: *The arguments that
  mean something particular*, *The brushes*, *Pressure*, *Colour*, *What the tool will
  tell you*, *Or through the MCP server*.
- **`CALIBRATION.md`**: headings grepped as an index; read *The graphite medium*, *The
  stump and the erasers* and *The check, measured on the first drawing* (302-489) in
  full. *The plan a painter declares* reached me through `easel explain plan-pairs`,
  which printed it whole.
- `easel --help` and `easel explain plan-pairs`. No source, no tests, nothing under
  `drawings/` other than my own folder.

## The exercises

All nine run as standalone scripts (each makes its own `Session`, so they could not go
through `easel run drawing.easel` without rebinding `s`), looks under `ex_out/`.

1. **The box of pencils** (18 marks): matched. `4H` at `0.3` is nearly nothing, every
   grade at `0.3` is a field of white points, `6B` at `1.0` near black; every side
   stroke ends in a block at both ends. The check fired *stack of bars* on the sheet
   and *18 marks with no look*, which the exercise invites.
2. **One line, six pressures**: matched. On the point the width swells with pressure;
   on the side only the darkness and the tooth change.
3. **A plane, laid and read**: half matched. The plan line said *inside 0.10* before and
   after the stump without printing the number, so I could not see the median move from
   that line; the `values:` clusters moved `0.52` to `0.55` (measured). The rows read as
   rows with speckle between them, and the `2H` diagonals ran far outside `B2:G7` as
   written. `s.sample(plane)` printed an RGB triple, `[0.92 0.905 0.87]`, not a value.
4. **A hard grade leant on, a soft grade held lightly**: matched exactly: `HB` at `0.5`
   a field of white points, `2H` at `1.0` a tone with a few holes. `compare()` read them
   `0.51` and `0.60` (measured).
5. **Across a shape, and along it**: matched. The hatched oval ends in a staircase; the
   arcs end on their own fades, but the five arcs read as five bands with lighter seams,
   and the "along" version only fills a crescent, not the oval.
6. **What the stump does to the number**: matched and then some. The plan line went from
   *inside 0.10* to `D4 +0.15` after one stump at full strength (measured); the stump
   left a speckled margin outside the cell where the tone overhung it.
7. **Three edges**: matched for where the eye lands (the hard edge). Not said by the
   guide: this exercise costs **164 marks** (measured: `tone()` on six panels), and the
   lost edge's stump across the join leaves a visible pale smear on a speckled tone.
8. **The eraser and its ghost**: matched. `kneaded` at `0.5` took the strip and the `6B`
   line to half; `plastic` took most and left the line's ghost.
9. **Draw, rehearse, draw**: matched. The hatch at 20 degrees across the triangle ends
   in a sawtooth on every side, which is step 3's warning in miniature.

## The passes

**Pass 0, the envelope (free).** I decided the light is upper left and a little behind
the subject, so the bowl's interior shadow is a crescent along its far and right wall
and the egg's shadow side (lower right) can melt into it; the egg lies with its pointy
end up toward the light; the bowl's cast shadow falls lower right. First envelope: the
egg's top poked above the far lip, the cast shadow ran off the sheet, and my crescent
was built from the wrong arcs (thick at the right, not the far wall). I moved the bowl
up, shrank the egg, and wrote a proper `crescent()` from the two ellipses' crossing
points. The plan registered ten places; `plan-pairs` named `int_shade / egg_shade 0.00
apart (touch)`, which is the lost edge, meant, and `egg_cast_seen / bowl_cast_seen 0.04
apart (touch)`, which was a bug in my cast polygon (it ran inside the bowl) and went
away once I cut it round the bowl.

**Pass 1, the table (61).** Level rows at `width=0.07` and diagonals at 25 degrees on
screen, the far plane `2H`, the near plane `HB`, every row cut round the bowl grown by
half a stroke, one full stump per plane. Rehearsal 1 read `table_far +0.02`, `table_near
+0.01` (measured) but showed a pale band and a dark unstumped strip at y 0.37-0.40 where
the near stump started below the first near row, and a straight horizontal seam between
0.72 and 0.60 that read as a horizon; the check also flagged 19 marks with no look.
Rehearsal 2, with two `2H` rows as a step, still showed the seam. Rehearsal 3 gave every
row's pressure as a function of `(x, y)`, rising toward the near edge, and the seam
went. Committed at `table_far -0.05` (reads 0.65), `table_near -0.01` (0.53), `lightest
100% paper never touched`; check: nothing to report.

**Pass 2, the bowl (31).** The lit interior as `2H` arcs of the inner ellipse scaled
inward plus two level strokes on the flat of the floor; the crescent as arcs whose
reach shrinks with the crescent's own thickness; the outer wall as five `HB` arcs
ramped light-left to dark-right; one faint `2H` on the lip's right. Rehearsal 1: `HB`
at `0.92` under a bell list read the crescent at **0.67** against 0.46 planned
(measured, `int_shade +0.21`), 9% of the egg's light had been touched, and a dark
speckled patch sat where the innermost lit arcs piled up left of the egg. Rehearsal 2
raised `TypeError ... complex`: my own `bell()` took a tiny negative sine to a
fractional power. Rehearsal 3 (crescent in `2B` at `0.78`, egg margin widened to 14-18
px, small arcs dropped): `int_shade +0.01`, `int_lit +0.01`, `wall +0.01`, light 100%
paper, but the crescent's arcs ended in a staircase of blocks down the right wall.
Rehearsal 4 with the ends faded to `0.12`: staircase gone, `int_shade +0.08`.
Committed so. Check: nothing to report; `paper: 5.74%`.

**Pass 3, the egg (14).** Rehearsal 1 laid four cross-contour arcs over the outer 40%
of the radius: the egg read as a white disc with a dark C-shaped ring, and the lost
edge was a **white halo**, because the crescent had been cut 14-18 px short of the egg
and the egg's shade stopped at its outline, so the stump across the join had nothing to
spread. Rebuilt as eight arcs at 12 px grading from `HB` leant on at the core out to
`2H` half-tones, one stump over the shade, the `2B` core after the stump, and two short
`2B` strokes along the outline outside the egg to fill the crescent's gap before the
join stump. Rehearsal 2: `egg_shade +0.11`; two middle arcs leant to `1.0` and the core
to `0.8` gave `+0.07` (rehearsed with pass 4). Committed at `egg_shade +0.07`,
`lightest ... 98% of it paper never touched` (the terminator stump's width crossed the
light's inner boundary: measured by that line, 100% to 98%).

**Pass 4, the shadows (11).** Rehearsal 1 (with pass 3): the egg's cast shadow was a
detached dark lozenge, held off the egg by the same 14-18 px margin. Cut 4 px from the
egg instead and the ellipse widened to run under it: attached, reads as a shadow.
`bowl_cast_seen +0.05`. `egg_cast_seen` read `+0.28` with a third of it lighter by more
than 0.15; the heat map showed the **place** was wrong, a self-crossing polygon that
took in lit floor. I redrew it twice (closing on the ellipse's major axis the second
time) and it ends at `+0.17 (26% lighter)`; the laid shadow is right to the eye and
the place still is not, and I stopped there. Check after commit: nothing to report.

**Pass 5, the edges (9).** Two bands outside the bowl's silhouette in the table's own
value and grade (36 px at 20 px out, 50 px at 44 px out), both arcs run past the sides
so they overlap where rim meets wall, cut into runs round the bowl's cast shadow, one
stump each; then the hard edge, a `2H` side stroke 13 px wide along the rim's top arc,
its centre 2 px outside the rim. Rehearsal 1 left a lighter ring and two bare "wings"
at the bowl's sides (I had computed the side pieces and never laid them, and the first
band alone did not reach the rows' ragged ends). Rehearsal 2 and 3 were clean.
Committed; `edges:` went from 20% to 29% under 2.5 px (measured). A probe afterwards
(`probe_halo.py`, `--count`) read the ring 40-90 px out at the same median as the table
beside it, far 0.60 against 0.60 and near 0.53 against 0.55 (measured), so the ring I
kept seeing was texture, smooth against mottled, not value.

**Pass 6, the darks (6).** Three `6B` strokes under the bowl's lower-right wall, a `4B`
contact under the egg, a `4B` core in the egg's cast, an `HB` contact under the bowl's
lower left, none stumped. Rehearsal 1: three separate stripes with a blunt square end,
and the contact a heavy black outline. Rehearsal 2 faded the ends: still stripes.
Rehearsal 3 at 41 px wide and 14 px apart: one dark with faint stripes. Committed:
`bowl_cast_core +0.04` (reads 0.22), `darks: 0.15, 0.85 of the way` (measured, the
criterion met).

**Pass 7, the apology passage (8).** Without the envelope the egg's lit side dissolved
into the lit floor and its left end had no edge at all. One `2H` half-tone inside the
egg's lower-left outline and two outside it as the floor's occlusion, all fading to
nothing; then the second stump the guide allows over a large plane's mottle, in five
rectangles that avoid the bowl and the darks. Rehearsed once: `table_far -0.04`,
everything else unchanged, the egg's left end found. Committed. **Pass 8**: two `HB`
point ticks at bottom right, free under `note="signature"`, and the export.

## What went wrong

Each claim is tagged (measured) with its number and method, or (reasoned).

- **Pass 1 was flagged for 19 marks without a look** in its first rehearsal (measured:
  the check's line). Fixed before paying.
- **I repaired the egg once and the darks twice before committing** (rehearsal counts
  above). The guide's rule is about a passage that has failed twice *after* being paid
  for; mine failed in rehearsal, which is what the rehearsal is for. No committed
  passage was repaired, except that pass 7 went back over the egg's left end on purpose.
- **Stumps over the table planes covered the bowl and the egg** (reasoned from the
  polygons: `near_all` in pass 1 is the whole near rectangle). The channel did not move
  there, the light stayed `100% paper never touched` through passes 1 and 2
  (measured), so the record says the stump covered the light and the drawing says it
  did not; CALIBRATION.md warns of exactly this.
- **The egg's light lost 2% of its paper** to the terminator stump in pass 3 (measured:
  the `lightest:` line, 100% to 98%). I did not lift it back; a lift would have been
  a ghost.
- **`egg_cast_seen` ends `+0.17`**, 26% of it lighter by more than 0.15 (measured). My
  place polygon, three times drawn, still takes in a wedge of lit floor between the
  egg's right end and the shadow's. The laid shadow is right to the eye; the number is
  wrong because the place is.
- **`subject: 16% against 25% planned`**: my own number, written before I knew what a
  drawing laid this way costs; the egg, its lost edge and its cast shadow took 23 of
  140 marks (measured). The guide's card example of `subject_share=0.45` was my
  starting point and it is nowhere near what this method spends on a subject.
- **`boxes: no masses laid yet`**: a drawing lays no mass verb, so the line can never
  say anything in this medium (reasoned). I do not understand why it is printed for one.
- **The far plane's mottle**: `2H` at `0.5` to `0.8` leaves the tooth loud and one stump
  does not close it (seen at full size in every look); the second stump in pass 7
  helped and moved `table_far` from `-0.05` to `-0.04` (measured).
- **A side stroke's end block**: a run cut round the egg with a 6-8 px margin at
  `width=0.02` touched the egg's light over 9% of it; at 14-18 px, 0% (measured: the
  `lightest:` line in rehearsals 1 and 3 of pass 2). The guide says a stroke ends in a
  block but not that the block runs on past the last point, nor by how much.
- **`HB` under a bell-shaped pressure list is not `HB` at its peak**: the crescent in
  `HB` peaking at `0.92` read 0.67; in `2B` peaking at `0.78` it read 0.47 (measured,
  `int_shade` on rehearsals 1 and 3 of pass 2). The guide's grade-and-pressure numbers
  are for a flat list, and it says so nowhere.
- **Arcs scaled inward on a 4:1 ellipse** are 10 px apart at the top and 30 px at the
  ends for the same step in `k` (reasoned from the radii; seen in pass 2's arcs), so a
  shallow bowl's interior cannot be laid evenly that way; I lived with it and let the
  stump close the ends.
- **`bell()` crashed a rehearsal** with a complex number: my helper, not the engine,
  but the engine's error named only `pressure_curve`, and it took a moment to see the
  cause (a sine a hair below zero to a fractional power).
- **`plan-pairs` "touch"** is not defined in the guide; `explain plan-pairs` says it is
  within `0.01` of the long side, inside four screens of paint text.
- **The guide and the calibration disagree**: DRAFTSMAN.md says an even tone is a hard
  grade leant on; CALIBRATION.md's bullet under the grade table says *the grade for a
  light tone is a soft one at low pressure, not a hard one leant on*. Exercise 4 sides
  with the guide (measured, the two cells).
- **`sample()` is not a mean of values**: it printed an RGB triple in exercise 3, and
  the guide calls it *a mean of whatever is in it* as if it were a number.
- **The closing check's longest-run line is silent under 15**, so the guide's promise
  that the check says *the longest run of marks laid with no look between them* only
  holds when there is a finding; the real longest run (13 here) is not reported.
- **Exercise 7 costs 164 marks** (measured) and the guide says the exercises *take a
  minute each*; in a session with a budget that would be a third of it.
- **The guide is silent** on: how to cut a stroke round a thing standing in the passage
  (I wrote `runs_outside()`); that a pressure list may be one number per point (it
  works); that `erase()` clears the pencil envelope (REFERENCE's verb table says so,
  the guide does not); what a crescent's arcs should do at their ends; and that
  `--count` is the way to run a probe that lays nothing.

## Candidate rules

1. *Add to step 2 / section 3:* "A side stroke's end block runs on past its last point by
   half its width, so a run cut round a thing standing in the passage is cut at the thing
   grown by half the stroke's width plus a few pixels." Evidence: the egg's light 91%
   paper at a 6-8 px margin, 100% at 14-18 px, width 0.02 (measured, pass 2).
2. *Add to Getting started:* "The pressures quoted here are for a flat list; a list that
   falls to its ends reads a grade lighter, so a passage laid with faded ends wants the
   next softer grade." Evidence: HB peak 0.92 bell read 0.67, 2B peak 0.78 read 0.47 for
   the same crescent (measured).
3. *Add to section 3:* "Arcs whose reach shrinks with a crescent end in steps unless the
   pressure falls to near nothing over their last thirty pixels." Evidence: rehearsals
   005 and 006 of pass 2, ends 0.45 against 0.12 (seen).
4. *Add to section 6:* "A lost edge needs the two tones to actually butt: the band beside
   the thing, laid along its outline in the neighbour's value, is how the cut margin is
   closed before the stump goes across." Evidence: the white halo in pass 3's first
   rehearsal (seen), filled by two 2B strokes along the outline.
5. *Change in section 4:* say what `plan-pairs` means by *touch* (within 0.01 of the long
   side) and that a place whose line says *N% lighter* may be a wrong polygon; the
   compare heat map draws it. Evidence: `egg_cast_seen` three times (measured).
6. *Change in the card and exercise list:* say exercise 7 costs about 164 marks and the
   set about 330, so nobody runs them inside a budgeted session. Evidence: measured.
7. *Fix one of the two files:* DRAFTSMAN.md's "hard grade leant on" against
   CALIBRATION.md's "soft one at low pressure" bullet. Evidence: exercise 4 (measured).
8. *Change in step 4:* `sample()` returns a colour triple, not a mean value; say so, or
   point at `compare({place: v})` as the way to read one number. Evidence: exercise 3.
9. *Change in When you call it finished:* say the longest-run line prints only when a run
   is over 15; otherwise the draftsman must count. Evidence: this check.
10. *Change the card's example:* `subject_share=0.45` is not what this method spends on a
    subject; two drawings and this one spent a sixth to a quarter. Evidence: 23 of 140.
11. *Add to step 2:* "A table that runs from far to near is one plane with a pressure
    that is a function of where the row is, not two planes with a seam." Evidence: pass
    1's three rehearsals (seen; the seam measured as 0.72 against 0.60).
12. *Add to section 3:* "An ellipse four times wider than high cannot be laid evenly as
    arcs scaled inward; either space the arcs in pixels or accept the ends open and let
    the stump close them." Evidence: reasoned from the radii, seen in pass 2.

## The picture

Looked at small it reads as a shallow white bowl on a grey table, lit from the upper
left, with a crescent of shadow along its far wall, an egg sitting right of centre
whose shadow side turns into that crescent, and a dark cast shadow sliding off to the
lower right; the rim is a bright ring and the table grades from light at the far left
to dark at the near edge. The reason I wrote in the plan is half there: the egg is
found inside the bowl's light by its shade and its cast shadow, and after pass 7 by a
half-tone at its left end, but at 256 px the egg's lit side is still a bright blob and
its left end is more inferred than seen.

The passage I would apologise for is the egg's left end, where the lit egg meets the lit
floor with nothing but a half-tone I added last; second, the core of the bowl's cast
shadow, which at full size still shows three bands of 6B where one dark was wanted, and
which I would lay next time as one wide stroke in two overlapping passes rather than
three side by side.

## The films and the viewer

All three ran clean from the folder, each rebuilding 168 log records: `drawing_looks.mp4`
(the looks held, strokes in motion, 3.2 MB), `drawing_strokes.mp4` (the marks alone,
0.4 MB), and `viewer/` (`index.html`, `film.json`, 324 frames). No errors to keep.

---

## The round's re-measurement

*Written by the person running the round, off the session file, the PNG and the
engine, after the agent's write-up above was finished; the agent did not see this.*

### What changed between run 2 and this run

Drawn against the working tree after `cf116a0` on 2026-10-09, which differs from what
run 2 drew against in two ways, both listed here and not in the header so that the
write-up above was not steered by them:

- **The check, held to the guide** (`CHANGELOG.md`, *After the plan*): *no look between
  them* fires over 15 decisions where it fired at 30, a helper call counting as one
  decision; and a mark that turns 30 degrees or more between its first step and its
  last is left out of the stack-of-bars cluster.
- **Run 2's seven guide candidates, folded into `DRAFTSMAN.md`**: the hard edge laid in
  the mass's own value; a side stroke at one pressure ending in a block, so a stroke in
  the open and every arc wants a list that falls to its ends; the stump's number as a
  function of the holes (`0.03`, `0.06`, `0.11` to `0.15`); the band beside a thing
  stopping where a second thing breaks the silhouette; `s.compare(s.plan())` named as
  the number; `darks:` as an area; and the budget as twice what the subject has cost,
  with *unspent is not a finding by itself* in the closing section.

### Against the spec's pass criteria

| Criterion | Measured | Result |
|---|---|---|
| a look at least every 15 strokes | 44 looks and 110 rehearsals captured; the longest run of charged marks with no look inside it is **13**, in the table pass; no other pass over 10 | **met**, the first of the three runs to meet it |
| at least three grades, the side tip for the masses | five grades (`HB` 51, `2H` 42, `2B` 21, `6B` 3, `4B` 2 marks); 117 of 119 graphite marks on the side, the two points the signature | met |
| `compare()` within `0.10` on every planned place | 9 of 10; `egg_cast_seen +0.17` | **failed** on one place |
| darkest value at or above `0.80`; paper white kept in the subject | `0.85` of the way; `egg_lit` reads `0.96`, 98% of it paper never touched | met |
| the film plays, the viewer scrubs | `drawing_looks.mp4` 2,273 frames, 189 s; `drawing_strokes.mp4` 187 frames, 16 s; the viewer 324 frames | met |
| `replay()` matches the export | the replayed log against the saved canvas: **0 levels** on every pixel | met |
| `NOTES.md` names what went wrong | above, every claim tagged measured or reasoned | met |

Seven of eight, as run 2; the one that fails is a different one. Run 2 failed the loop
and met the plan; this run kept the loop (13 against 21) and lost one place of ten to
its own polygon.

### The agent's numbers, measured again

| Claim | As claimed | Measured | Held? |
|---|---|---|---|
| 140 of 400 spent, two signature ticks free | the budget line | 168 records, 140 charged; 24 `pencil`, 2 `erase` and the two `signature` ticks uncharged | yes |
| longest run with no look 13, none over 15; the first rehearsal of pass 1 flagged at 19 | counted off the scripts | 13 by the rule's own count over the committed log, in `p01_table.py`; the check printed no line, correctly; the rehearsal's 19 is not in the log | yes |
| the closing check's lines | verbatim | `easel check` run again on the file: every line identical | yes |
| a side stroke's end block runs on past its last point by half its width | the `lightest:` line, 9% at a 6 to 8 px margin, 0% at 14 to 18 px, `width=0.02` | a horizontal `HB` side stroke's value ends **2 px** past its last point at `width=0.02` and **12 px** at `0.07`, about a sixth of the width, not half; the margin the agent needed is the stroke's half-width across the outline, 10 px at `0.02`, plus that, which is the mechanism the guide states in section 2 for rows beside a thing | the number, yes; the mechanism, no |
| `HB` peaking at `0.92` under a bell list read `0.67` against `0.46` planned; `2B` at `0.78` read `0.47` | `int_shade` on two rehearsals | thirteen rows at `width=0.04`, flat against a bell list with the same peak, same place: `HB 0.92` reads `0.463` flat and `0.537` bell (**+0.07**); `2B 0.78` reads `0.322` flat and `0.400` bell (**+0.08**). A bell list reads about one grade lighter than its peak; the crescent's `0.67` has its arc spacing in it too | yes |
| the ring round the bowl reads at the table's median: texture, not value | `probe_halo.py`, `--count` | my own gauge, a ring 40 to 90 px out against the table 120 to 200 px out, the cast shadows excluded: upper half `0.608` against `0.631` (**-0.024**), lower half `0.533` against `0.545` (**-0.012**); a touch darker, not lighter, within `0.03` | yes |
| exercise 7 costs 164 marks | the budget line | 164 records, 164 charged, run again; in a session of its own, as every exercise is, so none of it against a drawing's budget | yes; the fear of a third of the budget is not |
| the guide and the calibration disagree on a light tone | read | `CALIBRATION.md` line 332, written off the sampler before any drawing; the guide's rule was measured on run 1 and by exercise 4 in runs 2 and 3; the calibration's sentence is the stale one, and is corrected with this run | yes |
| `sample()` returns a colour triple, not a value | exercise 3 | `Session.sample` returns the engine's linear colour at a place, for painting with; the guide's *a mean of whatever is in it* is true of a colour | yes |
| the closing check's longest-run line is silent under 15 | this check | by design: it is a finding, printed when a run is over the line, and the guide's closing paragraph promised a standing line; the paragraph is corrected with this run | yes |
| `egg_cast_seen +0.17` is the place polygon, not the shadow | the heat map | not re-measured: the polygon is the agent's own, and the criterion reads the place as declared | taken as stated |

And one the agent could not have claimed: **no stack-of-bars line fired on any pass**,
and none would have under the old rule either. Replayed without the arc gate, the
bowl's 27 long arcs cluster 12 by chord, under the three-fifths share, and the table's
rows 28 of 53. The gate built from run 2 was not exercised by this run; neither was the
helper-call rule, since the log has no helper call in it. The look-gap line at 15 was:
it fired once, in a rehearsal, at 19, and the agent put a look in before paying.

### The picture

A shallow bowl seen from a little above, lit from the upper left, with a crescent of
shade along its far wall, an egg right of centre whose shade turns into the crescent,
and the bowl's cast shadow sliding off to the lower right. Against run 2: the rim is a
continuous bright ring with no block at either side of the egg, the hard edge is a
speckled line in the table's value and not a dark ring, and the table grades from far
to near instead of reading as a cloud. Three faults, two of them the agent's own
apologies: the egg reads as a white disc with a dark C-shaped ring rather than a form
turning; the bowl's cast shadow is three `6B` bands side by side, visible at full size
and at 256 px; and the far table is still mottled, a second stump having closed it only
partly. The egg's cast shadow attaches to the egg and reads as a shadow, which run 2's
did not.

### What this run says of the guide

Run 2's seven candidates, against this run:

1. **The hard edge in the mass's own value**: **held**. The rim's edge is a `2H` at the
   table's own pressure function plus `0.05`, 13 px wide, centre 2 px outside the rim;
   no dark ring (the picture).
2. **A side stroke ends in a block; a list that falls to its ends**: **held, and
   sharpened**. The agent read the rule, saw a staircase of blocks down the crescent's
   right wall in rehearsal, and faded the ends to `0.12`; its candidate 3 below names
   the number the guide left out.
3. **The stump's number is a function of the holes**: **held as far as tested**.
   Exercise 6 moved a toned patch `+0.15`, inside the guide's `0.11` to `0.15`; the
   rows were not read before and after their stumps.
4. **The band stops where a second thing breaks the silhouette**: **not tested**. The
   agent moved the bowl up at the envelope so that the egg sits below the far lip, and
   nothing broke the silhouette.
5. **`compare(s.plan())` is the number**: **held**. Eight compares in the committed
   passes; the heat map is what found the wrong polygon, three times.
6. **`darks:` is an area**: **held**. `0.85` of the way in six marks, against run 2's
   twelve; laid as three strokes side by side that show as bands, which the guide does
   not forbid.
7. **The budget**: **held**. 140 spent, 8 of them on the apology passage after the
   closing check, then stopped; the check's `unspent:` line still asked for the weakest
   passage, so the line and the guide now disagree (an engine candidate, below).

The check's changes: the look gap at 15 did its work (the only run of three to meet the
criterion, and the one line it printed was acted on); the helper-call rule and the arc
gate were not exercised.

Of the agent's twelve candidate rules, after measuring:

1. **A run cut round a thing standing in the passage is cut at the thing grown by half
   the stroke's width and a few pixels.** The number holds; the mechanism is the
   half-width across the outline that section 2 already states for rows beside a thing,
   and the guide should say it once for any run cut round anything.
2. **A pressure list that falls to its ends reads about a grade lighter than its peak**
   (`+0.07` and `+0.08`, measured above): a passage laid with faded ends wants the next
   softer grade, or its peak leant on.
3. **Arc ends fall to near nothing over their last thirty pixels**, or they end in
   steps (seen in two rehearsals; consistent with run 2's measurement of a side
   stroke's end).
4. **A lost edge needs the two tones to butt**: the margin cut round the thing is
   filled along its outline in the neighbour's value before the stump goes across, or
   the stump spreads a white halo (seen in a rehearsal, and the two strokes that fixed
   it are in `p03_egg.py`).
5. **Say what *touch* means in the plan's pairs** (within `0.01` of the long side), and
   that a place whose line says *N% lighter* may be a wrong polygon, which the heat map
   draws.
6. **The exercises are sessions of their own**, and the seventh lays 164 marks; the
   guide's *a minute each* is about time, and should say the cost does not touch the
   drawing.
7. The calibration's stale sentence: **corrected with this run**, not a candidate.
8. `sample()` as a colour: **corrected with this run**.
9. The closing paragraph's promise of a standing longest-run line: **corrected with
   this run**; the standing line itself is an engine candidate.
10. **The card's `subject_share=0.45`**: three drawings of one subject spent a sixth to
    a quarter of their marks on it; the example steers the plan wrong.
11. **A plane that runs from far to near is one plane with a pressure that is a function
    of where the row is**, not two planes with a seam (three rehearsals; the seam read
    `0.72` against `0.60`).
12. **Arcs scaled inward on a wide shallow ellipse are not evenly spaced** (reasoned
    from the radii; seen).

Each a hypothesis until a fourth session draws against it.

For the engine and the check, candidates to measure before building:

- The `unspent:` line asks a drawing to name the weakest passage and spend the rest
  there, and the guide now says the rest is reserve; for a drawing the line could say
  the number and stop.
- A standing `looks:` line in a drawing's closing check, the longest run as a
  measurement, beside the finding that fires over 15.
- `boxes: no masses laid yet` is printed for a drawing, which lays no mass verb; the
  line could be silent in graphite.
- A pressure list that is not a list of numbers (the agent's helper handed a complex
  number) raises an error naming `pressure_curve` and nothing the draftsman wrote.
