import json
from components.level_factory import LevelFactory
from system_components.Core_Builded import core


class LevelLoader:
    @staticmethod
    def load_level_config(level_number: int, act_number: int) -> dict:
        with open(f"levels/{level_number}_{act_number}.json", encoding="utf-8") as f:
            level_config = json.load(f)
        return level_config

    @staticmethod
    def load_levels_info_list() -> dict:
        import os

        levels = {}
        for filename in os.listdir("levels"):
            if filename.endswith(".json"):
                with open(os.path.join("levels", filename), encoding="utf-8") as f:
                    level_config = json.load(f)
                    if (
                        "name" in level_config
                        and "number" in level_config
                        and "act_number" in level_config
                    ):
                        level_info = {
                            "name": level_config["name"],
                            "description": level_config.get("description", ""),
                            "number": level_config["number"],
                            "act_number": level_config["act_number"],
                            "timer": level_config.get("timer", float("+inf")),
                            "goal_score": level_config.get("goal_score", float("+inf")),
                        }
                        if level_info["act_number"] not in levels:
                            levels[level_info["act_number"]] = {}
                        levels[level_info["act_number"]][
                            level_info["number"]
                        ] = level_info
        levels = core.utils().sort_dict_recursive(levels)
        return levels

    @staticmethod
    def load_level(level_number: int, act_number: int) -> dict:
        level_config = LevelLoader.load_level_config(
            level_number=level_number, act_number=act_number
        )
        level = LevelFactory.create_level_from_config(level_config=level_config)
        return level
