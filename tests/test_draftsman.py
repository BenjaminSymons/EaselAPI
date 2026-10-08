"""The drawing's own check, and the guide written for it.

`SPEC.md` proposed seven standing warnings for the graphite medium before any drawing
existed, and `LESSONS.md` says a check earns its line by firing on a real pass. So each
was measured on the first test drawing's log before anything was built
(`CALIBRATION.md`, *The check, measured on the first drawing*), and what survived is
what is held here: one finding of the drawing's own -- a run of marks with no look
between them -- and four standing lines that read differently in a drawing: `values:`
against the box of pencils, `paper:` in place of `ground:`, `lightest:` carrying the
share of the named light that is paper never touched, and `darks:` in the closing
checklist. The three that could not fire on that log are not built, and this file says
so rather than testing their absence.

The second half holds `DRAFTSMAN.md` the way `tests/test_guide.py` holds `PAINTER.md`:
a budget, a card, the one habit, and no subject noun from the drawings it was written
from -- `LESSONS.md`, *a worked example is an instruction*.
"""

from __future__ import annotations

import re
import warnings
from pathlib import Path

import pytest

from easel import GRADES, Session, cell, docs, span
from easel.checklist import DARKS_REACH
from easel.cli import main
from easel.session import _REPORT_LOOK_GAP

ROOT = Path(__file__).resolve().parents[1]


def make(tmp_path, **kw):
    kw.setdefault("timelapse", False)
    kw.setdefault("medium", "graphite")
    return Session(480, 360, seed=4, out_dir=tmp_path, **kw)


def lay(s: Session, n: int, y: float = 0.5) -> None:
    """``n`` side strokes in rows across the middle, the way a plane is laid."""
    for i in range(n):
        yy = 0.2 + 0.6 * (i % 12) / 12
        s.line([(0.1, yy), (0.9, yy)], "2H", pressure=0.8, tip="side", width=0.05)


# --------------------------------------------------------------------------------------
# A run of marks with no look between them
# --------------------------------------------------------------------------------------
def test_a_run_of_marks_with_no_look_between_them_is_a_finding_at_the_line(tmp_path):
    s = make(tmp_path)
    before = len(s.history.records)
    lay(s, _REPORT_LOOK_GAP - 1)
    assert "no look between them" not in s.report(since=before)
    lay(s, 1)
    said = s.report(since=before)
    assert f"{_REPORT_LOOK_GAP} marks laid with no look between them" in said
    # The marks are named, as every finding that counts marks names them.
    assert f"records {before}-{before + _REPORT_LOOK_GAP - 1}" in said


def test_a_look_or_a_rehearsal_breaks_the_run(tmp_path):
    s = make(tmp_path)
    before = len(s.history.records)
    lay(s, _REPORT_LOOK_GAP - 1)
    s.look()
    lay(s, _REPORT_LOOK_GAP - 1)
    assert "no look between them" not in s.report(since=before)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.rehearse([{"points": [(0.1, 0.1), (0.3, 0.12)], "grade": "HB"}])
    lay(s, _REPORT_LOOK_GAP - 1)
    assert "no look between them" not in s.report(since=before)
    # The looks are kept apart from the captures, so a session that keeps no film
    # still looked.
    assert not s.capture and len(s._looked) == 2


def test_the_looks_survive_the_file_and_the_closing_check_reads_the_longest_run(tmp_path):
    s = make(tmp_path)
    lay(s, _REPORT_LOOK_GAP)
    s.look()
    lay(s, 3)
    path = tmp_path / "d.easel"
    s.save(path)
    again = Session.load(path)
    assert again._looked == s._looked == [_REPORT_LOOK_GAP]
    assert f"{_REPORT_LOOK_GAP} marks laid with no look between them" in again.checklist()
    # A pass after the look is clean on its own.
    assert "no look between them" not in again.report(since=_REPORT_LOOK_GAP)


def test_a_painting_is_not_asked(tmp_path):
    """Not measured on paint, where a recipe lays thirty marks between looks as a
    matter of course; the rule is the drawing's."""
    s = make(tmp_path, medium="paint")
    for i in range(_REPORT_LOOK_GAP + 2):
        s.stroke([(0.1, 0.2 + 0.6 * (i % 12) / 12), (0.9, 0.2 + 0.6 * (i % 12) / 12)],
                 "flat", "burnt_umber", size=0.05)
    assert "no look between them" not in s.report(since=0)
    assert "no look between them" not in s.checklist()


