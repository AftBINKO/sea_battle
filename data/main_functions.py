from datetime import datetime
from zipfile import ZipFile

import pygame
import sys
import os


def terminate():
    """Стандартная функция для безопасного выхода"""
    pygame.quit()
    sys.exit()


def load_image(name):
    """Стандартная функция для импорта изображения"""
    return pygame.image.load(os.path.join("data", name))


def put_sprite(sprite, x, y):
    """функция редактирует расположение sprite"""
    sprite.rect.x = x
    sprite.rect.y = y


def create_sprite(sprite, name, x, y, group, transform=None):
    """функция помогает быстрее поставить sprite"""

    image = load_image(name)

    if transform:
        image = pygame.transform.scale(image, transform)

    sprite.image = image
    sprite.rect = sprite.image.get_rect()
    put_sprite(sprite, x, y)
    group.add(sprite)


def add_fon(theme_value, size):
    """Функция ставит фон"""
    return pygame.transform.scale(load_image("fon_2.png"), size) if not (theme_value == "day" or (
            theme_value == "by_time_of_day" and 8 <= int(datetime.now().time().strftime("%H")
                                                         ) <= 18)) else pygame.transform.scale(
        load_image("fon_1.png"), size)


def set_statistic(path, number, value="XP", add=True):
    """Функция устанавливает либо добавляет значение статистики"""
    with open(path, encoding="utf-8") as statistic_for_read:
        statistic_for_read = list(
            map(lambda a: a.strip("\n"), statistic_for_read.readlines()))

    with open(path, "w", encoding="utf-8") as statistic_for_write:
        statistic_for_write.write(
            "\n".join([f"{value}: \
{str(int(statistic_for_read[i].split(': ')[1]) + number) if add else number}" if
                       statistic_for_read[i].split(": ")[0] == value else statistic_for_read[i] for i
                       in range(len(statistic_for_read))]))


def format_xp(path):
    """Функция возвращает отформатированный уровень"""
    with open(path, encoding="utf-8") as statistic_for_read:
        statistic_for_read = list(
            map(lambda a: a.strip("\n"), statistic_for_read.readlines()))

        for statistic in statistic_for_read:
            if statistic.split(": ")[0] == "XP":
                xp = int(statistic.split(": ")[1])

    level, requirement, x = None, None, xp

    for i in range(100):
        level, requirement = i, 100 * (i + 1)

        if requirement - x > 0:
            return f"""{level} LVL
{x}/{requirement} XP""", level, x, requirement
        x -= requirement

    return f"""100 LVL
{x} XP""", 100, x


def get_values(path, *values):
    """Функция получает значения переменной в файле"""
    with open(path, encoding="utf-8") as file:
        file = dict(map(lambda x: tuple(x.split(": ")), [line for line in list(
            map(lambda x: x.strip("\n"), file.readlines())) if line != "" if
                                                         line[0] != "#"]))
        return tuple([file[value] for value in values])


def extract_files(path_archive, path_extract, *values):
    """Функция распаковывает нужные файлы"""
    with ZipFile(path_archive, "r") as archive:
        for file in values:
            archive.extract(file, path_extract)


def create_window(path_config):
    """Функция создаёт окно pygame"""
    version, screensize, screenmode, fps = get_values(path_config, "version", "screensize",
                                                      "screenmode", "fps")

    if version != "1.01":
        raise ValueError("The configuration file version is not supported")

    size, screen = tuple(map(int, screensize.split("x"))), None

    if screenmode == "window":
        screen = pygame.display.set_mode(size)  # создаём окно
        pygame.display.set_caption("Sea Battle")  # ставим заголовок

    elif screenmode == "noframe":
        screen = pygame.display.set_mode(size, pygame.NOFRAME)

    elif screenmode == "fullscreen":
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    pygame.display.set_icon(load_image("SeaBattleIcon.ico"))

    return screen, int(fps)
