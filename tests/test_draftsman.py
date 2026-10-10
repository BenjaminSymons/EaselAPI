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
    lay(s, _REPORT_LOOK_GAP)
    assert "no look between them" not in s.report(since=before)
    lay(s, 1)
    said = s.report(since=before)
    assert f"{_REPORT_LOOK_GAP + 1} marks laid with no look between them" in said
    # The marks are named, as every finding that counts marks names them.
    assert f"records {before}-{before + _REPORT_LOOK_GAP}" in said


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
    lay(s, _REPORT_LOOK_GAP + 1)
    s.look()
    lay(s, 3)
    path = tmp_path / "d.easel"
    s.save(path)
    again = Session.load(path)
    assert again._looked == s._looked == [_REPORT_LOOK_GAP + 1]
    assert (f"{_REPORT_LOOK_GAP + 1} marks laid with no look between them"
            in again.checklist())
    # A pass after the look is clean on its own.
    assert "no look between them" not in again.report(since=_REPORT_LOOK_GAP + 1)


def test_a_helper_call_is_one_decision(tmp_path):
    """The lines one `hatch` lays are one decision, taken at the call: a single call of
    more lines than the gap does not fire, and counted with hand marks it counts once.
    The second drawing's painter read the rule, counted a line at a time, as a rule
    against the helpers; its refine pass's runs of 16 were a 15-line hatch and one mark."""
    s = make(tmp_path)
    before = len(s.history.records)
    laid = s.hatch(span("B2", "G5"), angle=30, grade="HB", spacing=0.012)
    assert len(laid) > _REPORT_LOOK_GAP
    assert "no look between them" not in s.report(since=before)
    # Hand marks and the call together: the call is one of the decisions, not all of
    # its lines, and the line says both counts when they differ.
    lay(s, _REPORT_LOOK_GAP)
    said = s.report(since=before)
    assert (f"{len(laid) + _REPORT_LOOK_GAP} marks in {_REPORT_LOOK_GAP + 1} calls laid "
            f"with no look between them") in said


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


def test_the_arcs_of_one_crescent_are_not_a_stack_of_bars(tmp_path):
    """The rule reads a chord, and the arcs of one crescent laid along a form share
    one: the line's own remedy for a curved passage fired it on the second drawing's
    egg, *15 of 15 long marks within 6 degrees*. A mark that turns `_REPORT_TURN_DEG`
    or more between its first step and its last is not a bar."""
    import math

    from easel.session import _REPORT_TURN_DEG, _mark_turn

    s = make(tmp_path)
    before = len(s.history.records)
    for i in range(15):
        cy = 0.35 + 0.02 * i
        pts = [(0.5 + 0.28 * math.cos(math.radians(t)), cy + 0.28 * math.sin(math.radians(t)))
               for t in range(200, 341, 10)]
        s.line(pts, "HB", pressure=0.8, tip="side", width=0.02)
    arcs = s.history.records[before:]
    assert all(_mark_turn(r, s.canvas) >= _REPORT_TURN_DEG for r in arcs)
    assert "stack of bars" not in s.report(since=before)
    assert "stack of bars" not in s.checklist()


# --------------------------------------------------------------------------------------
# The guide, held as the painting guide is held
# --------------------------------------------------------------------------------------
def test_the_draftsman_is_a_document_the_build_ships() -> None:
    assert docs.DOCUMENTS["draftsman"] == "DRAFTSMAN.md"
    assert docs.document_path("draftsman").is_file()
    assert set(docs.GUIDES) == {"guide", "draftsman"}


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
            "paper:", "pencil:", "darks:", "unspent:"} <= printed, said
    # A drawing lays no mass of the paint's kind, and the line that counted them could
    # only say so; two draftsmen asked what it was for.
    assert "boxes:" not in printed, said
    lines = text.split("| Line |")[1]
    named = set(re.findall(r"`([a-z][a-z ]*:)`", lines))
    assert printed <= named, f"no row for {sorted(printed - named)}"


