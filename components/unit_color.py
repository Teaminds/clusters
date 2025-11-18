from components.unit_similarity_trait import UnitSimilarityTrait
from enum import Enum


class Color(Enum):
    BLUE = 0
    GREEN = 1
    RED = 2
    YELLOW = 3
    VIOLET = 4


class UnitColor(UnitSimilarityTrait):
    value: Color
    rgb: tuple[int, int, int] = None

    def __init__(self, value: Color, income: float = None):
        self.value = value
        if income:
            self.income = income
        if value == Color.BLUE:
            self.rgb = (0, 0, 255)
        elif value == Color.GREEN:
            self.rgb = (0, 255, 0)
        elif value == Color.RED:
            self.rgb = (255, 0, 0)
        elif value == Color.YELLOW:
            self.rgb = (255, 255, 0)
        elif value == Color.VIOLET:
            self.rgb = (238, 130, 238)
        else:
            raise ValueError(f"Unknown color: {value}")
