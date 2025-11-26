from __future__ import annotations

from components.unit import Unit
from components.unit_similarity_trait import UnitSimilarityTrait
from random import choice, randint, random, uniform
from typing import TYPE_CHECKING, Literal, Any, Optional, Union

if TYPE_CHECKING:
    from components.level import Level


standart = {
    "name": "standart Level",
    "description": "This is a test level",
    "units": [
        {
            "traits": {
                "trait_a": {"value": 4, "income": 1.0},
                "trait_b": {"value": 4, "income": 2.0},
                "trait_c": {"value": 4, "income": 3.0},
                "trait_d": {"value": 4, "income": 4.0},
                "trait_e": {"value": 4, "income": 5.0},
            },
            "draggedable": True,
            "income_time": 0,
            "life_time": 0,
            "x": 0.5,
            "y": 0.5,
            "body_radius": 0.005,
            "aura_radius": 0.007,
        }
    ],
    "timer": 300,
    "goal_score": 100,
    "default_traits_pool": {
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
    },
}

lite = {
    "name": "lite Level",
    "units": [{}],
    "goal_score": 100,
}

level_config = {
    "name": "Complicated Level",
    "description": "This is a test level",
    "units": [
        {
            "traits": {
                "trait_a": {},
                "trait_b": {"value": 4},
                "trait_c": {"income": 1.0},
                "trait_e": {"value": 4, "income": 1.0},
            },
            "draggedable": True,
            "income_time": 0,
            "life_time": 0,
            "x": 0.5,
            "y": 0.5,
            "body_radius": 0.005,
            "aura_radius": 0.007,
        }
    ],
    "timer": 300,
    "goal_score": 100,
    "default_traits_pool": {
        "trait_a": {
            0: {"income": 1.0},
            4: {},
        },
        "trait_b": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
    },
    "income": 0.0,
    "starting_score": 0.0,
}

unit_config = [
    {
        "traits": {
            "trait_a": {},
            "trait_b": {"value": 4},
            "trait_c": {"income": 1.0},
            "trait_e": {"value": 4, "income": 1.0},
        },
        "draggedable": True,
        "income_time": 0,
        "life_time": 0,
        "x": 0.5,
        "y": 0.5,
        "body_radius": 0.005,
        "aura_radius": 0.007,
    }
]


