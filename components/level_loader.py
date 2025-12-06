import json
from components.level import Level
from components.level_factory import LevelFactory
from system_components.Core_Builded import core


class LevelLoader:
    @staticmethod
    def load_level_config(simple_name: str) -> dict:
        with open(f"levels/{simple_name}.json", encoding="utf-8") as f:
            level_config = json.load(f)
        return level_config

    @staticmethod
    def load_simple_levels_list() -> list:
        levels_info = LevelLoader.load_levels_info_list()
        simple_levels_list = []
        for act_number, levels_in_act in levels_info.items():
            for level_number, level_info in levels_in_act.items():
                simple_levels_list.append(level_info["simple_name"])
        return simple_levels_list

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
                        and "level_number" in level_config
                        and "act_number" in level_config
                    ):
                        level_info = {
                            "name": level_config["name"],
                            "description": level_config.get("description", ""),
                            "level_number": level_config["level_number"],
                            "act_number": level_config["act_number"],
                            "simple_name": f"{level_config['act_number']}_{level_config['level_number']}",
                            "timer": level_config.get("timer", float("+inf")),
                            "goal_score": level_config.get("goal_score", float("+inf")),
                        }
                        if level_info["act_number"] not in levels:
                            levels[level_info["act_number"]] = {}
                        levels[level_info["act_number"]][
                            level_info["level_number"]
                        ] = level_info
        levels = core.utils().sort_dict_recursive(levels)
        return levels

    @staticmethod
    def load_level(simple_name: str) -> Level:
        level_config = LevelLoader.load_level_config(simple_name=simple_name)
        level = LevelFactory.create_level_from_config(level_config=level_config)
        return level

    @staticmethod
    def load_next_level(simple_name: str) -> Level | None:
        levels_simple_list = LevelLoader.load_simple_levels_list()
        next_level_simple_name = core.utils().get_next_item_of_list(
            levels_simple_list,
            simple_name,
        )
        if next_level_simple_name:
            next_level = LevelLoader.load_level(simple_name=next_level_simple_name)
            return next_level
        return None
