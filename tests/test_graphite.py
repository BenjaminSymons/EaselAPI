"""The graphite medium: the channel, the grades, the stroke, and what it leaves alone.

Assertions are on the canvas, not on return values (``LESSONS.md``, trap 3): the plane
is diffed either side of every mark. And on what a graphite mark must *not* touch --
the paint channels and the sketch -- because the medium was added beside the paint,
never through it, and that is the contract every stored golden depends on.
"""

from __future__ import annotations

import json

import numpy as np
import pytest

from easel import GRADES, Session
from easel.canvas import Canvas
from easel.graphite import GRAPHITE_TIPS, get_grade
from easel.history import History
from easel.regions import Region, cell
from easel.stroke import draw_graphite
from easel.texture import TEXTURES, make_texture


def make(tmp_path, **kw):
    kw.setdefault("timelapse", False)
    kw.setdefault("medium", "graphite")
    return Session(480, 360, seed=4, out_dir=tmp_path, **kw)


LINE = [(0.15, 0.5), (0.5, 0.45), (0.85, 0.55)]


def band(s: Session, y0: int = 150, y1: int = 210, x0: int = 90, x1: int = 390):
    return s.canvas.graphite[y0:y1, x0:x1]


# --------------------------------------------------------------------------------------
# The medium, declared
# --------------------------------------------------------------------------------------
def test_a_drawing_is_on_cartridge_and_a_painting_on_linen(tmp_path):
    assert make(tmp_path).canvas.texture_name == "cartridge"
    assert make(tmp_path, medium="paint").canvas.texture_name == "linen"
    assert make(tmp_path, texture="rough").canvas.texture_name == "rough"


def test_an_unknown_medium_names_the_two(tmp_path):
    with pytest.raises(ValueError, match="paint, graphite"):
        make(tmp_path, medium="charcoal")


def test_a_drawing_looks_in_values_unless_told_otherwise(tmp_path):
    s = make(tmp_path)
    s.line(LINE, "6B", pressure=1.0)
    grey = np.asarray(s.look_image(scale=240), dtype=np.int16)
    assert (grey[..., 0] == grey[..., 1]).all() and (grey[..., 1] == grey[..., 2]).all()
    colour = np.asarray(s.look_image(scale=240, values=False), dtype=np.int16)
    assert not ((colour[..., 0] == colour[..., 1]).all()
                and (colour[..., 1] == colour[..., 2]).all()), \
        "values=False still rendered the drawing in greyscale"
    p = make(tmp_path, medium="paint")
    p.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "cadmium_red")
    red = np.asarray(p.look_image(scale=240), dtype=np.int16)
    assert (red[..., 0] != red[..., 1]).any(), "a painting's look lost its colour"


# --------------------------------------------------------------------------------------
# The stroke
# --------------------------------------------------------------------------------------
def test_a_line_lays_graphite_and_nothing_else(tmp_path):
    """No paint, no wetness, no height, and no sketch: a channel of its own."""
    s = make(tmp_path)
    rgb, sketch = s.canvas.rgb.copy(), s.canvas.sketch.copy()
    record = s.line(LINE, "HB", pressure=0.6)
    assert record.kind == "graphite" and record.brush == "HB"
    assert record.paint > 0, "the line reported drawing nothing"
    assert s.canvas.has_graphite and float(band(s).max()) > 0.2
    assert np.array_equal(s.canvas.rgb, rgb), "a graphite line deposited paint"
    assert np.array_equal(s.canvas.sketch, sketch) and not s.canvas.has_sketch
    assert float(s.canvas.wetness.max()) == 0.0
    assert float(s.canvas.thickness.max()) == 0.0


def test_a_line_is_charged_and_a_pencil_beside_it_is_not(tmp_path):
    s = make(tmp_path)
    s.pencil(LINE)
    assert s.stroke_count == 0
    s.line(LINE, "2B")
    assert s.stroke_count == 1
    assert "graphite" not in History.UNPAINTED_KINDS


