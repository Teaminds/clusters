from typing import TYPE_CHECKING
from system_components.Core_Builded import core
from components.group import Group
from components.unit import Unit

if TYPE_CHECKING:
    from components.level import Level


class GroupManager:
    uid: str
    groups: dict[str, Group] = {}  # ключ: uid группы, значение: группа

    def __init__(self):
        self.uid = core.utils().uid()
        core.registry().register(self)
        self.groups = {}

    def _create_group(self) -> Group:
        new_group = Group()
        new_group_uid = new_group.get_uid()
        self.groups[new_group_uid] = new_group
        return new_group

    def _remove_group(self, group_uid: str) -> None:
        if group_uid in self.groups:
            del self.groups[group_uid]

    def _get_groups_with_unit(self, unit_uid: str) -> list[Group]:
        groups_uids_with_unit = []
        for group in self.groups.values():
            if group.is_unit_in_group_by_uid(unit_uid):
                groups_uids_with_unit.append(group)
        return groups_uids_with_unit

    def _found_neighbors_of_unit(
        self, unit_uid: str, other_units_ids: list[str]
    ) -> list[str]:
        neighbors_uids = []
        unit: Unit = core.registry().get(unit_uid)
        for other_unit_uid in other_units_ids:
            if other_unit_uid != unit_uid:
                unit: Unit = core.registry().get(unit_uid)
                other_unit: Unit = core.registry().get(other_unit_uid)
                if unit.are_we_neighbors(other_unit):
                    neighbors_uids.append(other_unit_uid)
        return neighbors_uids

    def _merge_groups(self, main_group_uid: str, other_group_uid: str) -> None:
        other_group: Group = core.registry().get(other_group_uid)
        other_group_uids = other_group.get_list_of_units_uids()
        for unit_uid in other_group_uids:
            other_group.move_unit_to_another_group(
                unit_uid=unit_uid, target_group_uid=main_group_uid
            )
        self._remove_group(other_group_uid)

    def process_unit_placed(self, unit_uid: str, other_units_ids: list[str]) -> None:
        if unit_uid in other_units_ids:
            other_units_ids.remove(unit_uid)
        neigbours = self._found_neighbors_of_unit(unit_uid, other_units_ids)
        if unit_uid in neigbours:
            neigbours.remove(unit_uid)
        potential_groups = []
        biggest_group = None
        no_groups_units = []
        for neighbor_uid in neigbours:
            neighbor_groups = self._get_groups_with_unit(neighbor_uid)
            if len(neighbor_groups) == 0:
                no_groups_units.append(neighbor_uid)
            elif len(neighbor_groups) >= 1:
                for group in neighbor_groups:
                    if group not in potential_groups:
                        potential_groups.append(group)
                        if (
                            biggest_group is None
                            or group.get_group_size() > biggest_group.get_group_size()
                        ):
                            biggest_group = group
        for group in potential_groups:
            if group != biggest_group:
                self._merge_groups(biggest_group.get_uid(), group.get_uid())
        if biggest_group is not None and len(neigbours) > 0:
            biggest_group.add_unit(unit_uid, neigbours)
        if len(no_groups_units) > 0:
            if biggest_group is None:
                biggest_group = self._create_group()
                biggest_group.add_unit(unit_uid, list(neigbours))
            for unit_no_group in no_groups_units:
                biggest_group.add_unit(unit_no_group, [unit_uid])

    def process_unit_removed(self, unit_uid: str) -> None:
        former_groups = self._get_groups_with_unit(unit_uid)
        if len(former_groups) == 0:
            return
        if len(former_groups) > 1:
            raise ValueError(
                "Юнит не может состоять в нескольких группах одновременно."
            )
        former_group = former_groups[0]
        former_group.remove_unit(unit_uid)
        former_group_units_neighbors = former_group.get_dict_of_units_neighbors()
        former_group_units_uids = list(former_group_units_neighbors.keys())
        groups_templates = []
        if former_group.is_empty():
            return
        if former_group.get_group_size() < 2:
            self._remove_group(former_group.get_uid())
            return
        visited_units = set()
        while len(former_group_units_uids) > 0:
            group_template = {}
            plan_to_visit = []
            unit_to_plan = former_group_units_uids.pop(0)
            plan_to_visit.extend([unit_to_plan])
            while len(plan_to_visit) > 0:
                current_unit_uid = plan_to_visit.pop(0)
                pass
                visited_units.add(current_unit_uid)
                if len(former_group_units_neighbors[current_unit_uid]) > 0:
                    group_template[current_unit_uid] = former_group_units_neighbors[
                        current_unit_uid
                    ]
                    insertion = (
                        former_group_units_neighbors[current_unit_uid] - visited_units
                    )
                    plan_to_visit.extend(insertion)
                else:
                    former_group.remove_unit(current_unit_uid)

            if len(group_template) >= 2:
                groups_templates.append(group_template)
        if len(groups_templates) == 1:
            return
        if len(groups_templates) == 0:
            self._remove_group(former_group.get_uid())
            return
        if len(groups_templates) > 1:
            self._remove_group(former_group.get_uid())
            for group_template in groups_templates:
                if len(group_template) < 2:
                    continue
                else:
                    new_group = self._create_group()
                    for (
                        current_unit_uid,
                        current_neighbors_uids,
                    ) in group_template.items():
                        new_group.add_unit(current_unit_uid, current_neighbors_uids)

    def _get_distance(self, unit_a: Unit | str, unit_b: Unit | str) -> float:
        if isinstance(unit_a, Unit):
            unit_1 = unit_a
        elif isinstance(unit_a, str):
            unit_1 = core.registry().get(unit_a)
        else:
            raise ValueError("Аргумент должен быть экземпляром Unit или строкой uid.")
        if isinstance(unit_b, Unit):
            unit_2 = unit_b
        elif isinstance(unit_b, str):
            unit_2 = core.registry().get(unit_b)
        else:
            raise ValueError("Аргумент должен быть экземпляром Unit или строкой uid.")
        x1, y1 = unit_1.get_position()
        x2, y2 = unit_2.get_position()
        return core.utils().get_2d_distance(x1, y1, x2, y2)

    def get_unit_group_uid(self, unit_uid: str) -> str | None:
        groups_with_unit = self._get_groups_with_unit(unit_uid)
        if len(groups_with_unit) == 0:
            return None
        elif len(groups_with_unit) > 1:
            raise ValueError(
                "Юнит не может состоять в нескольких группах одновременно."
            )
        else:
            return groups_with_unit[0].get_uid()
