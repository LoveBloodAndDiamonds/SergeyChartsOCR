from PIL import Image


COLORS_DICT = {
    (0, 143, 136): "GREEN",
    (0, 192, 115): "LIGHT_GREEN",
    (255, 220, 72): "YELLOW",
    (255, 163, 62): "ORANGE",
    (255, 51, 58): "RED",
}

# Задаем исходный и целевой цвета
source_rgb = (255, 163, 62)

# На который изменяем
target_rgb = (0, 0, 0)


# Открываем изображение
image = Image.open('../data/01.png')
pixels = image.load()


# Получаем размеры изображения
width, height = image.size

# Проходим по всем пикселям и заменяем цвет
res = 0
for x in range(width):
    for y in range(height):
        r, g, b, a = pixels[x, y]
        if (r, g, b) == source_rgb:
            # print(f"find! {shade}")
            res += 1
            pixels[x, y] = target_rgb

print(res)
# Сохраняем измененное изображение
image.save('../tmp/modified_image.png')
