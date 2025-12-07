from email.headerregistry import Group
from system_components.Core_Builded import core
from components.group_manager import GroupManager

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from components.unit_similarity_trait import UnitSimilarityTrait
    from components.unit import Unit


class Level:
    """Класс уровня, содержащий юниты, таймер, цель и менеджер групп."""

    level_name: str
    level_description: str
    level_number: int
    level_act_number: int
    units_active: dict[str, Unit]
    units_planned: dict[str, Unit]
    units_wasted: dict[str, Unit]
    time: float
    timer: int
    goal: int
    group_manager: GroupManager
    income: float
    score: float
    unique_traits_counts: dict[str, int]
    uid: str
    unit_activation_check_checkpoint: float

    def __init__(
        self,
        level_number: int,
        level_act_number: int,
        units: list,
        timer: int,
        goal: int,
        name: str,
        description: str,
        income: float,
        score: float,
    ):
        self.name: str = name
        self.description: str = description
        self.level_number: int = level_number
        self.act_number: int = level_act_number
        self.time: float = 0.0
        self.timer: int = timer
        self.goal: int = goal
        self.units_active: dict[str, Unit] = {}
        self.units_planned: dict[str, Unit] = {unit.get_uid(): unit for unit in units}
        self.units_wasted: dict[str, Unit] = {}
        self.income: float = income
        self.score: float = score
        self.group_manager: GroupManager = GroupManager()
        self.unique_traits_counts: dict[str, dict[str, int]] = {}
        self.unit_activation_check_checkpoint: float = 0.0
        self.uid: str = core.utils().uid()
        core.registry().register(self)
        core.signals().subscribe(
            signal_names=["unit_activated", "unit_deactivated"],
            object_uid=self.uid,
            method_name="recalc_unique_trait_types_count",
        )
        self.recalc_units_activation()
        # self.group_manager.refresh_groups()

    def level_score_income(self):
        """Обновляет счёт уровня, добавляя доход от активных юнитов."""
        self.score += self.calculate_level_income()

    def calculate_level_income(self) -> float:
        """Вычисляет общий доход уровня от всех активных юнитов."""
        income = 0.0
        for unit in self.units_active.values():
            if unit.dragging is False and unit.active is True:
                income += self.calculate_unit_income(unit)
        return income

    def calculate_unit_income(
        self,
        unit: Unit,
        weather_effect: float = 1.0,
        zone_effect: float = 1.0,
    ) -> float:
        """Вычисляет доход от одного юнита на уровне."""
        income = 0.0
        if unit.dragging is False:
            unit_uid = unit.get_uid()
            group_uid = self.group_manager.get_unit_group_uid(unit_uid)
            group: Group = core.registry().get(group_uid)
            all_units_count = len(self.get_active_units())
            group_units_count = group.get_group_size() if group is not None else 0
            weather_effect = weather_effect
            zone_effect = zone_effect
            for trait in unit.get_traits().values():
                trait_income = trait.get_income()
                trait_value = trait.get_value()
                trait_name = trait.get_name()
                unique_count_in_group = (
                    group.get_unique_trait_count(trait_name) if group is not None else 0
                )
                unique_count_in_level = self.get_unique_trait_types_count(trait_name)
                trait_base_income = trait_income
                income += self.calculate_trait_income(
                    trait_base_income=trait_base_income,
                    unique_count_in_group=unique_count_in_group,
                    unique_count_in_level=unique_count_in_level,
                    group_units_count=group_units_count,
                    all_units_count=all_units_count,
                    weather_effect=weather_effect,
                    zone_effect=zone_effect,
                )

        return income or 0.0

    def calculate_trait_income(
        self,
        trait_base_income: float,
        unique_count_in_group: int,
        unique_count_in_level: int,
        group_units_count: int,
        all_units_count: int,
        weather_effect: float = 1.0,
        zone_effect: float = 1.0,
        alpha: float = 5.0,
        beta: float = 1.0,
    ) -> float:
        """
        Расчёт дохода от одного признака в группе юнитов.

        :param trait_base_income: базовый доход признака
        :param unique_count_in_group: количество уникальных вариантов признака в группе
        :param unique_count_in_level: количество уникальных вариантов признака на уровне (на поле)
        :param group_units_count: количество юнитов в группе
        :param all_units_count: количество юнитов на уровне (на поле)
        :param alpha: степень влияния гомогенности (по умолчанию 2)
        :param beta: степень влияния размера группы (по умолчанию 1)
        :return: доход от признака для юнита
        """
        if group_units_count == 1:
            return 0.0  # Юнит вне группы
        if unique_count_in_group == unique_count_in_level:
            return 0.0  # Полная разнотипность, доход признака нулевой
        if unique_count_in_level == 1:
            return 0.0  # Все юниты одинаковы, доход признака нулевой
        homogeneity = 1 - (
            (unique_count_in_group - 1) / (unique_count_in_level - 1)
        )  # Гомогенность от 0 до 1
        group_size_ratio = (
            group_units_count / all_units_count
        )  # Размер группы от 0 до 1
        result = (
            trait_base_income
            * (homogeneity * alpha)
            * (group_size_ratio * beta)
            * weather_effect
            * zone_effect
        )
        return result

    def increase_unique_trait_types_count(self, trait_name: str, trait_value: Any):
        """Увеличивает счётчик уникальных типов признаков."""
        if trait_name not in self.unique_traits_counts:
            self.unique_traits_counts[trait_name] = {}
        if trait_value not in self.unique_traits_counts[trait_name]:
            self.unique_traits_counts[trait_name][trait_value] = 0
        self.unique_traits_counts[trait_name][trait_value] += 1

    def decrease_unique_trait_types_count(self, trait_name: str, trait_value: Any):
        """Уменьшает счётчик уникальных типов признаков."""
        if trait_name in self.unique_traits_counts:
            self.unique_traits_counts[trait_name][trait_value] -= 1
            if self.unique_traits_counts[trait_name][trait_value] < 0:
                raise ValueError(
                    f"Trait {trait_name} {trait_value} count went below zero in unique_traits_counts"
                )
        else:
            raise ValueError(f"Trait {trait_name} not found in unique_traits_counts")
        if self.unique_traits_counts[trait_name][trait_value] == 0:
            del self.unique_traits_counts[trait_name][trait_value]

    def increase_unique_trait_type_count_by_unit(self, unit_uid: str):
        """Увеличивает счётчик уникальных типов признаков для юнита."""
        unit = core.registry().get(unit_uid)
        for trait_name in unit.get_traits().keys():
            value = unit.get_trait_value(trait_name)
            self.increase_unique_trait_types_count(trait_name, value)

    def decrease_unique_trait_type_count_by_unit(self, unit_uid: str):
        """Уменьшает счётчик уникальных типов признаков для юнита."""
        unit = core.registry().get(unit_uid)
        for trait_name in unit.get_traits().keys():
            value = unit.get_trait_value(trait_name)
            self.decrease_unique_trait_types_count(trait_name, value)

    def recalc_unique_trait_types_count(self):
        """Пересчитывает счётчики уникальных типов признаков на уровне."""
        self.unique_traits_counts.clear()
        for unit in self.units_active.values():
            if unit.active is True:
                for trait_name, trait_body in unit.get_traits().items():
                    self.increase_unique_trait_types_count(trait_name, trait_body.value)

    def get_unique_trait_types_count(self, trait_name) -> int:
        """Возвращает количество уникальных типов признаков на уровне."""
        if trait_name in self.unique_traits_counts:
            return len(self.unique_traits_counts[trait_name])
        return 0

    def recalc_units_activation(self):
        """Пересчитывает активацию юнитов на уровне."""
        units_planned = list(self.get_planned_units())
        for unit in units_planned:
            if unit.is_active() is False and self.time >= unit.income_time:
                self.units_active[unit.get_uid()] = unit
                del self.units_planned[unit.get_uid()]
                unit.activate()
                self.groups_manager_process_unit_placed(unit_uid=unit.get_uid())

        units_active = list(self.get_active_units())
        for unit in units_active:
            if (
                unit.is_active() is True
                and self.time > unit.income_time + unit.life_time
                and unit.life_time not in [0, float("+inf")]
            ):
                self.units_wasted[unit.get_uid()] = unit
                del self.units_active[unit.get_uid()]
                unit.deactivate()
                self.groups_manager_process_unit_removed(unit_uid=unit.get_uid())

    def update_timer(self, delta_time: float):
        """Обновляет таймер уровня и пересчитывает активацию юнитов."""
        self.timer += delta_time
        self.time += delta_time * -1
        if self.time >= self.unit_activation_check_checkpoint + 1:
            self.recalc_units_activation()
            self.unit_activation_check_checkpoint = self.time

    def get_active_units(self) -> list[Unit]:
        """Возвращает список активных юнитов на уровне."""
        return list(self.units_active.values())

    def get_planned_units(self) -> list[Unit]:
        """Возвращает список запланированных юнитов на уровне."""
        return list(self.units_planned.values())

    def get_wasted_units(self) -> list[Unit]:
        """Возвращает список потраченных юнитов на уровне."""
        return list(self.units_wasted.values())

    def get_level_time(self) -> float:
        """Возвращает текущее время уровня."""
        return self.time

    def get_level_timer(self) -> int:
        """Возвращает таймер уровня."""
        return self.timer

    def get_level_score(self) -> float:
        """Возвращает счёт уровня."""
        return self.score

    def get_level_goal(self) -> int:
        """Возвращает цель уровня."""
        return self.goal

    def get_level_act_number(self) -> int:
        """Возвращает номер акта."""
        return self.act_number

    def get_level_number(self) -> int:
        """Возвращает номер уровня в акте."""
        return self.level_number

    def get_level_name(self) -> str:
        """Возвращает имя уровня."""
        return self.name

    def get_level_description(self) -> str:
        """Возвращает описание уровня."""
        return self.description

    def groups_manager_process_unit_placed(self, unit_uid: str) -> None:
        """Обрабатывает размещение юнита в менеджере групп."""
        self.group_manager.process_unit_placed(unit_uid, list(self.units_active.keys()))

    def groups_manager_process_unit_removed(self, unit_uid: str) -> None:
        """Обрабатывает удаление юнита в менеджере групп."""
        self.group_manager.process_unit_removed(unit_uid)

    def get_simple_name(self) -> str:
        """Возвращает простое имя уровня в формате 'акт_уровень'."""
        return f"{self.act_number}_{self.level_number}"

    def __str__(self):
        return f"Level {self.level_number}"

    def __repr__(self):
        return f"Level({self.level_number})"