# --------------------------------------------------------------------------------------
# The standing lines of a drawing
# --------------------------------------------------------------------------------------
def test_the_values_line_names_the_box_of_pencils_on_this_paper(tmp_path):
    s = make(tmp_path)
    lay(s, 4)
    paper = s._paper_value()
    floor = paper * (1.0 - GRADES["6B"].ceiling)
    assert f"of a box that reaches {floor:.2f}-{paper:.2f}" in s.report(since=0)
    p = make(tmp_path, medium="paint")
    p.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", size=0.1)
    assert (f"of a box that reaches {p.palette.darkest_value:.2f}-"
            f"{p.palette.lightest_value:.2f}") in p.report(since=0)


def test_a_drawing_prints_paper_never_touched_in_place_of_ground(tmp_path):
    s = make(tmp_path)
    lay(s, 2)
    said = s.report(since=0)
    untouched = float((s.canvas.graphite <= 0.0).mean())
    assert f"paper: {untouched:.2%} of the canvas is paper never touched" in said
    assert "ground:" not in said
    # Exact where the ground line is a tolerance: a stump over bare paper moves
    # nothing into it, and the channel says so.
    s.stump(cell("A1"), strength=1.0)
    assert float((s.canvas.graphite <= 0.0).mean()) == untouched


def test_the_pencil_line_calls_the_envelope_by_its_name_in_a_drawing(tmp_path):
    s = make(tmp_path)
    s.pencil([(0.1, 0.1), (0.9, 0.2)])
    lay(s, 1)
    assert "pencil: the envelope still shows over" in s.report(since=0)
    p = make(tmp_path, medium="paint")
    p.pencil([(0.1, 0.1), (0.9, 0.2)])
    p.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", size=0.1)
    assert "still has graphite showing" in p.report(since=0)


def test_the_lightest_line_carries_the_share_of_paper_never_touched(tmp_path):
    s = make(tmp_path)
    light, rest = span("A1", "H4"), span("A5", "H8")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(why="the light", values={light: 0.9, rest: 0.5}, lightest=light)
    s.hatch(rest, angle=0, grade="2B", tip="side", pressure=0.9)
    said = s.report(since=0)
    # The hatch's side strokes overhang the place by their half-width, so a sliver of
    # the light is touched; nearly all of it is paper.
    assert re.search(r"lightest: .*; 9\d% of it paper never touched", said), said
    s.hatch(light, angle=0, grade="2H", tip="side", pressure=0.9)
    s.stump(light, strength=1.0)
    said = s.checklist()
    assert "none of it paper never touched -- a highlight lifted is a value" in said
    # A painting's line says nothing of the paper.
    p = make(tmp_path, medium="paint")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        p.plan(why="the light", values={light: 0.9, rest: 0.5}, lightest=light)
    p.block_in(rest, "flat", "burnt_umber", size=0.1, solid=True)
    assert "paper never touched" not in p.report(since=0)


def test_the_darks_line_closes_a_drawing_and_says_how_far_they_reached(tmp_path):
    s = make(tmp_path)
    s.hatch(cell("D5"), angle=0, grade="2H", tip="side", pressure=0.5)
    said = s.checklist()
    assert re.search(r"darks: the darkest half-percentile reads 0\.\d\d, 0\.\d\d of the "
                     r"way from paper to black -- under 0\.80", said), said
    # Not a pass line: the darks come last, so the answer is only asked at the end.
    assert "darks:" not in s.report(since=0)
    for y in (0.3, 0.4, 0.5, 0.6, 0.7):
        s.line([(0.05, y), (0.95, y)], "6B", pressure=1.0, tip="side", width=0.12)
    said = s.checklist()
    reached = re.search(r"darks: .* (0\.\d\d) of the way from paper to black", said)
    assert reached and float(reached.group(1)) >= DARKS_REACH
    assert "under 0.80" not in said
    p = make(tmp_path, medium="paint")
    p.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", size=0.1)
    assert "darks:" not in p.checklist()


def test_the_bars_line_gives_a_drawing_the_drawings_remedy(tmp_path):
    s = make(tmp_path)
    before = len(s.history.records)
    for i in range(14):
        y = 0.2 + 0.6 * i / 14
        s.line([(0.1, y), (0.9, y)], "HB", pressure=0.8, tip="side", width=0.04)
    said = s.report(since=before)
    assert "a stack of bars unless the subject runs that way" in said
    assert "two angles 20 degrees or more apart" in said
    assert "direction=" not in said


# --------------------------------------------------------------------------------------
# The guide, held as the painting guide is held
# --------------------------------------------------------------------------------------
def test_the_draftsman_is_a_document_the_build_ships() -> None:
    assert docs.DOCUMENTS["draftsman"] == "DRAFTSMAN.md"
    assert docs.document_path("draftsman").is_file()
    assert set(docs.GUIDES) == {"guide", "draftsman"}


