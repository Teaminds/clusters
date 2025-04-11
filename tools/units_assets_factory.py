import os
from PIL import Image, ImageOps
from itertools import product

# Настройки
SIZE = (128, 128)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "../assets/units")
SHAPE_DIR = os.path.join(BASE_DIR, "../assets/units_parts/shapes")
TEXTURE_DIR = os.path.join(BASE_DIR, "../assets/units_parts/textures")
OUTLINE_DIR = os.path.join(BASE_DIR, "../assets/units_parts/outlines")

# Цвета тела и обводки (RGB)
BODY_COLORS = [
    (255, 100, 100),  # Красный
    (100, 255, 100),  # Зелёный
    (100, 100, 255),  # Синий
    (255, 255, 100),  # Жёлтый
    (255, 100, 255),  # Фиолетовый
]

OUTLINE_COLORS = [
    (200, 20, 20),
    (20, 200, 20),
    (20, 20, 200),
    (200, 200, 20),
    (200, 20, 200),
]


def _rgb_hex(rgb):
    pass
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def bake_unit(body_color, outline_color, shape_path, texture_path, outline_path):
    # Загрузка слоёв
    shape_original = Image.open(shape_path).convert("RGBA").resize(SIZE)
    shape_grayscale = Image.open(shape_path).convert("L").resize(SIZE)
    shape_alpha = shape_original.getchannel("A")
    texture = Image.open(texture_path).convert("RGBA").resize(SIZE)
    outline_original = Image.open(outline_path).convert("RGBA").resize(SIZE)
    outline_grayscale = Image.open(outline_path).convert("L").resize(SIZE)
    outline_alpha = outline_original.getchannel("A")
    outline_mask = Image.open(outline_path).convert("L").resize(SIZE)

    # Цветная форма
    colored_body = ImageOps.colorize(
        shape_grayscale, black="#00000000", white=body_color
    )
    colored_body.putalpha(shape_original.getchannel("A"))

    # Ограниченная текстура

    r, g, b, a = texture.split()
    a = a.point(lambda val: int(val * 0.3))  # 30% прозрачности
    texture = Image.merge("RGBA", (r, g, b, a))

    # Обрезаем текстуру по форме
    masked_texture = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    masked_texture.paste(texture, (0, 0), mask=shape_alpha)

    # Цветная обводка
    outline_layer = Image.new("RGBA", SIZE, outline_color)
    outline_layer.putalpha(outline_alpha)

    # Финальный композит
    result = Image.alpha_composite(colored_body, masked_texture)
    result = Image.alpha_composite(result, outline_layer)
    return result


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    shape_files = sorted(os.listdir(SHAPE_DIR))
    texture_files = sorted(os.listdir(TEXTURE_DIR))

    for shape in shape_files:
        shape_file = os.path.join(SHAPE_DIR, shape)
        shape_idx = shape_files.index(shape)
        otline_dir_final = OUTLINE_DIR + "/" + str(shape_idx)
        outline_files = sorted(os.listdir(otline_dir_final))
        for outline in outline_files:
            outline_file = os.path.join(otline_dir_final, outline)
            outline_idx = outline_files.index(outline)
            for texture in texture_files:
                texture_file = os.path.join(TEXTURE_DIR, texture)
                texture_idx = texture_files.index(texture)
                for body_color in BODY_COLORS:
                    body_color_idx = BODY_COLORS.index(body_color)
                    body_color_hex = _rgb_hex(body_color)
                    for outline_color in OUTLINE_COLORS:
                        outline_color_idx = OUTLINE_COLORS.index(outline_color)
                        outline_color_hex = _rgb_hex(outline_color)
                        # ПРОДОЛЖАЙ ТУТ
                        result = bake_unit(
                            body_color_hex,
                            outline_color_hex,
                            shape_file,
                            texture_file,
                            outline_file,
                        )
                        code = f"{shape_idx:02d}_{texture_idx:02d}_{outline_idx:02d}_{body_color_idx:02d}_{outline_color_idx:02d}"
                        result.save(os.path.join(OUTPUT_DIR, f"{code}.png"))

    print("Готово!")
    print("Сохранено в:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
