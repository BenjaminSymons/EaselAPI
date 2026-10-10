"""Capture and the film: what a capturing session keeps beside the log, and the film
and the viewer built from it.

Nothing here is a record. The tests hold that line as much as they hold the frames:
a look, a rehearsal and a pass are kept keyed by the log's length, the log itself is
what it was, and a file written before any of this existed opens with none.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from easel import Session
from easel.film import CAPTION_H, ffmpeg_path, frames, write_film, write_viewer
from easel.regions import cell


def make(tmp_path, **kw):
    kw.setdefault("timelapse", False)
    kw.setdefault("medium", "graphite")
    kw.setdefault("capture", True)
    return Session(320, 240, seed=4, out_dir=tmp_path / "out", **kw)


def drawn(tmp_path, **kw) -> Session:
    s = make(tmp_path, **kw)
    s.pencil([(0.1, 0.9), (0.9, 0.85)])
    s.hatch(cell("C3"), angle=35, grade="HB", spacing=0.03)
    s.look(grid=True)
    s.line([(0.1, 0.2), (0.5, 0.15), (0.9, 0.3)], "6B", pressure=0.9)
    s.rehearse({"hatch": cell("E5"), "grade": "2B"}, region=cell("E5"))
    s.tone(cell("E5"), 0.5)
    s.look(values=True, region=cell("E5"))
    # A region by its name, as `easel look --region D4` hands one over: the first
    # drawing's film fell over on exactly this capture.
    s.look(region="D4", grid="fine")
    return s


# --------------------------------------------------------------------------------------
# Capture
# --------------------------------------------------------------------------------------
def test_a_capturing_session_keeps_its_looks_and_rehearsals_beside_the_log(tmp_path):
    s = drawn(tmp_path)
    kinds = [(c["kind"], c["at"]) for c in s.captures]
    n_hatch = sum(1 for r in s.history.records if r.params.get("via") == "hatch")
    assert kinds[0] == ("look", 1 + n_hatch)
    assert kinds[1][0] == "rehearse" and kinds[1][1] == kinds[0][1] + 1
    assert kinds[2][0] == "look" and kinds[2][1] == len(s.history.records)
    assert kinds[3] == ("look", len(s.history.records)) and s.captures[3]["args"]["region"] == "D4"
    assert s.captures[0]["file"].startswith("look_") and s.captures[0]["args"]["grid"] is True
    assert s.captures[2]["args"]["values"] is True and len(s.captures[2]["args"]["region"]) == 4
    # And the log is what it was: no record of any kind for a look.
    assert {r.kind for r in s.history.records} <= {"pencil", "graphite"}


def test_a_session_that_does_not_capture_keeps_nothing(tmp_path):
    s = drawn(tmp_path, capture=False)
    assert s.captures == [] and s.passes == []


def test_captures_survive_the_file_and_the_replay_and_an_old_file_has_none(tmp_path):
    s = drawn(tmp_path)
    path = s.save(tmp_path / "d.easel")
    back = Session.load(path)
    assert back.capture and back.captures == s.captures
    assert back.replay().captures == s.captures
    with np.load(path, allow_pickle=False) as data:
        fields = {k: data[k] for k in data.files}
    meta = json.loads(str(fields.pop("meta")))
    for key in ("capture", "captures", "passes"):
        meta.pop(key)
    with open(path, "wb") as fh:
        np.savez_compressed(fh, meta=np.array(json.dumps(meta)), **fields)
    old = Session.load(path)
    assert not old.capture and old.captures == [] and old.passes == []


def test_a_pass_is_kept_with_its_scripts_and_its_lines(tmp_path):
    s = make(tmp_path)
    source = ("s.hatch(cell('B2'), angle=20, grade='HB', spacing=0.04)\n"
              "s.line([(0.2, 0.8), (0.8, 0.7)], '2B')\n")
    before = len(s.history.records)
    exec(compile(source, "p01_test.py", "exec"), {"s": s, "cell": cell})  # noqa: S102
    s.keep_pass(s, "p01_test.py", [("p01_test.py", source)], before)
    (entry,) = s.passes
    assert entry["mode"] == "painted" and entry["at"] == before
    assert entry["until"] == len(s.history.records)
    assert entry["sources"] == [["p01_test.py", source]]
    last = str(len(s.history.records) - 1)
    assert entry["lines"][last] == ["p01_test.py", 2]
    assert entry["lines"][str(before)] == ["p01_test.py", 1]
    # A rehearsed pass is kept as one, and its copy's looks come with it.
    trial = s.scratch()
    exec(compile(source, "p02_test.py", "exec"), {"s": trial, "cell": cell})  # noqa: S102
    trial.look()
    s._keep_report(trial, "p02_test.py", 0, "nothing")
    s.keep_pass(trial, "p02_test.py", [("p02_test.py", source)], 0)
    assert s.passes[-1]["mode"] == "rehearsed" and s.passes[-1]["at"] == len(s.history.records)
    assert s.captures[-1]["kind"] == "rehearse"
    assert s.captures[-1]["at"] == len(s.history.records) + len(trial.history.records)


# --------------------------------------------------------------------------------------
# The film
# --------------------------------------------------------------------------------------
def test_the_film_is_a_frame_per_mark_with_the_looks_held(tmp_path):
    s = drawn(tmp_path)
    seq = list(frames(s, every=1, scale=160, hold_looks=0.5, fps=12))
    kinds = [f.kind for f in seq]
    n = len(s.history.records)
    assert kinds[0] == "start" and kinds[-1] == "end"
    assert kinds.count("mark") == n
    assert kinds.count("look") == 3 and kinds.count("rehearse") == 1
    looks = [f for f in seq if f.kind == "look"]
    assert all(f.hold == 6 for f in looks)
    # Held where it was taken: the look comes after the records it saw, before the next.
    first = seq.index(looks[0])
    assert seq[first - 1].kind == "mark" and seq[first - 1].at == looks[0].at
    assert seq[first + 1].kind == "mark" and seq[first + 1].at == looks[0].at + 1
    (rehearsal,) = [f for f in seq if f.kind == "rehearse"]
    where = seq.index(rehearsal)
    assert seq[where - 1].kind == "mark" and seq[where - 1].at == rehearsal.at
    assert all(f.image.size == seq[0].image.size for f in seq)
    assert seq[0].image.size == (160, 120)
    # The last mark's frame is the painting.
    final = np.asarray(seq[-1].image)
    rebuilt = np.asarray(Image.fromarray(np.repeat(s.canvas.values()[:, :, None], 3, axis=2))
                         .resize((160, 120), Image.LANCZOS))
    assert np.abs(final.astype(int) - rebuilt.astype(int)).max() <= 2


def test_a_look_taken_without_the_grid_is_held_without_it(tmp_path):
    """The film held every look gridded: the capture drops a false argument, and the
    film read a missing grid as `True`. A look the painter took plain is held plain,
    and one taken with the grid, or the fine grid, is held as taken."""
    from easel.look import render_look

    s = make(tmp_path)
    s.line([(0.1, 0.2), (0.5, 0.15), (0.9, 0.3)], "6B", pressure=0.9)
    s.look(grid=False)
    s.look(grid=True)
    s.look(grid="fine")
    assert "grid" not in s.captures[0]["args"]
    looks = [f for f in frames(s, every=1, scale=320, hold_looks=0.5, fps=12)
             if f.kind == "look"]
    assert len(looks) == 3
    plain = np.asarray(render_look(s.canvas, scale=320, values=True, marks=None,
                                   guides=s.guides))
    gridded = np.asarray(render_look(s.canvas, scale=320, grid=True, values=True,
                                     marks=None, guides=s.guides))
    assert np.array_equal(np.asarray(looks[0].image), plain)
    assert np.array_equal(np.asarray(looks[1].image), gridded)
    assert not np.array_equal(np.asarray(looks[2].image), plain)
    assert not np.array_equal(np.asarray(looks[2].image), gridded)


def test_every_thins_the_marks_and_keeps_the_last(tmp_path):
    s = drawn(tmp_path, capture=False)
    seq = [f for f in frames(s, every=4, scale=120, hold_looks=0) if f.kind == "mark"]
    n = len(s.history.records)
    assert len(seq) == n // 4 + (1 if n % 4 else 0)
    assert seq[-1].at == n


def test_stroke_motion_lays_a_graphite_stroke_over_three_frames(tmp_path):
    s = make(tmp_path, capture=False)
    s.line([(0.1, 0.5), (0.9, 0.5)], "6B", pressure=1.0, smooth=False)
    seq = list(frames(s, scale=0, stroke_motion=True, hold_looks=0))
    kinds = [f.kind for f in seq]
    assert kinds == ["start", "motion", "motion", "mark", "end"]
    dark = [int((np.asarray(f.image)[..., 0] < 128).sum()) for f in seq[1:4]]
    assert dark[0] < dark[1] < dark[2], f"the stroke did not travel: {dark}"
    # Each partial stroke lies inside the whole one, and the mark frame is the painting.
    whole = np.asarray(seq[3].image)[..., 0] < 200
    for f in seq[1:3]:
        part = np.asarray(f.image)[..., 0] < 200
        assert (part & ~whole).sum() < 0.02 * part.sum() + 5
    assert np.array_equal(np.asarray(seq[3].image)[..., 0], s.canvas.values())


def test_a_painting_films_too_and_its_strokes_arrive_whole(tmp_path):
    s = Session(240, 180, seed=3, timelapse=False, out_dir=tmp_path / "out", capture=True)
    s.block_in("upper-band", "bristle", "burnt_umber", size=0.12, density=0.8)
    s.look()
    s.stroke([(0.1, 0.7), (0.9, 0.75)], "flat", "cadmium_red")
    seq = list(frames(s, scale=120, stroke_motion=True, hold_looks=0.25, fps=8))
    kinds = [f.kind for f in seq]
    assert "motion" not in kinds and kinds.count("look") == 1
    assert kinds.count("mark") == len(s.history.records)
    colour = np.asarray(seq[-1].image)
    assert (colour[..., 0] != colour[..., 1]).any(), "a painting's film lost its colour"


def test_the_writers_write_a_gif_a_directory_and_captions(tmp_path):
    s = drawn(tmp_path)
    gif = write_film(s, tmp_path / "d.gif", fps=12, scale=120, hold_looks=0.5, captions=True)
    with Image.open(gif) as im:
        assert im.n_frames == len(list(frames(s, scale=120, hold_looks=0.5)))
        assert im.size == (120, 90 + 22)
    folder = write_film(s, tmp_path / "frames", every=2, scale=120, hold_looks=0)
    listed = json.loads((folder / "frames.json").read_text(encoding="utf-8"))
    assert len(list(folder.glob("frame_*.png"))) == len(listed) >= 3
    assert listed[0]["kind"] == "start" and listed[-1]["kind"] == "end"
    with pytest.raises(ValueError, match="mp4"):
        write_film(s, tmp_path / "d.webm")
    assert s.film(tmp_path / "e.gif", scale=80).exists()


@pytest.mark.skipif(ffmpeg_path() is None, reason="no ffmpeg on this machine")
def test_an_mp4_is_written_when_ffmpeg_is_there(tmp_path):
    s = drawn(tmp_path)
    mp4 = write_film(s, tmp_path / "d.mp4", fps=12, scale=121, stroke_motion=True)
    assert mp4.exists() and mp4.stat().st_size > 1000
    with open(mp4, "rb") as fh:
        assert b"ftyp" in fh.read(64)


def test_an_mp4_without_ffmpeg_says_how_to_get_one(tmp_path, monkeypatch):
    import easel.film as film
    monkeypatch.setattr(film, "ffmpeg_path", lambda: None)
    s = make(tmp_path)
    s.line([(0.1, 0.5), (0.9, 0.5)])
    with pytest.raises(RuntimeError, match=r"easel-paint\[film\]"):
        film.write_film(s, tmp_path / "d.mp4")


# --------------------------------------------------------------------------------------
# The viewer
# --------------------------------------------------------------------------------------
def test_the_viewer_is_a_page_a_json_and_the_frames(tmp_path):
    s = drawn(tmp_path)
    source = "s.line([(0.2, 0.6), (0.8, 0.65)], '4B')\n"
    before = len(s.history.records)
    exec(compile(source, "p03.py", "exec"), {"s": s})  # noqa: S102
    s.keep_pass(s, "p03.py", [("p03.py", source)], before)
    page = write_viewer(s, tmp_path / "view", scale=120, hold_looks=0.5, stroke_motion=True)
    assert page.name == "index.html" and page.exists()
    data = json.loads((page.parent / "film.json").read_text(encoding="utf-8"))
    assert data["fps"] == 12.0 and data["medium"] == "graphite"
    assert len(data["records"]) == len(s.history.records)
    assert len(data["passes"]) == 1 and data["passes"][0]["lines"][str(before)] == ["p03.py", 1]
    assert len(data["captures"]) == 4
    for entry in data["frames"]:
        assert (page.parent / entry["file"]).exists()
    assert len(data["frames"]) == len(list(frames(s, scale=120, hold_looks=0.5,
                                                 stroke_motion=True)))
    text = page.read_text(encoding="utf-8")
    assert "<!doctype html>" in text and '"frames":' in text and "p03.py" in text
    assert "fetch(" not in text, "the page must open from a file: its data is inline"
    assert s.viewer(tmp_path / "view2", scale=80).exists()
    shutil.rmtree(tmp_path / "view2")


def test_an_undo_forgets_the_looks_captures_and_passes_past_the_log(tmp_path):
    """The sidecars are keyed by the log's length, and an undo that cut the log and
    left them was a film holding a look at a mark the painter never saw, the check
    crediting a mark laid after the undo with a look taken before it, and the viewer
    naming a script line for a record no longer there. Both undo paths forget them;
    a look taken at exactly the new length is a look at what is still there."""
    s = make(tmp_path)
    s.line([(0.1, 0.1), (0.9, 0.9)], "HB")
    s.look()
    s.line([(0.1, 0.9), (0.9, 0.1)], "HB")
    s.look()
    s.keep_pass(s, "p1.py", [("p1.py", "s.line(...)")], 0)
    s.rehearse({"hatch": cell("E5"), "grade": "2B"}, region=cell("E5"))
    assert [c["at"] for c in s.captures] == [1, 2, 2]
    s.undo(1)
    assert [c["at"] for c in s.captures] == [1] and s._looked == [1]
    assert [(p["at"], p["until"]) for p in s.passes] == [(0, 1)]
    assert list(s.passes[0]["lines"]) <= ["0"]
    s.line([(0.1, 0.9), (0.9, 0.1)], "HB")
    assert [f.kind for f in frames(s, hold_looks=1.0)].count("look") == 1
    # The rebuild path, when the snapshots are gone.
    s.look()
    s.history.invalidate_snapshots()
    s.undo(2)
    assert len(s.history.records) == 0
    assert s.captures == [] and s._looked == [] and s.passes == []
    # A pass that only rehearsed is kept while the log reaches where it began.
    t = make(tmp_path)
    t.line([(0.1, 0.1), (0.9, 0.9)], "HB")
    trial = t.scratch()
    trial.line([(0.1, 0.9), (0.9, 0.1)], "HB")
    t.keep_pass(trial, "p2.py", [("p2.py", "s.line(...)")], 1)
    assert [p["mode"] for p in t.passes] == ["rehearsed"]
    t.undo(1)
    assert t.passes == []


# --------------------------------------------------------------------------------------
# The film's edges: what it refuses, leaves out, skips, and writes under a frame
# --------------------------------------------------------------------------------------
def test_a_film_is_a_frame_per_at_least_one_mark(tmp_path):
    """`every=0` is a modulo by nought under the loop; the film says what `every` is."""
    s = make(tmp_path)
    s.line([(0.1, 0.5), (0.9, 0.5)], "HB")
    with pytest.raises(ValueError, match="every"):
        list(frames(s, every=0))
    with pytest.raises(ValueError, match="every"):
        list(frames(s, every=-3))


def test_holding_the_looks_for_no_time_leaves_them_out(tmp_path):
    """`hold_looks=0` is the switch the shell's `--hold-looks 0` turns: no look and no
    rehearsal frame, and every mark still filmed."""
    s = make(tmp_path)
    s.line([(0.1, 0.5), (0.9, 0.5)], "HB")
    s.look()
    s.rehearse({"hatch": cell("E5"), "grade": "2B"}, region=cell("E5"))
    s.line([(0.1, 0.2), (0.9, 0.3)], "2B")
    assert [c["kind"] for c in s.captures] == ["look", "rehearse"]
    kinds = [f.kind for f in frames(s, every=1, scale=80, hold_looks=0)]
    assert "look" not in kinds and "rehearse" not in kinds
    assert kinds == ["start", "mark", "mark", "end"]


def test_a_rehearsal_whose_picture_is_gone_is_skipped_while_the_looks_still_play(tmp_path):
    """A look is re-rendered on the rebuilt canvas; a rehearsal's picture is the path
    not taken, and only its PNG holds it. One deleted from `out_dir` is a frame the
    film cannot make, and it is left out rather than failing the whole film."""
    s = make(tmp_path)
    s.line([(0.1, 0.5), (0.9, 0.5)], "HB")
    s.look()
    s.rehearse({"hatch": cell("E5"), "grade": "2B"}, region=cell("E5"))
    s.line([(0.1, 0.2), (0.9, 0.3)], "2B")
    s.look(values=True)
    kinds = [f.kind for f in frames(s, every=1, scale=80, hold_looks=0.5, fps=12)]
    assert kinds.count("look") == 2 and kinds.count("rehearse") == 1
    (rehearsal,) = [c for c in s.captures if c["kind"] == "rehearse"]
    png = Path(s.out_dir) / rehearsal["file"]
    assert png.exists()
    png.unlink()
    kinds = [f.kind for f in frames(s, every=1, scale=80, hold_looks=0.5, fps=12)]
    assert kinds.count("look") == 2 and kinds.count("rehearse") == 0
    assert kinds.count("mark") == len(s.history.records)


def test_captions_name_the_grade_under_each_mark_in_the_frames_listing(tmp_path):
    """Through the PNG-directory writer, where the listing keeps each frame's label
    beside its file: a mark's caption carries its index and its pencil."""
    s = make(tmp_path)
    s.line([(0.1, 0.5), (0.9, 0.5)], "HB")
    s.line([(0.1, 0.2), (0.9, 0.3)], "6B", pressure=0.9)
    folder = write_film(s, tmp_path / "captioned", every=1, scale=80, hold_looks=0,
                        captions=True)
    listed = json.loads((folder / "frames.json").read_text(encoding="utf-8"))
    marks = [entry for entry in listed if entry["kind"] == "mark"]
    assert len(marks) == 2
    for entry, record in zip(marks, s.history.records, strict=True):
        assert f"#{record.index:03d}" in entry["label"]
        assert record.params["grade"] in entry["label"], entry["label"]
    assert "HB" in marks[0]["label"] and "6B" in marks[1]["label"]
    with Image.open(folder / marks[0]["file"]) as im:
        assert im.size[1] == 60 + CAPTION_H, "the caption strip is not under the frame"