def test_the_channel_is_in_the_view_and_in_the_values(tmp_path):
    """What is drawn is what is seen: the greyscale view, the export and the
    thumbnail all read the channel, in the unit it is defined in."""
    s = make(tmp_path)
    bare = s.canvas.values().copy()
    s.line(LINE, "6B", pressure=1.0)
    values = s.canvas.values()
    drawn = s.canvas.graphite > 0.5
    assert drawn.any()
    assert (values[drawn] < bare[drawn] - 100).all(), "the view did not darken where drawn"
    # The unit: paper's value times what the graphite leaves, to a level or two.
    paper = float(bare[drawn].mean()) / 255.0
    left = 1.0 - s.canvas.graphite[drawn].astype(np.float64)
    expected = paper * left
    assert np.abs(values[drawn] / 255.0 - expected).max() < 0.02
    # Hidden by nothing: the sketch flag hides the underdrawing and the overlay only.
    assert np.array_equal(s.canvas.values(sketch=False), values)
    s.line([(0.2, 0.2), (0.8, 0.25)], "6B", pressure=1.0, tip="side")
    thumb = s.canvas.thumbnail_srgb8(120)
    assert int(thumb.min()) < 60, "the time-lapse frame did not show the drawing"


def test_pressure_darkens_widens_and_fills_the_tooth(tmp_path):
    def laid(press):
        s = make(tmp_path)
        # Wide enough for the width to be measured in pixels on a 480-wide canvas:
        # at the grade's own width both pressures round to a two-pixel line.
        s.line([(0.1, 0.5), (0.9, 0.5)], "2B", pressure=press, smooth=False, width=0.02)
        g = s.canvas.graphite
        touched = g > 0.02
        return float(g.max()), int(touched.any(axis=0).sum()), int(touched.sum(axis=0).max()), \
            float((g[touched] > 0.3 * g.max()).mean())
    light, heavy = laid(0.25), laid(1.0)
    assert heavy[0] > light[0] * 1.5, "pressure did not darken the line"
    assert heavy[2] > light[2], "pressure did not widen a point line"
    assert heavy[3] > light[3], "pressure did not fill more of the tooth"


def test_grades_sit_in_order_and_saturate_toward_their_own_ceiling(tmp_path):
    """Three passes of each grade over one patch: darker down the box, and no grade
    past its ceiling however many times it is laid."""
    def patch(grade, passes):
        s = make(tmp_path)
        for _k in range(passes):
            for i in range(6):
                y = 0.40 + i * 0.03
                s.line([(0.2, y), (0.8, y)], grade, pressure=1.0, tip="side", smooth=False)
        g = s.canvas.graphite[150:210, 140:340]
        return float(np.median(g)), float(g.max())
    order = [patch(name, 3)[0] for name in GRADES]
    assert order == sorted(order), f"grades out of order: {dict(zip(GRADES, order, strict=True))}"
    assert order[0] < 0.4 and order[-1] > 0.85
    for name, grade in GRADES.items():
        assert patch(name, 6)[1] <= grade.ceiling + 1e-4, f"{name} was pushed past its ceiling"
    two, six = patch("2H", 8)[0], patch("6B", 1)[0]
    assert two < six, "eight passes of a 2H laid a 6B's black"


def test_a_stroke_accumulates_as_a_maximum_and_strokes_add(tmp_path):
    """One stroke's overlapping dabs are not a bar; a second stroke over the first is
    darker than the first alone. The rule ``LESSONS.md`` lists as load-bearing."""
    s = make(tmp_path)
    s.line([(0.1, 0.5), (0.9, 0.5)], "HB", pressure=0.5, smooth=False)
    once = s.canvas.graphite.copy()
    core = once[once > 0.5 * once.max()]
    # A pencil line at half pressure is a mid grey, not the grade's ceiling.
    assert float(np.median(core)) < 0.55 * GRADES["HB"].ceiling + 0.15
    s.line([(0.1, 0.5), (0.9, 0.5)], "HB", pressure=0.5, smooth=False)
    twice = s.canvas.graphite
    where = once > 0.1
    assert float(twice[where].mean()) > float(once[where].mean()) * 1.2
    assert float(twice.max()) <= GRADES["HB"].ceiling + 1e-4


def test_the_side_is_wider_than_the_point_and_follows_the_stroke(tmp_path):
    def across(tip):
        s = make(tmp_path)
        s.line([(0.1, 0.5), (0.9, 0.5)], "2B", pressure=0.8, tip=tip, smooth=False)
        return int((s.canvas.graphite > 0.02).sum(axis=0).max())
    assert across("side") > 3 * across("point")


