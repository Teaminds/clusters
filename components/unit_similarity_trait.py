from typing import Any
from system_components.Core_Builded import core


class UnitSimilarityTrait:

    name: str
    income: float
    value: Any
    uid: str

    def __init__(
        self,
        name: str,
        income: float,
        value: Any,
    ):
        self.name = name
        self.value = value
        self.income = income
        self.uid = core.utils().uid()
        core.registry().register(self)

    def get_uid(self) -> str:
        return self.uid

    def get_name(self) -> str:
        return self.name

    def get_value(self) -> Any:
        return self.value

    def get_income(self) -> float:
        return self.income

    def __repr__(self) -> str:
        return f"{self.name}: {self.value} (income: {self.income})"