def test_a_drawings_plan_line_carries_every_places_reading(tmp_path) -> None:
    """Two draftsmen running called `compare(s.plan())` after every pass because the
    `plan:` line said nothing of a place inside the threshold; a drawing's line now
    carries each one's median. A painting's line is as it was."""
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(why="the light", values={"A1:H4": 0.9, "A5:H8": 0.5}, lightest="A1:H4")
        s.hatch(span("A5", "H8"), angle=0, grade="2B", tip="side", pressure=0.8)
    line = [ln for ln in s.checklist().splitlines() if ln.strip().startswith("plan:")][0]
    assert re.search(r"plan: \d of 2 places inside 0\.10.*A1:H4 0\.\d\d", line), line
    p = make(tmp_path, medium="paint")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        p.plan(why="the light", values={"A1:H4": 0.9, "A5:H8": 0.5}, lightest="A1:H4")
        p.stroke([(0.1, 0.8), (0.9, 0.8)], "flat", "burnt_umber", size=0.1)
    line = [ln for ln in p.checklist().splitlines() if ln.strip().startswith("plan:")][0]
    assert "A1:H4 0." not in line, line


def test_a_drawings_closing_check_carries_the_loop_as_a_standing_line(tmp_path) -> None:
    """The finding fires over the line and is silent under it, and the third drawing's
    draftsman, whose longest run was 13, asked where the number had gone. The closing
    check now says the looks taken and the longest run between them whatever the run;
    the finding still fires over the line beside it. A painting is not asked."""
    s = make(tmp_path)
    lay(s, 3)
    s.look()
    lay(s, 5)
    said = s.checklist()
    line = [ln for ln in said.splitlines() if ln.strip().startswith("looks:")][0]
    assert "1 look taken" in line and "5 marks" in line, line
    assert f"5 to {_REPORT_LOOK_GAP}" in line
    assert "no look between them: the loop" not in said
    # Over the line the standing line and the finding say the same number.
    lay(s, _REPORT_LOOK_GAP - 4)
    said = s.checklist()
    assert f"{_REPORT_LOOK_GAP + 1} marks laid with no look between them" in said
    assert f"{_REPORT_LOOK_GAP + 1} marks, against" in said
    s.look()
    assert "2 looks taken, rehearsals among them" in s.checklist()
    # Helper calls are decisions here too, and the line says both counts.
    u = make(tmp_path)
    u.hatch(span("B2", "G5"), angle=30, grade="HB", spacing=0.012)
    lay(u, 1)
    assert re.search(r"looks: no look taken; .* \d+ marks in 2 calls, against", u.checklist())
    p = make(tmp_path, medium="paint")
    p.stroke([(0.1, 0.2), (0.9, 0.2)], "flat", "burnt_umber", size=0.05)
    assert "looks:" not in p.checklist()


def test_a_drawings_unspent_line_is_the_number_without_the_instruction(tmp_path) -> None:
    """Three drawings stopped with every planned place met and were each asked to
    name the weakest passage and spend the rest there, which the guide holds as a
    reserve. A drawing's line is the number; a painting's keeps the instruction."""
    s = make(tmp_path, budget=100)
    lay(s, 4)
    line = [ln for ln in s.checklist().splitlines() if ln.strip().startswith("unspent:")][0]
    assert line.strip() == "unspent: 96 of 100 unspent (96%)", line
    p = make(tmp_path, medium="paint", budget=100)
    p.stroke([(0.1, 0.2), (0.9, 0.2)], "flat", "burnt_umber", size=0.05)
    assert "name the weakest passage and spend them there" in p.checklist()


def test_a_planned_pair_the_light_is_in_says_so(tmp_path) -> None:
    """Twice a draftsman read *the light and its floor, 0.03 apart* in the same words
    as any other pair and took the two for the subject's one light mass. A pair the
    plan's own light is in says so, in the notice and in the pairs table alike."""
    s = make(tmp_path)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        s.plan(why="the light", values={"A1:H4": 0.90, "A5:H8": 0.87, "A1:D2": 0.4},
               lightest="A1:H4")
    said = [str(w.message) for w in caught if "planned pair" in str(w.message)][0]
    assert "A1:H4 is the light you declared, so against A5:H8 it has no edge" in said
    table = s._plan.pairs_text(s.plan_pairs())
    assert "A1:H4 / A5:H8: 0.03 apart, and they meet; A1:H4 is the light you declared" in table
    # Without a light named, or for a pair the light is not in, nothing is added.
    t = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        t.plan(why="the light", values={"A1:H4": 0.90, "A5:H8": 0.87})
    assert "light you declared" not in t._plan.pairs_text(t.plan_pairs())


