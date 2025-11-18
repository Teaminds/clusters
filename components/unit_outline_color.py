from enum import Enum
from components.unit_similarity_trait import UnitSimilarityTrait


class OutlineColor(Enum):
    DARK_BLUE = 0
    DARK_GREEN = 1
    DARK_RED = 2
    DARK_YELLOW = 3
    DARK_VIOLET = 4
    # DARK_GRAY = 5


class UnitOutlineColor(UnitSimilarityTrait):
    value: OutlineColor
    rgb: tuple[int, int, int] = None

    def __init__(self, value: OutlineColor, income: float = None):
        self.value = value
        if income:
            self.income = income
        if value == OutlineColor.DARK_BLUE:
            self.rgb = (0, 0, 205)
        elif value == OutlineColor.DARK_GREEN:
            self.rgb = (0, 205, 0)
        elif value == OutlineColor.DARK_RED:
            self.rgb = (205, 0, 0)
        elif value == OutlineColor.DARK_YELLOW:
            self.rgb = (205, 205, 0)
        elif value == OutlineColor.DARK_VIOLET:
            self.rgb = (188, 80, 188)
        elif value == OutlineColor.DARK_GRAY:
            self.rgb = (169, 169, 169)
        else:
            raise ValueError(f"Unknown outline color: {value}")
