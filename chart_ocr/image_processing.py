from PIL import Image, ImageEnhance, ImageFilter

from .settings import REPLACING_PIXELS_BOUNDAREA, IMAGE_SCALE_FACTOR, CONTRAST_FACTOR, PIXELS_TRIM_FROM_LEFT, \
    TMP_FOLDER_PATH, GREEN


def split_image_to_parts(image: Image) -> list[str]:
    """
    Разделяет изображение на 4 части, каждый из которых содержит свой столбец
    на графике.
    :param image:
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

        part_image_path = f'{TMP_FOLDER_PATH}/part_{i}.png'
        part_image.save(part_image_path)

        path_list.append(part_image_path)

    return path_list


def trim_image(image: Image) -> Image:
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

    # Замена белых пикселей на синие
    # pixels = image.load()  # Получение доступа к пикселям изображения
    # for y in range(image.size[1]):  # Высота изображения
    #     for x in range(image.size[0]):  # Ширина изображения
    #         r, g, b, a = pixels[x, y]
    #         # Проверить, является ли пиксель белым
    #         if all([r > REPLACING_PIXELS_BOUNDAREA, g > REPLACING_PIXELS_BOUNDAREA, b > REPLACING_PIXELS_BOUNDAREA]):
    #             # Заменить цвет пикселя на синий и установить полную непрозрачность
    #             pixels[x, y] = (0, 0, 0, 255)  # pixels[x, y] = (0, 0, 255, 255)
    #         if (r, g, b) == GREEN:
    #             pixels[x, y] = (255, 0, 0, 255)

    # Увеличение контрастности
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(CONTRAST_FACTOR)

    return image


# Так же может понадобиться:

# Конвертация в черно-белое
# image = image.convert('L')

# Инверсия цветов
# image = ImageOps.invert(image)

# Удаление шума
# image = image.filter(ImageFilter.MedianFilter())