import arcade
from components import level
from levels.testo_3 import get_level
from ui.drawer import draw_unit

# print(level)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
AURA_ALPHA = 40  # прозрачность ауры


class GameView(arcade.View):
    def __init__(self, level: level):
        super().__init__()
        self.level = level
        self.dragged_unit = None
        self.drag_offset = (0, 0)
        self.score_timer = 0.0
        self.state = "playing"

    def on_key_press(self, key, modifiers):

        if key == arcade.key.R and self.state in ("win", "lose"):
            self.level = get_level()
            self.level.group_manager.refresh_groups(self.level.units)
            self.state = "playing"
            self.score_timer = 0.0

    def on_draw(self):
        self.clear()
        if self.state == "playing":
            if self.level.timer <= 0:
                self.state = "lose"
            elif self.level.score >= self.level.goal:
                self.state = "win"
        if self.state == "playing":
            units_sprites = arcade.SpriteList()
            for unit in self.level.units:
                x = unit.x
                y = unit.y

                # AURA
                if (
                    unit.group_uid is not None
                    and len(self.level.group_manager.groups[unit.group_uid].units) > 1
                ):
                    arcade.draw_circle_filled(
                        center_x=x,
                        center_y=y,
                        radius=unit.aura_radius,
                        color=arcade.color.GRAY,
                    )
            for unit in self.level.units:
                x = unit.x
                y = unit.y
                # BODY
                # arcade.draw_circle_filled(
                #     center_x=x,
                #     center_y=y,
                #     radius=unit.body_radius,
                # )
                # points = make_shape(unit.shape.value, x, y, unit.body_radius)
                # draw_shape_filled(
                #     points,
                #     unit.color.rgb,
                # )
                # draw_styled_outline(
                #     points, unit.outline.value, unit.outline_color.rgb, 4
                # )
                unit_sprite = draw_unit(unit, x, y)
                units_sprites.append(unit_sprite)
            units_sprites.draw()
            for unit in self.level.units:
                arcade.draw_text(
                    round(self.level.calculate_unit_income(unit), 2),
                    unit.x,
                    unit.y + (unit.body_radius * 0.5),
                    arcade.color.WHITE,
                    12,
                    anchor_x="center",
                    bold=True,
                )
            # информация
            info_lines = [
                f"Score: {self.level.score}",
                f"Goal: {self.level.goal}",
                f"Time: {self.level.timer:.1f}s",
            ]

            for i, line in enumerate(info_lines):
                arcade.draw_text(
                    line,
                    10,
                    self.window.height - 20 - i * 20,
                    arcade.color.WHITE,
                    14,
                    anchor_x="left",
                    anchor_y="top",
                )
        elif self.state == "win":
            arcade.draw_text(
                "🎉 Победа!", 500, 360, arcade.color.GREEN_YELLOW, 30, anchor_x="center"
            )
            arcade.draw_text(
                "Нажмите R чтобы начать заново",
                500,
                300,
                arcade.color.WHITE,
                16,
                anchor_x="center",
            )

        elif self.state == "lose":
            arcade.draw_text(
                "💀 Поражение", 500, 360, arcade.color.RED, 30, anchor_x="center"
            )
            arcade.draw_text(
                "Нажмите R чтобы начать заново",
                500,
                300,
                arcade.color.WHITE,
                16,
                anchor_x="center",
            )

    def on_update(self, delta_time: float):
        if self.state == "playing":
            self.level.timer -= delta_time

            # Защита от ухода в минус
            if self.level.timer < 0:
                self.level.timer = 0

            # Таймер уровня
            self.level.timer = max(0.0, self.level.timer - delta_time)

            # Накопление времени до 1 секунды
            self.score_timer += delta_time
            if self.score_timer >= 1.0:
                self.level.level_score_income()
                self.score_timer -= 1.0  # сохраняем остаток (чтобы не терялась дельта)
            for unit in self.level.units:
                arcade.draw_text(
                    self.level.calculate_unit_income(unit),
                    unit.x,
                    unit.y,
                    arcade.color.WHITE,
                    16,
                    anchor_x="center",
                )

    def on_mouse_press(self, x, y, button, modifiers):
        for unit in reversed(self.level.units):  # сверху вниз
            if unit.distance_to((x, y)) <= unit.body_radius:
                self.dragged_unit = unit
                self.dragged_unit.dragged = True
                self.level.group_manager.groups[
                    self.dragged_unit.group_uid
                ].remove_unit(self.dragged_unit)
                self.level.group_manager.refresh_groups(self.level.units)
                self.drag_offset = (x - unit.x, y - unit.y)
                break

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragged_unit:
            new_x = x - self.drag_offset[0]
            new_y = y - self.drag_offset[1]

            r = self.dragged_unit.body_radius
            w, h = self.window.width, self.window.height

            # Ограничения
            new_x = max(r, min(w - r, new_x))
            new_y = max(r, min(h - r, new_y))

            # Проверка на пересечение с другими body
            for other in self.level.units:
                if other is self.dragged_unit:
                    continue
                dist = ((new_x - other.x) ** 2 + (new_y - other.y) ** 2) ** 0.5
                min_dist = self.dragged_unit.body_radius + other.body_radius
                if dist < min_dist:
                    return  # отменяем перемещение

            # Всё в порядке — применяем позицию
            self.dragged_unit.x = new_x
            self.dragged_unit.y = new_y

    def on_mouse_release(self, x, y, button, modifiers):
        self.dragged_unit.dragged = False
        self.level.group_manager.refresh_groups(self.level.units)
        self.dragged_unit = None
