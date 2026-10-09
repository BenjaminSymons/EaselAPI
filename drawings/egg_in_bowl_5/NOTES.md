# A hen's egg in a shallow bowl, drawn a fifth time

**Run 5 of `SPEC.md`'s test drawing: run 4's candidates and two lines of the check,
measured.** The same subject as the four drawings before it, a fifth seed, drawn by a
fresh session against `DRAFTSMAN.md` and the check as they stand on 2026-10-10, the
working tree after `0a4fff4`. What changed in the guide and in the check between run 4
and this run is listed under the re-measurement at the end, so that the agent's own
write-up is not steered by it. Run 4 was the only measurement of what run 3 changed in
the guide; this run is the only measurement of what run 4 changed (`LESSONS.md`: a
guide change is a hypothesis until a fresh session draws against it).

## The subject, chosen before the agent saw anything

Written here by the person running the round, before the first stroke, as the protocol
asks. The same words as runs 1 to 4, so that the five drawings differ only in the seed
and in what the agent had to read:

> **A single hen's egg in a shallow white bowl on a plain wooden table, lit from a
> window to the upper left, out of frame.** Three or four value masses: the lit side of
> the egg and the bowl's lit rim, the egg's shadow side, the bowl's interior shadow with
> the egg's cast shadow in it, and the table. One hard edge: the bowl's rim against the
> table. One lost edge: the egg's shadow side into the bowl's shadow behind it.

The drawing agent is told this subject in its brief and nothing else about the picture.
It is not the spec's example subject.

## Setup

- `drawing.easel`: 1024x768, `cartridge`, white, **seed 19**, budget 400,
  `medium="graphite"`, `capture=True`, `out_dir` `out/` -- made with `easel new` from
  this folder.
- The agent works through the shell (`easel run`, `easel look`), as the earlier runs
  did, with `py -3.14 -m easel` and `PYTHONPATH` on the checkout's `src/`, because the
  installed wheel is 0.8.0 and has no graphite. The passes are its own numbered scripts
  beside this file.
- A fresh session: the agent has not seen this repository, the spec, the review or the
  earlier runs. It is given `DRAFTSMAN.md` as its guide, the paths of the documents the
  guide points at, and told that what it reads is part of the record. It is told not to
  open the four earlier drawings' folders, `SPEC.md`, `SPEC-REVIEW.md`, `PLAN-0.9.0.md`,
  `CHANGELOG.md`, `LESSONS.md` or `SUGGESTIONS.md`.

## What the agent read, what it did, what went wrong

*Written by the agent at the end of its run, below this line; re-measured by the person
running the round after it.*

---

## The agent's write-up

**Strokes spent: 143 of 400** (97 graphite lines, 47 stumps, no erasers; 1 signature tick,
free; 18 pencil records and one `erase()` of the first envelope, free). Passes in order,
with what each cost when committed:

| Pass | Script | Cost | Rehearsals before it |
|---|---|---|---|
| 0 | `p00_envelope.py` (twice; the first erased, free) | 0 | 0 |
| 1 | `p01_table.py` - rows at two angles, 8 stumps | 57 | 1 |
| 2 | `p02_bowl.py` - the band beside the bowl, its table shadow, walls, interior shadow, 7 stumps | 24 | 3 |
| 3 | `p03_egg.py` - 8 egg arcs, 2 far-wall arcs, 4 stumps | 14 | 3 |
| 4 | `p04_edges.py` - edge band 3, edge stumps 3, hard edge 3, lost-edge stump 1 | 10 | 2 |
| 5 | `p05_darks.py` - 3 `6B` arcs under the egg | 3 | 2 |
| 6 | `p06_sign.py` - the signature and the first export | 0 | 0 |
| 7 | `p07_floor.py` - 8 floor strokes, 16 floor stumps, 8 table stumps | 32 | 2 |
| 8 | `p08_darks2.py` - 1 `6B` along the crevice under the bowl, 2 more under the egg | 3 | 3 |

