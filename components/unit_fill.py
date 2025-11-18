from components.unit_similarity_trait import UnitSimilarityTrait
from enum import Enum


class Fill(Enum):
    PLAIN = 0
    STRIPED = 1
    CHECKERED = 2
    WAVED = 3
    DOTTED = 4


class UnitFill(UnitSimilarityTrait):
    value: Fill

    def __init__(self, value: Fill, income: float = None):
        self.value = value
        if income:
            self.income = income
