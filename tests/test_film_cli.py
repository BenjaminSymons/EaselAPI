"""The shell, end to end, for a drawing that captures: `easel new --medium graphite
--capture`, a pass through `easel run` that is kept with its lines, and `easel film`
writing the GIF and the viewer from what was kept.

Each verb is held elsewhere on its own; this is the road a draftsman takes through
all three, since the second test drawing's film fell over between them.
"""

from __future__ import annotations

import json

from easel import Session
from easel.cli import main


def test_a_drawing_made_run_and_filmed_through_the_shell(tmp_path, capsys):
    session = str(tmp_path / "d.easel")
    out = str(tmp_path / "out")
    assert main(["new", session, "--size", "160x120", "--medium", "graphite", "--capture",
                 "--out-dir", out]) == 0
    made = Session.load(session)
    assert made.medium == "graphite" and made.capture
    assert made.canvas.texture_name == "cartridge"
    assert made.passes == [] and made.captures == []

    script = tmp_path / "p01.py"
    script.write_text("s.hatch(cell('C3'), angle=30, grade='HB', spacing=0.04)\n",
                      encoding="utf-8")
    assert main(["run", session, str(script)]) == 0
    ran = Session.load(session)
    laid = len(ran.history.records)
    assert laid >= 2 and {r.kind for r in ran.history.records} == {"graphite"}
    (entry,) = ran.passes
    assert entry["mode"] == "painted" and entry["scripts"] == "p01.py"
    assert (entry["at"], entry["until"]) == (0, laid)
    assert entry["lines"]["0"] == ["p01.py", 1], "the first record is not mapped to its line"
    assert set(entry["lines"]) == {str(i) for i in range(laid)}

    gif = tmp_path / "d.gif"
    view = tmp_path / "view"
    assert main(["film", session, str(gif), "--html", str(view), "--every", "2"]) == 0
    assert gif.exists() and gif.stat().st_size > 0
    data = json.loads((view / "film.json").read_text(encoding="utf-8"))
    assert data["passes"] and data["passes"][0]["lines"]["0"] == ["p01.py", 1]
    assert (view / "index.html").exists()
    marks = [f for f in data["frames"] if f["kind"] == "mark"]
    assert len(marks) == laid // 2 + (1 if laid % 2 else 0)
    printed = capsys.readouterr().out
    assert str(gif) in printed and str(view / "index.html") in printed


def test_a_film_asked_for_with_nowhere_to_write_fails_with_a_message(tmp_path, capsys):
    session = str(tmp_path / "d.easel")
    assert main(["new", session, "--size", "32x32", "--medium", "graphite",
                 "--out-dir", str(tmp_path / "out")]) == 0
    assert main(["film", session]) == 1
    err = capsys.readouterr().err
    assert "easel:" in err and "--html" in err and "output" in err


def test_the_shells_look_at_a_drawing_is_its_values_view(tmp_path, capsys):
    """`easel look d.easel` captured `{"sketch": true, "marks": true}` and wrote the
    rendered picture, where `look()` on a drawing is a values view: the flag left off
    now follows the medium, as the Python default does."""
    session = str(tmp_path / "d.easel")
    out = str(tmp_path / "out")
    assert main(["new", session, "--size", "160x120", "--medium", "graphite", "--capture",
                 "--out-dir", out]) == 0
    script = tmp_path / "p01.py"
    script.write_text("s.line([(0.1, 0.1), (0.9, 0.9)], '2B', tip='side')\n", encoding="utf-8")
    assert main(["run", session, str(script)]) == 0
    assert main(["look", session]) == 0
    assert main(["look", session, "--values"]) == 0
    looks = [c for c in Session.load(session).captures if c["kind"] == "look"]
    assert [c["args"].get("values") for c in looks] == [True, True]
