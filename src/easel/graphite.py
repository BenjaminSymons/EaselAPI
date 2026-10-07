"""Graphite as a medium: the pencil grades and the two ways a pencil meets the paper.

The paint engine has a pencil already -- :meth:`easel.session.Session.pencil`, a free
underdrawing in the ``sketch`` channel that paint buries. This is the other thing a
pencil is: the picture itself, in a channel of its own (``Canvas.graphite``) that
nothing buries and that counts against the budget like paint. The two live beside
each other on purpose: a graphite drawing still gets its free envelope in ``sketch``.

A grade is six numbers, each holding one invariant:

``ceiling``
    how far from the paper toward black the grade can be pushed, as a fraction of the
    way: ``0.96`` for a 6B means the darkest 6B leaves 4% of the paper's value. The
    channel is defined in that unit (see :meth:`easel.canvas.Canvas.lay_graphite`), so
    this is the number ``compare()`` and ``look(values=True)`` read back.
``rate``
    how fast one stroke closes on that ceiling: a full-pressure pass takes
    ``1 - exp(-rate)`` of what is left. The unit is the stroke, not the dab -- within
    a stroke graphite accumulates as a maximum, the way it always has
    (``LESSONS.md``, *Graphite accumulates as a maximum, not a sum*).
``gamma``
    how pressure becomes darkness, ``pressure ** gamma``. Above 1 a grade stays light
    until leant on, which is what a hard pencil does.
``bite``, ``bite_gain``
    how far into the tooth the point reaches, ``bite + bite_gain * pressure``, as the
    share of the gating field it fills: ``0`` catches only the highest peaks, ``1``
    fills every valley. A hard grade speckles under heavy pressure and a soft one
    fills under light, and this is the term that lets the two differ at one pressure.
``width``, ``width_floor``
    the point's line width as a fraction of the canvas long side, and how much of it
    the lightest touch keeps -- a 4H holds its point whatever the hand does, a 6B
    spreads under it.

The numbers are the starting table from the spec, written as the invariant each one
holds rather than as a value, and calibrated on ``samples/pencils.png`` and the value
scale in ``CALIBRATION.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

from easel.brush import Brush

__all__ = ["Grade", "GRADES", "GRAPHITE_TIPS", "get_grade", "tip_brush",
           "SIDE_WIDTH", "SIDE_ASPECT"]

#: The two ways a pencil meets the paper: its point, or laid over on its side.
GRAPHITE_TIPS = ("point", "side")

#: The side of the lead as a mark: its width as a fraction of the canvas long side,
#: and how thick it is along its travel as a share of that width -- the ``flat`` tip's
#: geometry (``brush.py``), rotated to the stroke, so consecutive stamps overlap. Wide
#: on purpose: a side-of-pencil mark is how a mass is laid, and the point is how a line
#: is. The grade's own ``width`` is the point's; the side has one width for every grade.
SIDE_WIDTH = 0.024
SIDE_ASPECT = 0.30
#: The side rides on the peaks of the tooth more than the point does -- a broad lead
#: cannot get into the valleys a point can -- so its bite is the point's less this.
SIDE_BITE = 0.12
#: ...and it lays less per pass, since the same graphite is spread over a wider mark.
SIDE_RATE = 0.70


@dataclass(frozen=True)
class Grade:
    """One pencil grade. See the module docstring for what each number holds."""

    name: str
    ceiling: float
    rate: float
    gamma: float
    bite: float
    bite_gain: float
    width: float
    width_floor: float

    def strength(self, pressure: float) -> float:
        """How dark a dab at ``pressure`` is asked to be, before the tooth has its say."""
        return float(max(pressure, 0.0)) ** self.gamma

    def bite_at(self, pressure: float, tip: str = "point") -> float:
        """How far into the tooth the lead reaches at ``pressure``, ``0..1``."""
        reach = self.bite + self.bite_gain * float(pressure)
        if tip == "side":
            reach -= SIDE_BITE
        return min(max(reach, 0.0), 1.0)

    def rate_for(self, tip: str = "point") -> float:
        return self.rate * (SIDE_RATE if tip == "side" else 1.0)


#: The box of pencils, hardest first. Written as the invariants the module docstring
#: names; the values are the spec's starting table moved by what the sampler showed.
GRADES: dict[str, Grade] = {
    "4H": Grade("4H", ceiling=0.35, rate=1.6, gamma=1.6, bite=0.00, bite_gain=0.55,
                width=0.0020, width_floor=0.80),
    "2H": Grade("2H", ceiling=0.45, rate=1.9, gamma=1.4, bite=0.06, bite_gain=0.60,
                width=0.0022, width_floor=0.70),
    "HB": Grade("HB", ceiling=0.60, rate=2.3, gamma=1.2, bite=0.15, bite_gain=0.65,
                width=0.0026, width_floor=0.55),
    "2B": Grade("2B", ceiling=0.78, rate=2.7, gamma=1.0, bite=0.26, bite_gain=0.66,
                width=0.0034, width_floor=0.45),
    "4B": Grade("4B", ceiling=0.88, rate=3.1, gamma=0.9, bite=0.36, bite_gain=0.62,
                width=0.0046, width_floor=0.40),
    "6B": Grade("6B", ceiling=0.96, rate=3.6, gamma=0.8, bite=0.46, bite_gain=0.54,
                width=0.0060, width_floor=0.35),
}


def get_grade(grade: str | Grade) -> Grade:
    """Look a grade up by name, the way a painter names it: ``"2b"`` is ``2B``."""
    if isinstance(grade, Grade):
        return grade
    key = str(grade).strip().upper()
    if key not in GRADES:
        raise ValueError(
            f"Unknown grade {grade!r}. The box holds {', '.join(GRADES)}, hardest first."
        )
    return GRADES[key]


def tip_brush(grade: Grade, tip: str, width: float | None = None) -> Brush:
    """The carrier :class:`~easel.brush.Brush` a graphite mark walks the path with.

    A pencil is not a brush, but the stroke machinery -- :func:`easel.stroke._dabs`'s
    spacing along travel, :func:`easel.brush.tip_mask`'s rotated and cached stamps, the
    box a mark can reach before it is laid -- is asked questions in terms of one, so a
    grade and a tip are written as the brush that answers them. ``point`` is a hard
    round tip at the grade's line width; ``side`` is the ``flat`` geometry at
    :data:`SIDE_WIDTH`, following the stroke's direction. Nothing about paint on it is
    read: load, wetness, opacity and the rest are never consulted.
    """
    if tip not in GRAPHITE_TIPS:
        raise ValueError(
            f"Unknown tip {tip!r}. A pencil meets the paper with its "
            f"{' or its '.join(GRAPHITE_TIPS)}."
        )
    if tip == "point":
        return Brush(name=grade.name, tip="round_hard",
                     size=float(width if width is not None else grade.width),
                     hardness=0.75, spacing=0.25, jitter=0.0, size_jitter=0.0,
                     angle_follow=False)
    # Spaced close: a graphite stroke accumulates as a maximum, and the maximum of
    # two overlapping ramps dips between their centres by the spacing's share of the
    # ramp -- at the flat brush's 0.12 that printed as stripes across the mark.
    return Brush(name=grade.name, tip="flat",
                 size=float(width if width is not None else SIDE_WIDTH),
                 hardness=0.55, spacing=0.04, jitter=0.0, size_jitter=0.0,
                 angle_follow=True, aspect=SIDE_ASPECT)
