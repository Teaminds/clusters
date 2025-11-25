from __future__ import annotations
from system_components.Core_Builded import core

from typing import TYPE_CHECKING, Literal, Any, Optional, Union

if TYPE_CHECKING:
    from components.unit_similarity_trait import UnitSimilarityTrait


class Unit:
    uid: str
    traits: dict[str, UnitSimilarityTrait]
    x: float
    y: float
    draggedable: bool
    income_time: float
    life_time: float
    body_radius: float
    aura_radius: float
    dragging: bool
    group_uid: str
    active: bool

    def __init__(
        self,
        traits: dict[str, UnitSimilarityTrait],
        x: float,
        y: float,
        income_time: float,
        life_time: float,
        draggedable: bool,
        body_radius: float,
        aura_radius: float,
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
        self.group_uid = None
        core.registry().register(self)

    def get_uid(self) -> str:
        return self.uid

    def get_position(self) -> tuple[float, float]:
        return self.x, self.y

    def distance_to(self, point: tuple[float, float]) -> float:
        x, y = self.get_position()
        target_x, target_y = point
        dx = x - target_x
        dy = y - target_y
        return (dx**2 + dy**2) ** 0.5

    def move_to(self, x: float, y: float):
        self.x = x
        self.y = y

    def set_dragged(self, dragging: bool):
        if self.draggedable:
            self.dragging = dragging

    def activate(self):
        if not self.active:
            self.active = True
            core.signals().notify("unit_activated", unit_uid=self.get_uid())

    def deactivate(self):
        if self.active:
            self.active = False
            core.signals().notify("unit_deactivated", unit_uid=self.get_uid())

    def starting_life_try(self, time_now: float):
        if not self.active and self.income_time <= time_now:
            self.activate()

    def spend_life_time(self, time_now: float):
        if self.active and self.life_time != float("+inf"):
            if self.life_time > 0.0:
                time_gone = time_now - self.income_time
                self.life_time = max(0.0, self.life_time - time_gone)
                if self.life_time == 0.0:
                    self.deactivate()
            elif self.life_time == 0.0:
                self.deactivate()

    def get_traits(self) -> dict[str, UnitSimilarityTrait]:
        return self.traits

    def get_trait_value(self, trait_name: str) -> Any:
        trait = self.traits.get(trait_name)
        if trait:
            return trait.value
        return None
