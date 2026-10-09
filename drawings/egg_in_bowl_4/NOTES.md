# A hen's egg in a shallow bowl, drawn a fourth time

**Run 4 of `SPEC.md`'s test drawing: two of run 3's candidates, measured.** The same
subject as `drawings/egg_in_bowl/` (run 1), `drawings/egg_in_bowl_2/` (run 2) and
`drawings/egg_in_bowl_3/` (run 3), a fourth seed, drawn by a fresh session against
`DRAFTSMAN.md` as it stands on 2026-10-09, the working tree after `a66e6c4`. What changed
in the guide between run 3 and this run is listed under the re-measurement at the end,
so that the agent's own write-up is not steered by it. Run 3 was the only measurement of
what run 2 changed in the guide; this run is the only measurement of what run 3 changed
(`LESSONS.md`: a guide change is a hypothesis until a fresh session draws against it).

## The subject, chosen before the agent saw anything

Written here by the person running the round, before the first stroke, as the protocol
asks. The same words as runs 1 to 3, so that the four drawings differ only in the seed
and in what the agent had to read:

> **A single hen's egg in a shallow white bowl on a plain wooden table, lit from a
> window to the upper left, out of frame.** Three or four value masses: the lit side of
> the egg and the bowl's lit rim, the egg's shadow side, the bowl's interior shadow with
> the egg's cast shadow in it, and the table. One hard edge: the bowl's rim against the
> table. One lost edge: the egg's shadow side into the bowl's shadow behind it.

The drawing agent is told this subject in its brief and nothing else about the picture.
It is not the spec's example subject.

## Setup

- `drawing.easel`: 1024x768, `cartridge`, white, **seed 17**, budget 400,
  `medium="graphite"`, `capture=True`, `out_dir` `out/` -- made with `easel new` from
  this folder.
- The agent works through the shell (`easel run`, `easel look`), as the earlier runs
  did, with `py -3.14 -m easel` and `PYTHONPATH` on the checkout's `src/`, because the
  installed wheel is 0.8.0 and has no graphite. The passes are its own numbered scripts
  beside this file.
- A fresh session: the agent has not seen this repository, the spec, the review or the
  earlier runs. It is given `DRAFTSMAN.md` as its guide, the paths of the documents the
  guide points at, and told that what it reads is part of the record. It is told not to
  open the three earlier drawings' folders, `SPEC.md`, `SPEC-REVIEW.md`, `PLAN-0.9.0.md`,
  `CHANGELOG.md`, `LESSONS.md` or `SUGGESTIONS.md`.

## What the agent read, what it did, what went wrong

*Written by the agent at the end of its run, below this line; re-measured by the person
running the round after it.*

---

## The agent's write-up

**Strokes spent: 113 of 400.** Measured: the closing check's first line, and `s.spent`
read off the session file by `probe_counts.py`. 121 records: 6 pencil (free), 95
lines, 20 stumps; the two signature lines are free, so 113 charged. No eraser was used.
Grades over the whole drawing, counted off the records: 2H 29, HB 53, 2B 6, 4B 5, 6B 2.

The passes in order, each with what `easel run` printed as its cost (measured):

| Pass | Script | Cost | What it laid |
|---|---|---|---|
| 0 | `p00_envelope.py` | 0 | six pencil lines, a gridded look, a thumbnail |
| 1 | `p01_table.py` | 51 | 49 rows at -5 and +15 degrees cut round the bowl, one stump over the far plane and one over the near |
| 2 | `p02_bowl.py` | 23 | the table's band round the bowl (4 arcs, 2 stumps along them), the interior shade as arcs of the interior inset in pixels and arcs of the egg grown, the lit end as three 2H arcs, five stumps along the arcs |
| 3 | `p03_egg.py` | 10 | six cross-contour arcs of the egg's own shape, a stump along the terminator and one along the outer arcs, two bands beside the egg |
| 4 | `p04_wall.py` | 8 | three arcs for the near wall and a stump along it, two stumps along the lit end, a stump along each band beside the egg |
| 5 | `p05_edges.py` | 6 | a stump behind the egg's top, the hard edge round the silhouette in two halves, the egg's lit edge found, two stumps across the lost edge |
| 6 | `p06_darks.py` | 11 | the cast shadow as seven arcs attached to the egg (cut into runs), a 4B arc along the contact, a stump along the shadow's outer edge only |
| 7 | `p07_core.py` | 4 | two 6B arcs along the contact, one 2H arc and a stump for the last sliver of bare floor |
| 8 | `p08_sign.py` | 0 | two signature strokes, after `easel undo 2` removed a first pair that landed nothing |

