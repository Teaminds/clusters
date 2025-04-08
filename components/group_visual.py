from enum import Enum


class Color(Enum):
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"
    VIOLET = "violet"


class GroupVisual:
    def __init__(
        self,
        color: Color,
        fill_visibility: float = 0.2,
        outline_visibility: float = 0.5,
    ):
        self.color = color
        if color == Color.BLUE:
            self.rgb = (0, 0, 255)
        elif color == Color.GREEN:
            self.rgb = (0, 255, 0)
        elif color == Color.RED:
            self.rgb = (255, 0, 0)
        elif color == Color.YELLOW:
            self.rgb = (255, 255, 0)
        elif color == Color.VIOLET:
            self.rgb = (238, 130, 238)
        else:
            raise ValueError(f"Unknown color: {color}")
