from components.unit import Unit
from components.group_manager import GroupManager
from components.unit_color import UnitColor
from components.unit_shape import UnitShape
from components.unit_outline import UnitOutline
from components.unit_fill import UnitFill
from components.utils import Utils


class Level:
    level_name: str = None
    level_description: str = None
    level_number: int
    units: list[Unit]
    timer: int
    goal: int
    group_manager: GroupManager
    income: float = 0.0
    score: float = 0.0

    def __init__(
        self,
        level_number: int,
        units: list,
        timer: int,
        goal: int,
        level_name: str = None,
        level_description: str = None,
    ):
        self.level_name: str = level_name
        self.level_description: str = level_description
        self.level_number: int = level_number
        self.timer: int = timer
        self.goal: int = goal
        self.units: list[Unit] = []
        self.group_manager: GroupManager = GroupManager(units=units)

        for unit in units or []:
            if not isinstance(unit, Unit):
                raise TypeError(f"Expected Unit, got {type(unit).__name__}")
            self.units.append(unit)

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
    def unique_outlines_count(self) -> int:
        uniques = []
        for unit in self.units:
            if unit.outline.value not in uniques:
                uniques.append(unit.outline.value)
        return len(uniques)

    @property
    def unique_fills_count(self) -> int:
        uniques = []
        for unit in self.units:
            if unit.fill.value not in uniques:
                uniques.append(unit.fill.value)
        return len(uniques)

    def level_score_income(self):
        self.score += self.calculate_level_income()
        # print(f"Score: {self.score}")

    def calculate_level_income(self) -> float:
        income = 0.0
        for unit in self.units:
            if unit.dragged is False:
                income += self.calculate_unit_income(unit)
        return income

    def calculate_unit_income(self, unit: Unit) -> float:
        income = 0.0
        if unit.dragged is False:
            income += self.calculate_trait_income(unit, unit.color)
            income += self.calculate_trait_income(unit, unit.shape)
            income += self.calculate_trait_income(unit, unit.outline)
            income += self.calculate_trait_income(unit, unit.fill)
        return income

    def calculate_trait_income(
        self, unit: Unit, trait: UnitColor | UnitShape | UnitShape | UnitFill
    ) -> float:
        if unit.dragged is False:
            group = self.group_manager.groups[unit.group_uid]
            all_units_count = len(self.units)
            group_units_count = len(group.units)
            weather_effect = 1.0
            zone_effect = 1.0
            if trait == unit.color:
                unique_count_in_group = group.unique_colors_count
                unique_count_in_level = self.unique_colors_count
                trait_base_income = unit.color.income
            elif trait == unit.shape:
                unique_count_in_group = group.unique_shapes_count
                unique_count_in_level = self.unique_shapes_count
                trait_base_income = unit.shape.income
            elif trait == unit.outline:
                unique_count_in_group = group.unique_outlines_count
                unique_count_in_level = self.unique_outlines_count
                trait_base_income = unit.outline.income
            elif trait == unit.fill:
                unique_count_in_group = group.unique_fills_count
                unique_count_in_level = self.unique_fills_count
                trait_base_income = unit.fill.income
            else:
                raise ValueError(f"Unknown trait: {trait}")
            income = Utils.calculate_trait_income(
                b=trait_base_income,
                n=unique_count_in_group,
                m=unique_count_in_level,
                q=group_units_count,
                w=all_units_count,
                t=weather_effect,
                z=zone_effect,
                alpha=2.0,
                beta=1.0,
            )

        return income or 0.0

    def __str__(self):
        return f"Level {self.level_number}"

    def __repr__(self):
        return f"Level({self.level_number})"
