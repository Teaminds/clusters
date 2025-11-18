from components.unit import Unit
from components.trait_class_map import TRAIT_CLASS_MAP
from components.unit_trait_a import UnitTraitA
from typing import Literal, Any, Optional, Union
from random import choice, randint, randfloat, 

config = [
    {
        "x": 1,
        "y": 1,
        "income_time": 0.0,
        "life_time": None,
        "trait_a": 1,
        "trait_b": 2,
        "trait_c": 3,
        "trait_d": 4,
    }
]



class UnitFactory:
    # traits: dict[Literal["a","b","c","d"], UnitSimilarityTrait] = {},
    # x: float = None,
    # y: float = None,
    # income_time: float = 0.0,
    # life_time: float = float('+inf'),
    @staticmethod
    def create_unit(
        x: Optional[float] = None,
        y: Optional[float] = None,
        income_time: Optional[Union[float,Literal["random"]]] = 0.0,
        life_time: Optional[Union[float,Literal["random",]]] = 0.0,
        trait_a: Optional[int] = None,
        trait_b: Optional[int] = None,
        trait_c: Optional[int] = None,
        trait_d: Optional[int] = None,
    ) -> Unit:
        if x is None:
            x = randfloat(0,100)
        elif isinstance(x, float) or isinstance(x, int):
            if x < 0.0:
                x = 0.0
            elif x > 100.0:
                x = 100.0
        
        if y is None:
            y = randfloat(0,100)
        elif isinstance(y, float) or isinstance(y, int):
            if y < 0.0:
                y = 0.0
            elif y > 100.0:
                y = 100.0
        
        if income_time is None:
            income_time = 0.0
        elif income_time == "random":
            pass
        elif (isinstance(income_time, float) or isinstance(income_time, int)) and income_time < 0.0:
            income_time = 0.0
        else:
            income_time = 0.0
        
        if life_time is None:
            life_time = float('+inf')
        elif life_time == "random":
            pass
        elif (isinstance(life_time, float) or isinstance(life_time, int)) and life_time < 0.0:
            life_time = float('+inf')
        else:
            life_time = float('+inf')
        
        traits={
            "a": None,
            "b": None,
            "c": None,
            "d": None,
        }
        
        def trait_set(trait_key: Literal["a","b","c","d"], trait_value: Optional[int]):
            unit_trait_class = TRAIT_CLASS_MAP[trait_key]
            if trait_value is None or trait_value in unit_trait_class.options:
                traits[trait_key] = unit_trait_class(
                    value=trait_value
                )
            else:
                raise ValueError(f"Value for {unit_trait_class.__class__.__name__} (trait key: {trait_key}) must be one of {unit_trait_class.options}, got {trait_value}")
        
        for trait_key, trait_value in {