from components.unit_color import UnitColor, Color
from components.unit_fill import UnitFill, Fill
from components.unit_outline_color import UnitOutlineColor, OutlineColor
from components.unit_shape import UnitShape, Shape
from components.unit import Unit
from components.level import Level


def get_level() -> Level:
    units = [
        # Группа: синие круги
        Unit(
            shape=UnitShape(Shape.CIRCLE),
            color=UnitColor(Color.BLUE),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        Unit(
            shape=UnitShape(Shape.CIRCLE),
            color=UnitColor(Color.BLUE),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        # Группа: зелёные квадраты
        Unit(
            shape=UnitShape(Shape.SQUARE),
            color=UnitColor(Color.GREEN),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        Unit(
            shape=UnitShape(Shape.SQUARE),
            color=UnitColor(Color.GREEN),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        Unit(
            shape=UnitShape(Shape.SQUARE),
            color=UnitColor(Color.GREEN),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        # Группа: жёлтые треугольники
        Unit(
            shape=UnitShape(Shape.TRIANGLE),
            color=UnitColor(Color.YELLOW),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        Unit(
            shape=UnitShape(Shape.TRIANGLE),
            color=UnitColor(Color.YELLOW),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        # Пара ловушек: разношёрстные юниты, портящие группы
        Unit(
            shape=UnitShape(Shape.SQUARE),
            color=UnitColor(Color.RED),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        Unit(
            shape=UnitShape(Shape.STAR),
            color=UnitColor(Color.VIOLET),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        # Одиночки: можно перетащить в другие группы
        Unit(
            shape=UnitShape(Shape.CIRCLE),
            color=UnitColor(Color.BLUE),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        Unit(
            shape=UnitShape(Shape.TRIANGLE),
            color=UnitColor(Color.YELLOW),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
        ),
        Unit(
            shape=UnitShape(Shape.SQUARE),
            color=UnitColor(Color.GREEN),
            fill=UnitFill(Fill.PLAIN, income=0.0),
            outline_color=UnitOutlineColor(OutlineColor.DARK_GRAY, income=0.0),
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
