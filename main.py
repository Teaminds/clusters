# from levels.testo_2 import get_level

# import arcade
# from ui import game_view
from system_components.Core_Builded import core
from components.level_loader import LevelLoader

core.set_utils()
core.set_registry()
core.set_logger()
core.set_signals()
core.uid = core.utils().uid()
core.registry().register(core)
core.logger().uid = core.utils().uid()
core.registry().register(core.logger())

# t = LevelFactory.prepare_level_config(level_config=level_config)
levels_info_list = LevelLoader.load_levels_info_list()
level_config = LevelLoader.load_level_config(level_number=1, act_number=1)
level = LevelLoader.load_level(level_number=1, act_number=1)
breakpoint()
pass


# def main():
#     window = arcade.Window(1200, 720, "Clusters")
#     view = game_view.LevelView(level=l)
#     window.show_view(view)
#     arcade.run()


# if __name__ == "__main__":
#     main()
