from __future__ import annotations
from typing import TYPE_CHECKING
from components import unit
from system_components.Core_Builded import core
from random import uniform

if TYPE_CHECKING:
    from components.unit import Unit


class Group:
    uid: str
    units_with_neighbors: dict[str, set[str]]  # ключ: uid юнита, значение: uid юнита
    neighbors: dict[str, list[str]]  # ключ: uid юнита, значение: список uid соседей
    unique_traits_counts: dict[
        str, int
    ]  # ключ: имя трейта, значение: количество уникальных значений этого трейта в группе
    group_color: tuple[float, float, float]  # для отладки

    def __init__(self) -> Group:
        self.units_with_neighbors = {}
        self.uid = core.utils().uid()
        self.group_color = (
            uniform(0, 255),
            uniform(0, 255),
            uniform(0, 255),
        )  # случайный цвет для отладки
        core.registry().register(self)

    def get_uid(self) -> str:
        return self.uid

    def add_unit(self, unit_uid: str, neighbors_uids: list[str]) -> None:
        self.units_with_neighbors.setdefault(unit_uid, set())
        self.units_with_neighbors[unit_uid].update(neighbors_uids)
        for neighbor_uid in neighbors_uids:
            self.units_with_neighbors.setdefault(neighbor_uid, set())
            self.units_with_neighbors[neighbor_uid].add(unit_uid)
        self._unique_traits_counts_update()

    def remove_unit(self, unit_uid: str) -> None:
        neighbours = self.units_with_neighbors[unit_uid]
        for neighbor_uid in neighbours:
            if neighbor_uid in self.units_with_neighbors:
                if unit_uid in self.units_with_neighbors[neighbor_uid]:
                    self.units_with_neighbors[neighbor_uid].remove(unit_uid)
        if unit_uid in self.units_with_neighbors:
            del self.units_with_neighbors[unit_uid]
        self._unique_traits_counts_update()

    def move_unit_to_another_group(self, unit_uid: str, target_group_uid: str) -> None:
        target_group: Group = core.registry().get(target_group_uid)
        if self.is_unit_in_group_by_uid(
            unit_uid
        ) and not target_group.is_unit_in_group_by_uid(unit_uid):
            neighbors_uids = self.units_with_neighbors[unit_uid]
            self.remove_unit(unit_uid)
            target_group.add_unit(unit_uid, neighbors_uids)

    def is_empty(self) -> bool:
        return len(self.units_with_neighbors) == 0

    def is_unit_in_group_by_uid(self, unit_uid: str) -> bool:
        return unit_uid in self.units_with_neighbors

    def get_list_of_units_uids(self) -> list[str]:
        return list(self.units_with_neighbors.keys())

    def get_dict_of_units_neighbors(self) -> dict[str, set[str]]:
        return self.units_with_neighbors

    def _unique_traits_counts_update(self) -> None:
        # TODO: переосмыслить логику подсчета уникальных трейтов, отдельно проверить чтобы у объектов извне не редактировалсь атрибуты.
        tempo = {}
        final = {}
        for unit_uid in self.units_with_neighbors.keys():
            unit: Unit = core.registry().get(unit_uid)
            if unit.is_dragging() is False and unit.is_active() is True:
                for trait_name, trait_body in unit.get_traits().items():
                    tempo.setdefault(trait_name, [])
                    trait_value = trait_body.get_value()
                    if trait_value not in tempo[trait_name]:
                        tempo[trait_name].append(trait_value)
        for trait_name, trait_values in tempo.items():
            final[trait_name] = len(trait_values)
        self.unique_traits_counts = final

    def get_unique_trait_count(self, trait_name: str) -> int:
        return self.unique_traits_counts.get(trait_name, 0)

    def get_group_size(self) -> int:
        return len(self.units_with_neighbors)

    def get_group_color(self) -> tuple[float, float, float]:
        return self.group_color


# Вся вот эта красивая логика ниже оказалась не нужна, так как уровнем выше в менеджере групп все
# равно юниты добавляются в группу по одному, а значит можно просто удалить старую группу и
# перебрать юниты в "безхозных" группах заново.

# def gather_pieces(self, unit_neighbors_uids: list[str]) -> list[list[str]]:
#     """
#     Функция выполняющая обход графа юнитов группы, начиная с переданных соседей
#     удаленного юнита с целью выявление не привело ли удаление юнита к образованию
#     несвязанных частей группы. Если в процессе обхода удается найти всех переданных
#     соседей удаленного юнита - значит группа осталась целостной и можно прекращать обход.
#     Если же нет, то нужно оставлять один набор юнитов в текущей группе, и выявлять этим же
#     методом остальные несвязанные части группы - для этого метод запускается с непосещенными
#     юнитами группы, пока не будут посещены все юниты группы.

#     Возвращает список списков uid юнитов, которые образуют несвязанные части группы.
#     Эти списки готовы к созданию новых групп через менеджер групп.
#     """
#     checkpoints = {}
#     unvisited_group_units = self.get_list_of_units_uids()
#     visited_units = []
#     plan_to_visit = []
#     result = []
#     for unit_neighbor_uid in unit_neighbors_uids:
#         checkpoints[unit_neighbor_uid] = False
#     for checkpoint in checkpoints:
#         plan_to_visit.append(checkpoint)

#     def _gather_pieces_inner_method(
#         checkpoints: dict[str, bool],
#         unvisited_group_units: list[str],
#         visited_units: list[str],
#         result: list[list[str]],
#     ) -> list[list[str]]:
#         while plan_to_visit:
#             current_unit_uid = plan_to_visit.pop(0)
#             if current_unit_uid in unvisited_group_units:
#                 unvisited_group_units.remove(current_unit_uid)
#             if current_unit_uid not in visited_units:
#                 visited_units.append(current_unit_uid)
#             if current_unit_uid in checkpoints:
#                 checkpoints[current_unit_uid] = True
#             neighbors = self.units_with_neighbors.get(current_unit_uid, [])
#             for neighbor_uid in neighbors:
#                 if neighbor_uid not in visited_units:
#                     plan_to_visit.insert(0, neighbor_uid)
#             if _is_checkpoints_all_visited(
#                 checkpoints, visited_units
#             ):  # После обхода проверяем достигли ли мы всех контрольных точек
#                 break

#         if _is_checkpoints_all_visited(checkpoints, visited_units):
#             semifinal = []
#             semifinal.extend(unvisited_group_units)
#             semifinal.extend(visited_units)
#             if len(semifinal) > 1:
#                 result.append(semifinal)
#             return result
#         else:
#             _gather_pieces_inner_method(
#                 checkpoints=checkpoints,
#                 unvisited_group_units=unvisited_group_units,
#                 visited_units=visited_units,
#                 result=result,
#             )
#             return result

#     def _is_checkpoints_all_visited(checkpoints, visited_units) -> bool:
#         for checkpoint in checkpoints:
#             if checkpoint not in visited_units:
#                 return False
#         return True

#     result.extend(
#         _gather_pieces_inner_method(
#             checkpoints=checkpoints,
#             unvisited_group_units=unvisited_group_units,
#             visited_units=visited_units,
#             result=result,
#         )
#     )
#     return result
