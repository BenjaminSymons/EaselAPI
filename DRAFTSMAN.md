# Drawing with Easel

You are about to draw, in graphite, on paper. This file is the method for that medium:
the loop, the order of work, the mistakes you will make, nine exercises, and a
checklist. It is the drawing's `PAINTER.md`, and you read one of the two, never both:
the paint guide's order of work is wrong for a pencil, and its rules about brushes have
no verb here. Read *The first hour*, draw the nine exercises, and begin; keep this file
open as you draw, and open the other two when a situation calls for one.

| File | What it holds | When |
|---|---|---|
| **`DRAFTSMAN.md`** - this one | the method for graphite | now, and open beside you while you draw |
| [`REFERENCE.md`](REFERENCE.md#the-graphite-medium) | every fact on one page; *The graphite medium* is the section | when you want to look something up |
| [`CALIBRATION.md`](CALIBRATION.md#the-graphite-medium) | the measurement behind every number quoted here | when a number is the question |

`RECIPES.md` and `PAINTING.md` are about paint, and have no verb here.

**First: have you chosen a subject?** If you have, the finished drawings in
[`drawings/`](https://github.com/Gemberkoekje/EaselAPI/tree/main/drawings) are open
to you, in the repository: each with the pass scripts that built it, the prelude of
shapes beside them, the two films, and the draftsman's own notes. **Decide first; the
drawings are not for choosing by.** Each names its subject, and a named subject
chooses for you.

---

## The first hour

**What this is.** A pencil lays value on paper, gated by the paper's tooth, and
saturates toward its grade's own darkness: six grades, `4H` to `6B`, each with a
ceiling, so a `2H` cannot be pushed to a `6B` black however many passes you lay. There
is no paint over it. **A mark stays**: a stump moves it about, an eraser lifts most of
it and leaves a ghost, and nothing covers it. You work light to dark, in passes, and you
look between them.

```python
from easel import Session, cell, span, ellipse, polygon

s = Session(1024, 768, medium="graphite", seed=7, budget=400, capture=True)
```

Coordinates run `0..1` from the top-left; a place is `cell("D5")`, `span("C3", "F6")`,
or a shape. The paper is white `cartridge` unless you say otherwise, and `look()` is
greyscale. **The `budget=400` is this example's**, and it is twice what one subject with
three or four value masses has cost at this size, laid the way this page says: two
drawings of one spent 154 and 138, and the rest is reserve.

**The loop.** **Look every 5 to 15 strokes.** `s.look()` returns the path of a PNG,
and you open it. **Rehearse every pass before you pay for it**: `s.rehearse(plan)` lays
the plan on a copy and shows the result, and `easel run pass.py --rehearse` does it for
a script. A rehearsal is a look, and the check counts it: over fifteen marks with no
look between them is a finding; a helper call counts once.

**What a mark costs.** `line` is one. `hatch`, `crosshatch`, `scribble` and `tone` are
one *per line laid*, and at the side's default width that is **ten a grid cell** for
`tone` or a side `hatch`, fifteen for a point hatch; a 1024x768 sheet is sixty-four
cells, so a plane cannot be toned cell by cell on a budget of 400. `contour`, `stump`,
`kneaded` and `plastic` are one each. The envelope, the looks, the rehearsals and the
plan cost nothing.

```python
plan = [{"hatch": ellipse((0.5, 0.55), 0.2, 0.14), "grade": "2B", "tip": "side",
         "pressure": 0.8}]
s.cost(plan)                  # what it charges
s.rehearse(plan)              # what it would look like
s.hatch(ellipse((0.5, 0.55), 0.2, 0.14), grade="2B", tip="side", pressure=0.8)
```

**The order. Not optional, and most of the method.**

1. **Draw the envelope in pencil.** `s.pencil()` is free and is not the drawing: it is
   the arrangement, moved until it is right, and the export leaves it out when you
   ask. `s.thumbnail({shape: value})` shows the masses flat and small, free.
2. **Lay the big planes as rows of broad side strokes by hand**, a hard grade leant on,
   and one stump each. `line(row, "2H", pressure=0.7, tip="side", width=0.07)` in rows
   at two angles twenty degrees apart; sixteen strokes for a far plane, fifty for a near
   one, `stump(place, 1.0)` once over each. Not `tone()`: that is ten lines a cell.
3. **Lay each curved passage along its own shape**: arcs of its outline scaled or
   offset, cut into runs a sixth of a stroke short of whatever stands in it, the
   pressure varying along the arc. Side strokes hatched *across* a curved shape end on its outline in steps, and a
   row of steps is a staircase.
4. **Check the values before anything else.** Write the plan down where the check can
   see it, read the places back after every pass, and **read medians, not means**: the
   check reads a place by its median, and `sample()` is a mean colour of whatever is in it.
5. **Then the mid-tones**, each passage along its own form, a stump along the arcs to
   close the tooth.
6. **Edges last but one.** A hard edge is a narrow side stroke laid last with its
   centre a pixel or two inside the line, in the mass's own value and not a hard grade
   leant on; a lost edge is two tones of one value butting on the line and one stump
   dragged across the join.
7. **Darks last, and leave them unstumped.** A stump lightens what the check reads by
   three to fifteen hundredths, more the more holes it has to spread. The darkest mass
   is a `4B` or `6B` leant on, laid after every stump near it; the closing check says
   how far the darks reached.
8. **Highlights are paper never touched.** Plan them as places no line crosses, and
   build the drawing round them. An eraser is a repair with a residue, for a passage
   that went wrong, not the way a light is made.

```python
far = polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 0.33), (0.0, 0.35)], name="far")
for y in (0.06, 0.12, 0.18, 0.24, 0.30):                    # a plane: rows by hand
    s.line([(-0.02, y), (1.02, y)], "2H", pressure=[0.55, 0.80], tip="side",
           width=0.07, smooth=False, note="far")
s.stump(far, strength=1.0)                                  # one stump closes the rows
s.look()
mass = ellipse((0.5, 0.6), 0.16, 0.12)
s.thumbnail({far: 0.70, mass: 0.42})                        # the masses flat and small
s.contour(mass, grade="HB", pressure="taper", tip="point")   # one line, corners kept
s.kneaded(cell("B2"), strength=0.5)      # lifts half; the ghost stays
```

**Before the first stroke.** Decide which mass is the light and which is the dark, and
say so: `s.plan(values={far: 0.70, ...}, lightest=mass, subject_share=0.45,
why=...)`. The plan's places are read by their medians after every pass, the light's
line says how much of it is still paper never touched, and `s.checklist()` quotes your
`why` back at the end. **Count the rows in the envelope** while it is still free: a
drawing's planes are laid in rows, and the check says so after a pass of them; two
angles, and a passage crossing them along its own form, is the answer, and
`s.plan(bands="subject")` is for a subject that runs that way.

**Six mistakes, each with its fix beside it.**

| The mistake | What it looks like | Do this instead | Where |
|---|---|---|---|
| **A soft grade held lightly** | a field of white holes; a plane a tenth darker than planned once the holes are closed | an even tone is a hard grade leant on: `2H` at `0.7` to `1.0`, `HB` at `0.9`; the stump closes the rest | *What you are bad at*, below |
| **Hatching across a curved shape** | side strokes ending on the outline in steps; a staircase down the side of a form | arcs along the shape's own outline, scaled inward, cut into runs round what stands in it | step 3 above |
| **Toning a plane with `tone()`** | a ground that costs the budget | rows of `line(..., tip="side", width=0.07)` by hand and one stump | step 2 above |
| **Stumping the darks** | darks laid at `0.9` of a `6B` and read at `0.26`; `darks:` under `0.80` at the end | lay the darks last, after every stump near them, and leave them | step 7 above |
| **Erasing into the light** | a highlight that reads as a value, with a ghost in it | plan the light as paper no line crosses; `kneaded` for a passage that went wrong, held to a place that excludes what is to be kept | step 8 above |
| **Repairing a passage that has failed twice** | a third treatment of one passage, dearer than the last | a passage that has failed twice was laid into the wrong shape; go back to the envelope, which is free | *What you are bad at*, below |

**At the end, `s.checklist()`** answers each line that has a number behind it and
leaves three it cannot, which are at the end of this file.

**Now draw the nine exercises** at the end of this file, and start.

---

## Getting started

`medium="graphite"` is a declaration the file keeps: the paper defaults to `cartridge`,
every `look()` is a values view, and the check reads the drawing against the box of
pencils rather than the box of paints. Textures: `cartridge`, `smooth`, `linen`,
`rough`; the paper is white, and its bare value reads `0.957`.

On a sheet whose sides differ, one number is two distances: both axes run `0..1`. A
line's width and a side stroke's are fractions of the **long side**.

**The box.** The grade is the value a passage can reach, `4H` at `0.35` of the way to
black up to `6B` at `0.96`; the pressure is the width, the tooth and how fast it gets
there, and **pressure is worth about a grade** in the middle of the box. The grades at
three pressures are a table in `REFERENCE.md` and measured in `CALIBRATION.md`.

**Two tips.** `tip="point"` is a line at the grade's own width, widening under pressure
as the grade allows. `tip="side"` is the lead laid over, a mark `0.024` of the long side
wide unless `width=` says otherwise, following the stroke's direction, riding on the
peaks of the tooth: how a mass is laid. A pressure list on a hand-laid `line()` is read
**along the stroke**, so a row laid right to left wants its list turned round; the
helpers do that for their own flipped passes. **A side stroke at one pressure ends in a
block at both ends**, and a short one reads as a rectangle: a stroke in the open, and
every arc, wants a list that falls to its ends, which fade over their last thirty pixels.
**A list that falls to its ends reads about a grade lighter than its peak**, so a passage
laid that way wants the next softer grade, or its peak leant on.

---

## The workflow

The card's eight steps, with the mechanism under each.

### 1. Draw the envelope in pencil

`s.pencil()` lays the free underdrawing in the `sketch` channel; the drawing itself goes
over it in `line()`, in a channel of its own. `export(path, sketch=False)` leaves the
envelope out, and the check's `pencil:` line says how much of it still shows.

**Before the first mark, write one sentence saying why this subject.** Then draw the
arrangement, look, move it, draw it again; `s.thumbnail({shape: value})` is the masses
flat and small, which is where a silhouette reads or does not. Put the shapes, named,
in a `prelude.py` for every pass to lay to. Decide the light's direction now and draw
every round thing's terminator in the envelope: which half is in shade decides which
edge is lost.

**Build a place to exclude what is to be kept.** No helper takes `clip=`, and a stump
or an eraser acts on everything under the place it is handed: a lift over a floor took
the cast shadow lying on it down by `0.29`. The polygon you hand the eraser is the
drawing's only hold.

### 2. Lay the big planes as rows by hand

**What a plane costs.** `tone()` costs ten lines a grid cell; a plane of twenty cells
is two hundred. `hatch()` with the side costs the same. A plane is laid instead by hand,
as the card's example and exercise 3 lay one.

**An even tone is a hard grade leant on, not a soft grade held lightly.** The paper's
tooth is loud: `HB` at `0.5` leaves 18% of a cell bare paper, `2B` at `0.5` 4%, and the
holes read as a field of white points at full size. `2H` at `1.0` leaves 2% and `HB` at
`0.9` none. Hand-laid at `width=0.07`, `2H` at `0.55` to `0.80` reads about `0.70` and
`HB` at `0.55` to `0.72` about `0.52` after the stump, which is the whole range a far and
a near plane want; a pressure list along each row makes the plane lighter toward its
light. **A run that ends at a thing stops a sixth of the stroke's width short of it**,
12 px at `0.07`, since a side stroke's value runs that far past its last point; **a run
that passes beside a thing keeps half the width clear**, 35 px at `0.07`, and `hatch`
cuts its paths, not its widths. The band beside the thing is laid
in the thing's own pass, along its silhouette, as one layer where the rows are two, and
**it stops where a second thing standing in the first breaks the silhouette**: a band
and an edge stroke each laid across that crown cost two lifts to take back.

**One stump at full strength closes the rows**; a second evens the mottle a single
stump leaves over a large place. A stump over a plane moves its mean by two hundredths
and its median by about six, so read the plane after the stump, not before.

### 3. Lay each curved passage along its own shape

A side stroke that ends on a curved outline ends there at a different place on every
row, and the ends read as steps. **Build the passage as arcs of its own shape**, the outline scaled toward the centre or grown away
from it, each arc a `line()` with a pressure list that is heavier where the form turns
from the light, cut into runs round whatever stands in it. For a hollow thing, the arcs
run round the inside; for a form, the arcs are cross-contours, and each is shorter than
the one before so that their ends trace the terminator; exercise 5 lays one.

A silhouette made of two shapes is one closed run of points round both, or it leaves a
notch of paper where they meet.

### 4. Check the values before anything else

**Plan the values as numbers**, and write them down where the check can read them:

```python
from easel import Session, span

s = Session(1024, 768, medium="graphite", seed=4)
far, near = "A1:H3", "A4:H8"               # strings; span() has no name
s.plan(why="the light is the paper, and everything else is drawn to make it read as light",
       values={far: 0.70, near: 0.52}, lightest=far, subject_share=0.45)
s.hatch(span("A4", "H8"), angle=0, grade="HB", pressure=0.9, tip="side", width=0.07)
print(s.report(since=0))        # the plan, the light, the values and the paper, read
```

After every pass the check says which places read within `0.10` of what was promised,
the sign being the drawing minus the plan, and which place is lightest. **A place reads
by its median**, so a shade polygon bowed to take in the half-tone reads the paper in it
and not the shade; the first drawing read means through `sample()` all session and got
`0.63` where the check read `0.49`. Two places planned within `0.10` that touch are
named at registration: that pair is a lost edge, meant or not. **The `plan:` line
carries every place's reading**, and `s.compare(s.plan())` draws the heat map. Name
every place; one handed over bare prints as `place 1`.

**The stump moves the number**, by what the holes let it spread: the median moves
`0.03` lighter under a stump at full strength on rows leant on, `0.06` on rows laid at
`0.55` to `0.80`, and `0.11` to `0.15` on a toned patch, because a toned patch is dark
pixels and white holes and the median sits on the dark ones until the stump spreads
them. So a passage that will be stumped is laid darker than it should read, by that
much, and a value the plan names is read after the stump.

### 5. Refine the mid-tones

The grade for a half-tone is a harder one leant on, not a softer one held off: `2H` at
`0.85` is the half-tone that turns into the light, `HB` at `0.95` the tone beside it, and
a `2B` at `0.9` the core. One stump along the arcs closes the tooth between them; a
stump dragged along a path is biased along it, and over a shape it is worked every way.
**A tone between `0.70` and `0.85` is `2H` held off and stumped at full strength
twice**; it is speckle until the second stump.

### 6. Edges: lost and found

**A hard edge is a narrow side stroke laid last**, after any stump near it: thirteen
pixels wide at `pressure=0.9`, along the line, with its centre a pixel or two inside the
outline, because the tooth leaves a line of paper speckle along a stroke whose centre
sits on it. **It is laid in the mass's own value**, the grade and pressure that read as
the mass, narrow: a `2H` at full pressure reads `0.58`, and round a plane at `0.67` that
is a dark ring, not an edge. **A lost edge is two tones of one value butting on the line and one stump
dragged across the join**, and nothing else: two values under `0.10` apart are already
one mass where they meet. A soft edge is a stump dragged along the line once.

### 7. Darks last, unstumped

The acceptance criterion for a finished drawing is a darkest value `0.80` of the way from
the paper to black, which is a `2B` at full pressure twice, a `4B` once, or a `6B` at
half pressure. **`darks:` reads an area**, the darkest half-percent of the sheet, about
four thousand pixels on this one, so the dark is a place laid once at the grade that
reaches the value, and a dark laid over a dark adds none of it. **A dark laid with a
list that falls to its ends wants the softer grade**: seven `4B` arcs at bells to half
read `0.78` of the way, two `6B` at a bell to `0.9` read `0.85`. Lay
the darks after every stump near them, and leave them.

### 8. Highlights are paper never touched

A highlight lifted is a value: an eraser leaves a ghost, and a `6B` passage lifted hard
reads `0.74` where the paper reads `0.96`. `plastic` takes most of a passage in one pass
with a clean edge; `kneaded` takes a share with a soft one; both are charged, and both
act on everything under the place. **Every stump or edge stroke beside the light takes
two to five percent of its paper**: cut a stump's path round the light by half its
width, as a row is, and count the treatments before laying them; the `lightest:` line
says what each took.

---

## What you are bad at, and what to do instead

**You cannot reason in pixels.** Look with the grid on, say which cells a mass sits in,
and lay to the cell or to a shape built from landmarks.

**You will hold a soft pencil lightly to get a light tone**, because that is what the
words say, and the paper will fill with white holes. The pressure, not the grade, is what
fills the tooth; the light tone is the hard grade at full pressure.

**You will hatch across a curved shape** because `hatch()` takes a shape, and get a
staircase at its outline. Arcs along the shape, by hand, are the passage; the helper is
for a plane.

**You will stump everything**, because the stump is the only thing that quiets the
tooth, and the darks will come out a step lighter than you laid them. Stump the planes
and the half-tones; lay the darks after, and leave them.

**You will read a mean and believe it.** `sample()` averages whatever is under the
place; the check reads medians and says when a tenth of a place sits far from its own.
Read the check.

**You will repair a passage that has failed twice.** The rule is a number so that it
holds at the moment it is needed: **a passage that has failed twice was laid into the
wrong shape**, and the shape is free to redraw and the only thing that is.

---

## Nine exercises

Give each `look()` a `path=` of its own.

**1. The box of pencils.** Every grade at three pressures, on the side. Look at it at
full size: which grades speckle at which pressure, and where each one stops.

```python
from easel import Session, GRADES

s = Session(900, 450, medium="graphite", seed=1)
for i, grade in enumerate(GRADES):
    y = 0.1 + i * 0.15
    for j, p in enumerate((0.3, 0.6, 1.0)):
        x = 0.06 + j * 0.31
        s.line([(x, y), (x + 0.25, y)], grade, pressure=p, tip="side", width=0.05,
               note=f"{grade} at {p}")
s.look(scale=None)          # full size: the tooth is the point
```

**2. One line, six pressures.** On the point the pressure changes the width as well as
the darkness; on the side only the darkness and the tooth.

```python
from easel import Session

s = Session(900, 500, medium="graphite", seed=2)
for i, p in enumerate(["taper", "press_in", "lift_off", "even", "swell", [0.1, 1.0]]):
    y = 0.12 + i * 0.15
    s.line([(0.08, y), (0.46, y)], "2B", pressure=p, tip="point", width=0.012, note=str(p))
    s.line([(0.54, y), (0.92, y)], "2B", pressure=p, tip="side", note=str(p))
s.look()
```

**3. A plane, laid and read.** Rows by hand at two angles, read before and after the
stump, against a plan. The median moves lighter under the stump; the mean barely does.

```python
from easel import Session, span

s = Session(900, 600, medium="graphite", seed=3)
plane = span("B2", "G7")
s.plan(why="a plane that reads as one tone", values={plane: 0.60})
for k, (y, x0, x1) in enumerate(((0.16, 0.12, 0.88), (0.24, 0.10, 0.80), (0.33, 0.16, 0.90),
                                 (0.41, 0.11, 0.84), (0.50, 0.12, 0.89), (0.58, 0.10, 0.78),
                                 (0.67, 0.15, 0.88), (0.75, 0.12, 0.82))):
    row = [(x0, y), (x1, y)]         # rows closer than their width, no two alike
    s.line(row if k % 2 == 0 else row[::-1], "HB", pressure=0.9, tip="side", width=0.06,
           smooth=False)
for k, (x, y0, y1) in enumerate(((-0.05, 0.14, 0.80), (0.10, 0.30, 0.76), (0.29, 0.14, 0.74),
                                 (0.43, 0.40, 0.80), (0.63, 0.14, 0.70), (0.78, 0.26, 0.80))):
    row = [(x, y0), (x + 0.36 * (y1 - y0) / 0.66, y1)]
    s.line(row if k % 2 == 0 else row[::-1], "2H", pressure=1.0, tip="side", width=0.06,
           smooth=False)                 # a second angle, and a second grade
print(s.report(since=0))                 # the plan line before the stump
s.stump(plane, strength=1.0)
print(s.report())                        # and after it: the median has moved
```

**4. A hard grade leant on, a soft grade held lightly.** The same cell twice. Look at
full size: one is a tone with a few holes, the other a field of white points.

```python
from easel import Session, cell

s = Session(900, 450, medium="graphite", seed=4)
s.hatch(cell("C4"), angle=0, grade="HB", pressure=0.5, tip="side", note="soft, light")
s.hatch(cell("F4"), angle=90, grade="2H", pressure=1.0, tip="side", note="hard, leant on")
s.look(scale=None)
print(s.report())                        # the values line, and the paper line
```

**5. Across a shape, and along it.** The same oval twice: hatched across with side
strokes, and laid as arcs of its own outline. Look at the outline of each.

```python
import math
from easel import Session, ellipse

s = Session(900, 450, medium="graphite", seed=5)
s.hatch(ellipse((0.27, 0.5), 0.17, 0.32), angle=0, grade="2B", pressure=0.8, tip="side",
        width=0.05)                      # across: every row ends on the outline
cx, cy = 0.73, 0.5
for k in (1.0, 0.85, 0.7, 0.55, 0.4):    # along: the outline, scaled inward
    arc = [(cx + 0.17 * k * math.cos(math.radians(t)), cy + 0.32 * k * math.sin(math.radians(t)))
           for t in range(-80, 101, 8)]
    s.line(arc, "2B", pressure=[0.4, 0.9, 0.9, 0.4], tip="side", width=0.05, smooth=False)
s.look()
```

**6. What the stump does to the number.** Tone a cell to a value, read it, stump it,
read it again.

```python
from easel import Session, cell

s = Session(900, 450, medium="graphite", seed=6)
s.plan(why="one patch", values={cell("D4"): 0.45})
s.tone(cell("D4"), 0.45, grade="2B")
print(s.report(since=0))                 # the plan line: inside 0.10
s.stump(cell("D4"), strength=1.0)
print(s.report())                        # and now it reads lighter, by a tenth or more
s.look(region="C3:E5", scale=None)
```

**7. Three edges.** Hard, soft and lost, side by side; notice where your eye lands.

```python
from easel import Session, Region

s = Session(900, 300, medium="graphite", seed=7)
for i, (left, right, angle) in enumerate(((0.40, None, 20), (0.40, None, 110),
                                          (0.50, 0.56, 65))):
    x0 = 0.05 + i * 0.31
    s.tone(Region(x0, 0.2, x0 + 0.14, 0.8), left, grade="2B", angle=angle)
    if right is not None:
        s.tone(Region(x0 + 0.14, 0.2, x0 + 0.28, 0.8), right, grade="HB", angle=angle + 90)
    s.look(region=Region(x0 - 0.02, 0.1, x0 + 0.3, 0.9))     # the loop, between panels
edge = 0.05 + 0.14                       # the first panel's line, in x
s.line([(edge - 0.004, 0.2), (edge - 0.004, 0.8)], "2B", pressure=0.9, tip="side",
       width=0.013, smooth=False)        # hard: laid last, its centre just inside
edge = 0.36 + 0.14
s.stump([(edge, 0.2), (edge, 0.8)], strength=0.8, width=0.03)     # soft: along it
edge = 0.67 + 0.14
s.stump([(edge - 0.03, 0.5), (edge + 0.03, 0.5)], strength=0.8, width=0.05)  # lost: across
s.look()
```

**8. The eraser and its ghost.** A toned strip with a dark line in it, lifted two ways.
Everything under the place lifts, the dark line too, and neither comes back to paper.

```python
from easel import Session, Region

s = Session(900, 300, medium="graphite", seed=8)
strip = Region(0.15, 0.38, 0.85, 0.62)
s.tone(strip, 0.55, grade="HB")
s.line([(0.2, 0.39), (0.8, 0.61)], "6B", pressure=0.9, tip="point", width=0.01)
s.look()                                 # before the lifts
s.kneaded(Region(0.35, 0.33, 0.55, 0.67), strength=0.5)
s.plastic(Region(0.65, 0.33, 0.80, 0.67))
s.look(scale=None)
print(s.report())                        # the paper line: never touched, and lifted
```

**9. Draw, rehearse, draw.** The whole loop, on an abstract shape: the envelope, a
rehearsal of the pass, the pass, and a look with the envelope left out.

```python
from easel import Session, cell, polygon

s = Session(900, 600, medium="graphite", seed=9)
s.mark("a", *cell("C3").point(0.5, 0.5))
s.mark("b", *cell("F3").point(0.5, 0.5))
s.mark("c", *cell("D6").point(0.5, 0.5))
shape = polygon([s.pt("a"), s.pt("b"), s.pt("c")])
s.pencil(shape, pressure=0.6)            # the envelope, free
s.look()
plan = [{"hatch": shape, "grade": "2B", "tip": "side", "pressure": 0.8, "angle": 20}]
s.rehearse(plan)                         # what the pass would look like
s.hatch(shape, angle=20, grade="2B", tip="side", pressure=0.8)
s.look(sketch=False)                     # the drawing without its envelope
```

---

## When you call it finished

The check can say a drawing is not *wrong*; finished is another question. The lines
with a number behind them answer themselves:

```python
print(s.checklist())          # or `easel check drawing.easel` from a shell
```

`plan:` and `lightest:` against what you declared, with how much of the light is paper
never touched; `values:` against the box of pencils on this paper; `edges:`; `paper:`,
the share of the sheet no line has crossed; `pencil:`, how much of the envelope still
shows; `darks:`, how far the darks reached; `looks:`, the longest run laid with no
look between them, and a finding when it passed fifteen; `unspent:`. What each measures is
one table under *The graphite medium* in [`REFERENCE.md`](REFERENCE.md#the-graphite-medium).

**Then the three it cannot ask**, printed as questions with your own `why` quoted back,
which are the ones to answer slowly: whether the thing you measured most carefully is
still part of the picture when you cover it, and whether the light is where you planned
it; which passage you would apologise for, because the marks left are for that one;
and whether the reason you chose the subject is still there when the drawing is looked
at small, `s.look(scale=256)`, rather than in a crop.

**The budget unspent is not a finding by itself.** Three drawings of one subject
stopped under 150 of 400 with nothing left to mend, so a drawing's `unspent:` line is
the number alone. The rest goes to the passage you would apologise for, if there is one, and
nowhere else.

## Sign it

When you have decided it is finished, sign it: up to five marks that do not come out of
the budget, so long as each carries `note="signature"`. A mark, not a name: small, in a
corner, close in value to what it sits on. **A dot is a two-point tick**, since a
one-point line lands nothing, and **over a tone the tick is leant on**: `HB` at `0.6`
lands on paper, not on a stumped corner.

```python
s.line([(0.90, 0.95), (0.93, 0.942)], "HB", pressure=0.9, tip="point", width=0.004,
       note="signature")
s.export("drawing.png", sketch=False)    # without the envelope
```

---

## Working from a shell instead

The same thing from the command line. The state lives in one `.easel` file, and
`python -m easel` works where `easel` is not on the path.

```bash
easel new drawing.easel --medium graphite --size 1024x768 --seed 7 --budget 400 --capture
easel run drawing.easel pass1.py --rehearse       # against a copy, committing nothing
easel run drawing.easel pass1.py                  # `s` and the shapes are already in scope
easel look drawing.easel --grid
easel look drawing.easel --region D4 --scale 0    # a crop, at full size
easel check drawing.easel
easel export drawing.easel drawing.png --no-sketch
easel film drawing.easel drawing_looks.mp4 --stroke-motion          # the looks held
easel film drawing.easel drawing_strokes.mp4 --hold-looks 0         # the marks alone
easel film drawing.easel --html viewer                              # scrubs to any mark
```

A script given to `easel run` has `s` and the whole API in scope, and a `prelude.py`
beside the session file runs first, in the same scope: the shapes, the helpers and the
plan live there. `--capture` keeps every look, rehearsal and pass beside the log. After
every pass `run` prints the budget line, the pass's dearest
calls, and the check. Read it before the next pass.
