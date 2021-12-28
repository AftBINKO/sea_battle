# импортируем библиотеки
from data.menu import Menu
from data.settings import Settings
from data.main_functions import create_window
import pygame
import sys


# основная функция
def main():
    pygame.init()  # инициализируем pygame
    screen, config, fps = create_window()
    menu = Menu(screen, fps)
    pygame.mouse.set_visible(False)  # погашаем мышь
    menu.screensaver()  # заставка
    pygame.mouse.set_visible(True)  # показываем мышь
    while True:
        result = menu.menu()  # меню
        if result == 'Settings':
            settings = Settings(screen, fps, config)
            settings.menu()
            if settings:
                screen, config, fps = create_window()
                menu = Menu(screen, fps)


if __name__ == '__main__':
    sys.exit(main())
