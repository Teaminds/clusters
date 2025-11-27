from __future__ import annotations
from components.level import Level
from components.unit_factory import UnitFactory
from components.traits_options_range import TraitsOptionsRange
from typing import TYPE_CHECKING, Literal, Any, Optional, Union

if TYPE_CHECKING:
    from components.unit import Unit


# standart = {
#     "name": "standart Level",
#     "description": "This is a test level",
#     "number": 1,
#     "act_number": 1,
#     "units": [
#         {
#             "traits": {
#                 "trait_a": {"value": 4, "income": 1.0},
#                 "trait_b": {"value": 4, "income": 2.0},
#                 "trait_c": {"value": 4, "income": 3.0},
#                 "trait_d": {"value": 4, "income": 4.0},
#                 "trait_e": {"value": 4, "income": 5.0},
#             },
#             "draggedable": True,
#             "income_time": 0,
#             "life_time": 0,
#             "x": 0.5,
#             "y": 0.5,
#             "body_radius": 0.005,
#             "aura_radius": 0.007,
#         }
#     ],
#     "timer": 300,
#     "goal_score": 100,
#     "default_traits_pool": {
#         "trait_a": {
#             0: {"income": 1.0},
#             1: {"income": 1.0},
#             2: {"income": 1.0},
#             3: {"income": 1.0},
#             4: {"income": 1.0},
#         },
#         "trait_b": {
#             0: {"income": 1.0},
#             1: {"income": 1.0},
#             2: {"income": 1.0},
#             3: {"income": 1.0},
#             4: {"income": 1.0},
#         },
#         "trait_c": {
#             0: {"income": 1.0},
#             1: {"income": 1.0},
#             2: {"income": 1.0},
#             3: {"income": 1.0},
#             4: {"income": 1.0},
#         },
#         "trait_d": {
#             0: {"income": 1.0},
#             1: {"income": 1.0},
#             2: {"income": 1.0},
#             3: {"income": 1.0},
#             4: {"income": 1.0},
#         },
#         "trait_e": {
#             0: {"income": 1.0},
#             1: {"income": 1.0},
#             2: {"income": 1.0},
#             3: {"income": 1.0},
#             4: {"income": 1.0},
#         },
#     },
# }

# lite = {
#     "name": "lite Level",
#     "number": 1,
#     "act_number": 1,
#     "units": [{}],
#     "goal_score": 100,
# }

# level_config = {
#     "name": "Complicated Level",
#     "description": "This is a test level",
#     "number": 1,
#     "act_number": 1,
#     "units": [
#         {
#             "traits": {
#                 "trait_a": {},
#                 "trait_b": {"value": 4},
#                 "trait_c": {"income": 1.0},
#                 "trait_e": {"value": 4, "income": 1.0},
#             },
#             "draggedable": True,
#             "income_time": 0,
#             "life_time": 0,
#             "x": 0.5,
#             "y": 0.5,
#             "body_radius": 0.005,
#             "aura_radius": 0.007,
#         }
#     ],
#     "timer": 300,
#     "goal_score": 100,
#     "default_traits_pool": {
#         "trait_a": {
#             0: {"income": 1.0},
#             4: {},
#         },
#         "trait_c": {
#             0: {"income": 5.0},
#             4: {},
#         },
#         "trait_b": {
#             0: {"income": 1.0},
#             1: {"income": 1.0},
#             2: {"income": 1.0},
#             3: {"income": 1.0},
#             4: {"income": 1.0},
#         },
#     },
#     "income": 0.0,
#     "starting_score": 0.0,
# }

# unit_config = [
#     {
#         "traits": {
#             "trait_a": {},
#             "trait_b": {"value": 4},
#             "trait_c": {"income": 1.0},
#             "trait_e": {"value": 4, "income": 1.0},
#         },
#         "draggedable": True,
#         "income_time": 0,
#         "life_time": 0,
#         "x": 0.5,
#         "y": 0.5,
#         "body_radius": 0.005,
#         "aura_radius": 0.007,
#     }
# ]


class LevelFactory:

    @staticmethod
    def check_level_config(level_config: dict) -> bool:
        available_keys = [
            "name",
            "description",
            "number",
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

        if "number" not in level_config:
            raise ValueError("Level config must contain 'number' key")
        elif not isinstance(level_config["number"], int):
            raise ValueError("'number' must be an integer")

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
    def prepare_level_config(
        level_config: dict[str, Any],
    ) -> dict[str, Any]:
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
        else:
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
        prepared_units_configs = []
        for unit_cfg in prepared_config["units"]:
            if UnitFactory.check_unit_config(
                unit_config=unit_cfg,
                trait_options=prepared_config["default_traits_pool"],
                level_timer=prepared_config["timer"],
            ):
                prepared_units_configs.append(
                    UnitFactory.prepare_unit_config(
                        unit_config=unit_cfg,
                        level_timer=prepared_config["timer"],
                        trait_options=prepared_config["default_traits_pool"],
                    )
                )
        prepared_config["units"] = prepared_units_configs
        return prepared_config

        # if "default_traits_pool" not in prepared_config:
        #     prepared_config["default_traits_pool"] = {}
        # for trait_name in trait_keys:
        #     if (
        #         trait_name not in prepared_config["default_traits_pool"]
        #         or prepared_config["default_traits_pool"][trait_name] is None
        #         or prepared_config["default_traits_pool"][trait_name] == {}
        #     ):
        #         prepared_config["default_traits_pool"][trait_name] = (
        #             UnitSimilarityTrait.get_hardcoded_options_by_trait_name(trait_name)
        #         )
        #     elif isinstance(prepared_config["default_traits_pool"][trait_name], int):
        #         prepared_config["default_traits_pool"][trait_name] = {
        #             "value": prepared_config["default_traits_pool"][trait_name],
        #             "income": UnitSimilarityTrait.get_hardcoded_option_by_trait_name_and_value(
        #                 trait_name,
        #                 prepared_config["default_traits_pool"][trait_name],
        #             )[
        #                 "income"
        #             ],
        #         }
        #     elif isinstance()
        #
        # else:
        #     for trait_name, options in prepared_config[
        #         "default_traits_pool"
        #     ].items():
        #         if options is None:
        #             prepared_config["default_traits_pool"][
        #                 trait_name
        #             ] = UnitSimilarityTrait.get_hardcoded_options_by_trait_name(
        #                 trait_name
        #             )
        #         elif isinstance(options, list):

    @staticmethod
    def create_level_from_prepared_config(
        prepared_level_config: dict[str, Any], units: list[Unit]
    ) -> Level:
        lev = Level(
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
        if LevelFactory.check_level_config(level_config):
            prepared_level_config = LevelFactory.prepare_level_config(level_config)
            units = UnitFactory.create_many_units_from_list_of_configs(
                prepared_level_config["units"],
                prepared_level_config["default_traits_pool"],
                prepared_level_config["timer"],
            )
            level = LevelFactory.create_level_from_prepared_config(
                prepared_level_config, units
            )
            return level
        else:
            raise ValueError("Invalid level config")


# t = LevelFactory.prepare_level_config(level_config)
