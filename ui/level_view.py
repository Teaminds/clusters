import time
import arcade
from components import level
from system_components.Core_Builded import core
from typing import TYPE_CHECKING
from components.level_loader import LevelLoader
from ui.drawer import draw_unit

if TYPE_CHECKING:
    from components.level import Level
    from components.unit import Unit
    from components.group import Group

AURA_ALPHA = 40  # прозрачность ауры


class LevelView(arcade.View):
    def __init__(self, level: Level):
        super().__init__()
        self.level: Level = level
        self.dragging_unit: Unit = None
        self.drag_offset: tuple[int, int] = (0, 0)
        self.score_timer: float = 0.0
        self.state: str = "playing"

    def on_draw(self):
        self.clear()
        active_units = self.level.get_active_units()
        planned_units = self.level.get_planned_units()
        level_timer = self.level.get_level_timer()
        level_score = self.level.get_level_score()
        level_goal = self.level.get_level_goal()
        level_name = self.level.get_level_name()
        level_description = self.level.get_level_description()
        level_act_number = self.level.get_level_act_number()
        level_number = self.level.get_level_number()
        level_time = self.level.get_level_time()

        if self.state == "playing":
            if level_timer <= 0:
                self.state = "lose"
            elif level_score >= level_goal:
                self.state = "win"
        if self.state == "playing":
            units_sprites = arcade.SpriteList()
            for unit in planned_units:
                if unit.is_active() is False:
                    unit.starting_life_try(time_now=level_timer)
                    pass
            for unit in active_units:
                if unit.is_active() is True:
                    unit.spend_life_time_check(time_now=level_timer)
                    x, y = unit.get_position()
                    radius = unit.get_radius()
                    aura_radius = unit.get_aura_radius()
                    unit_group_uid = self.level.group_manager.get_unit_group_uid(
                        unit.get_uid()
                    )
                    unit_group: Group = core.registry().get(unit_group_uid)
                    # AURA
                    if unit_group is not None:
                        arcade.draw_circle_filled(
                            center_x=x,
                            center_y=y,
                            radius=aura_radius,
                            color=unit_group.get_group_color(),
                        )
                    unit_sprite = draw_unit(unit, x, y)
                    units_sprites.append(unit_sprite)
            units_sprites.draw()

            for unit in active_units:
                if unit.is_active():
                    x, y = unit.get_position()
                    radius = unit.get_radius()
                    income_value = round(self.level.calculate_unit_income(unit), 2)
                    if income_value > 0:
                        income_value_prefix = "+"
                    else:
                        income_value_prefix = ""
                    arcade.draw_text(
                        f"{income_value_prefix}{income_value}",
                        x,
                        y + (radius * 0.5),
                        arcade.color.WHITE,
                        12,
                        anchor_x="center",
                        bold=True,
                    )

            # информация об уровне
            info_lines = [
                f"Level: ({level_act_number}-{level_number}) {level_name}",
                f"Score: {level_score:.2f}",
                f"Goal: {level_goal}",
                f"Time: {level_timer:.1f}s",
            ]

            for i, line in enumerate(info_lines):
                arcade.draw_text(
                    line,
                    20,
                    700 - i * 20,
                    arcade.color.WHITE,
                    12,
                    anchor_x="left",
                    anchor_y="top",
                )
        elif self.state == "win":
            arcade.draw_text(
                "🎉 Победа!",
                620,
                320,
                arcade.color.GREEN_YELLOW,
                84,
                anchor_x="center",
            )
            arcade.draw_text(
                "Нажмите R чтобы начать заново",
                620,
                288,
                arcade.color.WHITE,
                12,
                anchor_x="center",
            )

        elif self.state == "lose":
            arcade.draw_text(
                "💀 Поражение",
                620,
                320,
                arcade.color.RED,
                84,
                anchor_x="center",
            )
            arcade.draw_text(
                "Нажмите R чтобы начать заново",
                620,
                288,
                arcade.color.WHITE,
                12,
                anchor_x="center",
            )

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.R:
            self.level = LevelLoader.load_level(
                self.level.get_level_number(), self.level.get_level_act_number()
            )
            self.dragging_unit = None
            self.drag_offset = (0, 0)
            self.score_timer = 0.0
            self.state = "playing"
        return super().on_key_release(symbol, modifiers)

    def on_update(self, delta_time: float):
        if self.state == "playing":
            self.level.update_timer(-delta_time)

            # Защита от ухода в минус
            if self.level.get_level_timer() < 0:
                self.level.update_timer(-self.level.get_level_timer())

            # Накопление времени до 1 секунды
            self.score_timer += delta_time
            if self.score_timer >= 1.0:
                self.level.level_score_income()
                self.score_timer -= 1.0  # сохраняем остаток (чтобы не терялась дельта)
            for unit in self.level.get_active_units():
                arcade.draw_text(
                    self.level.calculate_unit_income(unit),
                    unit.x,
                    unit.y,
                    arcade.color.WHITE,
                    16,
                    anchor_x="center",
                )

    def on_mouse_press(self, x, y, button, modifiers):
        for unit in reversed(list(self.level.get_active_units())):  # сверху вниз
            if unit.is_active() and unit.distance_to((x, y)) <= unit.get_radius():
                core.signals().notify("unit_removed")
                core.signals().notify("specific_unit_removed", unit_uid=unit.get_uid())
                self.dragging_unit = unit
                self.dragging_unit.set_dragged(True)
                self.level.groups_manager_process_unit_removed(
                    self.dragging_unit.get_uid()
                )
                self.drag_offset = (x - unit.x, y - unit.y)
                break

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging_unit:
            new_x = x - self.drag_offset[0]
            new_y = y - self.drag_offset[1]

            r = self.dragging_unit.get_radius()
            w, h = self.window.width, self.window.height

            # Ограничения
            new_x = max(r, min(w - r, new_x))
            new_y = max(r, min(h - r, new_y))

            # Проверка на пересечение с другими body
            for other in self.level.get_active_units():
                if other.is_active():
                    if other is self.dragging_unit:
                        continue
                    dist = ((new_x - other.x) ** 2 + (new_y - other.y) ** 2) ** 0.5
                    min_dist = self.dragging_unit.get_radius() + other.get_radius()
                    if dist < min_dist:
                        return  # отменяем перемещение

            # Всё в порядке — применяем позицию
            self.dragging_unit.x = new_x
            self.dragging_unit.y = new_y

    def on_mouse_release(self, x, y, button, modifiers):
        self.dragging_unit.set_dragged(False)
        self.level.groups_manager_process_unit_placed(self.dragging_unit.get_uid())
        core.signals().notify("unit_moved")
        core.signals().notify("specific_unit_moved", self.dragging_unit.uid)
        self.dragging_unit = None
