from __future__ import annotations
from system_components.Core_Builded import core
from components.level import Level
from components.traits_options_range import TraitsOptionsRange
from typing import TYPE_CHECKING, Any, Optional
from components.unit import Unit
from components.unit_similarity_trait import UnitSimilarityTrait
from random import choice, uniform


class LevelFactory:
    """
    Фабрика уровней из конфигурационных данных. Предоставляет методы для:
    - Проверки валидности конфигурации уровня и юнитов
    - Подготовки конфигурации уровня и юнитов (установка значений по умолчанию)
    - Создания уровней и юнитов из подготовленных конфигураций

    В будущем с добавлении schema.json для уровней можно переписать на схему.

    Все методы статические, так как фабрика не хранит состояние.
    """

    @staticmethod
    def _check_level_config(level_config: dict) -> bool:
        """Проверяет валидность конфигурации уровня."""
        available_keys = [
            "name",
            "description",
            "level_number",
            "act_number",
            "units",
            "timer",
            "goal_score",
            "default_traits_pool",
            "income",
            "starting_score",
        ]
        trait_keys = TraitsOptionsRange.get_traits_keys()

        if not isinstance(level_config, dict):
            raise ValueError("Level config must be a dictionary")

        if not set(level_config.keys()).issubset(set(available_keys)):
            raise ValueError("Config contains invalid keys")

        if "name" not in level_config:
            raise ValueError("Level config must contain 'name' key")
        elif not isinstance(level_config["name"], str):
            raise ValueError("'name' must be a string")

        if "description" in level_config:
            if not isinstance(level_config["description"], str):
                raise ValueError("'description' must be a string")

        if "level_number" not in level_config:
            raise ValueError("Level config must contain 'level_number' key")
        elif not isinstance(level_config["level_number"], int):
            raise ValueError("'level_number' must be an integer")

        if "act_number" not in level_config:
            raise ValueError("Level config must contain 'act_number' key")
        elif not isinstance(level_config["act_number"], int):
            raise ValueError("'act_number' must be an integer")

        if "units" not in level_config:
            raise ValueError("Level config must contain 'units' key")
        elif not isinstance(level_config["units"], list):
            raise ValueError("'units' must be a list")
        elif len(level_config["units"]) == 0:
            raise ValueError("'units' list must contain at least one unit config")
        for unit_cfg in level_config["units"]:
            if not isinstance(unit_cfg, dict):
                raise ValueError("Each unit config must be a dictionary")

        if "goal_score" not in level_config:
            raise ValueError("Level config must contain 'goal_score' key")
        elif not isinstance(level_config["goal_score"], int):
            raise ValueError("'goal_score' must be an integer")

        if "timer" in level_config:
            if not isinstance(level_config["timer"], (int, float)):
                raise ValueError("'timer' must be an integer or float")
        if "default_traits_pool" in level_config:
            if not isinstance(level_config["default_traits_pool"], dict):
                raise ValueError("'default_traits_pool' must be a dictionary")
            if not set(level_config["default_traits_pool"].keys()).issubset(
                set(trait_keys)
            ):
                raise ValueError("'default_traits_pool' contains invalid keys")
            for trait_name, options in level_config["default_traits_pool"].items():
                if trait_name not in trait_keys:
                    raise ValueError(f"Invalid trait name: {trait_name}")
                if not (isinstance(options, dict)):
                    raise ValueError(
                        f"'default_traits_pool' for trait {trait_name} must be a dictionary"
                    )
                for value, option_data in options.items():
                    if not isinstance(value, str):
                        raise ValueError(
                            f"Trait value for trait '{trait_name}' must be a string"
                        )
                    for option_key, option_value in option_data.items():
                        if option_key not in ["value", "income"]:
                            raise ValueError(
                                f"Invalid option key '{option_key}' for trait '{trait_name}'"
                            )
                        if option_key == "value":
                            if not isinstance(option_value, int):
                                raise ValueError(
                                    f"'value' for trait '{trait_name}' must be an integer"
                                )
                        if option_key == "income":
                            if not isinstance(option_value, (int, float)):
                                raise ValueError(
                                    f"'income' for trait '{trait_name}' must be a number"
                                )

        if "income" in level_config:
            if not isinstance(level_config["income"], (int, float)):
                raise ValueError("'income' must be a number")

        if "starting_score" in level_config:
            if not isinstance(level_config["starting_score"], (int, float)):
                raise ValueError("'starting_score' must be a number")

        return True

    @staticmethod
    def _prepare_level_config(
        level_config: dict[str, Any],
    ) -> dict[str, Any]:
        """Подготавливает конфигурацию уровня, устанавливая значения по умолчанию и проверяя трейты."""
        prepared_config = level_config.copy()
        trait_keys = TraitsOptionsRange.get_traits_keys()
        prepared_config.setdefault("description", "")
        prepared_config.setdefault("timer", float("+inf"))
        if prepared_config["timer"] is None or prepared_config["timer"] == 0:
            prepared_config["timer"] = float("+inf")
        prepared_config.setdefault("income", 0.0)
        prepared_config.setdefault("starting_score", 0.0)

        if "default_traits_pool" not in prepared_config:
            prepared_config.setdefault(
                "default_traits_pool",
                TraitsOptionsRange.get_hardcoded_options(),
            )
        else:  # TODO: что-то не так с подсчетом дефолтных трейтов
            for trait_name in trait_keys:
                if trait_name not in prepared_config["default_traits_pool"]:
                    prepared_config["default_traits_pool"][trait_name] = (
                        TraitsOptionsRange.get_trait_options(trait_name)
                    )
                else:
                    for trait_value in prepared_config["default_traits_pool"][
                        trait_name
                    ]:
                        if (
                            "income"
                            not in prepared_config["default_traits_pool"][trait_name][
                                trait_value
                            ]
                        ):
                            prepared_config["default_traits_pool"][trait_name][
                                trait_value
                            ]["income"] = TraitsOptionsRange.get_trait_income(
                                trait_name=trait_name, value=trait_value
                            )
                        if (
                            "value"
                            not in prepared_config["default_traits_pool"][trait_name][
                                trait_value
                            ]
                        ):
                            prepared_config["default_traits_pool"][trait_name][
                                trait_value
                            ]["value"] = trait_value
        prepared_units_configs = []
        for unit_cfg in prepared_config["units"]:
            if LevelFactory._check_unit_config(
                unit_config=unit_cfg,
                trait_options=prepared_config["default_traits_pool"],
                level_timer=prepared_config["timer"],
            ):
                prepared_units_configs.append(
                    LevelFactory._prepare_unit_config(
                        unit_config=unit_cfg,
                        level_timer=prepared_config["timer"],
                        trait_options=prepared_config["default_traits_pool"],
                    )
                )
        prepared_config["units"] = prepared_units_configs
        return prepared_config

    @staticmethod
    def _create_level_from_prepared_config(
        prepared_level_config: dict[str, Any], units: list[Unit]
    ) -> Level:
        """Создаёт уровень из подготовленной конфигурации и списка юнитов."""
        lev = Level(
            level_number=prepared_level_config["level_number"],
            level_act_number=prepared_level_config["act_number"],
            units=units,
            timer=prepared_level_config["timer"],
            goal=prepared_level_config["goal_score"],
            name=prepared_level_config["name"],
            description=prepared_level_config["description"],
            income=prepared_level_config["income"],
            score=prepared_level_config["starting_score"],
        )
        return lev

    @staticmethod
    def create_level_from_config(level_config: dict[str, Any]) -> Level:
        """Создаёт уровень из конфигурации, проверяя и подготавливая её."""
        if LevelFactory._check_level_config(level_config):
            prepared_level_config = LevelFactory._prepare_level_config(level_config)
            units = LevelFactory._create_many_units_from_list_of_configs(
                prepared_level_config["units"],
                prepared_level_config["default_traits_pool"],
                prepared_level_config["timer"],
            )
            level = LevelFactory._create_level_from_prepared_config(
                prepared_level_config, units
            )
            return level
        else:
            raise ValueError("Invalid level config")

    @staticmethod
    def _check_unit_config(
        unit_config: dict[str, Any],
        trait_options: dict[str, list[int]],
        level_timer: float | int,
    ) -> bool:
        """Проверяет валидность конфигурации юнита."""
        trait_keys = TraitsOptionsRange.get_traits_keys()

        available_keys = [
            "traits",
            "draggedable",
            "income_time",
            "life_time",
            "x",
            "y",
            "body_radius",
            "aura_radius",
        ]
        available_keys.extend(trait_keys)

        if not isinstance(unit_config, dict):
            raise ValueError("Unit config must be a dictionary")

        if not set(unit_config.keys()).issubset(set(available_keys)):
            raise ValueError("Config contains invalid keys")

        if "traits" in unit_config:  # НАДО ПОЧИНИТЬ
            for trait in unit_config["traits"].keys():
                if trait not in trait_keys:
                    raise ValueError(f"Invalid trait key: {trait}")
                if trait not in TraitsOptionsRange.get_traits_keys():
                    raise ValueError(f"invalid trait key (hardcoded): {trait}")
                if not isinstance(unit_config["traits"][trait], dict):
                    raise ValueError(f"Trait '{trait}' must be a dictionary")
                if trait not in trait_options:
                    raise ValueError(f"Trait options for '{trait}' not provided")
                for trait_element in unit_config["traits"][trait].keys():
                    if trait_element not in ["value", "income"]:
                        raise ValueError(
                            f"Trait '{trait}' contains invalid key: {trait_element}"
                        )
                test_value = unit_config["traits"][trait].get("value")
                if test_value is not None:
                    if not isinstance(test_value, str):
                        raise ValueError(f"Trait '{trait}' value must be an string")
                    if test_value not in trait_options[trait]:
                        raise ValueError(
                            f"Trait '{trait}' value '{test_value}' not in options {trait_options[trait]}"
                        )
                    if test_value not in TraitsOptionsRange.get_trait_options(trait):
                        raise ValueError(
                            f"Trait '{trait}' value '{test_value}' not in hardcoded options {TraitsOptionsRange.get_trait_options(trait)}"
                        )
                test_income = unit_config["traits"][trait].get("income")
                if test_income is not None:
                    if not isinstance(test_income, (int, float)):
                        raise ValueError(f"Trait '{trait}' income must be a number")
        if "draggedable" in unit_config:
            if not isinstance(unit_config["draggedable"], bool):
                raise ValueError("'draggedable' must be a boolean")

        if "income_time" in unit_config:
            if not isinstance(unit_config["income_time"], (int, float)):
                raise ValueError("'income_time' must be a number")
            if (
                unit_config["income_time"] < 0
                or unit_config["income_time"] > level_timer
            ):
                raise ValueError("'income_time' must be between 0 and level_timer")

        if "life_time" in unit_config:
            if not isinstance(unit_config["life_time"], (int, float)):
                raise ValueError("'life_time' must be a number")
            if unit_config["life_time"] < 0:
                raise ValueError("'life_time' must be between 0 and infinity")

        if "x" in unit_config:
            if not isinstance(unit_config["x"], (int, float)):
                raise ValueError("'x' must be a number")
            if unit_config["x"] < 0 or unit_config["x"] > 1280:
                raise ValueError(f"'x' must be between 0 and 1")

        if "y" in unit_config:
            if not isinstance(unit_config["y"], (int, float)):
                raise ValueError("'y' must be a number")
            if unit_config["y"] < 0 or unit_config["y"] > 720:
                raise ValueError(f"'y' must be between 0 and 1")

        if "body_radius" in unit_config:
            if not isinstance(unit_config["body_radius"], (int, float)):
                raise ValueError("'body_radius' must be a number")
            if unit_config["body_radius"] <= 0:
                raise ValueError("'body_radius' must be greater than 0")

        if "aura_radius" in unit_config:
            if not isinstance(unit_config["aura_radius"], (int, float)):
                raise ValueError("'aura_radius' must be a number")
            if unit_config["aura_radius"] < 0 or unit_config["aura_radius"] > 1280:
                raise ValueError("'aura_radius' must be between 0 and 1280")
            if "body_radius" not in unit_config:
                raise ValueError(
                    "'body_radius' must be defined if 'aura_radius' is defined"
                )
            if unit_config["aura_radius"] < unit_config["body_radius"]:
                raise ValueError("'aura_radius' must be greater than 'body_radius'")

        return True

    @staticmethod
    def _prepare_unit_config(
        unit_config: dict[str, Any],
        level_timer: float | int,
        trait_options: Optional[dict[str, list[int]]] = {},
    ) -> dict[str, Any]:
        """Подготавливает конфигурацию юнита, устанавливая значения по умолчанию."""
        prepared_config = unit_config.copy()
        if "traits" not in prepared_config:
            prepared_config["traits"] = {}
        trait_keys = TraitsOptionsRange.get_traits_keys()
        for trait_key in trait_keys:
            if trait_key not in prepared_config["traits"]:
                if trait_key in trait_options:
                    keys = list(trait_options[trait_key].keys())
                    option_value = choice(keys)
                    option = trait_options[trait_key][option_value]
                    option["value"] = option_value
                prepared_config["traits"][trait_key] = option
            else:
                value = choice(list(trait_options[trait_key].keys()))
                income = trait_options[trait_key][value]["income"]
                if "value" not in prepared_config["traits"][trait_key]:
                    prepared_config["traits"][trait_key]["value"] = value
                if "income" not in prepared_config["traits"][trait_key]:
                    prepared_config["traits"][trait_key]["income"] = income

        if "draggedable" not in prepared_config:
            prepared_config["draggedable"] = choice([True, False])
        if "income_time" not in prepared_config:
            immediate_income_time = choice([True, False])
            if immediate_income_time:
                prepared_config["income_time"] = 0
            else:
                prepared_config["income_time"] = uniform(0, level_timer)
        if "life_time" not in prepared_config:
            endless_life_time = choice([True, False])
            if endless_life_time:
                prepared_config["life_time"] = float("+inf")
            else:
                prepared_config["life_time"] = uniform(0.01, level_timer * 2)
        if "life_time" == 0:
            prepared_config["life_time"] = float("+inf")
        if "x" not in prepared_config:
            prepared_config["x"] = uniform(0, 1280)
        if "y" not in prepared_config:
            prepared_config["y"] = uniform(0, 720)
        if "body_radius" not in prepared_config:
            prepared_config["body_radius"] = float(30)
        if "aura_radius" not in prepared_config:
            prepared_config["aura_radius"] = prepared_config["body_radius"] * 1.4

        return prepared_config

    @staticmethod
    def _create_one_unit_from_prepared_unit_config(
        prepared_unit_config: dict[str, Any],
    ) -> Unit:
        """Создаёт юнит из подготовленной конфигурации."""
        unit_traits: dict[str, UnitSimilarityTrait] = {}
        for trait_name, trait_body in prepared_unit_config["traits"].items():
            unit_traits[trait_name] = UnitSimilarityTrait(
                name=trait_name,
                income=trait_body["income"],
                value=trait_body["value"],
            )
        return Unit(
            traits=unit_traits,
            x=prepared_unit_config["x"],
            y=prepared_unit_config["y"],
            income_time=prepared_unit_config["income_time"],
            life_time=prepared_unit_config["life_time"],
            draggedable=prepared_unit_config["draggedable"],
            body_radius=prepared_unit_config["body_radius"],
            aura_radius=prepared_unit_config["aura_radius"],
        )

    @staticmethod
    def _create_many_units_from_list_of_configs(
        list_of_units_configs: list[dict[str, Any]],
        trait_options: dict[str, list[int]],
        level_timer: float | int,
    ) -> list[Unit]:
        """Создаёт множество юнитов из списка конфигураций юнитов."""
        units: list[Unit] = []
        for unit_config in list_of_units_configs:
            if LevelFactory._check_unit_config(unit_config, trait_options, level_timer):
                prepared_unit_config = LevelFactory._prepare_unit_config(
                    unit_config, level_timer, trait_options
                )
                unit = LevelFactory._create_one_unit_from_prepared_unit_config(
                    prepared_unit_config
                )
                units.append(unit)
            else:
                raise ValueError("Invalid unit config")

        return units
