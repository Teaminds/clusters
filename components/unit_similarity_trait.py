import random


class UnitSimilarityTrait:
    income: float = 1.0
    value: int = 0

    def __init__(self, value: int, income: float = 1.0):
        self.value = value
        self.income = income or random.randint(0, 4)
