from typing import Literal, Any
from system_components.Core_Builded import core


class UnitSimilarityTrait:
    hardcoded_options = {
        "trait_a": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
        "trait_b": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
        "trait_c": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
        "trait_d": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
        "trait_e": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
    }

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

    @staticmethod
    def get_traits_keys() -> list[str]:
        return list(UnitSimilarityTrait.hardcoded_options.keys())

    @staticmethod
    def get_hardcoded_traits_options() -> dict[str, list[Any]]:
        return UnitSimilarityTrait.hardcoded_options

    @staticmethod
    def get_hardcoded_options_by_trait_name(trait_name: str) -> list[Any]:
        return UnitSimilarityTrait.hardcoded_options[trait_name]

    @staticmethod
    def get_hardcoded_option_by_trait_name_and_value(
        trait_name: str, value: Any
    ) -> Any:
        options = UnitSimilarityTrait.hardcoded_options[trait_name]
        for option in options:
            if option == value:
                return options[option]
        raise ValueError(f"Unknown value {value} for trait {trait_name}")

    def __repr__(self) -> str:
        return f"{self.name}: {self.value} (income: {self.income})"