16 rehearsals in all (`out/rehearse_001..016.png`). Looks: 35 named `look()` PNGs under
`out/` (crops included), 2 thumbnails, 3 `compare()` heat maps; the session's own count of
looks and rehearsals, including those inside rehearsed copies, is 106 (`s._looked`,
read with `Session.load`). The drawing was exported after pass 8 with `easel export
--no-sketch`, so the pass-6 export is superseded.

The final check's lines, from `check_final.txt`:

```
plan: 7 of 8 places inside 0.10; cast_core -0.11 (21% of it lighter by more than 0.15); inside: table_far 0.70, table_near 0.58, cast_table 0.41, egg_lit 0.96, bowl_lit 0.87, egg_shade 0.49, bowl_shadow 0.36
lightest: egg_lit reads 0.96 as a place, 0.96 at its brightest twentieth, the lightest of the 8 places planned; 79% of it paper never touched
subject: 13 of 143 marks so far (9%), against 45% planned -- behind, if the subject is finished
values: 0.42-0.85 of a box that reaches 0.04-0.96, clusters at 0.38, 0.63, 0.78; a clear light, mid and dark
edges: 29% of edges are under 2.5 px wide, median 3.9 px
paper: 1.48% of the canvas is paper never touched
pencil: the envelope still shows over 1.67% of the canvas -- export(sketch=False) leaves it out
darks: the darkest half-percentile reads 0.17, 0.82 of the way from paper to black
unspent: 257 of 400 unspent (64%) -- name the weakest passage and spend them there
```

The closing check printed no *no look between them* line. The longest run in a
committed pass, by my own count of the scripts, is 12 (the table rows, a look every
twelfth row). The check did print one during a rehearsal: 16 floor stumps in the first
rehearsal of pass 7, fixed with a look between the two rounds before committing.

## What I read, and how far

- `DRAFTSMAN.md`: whole, 560 lines, in one read, before anything else. No index; I kept
  it open and re-read *The workflow* steps 2, 6 and 7 and *Nine exercises* while working.
- `REFERENCE.md`: whole, 999 lines, in two reads. I first listed its `##`/`###` headings
  with `grep` as an index, then read both halves because the API I needed (`line`,
  `stump`, `plan`, `compare`, shapes, `Session.load`, the shell) is spread through it.
  *The graphite medium* (lines 405-510) was the section the guide pointed at.
- `CALIBRATION.md`: the heading list by `grep` as an index (4740 lines; not read whole),
  then lines 302-507 only: *The graphite medium*, *The stump and the erasers*, *The
  check, measured on the first drawing*. I went there for the grade-at-three-pressures
  table before choosing grades, as the guide says to when a number is the question.
- Nothing under `src/` or `tests/`; no `easel guide`, `explain`, `diagnose` or `demo`.
  No earlier drawing, no spec, no review.
- One thing the documents left me to discover in the engine: `Region` takes no `name=`,
  so the two table places printed as `place 1` and `place 2` (pass 1 rehearsal); I
  rebuilt them as named polygons.

## The exercises

Scripts `ex_01_box.py` to `ex_09_loop.py`, each its own `Session` with `out_dir="ex_out"`,
run as plain Python so `s` was never rebound against `drawing.easel`.

1. **The box.** At `0.3` the hard rows are nearly nothing and the soft ones are speckle;
   at `1.0` every row closes and each stops at its own darkness, `4H` a pale grey, `6B`
   near black. Matched the guide.
2. **One line, six pressures.** The point widened with pressure, the side only darkened
   and opened the tooth; `[0.1, 1.0]` fades in. Matched.
3. **A plane.** Read `0.53` before the stump and `0.56` after against `0.60` planned:
   the median moved `+0.03`, the guide's figure for rows leant on. Matched the number.
   Two things seen: the diagonal `2H` rows overshoot the span at two corners, and the
   rows still read as rows after one stump (`ex_out/ex_03_plane_after.png`).
