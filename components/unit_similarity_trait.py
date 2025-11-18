import random
from typing import Literal, Any


class UnitSimilarityTrait:
    options: list[int] = []
    income: float = 1.0
    value: any = None

    def __init__(
        self,
        # options: list[int] = [],
        income: float = 1.0,
        value: any = None,
    ):
        self.value = value or random.choice([1, 2, 3, 4, 5])
        self.income = income

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.value}"
