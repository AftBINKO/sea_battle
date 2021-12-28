import os
import sys
import pygame


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, c=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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


def create_window():
    with open(os.path.join("data", "config.txt"), encoding="utf-8") as config:
        config = dict(map(lambda x: tuple(x.split(': ')),
                          [line for line in list(map(lambda x: x.strip('\n'), config.readlines())) if
                           line != '' if line[0] != '#']))
    if config['version'] != '1.0 ALPHA':
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