def test_the_draftsman_stays_inside_its_word_budget() -> None:
    """Set before the file was written (`easel.docs.DRAFTSMAN_WORDS`), so the first
    rule in had to be bought like every later one. Over budget, move a measurement to
    `CALIBRATION.md` or a fact to `REFERENCE.md`; do not raise the number."""
    words = len(docs.read("draftsman").split())
    assert words <= docs.DRAFTSMAN_WORDS, (
        f"DRAFTSMAN.md is {words} words, over its {docs.DRAFTSMAN_WORDS}-word budget by "
        f"{words - docs.DRAFTSMAN_WORDS}. Move a section out rather than raising this."
    )


def test_the_draftsmans_card_is_held_to_the_cards_budget() -> None:
    card = docs.front_page("draftsman")
    assert card.startswith(docs.FRONT_PAGE)
    assert [ln for ln in card.splitlines() if ln.startswith("## ")] == [docs.FRONT_PAGE]
    words = len(card.split())
    assert words <= docs.CARD_WORDS, (
        f"DRAFTSMAN.md's `The first hour` is {words} words, over its {docs.CARD_WORDS}-word "
        f"budget by {words - docs.CARD_WORDS}. Take a paragraph out rather than raising this."
    )


def test_the_draftsmans_card_carries_the_one_habit_and_the_mediums_rule() -> None:
    card = docs.front_page("draftsman")
    assert "Look every 5 to 15 strokes" in card
    assert "paper never touched" in card


@pytest.mark.parametrize("noun", ["egg", "bowl", "pear", "hen"])
def test_the_draftsman_names_no_subject_from_the_drawings_or_the_spec(noun: str) -> None:
    """`LESSONS.md`: a subject noun in the guide is the picture the next session
    draws, and the grep for the references' nouns has caught its own author seven
    times. The drawings' subjects and the spec's example are the references here."""
    text = docs.read("draftsman").casefold()
    assert not re.search(rf"\b{noun}s?\b", text), f"DRAFTSMAN.md names {noun!r}"


def test_the_draftsman_names_what_the_card_leans_on() -> None:
    """The calls a drawing's pass leans on, in the card's own code, where a reader
    who takes the code blocks for the whole page will meet them."""
    code = "\n".join(re.findall(r"```python\n(.*?)```", docs.front_page("draftsman"), re.S))
    for call in ("tip=\"side\"", "width=", "stump(", "kneaded(", "pressure=", "hatch(",
                 "contour(", "rehearse(", "cost(", "smooth=False", "thumbnail"):
        assert call in code, f"the draftsman's card no longer shows {call}"


@pytest.mark.parametrize("argv", [["guide", "--draftsman"], ["guide", "--draftsman", "--full"],
                                  ["guide", "--draftsman", "--path"]])
def test_the_shell_prints_the_draftsman(argv, capsys) -> None:
    assert main(argv) == 0
    out = capsys.readouterr().out
    assert out.strip()
    if "--path" in argv:
        assert Path(out.strip()).name == "DRAFTSMAN.md"
    elif "--full" in argv:
        assert out.strip() == docs.read("draftsman").strip()
    else:
        assert out.strip() == docs.front_page("draftsman").strip()


def test_the_reference_holds_the_drawings_rule_to_the_engine() -> None:
    """The drawing's one rule has a row of its own under *The graphite medium*, named
    by the words the check prints and carrying the number it is gated on, as the
    painting's ten are held under `report()`."""
    text = (ROOT / "REFERENCE.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if "*no look between them*" in ln]
    assert len(rows) == 1, rows
    assert f"`{_REPORT_LOOK_GAP}`" in rows[0]
    assert f"`{DARKS_REACH:.2f}`" in text
    for name in ("`paper:`", "`darks:`"):
        assert any(ln.startswith(f"| {name}") for ln in text.splitlines()), name


def test_a_drawings_standing_lines_are_rows_of_the_reference_table(tmp_path) -> None:
    """The same guard `tests/test_reference.py` keeps for a painting, made to speak by
    a drawing: every line its closing checklist prints has a row."""
    text = (ROOT / "REFERENCE.md").read_text(encoding="utf-8")
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(why="the light", values={"A1:H4": 0.9, "A5:H8": 0.5}, lightest="A1:H4",
               subject_share=0.4)
        s.pencil([(0.1, 0.8), (0.9, 0.85)])
        s.hatch(span("A5", "H8"), angle=0, grade="2B", tip="side", pressure=0.8,
                note="subject")
        s.line([(0.5, 0.5)], "HB")
        said = s.checklist()
    printed = set(re.findall(r"^  ([a-z][a-z ]*:)", said, re.M))
    assert {"landed nothing:", "plan:", "lightest:", "subject:", "values:", "edges:",
            "paper:", "pencil:", "boxes:", "darks:", "unspent:"} <= printed, said
    lines = text.split("| Line |")[1]
    named = set(re.findall(r"`([a-z][a-z ]*:)`", lines))
    assert printed <= named, f"no row for {sorted(printed - named)}"
