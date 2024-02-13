"""
Модуль, который отвечает за обработку и предобработку изображения для корректного распознавания текста на ней
используя OCR
"""


from PIL import Image, ImageEnhance

from .settings import IMAGE_SCALE_FACTOR, CONTRAST_FACTOR, PIXELS_TRIM_FROM_LEFT, \
    TMP_FOLDER_PATH, PIXELS_TRIM_TOP_AND_BOTTOM


def split_image_to_parts(image: Image, is_enchanced: bool) -> list[str]:
    """
    Разделяет изображение на 4 части, каждый из которых содержит свой столбец
    на графике.
    :param image:
    :param is_enchanced:
    :return: Список путей до этих частей.
    """
    # Разрезаем изображение на 4 части, каждая из которых содержит в себе свой график
    part_width = image.width // 4
    full_height = image.height

    path_list = []

    for i in range(4):
        left = i * part_width
        right = (i + 1) * part_width if (i < 3) else image.width
        top = 0
        bottom = full_height

        part_image = image.crop((left, top, right, bottom))

        part_image_path = f'{TMP_FOLDER_PATH}/{"e_" if is_enchanced else ""}part_{i}.png'
        part_image.save(part_image_path)

        path_list.append(part_image_path)

    return path_list


def trim_image_left(image: Image) -> Image:
    """
    Обрезает изображение и возвращает путь к новому обрезаному изображению.
    :param image: Путь до картинки
    :return:
    """
    # Получение размеров исходного изображения
    width, height = image.size

    # Обрезаем легенду изображения (Та часть, что слева)
    left = PIXELS_TRIM_FROM_LEFT
    top = 0
    right = width
    bottom = height
    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image


def trim_image_top_and_bottom(image: Image) -> Image:
    """
    Обрезает изображение и возвращает путь к новому обрезаному изображению.
    :param image: Путь до картинки
    :return:
    """
    # Получение размеров исходного изображения
    width, height = image.size

    # Обрезаем изображение сверху и снизу на 400 пикселей
    left = 0
    top = PIXELS_TRIM_TOP_AND_BOTTOM
    right = width
    bottom = height - PIXELS_TRIM_TOP_AND_BOTTOM
    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image


def improve_image_quality(image: Image) -> Image:
    """
    Функция улучшает качество изображения, изменяет его цвета и делает более читабельным для OCR библиотек.
    :param image:
    :return:
    """
    # Масштабирование
    image = image.resize((image.width * IMAGE_SCALE_FACTOR, image.height * IMAGE_SCALE_FACTOR), Image.LANCZOS)

    # Конвертация в черно-белое
    image = image.convert('L')

    # Увеличение контрастности
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(CONTRAST_FACTOR)

    return image