def test_a_shape_is_drawn_as_its_outline(tmp_path):
    s = make(tmp_path)
    s.line(cell("D4"), "HB", pressure=0.8)
    g = s.canvas.graphite
    x0, y0, x1, y1 = s.canvas.region_px(cell("D4"))
    inside = g[y0 + 8:y1 - 8, x0 + 8:x1 - 8]
    assert float(inside.max()) < 0.02, "the outline filled the cell"
    assert float(g[y0 - 3:y0 + 4, x0:x1].max()) > 0.3, "no line along the cell's top"


def test_unknown_grade_and_tip_name_the_choices(tmp_path):
    s = make(tmp_path)
    with pytest.raises(ValueError, match="4H, 2H, HB, 2B, 4B, 6B"):
        s.line(LINE, "9B")
    with pytest.raises(ValueError, match="point or its side"):
        s.line(LINE, "HB", tip="flat")
    assert get_grade("hb").name == "HB" and GRAPHITE_TIPS == ("point", "side")
    with pytest.raises(TypeError, match="grade= is a pencil"):
        s.stroke(LINE, "bristle", "burnt_umber", grade="HB")


def test_nothing_is_laid_off_the_canvas():
    c = Canvas(120, 80, texture="cartridge", ground="white", seed=2)
    r = draw_graphite(c, [(-0.5, -0.5), (-0.2, -0.3)], "6B", 1.0)
    assert r.paint == 0.0 and not c.has_graphite
    r = draw_graphite(c, [(0.9, 0.5), (1.4, 0.6)], "6B", 1.0, tip="side")
    assert r.paint > 0.0 and np.isfinite(c.graphite).all()


# --------------------------------------------------------------------------------------
# Undo, replay, the file, the rehearsal
# --------------------------------------------------------------------------------------
def test_undo_restores_the_plane_exactly_and_only_the_plane(tmp_path):
    s = make(tmp_path)
    s.line(LINE, "HB")
    s.stroke([(0.1, 0.8), (0.9, 0.8)], "bristle", "burnt_umber")
    kept_g, kept_rgb = s.canvas.graphite.copy(), s.canvas.rgb.copy()
    s.line([(0.1, 0.2), (0.9, 0.3)], "6B", pressure=1.0, tip="side")
    s.line([(0.2, 0.7), (0.8, 0.7)], "2B")
    assert not np.array_equal(s.canvas.graphite, kept_g)
    assert s.undo(2) == 2
    assert np.array_equal(s.canvas.graphite, kept_g), "undo did not put the plane back"
    assert np.array_equal(s.canvas.rgb, kept_rgb), "undo of a graphite mark moved the paint"
    assert s.stroke_count == 2


def test_a_boxed_graphite_snapshot_keeps_one_channel(tmp_path):
    s = make(tmp_path)
    s.line(LINE, "HB")
    snap = s.history._snapshots[-1]
    assert set(snap) == {"box", "graphite", "stroke_count"}
    s.line(LINE, "HB")
    snap = s.history._snapshots[-1]
    h, w = snap["graphite"].shape
    assert h < s.canvas.height and w < s.canvas.width


def test_undo_past_the_snapshots_rebuilds_the_same_drawing(tmp_path):
    s = make(tmp_path)
    for i in range(6):
        s.line([(0.1, 0.1 + i * 0.12), (0.9, 0.15 + i * 0.12)], "2B", pressure=0.4 + i * 0.1)
    kept = s.replay(upto=3).canvas.graphite
    s.history.invalidate_snapshots()
    s.undo(3)
    assert np.array_equal(s.canvas.graphite, kept)


