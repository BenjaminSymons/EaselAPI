# EaselAPI: instructions for Claude sessions

## Status: severed from upstream (2026-10-10)

This repository is a graphite drawing engine for LLM agents. It was forked from
`Gemberkoekje/EaselAPI` (the `upstream` remote, easel-paint) and is no longer tracking it.

- Do not fetch, merge, rebase onto, cherry-pick from, or open pull requests or issues
  against `upstream`. Its last commit in this history is `f416bcf` (#101). Everything
  after it is this project's.
- Do not plan around upstream. Its rounds, its painting goldens and its painting guide
  exist to serve painting, and painting is not this project's product.
- The product is drawing, with graphite as the only medium. Where a change serves a
  drawer, make it, even if it changes shared code, a painting output or an old rule.
- Painting code stays in the tree and its tests still run. Nothing new is built for
  painting. If a drawing change moves a painting golden, look at the new image and
  regenerate the golden; do not contort the drawing change to keep it.

## What no longer binds

- **"Add capability beside the old path, never through it"** (`LESSONS.md`, *Engine
  decisions that are load-bearing*). Superseded for drawing. Change shared code in place
  when that is the right design for a drawing.
- **"The engine refuses nothing"** (`REFERENCE.md`, `Session` docstring). Superseded for
  graphite: a paint verb on a graphite session raises. Painting sessions are unchanged.
- **A word ceiling on `DRAFTSMAN.md`.** Removed 2026-10-10: a ceiling set above the file's
  size made every measured rule displace another measured rule. Its growth is held by
  `scripts/check_guide_overlap.py` (one home per rule) and by measurement. The card,
  `The first hour`, is still held to `CARD_WORDS`.
- **Replaying an old drawing as the record of what it looked like.** A drawing's PNG and
  films are its record. If a later change alters how a mark renders, replay of an older
  `.easel` no longer reproduces that picture. The drawing's `NOTES.md` says what was
  measured, and when.

## What still binds

- **Measure before building, and before writing a rule into the guide.** A guide claim is
  a hypothesis until a fresh session draws against it. A check that cannot fire on a real
  log is worse than none (`SPEC-REVIEW.md`).
- **Every mark is in the log, and the log is the source of truth.** Strokes are seeded per
  stroke index; `replay()` and `undo` depend on that. Looks, rehearsals and pass scripts
  are kept beside the log, never in it.
- **One home per rule in the guides.** `scripts/check_guide_overlap.py` and the block
  checker run in the suite.
- **The card budget**: `CARD_WORDS` (1,400) on `DRAFTSMAN.md`'s `The first hour`.
- **Docs**: no em dashes and no arrow characters in shipped docs (the suite enforces it, and the Windows
  console is cp1252). Use a plain dash.
- **Regenerate goldens only after looking at them.**

## Layout

- `src/easel/` is the engine. Graphite lives in `graphite.py`, the `line` and helper verbs
  in `session.py`, the channel in `canvas.py`, the film in `film.py`, the MCP server in
  `mcp_server.py`.
- `DRAFTSMAN.md` is the drawing guide. `PAINTER.md` is the painting guide and is frozen.
- `SPEC.md` is the graphite spec as written on 2026-10-07. It is a record of intent, and
  `SPEC-REVIEW.md` records where the build differs.
- `drawings/egg_in_bowl*/` are the test drawings. A new drawing gets the next number and a
  `NOTES.md` header written before its first stroke.
- `CHANGELOG.md` *Unreleased* holds the graphite work. Nothing is released yet.

## Commands

```powershell
$env:PYTHONPATH = "src"
py -3.14 -m pytest -o addopts=""           # the full suite, about nine minutes
py -3.14 -m pytest -o addopts="" tests/test_reference.py tests/test_draftsman.py
```

Read the summary line before chaining anything after `pytest`. `tail` hides its exit code.
Pytest is installed on 3.14 only.

## Git

- Branch `main`. `origin` is `BenjaminSymons/EaselAPI`.
- Commit or push only when asked.
- Each commit message names the step or round it belongs to, as the history does.