**Rehearsals and looks.** 15 rehearsal runs (`easel run --rehearse`: pass 1 once, pass 2
three times, pass 3 twice, pass 4 twice, pass 5 twice, pass 6 three times, pass 7
twice) and 8 committed runs; measured off `s.passes`, which keeps 25 entries (one per
run, the signing pass twice because of the undo). The capture kept 61 rehearsal images
and 28 looks (`s.captures` by kind). Of those I opened and looked at, with the Read
tool, 31 PNGs of the drawing (the envelope and thumbnail; the table's rows before and
after the stump; every rehearsal's final look and, from pass 3 on, its full-size crop;
the mid-pass looks of pass 2 twice; the committed small look at 256; the export; the
signature crop) and 15 of the exercises. Counted by hand from this session's record;
not measured by the engine, which cannot see what I opened.

**The closing check** (`check_final.txt`, verbatim lines):

```
checklist for this painting -- 113 of 400 marks spent
  plan: 9 of 9 places inside 0.10
  lightest: egg_lit reads 0.96 as a place, 0.96 at its brightest twentieth, the lightest of the 9 places planned; 89% of it paper never touched
  subject: 40 of 113 marks so far (35%), against 45% planned -- behind, if the subject is finished
  values: 0.47-0.83 of a box that reaches 0.04-0.96, clusters at 0.50, 0.62, 0.90; a clear light, mid and dark
  edges: 35% of edges are under 2.5 px wide, median 3.3 px
  paper: 2.75% of the canvas is paper never touched
  pencil: the envelope still shows over 1.31% of the canvas -- export(sketch=False) leaves it out
  boxes: no masses laid yet
  darks: the darkest half-percentile reads 0.14, 0.85 of the way from paper to black
  unspent: 287 of 400 unspent (72%) -- name the weakest passage and spend them there
```

**The longest run of marks with no look between them.** The check printed no such
line, on any pass or at the close. By my own count off the session's look indices
(`probe_counts.py`, the log length at each look or rehearsal capture), the longest run of
records between two looks is **12**, inside the table pass, where the script took a look
every twelve rows. Measured.

## What I read, and how far

- **`DRAFTSMAN.md`**: the whole file, all 572 lines, once, before anything else, with no
  index. I did not reopen it; everything I followed later I followed from that reading.
- **`REFERENCE.md`**: I pulled the heading list first (a grep for lines starting `#`) and
  used it as an index. Then read whole, by section: *Units, which is where the surprises
  are*; *What counts against the budget*; *The verbs* (for the `line()` and `pencil()`
  signatures); *Pressure*; *Places*; *Shapes*; *The graphite medium*; *Looking, planning,
  measuring* with *What the plan changes*; *What the tool will tell you*; *The session,
  and the shell*. Not read: *The arguments that mean something particular*, *Where a
  stack of passes starts*, *The brushes*, *Colour*, *Or through the MCP server*.
- **`CALIBRATION.md`**: the heading list as an index, then *The graphite medium*, *The
  stump and the erasers* and *The check, measured on the first drawing* (lines 302 to
  492), whole. Nothing else in it.
- **Source**: none read. One probe, `inspect.signature(Region)` and
  `inspect.signature(polygon)`, to learn that `Region(..., name=)` exists, because the
  reference says to name every place and shows no way to name a `Region`.
- `easel explain`, `easel guide`, `easel diagnose`, `easel demo`: not used.

## The exercises

Looks under `ex_out/`, scripts `ex_01_box.py` to `ex_09_loop.py`, run as plain scripts
with `Session(out_dir="ex_out")`.

1. **The box.** At `0.3`, `4H` and `2H` left almost nothing and `HB` a scatter; `2B` to
   `6B` at `0.3` were dark but full of holes. At `1.0`, `2H` an even light grey with a
   few holes, `HB` a mid grey, `2B` to `6B` near black with the side tip's striations
   running across the stroke. Matched the guide and the calibration table.
2. **Six pressures.** On the point the width swells and tapers with the profile; on the
   side only the darkness and the speckle change. Matched.
3. **A plane.** `plan: 1 of 1 inside 0.10` before and after the stump; the `values:`
   cluster for the plane moved `0.52` to `0.55` (measured off the two reports), which is
   the guide's `0.03` for rows leant on. What the guide did not say: the rows at `0.06`
   wide and `0.08` apart on a 600-high sheet left visible seams between them, and the
   stump mottled the plane rather than evening it. The diagonal `2H` rows ran off the
   plane's box.
