from components.unit_similarity_trait import UnitSimilarityTrait
from enum import Enum


class Color(Enum):
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"
    VIOLET = "violet"


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

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"
