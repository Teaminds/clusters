from components.unit_similarity_trait import UnitSimilarityTrait
from enum import Enum


class Shape(Enum):
    CIRCLE = 0
    SQUARE = 1
    TRIANGLE = 2
    STAR = 3


class UnitShape(UnitSimilarityTrait):
    value: Shape

    def __init__(self, value: Shape, income: float = None):
        self.value = value
        if income:
            self.income = income
