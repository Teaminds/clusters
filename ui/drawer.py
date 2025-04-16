import arcade
import math
from typing import Tuple
from components.unit_shape import Shape
from components.unit_outline_color import OutlineColor
from components.group import Group
from components.unit_outline import UnitOutline, Outline
from components.unit import Unit


def make_shape(
    shape: Shape,
    x: float,
    y: float,
    radius: float,
):
    if shape == Shape.CIRCLE:
        points = []
        resolution = 8
        for i in range(resolution):
            angle = 2 * math.pi * i / resolution
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.append((px, py))

    elif shape == Shape.SQUARE:
        points = [
            (x - radius * 0.8, y - radius * 0.8),
            (x + radius * 0.8, y - radius * 0.8),
            (x + radius * 0.8, y + radius * 0.8),
            (x - radius * 0.8, y + radius * 0.8),
        ]

    elif shape == Shape.TRIANGLE:
        points = [
            (x, y + radius),
            (x - radius * 0.87, y - radius / 2),
            (x + radius * 0.87, y - radius / 2),
        ]

    elif shape == Shape.STAR:
        points = []
        for i in range(10):
            angle = math.radians(i * 36)
            r = radius * (0.5 if i % 2 else 1.0)
            px = x + math.cos(angle) * r
            py = y + math.sin(angle) * r
            points.append((px, py))
    else:
        raise ValueError(f"Unknown shape: {shape}")
    return points


def draw_unit(unit: Unit, x: float, y: float) -> None:
    visual_code = f"{unit.shape.value:02d}_{unit.fill.value:02d}_{unit.outline.value:02d}_{unit.color.value:02d}_{unit.outline_color.value:02d}"
    sprite = arcade.Sprite(path_or_texture=f"assets/units/{visual_code}.png", scale=0.5)
    sprite.center_x = x
    sprite.center_y = y
    return sprite


# def draw_shape_filled(
#     points: list,
#     color: Tuple[int, int, int],
# ):

#     arcade.draw_polygon_filled(points, color)


# def draw_styled_outline(points, style, color, width=1.0):
#     if len(points) < 2:
#         return

#     points = points + [points[0]]
#     segments = [(points[i], points[i + 1]) for i in range(len(points) - 1)]

#     spacing = {
#         # Outline.SOLID: (1.0, 0.0),
#         # Outline.DASHED: (6, 6),
#         # Outline.DOTTED: (2, 6),
#         # Outline.IRREGULAR: [(4, 4), (10, 2), (6, 6), (2, 8)],
#         # Outline.RARE: (4, 12),
#         Outline.SOLID: (1.0, 0.0),
#         Outline.DASHED: (8, 2),
#         Outline.DOTTED: (4, 4),
#         Outline.SUPER_RARE: (2.0, 20.0),
#         Outline.RARE: (2.0, 10.0),
#     }

#     for i, (p1, p2) in enumerate(segments):
#         dx, dy = p2[0] - p1[0], p2[1] - p1[1]
#         seg_length = math.hypot(dx, dy)
#         angle = math.atan2(dy, dx)

#         if style == Outline.SOLID:
#             arcade.draw_line(p1[0], p1[1], p2[0], p2[1], color, width)
#         else:
#             pattern = spacing[style]
#             # if style == Outline.IRREGULAR:
#             #     pattern = pattern[i % len(pattern)]
#             _draw_segmented_line(p1, angle, seg_length, pattern, color, width)


# def _draw_segmented_line(start, angle, length, pattern, color, width):
#     dash, gap = pattern
#     pos = 0.0
#     while pos < length:
#         end = min(dash, length - pos)
#         x1 = start[0] + math.cos(angle) * pos
#         y1 = start[1] + math.sin(angle) * pos
#         x2 = start[0] + math.cos(angle) * (pos + end)
#         y2 = start[1] + math.sin(angle) * (pos + end)
#         arcade.draw_line(x1, y1, x2, y2, color, width)
#         pos += dash + gap
