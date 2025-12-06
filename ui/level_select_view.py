from system_components.Core_Builded import core
import textwrap
import time
import arcade
from arcade.gui import (
    UIAnchorLayout,
    UILabel,
    UISpace,
    UIOnActionEvent,
    UIButtonRow,
    UIView,
    UIFlatButton,
    UITextArea,
)
from components import level
from system_components.Core_Builded import core
from typing import TYPE_CHECKING
from components.level_loader import LevelLoader
from ui.level_view import LevelView

if TYPE_CHECKING:
    from components.level import Level
    from components.unit import Unit
    from components.group import Group


DEFAULT_FONT = "arial"
DETAILS_FONT = "arial"


class LevelSelectView(UIView):
    """Представление для выбора уровня."""

    def __init__(self):
        super().__init__()
        self.levels = LevelLoader.load_levels_info_list()
        root = self.add_widget(UIAnchorLayout())
        self.levels_simple = LevelLoader.load_simple_levels_list()
        nav_side = UIButtonRow(vertical=True, size_hint=(0.3, 1))
        nav_side.add(
            UILabel(
                "Уровни",
                font_name=DEFAULT_FONT,
                font_size=32,
                text_color=arcade.uicolor.WHITE,
                size_hint=(1, 0.1),
                align="center",
            )
        )
        nav_side.add(UISpace(size_hint=(1, 0.01), color=arcade.uicolor.WHITE))

        nav_side.with_padding(all=10)
        nav_side.with_background(color=arcade.uicolor.BLACK)
        for act_number, levels_in_act in self.levels.items():
            for level_number, level_info in levels_in_act.items():
                button_text = f"{act_number}-{level_number}: {level_info['name']}"
                nav_side.add_button(
                    button_text,
                    size_hint=(1, 0.1),
                    align="left",
                )

        root.add(nav_side, anchor_x="left", anchor_y="top")

        @nav_side.event("on_action")
        def on_action(event: UIOnActionEvent):
            level_simple_name = event.action.split(":")[0].strip().replace("-", "_")
            level = LevelLoader.load_level(
                simple_name=level_simple_name,
            )
            arcade.get_window().show_view(LevelView(level=level))

        self._body = UIAnchorLayout(size_hint=(0.7, 1))

        self._body.with_padding(all=20)
        root.add(self._body, anchor_x="right", anchor_y="top")
        self._show_start_widgets()

    def _show_start_widgets(self):
        """Отображает приветственный текст и ссылку на исходный код."""
        self._body.clear()
        self._body.add(
            UITextArea(
                text=textwrap.dedent(
                    """
                    Кластеры (прототип)
                    
                    Цель игры: набрать заданное количество очков за отведенное время.
                    
                    Управление мышью.
                    
                    Подсказка: чем сильнее фигруы в группе похожи друг на друга, тем больше очков приносит каждая.
                    
                    Напоминание: это прототип - здесь пока нет графики, звуков, эффектов, сюжета и полного набора уровней.
                    
                    Спасибо за интерес к игре!
                    """
                ).strip(),
                font_name=DETAILS_FONT,
                font_size=22,
                text_color=arcade.uicolor.WHITE,
                size_hint=(0.8, 0.8),
            ),
            anchor_y="top",
        )
        open_sourcecode = self._body.add(
            UIFlatButton(
                text="GitHub",
                size_hint=(0.3, 0.1),
            ),
            anchor_y="bottom",
            align_y=20,
        )

        @open_sourcecode.event("on_click")
        def on_click(_):
            """Открывает страницу с исходным кодом игры в браузере."""
            import webbrowser

            webbrowser.open("https://github.com/Teaminds/clusters")