4. **Hard leant on, soft held lightly.** `HB` at `0.5` a field of white points; `2H` at
   `1.0` a tone with a few holes, its cluster at `0.58`. Matched.
5. **Across and along.** The hatched oval came out near black (`2B` at `0.8` on the side
   at half-width spacing lays everything twice) and its rows' ends step down the
   outline, subtly at look size; the arcs along the shape made a crescent whose ends
   speckle where the list falls to `0.4`. Matched, and the speckled ends were a warning
   I used later.
6. **The stump's number.** `D4` inside `0.10` before, `+0.15` after (measured, the
   `plan:` line). The guide said a tenth or more; `0.15` is the top of its range. The
   `tone()` also bled a fringe of speckle past the cell's edge.
7. **Three edges.** The hard edge reads as a line; the soft one as a slight blur; the
   lost one as a *lighter smear* across the join, not a merge, because `tone()` at
   `0.6` leaves holes for the stump to spread into. 164 marks for three small panels:
   `tone()` is as dear as the guide says.
8. **The eraser.** The kneaded patch lifted to a ghost with the `6B` line still faint
   inside it; the plastic patch to near paper with a faint ghost of the line. Matched.
9. **The loop.** `cost` 36, the rehearsal and the committed hatch identical, `pencil:
   0.38%` after. Matched.

## The passes

**Pass 0, the envelope (0).** I decided the picture in the prelude before drawing it:
the bowl's silhouette an ellipse centred at `(0.50, 0.615)`, `0.31` by `0.175`; a rim
line inside it and an interior inside that; the egg at `(0.455, 0.615)`, `0.105` by
`0.085`, tilted `-8` degrees; the cast shadow's outer line the egg's shape shifted to
`(0.545, 0.648)`. Nine named places with values: `table_far 0.58`, `table_near 0.50`,
`rim_lit 0.93`, `wall 0.72`, `bowl_lit 0.80`, `bowl_shade 0.56`, `egg_lit 0.92`,
`egg_shade 0.56`, `cast 0.26`; `lightest=egg_lit`; `subject_share=0.45`. At
registration the check named two pairs within `0.10` that touch: `bowl_shade /
egg_shade` (the lost edge, meant) and `wall / bowl_lit` (they touch across the near rim,
which is paper between them; I let it stand). Six pencil lines, a gridded look and a
thumbnail: the bowl sits in B5 to G7, the egg in C5 to E6, and the thumbnail read as a
bowl with an egg and a wedge of shadow. Nothing rehearsed, nothing committed.

