from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import pytesseract
from pprint import pp


def process_image(image: Image) -> Image:
    """
    Функция улучшает качество изображения.
    :param image:
    :return:
    """

    # Масштабирование
    image = image.resize((image.width * 4, image.height * 4), Image.LANCZOS)

    # Получение размеров изображения
    width, height = image.size

    # Получение доступа к пикселям изображения
    pixels = image.load()

    # Замена белых пикселей на синие
    for y in range(height):  # Высота изображения
        for x in range(width):  # Ширина изображения
            r, g, b, a = pixels[x, y]
            # Проверить, является ли пиксель белым
            brdr = 200  # 200 good
            if all([r > brdr, g > brdr, b > brdr]):
                # Заменить цвет пикселя на синий и установить полную непрозрачность
                pixels[x, y] = (0, 0, 0, 255)  # pixels[x, y] = (0, 0, 255, 255)

    # Конвертация в черно-белое
    # image = image.convert('L')

    # Увеличение контрастности
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # Подберите коэффициент на основе вашего изображения

    # Инверсия цветов
    # image = ImageOps.invert(image)

    # Удаление шума
    # image = image.filter(ImageFilter.MedianFilter())

    return image


def parse_image(image_path: str) -> dict[str, list]:
    """
    Функция, которая обрабатывает изображение с графиком.
    :param image_path: Путь до картинки
    :return: Словарь, где ключами являются названия месяца, а значением - упорядоченый список
    значений символизирующих высоту частей графика.

    Пример:
    {
        'Aug': [29, 1, 4, 14, 6, 4],

        'Sep': [27, 1, 3, 11, 8, 4],

        'Oct': [28, 1, 2, 12, 8, 5],

        'Nov': [25, 0, 0, 15, 7, 3]
    }
    """
    image = Image.open(image_path)
    output_image_name: str = f"output_0{image_path.split('.png')[0][-2:]}"

    # Получение размеров исходного изображения
    width, height = image.size

    # Обрезаем легенду изображения (Та часть, что слева)
    left = 35
    top = 0
    right = width
    bottom = height
    cropped_image = image.crop((left, top, right, bottom))

    cropped_image.save(f"tmp/cropped_{output_image_name}.png")  # todo remove

    # Улучшаем качество изображения
    cropped_image = process_image(cropped_image)

    # Разрезаем изображение на 4 части, каждая из которых содержит в себе свой график
    part_width = cropped_image.width // 4
    full_height = cropped_image.height

    # Обрезка и обработка каждой части
    result_dict = {}
    for i in range(4):
        left = i * part_width
        right = (i + 1) * part_width if (i < 3) else cropped_image.width
        top = 0
        bottom = full_height
        part_image = cropped_image.crop((left, top, right, bottom))
        part_image.save(f'tmp/part_{i}.png')

        custom_config = r'--oem 3 --psm 6'
        image_text = pytesseract.image_to_string(part_image, config=custom_config)
        image_text_list = [el for el in image_text.strip().split('\n') if el]

        result_dict[image_text_list[-1]] = image_text_list[:-1]

    return result_dict


def validate_image(image_path: str) -> None:
    """
    Функция валидирует изображение.
    :raises AssertionError
    :param image_path: Путь до картинки
    :return:
    """
    image = Image.open(image_path)

    assert image.size == (226, 255), "Неверный размер изображения."


def check_result(chart_data: dict[str, list]):
    try:
        assert chart_data["Aug"] == ["35", "9", "20", "5"], "1"
        assert chart_data["Sep"] == ["31", "5", "15", "11"], "2"
        assert chart_data["Oct"] == ["31", "5", "15", "11"], "3"
        assert chart_data["Nov"] == ["31", "12", "18"], "4"
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    input_image_path = "data/01.png"
    validate_image(input_image_path)  # По желанию можно убрать.
    chart_dict: dict[str, list] = parse_image(input_image_path)
    pp(chart_dict)
    check_result(chart_dict)


