from re import L
import arcade
from arcade.gui import (
    UIAnchorLayout,
    UILabel,
    UISpace,
    UIOnActionEvent,
    UIButtonRow,
    UIView,
)
from components.level import Level
from system_components.Core_Builded import core
from typing import TYPE_CHECKING
from components.level_loader import LevelLoader

if TYPE_CHECKING:
    from components.level import Level
    from components.unit import Unit
    from components.group import Group


DEFAULT_FONT = "arial"
DETAILS_FONT = "arial"


class EndOfLevelView(UIView):
    """Представление для экрана окончания уровня (победа/поражение)."""

    def __init__(
        self,
        current_level: Level,
        state: str,
    ):
        super().__init__()
        self.levels = LevelLoader.load_levels_info_list()
        root = self.add_widget(UIAnchorLayout())
        self.labels = {
            "win": {"text": "🎉 Победа!", "color": arcade.color.GREEN_YELLOW},
            "lose": {"text": "💀 Поражение", "color": arcade.color.RED},
        }
        level = LevelLoader.load_level(current_level.get_simple_name())
        self.current_level_simple_name = current_level.get_simple_name()
        next_level = LevelLoader.load_next_level(current_level.get_simple_name())
        center = UIButtonRow(vertical=True, size_hint=(1, 0.3))
        center.add(
            UILabel(
                self.labels[state]["text"],
                font_name=DEFAULT_FONT,
                font_size=32,
                text_color=self.labels[state]["color"],
                size_hint=(1, 0.1),
                align="center",
            )
        )
        center.add(UISpace(size_hint=(1, 0.01), color=arcade.uicolor.WHITE))

        center.with_padding(all=10)
        center.with_background(color=arcade.uicolor.BLACK)
        center.add_button("Перезапустить уровень", size_hint=(0.3, 0.1), align="center")

        next_level = LevelLoader.load_next_level(current_level.get_simple_name())
        if isinstance(next_level, Level):
            center.add_button("Следующий уровень", size_hint=(0.3, 0.1), align="center")
        center.add_button("В меню", size_hint=(0.3, 0.1), align="center")

        root.add(center, anchor_x="center", anchor_y="center")

        @center.event("on_action")
        def on_action(event: UIOnActionEvent):
            from ui.level_view import LevelView

            level = LevelLoader.load_level(current_level.get_simple_name())
            next_level = LevelLoader.load_next_level(current_level.get_simple_name())

            if event.action == "Перезапустить уровень":
                arcade.get_window().show_view(LevelView(level=level))
            elif event.action == "Следующий уровень":
                arcade.get_window().show_view(LevelView(level=next_level))
            elif event.action == "В меню":
                from ui.level_select_view import LevelSelectView

                arcade.get_window().show_view(LevelSelectView())

    def on_key_release(self, symbol, modifiers):
        """Обрабатывает нажатия клавиш."""
        if symbol == arcade.key.R:
            from ui.level_view import LevelView

            level = LevelLoader.load_level(self.current_level_simple_name)
            arcade.get_window().show_view(LevelView(level=level))
        elif symbol == arcade.key.ESCAPE:
            from ui.level_select_view import LevelSelectView

            arcade.get_window().show_view(LevelSelectView())
        return super().on_key_release(symbol, modifiers)
