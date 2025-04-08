from components.unit_similarity_trait import UnitSimilarityTrait
from enum import Enum


class Shape(Enum):
    CIRCLE = "circle"
    SQUARE = "square"
    TRIANGLE = "triangle"
    STAR = "star"


class UnitShape(UnitSimilarityTrait):
    value: Shape

    def __init__(self, value: Shape, income: float = None):
        self.value = value
        if income:
            self.income = income

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"
