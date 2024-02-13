"""
Модуль, который описывает ошибки, которые мы хотим отловить при работе скрипта.
"""

from chart_ocr.settings import INC


class ColorNotFoundError(Exception):
    """
    Ошибка, которая вызывается, когда скрипт не смог найти цвет на графике.
    Данные в init необходимы чтобы при ошибке сохранить картинку в директорию errors.
    """
    def __init__(self, image, bbox: tuple, not_found_color: int):
        # Картинка
        self.image = image

        # Диапаназон поиска дом. значения
        (tl, tr, br, bl) = bbox
        self.start_x, self.start_y = int(tl[0]) - INC, int(tl[1]) - INC
        self.end_x, self.end_y = int(br[0]) + INC, int(br[1]) + INC

        # Не найденное значение:
        self.not_found_color = not_found_color


class ColorsSumError(ValueError):
    """
    Ошибка, которая вызывается, когда сумма значений всех цветов не равна общему значению.
    """
    pass
