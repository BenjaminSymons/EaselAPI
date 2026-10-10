"""The film: a painting played back a mark at a time, with the painter's looks held.

The time-lapse (:meth:`easel.session.Session.timelapse_gif`) is a thinned sequence --
:data:`~easel.history.MAX_FRAMES` frames at most, by halves -- recorded as the painting
was made or rebuilt the same way. This is the other film: the log walked onto a fresh
session one record at a time (:meth:`Session._fresh_session`), a frame per mark, never
through :class:`~easel.history.History`'s frames at all, so a 400-mark drawing is 400
frames and the memory that bounded the time-lapse is never spent. Because every mark
is seeded by its index and every record carries the stream, the rebuild is the
painting to the stroke (``CALIBRATION.md``, *The log, undo, and the stream*).

Three things the time-lapse has not got:

* **the painter's looks**, held where they were taken. A session made with
  ``capture=True`` keeps each ``look()`` and ``rehearse()`` beside the log, keyed by
  the log's length at the moment (:attr:`Session.captures`); the film re-renders the
  look on the rebuilt canvas at the frame's size and holds it, so the viewer sees the
  painter stop and check, and a rehearsal's own picture -- the path not taken -- is
  shown from its PNG when it is still there;
* **stroke motion**: a graphite stroke laid over three frames, its first third, its
  second and the whole, so a long contour line visibly travels (``draw_graphite(upto=)``
  on a throwaway copy, then the record laid for real). A paint stroke has no partial
  form and arrives whole;
* **an MP4**, through ffmpeg -- the one ``pip install easel-paint[film]`` brings, or one
  on the path -- beside the GIF Pillow writes and a directory of PNG frames.

And a viewer (:func:`write_viewer`): one HTML page, plain JavaScript, a scrubber over
the frames, play at a chosen rate, and a side panel showing the mark under the
scrubber, the line of the pass script that laid it (:attr:`Session.passes`, kept by
``easel run`` and the server when the session captures) and the painter's last look
before it. Frames are separate PNGs loaded as they are shown, so a 400-mark drawing
is not 400 images in memory.
"""

from __future__ import annotations

import html
import json
import shutil
import subprocess
import tempfile
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from easel.look import render_look
from easel.regions import as_region
from easel.stroke import draw_graphite

__all__ = ["Frame", "frames", "write_film", "write_viewer", "ffmpeg_path"]

#: Where along a stroke the motion frames are taken: the first third and the second,
#: with the whole stroke as the mark's own frame making three.
MOTION_STEPS = (1.0 / 3.0, 2.0 / 3.0)
#: The caption strip under a frame, in pixels, when captions are asked for.
CAPTION_H = 22
#: How long the finished picture holds at the end, in seconds.
HOLD_LAST = 1.5


@dataclass
class Frame:
    """One frame of the film, and what it is.

    ``at`` is how many records were laid when it was taken; ``kind`` is ``"start"``
    (the bare surface), ``"mark"`` (a record laid), ``"motion"`` (a graphite stroke
    partway along), ``"look"`` or ``"rehearse"`` (a held capture) or ``"end"``;
    ``index`` is the record's index for a mark or motion; ``hold`` is how many film
    frames it is shown for at the film's rate.
    """

    image: Image.Image
    at: int
    kind: str
    index: int | None
    label: str
    hold: int = 1

    def to_json(self) -> dict:
        return {"at": self.at, "kind": self.kind, "index": self.index,
                "label": self.label, "hold": self.hold}


def ffmpeg_path() -> str | None:
    """The ffmpeg this build can run: imageio-ffmpeg's bundled one, or one on the path."""
    try:
        import imageio_ffmpeg  # noqa: PLC0415 - an optional extra
        return str(imageio_ffmpeg.get_ffmpeg_exe())
    except Exception:  # noqa: BLE001 - absent, or present and broken: the path's turn
        return shutil.which("ffmpeg")


def _frame_size(session, scale: int | None) -> tuple[int, int]:
    w, h = session.canvas.width, session.canvas.height
    if scale is None or int(scale) <= 0 or int(scale) >= max(w, h):
        return w, h
    f = float(scale) / float(max(w, h))
    return max(1, int(round(w * f))), max(1, int(round(h * f)))


