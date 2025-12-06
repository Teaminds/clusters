from turtle import st


class TraitsOptionsRange:
    """
    Класс для управления захардкоженными вариантами черт.
    Все методы статические.
    """

    hardcoded_options = {
        "trait_a": {
            "0": {"income": 1.0, "value": "0"},
            "1": {"income": 1.0, "value": "1"},
            "2": {"income": 1.0, "value": "2"},
            "3": {"income": 1.0, "value": "3"},
            "4": {"income": 1.0, "value": "4"},
        },
        "trait_b": {
            "0": {"income": 1.0, "value": "0"},
            "1": {"income": 1.0, "value": "1"},
            "2": {"income": 1.0, "value": "2"},
            "3": {"income": 1.0, "value": "3"},
            "4": {"income": 1.0, "value": "4"},
        },
        "trait_c": {
            "0": {"income": 1.0, "value": "0"},
            "1": {"income": 1.0, "value": "1"},
            "2": {"income": 1.0, "value": "2"},
            "3": {"income": 1.0, "value": "3"},
            "4": {"income": 1.0, "value": "4"},
        },
        "trait_d": {
            "0": {"income": 1.0, "value": "0"},
            "1": {"income": 1.0, "value": "1"},
            "2": {"income": 1.0, "value": "2"},
            "3": {"income": 1.0, "value": "3"},
            "4": {"income": 1.0, "value": "4"},
        },
        "trait_e": {
            "0": {"income": 1.0, "value": "0"},
            "1": {"income": 1.0, "value": "1"},
            "2": {"income": 1.0, "value": "2"},
            "3": {"income": 1.0, "value": "3"},
            "4": {"income": 1.0, "value": "4"},
        },
    }

    @staticmethod
    def get_hardcoded_options():
        """Возвращает захардкоженные варианты черт."""

        return TraitsOptionsRange.hardcoded_options

    @staticmethod
    def get_traits_keys() -> list[str]:
        """Возвращает список ключей захардкоженных черт."""
        return list(TraitsOptionsRange.hardcoded_options.keys())

    @staticmethod
    def get_trait_options(trait_name: str) -> dict:
        """Возвращает варианты для заданной захардкоженной черты."""
        return TraitsOptionsRange.hardcoded_options.get(trait_name, {})

    @staticmethod
    def get_trait_values(trait_name: str) -> list:
        """Возвращает список значений для заданной захардкоженной черты."""
        options = TraitsOptionsRange.get_trait_options(trait_name)
        return list(options.keys())

    @staticmethod
    def get_trait_income(trait_name: str, value: str) -> float:
        """Возвращает доход для заданной захардкоженной черты и её значения."""
        options = TraitsOptionsRange.get_trait_options(trait_name)
        option = options.get(value, {})
        return option.get("income", 0.0)
