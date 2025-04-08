import arcade
import math
from typing import Tuple
from components.unit_shape import Shape
from components.unit_outline_color import OutlineColor
from components.group import Group


def draw_shape_filled(
    shape: Shape,
    x: float,
    y: float,
    radius: float,
    color: Tuple[int, int, int],
    outline_color: Tuple[int, int, int],
):
    outline_width = 4

    if shape == Shape.CIRCLE:
        arcade.draw_circle_filled(x, y, radius, color)
        arcade.draw_circle_outline(x, y, radius, outline_color, outline_width)

    elif shape == Shape.SQUARE:
        points = [
            (x - radius * 0.8, y - radius * 0.8),
            (x + radius * 0.8, y - radius * 0.8),
            (x + radius * 0.8, y + radius * 0.8),
            (x - radius * 0.8, y + radius * 0.8),
        ]
        arcade.draw_polygon_filled(points, color)
        arcade.draw_polygon_outline(
            points,
            outline_color,
            outline_width,
        )

    elif shape == Shape.TRIANGLE:
        points = [
            (x, y + radius),
            (x - radius * 0.87, y - radius / 2),
            (x + radius * 0.87, y - radius / 2),
        ]
        arcade.draw_polygon_filled(points, color)
        arcade.draw_polygon_outline(
            points,
            outline_color,
            outline_width,
        )

    elif shape == Shape.STAR:
        points = []
        for i in range(10):
            angle = math.radians(i * 36)
            r = radius * (0.5 if i % 2 else 1.0)
            px = x + math.cos(angle) * r
            py = y + math.sin(angle) * r
            points.append((px, py))
        arcade.draw_polygon_filled(points, color)
        arcade.draw_polygon_outline(
            points,
            outline_color,
            outline_width,
        )
