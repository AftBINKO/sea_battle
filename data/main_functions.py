import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, c=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выдаём ошибку
    if not os.path.isfile(fullname):
        raise FileNotFoundError(f'the file with the image f"{fullname}" was not found')
    image = pygame.image.load(fullname)
    return image


def create_sprite(sprite, name, x, y, group):  # функция помогает быстрее поставить sprite
    sprite.image = load_image(name)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = x
    sprite.rect.y = y
    group.add(sprite)


def create_window(path):
    with open(f"{path}\config.txt", encoding="utf-8") as config:
        config = dict(map(lambda x: tuple(x.split(': ')),
                          [line for line in list(map(lambda x: x.strip('\n'), config.readlines())) if
                           line != '' if line[0] != '#']))
    if config['version'] != '1.1 ALPHA':
        raise ValueError('The configuration file version is not supported')
    size = tuple(map(int, config['screensize'].split('x')))  # размеры экрана пока оставим такими
    screen = None
    if config['screenmode'] == 'window':
        screen = pygame.display.set_mode(size)  # создаём окно
        pygame.display.set_caption('Sea Battle')  # ставим заголовок
    elif config['screenmode'] == 'noframe':
        screen = pygame.display.set_mode(size, pygame.NOFRAME)
    elif config['screenmode'] == 'fullscreen':
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    fps = int(config['fps'])  # ставим количество кадров в секунду
    return screen, config, fps


def add_xp(path, number):
    with open(path, encoding="utf-8") as statistic_for_read:
        statistic_for_read = list(
            map(lambda a: a.strip('\n'), statistic_for_read.readlines()))
    with open(path, 'w', encoding="utf-8") as statistic_for_write:
        write = []
        for i in range(len(statistic_for_read)):
            if statistic_for_read[i].split(': ')[0] == 'XP':
                n = str(int(statistic_for_read[i].split(': ')[1]) + number)
                write.append(f"XP: {n}")
            else:
                write.append(statistic_for_read[i])
        statistic_for_write.write('\n'.join(write))


def format_xp(path):
    with open(path, encoding="utf-8") as statistic_for_read:
        statistic_for_read = list(
            map(lambda a: a.strip('\n'), statistic_for_read.readlines()))
        for statistic in statistic_for_read:
            if statistic.split(': ')[0] == 'XP':
                xp = int(statistic.split(': ')[1])
    level, requirement, x = None, None, xp
    for i in range(100):
        level, requirement = i, 100 * (i + 1)
        if requirement - x > 0:
            return f"""{level} LVL
{x}/{requirement} XP""", level, x, requirement
        x -= requirement
    return f"""100 LVL
{x} XP""", 100, x