def test_the_viewers_scrub_data_lines_up_with_the_log(tmp_path):
    """What the page's side panel reads: a mark frame's `index` is the record laid at
    its `at`, a held look's `hold` is the seconds asked for at the film's rate, and
    the last frame is the whole log."""
    s = make(tmp_path)
    s.line([(0.1, 0.5), (0.9, 0.5)], "HB")
    s.look()
    s.hatch(cell("E5"), angle=30, grade="2B", spacing=0.05)
    s.look(grid=True)
    hold_looks, fps = 0.75, 8.0
    page = write_viewer(s, tmp_path / "scrub", scale=80, hold_looks=hold_looks, fps=fps)
    data = json.loads((page.parent / "film.json").read_text(encoding="utf-8"))
    records = data["records"]
    marks = [f for f in data["frames"] if f["kind"] == "mark"]
    assert len(marks) == len(records) == len(s.history.records)
    for f in marks:
        assert f["index"] == records[f["at"] - 1]["index"], f
    looks = [f for f in data["frames"] if f["kind"] == "look"]
    assert len(looks) == 2 and all(f["hold"] == round(hold_looks * fps) for f in looks)
    assert all(f["index"] is None for f in looks)
    assert data["frames"][-1]["kind"] == "end" and data["frames"][-1]["at"] == len(records)
    assert data["frames"][0]["at"] == 0