**Pass 1, the table (51).** Planned: rows by hand at `width=0.07`, `-5` degrees every
`0.065` and `+15` degrees every `0.085`, each a dense polyline with a pressure list
lighter toward the window on the left, `2H` at `[0.80, 1.00]` above `y=0.42`, `HB` at
`[0.55, 0.70]` beside the bowl and `[0.62, 0.80]` below `0.74`, cut round the bowl
grown by 40 px (half the stroke's width and four pixels) with the pressure fading over
the last 30 px of a cut run; a look every twelve rows; a stump at `1.0` over each
plane. The rehearsal laid 49 rows and 2 stumps and read `table_far +0.04` (0.62) and
`table_near +0.02` (0.52); the look showed a plane, mottled after the stump, with a
clean gap round the bowl. Committed as rehearsed, the same numbers. The stack-of-bars
line did not fire. After: `plan: 4 of 9`, `paper: 18.25%`.

**Pass 2, the bowl (23).** Planned: the band the rows stopped short of, as two arcs
round the far half (`2H` at a bell to `1.0`) and two round the near (`HB`, to `0.85`);
the interior shade as arcs of the interior inset 18, 38, 58 and 78 px from the back-left
round to the right with a bell to `0.95` (`HB`, `width=0.03`) cut round the egg, and as
arcs of the egg's shape grown `1.22` to `2.18` for the floor beside it, held inside the
interior; the lit end as three `2H` arcs at a bell to `0.9`; stumps. **Rehearsed three
times.** The first rehearsal showed the band as a ring of white speckle (never
stumped), the shade with a hard diagonal boundary where its arcs started at the chord
and where a stump over the `bowl_shade` polygon stopped, and a notch of paper at the
top. I added stumps along the band, started the arcs further round the back so that
they fade out, and replaced the polygon stump with stumps along the arcs. The second
rehearsal read right (`bowl_shade -0.03`, `bowl_lit -0.06`) but the `lightest:` line
fell from 99% to **81%** of the egg's lit crescent paper never touched: two stump paths
along the interior's back, 61 px wide, crossed into the egg's top. Cut round the egg
grown 37 px, the third rehearsal read **100%** again, `bowl_shade -0.03` (0.53),
`bowl_lit -0.07` (0.73). Committed as the third. After: `plan: 6 of 9`, `paper: 7.31%`.
Measured, all of it, off the compare and check lines; what I saw in the looks is
reasoned.

**Pass 3, the egg (10).** Planned: six cross-contour arcs of the egg's own shape at
`k` 0.96 to 0.56, each shorter than the last so that their ends trace the terminator
(`HB 0.75`, `HB 0.95`, `2B 0.85`, `HB 0.95`, `2H 1.0`, `2H 0.8`, bells, `width=0.014`);
a stump along the terminator at `k=0.6`; then the two bands beside the egg that the
interior's arcs had stopped 19 px short of, laid along its silhouette 12 to 13 px
outside it, `2H` round the lit side in the floor's value and `HB` round the shade side.
The first rehearsal read `egg_shade +0.04` (0.60) and `bowl_lit -0.10` (the lit band
sits partly in that place), `lightest 97%`; its full-size crop showed the six arcs as
distinct rings. I added a stump along the outer arcs at `k=0.86`. The second rehearsal
looked like a form; committed. After: `plan: 7 of 9` (cast and wall still out), `egg_lit
0.96, 97% paper never touched`.

**Pass 4, the wall (8).** Planned: three arcs blended between the rim's lower half and
the silhouette's, `2H` on a ramp from `1.0` at the shade end to `0.5` at the lit end,
`width=0.016`, with eased ends; a stump along the middle one; and two stumps along the
lit end of the interior to close the 2H arcs' holes. First rehearsal: `wall +0.03`,
`bowl_lit -0.07`, but the stumps cut 37 px round the egg left a speckled halo of
unstumped 2H round the egg's lit side, and the `HB` band round its shade side read as a
dark ring where it doubled the shade's arcs. I added a stump along each band and cut the
lit-end stumps round a tighter keep-out (25 px). Second rehearsal: halo closed, ring
merged, `lightest 94%`. Committed. After: `plan: 8 of 9`.

**Pass 5, the edges (6).** Planned: a stump behind the egg's top where the shade's
stacked arcs were left unstumped and showed the side tip's striations; the hard edge
round the silhouette as a `0.013`-wide side stroke with its centre 2 px outside the
line, `2H` at a bell to `1.0` round the far half and `HB` to `0.85` round the near; the
egg's lit edge found with a `2H` at `0.7`, 12 px wide, 3 px outside the outline; a
narrow `HB` at `0.9` along the rim's inner line against the shade; two stumps across
the lost edge. First rehearsal: `lightest 89%` (the found edge's inner side and the
top stump took 5%), and the crop showed the rim's inner-line stroke as a dark ring
inside the rim with blocked ends, the guide's "dark ring, not an edge". Dropped it;
the paper rim against the stumped shade was already hard. Second rehearsal 6 strokes;
committed. After: `edges: 37% under 2.5 px`, `plan: 8 of 9`.

**Pass 6, the darks (11).** Planned first as six concentric arcs of the shifted shape,
`2B` outside and `4B` inside, cut short of the egg. **Rehearsed three times.** The
first read `cast +0.02` and `plan: 9 of 9`, and looked wrong: the arcs ended in the
open at both ends so the ends stepped down the far side as a staircase, and the shadow
was a hard wedge. Rewritten as arcs attached to the egg, each starting and ending on
the egg's lower-right outline and bulging out toward the shadow's outer line by a
factor `u`, the ends landing inside the egg's keep-out and cut there; a `4B` arc along
the contact; a stump along the outer edge only. The second rehearsal read right but
showed five arcs at `0.022` as ribs, and `lightest 83%` because the stump's ends sat on
the egg's outline at the lit crescent's lower tip. Seven arcs at `0.028` and the stump
cut round the egg: third rehearsal `lightest 89%`, `plan: 9 of 9`, a solid shadow with
a soft edge. Committed. The closing check then read **`darks: 0.22, 0.78 of the way`,
under 0.80**: the `4B` arcs at a bell falling to `0.5`, 25 px wide, had not reached it.

**Pass 7, the core (4).** Planned: two `6B` arcs along the contact under the egg at
12 and 34 px, `width=0.03`, and one `2H` arc with a stump for a sharp triangle of bare
floor at the interior's left end that read as a notch. First rehearsal: `darks: 0.13,
0.86`, but the `6B` arcs from 25 to 125 degrees with ends at `0.5` stood out of the
shadow as a slab under the egg's lower left: a `6B` at half pressure is black. Shortened
to 32 to 112 degrees with ends at `0.12`: `darks: 0.14, 0.85 of the way`. Committed.
Final: `plan: 9 of 9`, `lightest: egg_lit 0.96, 89% paper never touched`.

**Pass 8, the signature (0).** An `HB` tick 15 px long at `0.6` on the point and a 2 px
two-point dot, the guide's own recipe; the check said `landed nothing: 2 graphites at
records 119, 120`. `easel undo 2` (free), then two strokes of a chevron 30 px each, `HB`
at `0.9`, `width=0.004`: landed, no line printed. Exported `drawing.png` without the
envelope.

## What went wrong

Each claim is marked measured (M, with the number and where it came from) or reasoned (R).

- **Passages repaired.** None on the paper: no eraser, no `undo` of a charged mark. The
  repairs were all in rehearsal, eleven re-rehearsals over seven passes (M, `s.passes`).
  Two additions over committed passes count as treatments of a passage already laid:
  the stump behind the egg's top in pass 5 and the sliver of floor in pass 7. The
  signature was undone once (M, the log: records 119 and 120 removed).
- **The light eroded.** The egg's lit crescent read 100, 100, 97, 94, 89, 89 and 89
  percent paper never touched after passes 2 to 7 (M, the `lightest:` line each
  pass). Every stump or edge laid near the egg took 2 to 5 percent, and none was aimed
  at it. It still reads `0.96` as a place (M).
- **Rules broken.** (1) In pass 2's first version I stumped over a polygon, and the
  guide's "a stump acts on everything under the place" showed at the polygon's edge, not
  inside it: a hard chord (R, seen in the rehearsal look). (2) I committed pass 5's final
  version after a chained rehearsal whose image I did not open, because it differed from
  the one I had looked at by one removed stroke (R). (3) I laid a `6B` with its ends at
  half pressure, after the box exercise had shown me `6B` at `0.3` is dark (R). (4) The
  subject got 35% of the marks against 45% planned (M); the planned number was a guess
  and the table is most of the sheet. (5) The guide's signature recipe landed nothing
  (M, `landed nothing:` on records 119 and 120).
- **Check lines I did not understand or disagree with.** `boxes: no masses laid yet` is
  printed in a drawing's closing check and can say nothing else, since a drawing lays
  no masses (R). `plan: 9 of 9 inside 0.10` prints no number for a place inside the
  threshold, so I called `s.compare(s.plan())` at the end of every pass to read them;
  the guide says to, and the line could carry them (R). `edges: 35%` is a number I had
  no use for (R). `subject: behind, if the subject is finished` cannot know whether it
  is (R). The `plan-pairs` notice named `wall / bowl_lit`, which touch only across the
  near rim's paper; true and harmless (R). The most useful line was `lightest: ... N% of
  it paper never touched`: it caught stumps crossing the egg's top in pass 2 (81%) and
  the shadow stump's ends on the lit tip in pass 6 (83%) before any look did (M).
- **Where the guide was wrong, unclear, or silent.**
  - *Silent on the side tip's striations.* A side stroke at full pressure leaves
    striations across its own direction (exercise 1 shows them), and where arcs stack
    unstumped, as behind the egg's top where a keep-out stopped the stump, they read as
    a comb (R, seen in the pass 4 crop; closed by one stump in pass 5).
  - *Silent on a stump's own edge.* "Over a shape it is worked every way" does not say
    the shape's outline shows where it stops (R, pass 2's first rehearsal).
  - *The band beside the thing.* Laid as the guide says, one layer along the silhouette
    and stumped, it reads at full size as a smooth halo ring round the bowl, a different
    surface from the stumped rows; small, it vanishes (R, every look from pass 2 on).
  - *A light tone.* The guide gives `2H` at `1.0` (reads `0.58`) and nothing between
    that and paper; `bowl_lit` planned at `0.80` was laid as `2H` at a bell to `0.9` and
    read `0.77`, `0.73`, then `0.77` after two more stumps (M, the compare lines), and
    was speckle until stumped twice. A tone of `0.70` to `0.85` is a hard grade held
    off *and stumped at full strength*, and the guide should say so.
  - *The darks.* "A `4B` once" reaches `0.80` in the calibration patch at full pressure;
    seven `4B` and `2B` arcs with lists falling to `0.5`, 25 to 29 px wide, read `0.22`,
    `0.78` of the way (M). Two `6B` arcs at a bell to `0.9` read `0.14`, `0.85` (M).
    The criterion reads the darkest half-percent, about 3,900 px; a dark laid with a
    list that falls at its ends wants the next softer grade, as the guide says of lists
    in general, and the darks section does not repeat it.
  - *The signature.* The guide's own example, an `HB` tick at `0.6` two points apart,
    carried under one unit on this paper (M). The "two-point tick" advice is about the
    point count, not the deposit.
  - *The cast shadow* is laid "as arcs of its own shape" in the calibration's note on
    the loop's signature; the guide does not say that a cast shadow's shape is attached
    to the thing that casts it, so arcs concentric with the shadow's own outline end in
    the open and staircase (R, pass 6's first rehearsal).
  - *"A list that falls to its ends reads about a grade lighter than its peak"* held:
    `HB` at a bell to `0.95`, stumped, read `0.52` to `0.53` where `HB` at `1.0` is
    `0.44` in the table (M).
  - *The stump's number on hand-laid arcs.* `bowl_shade` moved `+0.01` between the
    first rehearsal (polygon stump) and the second (path stumps), so I cannot separate
    the stump's shift from the rewrite; I did not read the shade before its stumps (R).

## Candidate rules

1. **Add** to step 2 of the card: *a stump dragged along a path is cut round what must
   stay paper, by half its width and a few pixels, as a row is; a stump over a shape
   stops at the shape's outline and the outline shows* -- evidence: pass 2's first
   rehearsal (a chord), its second (`lightest` 81%), its third (100%).
2. **Add** to step 8: *every stump or edge stroke laid beside the light takes two to
   five percent of its paper never touched; count them before laying them* -- evidence:
   100, 100, 97, 94, 89, 89, 89 percent over passes 2 to 7 (M).
3. **Change** step 7: *a dark laid with a list that falls to its ends wants the next
   softer grade: `4B` arcs at a bell to `1.0` falling to `0.5`, 25 px wide, read `0.22`
   (0.78 of the way); two `6B` arcs at a bell to `0.9` read `0.14` (0.85)* (M).
4. **Add** to step 3: *a cast shadow is attached to what casts it: lay its arcs from one
   contact point on the outline to the other, bulging out, never as concentric arcs of
   a shifted shape, whose open ends step down the far side* -- evidence: pass 6's first
   and second rehearsals (R, the looks).
5. **Add** to *Two tips*: *a `6B` at half pressure is black, so a `6B` list's ends want
   `0.1`, not `0.5`* -- evidence: pass 7's first rehearsal, a slab under the egg (R);
   the box exercise, `6B` at `0.3` dark with holes (R).
6. **Change** *Sign it*: the example tick landed nothing on this paper (M, records 119
   and 120); *a signature stroke is thirty pixels at `0.9`, four pixels wide*.
7. **Add** to step 5: *a tone between `0.70` and `0.85` is `2H` held off and stumped at
   full strength twice; it is speckle until the second stump* -- evidence: `bowl_lit`
   `0.77`, `0.73`, `0.77` (M) and the looks (R).
8. **Remove** `boxes:` from a drawing's closing check, or print it only when a mass was
   laid (R).
9. **Change** the `plan:` line to print each place's reading, not only the misses, since
   the guide tells the draftsman to read the numbers after every pass and the line
   makes a second call necessary (R).
10. **Add** to *Six mistakes*: *an edge stroke in a value darker than the mass is a dark
    ring; the rim's inner edge against a stumped shade needs no stroke at all* --
    evidence: pass 5's first rehearsal (R).

## The picture

Looked at small, it reads as a white bowl on a grey wooden table with a white egg in it,
lit from the upper left; the rim is a bright ring, the egg's lit side the brightest
thing, and a dark shadow under and to the right of the egg holds it on the bowl's
floor. The reason I gave the plan is still there: the egg's lit side and the rim are
the only paper, and everything else is darker (M, `lightest: egg_lit 0.96, the lightest
of the 9 places`; R, the look at 256). Cover the cast shadow and the egg still sits in
the bowl, because the egg's shade side and the bowl's shade do the sitting.

The passage I would apologise for is the cast shadow's lower-left end, where the 4B
runs attach under the egg and end in a hard corner, and after it the band round the
bowl, which at full size is a smooth ring of a different surface from the table. I
left the 287 unspent because neither is a passage more marks would mend: the corner is
in the darks, which the method says to leave, and the ring is a texture a stump made,
which only the envelope could undo.

Files created in this folder: `ex_01_box.py` to `ex_09_loop.py` and `ex_out/`;
`prelude.py` (filled in), `p00_envelope.py` to `p08_sign.py`, `probe_counts.py`;
`drawing.png`, `check_final.txt`, `drawing_looks.mp4`, `drawing_strokes.mp4`,
`viewer/`, `film_looks.log`, `film_strokes.log`, `film_viewer.log`; and `out/` with
every look, rehearsal and compare the session wrote.

---

## The round's re-measurement

*Written by the person running the round, off the session file, the PNG and the
engine, after the agent's write-up above was finished; the agent did not see this.*

### What changed between run 3 and this run

Two of run 3's twelve candidates, the two with a measurement behind them, folded into
`DRAFTSMAN.md` before this run and not named in the header:

- **A list that falls to its ends reads about a grade lighter than its peak** (*Two
  tips*): `+0.07` and `+0.08` on the same rows, flat against bell, measured after run 3.
- **Any run cut round a thing standing in it stops half the stroke's width and a few
  pixels short of the thing, rows and arcs alike** (section 2, and the card's step 3):
  section 2's half-width fact said once for every run.

The agent noted that `CHANGELOG.md` changed in the working tree during its run. It did:
the changelog entry for the fold above was written while it drew. `DRAFTSMAN.md` was
folded before the run began and did not change during it; the guide the agent read is
the one it drew against. Nothing under `src/` changed between run 3 and this run.

### Against the spec's pass criteria

| Criterion | Measured | Result |
|---|---|---|
| a look at least every 15 strokes | 28 looks and 61 rehearsals captured; the longest run of charged marks with no look inside it is **12**, four times, all in the table pass where the script looked every twelve rows; no other pass over 7 | met |
| at least three grades, the side tip for the masses | five grades (`HB` 53, `2H` 29, `2B` 6, `4B` 5, `6B` 2 marks); 93 of 95 graphite marks on the side, the two points the signature | met |
| `compare()` within `0.10` on every planned place | 9 of 9 | met |
| darkest value at or above `0.80`; paper white kept in the subject | `0.85` of the way; `egg_lit` reads `0.96`, 89% of it paper never touched | met |
| the film plays, the viewer scrubs | `drawing_looks.mp4` 1,398 frames, 117 s; `drawing_strokes.mp4` 140 frames, 12 s; the viewer built | met |
| `replay()` matches the export | the replayed log against the saved canvas: **0 levels** on every pixel | met |
| `NOTES.md` names what went wrong | above, every claim tagged M or R | met |

**Eight of eight**, the first of the four runs to meet them all: run 1 met six, runs 2
and 3 seven each with a different one failing.

### The agent's numbers, measured again

| Claim | As claimed | Measured | Held? |
|---|---|---|---|
| 113 of 400 spent; 121 records, 6 pencil, 95 lines, 20 stumps, two signature strokes free | `s.spent` and the records | 121 records, 113 charged; `graphite` 95, `stump` 20, `pencil` 6 | yes |
| longest run with no look 12, in the table pass | `probe_counts.py` | 12 by the rule's own count, four runs of 12, all in `p01_table.py`; the check printed no line, correctly | yes |
| the closing check's lines | verbatim | `easel check` run again on the file: every line identical | yes |
| the guide's own signature tick landed nothing (records 119 and 120, undone) | the `landed nothing:` line | the undone records are not in the log. Laid again: on **bare paper** the guide's tick (`HB` at `0.6` on the point, 15 px) carries **5 to 9 units** at two seeds and lands; over a **stumped `HB` tone** like the table's it carries **0.37 of a unit** and lands nothing, and a 2 px dot `0.06`. The agent's 30 px stroke at `0.9`, `width=0.004`, carries 3.3 units over the same tone. The recipe is right on paper and wrong over a tone: *close in value to what it sits on* and *HB at 0.6* cannot both hold on a toned corner | yes, with the mechanism |
| a list falling to its ends reads a grade lighter: `HB` at a bell to `0.95`, stumped, read `0.52` to `0.53` against `0.44` for `HB` at `1.0` | the compare lines | consistent with the `+0.07` measured after run 3 on flat against bell rows; not re-measured on this log | yes |
| seven `4B` and `2B` arcs with lists falling to `0.5` read `0.78` of the way; two `6B` arcs at a bell to `0.9` took it to `0.85` | the `darks:` line after passes 6 and 7 | the closing check reads `0.14`, `0.85`; the pass 6 reading is not kept in the log; the mechanism is the bell-list rule the guide now states, unapplied in the darks | yes |
| the egg's light eroded 100, 100, 97, 94, 89, 89, 89 percent over passes 2 to 7, from stumps and edge strokes beside it, none aimed at it | the `lightest:` line each pass | the closing 89% reproduces; the earlier readings are the engine's own line and are taken as stated; every charged mark that touches `egg_lit` in the log is a stump or an edge stroke, none a row or an arc of a mass | yes |
| the stack-of-bars line did not fire on the table pass | the check | replayed: nothing fires under the new rule, and nothing would have under the old one either (the table's rows cluster 25 of 49, under the three-fifths share); the arc gate was not exercised, nor the helper-call rule (no helper calls in the log) | yes |

### The picture

A shallow white bowl on a grey table lit from the upper left, its rim a bright ring,
with an egg left of centre whose lit side is the brightest thing on the sheet and whose
shade side turns into a solid dark cast shadow curling under it to the lower right.
Against run 3: the egg reads as a form and not as a disc with a ring; the darks are one
dark and not three bands; the cast shadow is attached to the egg. Three faults, two of
them the agent's own apologies: the cast shadow ends in a hard corner at its lower
left; the band round the bowl is a smooth halo of a different surface from the stumped
rows, plain at full size; and the table's rows show at two angles as a hatching at full
size, with the far plane mottled. The bowl's interior shade is faint, and the lost edge
is lost into not much.

### What this run says of the guide

Run 3's two folded candidates, against this run:

1. **A list that falls to its ends reads a grade lighter**: **held** in the mid-tones,
   where the agent measured it and planned by it, and **not carried to the darks**,
   where seven arcs at bells falling to `0.5` read `0.78` of the way and the agent only
   then went to `6B`. The rule sits in *Two tips*; step 7 does not repeat it.
2. **Any run cut round a thing stops half a stroke and a few pixels short of it**:
   **held**. The rows were cut 40 px round the bowl (half of `0.07` and four pixels)
   and the light stayed at 100% paper through the table pass; what took the light
   afterwards was stumps and edge strokes, which the rule does not name, and the
   agent's first candidate asks for the stump to be cut the same way.

Run 2's seven, carried: the hard edge in the mass's own value **held** again (the agent
dropped a rim stroke that read as *the guide's dark ring*); the budget as reserve
**held** (287 left, named as not mendable by marks); `darks:` as an area **held**
(`0.85` in two `6B` arcs after seven softer ones missed it); `compare(s.plan())`
**held** (called after every pass); the band beside a thing **tested for the first
time**, since the egg's top sits against the bowl's far interior, and it held as a
procedure while reading as a halo ring, which is a new fault of its own.

Of the agent's ten candidate rules, after measuring:

1. **A stump along a path is cut round the light as a row is, and a stump over a shape
   shows the shape's outline where it stops** (measured by the `lightest:` line, 81%
   to 100%, and seen).
2. **Count the stumps and edge strokes laid beside the light before laying them**;
   each took 2 to 5% of its paper (measured by the line).
3. **Step 7 should repeat the bell-list rule for the darks** (measured: `0.78` then
   `0.85`).
4. **A cast shadow is laid as arcs attached to the thing that casts it**, from contact
   to contact, not as concentric arcs of a shifted shape (seen in two rehearsals).
5. **A `6B` list's ends want about `0.1`**, since `6B` at half pressure is black (seen;
   the calibration table says `6B` at `0.5` reads `0.14`).
6. **The signature wants a heavier tick over a tone**: the guide's example lands on
   paper and not over a stumped tone (measured above, 5 to 9 units against `0.37`).
7. **A tone of `0.70` to `0.85` is `2H` held off and stumped twice** (measured: `0.77`,
   `0.73`, `0.77` on `bowl_lit`).
8. `boxes:` silent in a drawing's check: an engine candidate, now from two runs.
9. The `plan:` line carrying every place's reading: an engine candidate, from two runs
   (run 3's fifth candidate asked for the number by another route).
10. An edge stroke darker than its mass is a dark ring: section 6 says it since run 3,
    and the agent found it by the rule's own words in a rehearsal; the candidate is to
    say the rim's inner edge against a stumped shade needs no stroke at all.

Each a hypothesis until a fifth session draws against it.

For the engine and the check, the four candidates from run 3 stand, two of them now
asked for by two runs: `boxes:` silent in graphite, and the `plan:` line carrying each
place's reading. Nothing new for the engine from this run.