4. **Hard leant on, soft held lightly.** `HB` at `0.5` a field of white points, `2H` at
   `1.0` a tone with a few holes. Matched.
5. **Across and along.** The hatched oval ends in steps all round its outline; the arcs
   follow the oval and their `0.4` ends are speckly. Matched.
6. **The stump's number.** `0.45` before, `+0.15` (`0.60`) after: the guide says `0.11`
   to `0.15`. Matched, at the top of the range.
7. **Three edges.** The eye lands on the hard one; the soft one blurs; the stump across
   the lost join left a visible lighter thumbprint in the middle of the panel
   (`ex_out/ex_07_edges_full.png`), which the guide does not mention. Both `tone()`
   panels at `0.40` by `2B` came out as speckle fields.
8. **The eraser.** `kneaded` at `0.5` took about half of strip and line; `plastic` took
   most and left a grey ghost of the `6B` line. Matched.
9. **The loop.** Envelope, rehearsal (cost 36), hatch, look without the envelope: the
   side hatch at 20 degrees stepped down both slanted sides of the triangle, which is the
   staircase of exercise 5 again. Matched.

## The passes

**Pass 0, the envelope (free).** The bowl as three ellipses in pixels (rim, inner edge,
belly) plus a floor line, the egg as a parametric egg rotated 18 degrees with its big end
left, the terminator as a small inner egg, the interior shadow as the near crescent
joined to a cast ellipse, the bowl's shadow on the table, and the plan: eight named
places, `egg_lit` the lightest, `subject_share=0.45`. The first thumbnail showed the egg
too small (176 px in a 614 px bowl) and `egg_lit` built with its inner arc reversed, so I
erased the free pencil and redrew: egg 210 px, bowl 580 px. The check named two planned
pairs that touch, `egg_shade`/`bowl_shadow` at `0.00` apart and `egg_lit`/`bowl_lit` at
`0.03`; both are the subject's own lost edge and single light mass, so I kept them. A
third, `cast_table`/`bowl_shadow` at `0.05`, I separated by moving `cast_table` to `0.34`.

