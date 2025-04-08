import arcade
import math
from typing import Tuple
from components.unit_shape import Shape
from components.group import Group


def draw_shape_filled(
    shape: Shape, x: float, y: float, radius: float, color: Tuple[int, int, int]
):
    if shape == Shape.CIRCLE:
        arcade.draw_circle_filled(x, y, radius, color)

    elif shape == Shape.SQUARE:
        points = [
            (x - radius * 0.8, y - radius * 0.8),
            (x + radius * 0.8, y - radius * 0.8),
            (x + radius * 0.8, y + radius * 0.8),
            (x - radius * 0.8, y + radius * 0.8),
        ]
        arcade.draw_polygon_filled(points, color)

    elif shape == Shape.TRIANGLE:
        points = [
            (x, y + radius),
            (x - radius * 0.87, y - radius / 2),
            (x + radius * 0.87, y - radius / 2),
        ]
        arcade.draw_polygon_filled(points, color)

    elif shape == Shape.STAR:
        points = []
        for i in range(10):
            angle = math.radians(i * 36)
            r = radius * (0.5 if i % 2 else 1.0)
            px = x + math.cos(angle) * r
            py = y + math.sin(angle) * r
            points.append((px, py))
        arcade.draw_polygon_filled(points, color)


# def draw_group_aura_shapely(
#     group,
#     fill_color=(150, 150, 150, 40),
#     outline_color=(255, 255, 255),
#     outline_width=2,
# ):
#     # 1. Собираем все ауры как круги (через буфер)
#     shapes = []
#     for unit in group.units:
#         circle = Point(unit.x, unit.y).buffer(unit.aura_radius, resolution=32)
#         shapes.append(circle)

#     # 2. Объединяем в один сложный полигон
#     result = unary_union(shapes)

#     # 3. Отрисовываем
#     fill_rgba = (*fill_color, 50)
#     outline_rgba = (*outline_color, 150)

#     _draw_shape_from_shapely(result, fill_rgba, outline_rgba, outline_width)


# def _draw_shape_from_shapely(shape, fill_color, outline_color, outline_width):
#     if shape.geom_type == "Polygon":
#         exterior = list(shape.exterior.coords)
#         arcade.draw_polygon_filled(exterior, fill_color)
#         arcade.draw_polygon_outline(exterior, outline_color, outline_width)

#         for hole in shape.interiors:
#             arcade.draw_polygon_outline(list(hole.coords), (0, 0, 0), 1)

#     elif shape.geom_type == "MultiPolygon":
#         for poly in shape.geoms:
#             _draw_shape_from_shapely(poly, fill_color, outline_color, outline_width)
