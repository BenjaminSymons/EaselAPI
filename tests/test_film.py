"""Capture and the film: what a capturing session keeps beside the log, and the film
and the viewer built from it.

Nothing here is a record. The tests hold that line as much as they hold the frames:
a look, a rehearsal and a pass are kept keyed by the log's length, the log itself is
what it was, and a file written before any of this existed opens with none.
"""

from __future__ import annotations

import json
import shutil

import numpy as np
import pytest
from PIL import Image

from easel import Session
from easel.film import ffmpeg_path, frames, write_film, write_viewer
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
    assert kinds.count("look") == 2 and kinds.count("rehearse") == 1
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
    assert len(data["captures"]) == 3
    for entry in data["frames"]:
        assert (page.parent / entry["file"]).exists()
    assert len(data["frames"]) == len(list(frames(s, scale=120, hold_looks=0.5,
                                                 stroke_motion=True)))
    text = page.read_text(encoding="utf-8")
    assert "<!doctype html>" in text and '"frames":' in text and "p03.py" in text
    assert "fetch(" not in text, "the page must open from a file: its data is inline"
    assert s.viewer(tmp_path / "view2", scale=80).exists()
    shutil.rmtree(tmp_path / "view2")