def test_the_bars_rule_reads_a_mark_that_turns_either_side_of_its_gate(tmp_path) -> None:
    """The gate is `_REPORT_TURN_DEG`: a long mark that bends by less is a bar the
    rule counts, one that bends by more is an arc it leaves alone. Fourteen marks
    each bending by the gate less two fire the line; the same fourteen bending by
    the gate more two do not. Held at the number, so a change to it is a change to
    this test and not a quiet drift of the rule."""
    import math

    from easel.session import _REPORT_TURN_DEG, _mark_turn

    def bent_by(degrees: float) -> tuple[list[float], str]:
        s = make(tmp_path)
        before = len(s.history.records)
        turn = math.radians(degrees)
        for i in range(14):
            y = 0.2 + 0.6 * i / 14
            # Two legs along the row and a last leg turned by `degrees` in the
            # canvas's own pixels, which is the frame `_mark_turn` measures in.
            pts = [(0.1, y), (0.4, y), (0.6, y),
                   (0.6 + 0.25 * math.cos(turn),
                    y + 0.25 * math.sin(turn) * (s.canvas.width / s.canvas.height))]
            s.line(pts, "HB", pressure=0.8, tip="side", width=0.02, smooth=False)
        turns = [_mark_turn(r, s.canvas) for r in s.history.records[before:]]
        return turns, s.report(since=before)

    turns, said = bent_by(_REPORT_TURN_DEG - 2)
    assert all(abs(t - (_REPORT_TURN_DEG - 2)) < 0.1 for t in turns), turns
    assert "stack of bars" in said, said
    turns, said = bent_by(_REPORT_TURN_DEG + 2)
    assert all(abs(t - (_REPORT_TURN_DEG + 2)) < 0.1 for t in turns), turns
    assert "stack of bars" not in said, said


def test_darks_just_under_the_reach_are_said_to_be_under_it(tmp_path) -> None:
    """The line's remedy is gated on `DARKS_REACH`, and a drawing a few hundredths
    short of it is told so in the number's own words: the boundary is the number,
    not a looser one the remedy was tuned to."""
    s = make(tmp_path)
    for y in (0.3, 0.4, 0.5, 0.6, 0.7):
        s.line([(0.05, y), (0.95, y)], "4B", pressure=0.6, tip="side", width=0.12)
    said = s.checklist()
    reached = re.search(r"darks: .* (0\.\d\d) of the way from paper to black", said)
    assert reached, said
    way = float(reached.group(1))
    assert DARKS_REACH - 0.06 <= way < DARKS_REACH, f"the probe reached {way}, not just under"
    assert f"under {DARKS_REACH:.2f}" in said


def test_a_drawings_check_is_a_drawings_and_point_lines_are_not_detail(tmp_path) -> None:
    """A black-box run of the medium: the headers said *painting* over a drawing, and
    *detail before the masses are down* fired on a drawing that opened with point
    hatching, since a graphite line is under the paint rule's size by nature and a
    drawing opens with its envelope and placement lines by the method."""
    s = make(tmp_path, budget=60)
    before = len(s.history.records)
    s.hatch(span("B2", "G5"), angle=30, grade="HB", spacing=0.012)
    said = s.report(since=before)
    assert said.startswith("check over this pass")
    assert "detail before the masses" not in said
    assert "check over the drawing" in s.report()
    assert s.checklist().startswith("checklist for this drawing")
    p = make(tmp_path, medium="paint")
    assert p.checklist().startswith("checklist for this painting")


def test_a_budget_overspent_is_said_as_over(tmp_path) -> None:
    """`0 of 60 unspent` under a header saying 84 of 60 read as a budget met."""
    from easel.checklist import unspent_line

    assert unspent_line(84, 60) == "unspent: 24 over the budget of 60"
    assert unspent_line(84, 60, reserve=True) == "unspent: 24 over the budget of 60"
    assert unspent_line(60, 60) == "unspent: 0 of 60 unspent (0%)"