def _render(canvas, size: tuple[int, int], values: bool) -> Image.Image:
    arr = canvas.values() if values else canvas.to_srgb8(impasto=False)
    if values:
        arr = np.repeat(arr[:, :, None], 3, axis=2)
    img = Image.fromarray(arr, mode="RGB")
    return img if img.size == size else img.resize(size, Image.LANCZOS)


def _letterbox(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """``img`` fitted inside ``size`` on a dark ground, its aspect kept."""
    img = img.convert("RGB")
    f = min(size[0] / img.size[0], size[1] / img.size[1])
    fitted = img.resize((max(1, int(round(img.size[0] * f))),
                         max(1, int(round(img.size[1] * f)))), Image.LANCZOS)
    out = Image.new("RGB", size, (24, 24, 26))
    out.paste(fitted, ((size[0] - fitted.size[0]) // 2, (size[1] - fitted.size[1]) // 2))
    return out


def _caption(img: Image.Image, text: str) -> Image.Image:
    """``img`` with a strip under it carrying ``text``."""
    out = Image.new("RGB", (img.size[0], img.size[1] + CAPTION_H), (18, 18, 20))
    out.paste(img, (0, 0))
    draw = ImageDraw.Draw(out)
    draw.text((6, img.size[1] + 5), text[:160], fill=(225, 225, 230))
    return out


def _pass_of(passes: list[dict], index: int) -> dict | None:
    """The captured pass whose span holds the record ``index``, if any."""
    for entry in passes:
        if int(entry.get("at", -1)) <= index < int(entry.get("until", -1)):
            return entry
    return None


def _label(record, passes: list[dict]) -> str:
    """A mark's caption: its index, kind, tool and pressure, and the pass it was in."""
    bits = [f"#{record.index:03d}", record.kind]
    if record.brush:
        bits.append(record.brush)
    if record.kind in ("graphite",) and record.params:
        tip = record.params.get("tip")
        if tip and tip != "point":
            bits.append(str(tip))
    press = record.pressure
    if isinstance(press, (int, float)):
        bits.append(f"p={float(press):.2f}")
    elif isinstance(press, str) and record.kind not in ("dry", "erase", "lift", "stump"):
        bits.append(f"p={press}")
    entry = _pass_of(passes, record.index)
    if entry is not None:
        bits.append(f"· {entry.get('scripts', '')}")
    if record.note and entry is None:
        bits.append(f"· {record.note}")
    return " ".join(bits)


def frames(session, every: int = 1, scale: int | None = 720, stroke_motion: bool = False,
           hold_looks: float = 1.0, fps: float = 12.0,
           captions: bool = False) -> Iterator[Frame]:
    """The film's frames, in order, built one at a time from the log.

    Args:
        session: the painting. Nothing about it is touched: the log is walked onto a
            fresh session of its own.
        every: a frame per this many marks. The last mark always gets one.
        scale: the frame's long side in pixels; ``None`` or ``0`` for the canvas's own.
        stroke_motion: lay each graphite stroke over three frames rather than one.
        hold_looks: how long a captured look is held, in seconds at ``fps``; ``0``
            leaves the looks out.
        fps: the rate the holds are counted at.
        captions: a strip under each frame naming the mark and its pass.
    """
    if int(every) < 1:
        raise ValueError(f"film(every={every!r}) is a frame per this many marks, so it is "
                         f"at least 1.")
    every = int(every)
    fresh = session._fresh_session(frames=False)
    size = _frame_size(session, scale)
    values = session.medium == "graphite"
    records = session.history.records
    passes = session.passes
    hold = max(1, int(round(float(hold_looks) * float(fps)))) if hold_looks > 0 else 0
    by_at: dict[int, list[dict]] = defaultdict(list)
    if hold:
        for cap in session.captures:
            by_at[int(cap.get("at", 0))].append(cap)

    def finish(img: Image.Image, text: str) -> Image.Image:
        return _caption(img, text) if captions else img

    def held(cap: dict, at: int) -> Iterator[Frame]:
        kind = str(cap.get("kind", "look"))
        args = cap.get("args", {}) or {}
        label = f"{kind} {cap.get('file', '')}".strip()
        if kind == "rehearse":
            path = Path(session.out_dir) / str(cap.get("file", ""))
            if not cap.get("file") or not path.exists():
                return
            with Image.open(path) as im:
                img = _letterbox(im, size)
            yield Frame(finish(img, label + " (not laid)"), at, kind, None, label, hold)
            return
        # The capture keeps the look's own arguments and drops the false ones, so a
        # grid that is not there was `grid=False`: the held frame is what the painter
        # saw, gridded only when they asked. It forced the grid on until the fork's
        # fifth step, which turned every plain look into a gridded frame.
        grid = args.get("grid", False)
        region = args.get("region")
        # A captured region is a cell's name or four bounds; either is a place.
        crop = None
        if region:
            crop = as_region(region if isinstance(region, str) else tuple(region))
        img = render_look(fresh.canvas, scale=max(size), grid=grid,
                          values=bool(args.get("values", values)),
                          region=crop,
                          sketch=bool(args.get("sketch", True)),
                          marks=fresh.marks if args.get("marks", True) else None,
                          guides=fresh.guides)
        img = _letterbox(img, size) if img.size != size else img
        yield Frame(finish(img, label), at, kind, None, label, hold)

    yield Frame(finish(_render(fresh.canvas, size, values), "the surface"), 0, "start",
                None, "the surface")
    n = len(records)
    for i, record in enumerate(records):
        for cap in by_at.get(i, []):
            yield from held(cap, i)
        framed = (i + 1) % every == 0 or i == n - 1
        label = _label(record, passes)
        if framed and stroke_motion and record.kind == "graphite" and record.dabs > 2:
            params = record.params or {}
            for share in MOTION_STEPS:
                copy = fresh.canvas.trial_copy()
                draw_graphite(copy, record.points,
                              grade=str(params.get("grade", record.brush or "HB")),
                              pressure=record.pressure,
                              tip=str(params.get("tip", "point")),
                              width=params.get("width"),
                              rng=fresh._stroke_rng(record.index),
                              smooth=bool(params.get("smooth", True)), upto=share)
                yield Frame(finish(_render(copy, size, values), label), i, "motion",
                            record.index, label)
        with fresh._one_call("replay"):
            fresh._replay_records([record])
        if framed:
            yield Frame(finish(_render(fresh.canvas, size, values), label), i + 1, "mark",
                        record.index, label)
    for cap in by_at.get(n, []):
        yield from held(cap, n)
    yield Frame(finish(_render(fresh.canvas, size, values), "finished"), n, "end", None,
                "finished", max(1, int(round(HOLD_LAST * float(fps)))))


def write_film(session, path, fps: float = 12.0, every: int = 1, scale: int | None = 720,
               hold_looks: float = 1.0, stroke_motion: bool = False,
               captions: bool = False) -> Path:
    """Write the film. The suffix picks the format: ``.mp4``, ``.gif``, or none for a
    directory of PNG frames with a ``frames.json`` beside them."""
    p = Path(path)
    suffix = p.suffix.lower()
    seq = frames(session, every=every, scale=scale, stroke_motion=stroke_motion,
                 hold_looks=hold_looks, fps=fps, captions=captions)
    if suffix == ".gif":
        return _write_gif(seq, p, fps)
    if suffix == ".mp4":
        return _write_mp4(seq, p, fps)
    if suffix == "":
        return _write_pngs(seq, p)
    raise ValueError(
        f"film() writes .mp4, .gif, or a directory of PNG frames (a path with no "
        f"suffix); {p.name!r} is none of those."
    )


def _write_gif(seq: Iterator[Frame], p: Path, fps: float) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    per = max(20, int(round(1000.0 / max(float(fps), 0.1))))
    images: list[Image.Image] = []
    durations: list[int] = []
    for frame in seq:
        images.append(frame.image.convert("P", palette=Image.ADAPTIVE))
        durations.append(per * max(1, frame.hold))
    if not images:  # pragma: no cover - the surface is always a frame
        raise ValueError("Nothing to film.")
    images[0].save(p, save_all=True, append_images=images[1:], duration=durations, loop=0,
                   optimize=True)
    return p


def _write_pngs(seq: Iterator[Frame], folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    listed = []
    for k, frame in enumerate(seq):
        name = f"frame_{k:05d}.png"
        frame.image.save(folder / name)
        listed.append({"file": name, **frame.to_json()})
    (folder / "frames.json").write_text(json.dumps(listed, indent=1), encoding="utf-8")
    return folder


def _write_mp4(seq: Iterator[Frame], p: Path, fps: float) -> Path:
    exe = ffmpeg_path()
    if exe is None:
        raise RuntimeError(
            "Writing an .mp4 needs ffmpeg, and none was found: `pip install "
            "easel-paint[film]` brings one (imageio-ffmpeg), or put ffmpeg on the path. "
            "A .gif or a directory of PNG frames needs nothing."
        )
    p.parent.mkdir(parents=True, exist_ok=True)
    proc = None
    size = None
    # ffmpeg's complaints go to a file rather than a pipe: a pipe nobody drains while
    # the frames are written is a deadlock the moment ffmpeg has much to say, and the
    # file is what names the fault when it stops early -- a build without libx264, a
    # path it cannot write -- where a broken pipe said only `[Errno 22]`.
    with tempfile.TemporaryFile() as log:
        stopped = False
        code = 0
        try:
            for frame in seq:
                img = frame.image
                if size is None:
                    # yuv420p wants even dimensions; pad by a pixel rather than resample.
                    w, h = img.size
                    size = (w + (w % 2), h + (h % 2))
                    proc = subprocess.Popen(
                        [exe, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt",
                         "rgb24", "-s", f"{size[0]}x{size[1]}", "-r", f"{float(fps):g}",
                         "-i", "-", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                         "-movflags", "+faststart", str(p)],
                        stdin=subprocess.PIPE, stderr=log,
                    )
                if img.size != size:
                    padded = Image.new("RGB", size, (18, 18, 20))
                    padded.paste(img, (0, 0))
                    img = padded
                data = np.asarray(img.convert("RGB"), dtype=np.uint8).tobytes()
                assert proc is not None and proc.stdin is not None
                try:
                    for _ in range(max(1, frame.hold)):
                        proc.stdin.write(data)
                except OSError:
                    # ffmpeg stopped reading: its own words, below, say why. Only
                    # the write is caught -- a frame that fails to build is the
                    # frame's own error, not a film cut short and called whole.
                    stopped = True
                    break
        finally:
            if proc is not None:
                if proc.stdin is not None:
                    try:
                        proc.stdin.close()
                    except OSError:
                        pass
                # Reaped whatever happened above: stdin is closed, so this ends.
                code = proc.wait()
        if proc is None:  # pragma: no cover - the surface is always a frame
            raise ValueError("Nothing to film.")
        log.seek(0)
        err = log.read().decode("utf-8", "replace").strip()
    if code != 0 or stopped:
        # No half-written film left behind to be mistaken for one that plays.
        try:
            p.unlink()
        except OSError:
            pass
        raise RuntimeError(f"ffmpeg failed writing {p} (exit {code}): {err or 'no message'}")
    return p


# --------------------------------------------------------------------------------------
# The viewer
# --------------------------------------------------------------------------------------
def write_viewer(session, out_dir, fps: float = 12.0, every: int = 1,
                 scale: int | None = 720, hold_looks: float = 1.0,
                 stroke_motion: bool = False, captions: bool = False) -> Path:
    """Write ``index.html``, ``film.json`` and ``frames/`` under ``out_dir``.

    The page carries the film's data inline, so it opens from a file as well as from
    a server; the frames are separate PNGs it loads as they are shown. Returns the
    page's path.
    """
    folder = Path(out_dir)
    frames_dir = folder / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    listed = []
    size = None
    for k, frame in enumerate(frames(session, every=every, scale=scale,
                                     stroke_motion=stroke_motion, hold_looks=hold_looks,
                                     fps=fps, captions=captions)):
        name = f"{k:05d}.png"
        frame.image.save(frames_dir / name)
        size = frame.image.size
        listed.append({"file": f"frames/{name}", **frame.to_json()})
    records = [{"index": r.index, "kind": r.kind, "brush": r.brush,
                "pressure": r.pressure if isinstance(r.pressure, (str, int, float))
                else [float(v) for v in np.atleast_1d(np.asarray(r.pressure, dtype=float))],
                "note": r.note, "dabs": int(r.dabs), "paint": float(r.paint),
                "grade": (r.params or {}).get("grade"), "tip": (r.params or {}).get("tip"),
                "via": (r.params or {}).get("via")}
               for r in session.history.records]
    data = {"fps": float(fps), "size": list(size or (0, 0)), "frames": listed,
            "records": records, "passes": session.passes, "captures": session.captures,
            "medium": session.medium, "budget": session.budget,
            "canvas": [session.canvas.width, session.canvas.height]}
    (folder / "film.json").write_text(json.dumps(data), encoding="utf-8")
    page = _PAGE.replace("/*FILM*/", json.dumps(data).replace("</", "<\\/"))
    page = page.replace("<!--TITLE-->", html.escape(f"{session.medium} film, "
                                                    f"{len(records)} marks"))
    (folder / "index.html").write_text(page, encoding="utf-8")
    return folder / "index.html"


_PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><!--TITLE--></title>
<style>
  :root { color-scheme: dark; --bg: #141416; --fg: #e6e6ea; --dim: #9a9aa2; --line: #2a2a2e;
          --hi: #3b5bdb; --panel: #1c1c20; }
  body { margin: 0; background: var(--bg); color: var(--fg); font: 14px/1.45 system-ui, sans-serif; }
  main { display: grid; grid-template-columns: minmax(0, 2fr) minmax(280px, 1fr); gap: 16px;
         padding: 16px; max-width: 1600px; margin: 0 auto; }
  @media (max-width: 900px) { main { grid-template-columns: 1fr; } }
  #stage img { width: 100%; height: auto; display: block; background: #000; border: 1px solid var(--line); }
  .bar { display: flex; gap: 10px; align-items: center; margin: 10px 0; flex-wrap: wrap; }
  input[type=range] { flex: 1 1 200px; }
  button, input[type=number] { background: var(--panel); color: var(--fg); border: 1px solid var(--line);
          border-radius: 6px; padding: 6px 10px; font: inherit; }
  button:hover { border-color: var(--hi); }
  #label { color: var(--dim); font-variant-numeric: tabular-nums; }
  aside { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 12px 14px;
          min-width: 0; }
  aside h2 { font-size: 13px; text-transform: uppercase; letter-spacing: .06em; color: var(--dim);
             margin: 14px 0 6px; }
  aside h2:first-child { margin-top: 0; }
  pre { margin: 0; max-height: 46vh; overflow: auto; font: 12px/1.5 ui-monospace, Consolas, monospace;
        background: #111114; border: 1px solid var(--line); border-radius: 6px; padding: 8px 0; }
  pre .l { display: block; padding: 0 10px; white-space: pre; }
  pre .l.on { background: var(--hi); color: #fff; }
  pre .n { display: inline-block; width: 3ch; color: var(--dim); text-align: right; margin-right: 10px; }
  #look img { width: 100%; height: auto; border: 1px solid var(--line); display: block; }
  dl { display: grid; grid-template-columns: auto 1fr; gap: 2px 10px; margin: 0; }
  dt { color: var(--dim); } dd { margin: 0; overflow-wrap: anywhere; }
</style>
</head>
<body>
<main>
  <section id="stage">
    <img id="frame" alt="the painting at this mark">
    <div class="bar">
      <button id="play" type="button" aria-label="play or pause">Play</button>
      <input id="scrub" type="range" min="0" value="0" step="1" aria-label="frame">
      <label>fps <input id="fps" type="number" min="1" max="60" step="1" style="width:5em"></label>
      <span id="label"></span>
    </div>
  </section>
  <aside>
    <h2>Mark</h2>
    <dl id="mark"></dl>
    <h2>Pass</h2>
    <div id="passname" style="color:var(--dim);margin-bottom:6px"></div>
    <pre id="source"></pre>
    <h2>Last look</h2>
    <div id="look"><span style="color:var(--dim)">none yet</span></div>
  </aside>
</main>
<script>
const FILM = /*FILM*/;
const frames = FILM.frames, records = FILM.records, passes = FILM.passes || [];
const byIndex = new Map(records.map(r => [r.index, r]));
const img = document.getElementById('frame'), scrub = document.getElementById('scrub');
const play = document.getElementById('play'), fpsIn = document.getElementById('fps');
const label = document.getElementById('label'), mark = document.getElementById('mark');
const passName = document.getElementById('passname'), source = document.getElementById('source');
const look = document.getElementById('look');
scrub.max = String(frames.length - 1); fpsIn.value = String(FILM.fps || 12);
let k = 0, timer = null, shownPass = null;

function esc(s) { return String(s).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }
function passOf(index) { return passes.find(p => p.at <= index && index < p.until) || null; }
function lastLook(upto) {
  for (let i = upto; i >= 0; i--) if (frames[i].kind === 'look' || frames[i].kind === 'rehearse') return frames[i];
  return null;
}
function showSource(p, index) {
  if (p !== shownPass) {
    shownPass = p;
    source.innerHTML = '';
    if (!p) { passName.textContent = 'no pass captured for this mark'; return; }
    passName.textContent = p.mode + ' ' + p.scripts + ' (records ' + p.at + '–' + (p.until - 1) + ')';
    for (const [name, text] of p.sources) {
      const head = document.createElement('span'); head.className = 'l'; head.style.color = 'var(--dim)';
      head.textContent = '# ' + name; source.appendChild(head);
      text.split('\n').forEach((line, i) => {
        const el = document.createElement('span'); el.className = 'l'; el.dataset.file = name; el.dataset.line = String(i + 1);
        el.innerHTML = '<span class="n">' + (i + 1) + '</span>' + esc(line); source.appendChild(el);
      });
    }
  }
  source.querySelectorAll('.l.on').forEach(el => el.classList.remove('on'));
  if (!p) return;
  const where = p.lines && p.lines[String(index)];
  if (!where) return;
  const [file, line] = where;
  const el = Array.from(source.querySelectorAll('.l')).find(e =>
    e.dataset.line === String(line) && (e.dataset.file === file || (e.dataset.file || '').endsWith(file)));
  if (el) { el.classList.add('on'); el.scrollIntoView({block: 'center'}); }
  else passName.textContent += ' · laid from ' + file + ':' + line;
}
function show(i) {
  k = Math.max(0, Math.min(frames.length - 1, i));
  const f = frames[k];
  img.src = f.file; scrub.value = String(k);
  if (frames[k + 1]) { const pre = new Image(); pre.src = frames[k + 1].file; }
  label.textContent = (k + 1) + ' / ' + frames.length + '  ·  ' + f.label;
  const r = f.index != null ? byIndex.get(f.index) : null;
  mark.innerHTML = '';
  const rows = r ? [['record', '#' + r.index], ['kind', r.kind], ['tool', r.brush || '-'],
      ['grade', r.grade || '-'], ['tip', r.tip || '-'], ['pressure', JSON.stringify(r.pressure)],
      ['dabs', r.dabs], ['landed', Math.round(r.paint)], ['via', r.via || 'by hand'], ['note', r.note || '-']]
    : [['frame', f.kind], ['records laid', f.at]];
  for (const [a, b] of rows) { const dt = document.createElement('dt'); dt.textContent = a;
    const dd = document.createElement('dd'); dd.textContent = String(b); mark.append(dt, dd); }
  showSource(r ? passOf(r.index) : null, r ? r.index : -1);
  const l = lastLook(k);
  look.innerHTML = l ? '<img src="' + l.file + '" alt="the painter\'s last look"><div style="color:var(--dim)">'
      + esc(l.label) + ' · after ' + l.at + ' records</div>' : '<span style="color:var(--dim)">none yet</span>';
}
function stop() { if (timer) { clearTimeout(timer); timer = null; } play.textContent = 'Play'; }
function step() {
  if (k >= frames.length - 1) { stop(); return; }
  show(k + 1);
  const hold = Math.max(1, frames[k].hold || 1);
  timer = setTimeout(step, 1000 / Math.max(1, Number(fpsIn.value) || 12) * hold);
}
play.addEventListener('click', () => { if (timer) stop(); else { if (k >= frames.length - 1) show(0); play.textContent = 'Pause'; step(); } });
scrub.addEventListener('input', () => { stop(); show(Number(scrub.value)); });
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight') { stop(); show(k + 1); } else if (e.key === 'ArrowLeft') { stop(); show(k - 1); }
  else if (e.key === ' ') { e.preventDefault(); play.click(); }
});
show(0);
</script>
</body>
</html>
"""
