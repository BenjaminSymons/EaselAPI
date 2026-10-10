"""The graphite medium's helpers: what each lays, what it leaves alone, and that the
plan, the rehearsal, the undo, the replay and the file all agree about them.

Every helper that lays graphite lays ``line`` records and nothing else; the stump and
the erasers are their own kinds, charged, snapshot by box. Assertions are on the
canvas (``LESSONS.md``, trap 3).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from easel import Session
from easel.regions import Region, blob, cell, ellipse, hull, polygon


def make(tmp_path, **kw):
    kw.setdefault("timelapse", False)
    kw.setdefault("medium", "graphite")
    return Session(480, 360, seed=4, out_dir=tmp_path, **kw)


def kinds(records) -> set[str]:
    return {r.kind for r in records}


# --------------------------------------------------------------------------------------
# The helpers that lay lines
# --------------------------------------------------------------------------------------
def test_a_hatch_is_lines_inside_its_place_and_nothing_else(tmp_path):
    s = make(tmp_path)
    rgb = s.canvas.rgb.copy()
    records = s.hatch(cell("C3"), angle=40, grade="HB", spacing=0.02)
    assert len(records) >= 5 and kinds(records) == {"graphite"}
    assert all(r.params["via"] == "hatch" for r in records)
    assert "mass" in records[0].params and "mass" not in records[1].params
    assert s.stroke_count == len(records)
    assert np.array_equal(s.canvas.rgb, rgb)
    g = s.canvas.graphite
    x0, y0, x1, y1 = s.canvas.region_px(cell("C3"))
    # The passes wander a little past the rectangle, as block_in's do: half a brush
    # and the wobble. Nothing lands further than that.
    outside = g.copy()
    outside[max(0, y0 - 10):y1 + 10, max(0, x0 - 10):x1 + 10] = 0.0
    assert float(outside.max()) < 0.02, "a hatch laid graphite far outside its place"
    assert float(g[y0:y1, x0:x1].max()) > 0.2


def test_a_hatch_on_a_shape_stops_at_the_outline(tmp_path):
    s = make(tmp_path)
    shape = blob((0.5, 0.5), 0.24, 0.18, seed=2)
    s.hatch(shape, angle=0, grade="2B", spacing=0.012)
    mask = shape.mask(s.canvas.width, s.canvas.height)
    far = ~shape.inset(-0.03).mask(s.canvas.width, s.canvas.height)
    assert float(s.canvas.graphite[far].max()) < 0.02
    assert float(s.canvas.graphite[mask].mean()) > 0.05


def test_a_crosshatch_is_one_hatch_per_angle_and_darker_than_one(tmp_path):
    one = make(tmp_path)
    a = one.hatch(cell("D4"), angle=30, grade="HB", spacing=0.015)
    two = make(tmp_path)
    b = two.crosshatch(cell("D4"), angles=(30, 120), grade="HB", spacing=0.015)
    assert len(b) > len(a)
    x0, y0, x1, y1 = one.canvas.region_px(cell("D4"))
    assert float(two.canvas.graphite[y0:y1, x0:x1].mean()) > \
        1.4 * float(one.canvas.graphite[y0:y1, x0:x1].mean())


def test_the_pressure_reads_the_same_way_on_flipped_passes(tmp_path):
    """A press_in hatch is light at one side of the place and dark at the other, on
    every pass -- the profile is reversed on the passes that run back."""
    s = make(tmp_path)
    s.hatch(Region(0.1, 0.3, 0.9, 0.7), angle=0, grade="2B", pressure="press_in",
            spacing=0.03)
    g = s.canvas.graphite
    left = g[110:250, 50:150].sum()
    right = g[110:250, 330:430].sum()
    assert right > 1.5 * left


def test_a_contour_is_one_line_round_the_outline_with_its_corners(tmp_path):
    s = make(tmp_path)
    box = polygon([(0.2, 0.2), (0.8, 0.2), (0.8, 0.8), (0.2, 0.8)])
    r = s.contour(box, grade="2B", pressure="even")
    assert r.kind == "graphite" and s.stroke_count == 1
    assert r.params.get("via") is None, "a contour is a hand mark, not a mass"
    g = s.canvas.graphite
    w, h = s.canvas.width, s.canvas.height
    assert float(g[int(0.2 * h) - 2:int(0.2 * h) + 3, int(0.3 * w):int(0.7 * w)].max()) > 0.3
    assert float(g[int(0.3 * h):int(0.7 * h), int(0.3 * w):int(0.7 * w)].max()) < 0.02
    # The corner is a corner: graphite at the vertex itself.
    assert float(g[int(0.2 * h) - 2:int(0.2 * h) + 3, int(0.2 * w) - 2:int(0.2 * w) + 3].max()) > 0.2
    open_edge = make(tmp_path).contour([(0.1, 0.5), (0.5, 0.4), (0.9, 0.5)], closed=False)
    assert len(open_edge.points) == 3
    closed = make(tmp_path).contour([(0.1, 0.5), (0.5, 0.4), (0.9, 0.5)], closed=True)
    assert len(closed.points) == 4 and closed.points[0] == closed.points[-1]


def test_a_scribble_is_zigzags_fanned_round_the_place(tmp_path):
    s = make(tmp_path)
    shape = hull([(0.2, 0.3), (0.8, 0.25), (0.75, 0.75), (0.25, 0.7)])
    records = s.scribble(shape, density=1.0, grade="2B")
    assert len(records) == 4 and kinds(records) == {"graphite"}
    assert all(r.params["via"] == "scribble" and len(r.points) >= 3 for r in records)
    assert len(make(tmp_path).scribble(shape, density=2.0)) == 8
    mask = shape.mask(s.canvas.width, s.canvas.height)
    far = ~shape.inset(-0.04).mask(s.canvas.width, s.canvas.height)
    assert float(s.canvas.graphite[mask].mean()) > 0.03
    assert float(s.canvas.graphite[far].max()) < 0.05, "a scribble strayed far outside"


def test_a_tone_lands_on_its_value_and_says_when_it_cannot(tmp_path):
    s = make(tmp_path)
    place = cell("D4")
    records = s.tone(place, 0.45, grade="2B")
    assert kinds(records) == {"graphite"} and len(records) > 2
    assert all(r.params["via"] == "tone" for r in records)
    assert records[0].params["mass"]["value"] == pytest.approx(0.45)
    read = s._median_value(s.canvas, s._place_mask(place))
    assert abs(read - 0.45) <= 0.03, f"tone landed at {read:.3f}"
    with pytest.raises(ValueError, match="asks for nothing"):
        s.tone(place, 0.60)
    with pytest.raises(ValueError, match="out of a 2H's reach"):
        s.tone(cell("A1"), 0.10, grade="2H")
    darker = make(tmp_path)
    darker.tone(place, 0.15, grade="6B")
    assert abs(darker._median_value(darker.canvas, darker._place_mask(place)) - 0.15) <= 0.03


def test_a_tone_rehearsed_is_the_tone_that_lands(tmp_path):
    s = make(tmp_path)
    trial = s.scratch()
    trial.tone(cell("E5"), 0.5)
    s.tone(cell("E5"), 0.5)
    assert np.array_equal(trial.canvas.graphite, s.canvas.graphite)


# --------------------------------------------------------------------------------------
# The stump and the erasers
# --------------------------------------------------------------------------------------
def test_a_stump_moves_graphite_and_keeps_most_of_it(tmp_path):
    s = make(tmp_path)
    s.hatch(Region(0.2, 0.3, 0.8, 0.7), angle=0, grade="2B", spacing=0.03)
    g0 = s.canvas.graphite.copy()
    laid = s.stroke_count
    r = s.stump(Region(0.2, 0.3, 0.8, 0.7), strength=0.8)
    assert r.kind == "stump" and r.paint > 0
    assert s.stroke_count == laid + 1, "a stump is one charged mark"
    g1 = s.canvas.graphite
    band = (slice(110, 250), slice(100, 380))
    assert float(g1[band].std()) < 0.6 * float(g0[band].std()), "the stump did not blend"
    kept = float(g1[band].sum()) / float(g0[band].sum())
    assert 0.85 < kept < 1.0, f"a stump kept {kept:.0%} of the graphite"
    assert "shape" in r.params or "region" in r.params, "a stump over a place logs the place"


def test_a_stump_along_a_path_blends_along_it_and_only_there(tmp_path):
    s = make(tmp_path)
    s.hatch(Region(0.1, 0.2, 0.9, 0.8), angle=90, grade="4B", spacing=0.025)
    g0 = s.canvas.graphite.copy()
    r = s.stump([(0.15, 0.5), (0.85, 0.5)], strength=0.9, width=0.05)
    assert len(r.points) == 2 and r.params["direction"] == pytest.approx(0.0)
    g1 = s.canvas.graphite
    on = (slice(170, 190), slice(80, 400))
    off = (slice(90, 110), slice(80, 400))
    assert float(g1[on].std()) < 0.7 * float(g0[on].std())
    assert np.array_equal(g1[off], g0[off]), "a stump along a path touched the far rows"


def test_erasers_lift_toward_a_ghost_and_never_to_white(tmp_path):
    s = make(tmp_path)
    s.tone(Region(0.1, 0.1, 0.9, 0.9), 0.3, grade="6B")
    g0 = s.canvas.graphite.copy()
    laid = s.stroke_count
    soft = s.kneaded(Region(0.15, 0.2, 0.45, 0.8), strength=0.5)
    assert s.stroke_count == laid + 1, "a lift is one charged mark"
    hard = s.plastic(Region(0.55, 0.2, 0.85, 0.8))
    assert s.stroke_count == laid + 2, "a second lift is one more"
    assert soft.kind == hard.kind == "lift" and soft.brush == "kneaded" and hard.brush == "plastic"
    assert soft.paint > 0 and hard.paint > 0
    g1 = s.canvas.graphite
    a, b = (slice(100, 260), slice(90, 200)), (slice(100, 260), slice(280, 390))
    assert float(g1[a].mean()) < float(g0[a].mean())
    assert float(g1[b].mean()) < 0.5 * float(g1[a].mean()), "plastic did not lift harder"
    # Where there was graphite there still is some: the ghost. (The tooth leaves a
    # few pixels bare under any tone, and those were white before the eraser.)
    had = g0[b] > 0.05
    assert had.any() and (g1[b][had] > 0.0).all(), "an eraser lifted to white"
    assert float(g1[b].mean()) > 0.02, "no ghost left under a plastic eraser"
    # The kneaded edge is soft and the plastic edge is cut: read on the column means
    # across each eraser's left edge, so the tooth's own speckle averages out.
    profile = g1[100:260].mean(axis=0)
    soft_edge = np.abs(np.diff(profile[60:100])).max()
    hard_edge = np.abs(np.diff(profile[250:290])).max()
    assert hard_edge > 2.0 * soft_edge


def test_a_lift_logs_the_whole_place(tmp_path):
    s = make(tmp_path)
    s.tone(cell("D4"), 0.4)
    shape = ellipse((0.5, 0.5), 0.1, 0.08)
    r = s.kneaded(shape, strength=0.4)
    assert r.params["shape"] and len(r.params["shape"]) == len(shape.points)
    r = s.plastic(cell("D4"))
    assert r.params["region"] == pytest.approx(list(cell("D4").bounds))


def test_stump_and_lift_undo_replay_and_round_trip(tmp_path):
    s = make(tmp_path)
    s.hatch(cell("D4"), angle=20, grade="2B", spacing=0.02)
    s.scribble(cell("E5"), density=0.5)
    kept = s.canvas.graphite.copy()
    s.stump([(0.3, 0.4), (0.7, 0.45)], strength=0.6)
    s.kneaded(cell("D4"), strength=0.5)
    s.plastic(ellipse((0.6, 0.6), 0.05, 0.05))
    s.stump(cell("E5"), strength=0.4, direction=30)
    final = s.canvas.graphite.copy()
    assert s.undo(4) == 4
    assert np.array_equal(s.canvas.graphite, kept), "undo did not put the plane back"
    s.stump([(0.3, 0.4), (0.7, 0.45)], strength=0.6)
    s.kneaded(cell("D4"), strength=0.5)
    s.plastic(ellipse((0.6, 0.6), 0.05, 0.05))
    s.stump(cell("E5"), strength=0.4, direction=30)
    assert np.array_equal(s.canvas.graphite, final)
    again = s.replay()
    assert np.array_equal(again.canvas.graphite, final)
    assert [r.kind for r in again.history.records] == [r.kind for r in s.history.records]
    back = Session.load(s.save(tmp_path / "h.easel"))
    assert np.array_equal(back.canvas.graphite, final)
    back.undo(2)
    assert np.array_equal(back.canvas.graphite, s.replay(upto=len(s.history.records) - 2)
                          .canvas.graphite)


def test_the_log_names_what_moved_and_what_lifted(tmp_path):
    s = make(tmp_path)
    s.tone(cell("D4"), 0.4)
    s.stump(cell("D4"), strength=0.5)
    s.kneaded(cell("D4"), strength=0.5)
    text = s.log(2)
    assert "moved" in text and "lifted" in text
    assert isinstance(s.report(), str) and isinstance(s.checklist(), str)


# --------------------------------------------------------------------------------------
# The plan: cost, preview, rehearse, paint
# --------------------------------------------------------------------------------------
PLAN = [{"hatch": cell("B2"), "angle": 60, "grade": "2H", "spacing": 0.02},
        {"points": [(0.6, 0.8), (0.9, 0.75)], "grade": "6B", "pressure": 0.8},
        {"contour": cell("G3"), "grade": "HB"},
        {"scribble": cell("H5"), "density": 0.5}]


def test_a_drawing_plan_costs_what_it_charges_and_lands_as_rehearsed(tmp_path):
    s = make(tmp_path)
    priced = s.cost_of(PLAN)
    assert priced[1][0] == 1 and priced[2][0] == 1 and priced[3][0] == 2
    assert "lines" in priced[0][1]
    trial = s.scratch()
    trial.paint(PLAN)
    records = s.paint(PLAN)
    assert len(records) == s.cost(PLAN) == s.stroke_count
    assert np.array_equal(trial.canvas.graphite, s.canvas.graphite)
    s.preview(PLAN)
    s.rehearse(PLAN)


def test_a_bare_path_is_a_line_in_a_drawing_and_a_stroke_in_a_painting(tmp_path):
    d = make(tmp_path)
    assert d._plan_specs([(0.1, 0.1), (0.5, 0.5)])[0][0] == "line"
    assert d._plan_specs({"points": [(0.1, 0.1), (0.5, 0.5)], "brush": "liner"})[0][0] == "stroke"
    p = make(tmp_path, medium="paint")
    assert p._plan_specs([(0.1, 0.1), (0.5, 0.5)])[0][0] == "stroke"
    assert p._plan_specs({"points": [(0.1, 0.1), (0.5, 0.5)], "grade": "HB"})[0][0] == "line"
    with pytest.raises(ValueError, match="does not take"):
        d.cost({"hatch": cell("B2"), "color": "burnt_umber"})


def test_a_hatch_and_a_tone_are_in_the_thumbnail(tmp_path):
    s = make(tmp_path)
    s.hatch(cell("B2"), grade="2B", spacing=0.01)
    s.tone(cell("F6"), 0.5)
    s.scribble(cell("D4"))
    layers, unplaced, _fresh = s._laid_masses()
    assert len(layers) == 3 and unplaced == 0
    assert layers[1][1] == pytest.approx(0.5)
    assert 0.0 < layers[0][1] < 0.95


# --------------------------------------------------------------------------------------
# Undo through the rebuild, two seeds alike, and a place that is not there
# --------------------------------------------------------------------------------------
def test_a_stump_and_the_lifts_undo_past_the_snapshots_by_rebuilding(tmp_path):
    """The stump and the erasers snapshot one channel by box, and an undo past what
    the snapshots hold is a rebuild from the log. Both roads must land on the plane
    `replay(upto=k)` lands on, exactly, or a long drawing's undo of a stump leaves a
    blend the painter cannot see and cannot take back."""
    s = make(tmp_path)
    s.hatch(cell("D4"), angle=20, grade="2B", spacing=0.03)
    hatched = len(s.history.records)
    s.stump(cell("D4"), strength=0.6)
    s.kneaded(cell("D4"), strength=0.5)
    s.plastic(ellipse((0.5, 0.5), 0.04, 0.04))
    after_stump = s.replay(upto=hatched + 1).canvas.graphite
    before_stump = s.replay(upto=hatched).canvas.graphite
    s.history.invalidate_snapshots()
    assert s.undo(2) == 2
    assert np.array_equal(s.canvas.graphite, after_stump), \
        "the rebuilt undo of two lifts is not the replay to the stump"
    assert s.undo(1) == 1
    assert np.array_equal(s.canvas.graphite, before_stump), \
        "the rebuilt undo of the stump is not the replay to the hatch"
    assert len(s.history.records) == hatched


def test_two_sessions_from_one_seed_lay_the_same_scribble_tone_and_stump(tmp_path):
    """The helpers draw their wander from the stream and the stump reads the plane;
    a film, a rehearsal and a reload all lean on one seed giving one drawing."""
    def drawn() -> np.ndarray:
        s = Session(160, 120, seed=4, out_dir=tmp_path, timelapse=False, medium="graphite")
        s.scribble(cell("C3"), density=0.5)
        s.tone(cell("D4"), 0.5, grade="2B")
        s.stump(cell("D4"), strength=0.5)
        return s.canvas.graphite.copy()
    assert np.array_equal(drawn(), drawn())
    other = Session(160, 120, seed=5, out_dir=tmp_path, timelapse=False, medium="graphite")
    other.scribble(cell("C3"), density=0.5)
    assert not np.array_equal(other.canvas.graphite, drawn()), "the seed did nothing"


def test_a_tone_on_a_place_covering_no_pixel_says_so_and_lays_nothing(tmp_path):
    """A shape under a pixel across has an empty mask, and a median over no pixels is
    numpy's NaN warning and a plan of passes toward nothing. The verb says which
    place, before any pass is measured, and the log is as it was. (A `Region` never
    reaches this: `region_px` keeps it one pixel at least.)"""
    s = make(tmp_path)
    speck = ellipse((0.5, 0.5), 0.001, 0.001)
    assert not s._place_mask(speck).any(), "the probe place covers a pixel after all"
    before, depth = len(s.history.records), s.history.undo_depth
    with pytest.raises(ValueError, match="covers no pixel"):
        s.tone(speck, 0.3, grade="2B")
    assert (len(s.history.records), s.history.undo_depth) == (before, depth)


# --------------------------------------------------------------------------------------
# What the helpers refuse, and that a refusal leaves no trace
# --------------------------------------------------------------------------------------
def untouched(s: Session):
    return len(s.history.records), s.history.undo_depth


def test_a_hatch_with_no_spacing_is_refused_and_lays_nothing(tmp_path):
    """`spacing=0` once laid a thousand charged lines over one cell before the loop
    gave up, which spent a drawing's whole budget on a typo. It is refused in the
    hatch's own words, before a line is laid, and so is a negative one."""
    s = make(tmp_path)
    s.line([(0.1, 0.1), (0.9, 0.9)], "HB")
    state = untouched(s)
    for bad in (0, -0.02):
        with pytest.raises(ValueError, match="spacing"):
            s.hatch(cell("C3"), angle=40, grade="HB", spacing=bad)
        assert untouched(s) == state, f"hatch(spacing={bad}) left a record or a snapshot"
    with pytest.raises(ValueError, match="spacing"):
        s.crosshatch(cell("C3"), angles=(30, 120), spacing=0)
    assert untouched(s) == state


