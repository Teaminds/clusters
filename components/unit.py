from components.unit_color import UnitColor, Color
from components.unit_fill import UnitFill, Fill
from components.unit_outline import UnitOutline, Outline
from components.unit_outline_color import UnitOutlineColor, OutlineColor
from components.unit_shape import UnitShape, Shape
from components.unit_similarity_trait import UnitSimilarityTrait
from components.unit_trait_a import UnitTraitA
from typing import Literal, Any
import uuid
import random


class Unit:
    uid: uuid
    shape: UnitSimilarityTrait
    color: UnitSimilarityTrait
    fill: UnitSimilarityTrait
    outline: UnitSimilarityTrait
    outline_color: UnitSimilarityTrait
    position: tuple[int, int]
    x: float = 0.0
    y: float = 0.0
    dragged: bool = False
    group_uid: uuid.UUID = None
    body_radius: float = 30.0
    aura_radius: float = body_radius * 1.4

    def __init__(
        self,
        shape: UnitSimilarityTrait = None,
        color: UnitSimilarityTrait = None,
        fill: UnitSimilarityTrait = None,
        outline: UnitSimilarityTrait = None,
        outline_color: UnitSimilarityTrait = None,
        x: float = None,
        y: float = None,
        income_time: float = 0.0,
        life_time: float = float("+inf"),
    ):
        self.uid = uuid.uuid4()
        self.shape: UnitSimilarityTrait = shape or UnitSimilarityTrait(
            value=random.randint(0, 4)
        )
        self.outline: UnitSimilarityTrait = outline or UnitSimilarityTrait(
            value=random.randint(0, 4)
        )
        self.color: UnitColor = color or UnitSimilarityTrait(value=random.randint(0, 4))
        self.fill: UnitSimilarityTrait = fill or UnitSimilarityTrait(
            value=random.randint(0, 4)
        )
        self.outline_color: UnitOutlineColor = outline_color or UnitSimilarityTrait(
            value=random.randint(0, 4)
        )
        self.x: float = x or random.randint(50, 1150)
        self.y: float = y or random.randint(50, 670)
        self.dragged = False

    def distance_to(self, point: tuple[float, float]) -> float:
        dx = self.x - point[0]
        dy = self.y - point[1]
        return (dx**2 + dy**2) ** 0.5

    def __str__(self):
        return f"Unit {str(self.shape)} {str(self.color)} {str(self.fill)} {str(self.outline)} {str(self.position)}"

    def __repr__(self):
        return f"Unit {str(self.shape)} {str(self.color)} {str(self.fill)} {str(self.outline)} {str(self.position)}"