def test_a_drawing_replays_exactly(tmp_path):
    s = make(tmp_path)
    s.pencil([(0.1, 0.9), (0.9, 0.85)])
    s.line(LINE, "2H", pressure=0.3)
    s.line(Region(0.2, 0.2, 0.8, 0.6), "4B", pressure="taper", tip="side")
    s.stroke([(0.1, 0.8), (0.9, 0.8)], "bristle", "burnt_umber")
    s.line([(0.3, 0.3), (0.7, 0.35)], "6B", pressure=[0.2, 1.0, 0.4], width=0.01)
    again = s.replay()
    assert np.array_equal(again.canvas.graphite, s.canvas.graphite)
    assert np.array_equal(again.canvas.rgb, s.canvas.rgb)
    assert np.array_equal(again.canvas.sketch, s.canvas.sketch)
    assert again.medium == "graphite"
    assert [r.kind for r in again.history.records] == [r.kind for r in s.history.records]


def test_a_drawing_survives_the_file(tmp_path):
    s = make(tmp_path)
    s.line(LINE, "HB", pressure=0.7, note="a line")
    s.line([(0.2, 0.2), (0.8, 0.3)], "4B", tip="side")
    path = s.save(tmp_path / "d.easel")
    back = Session.load(path)
    assert back.medium == "graphite" and back.canvas.texture_name == "cartridge"
    assert back.canvas.has_graphite
    assert np.array_equal(back.canvas.graphite, s.canvas.graphite)
    assert np.array_equal(back.canvas.to_srgb8(), s.canvas.to_srgb8())
    assert back.history.records[-1].params["grade"] == "4B"
    # And undo from the file, which is a replay, lands on the same plane.
    before = s.replay(upto=1).canvas.graphite
    back.undo(1)
    assert np.array_equal(back.canvas.graphite, before)


def test_a_painting_that_never_drew_stores_no_graphite_and_an_old_file_opens(tmp_path):
    s = make(tmp_path, medium="paint")
    s.stroke([(0.1, 0.1), (0.9, 0.9)], "bristle", "burnt_umber")
    path = s.save(tmp_path / "p.easel")
    with np.load(path, allow_pickle=False) as data:
        assert data["graphite"].size == 0
        fields = {k: data[k] for k in data.files}
    back = Session.load(path)
    assert not back.canvas.has_graphite and back.medium == "paint"
    assert back.canvas.graphite.shape == (back.canvas.height, back.canvas.width)
    # A file written before the medium existed: no key, no array.
    meta = json.loads(str(fields.pop("meta")))
    meta.pop("medium")
    meta.pop("has_graphite")
    fields.pop("graphite")
    with open(path, "wb") as fh:
        np.savez_compressed(fh, meta=np.array(json.dumps(meta)), **fields)
    old = Session.load(path)
    assert old.medium == "paint" and not old.canvas.has_graphite
    assert np.array_equal(old.canvas.to_srgb8(), s.canvas.to_srgb8())


def test_a_rehearsal_draws_on_a_copy_and_lands_the_same_mark(tmp_path):
    s = make(tmp_path)
    s.line(LINE, "HB")
    kept = s.canvas.graphite.copy()
    trial = s.scratch()
    assert trial.medium == "graphite"
    trial.line([(0.2, 0.2), (0.8, 0.3)], "4B", tip="side")
    assert np.array_equal(s.canvas.graphite, kept), "a rehearsal drew on the painting"
    s.line([(0.2, 0.2), (0.8, 0.3)], "4B", tip="side")
    assert np.array_equal(trial.canvas.graphite, s.canvas.graphite), \
        "what was rehearsed is not what landed"
    counted = s.scratch(count_only=True)
    counted.line(LINE, "6B")
    assert counted.spent == s.spent + 1


def test_the_log_says_graphite_and_the_check_does_not_fall_over(tmp_path):
    s = make(tmp_path)
    for i in range(12):
        s.line([(0.1, 0.1 + i * 0.07), (0.9, 0.12 + i * 0.07)], "HB", pressure=0.5)
    s.line([(0.5, 0.1), (0.5, 0.9)], "2B", tip="side")
    text = s.log(3)
    assert "graphite" in text and "paint" not in text.replace("graphite", "")
    assert isinstance(s.report(), str) and isinstance(s.checklist(), str)


