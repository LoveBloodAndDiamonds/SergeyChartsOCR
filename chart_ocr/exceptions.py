from chart_ocr.settings import INC


class ColorNotFoundError(Exception):

    def __init__(self, image, bbox: tuple, not_found_color: int):
        # Картинка
        self.image = image

        # Диапаназон поиска дом. значения
        (tl, tr, br, bl) = bbox
        self.start_x, self.start_y = int(tl[0]) - INC, int(tl[1]) - INC
        self.end_x, self.end_y = int(br[0]) + INC, int(br[1]) + INC

        # Не найденное значение:
        self.not_found_color = not_found_color
