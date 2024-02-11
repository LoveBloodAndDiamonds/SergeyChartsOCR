# Значение, во сколько раз увеличивается картинка перед поиском текста на ней
IMAGE_SCALE_FACTOR: int = 20

# Значение r g b при >= котором белые пиксели заменяются на синие перед поиском текста на ней
REPLACING_PIXELS_BOUNDAREA: int = 190

# Значение, которое отвечает за увеличение контрастности картинки перед поиском текста на ней
CONTRAST_FACTOR: int = 1

# Количество пикселей, которое обрезается слева
PIXELS_TRIM_FROM_LEFT: int = 35

# Количество пикселей, которое обрезается сверху и снизу
PIXELS_TRIM_TOP_AND_BOTTOM: int = 400

# Названия месяцев на картинке
MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Путь до папки tmp
TMP_FOLDER_PATH = "tmp"


# RGB цвета
COLORS_DICT = {
    (0, 143, 136): "GREEN",
    (0, 192, 115): "LIGHT_GREEN",
    (255, 220, 72): "YELLOW",
    (255, 163, 62): "ORANGE",
    (255, 51, 58): "RED",
}

# Цвета после инвертации цветов
REVERTED_COLORS_DICT = {
    255: "WHITE",
    254: "WHITE",
    253: "WHITE",

    100: "GREEN",
    99: "GREEN",
    98: "GREEN",

    125: "LIGHT_GREEN",
    126: "LIGHT_GREEN",
    127: "LIGHT_GREEN",

    213: "YELLOW",
    214: "YELLOW",
    215: "YELLOW",

    178: "ORANGE",
    179: "ORANGE",
    180: "ORANGE",

    112: "RED",
    113: "RED",
    114: "RED"
}

# REVERTED_COLORS_DICT = {
#     255: "WHITE",
#     99: "GREEN",
#     126: "LIGHT_GREEN",
#     214: "YELLOW",
#     179: "ORANGE",
#     113: "RED",
# }

# Немного расширим диапазон поиска
# keys_to_add = []
#
# for original_key, color in REVERTED_COLORS_DICT.items():
#     for i in range(original_key - 1, original_key + 2):
#         if i != original_key and i not in REVERTED_COLORS_DICT:
#             keys_to_add.append((i, color))
#
# for key, color in keys_to_add:
#     REVERTED_COLORS_DICT[key] = color
