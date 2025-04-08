from components.unit_similarity_trait import UnitSimilarityTrait
from enum import Enum


class Fill(Enum):
    PLAIN = "plain"
    STRIPED = "striped"
    CHECKERED = "checkered"
    WAVED = "waved"
    DOTTED = "dotted"


class UnitFill(UnitSimilarityTrait):
    value = Fill

    def __init__(self, value: Fill, income: float = None):
        self.value = value
        if income:
            self.income = income

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"
