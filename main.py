# from levels.testo_2 import get_level

import arcade
from ui import game_view
from system_components.Core_Builded import core
from components.level_factory import LevelFactory, level_config

core.set_utils()
core.set_registry()
core.set_logger()
core.set_signals()
core.uid = core.utils().uid()
core.registry().register(core)
core.logger().uid = core.utils().uid()
core.registry().register(core.logger())

# t = LevelFactory.prepare_level_config(level_config=level_config)
l = LevelFactory.create_level_from_config(level_config=level_config)
l.recalc_units_activation()
# breakpoint()
# pass


# def main():
#     window = arcade.Window(1200, 720, "Clusters")
#     view = game_view.LevelView(level=l)
#     window.show_view(view)
#     arcade.run()


# if __name__ == "__main__":
#     main()
