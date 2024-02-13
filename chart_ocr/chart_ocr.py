"""
Главный модуль скрипта, точка запуска.
Как работает скрипт:
- Изображение обрезается и разбивается на 4 части, каждая из которых содержит свой график
- Изображение обрабатывается модулем image_processing.py, чтобы улучшить читаемость текста
- Чтение текста с изображения посредством easyocr
- Поиск цветов, которые не смог найти ocr, добавление их используя пропорции и ненайденные на пред. шаге цвета.
- Выходные данные проверяются на валидность
"""

import logging
import os
from collections import Counter

import cv2
import easyocr
from PIL import Image
from PIL.PyAccess import PyAccess

from .exceptions import ColorNotFoundError, ColorsSumError
from .image_processing import improve_image_quality, trim_image_left, split_image_to_parts
from .settings import MONTH_NAMES, TMP_FOLDER_PATH, REVERTED_COLORS_DICT, COLORS_DICT, ERRORS_FOLDER_PATH, INC

reader = easyocr.Reader(['en'], gpu=True)


def _validity_check(values: list[int]) -> None:
    """
    Проверка на валидность значений
    :param values: [TOTAL, RED, ORANGE, YELLOW, LIGHT_GREEN, GREEN]
    :raises ColorsSumError: Неверная сумма цветов в столбцах
    :return:
    """
    if values[0] != sum(values[1:]):
        raise ColorsSumError("OCR, incorrect sum")


def _get_dominant_color(enchanced_part_path: str, bbox: tuple[str, str, str, str]) -> str:
    # Загрузка изображения
    image = cv2.imread(enchanced_part_path)
    if image is None:
        raise FileNotFoundError(f"Файл {enchanced_part_path} не найден.")

    # Преобразование координат для обрезки изображения
    (tl, tr, br, bl) = bbox
    start_x, start_y = int(tl[0]) - INC, int(tl[1]) - INC
    end_x, end_y = int(br[0]) + INC, int(br[1]) + INC

    # Проверка, что координаты находятся в пределах изображения
    if start_x < 0 or start_y < 0 or end_x > image.shape[1] or end_y > image.shape[0]:
        raise ValueError("Координаты bbox выходят за пределы изображения.")

    # Обрезка изображения по bbox
    cropped_image = image[start_y:end_y, start_x:end_x]

    # Проверка, что обрезанное изображение не пустое
    if cropped_image.size == 0:
        raise ValueError("Обрезанное изображение пустое.")

    # Преобразование изображения в одномерный список пикселей
    pixels = cropped_image.reshape(-1, cropped_image.shape[-1])

    # Подсчет количества каждого цвета
    color_counts = Counter(map(tuple, pixels))

    # Нахождение доминирующего цвета
    # Только первое значение, потому что это оттенки серого.
    dominant_color = max(color_counts, key=color_counts.get)[0]

    try:
        return REVERTED_COLORS_DICT[dominant_color]
    except KeyError:
        raise ColorNotFoundError(
            image=image,
            bbox=bbox,
            not_found_color=dominant_color
        )


def _find_missing_colors(image_path: str, colors_dict: dict[str, int]) -> tuple[int, int, int, int, int]:
    """
    Функция перебирает все пиксели на картинке, и смотрит, чтобы в словаре с цветами было любое
    ненулевое значение, если этот цвет обнаружен.
    :param colors_dict:
    :return: Возвращает количество пропущенных пикселей по каждому цвету, порядок такой:
    return RED, ORANGE, YELLOW, LIGHT_GREEN, GREEN
    """
    red, orange, yellow, light_green, green = 0, 0, 0, 0, 0

    # Загрузка изображения
    image = Image.open(image_path)

    pixels: PyAccess = image.load()  # noqa (pycharm type error)

    # Перебор всех пикселей
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            r, g, b, a = pixels[x, y]  # Оттенок серого определяется одним числом.

            if (r, g, b) in COLORS_DICT:
                color = COLORS_DICT[(r, g, b)]
                if color not in colors_dict:
                    if color == "RED":
                        red += 1
                    elif color == "ORANGE":
                        orange += 1
                    elif color == "YELLOW":
                        yellow += 1
                        pixels[x, y] = (0, 0, 0, 255)
                    elif color == "LIGHT_GREEN":
                        light_green += 1
                    elif color == "GREEN":
                        green += 1

    return red, orange, yellow, light_green, green


