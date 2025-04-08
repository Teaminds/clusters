import uuid
from components.group import Group
from components.unit import Unit


class GroupManager:
    groups: dict[uuid.UUID, Group] = {}
    _id_counter: int = 0

    def __init__(self, units: list[Unit] = None):
        self.groups = {}
        self.refresh_groups(units)

    def get_distance(self, unit1: Unit, unit2: Unit) -> float:
        return ((unit1.x - unit2.x) ** 2 + (unit1.y - unit2.y) ** 2) ** 0.5

    def refresh_groups(self, units: list[Unit]):
        for unit in units:
            if unit.dragged is False:
                neghbours = []
                potential_groups = []
                biggest_group = None
                unit_group = None
                for other_unit in units:
                    if (
                        unit != other_unit
                        and self.get_distance(unit, other_unit) < unit.aura_radius * 2
                    ):
                        neghbours.append(other_unit)
                        if (
                            other_unit.group_uid is not None
                            and self.groups[other_unit.group_uid]
                            not in potential_groups
                        ):
                            potential_groups.append(self.groups[other_unit.group_uid])
                            if biggest_group is None or len(
                                self.groups[other_unit.group_uid].units
                            ) > len(biggest_group.units):
                                biggest_group = self.groups[other_unit.group_uid]
                if len(potential_groups) > 0:
                    if unit.group_uid is not None:
                        unit_group = self.groups[unit.group_uid]
                        unit_group.remove_unit(unit)
                        if len(unit_group.units) == 0:
                            del self.groups[unit_group.uid]
                    biggest_group.add_unit(unit)

                    for potential_group in potential_groups:
                        if potential_group != biggest_group:
                            self.collapse_groups(biggest_group, potential_group)
                else:
                    if unit.group_uid is not None:
                        unit_group = self.groups[unit.group_uid]
                        if len(unit_group.units) == 1 and unit in unit_group.units:
                            pass
                        else:
                            unit_group.remove_unit(unit)
                            if len(unit_group.units) == 0:
                                del self.groups[unit_group.uid]
                            unit_group = Group()
                            unit_group.add_unit(unit)
                            self.groups[unit_group.uid] = unit_group
                    else:
                        unit_group = Group()
                        unit_group.add_unit(unit)
                        self.groups[unit_group.uid] = unit_group

    def move_to_group(self, unit: Unit, group_uid: uuid.UUID):
        if unit.group_uid is not None:
            self.groups[unit.group_uid].remove_unit(unit)
            if len(self.groups[unit.group_uid].units) == 0:
                del self.groups[unit.group_uid]
        self.groups[group_uid].add_unit(unit)

    def collapse_groups(self, main_group: Group, assimilated_group: Group):
        if main_group == assimilated_group:
            return
        for unit in assimilated_group.units:
            assimilated_group.remove_unit(unit)
            if len(assimilated_group.units) == 0:
                del self.groups[assimilated_group.uid]
            main_group.add_unit(unit)
