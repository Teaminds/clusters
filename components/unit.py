from __future__ import annotations
from system_components.Core_Builded import core

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from components.unit_similarity_trait import UnitSimilarityTrait


class Unit:
    uid: str
    traits: dict[str, UnitSimilarityTrait]
    x: int | float
    y: int | float
    draggedable: bool
    income_time: float
    life_time: float
    body_radius: int | float
    aura_radius: int | float
    dragging: bool
    active: bool

    def __init__(
        self,
        traits: dict[str, UnitSimilarityTrait],
        x: int | float,
        y: int | float,
        income_time: float,
        life_time: float,
        draggedable: bool,
        body_radius: int | float,
        aura_radius: int | float,
    ):
        self.uid = core.utils().uid()
        self.traits = traits
        self.x = x
        self.y = y
        self.income_time = income_time
        self.life_time = life_time
        self.draggedable = draggedable
        self.body_radius = body_radius
        self.aura_radius = aura_radius
        self.dragging = False
        self.active = False
        core.registry().register(self)

    def get_uid(self) -> str:
        return self.uid

    def get_position(self) -> tuple[float, float]:
        return self.x, self.y

    def distance_to(self, point: tuple[float, float]) -> float:
        x1, y1 = self.get_position()
        x2, y2 = point
        return core.utils().get_2d_distance(x1, y1, x2, y2)

    def move_to(self, x: float, y: float):
        self.x = x
        self.y = y

    def set_dragged(self, dragging: bool):
        if self.draggedable:
            self.dragging = dragging

    def activate(self):
        if not self.active:
            self.active = True
            core.signals().notify("unit_activated")
            core.signals().notify("specific_unit_activated", unit_uid=self.uid)

    def deactivate(self):
        if self.active:
            self.active = False
            core.signals().notify("unit_deactivated")
            core.signals().notify("specific_unit_deactivated", unit_uid=self.uid)

    def starting_life_try(self, time_now: float):
        if not self.active and self.income_time <= time_now:
            self.activate()

    def spend_life_time_check(self, time_now: float):
        if (
            self.active
            and self.life_time != float("+inf")
            and (
                time_now - self.income_time - self.life_time <= 0
                or time_now - self.income_time <= 0
            )
        ):
            self.deactivate()

    def get_traits(self) -> dict[str, UnitSimilarityTrait]:
        return self.traits

    def get_trait_value(self, trait_name: str) -> Any:
        trait = self.traits.get(trait_name)
        if trait:
            return trait.value
        return None

    def is_active(self) -> bool:
        return self.active

    def is_dragging(self) -> bool:
        return self.dragging

    def are_we_neighbors(self, other_unit: Unit) -> bool:
        distance = self.distance_to(other_unit.get_position())
        combined_aura_radius = self.aura_radius + other_unit.aura_radius
        return distance <= combined_aura_radius

    def get_radius(self) -> float:
        return self.body_radius

    def get_aura_radius(self) -> float:
        return self.aura_radius