def _find_undefined_colors(part_path: str, colors_dict: dict[str, int]) -> dict[str, int]:
    """
    Функция ищет неподписанные цифрой значения.
    :param part_path: Путь до картинки со столбцом.
    :param colors_dict: Текущий словарь соответствий цвета и его размера.
    :return:
    """
    total_elements = colors_dict["WHITE"]
    sum_signed_elements = sum(
        [colors_dict.get(color, 0) for color in ["RED", "ORANGE", "YELLOW", "LIGHT_GREEN", "GREEN"]])
    missing_elements = total_elements - sum_signed_elements

    if missing_elements > 0:
        pixels_red, pixels_orange, pixels_yellow, pixels_light_green, pixels_green = _find_missing_colors(part_path,
                                                                                                          colors_dict)

        # Считаем общее количество пикселей для неподписанных цветов
        total_missing_pixels = pixels_red + pixels_orange + pixels_yellow + pixels_light_green + pixels_green

        # Рассчитываем пропорцию для каждого цвета
        if total_missing_pixels > 0:
            proportion_red = (pixels_red / total_missing_pixels) * missing_elements
            proportion_orange = (pixels_orange / total_missing_pixels) * missing_elements
            proportion_yellow = (pixels_yellow / total_missing_pixels) * missing_elements
            proportion_light_green = (pixels_light_green / total_missing_pixels) * missing_elements
            proportion_green = (pixels_green / total_missing_pixels) * missing_elements

            # Присваиваем расчитанные значения в словарь
            if pixels_red > 0:
                colors_dict["RED"] = colors_dict.get("RED", 0) + round(proportion_red)
            if pixels_orange > 0:
                colors_dict["ORANGE"] = colors_dict.get("ORANGE", 0) + round(proportion_orange)
            if pixels_yellow > 0:
                colors_dict["YELLOW"] = colors_dict.get("YELLOW", 0) + round(proportion_yellow)
            if pixels_light_green > 0:
                colors_dict["LIGHT_GREEN"] = colors_dict.get("LIGHT_GREEN", 0) + round(proportion_light_green)
            if pixels_green > 0:
                colors_dict["GREEN"] = colors_dict.get("GREEN", 0) + round(proportion_green)

        return colors_dict


def _part_ocr(enchanced_part_path: str, part_path: str) -> dict[str, list[int]]:
    """
    Функция, которая обрабатывает часть изображения, на которой только один график.
    :param enchanced_part_path: Путь до обработоной картинки со столбцом
    :param part_path: Путь до исходной картинки
    :return:
    """

    # Распознавание текста с помощью EasyOCR
    results = reader.readtext(enchanced_part_path)

    # Извлечение чисел и месяцев из результатов
    colors_dict: dict[str, int] = {}
    month = None
    for (bbox, text, prob) in results:
        # Определение значений
        if text.isdigit():
            dominant_color = _get_dominant_color(enchanced_part_path, bbox)
            colors_dict[dominant_color] = int(text)

        # Определение месяца
        elif any(text.startswith(m) for m in MONTH_NAMES):
            month = text

    # Поиск неподписанных цифрой значений:
    colors_dict = _find_undefined_colors(part_path, colors_dict)

    # Расположение элементов в правильном порядке.
    sorted_num_list: list[int] = [
        colors_dict.get("WHITE", 0),
        colors_dict.get("RED", 0),
        colors_dict.get("ORANGE", 0),
        colors_dict.get("YELLOW", 0),
        colors_dict.get("LIGHT_GREEN", 0),
        colors_dict.get("GREEN", 0),
    ]

    # Проверка значений на валидность
    _validity_check(sorted_num_list)

    return {month: sorted_num_list}


def chart_ocr(image_path: str) -> dict[str, list[int]]:
    """
    Функция, которая обрабатывает изображение с графиком.
    :param image_path: Путь до картинки
    :raises: ColorNotFoundError: Не найден цвет
    :raises: ColorsSumError: Не пройдена проверка на сумму значений для каждого столбца
    :return: Словарь, где ключами являются названия месяца, а значением - упорядоченый список
    значений символизирующих высоту частей графика.

    myDict[MONTH] = [TOTAL, RED, ORANGE, YELLOW, LIGHT_GREEN, GREEN]

    Пример:
    {
        'Aug': [29, 1, 4, 14, 6, 4],

        'Sep': [27, 1, 3, 11, 8, 4],

        'Oct': [28, 1, 2, 12, 8, 5],

        'Nov': [25, 0, 0, 15, 7, 3]
    }
    """
    try:
        # Создаем обьект Image
        image = Image.open(image_path)

        # Валидируем размер картинки
        assert image.size == (226, 255), "Неверный размер изображения."

        # Создаем папку tmp, которая нужна для хранения временных данных
        try:
            os.mkdir(TMP_FOLDER_PATH)
        except FileExistsError:
            pass
        # Создаем папку tmp, которая нужна для хранения временных данных
        try:
            os.mkdir(ERRORS_FOLDER_PATH)
        except FileExistsError:
            pass

        # Обрезаем изображение
        cropped_image = trim_image_left(image)

        # Разрезаем изображение на 4 части, каждая из которых содержит в себе свой график
        image_parts_paths: list[str] = split_image_to_parts(cropped_image, is_enchanced=False)

        # Улучшаем качество изображения
        enchanced_image = improve_image_quality(cropped_image)

        # Разрезаем отредактированное изображение на 4 части, каждая из которых содержит в себе свой график
        enchanced_image_parts_paths: list[str] = split_image_to_parts(enchanced_image, is_enchanced=True)

        # Определение результата для каждой части и их объединение.
        result_dict = {}
        for i in range(0, 4):
            part_result = _part_ocr(enchanced_image_parts_paths[i], image_parts_paths[i])
            result_dict.update(part_result)

        return result_dict

    except ColorNotFoundError as e:
        logging.error(f"Color not found: {e.not_found_color}")
        cv2.imwrite(
            f"{ERRORS_FOLDER_PATH}/{e.not_found_color}:{e.start_x}-{e.start_y}-{e.end_x}-"
            f"{e.end_y}.png", e.image)

    except ColorsSumError as e:
        logging.error(f"Can't parce: {e}")