def test_a_scribble_with_no_density_is_refused_and_lays_nothing(tmp_path):
    s = make(tmp_path)
    s.line([(0.1, 0.1), (0.9, 0.9)], "HB")
    state = untouched(s)
    for bad in (0, -1.0):
        with pytest.raises(ValueError, match="density"):
            s.scribble(cell("C3"), density=bad)
        assert untouched(s) == state


def test_a_kneaded_eraser_with_no_strength_is_refused_and_lifts_nothing(tmp_path):
    """A strength of nought is a lift record that moved nothing, charged against the
    budget; the eraser says what a strength is instead."""
    s = make(tmp_path)
    s.tone(cell("D4"), 0.4)
    state = untouched(s)
    for bad in (0, -0.5):
        with pytest.raises(ValueError, match="strength"):
            s.kneaded(cell("D4"), strength=bad)
        assert untouched(s) == state


def test_an_eraser_handed_a_path_names_the_stump(tmp_path):
    """A run of points is what `stump()` takes, and a draftsman who reaches for the
    eraser the same way was answered by the region parser's complaint about a tuple.
    Each eraser now names itself and the verb that takes a path."""
    s = make(tmp_path)
    s.tone(cell("D4"), 0.4)
    state = untouched(s)
    path = [(0.1, 0.1), (0.5, 0.5)]
    with pytest.raises(ValueError, match=r"kneaded\(\) lifts over a place.*stump\(\)"):
        s.kneaded(path, strength=0.5)
    with pytest.raises(ValueError, match=r"plastic\(\) lifts over a place.*stump\(\)"):
        s.plastic(path)
    assert untouched(s) == state


