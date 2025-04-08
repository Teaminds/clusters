from components.unit_similarity_trait import UnitSimilarityTrait
from enum import Enum


class Outline(Enum):
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"
    DOUBLE = "double"
    GROOVE = "groove"


class UnitOutline(UnitSimilarityTrait):
    value: Outline

    def __init__(self, value: Outline, income: float = None):
        self.value = value
        if income:
            self.income = income

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"
