from components.unit_color import UnitColor, Color
from components.unit_fill import UnitFill, Fill

# from components.unit_outline import UnitOutline, Outline
from components.unit_outline_color import UnitOutlineColor, OutlineColor
from components.unit_shape import UnitShape, Shape
from components.unit import Unit
from components.level import Level


def get_level() -> Level:
    units = [
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
        Unit(),
    ]

    return Level(
        level_number=1,
        units=units,
        timer=600,
        goal=1000,
        level_name="Святой рандом",
        level_description="Объединяй юниты, чтобы получить больше юнитов.",
    )