def test_a_crosshatch_handed_one_angle_names_angles(tmp_path):
    """`crosshatch(angle=30)` is `hatch()`'s keyword on the verb that takes a
    sequence; it fell through `**kw` into `hatch(angle=[30, 120], angle=30)` and
    Python's own `TypeError` about a repeated keyword. The verb says which keyword
    it takes, and nothing is laid."""
    s = make(tmp_path)
    state = untouched(s)
    with pytest.raises(TypeError, match="angles="):
        s.crosshatch(cell("D4"), angle=30)
    assert untouched(s) == state


def test_a_tone_at_no_pressure_says_it_lays_nothing_and_leaves_no_record(tmp_path):
    """A pass that moves the place not at all is not laid and not charged, and when
    it is the first pass there is no tone to lay: the verb says so, naming the
    pressure and the grade, rather than returning an empty list that reads as done."""
    s = make(tmp_path)
    state = untouched(s)
    with pytest.raises(ValueError, match="lays nothing"):
        s.tone(cell("D4"), 0.25, grade="2B", pressure=0.0)
    assert untouched(s) == state
    assert not s.canvas.has_graphite


def test_a_counted_copy_prices_a_tone_at_the_lines_it_lays(tmp_path):
    """`scratch(count_only=True)` skips the pixel work, and a tone's trial inherited
    the skip: every pass read the same value, so every tone was priced at one pass,
    and `easel run --count` under-quoted a four-pass tone by four. The count is the
    lines the real call lays, on fresh equal sessions."""
    priced = make(tmp_path).scratch(count_only=True)
    laid = make(tmp_path)
    counted = priced.tone(cell("D4"), 0.25, "2B")
    real = laid.tone(cell("D4"), 0.25, "2B")
    assert len(real) > 1, "the probe tone is one pass, which the bug priced right"
    assert len(counted) == len(real)
    assert priced.spent == laid.spent
    # And the copy laid nothing while it counted.
    assert not priced.canvas.has_graphite and laid.canvas.has_graphite


