from typing import TYPE_CHECKING
import arcade
from system_components.ResourceLoader import resource_path

if TYPE_CHECKING:
    from components.unit import Unit


def draw_unit(unit: Unit, x: float, y: float) -> None:
    """Создаёт и возвращает спрайт юнита для отрисовки в заданной позиции."""
    traits = unit.get_traits()
    traits_simple = {}
    for trait_name, trait in traits.items():
        traits_simple[trait_name] = trait.value
    # trait_b_0_trait_c_0_trait_e_0_trait_a_0_trait_d_0.png
    visual_code = f"{int(traits_simple['trait_b']):02d}_{int(traits_simple['trait_c']):02d}_{int(traits_simple['trait_e']):02d}_{int(traits_simple['trait_a']):02d}_{int(traits_simple['trait_d']):02d}"
    path_of_texture = resource_path(f"assets/units/{visual_code}.png")
    sprite = arcade.Sprite(path_or_texture=path_of_texture, scale=0.5)
    sprite.width = unit.body_radius * 2
    sprite.height = unit.body_radius * 2
    sprite.center_x = x
    sprite.center_y = y
    return sprite