def test_an_mp4_that_ffmpeg_cannot_write_is_named_and_not_left_behind(tmp_path, monkeypatch):
    """An ffmpeg that stops early -- a build without libx264, a path it cannot
    write -- used to surface as a broken pipe's `[Errno 22]` and leave a partial
    file that looked like a film. The error carries ffmpeg's exit code and its own
    words, and the file is gone. The stand-in is a script that complains and exits 3."""
    import os
    import stat

    import easel.film as film

    if os.name == "nt":
        stand_in = tmp_path / "ffmpeg.cmd"
        stand_in.write_text("@echo libx264 missing 1>&2 & exit /b 3\r\n", encoding="ascii")
    else:
        stand_in = tmp_path / "ffmpeg"
        stand_in.write_text("#!/bin/sh\necho libx264 missing >&2\nexit 3\n", encoding="ascii")
        try:
            stand_in.chmod(stand_in.stat().st_mode | stat.S_IXUSR)
        except OSError:
            pytest.skip("the stand-in ffmpeg cannot be made executable here")
        if not os.access(stand_in, os.X_OK):
            pytest.skip("the stand-in ffmpeg cannot be made executable here")
    monkeypatch.setattr("easel.film.ffmpeg_path", lambda: str(stand_in))
    s = make(tmp_path)
    s.line([(0.1, 0.5), (0.9, 0.5)], "HB")
    out = tmp_path / "broken.mp4"
    with pytest.raises(RuntimeError, match=r"\(exit 3\): libx264 missing") as caught:
        film.write_film(s, out, scale=0)
    assert str(out) in str(caught.value)
    assert not out.exists(), "a partial film was left behind"
