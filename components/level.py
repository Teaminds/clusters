from system_components.Core_Builded import core
from components.group_manager import GroupManager

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from components.unit_similarity_trait import UnitSimilarityTrait
    from components.unit import Unit


class Level:
    level_name: str
    level_description: str
    # level_number: int
    units: list[Unit]
    time: float
    timer: int
    goal: int
    group_manager: GroupManager
    income: float
    score: float
    unique_traits_counts: dict[str, int]
    uid: str

    def __init__(
        self,
        # level_number: int,
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
        self.number: int = 0
        self.act_number: int = 0
        self.time: float = 0.0
        self.timer: int = timer
        self.goal: int = goal
        self.units: list[Unit] = units
        self.income: float = income
        self.score: float = score
        self.group_manager: GroupManager = GroupManager(units=units)
        self.unique_traits_counts: dict[str, dict[str, int]] = {}
        self.uid: str = core.utils().uid()
        core.registry().register(self)
        core.signals().subscribe(
            signal_names="unit_activated",
            object_uid=self.uid,
            method_name="increase_unique_trait_type_count_by_unit",
        )
        core.signals().subscribe(
            signal_names="unit_deactivated",
            object_uid=self.uid,
            method_name="decrease_unique_trait_type_count_by_unit",
        )
        self.recalc_units_activation()
        # self.level_number: int = level_number

        # for unit in units or []:
        #     if not isinstance(unit, Unit):
        #         raise TypeError(f"Expected Unit, got {type(unit).__name__}")
        #     self.units.append(unit)

    # @property
    # def unique_traits_counts(self) -> dict[str, int]:
    #     tempo = {}

    #     for unit in self.units:
    #         for trait_name, trait_value in unit.get_traits().items():
    #             pass

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

    def level_score_income(self):
        self.score += self.calculate_level_income()
        # print(f"Score: {self.score}")

    def calculate_level_income(self) -> float:
        income = 0.0
        for unit in self.units:
            if unit.dragging is False:
                income += self.calculate_unit_income(unit)
        return income

    def calculate_unit_income(self, unit: Unit) -> float:
        income = 0.0
        if unit.dragging is False:
            for trait_name, trait in unit.get_traits().items():
                income += self.calculate_trait_income(unit, trait)
        return income

    def calculate_trait_income(
        self,
        unit: Unit,
        trait: UnitSimilarityTrait,
        weather_effect: float = 1.0,
        zone_effect: float = 1.0,
    ) -> float:
        if unit.dragging is False:
            group = self.group_manager.groups[unit.group_uid]
            all_units_count = len(self.units)
            group_units_count = len(group.units)
            weather_effect = weather_effect
            zone_effect = zone_effect

            # unique_count_in_group = group.unique_colors_count
            unique_count_in_group = group.unique_traits_counts[trait.name]
            unique_count_in_level = self.unique_traits_counts[trait.name]
            trait_base_income = trait.income

            # if trait == unit.color:
            #     unique_count_in_group = group.unique_colors_count
            #     unique_count_in_level = self.unique_colors_count
            #     trait_base_income = unit.color.income
            # elif trait == unit.shape:
            #     unique_count_in_group = group.unique_shapes_count
            #     unique_count_in_level = self.unique_shapes_count
            #     trait_base_income = unit.shape.income
            # elif trait == unit.outline_color:
            #     unique_count_in_group = group.unique_outline_colors_count
            #     unique_count_in_level = self.unique_outline_colors_count
            #     trait_base_income = unit.outline_color.income
            # elif trait == unit.fill:
            #     unique_count_in_group = group.unique_fills_count
            #     unique_count_in_level = self.unique_fills_count
            #     trait_base_income = unit.fill.income
            # else:
            #     raise ValueError(f"Unknown trait: {trait}")

            income = self.calculate_trait_income(
                trait_base_income=trait_base_income,
                unique_count_in_group=unique_count_in_group,
                unique_count_in_level=unique_count_in_level,
                group_units_count=group_units_count,
                all_units_count=all_units_count,
                weather_effect=weather_effect,
                zone_effect=zone_effect,
                alpha=3.0,
                beta=1.0,
            )

        return income or 0.0

    def calculate_trait_income(
        trait_base_income: float,
        unique_count_in_group: int,
        unique_count_in_level: int,
        group_units_count: int,
        all_units_count: int,
        weather_effect: float = 1.0,
        zone_effect: float = 1.0,
        alpha: float = 2.0,
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
        if group_units_count <= 1:
            return 0.0  # Юнит вне группы
        if unique_count_in_group >= unique_count_in_level:
            return 0.0  # Полная разнотипность, доход признака нулевой

        homogeneity = 1 - (unique_count_in_group - 1) / (
            unique_count_in_level - 1
        )  # Гомогенность от 0 до 1
        group_size_ratio = (
            group_units_count / all_units_count
        )  # Размер группы от 0 до 1
        result = (
            trait_base_income
            * (homogeneity**alpha)
            * (group_size_ratio**beta)
            * weather_effect
            * zone_effect
        )
        return result

    def increase_unique_trait_types_count(self, trait_name: str, trait_value: Any):
        if trait_name not in self.unique_traits_counts:
            self.unique_traits_counts[trait_name] = {}
        if trait_value not in self.unique_traits_counts[trait_name]:
            self.unique_traits_counts[trait_name][trait_value] = 0
        self.unique_traits_counts[trait_name][trait_value] += 1

    def decrease_unique_trait_types_count(self, trait_name: str, trait_value: Any):
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
        unit = core.registry().get(unit_uid)
        for trait_name in unit.get_traits().keys():
            value = unit.get_trait_value(trait_name)
            self.increase_unique_trait_types_count(trait_name, value)

    def decrease_unique_trait_type_count_by_unit(self, unit_uid: str):
        unit = core.registry().get(unit_uid)
        for trait_name in unit.get_traits().keys():
            value = unit.get_trait_value(trait_name)
            self.decrease_unique_trait_types_count(trait_name, value)

    def recalc_unique_trait_types_count(self):
        self.unique_traits_counts.clear()
        for unit in self.units:
            if unit.active is True:
                for trait_name, trait_body in unit.get_traits().items():
                    self.increase_unique_trait_types_count(trait_name, trait_body.value)

    def recalc_units_activation(self):
        for unit in self.units:
            if unit.active is False:
                if (
                    self.time >= unit.income_time
                    and self.time <= unit.income_time + unit.life_time
                ):
                    unit.activate()
            elif unit.active is True:
                if self.time > unit.income_time + unit.life_time:
                    unit.deactivate()

    def __str__(self):
        return f"Level {self.level_number}"

    def __repr__(self):
        return f"Level({self.level_number})"
