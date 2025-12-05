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

from ui.level_select_view import LevelSelectView


def main():
    window = arcade.Window(1200, 720, "Clusters")
    view = LevelSelectView()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
