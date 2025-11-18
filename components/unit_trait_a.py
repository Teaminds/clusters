from components.unit_similarity_trait import UnitSimilarityTrait
from enum import Enum
from typing import Literal


class UnitTraitA(UnitSimilarityTrait):
    options: Literal[0, 1, 2, 3, 4]
