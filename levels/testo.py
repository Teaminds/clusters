from components.unit_color import UnitColor, Color
from components.unit_fill import UnitFill, Fill
from components.unit_outline_color import UnitOutlineColor, OutlineColor
from components.unit_shape import UnitShape, Shape
from components.unit import Unit
from components.level import Level
from components.unit_similarity_trait import UnitSimilarityTrait


def get_level() -> Level:

    return Level(
        level_number=0,
        units=[
            Unit(
                shape=UnitSimilarityTrait(0),
                color=UnitSimilarityTrait(0),
                fill=UnitSimilarityTrait(0),
                outline=UnitSimilarityTrait(0),
                outline_color=UnitSimilarityTrait(0),
                x=100,
                y=100,
            )
        ],
        timer=60,
        goal=40,
        level_name="Test Level",
        level_description="This is a test level for the game.",
    )
