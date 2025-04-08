from components.unit_color import UnitColor, Color
from components.unit_fill import UnitFill, Fill
from components.unit_outline import UnitOutline, Outline
from components.unit_shape import UnitShape, Shape
from components.unit import Unit
from components.level import Level


def get_level() -> Level:
    units = [
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
        Unit(
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline=UnitOutline(Outline.SOLID, income=0.0),
        ),
    ]

    return Level(
        level_number=1,
        units=units,
        timer=600,
        goal=1000,
        level_name="Форма и Цвет",
        level_description="Объединяй по форме и цвету. Осторожно с ловушками!",
    )
