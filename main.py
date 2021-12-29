# импортируем библиотеки
import ctypes.wintypes
import pygame
import sys
import os

from zipfile import ZipFile

from data.menu import Menu, Achievements
from data.settings import Settings
from data.main_functions import create_window


# основная функция
def main():
    # получим путь к документам пользователя
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
    path = buf.value

    with ZipFile(os.path.join("data", "files.zip"), 'r') as file:
        if not os.path.isdir(f"{path}\Sea Battle"):
            os.mkdir(f"{path}\Sea Battle")
            file.extractall(f"{path}\Sea Battle")
        else:
            if not os.path.isfile(f"{path}\Sea Battle\config.txt"):
                file.extract('config.txt', f"{path}\Sea Battle")
            if not os.path.isfile(f"{path}\Sea Battle\achievements.sqlite"):
                file.extract('achievements.sqlite', f"{path}\Sea Battle")

    pygame.init()  # инициализируем pygame
    screen, config, fps = create_window(f"{path}\Sea Battle")
    menu = Menu(screen, fps)
    # pygame.mouse.set_visible(False)  # погашаем мышь
    # menu.screensaver()  # заставка
    # pygame.mouse.set_visible(True)  # показываем мышь
    while True:
        result = menu.menu()  # меню
        if result == 'Settings':
            settings = Settings(screen, fps, config, f"{path}\Sea Battle")
            settings.menu()
            if settings:
                screen, config, fps = create_window(f"{path}\Sea Battle")
                menu = Menu(screen, fps)
        elif result == 'Achievements':
            achievements = Achievements(screen, fps, f"{path}\Sea Battle")
            achievements.menu()


if __name__ == '__main__':
    sys.exit(main())
