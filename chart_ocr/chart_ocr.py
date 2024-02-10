import os

import easyocr
from PIL import Image

from .image_processing import improve_image_quality, trim_image, split_image_to_parts
from .settings import MONTH_NAMES, TMP_FOLDER_PATH

reader = easyocr.Reader(['en'], gpu=True)


def _part_ocr(part_path: str) -> dict[str, list[int]]:
    """
    Функция, которая обрабатывает часть изображения, на которой только один график.
    :param part_path:
    :return:
    """
    # Распознавание текста с помощью EasyOCR
    results = reader.readtext(part_path)

    # Извлечение чисел и месяцев из результатов
    num_text_list = []
    month = None
    for (bbox, text, prob) in results:
        if text.isdigit():
            num_text_list.append(text)
        elif any(text.startswith(m) for m in MONTH_NAMES):
            month = text

    return {month: num_text_list}


def chart_ocr(image_path: str) -> dict[str, list[int]]:
    """
    Функция, которая обрабатывает изображение с графиком.
    :param image_path: Путь до картинки
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
    # Создаем обьект Image
    image = Image.open(image_path)

    # Валидируем размер картинки
    assert image.size == (226, 255), "Неверный размер изображения."

    # Создаем папку tmp, которая нужна для хранения временных данных
    try:
        os.mkdir(TMP_FOLDER_PATH)
    except FileExistsError:
        pass

    # Обрезаем изображение
    cropped_image = trim_image(image)

    # Улучшаем качество изображения
    enchanced_image = improve_image_quality(cropped_image)

    # Разрезаем изображение на 4 части, каждая из которых содержит в себе свой график
    image_parts_paths: list[str] = split_image_to_parts(enchanced_image)

    # Определение результата для каждой части и их объединение.
    result_dict = {}
    for part_path in image_parts_paths:
        part_result = _part_ocr(part_path)
        result_dict.update(part_result)

    return result_dict
