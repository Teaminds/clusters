from components.unit import Unit
import uuid
from shapely.geometry import Point
from shapely.ops import unary_union


class Group:
    units: list[Unit]
    uid: uuid.UUID

    def __init__(self):
        self.units = []
        self.uid = uuid.uuid4()

    def add_unit(self, unit: Unit):
        if unit not in self.units:
            self.units.append(unit)
            unit.group_uid = self.uid

    def remove_unit(self, unit: Unit):
        if unit in self.units:
            self.units.remove(unit)
            unit.group_uid = None

    @property
    def unique_colors_count(self) -> int:
        uniques = []
        for unit in self.units:
            if unit.color.value not in uniques:
                uniques.append(unit.color.value)
        return len(uniques)

    @property
    def unique_shapes_count(self) -> int:
        uniques = []
        for unit in self.units:
            if unit.shape.value not in uniques:
                uniques.append(unit.shape.value)
        return len(uniques)

    @property
    def unique_outline_colors_count(self) -> int:
        uniques = []
        for unit in self.units:
            if unit.outline_color.value not in uniques:
                uniques.append(unit.outline_color.value)
        return len(uniques)

    @property
    def unique_fills_count(self) -> int:
        uniques = []
        for unit in self.units:
            if unit.fill.value not in uniques:
                uniques.append(unit.fill.value)
        return len(uniques)
