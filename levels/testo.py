from components.unit_color import UnitColor, Color
from components.unit_fill import UnitFill, Fill
from components.unit_outline_color import UnitOutlineColor, OutlineColor
from components.unit_shape import UnitShape, Shape
from components.unit import Unit
from components.level import Level


def get_level() -> Level:

    return Level(
        level_number=0,
        units=[
            Unit(
                shape=UnitShape(Shape.CIRCLE),
                color=UnitColor(Color.BLUE),
                fill=UnitFill(Fill.PLAIN),
                outline_color=UnitColor(OutlineColor.DARK_GRAY),
                x=100,
                y=100,
            ),
            Unit(
                shape=UnitShape(Shape.SQUARE),
                color=UnitColor(Color.BLUE),
                fill=UnitFill(Fill.PLAIN),
                outline_color=UnitColor(OutlineColor.DARK_GRAY),
                x=200,
                y=100,
            ),
            Unit(
                shape=UnitShape(Shape.TRIANGLE),
                color=UnitColor(Color.BLUE),
                fill=UnitFill(Fill.PLAIN),
                outline_color=UnitColor(OutlineColor.DARK_GRAY),
                x=300,
                y=100,
            ),
            Unit(
                shape=UnitShape(Shape.TRIANGLE),
                color=UnitColor(Color.RED),
                fill=UnitFill(Fill.PLAIN),
                outline_color=UnitColor(OutlineColor.DARK_GRAY),
                x=200,
                y=200,
            ),
        ],
        timer=60,
        goal=40,
        level_name="Test Level",
        level_description="This is a test level for the game.",
    )
