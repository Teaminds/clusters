import arcade
from system_components.Core_Builded import core


def _initialize_core():
    """Инициализация core из системных компонентов. Порядок имеет значение!"""
    core.set_utils()
    core.set_registry()
    core.set_logger()
    core.set_signals()
    core.set_shortcuts()


_initialize_core()

from components.level_loader import LevelLoader

level = LevelLoader.load_level(act_number=9, level_number=99)

pass

from ui.level_view import LevelView


def main():
    window = arcade.Window(1200, 720, "Clusters")
    view = LevelView(level=level)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