def test_a_stump_runs_along_a_hatch_at_the_same_angle_on_any_canvas(tmp_path):
    """`direction=` is an angle in the 0..1 space, as `hatch(angle=)` and every other
    direction here is: on 800x400 a hatch at 45 runs at 26.6 degrees on screen, and a
    stump at 45 was a screen angle, 18 degrees off it. The record keeps what was given
    and the screen angle the kernel ran at, and a record from before this -- the
    screen angle alone -- replays by it, exactly."""
    s = Session(800, 400, medium="graphite", seed=3, out_dir=tmp_path, timelapse=False)
    s.hatch(cell("D4"), angle=45, grade="2B", tip="side")
    r = s.stump(cell("D4"), strength=0.5, direction=45)
    assert r.params["given"] == 45.0
    assert abs(r.params["direction"] - math.degrees(math.atan2(399, 799))) < 1e-6
    along = s.stump(cell("D4"), strength=0.3, direction=[(0.1, 0.1), (0.9, 0.9)])
    assert along.params["given"] == 45.0
    assert np.array_equal(s.replay().canvas.graphite, s.canvas.graphite)
    # A path's own direction is the screen's, read off its pixels, and is not given.
    path = s.stump([(0.1, 0.5), (0.9, 0.5)], strength=0.3)
    assert path.params["given"] is None and path.params["direction"] == 0.0
    # The record from before: strip what it did not have, and the replay still lands,
    # exactly, since the screen angle is passed through and never inverted -- the
    # inverse through atan2 is not exact to the bit, and on 1024x768 at 45 degrees a
    # kernel a hair off its angle moved thirteen thousand pixels. The replayed record
    # stays a record without `given`, so a rebuilt undo does not rewrite the log.
    t = Session(1024, 768, medium="graphite", seed=5, out_dir=tmp_path, timelapse=False)
    t.hatch("B2:G5", angle=30, grade="2B", tip="side")
    for i, angle in enumerate((45, -45, 90, 270, 30, 170.5, -360)):
        t.stump(cell("CDEF"[i % 4] + str(2 + i % 4)), strength=0.5, direction=angle)
    file = tmp_path / "d.easel"
    t.save(file)
    old = Session.load(file)
    for rec in old.history.records:
        rec.params.pop("given", None)
    back = old.replay()
    assert np.array_equal(back.canvas.graphite, old.canvas.graphite)
    for rec in back.history.records:
        if rec.kind == "stump":
            assert "given" not in rec.params
    assert ([r.params["direction"] for r in back.history.records if r.kind == "stump"]
            == [r.params["direction"] for r in old.history.records if r.kind == "stump"])
