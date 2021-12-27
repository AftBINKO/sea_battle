# импортируем библиотеки
import os
from data.menu import Menu
from data.settings import Settings
import pygame
import sys


# основная функция
def main():
    pygame.init()  # инициализируем pygame
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
    menu = Menu(screen, fps)
    # pygame.mouse.set_visible(False)  # погашаем мышь
    # menu.screensaver()  # заставка
    # pygame.mouse.set_visible(True)  # показываем мышь
    while True:
        result = menu.menu()  # меню
        if result == 'Settings':
            settings = Settings(screen, fps, config)
            settings.menu()


if __name__ == '__main__':
    sys.exit(main())