# --------------------------------------------------------------------------------------
# The paper
# --------------------------------------------------------------------------------------
def test_cartridge_is_a_texture_between_smooth_and_linen():
    assert "cartridge" in TEXTURES and TEXTURES[-1] == "cartridge"
    spans = {}
    for name in ("smooth", "cartridge", "linen"):
        h = make_texture(name, 300, 400, np.random.default_rng(3))
        spans[name] = float(np.percentile(h, 95) - np.percentile(h, 5))
        assert 0.4 < float(h.mean()) < 0.6
    assert spans["smooth"] < spans["cartridge"] < spans["linen"]
    a = make_texture("cartridge", 60, 80, np.random.default_rng(9))
    b = make_texture("cartridge", 60, 80, np.random.default_rng(9))
    assert np.array_equal(a, b)


def test_a_pressure_that_is_not_a_number_is_refused_in_the_painters_words(tmp_path):
    """A string, a None or a complex in a pressure list used to surface from under the
    stroke as numpy's own complaint -- `could not convert string to float`, `cannot
    convert float NaN to integer` -- naming nothing the draftsman wrote; the third
    drawing's helper handed one over. The error names what a pressure is, and the
    refused mark leaves no record and no snapshot behind."""
    s = make(tmp_path)
    s.line([(0.1, 0.1), (0.9, 0.9)], "HB")
    before, depth = len(s.history.records), s.history.undo_depth
    for bad in (["a", 0.5], [0.2, 1 + 2j], [0.2, None], [0.2, float("nan")]):
        with pytest.raises(ValueError, match=r"A pressure is a number in 0\.\.1"):
            s.line([(0.1, 0.1), (0.9, 0.9)], "HB", pressure=bad)
    with pytest.raises(ValueError, match="Unknown pressure profile"):
        s.line([(0.1, 0.1), (0.9, 0.9)], "HB", pressure="squeeze")
    assert (len(s.history.records), s.history.undo_depth) == (before, depth)


def test_undo_interleaves_paint_and_graphite_and_puts_each_channel_back_in_turn(tmp_path):
    """A paint stroke over a graphite line and a line over the paint: the two
    channels are snapshot apart, so each undo restores exactly the channel its mark
    touched and leaves the other alone. The test the stored goldens lean on, since
    the medium was added beside the paint and never through it."""
    s = make(tmp_path)
    s.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "burnt_umber")
    rgb_a, g_a = s.canvas.rgb.copy(), s.canvas.graphite.copy()
    assert not g_a.any(), "a paint stroke laid graphite"
    s.line([(0.1, 0.4), (0.9, 0.6)], "6B", pressure=1.0, tip="side")
    rgb_b, g_b = s.canvas.rgb.copy(), s.canvas.graphite.copy()
    assert np.array_equal(rgb_b, rgb_a) and g_b.any()
    s.stroke([(0.1, 0.6), (0.9, 0.4)], "flat", "ultramarine")
    rgb_c, g_c = s.canvas.rgb.copy(), s.canvas.graphite.copy()
    assert not np.array_equal(rgb_c, rgb_b) and np.array_equal(g_c, g_b)
    s.line([(0.5, 0.1), (0.5, 0.9)], "2B")
    assert not np.array_equal(s.canvas.graphite, g_c)
    # Undo the line over the paint: the plane goes back, the paint stays.
    assert s.undo(1) == 1
    assert np.array_equal(s.canvas.graphite, g_c) and np.array_equal(s.canvas.rgb, rgb_c)
    # Undo the paint over the line: the paint goes back, the plane stays.
    assert s.undo(1) == 1
    assert np.array_equal(s.canvas.rgb, rgb_b), "undo of a paint stroke did not restore the paint"
    assert np.array_equal(s.canvas.graphite, g_b), "undo of a paint stroke moved the graphite"
    # Undo the line over the paint stroke: the plane is bare, the paint is the first stroke.
    assert s.undo(1) == 1
    assert np.array_equal(s.canvas.graphite, g_a) and np.array_equal(s.canvas.rgb, rgb_a)
    assert s.stroke_count == 1
    # And the rebuild road, with the snapshots gone, lands on the same two channels.
    s.line([(0.1, 0.4), (0.9, 0.6)], "6B", pressure=1.0, tip="side")
    s.stroke([(0.1, 0.6), (0.9, 0.4)], "flat", "ultramarine")
    s.history.invalidate_snapshots()
    assert s.undo(1) == 1
    assert np.array_equal(s.canvas.rgb, rgb_b) and np.array_equal(s.canvas.graphite, g_b)