**Pass 1, the table (57).** Fifteen horizontal rows at `width=0.07`, `2H` at `[0.50,
0.75]` to `[0.62, 0.90]` above the bowl and `HB` at `[0.50, 0.72]` to `[0.65, 0.90]`
below, lighter toward the window; twenty-two rows at 22 degrees in pixels, `2H` at `[0.72,
0.92]`; every row cut 40 px short of the bowl's silhouette (half the 72 px stroke and a
few more), 49 runs; one stump at `1.0` over four rectangles clear of the bowl and four
polygons hugging it 6 px off. The rehearsal read `table_far 0.69` (plan `0.68`) and
`table_near 0.57` (plan `0.55`), the light `100%` paper, 57 strokes; committed unchanged
(the plan's places renamed). What I saw: a 40-50 px halo of paper round the bowl with
stepped row ends, and the diagonal rows showing as a weave after one stump.

**Pass 2, the bowl (24).** The band beside the bowl as arcs along the silhouette grown 44
px (`width=0.07`) and 15 px (`0.03`), `2H` over the top, `HB` near-left, and `2B` leant
on where the bowl's shadow falls on the table, with a third `HB` layer at 88 px; the
outer wall's half-tone and the left inner wall in `2H`; the near crescent as two `HB` arcs
of the inner edge, cut round the egg; the cast shadow as four `2B` arcs of its own ellipse
under and right of the egg, cut round it; stumps along each at `1.0`, the interior at
`0.6`. Three rehearsals: the first laid nothing inside the bowl (my `arc_cut` took the
normalised points as pixels and the check said `landed nothing:`); the second read the
interior `0.60`-`0.66` against `0.45`, the table shadow `0.49` against `0.34`, and showed
the cast body as a detached blob with a hole in it; the third read `cast_table 0.38`,
`bowl_shadow 0.53`, `cast_body 0.35`, the far band `-0.03` from the table (my own
`compare()` probes). Committed on the third. Seen: block ends against the egg at the
lower left, and a 10-15 px fringe of paper speckle along the rim outside.

**Pass 3, the egg (14).** Six arcs of the egg's own outline scaled `0.85` to `0.28` over
the shade sector, each shorter than the last so the ends trace the terminator, `HB` at
the outline for the reflected light, `2B` at the core, `2H` at the half-tone; a stump at
`0.6` held to the shade polygon and one along the terminator; two `2H` arcs held off on
the far inner wall, stumped twice. Three rehearsals: `egg_shade 0.67` and the light's
paper down to `82%` (two half-tone arcs lay inside `egg_lit` as I had drawn it); `0.60`
and `58%` (I redrew `egg_lit` the wrong way, with its inner boundary at scale `0.62`);
then, with `egg_lit` the lit sector closed at the egg's centre and the two core arcs laid
a second time, `egg_shade 0.54`, light `0.96` with `80%` paper. Committed on the third;
after it 7 of 8 places were inside `0.10`.

**Pass 4, the edges (10).** First rehearsal: the narrow hard edge alone (three `0.013`
strokes 2 px outside the line, `2H`/`HB`/`2B` by side) and the lost-edge stump over a
band straddling the egg's lower-right outline; it tightened the lower rim but left the
speckle fringe. Second: a `0.02` stroke 8 px out, a stump along it 14 px out, then the
narrow edge last; the fringe closed. `edges:` moved from `35%` to `26%` under 2.5 px in
the rehearsal and read `29%` at the end. Committed on the second.

**Pass 5, the darks (3).** Three `6B` arcs along the egg's underside just outside it.
First rehearsal: bells falling to `0.4`, and a `6B` at `0.4` is still a dark block at both
ends. Second: bells to `0.15`, shorter arcs, `cast_core 0.19`, 8 of 8 places inside.
Committed. Then I signed and exported, and the closing check read **`darks: 0.26, 0.73
of the way`**, under `0.80`: the contact shadow was dark enough by its median but not by
area.

**Pass 6, the signature (free).** One `HB` tick at `0.9` on the point, 30 px, lower
right, over the stumped table; it landed (`out/p06_signature_crop.png`).

**Pass 7, the floor (32).** The export without the envelope showed the egg's lit side
gone: paper against paper. Rings of the floor ellipse, `2H` at `[0.7, 0.55, 0.6, 0.78,
0.7]`, `width=0.03`, cut 8 px short of the egg, stumped twice along the same paths cut
round the egg and the cast shadow; and a second table stump. First rehearsal: scaled
rings on so flat an ellipse overlapped four deep at the top and left gaps at the sides
(swirls, a paper patch left of the egg), and the table's second stump over the rectangles
alone left a faint rectangle. Second: rings offset 24 px in both axes plus a row across
the middle, and the hugging polygons stumped again: `floor_probe 0.83` against `0.84`
wanted, `floor_right 0.77`, the egg's crown standing. The check found 16 stumps with no
look; a look went between the rounds and it was committed.

**Pass 8, more dark (3).** One `6B` along the crevice where the belly meets the table,
under the near rim, and two more arcs widening the egg's contact shadow, all after every
stump near them. First rehearsal with two crevice strokes read `darks: 0.85` but as two
stacked bars with a block at the left end; the second, one stroke, `0.82`; the third with
the stroke's ends moved into the bowl's own shadow, `0.82`, committed. Final: `darks:
0.17, 0.82 of the way`.

## What went wrong

- **`arc_cut` took normalised points as pixels** (pass 2, first rehearsal): every interior
  run collapsed to the top-left corner. Measured: the check's `landed nothing: the
  graphite at p02_bowl.py:42`, and the look showed a bare bowl. Mine, not the guide's.
- **The rows' halo was the whole margin, not a few pixels.** The guide says a side stroke's
  half-width crosses the outline by 35 px at `width=0.07`, so a run cut 40 px short leaves
  a few pixels; what I saw in `out/p01_after_stump_crop.png` was a 40-50 px halo of paper
  with stepped ends, and the band had to be two layers 72 and 31 px wide to cover it.
  Seen, not measured in pixels; worth measuring.
- **The band's inner edge rode the tooth** and left a 10-15 px speckled fringe outside the
  rim; one 13 px edge stroke did not close it, a 20 px stroke 8 px out plus a stump along
  it plus the edge did, 9 strokes where the guide's step 6 costs 3. Seen in
  `out/p04_look_02_crop.png` of the two rehearsals.
- **The egg's lit side vanished without the envelope.** The biggest fault, and the guide
  is silent on it: *highlights are paper never touched* and *two values under 0.10 apart
  are one mass where they meet* together mean a white thing on a white thing has no edge
  unless the ground under the light is toned. The plan-pairs line said `egg_lit` and
  `bowl_lit 0.03 apart` at registration and I read it as the subject's single light mass;
  it was warning me. Measured: the floor read `0.96` before pass 7 and `0.83` after, and
  the egg's crown reads in `out/p07_look_03_nosketch.png` where it did not in
  `out/p06_final.png`. 32 strokes.
- **`darks:` is an area and I laid a line.** `cast_core` read `0.19` by its median after
  pass 5, and `darks:` read `0.26`, `0.73` of the way: about 2400 px of `6B` where the
  half-percentile wants about 3900. The guide says the number; I did not do the sum.
- **A falling list on a `6B` still ends in a block**: ends at `0.4` read as blocks (pass
  5, first rehearsal), at `0.15` they faded, at `0.05` the crevice stroke's end is still a
  small dark patch (`out/p08_look_01_crop.png`). Reasoned from the calibration table (`6B`
  at `0.25` reads `0.31`) and seen.
- **Scaled rings on a flat ellipse** overlap along the short axis and gap along the long
  one (pass 7, first rehearsal). The guide says *scaled or offset*; for a shape 250 by 68
  px only offset works.
- **A second stump over part of a place draws its boundary**: the rectangles stumped
  twice and the hugging polygons once showed as a faint rectangle round the bowl
  (`out/p07_look_03_nosketch.png`, first rehearsal). Seen.
- **16 stumps with no look** in the pass 7 rehearsal: the check caught it; fixed before
  committing. Mine.
- **`subject: 13 of 143 (9%) against 45%`**: I noted only the egg's arcs and the darks as
  `subject`, not the bowl's interior; the line counts what I chose to note and the guide
  never says what to note. The number says nothing about this drawing, and I do not know
  what it should say.
- **`Region` has no `name=`**, so two places printed as `place 1` and `place 2` until I
  rebuilt them as polygons (pass 1 rehearsal). The guide says *name every place* and shows
  `span()` in its own example, which cannot be named either.
- **The light's paper share fell from `100%` to `79%`** across the egg's two stumps and
  the floor's (`lightest:` line). The guide says every stump beside the light takes two to
  five percent; mine took 20 over three stumps, because the terminator stump and the
  floor stumps were meant to cross into it. Measured.
- **`values:` ends at `0.85`** (95th percentile) with the paper at `0.96`: the light is
  under 5% of the sheet. The line said *a clear light, mid and dark* throughout; reasoned,
  the light here is small and the line reads percentiles.
- **Exercise 7's lost edge** left a lighter thumbprint where the stump crossed the join;
  on the drawing the stump across the egg's join was held to a band and showed none that
  I could see. Seen.
- **Pressure lists on cut runs**: my `cut()` and `cut_arc()` slice the row's list per run so
  the gradient is continuous across the thing; the guide's helpers do this for their own
  flipped passes but nothing in the guide says to do it for hand-cut runs, and without it
  each run's ends would restart the list. Reasoned.
- Nothing was repaired with an eraser. Two passages were laid a third time in rehearsal
  (the bowl pass, the egg pass) before any of them was paid for; nothing committed was
  treated twice except the darks, which were extended, not relaid.

## Candidate rules

1. **Add to step 8:** *a highlight against a white ground needs the ground toned, `2H` held
   off and stumped twice to `0.82`-`0.85`, or the light has no edge* - the egg's crown read
   in no look without the envelope until the floor was toned (`out/p06_final.png` against
   `out/p07_look_03_nosketch.png`), and the plan-pairs line at `0.03` apart was the warning.
2. **Add to step 7:** *`darks:` wants about four thousand pixels at the value, which is
   three 20 px arcs 150 px long and one more 300 px long, not three* - three read `0.73`,
   six read `0.82`.
3. **Change in step 7:** *a `6B` bell must fall to under `0.15`, not merely fall* - ends at
   `0.4` read as blocks, `6B` at `0.25` is `0.31` in the calibration table.
4. **Change in step 3:** *arcs of a flat shape are offset a stroke's width in both axes,
   not scaled* - scaled rings of a 250 by 68 px floor overlapped four deep at the top and
   gapped at the sides.
5. **Add to step 2:** *the second stump covers exactly what the first did, polygons and
   all* - stumping the rectangles alone the second time drew a faint rectangle.
6. **Change in step 6:** *the hard edge is three strokes: a 20 px stroke 8 px out, a stump
   along it, and the 13 px edge last* - the edge alone left the band's 10-15 px fringe.
7. **Re-measure in step 2:** whether a side stroke's half-width really crosses its
   endpoint by 35 px at `0.07`; cut 40 px short the rows left a 40-50 px halo.
8. **Change in step 4:** *name every place with `polygon(..., name=)`; `Region` and
   `span()` cannot be named* - the guide's own `span()` example prints as `place 1`.
9. **Say what `subject` is**, or drop `subject_share` from the example: the line read 9%
   against 45% and measured only my noting habit.
10. **Keep** *look every 5 to 15*: the check's 16-stump finding in a rehearsal was the one
    time I had stopped looking, and the look showed nothing wrong, which is the point.

## The picture

Looked at small (`out/look_001.png`, 256 px): an egg lying in a shallow white dish on a
grey wooden table, lit from the upper left, the dish's shadow falling to the lower right
and the egg's shadow pooling under and right of it. The light is the paper of the egg's
crown and the dish's rim, and the rest is drawn round it, which is what I wrote I was
for; the lost edge at the egg's lower right into the dish's shadow reads, the rim against
the table reads hard. The passage I would apologise for is the dark under the egg and
along the crevice: a heavy bar, drawn to satisfy `darks:` rather than seen, with a small
block at its left end, and the one thing in the picture that looks laid rather than lit.
Second to it, the egg's lit outline against the floor at the left is soft to the point of
nearly lost; it reads at 256 px and only just at full size. The 257 unspent strokes are
not a finding: the method had no use for them, and the passage to apologise for wants
marks taken away, not added, which this medium cannot do without a ghost.

---

## The round's re-measurement

*Written by the person running the round, off the session file, the PNG and the
engine, after the agent's write-up above was finished; the agent did not see this.*

### What changed between run 4 and this run

Not named in the header, so that the write-up above was not steered by it:

- **The check**: a drawing's closing check no longer prints `boxes:`, and its `plan:`
  line carries what every place inside the threshold reads, as its median.
- **The guide**, run 4's four measured candidates: a dark laid with a list that falls
  to its ends wants the softer grade (step 7, with run 4's numbers); a tone between
  `0.70` and `0.85` is `2H` held off and stumped at full strength twice (section 5);
  every stump or edge stroke beside the light takes two to five percent of its paper,
  so a stump's path is cut round the light as a row is and the treatments are counted
  first (section 8); and the signature is leant on over a tone, the example rewritten
  to the stroke that lands (*Sign it*). Section 3's arcs example was cut to pay.

Nothing in the working tree changed during the run.

### Against the spec's pass criteria

| Criterion | Measured | Result |
|---|---|---|
| a look at least every 15 strokes | 35 looks and 71 rehearsals captured; the longest run of charged marks with no look inside it is **12**, four times, all in the table pass; no other pass over 8 | met |
| at least three grades, the side tip for the masses | four grades (`2H` 55, `HB` 24, `2B` 12, `6B` 6 marks; no `4B`); 96 of 97 graphite marks on the side, the point the signature | met |
| `compare()` within `0.10` on every planned place | 7 of 8; `cast_core -0.11` | **failed** on one place, by a hundredth |
| darkest value at or above `0.80`; paper white kept in the subject | `0.82` of the way; `egg_lit` reads `0.96`, 79% of it paper never touched | met |
| the film plays, the viewer scrubs | `drawing_looks.mp4` 1,612 frames, 134 s; `drawing_strokes.mp4` 182 frames, 15 s; the viewer built | met |
| `replay()` matches the export | the replayed log against the saved canvas: **0 levels** on every pixel | met |
| `NOTES.md` names what went wrong | above, each claim marked measured or reasoned | met |

Seven of eight: run 4 met all eight, and this run lost one place by a hundredth, the
contact dark laid a shade darker than planned to satisfy `darks:`.

### The agent's numbers, measured again

| Claim | As claimed | Measured | Held? |
|---|---|---|---|
| 143 of 400; 97 lines, 47 stumps, 18 pencil records and one erase free, one signature tick free | the check and the log | 163 records, 143 charged; `graphite` 97, `stump` 47, `pencil` 18, `erase` 1 | yes |
| longest run with no look 12, the table rows | counted off the scripts | 12 by the rule's own count, four runs of 12, all in `p01_table.py`; the check printed no line, correctly | yes |
| the closing check's lines | verbatim | `easel check` run again on the file: every line identical | yes |
| rows cut 40 px short of the bowl left a **40 to 50 px halo** of paper, where the guide's 35 px half-width should have left a few | seen in a crop | the log replayed to the end of the table pass, paper never touched in rings out from the bowl's silhouette (`probe_halo_remeasure.py`): **68% at 0 to 10 px, 22% at 10 to 20, 5% at 20 to 30, 1% at 30 to 40, none past 40**. The halo is a ragged band inside 20 px, not 40 to 50. The mechanism the agent points at is real: a side stroke's value ends 12 px past its last point at `width=0.07` (measured after run 3), so a run that *ends* at a thing and is cut 40 px short leaves about 28 px of paper before the stump, and the 35 px half-width is what a stroke running *beside* a thing crosses. Run 3's cut-margin rule, folded as *half the stroke's width and a few pixels*, conflates the two, and over-cuts a run that ends at a thing | the number, no; the mechanism, yes |
| `Region` has no `name=`; `span()` cannot be named; the guide's own example prints `place 1` | the pass 1 rehearsal | `Region(x0, y0, x1, y1, name="")` takes a name, which run 4 found by `inspect`; `span()` returns a `Region` with none, and section 4's example builds its places with `span()` while the same section says *name every place*, so the example's two places print as `place 1` and `place 2`. The guide's example is the fault, and is corrected with this run | half: `span`, yes; `Region`, no |
| three `6B` arcs read `0.19` by median and `darks:` read `0.73`; six marks read `0.82` | the lines | the closing `0.82` reproduces; the pass 5 reading is not in the log; the mechanism is the area the guide states in step 7 | yes |
| a `6B` bell with ends at `0.4` ends in blocks; at `0.15` it fades | two rehearsals | consistent with the calibration table (`6B` at `0.25` reads `0.31`); not re-measured | taken as stated |
| the light fell from 100% to 79% paper under three stumps meant to cross into it | the `lightest:` line | the closing 79% reproduces; every charged mark touching `egg_lit` in the log is a stump | yes |
| no probe scripts were needed: the numbers came off the `plan:` line | - | the folder holds no probe of the agent's; the `plan:` line in `check_final.txt` carries all seven inside places' medians | yes |

No stack-of-bars line fired, and none would have under the old rule: the table's rows
cluster 28 of 49 by chord, 57%, just under the three-fifths share. `boxes:` is absent
from the closing check and the agent did not miss it.

### The picture

A shallow white dish on a grey table lit from the upper left, its rim a speckled bright
ring, its shadow falling lower right. The egg is the weakest of the five runs': its lit
side is paper against a floor toned to `0.83` and reads only just, as the agent says;
what reads is a crescent of shade and, under it, a heavy black bar, the contact dark
laid to satisfy `darks:`, with a block at its left end, which the agent names as the
passage to apologise for. The table is a woven texture of rows at two angles with a
stump's rectangle faintly visible. Against run 4: the cast shadow and the egg's form
are both weaker, the rim and the dish's floor better.

### What this run says of the guide

Run 4's four folded candidates, against this run:

1. **A dark with a falling list wants the softer grade**: **held, and sharpened**. The
   agent went to `6B` at once, and found that a `6B` bell's ends must fall under
   `0.15` or they are blocks.
2. **A tone of `0.70` to `0.85` is `2H` held off and stumped twice**: **held**. The
   floor was laid exactly so and read `0.83` against `0.84` wanted.
3. **Every stump or edge stroke beside the light takes two to five percent**: **held
   as a warning, exceeded in the number**: three stumps meant to cross into the light
   took 21%. The rule names stumps laid beside the light, not across it.
4. **The signature leant on over a tone**: **held**. An `HB` tick at `0.9`, 30 px,
   over the stumped table landed.

Run 3's two, carried: the bell-list rule **held** (the darks); the cut-margin rule
**over-cuts a run that ends at a thing**, measured above, and is corrected with this
run: a run that ends at a thing stops a sixth of the stroke's width short of it, and a
run that passes beside it keeps half the width clear.

Of the agent's ten candidate rules, after measuring:

1. **A highlight against a white ground needs the ground toned**, or the light has no
   edge: the egg's crown read in no look without the envelope until the floor was
   toned from `0.96` to `0.83` (measured), and the plan's pairs line at `0.03` apart
   was the warning the agent read as the subject's single light. The strongest
   candidate of the run, and a fault the guide's own rules produce together.
2. **`darks:` wants about four thousand pixels at the value**, which three 150 px arcs
   did not reach and six marks did: the guide gives the area; the candidate is the
   sum.
3. **A `6B` bell's ends fall under `0.15`** (seen in two rehearsals; the table says
   `6B` at `0.25` reads `0.31`).
4. **Arcs of a flat shape are offset, not scaled** (seen; run 3's twelfth candidate
   again).
5. **A second stump covers exactly what the first did** (seen: a faint rectangle).
6. **The hard edge against a speckled band is three strokes** where the guide says
   one (seen: nine strokes against three).
7. The half-width: **re-measured above and corrected**.
8. Naming places: **corrected above**, the example rather than the rule.
9. **Say what `subject` counts**: the line measures the noting habit; a doc candidate.
10. Keep the loop: **held**, the check's one rehearsal finding was the one time the
    agent had stopped looking.

Each a hypothesis until a sixth session draws against it.

For the engine and the check: the two standing candidates from run 3 (the `unspent:`
line for a drawing, a standing longest-run line) stand; and one new: the plan's pairs
line names the lightest place and its neighbour as touching within `0.10` in the same
words as any other pair, and twice now a draftsman has read that as the subject's one
light mass; a pair that includes the declared light could say so.
