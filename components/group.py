from __future__ import annotations

from system_components.Core_Builded import core

from shapely.geometry import Point
from shapely.ops import unary_union

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.unit import Unit


class Group:
    units: list[Unit]
    uid: str

    def __init__(self):
        self.units = []
        self.uid = core.utils().uid()
        core.registry().register(self)

    def add_unit(self, unit: Unit):
        if unit not in self.units:
            self.units.append(unit)
            unit.group_uid = self.uid

    def remove_unit(self, unit: Unit):
        if unit in self.units:
            self.units.remove(unit)
            unit.group_uid = None

    @property
    def unique_traits_counts(self) -> dict[str, int]:
        tempo = {}

        for unit in self.units:
            for trait_name, trait_value in unit.get_traits().items():
                pass

    # @property
    # def unique_colors_count(self) -> int:
    #     uniques = []
    #     for unit in self.units:
    #         if unit.color.value not in uniques:
    #             uniques.append(unit.color.value)
    #     return len(uniques)

    # @property
    # def unique_shapes_count(self) -> int:
    #     uniques = []
    #     for unit in self.units:
    #         if unit.shape.value not in uniques:
    #             uniques.append(unit.shape.value)
    #     return len(uniques)

    # @property
    # def unique_outline_colors_count(self) -> int:
    #     uniques = []
    #     for unit in self.units:
    #         if unit.outline_color.value not in uniques:
    #             uniques.append(unit.outline_color.value)
    #     return len(uniques)

    # @property
    # def unique_fills_count(self) -> int:
    #     uniques = []
    #     for unit in self.units:
    #         if unit.fill.value not in uniques:
    #             uniques.append(unit.fill.value)
    #     return len(uniques)
