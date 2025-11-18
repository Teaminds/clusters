from components.unit_similarity_trait import UnitSimilarityTrait
from enum import Enum


class Outline(Enum):
    SOLID = 0
    DASHED = 1
    DOTTED = 2
    RARE = 3
    SUPER_RARE = 4


class UnitOutline(UnitSimilarityTrait):
    value: Outline

    def __init__(self, value: Outline, income: float = None):
        self.value = value
        if income:
            self.income = income
