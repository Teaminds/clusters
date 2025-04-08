from components.unit_color import UnitColor, Color
from components.unit_fill import UnitFill, Fill
from components.unit_outline import UnitOutline, Outline
from components.unit_shape import UnitShape, Shape
import uuid
import random


class Unit:
    uid: uuid
    shape: UnitShape
    color: UnitColor
    fill: UnitFill
    outline: UnitOutline
    position: tuple[int, int]
    x: float = 0.0
    y: float = 0.0
    group_uid: uuid.UUID = None
    body_radius: float = 30.0
    aura_radius: float = body_radius * 1.4

    def __init__(
        self,
        shape: UnitShape = None,
        color: UnitColor = None,
        fill: UnitFill = None,
        outline: UnitOutline = None,
        x: float = None,
        y: float = None,
    ):
        self.uid = uuid.uuid4()
        self.shape: UnitShape = shape or UnitShape(value=random.choice(list(Shape)))
        self.color: UnitColor = color or UnitColor(value=random.choice(list(Color)))
        self.fill: UnitFill = fill or UnitFill(value=random.choice(list(Fill)))
        self.outline: UnitOutline = outline or UnitOutline(
            value=random.choice(list(Outline))
        )
        self.x: float = x or random.randint(0, 800)
        self.y: float = y or random.randint(0, 600)
        self.dragged = False

    def distance_to(self, point: tuple[float, float]) -> float:
        dx = self.x - point[0]
        dy = self.y - point[1]
        return (dx**2 + dy**2) ** 0.5

    def __str__(self):
        return f"Unit {str(self.shape)} {str(self.color)} {str(self.fill)} {str(self.outline)} {str(self.position)}"

    def __repr__(self):
        return f"Unit {str(self.shape)} {str(self.color)} {str(self.fill)} {str(self.outline)} {str(self.position)}"