class UnitFactory:

    @staticmethod
    def check_unit_config(
        unit_config: dict[str, Any],
        trait_options: dict[str, list[int]],
        level_timer: Union[float, int],
    ) -> bool:
        trait_keys = UnitSimilarityTrait.get_traits_keys()

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
                if trait not in UnitSimilarityTrait.get_traits_keys():
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
                    if (
                        test_value
                        not in UnitSimilarityTrait.get_hardcoded_options_by_trait_name(
                            trait
                        )
                    ):
                        raise ValueError(
                            f"Trait '{trait}' value '{test_value}' not in hardcoded options {UnitSimilarityTrait.get_hardcoded_options_by_trait_name(trait)}"
                        )
                test_income = unit_config["traits"][trait].get("income")
                if test_income is not None:
                    if not isinstance(test_income, (int, float)):
                        raise ValueError(f"Trait '{trait}' income must be a number")

            # for trait_key in trait_keys:
            #     if trait_key in unit_config["traits"]:
            #         if (
            #             "value" in unit_config["traits"][trait_key]
            #             and unit_config["traits"][trait_key]["value"]
            #             not in trait_options[trait_key]
            #         ):
            #             raise ValueError(
            #                 f"'{trait_key}' value '{unit_config['traits'][trait_key]}' not in options '{trait_options[trait_key]}'"
            #             )
            #         if isinstance(unit_config["traits"][trait_key], int):
            #             trait = unit_config["traits"][trait_key]
            #         elif isinstance(unit_config["traits"][trait_key], dict):

            #             if unit_config["traits"][trait_key] != {}:
            #                 for key in unit_config["traits"][trait_key].keys():
            #                     if key not in ["value", "income"]:
            #                         raise ValueError(
            #                             f"'{trait_key}' dict must only contain 'value' and 'income' keys"
            #                         )
            #                 trait = unit_config["traits"][trait_key]["value"]
            #                 if not isinstance(
            #                     unit_config["traits"][trait_key]["income"], (int, float)
            #                 ):
            #                     raise ValueError(
            #                         f"'{trait_key}' income must be a integer or float"
            #                     )
            #                 if (
            #                     trait
            #                     not in UnitSimilarityTrait.get_hardcoded_options_by_trait_name(
            #                         trait_key
            #                     )
            #                 ):
            #                     raise ValueError(
            #                         f"'{trait_key}' value '{trait}' not in hardcoded options '{UnitSimilarityTrait.get_hardcoded_options_by_trait_name(trait_key)}'"
            #                     )
            #     else:
            #         raise ValueError(f"'{trait_key}' must be defined in 'traits'")

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
            if unit_config["x"] < 0 or unit_config["x"] > 1:
                raise ValueError(f"'x' must be between 0 and 1")

        if "y" in unit_config:
            if not isinstance(unit_config["y"], (int, float)):
                raise ValueError("'y' must be a number")
            if unit_config["y"] < 0 or unit_config["y"] > 1:
                raise ValueError(f"'y' must be between 0 and 1")

        if "body_radius" in unit_config:
            if not isinstance(unit_config["body_radius"], (int, float)):
                raise ValueError("'body_radius' must be a number")
            if unit_config["body_radius"] <= 0:
                raise ValueError("'body_radius' must be greater than 0")

        if "aura_radius" in unit_config:
            if not isinstance(unit_config["aura_radius"], (int, float)):
                raise ValueError("'aura_radius' must be a number")
            if unit_config["aura_radius"] < 0 or unit_config["aura_radius"] > 1:
                raise ValueError("'aura_radius' must be between 0 and 1")
            if "body_radius" not in unit_config:
                raise ValueError(
                    "'body_radius' must be defined if 'aura_radius' is defined"
                )
            if unit_config["aura_radius"] < unit_config["body_radius"]:
                raise ValueError("'aura_radius' must be greater than 'body_radius'")

        return True

    @staticmethod
    def prepare_unit_config(
        unit_config: dict[str, Any],
        level_timer: Union[float, int],
        trait_options: Optional[dict[str, list[int]]] = {},
    ) -> dict[str, Any]:
        prepared_config = unit_config.copy()
        if "traits" not in prepared_config:
            prepared_config["traits"] = {}
        trait_keys = UnitSimilarityTrait.get_traits_keys()
        for trait_key in trait_keys:
            if trait_key not in prepared_config["traits"]:
                if trait_key in trait_options:
                    keys = list(trait_options[trait_key].keys())
                    option_value = choice(keys)
                    option = trait_options[trait_key][option_value]
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
            prepared_config["income_time"] = uniform(0, level_timer)
        if "life_time" not in prepared_config:
            prepared_config["life_time"] = uniform(0, level_timer * 2)
        if "x" not in prepared_config:
            prepared_config["x"] = uniform(0, 1)
        if "y" not in prepared_config:
            prepared_config["y"] = uniform(0, 1)
        if "body_radius" not in prepared_config:
            prepared_config["body_radius"] = float(0.005)
        if "aura_radius" not in prepared_config:
            prepared_config["aura_radius"] = prepared_config["body_radius"] * 1.4

        return prepared_config

    @staticmethod
    def create_one_unit_from_prepared_unit_config(
        prepared_unit_config: dict[str, Any],
    ) -> Unit:
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
    def create_many_units_from_list_of_configs(
        list_of_units_configs: list[dict[str, Any]],
        trait_options: dict[str, list[int]],
        level_timer: Union[float, int],
    ) -> list[Unit]:
        units: list[Unit] = []
        for unit_config in list_of_units_configs:
            if UnitFactory.check_unit_config(unit_config, trait_options, level_timer):
                prepared_unit_config = UnitFactory.prepare_unit_config(
                    unit_config, level_timer, trait_options
                )
                unit = UnitFactory.create_one_unit_from_prepared_unit_config(
                    prepared_unit_config
                )
                units.append(unit)
            else:
                raise ValueError("Invalid unit config")

        return units
