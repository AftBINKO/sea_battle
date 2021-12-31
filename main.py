# импортируем библиотеки
import ctypes.wintypes
import pygame
import csv
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
            if not os.path.isfile(os.path.join(f"{path}\Sea Battle", 'config.txt')):
                file.extract('config.txt', f"{path}\Sea Battle")
            if not os.path.isfile(os.path.join(f"{path}\Sea Battle", 'achievements.csv')):
                file.extract('achievements.csv', f"{path}\Sea Battle")
            if not os.path.isfile(os.path.join(f"{path}\Sea Battle", 'statistic.txt')):
                file.extract('statistic.txt', f"{path}\Sea Battle")

    pygame.init()  # инициализируем pygame
    screen, config, fps = create_window(f"{path}\Sea Battle")
    # menu, settings, achievements = Menu(
    #     screen, fps, f"{path}\Sea Battle"), Settings(
    #     screen, fps, config, f"{path}\Sea Battle"), Achievements(screen, fps, f"{path}\Sea Battle")
    menu = Menu(screen, fps, f"{path}\Sea Battle")
    settings = Settings(screen, fps, config, f"{path}\Sea Battle")
    achievements = Achievements(screen, fps, f"{path}\Sea Battle")
    pygame.mouse.set_visible(False)  # погашаем мышь
    menu.screensaver()  # заставка
    pygame.mouse.set_visible(True)  # показываем мышь
    achievements.add_progress(1, 1)
    while True:
        menu = Menu(screen, fps, f"{path}\Sea Battle")
        result = menu.menu()  # меню
        if result == 'Settings':
            settings.menu()
            if settings:
                screen, config, fps = create_window(f"{path}\Sea Battle")
        elif result == 'Achievements':
            achievements.menu()


if __name__ == '__main__':
    sys.exit(main())
