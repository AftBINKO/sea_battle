# 1.0.1
import ctypes.wintypes
import pygame
import sys
import os

from datetime import datetime

from data.main_functions import create_window, format_xp, extract_files, get_values
from data.settings import Settings, About
from data.menu import Menu, Achievements
from data.play import Play, PlayWithBot


def main():
    """Запуск игры"""
    # получим путь к документам пользователя
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
    path = buf.value

    """Основные переменные"""
    path, archive, cfg, ach, stat = os.path.join(path, "Sea Battle"), os.path.join(
        "data", "files.zip"), "config.txt", "achievements.sqlite", "statistic.txt"
    path_config, path_achievements, path_statistic = os.path.join(path, cfg), os.path.join(
        path, ach), os.path.join(path, stat)

    if not os.path.isdir(path):
        os.mkdir(path)
        extract_files(archive, path, cfg, ach, stat)
    else:
        if not os.path.isfile(path_config):
            extract_files(archive, path, cfg)
        if not os.path.isfile(path_achievements):
            extract_files(archive, path, ach)
        if not os.path.isfile(path_statistic):
            extract_files(archive, path, stat)

    """Инициализация"""
    pygame.init()
    pygame.mixer.init()

    screen, fps = create_window(path_config)  # создаём окно

    menu, settings, achievements = Menu(screen, fps, path), Settings(
        screen, fps, path), Achievements(screen, fps, path)

    pygame.mouse.set_visible(False)  # погашаем мышь
    menu.screensaver()  # заставка
    pygame.mouse.set_visible(True)  # показываем мышь

    achievements.set_progress(1, 1, True)  # достижение за вход в игру

    while True:
        x = menu.get_n()  # сохраним значение x в переменную

        # обновляем достижения, меню и настройки
        menu, settings, achievements = Menu(screen, fps, path), Settings(
            screen, fps, path), Achievements(screen, fps, path)
        menu.set_n(x)  # и вставим обратно

        result = menu.menu()  # меню

        if result == "Settings":
            while True:  # цикл был создан для того, чтобы выходить из подменю в меню настройки
                about, result_settings = About(screen, fps, path_config), settings.menu()
                if result_settings == "apply":
                    screen, fps = create_window(path_config)  # обновляем экран
                    break
                elif result_settings == "developers":
                    about.menu()
                else:
                    break

        elif result == "Achievements":
            achievements.menu()

        elif result == "Play_With_Bot":
            d = ["easiest", "easy", "normal", "hard", "impossible"].index(
                get_values(path_config, "difficulty")[0]) + 1  # получаем сложность
            theme_value = get_values(path_config, "theme")[0]
            PlayWithBot(screen, fps, path, [0, 150, 300, 600, 1200, 10000][d], d,
                        theme_value == "day" or (theme_value == "by_time_of_day" and 8 <= int(
                            datetime.now().time().strftime("%H")) <= 18))

        elif result == "Play":
            while True:
                play = Play(screen, fps, path)
                theme_value = get_values(path_config, "theme")[0]
                result_play = play.menu()
                if result_play is None:
                    break
                elif result_play != "replay":
                    PlayWithBot(screen, fps, path, *result_play,
                                theme_value == "day" or (
                                        theme_value == "\
by_time_of_day" and 8 <= int(datetime.now().time().strftime("%H")) <= 18),
                                get_values(path_statistic, "mission")[0], "Андрей")
                    break

        """Установка прогресса для достижений"""
        m = get_values(path_statistic, "mission")[0]
        for i, val in enumerate(["2", "3", "4", "5", "6", "7", "8", "8b", "8a"], start=6):
            if m == val:
                achievements.set_progress(1, i)

        level = format_xp(path_statistic)[1]
        for i, val in enumerate(["25", "50", "75", "100"], start=2):
            achievements.set_progress(level / int(val), i)

        games = get_values(path_statistic, "games")[0]
        for i, val in enumerate(["1", "10", "100", "1000", "10000"], start=15):
            achievements.set_progress(int(games) / int(val), i)

        victories = get_values(path_statistic, "victories")[0]
        for i, val in enumerate(["1", "10", "50", "100", "1000"], start=20):
            achievements.set_progress(int(victories) / int(val), i)

        defeats = get_values(path_statistic, "defeats")[0]
        for i, val in enumerate(["1", "10", "50", "100", "1000"], start=25):
            achievements.set_progress(int(defeats) / int(val), i)

        # я уверен, что это работает, но проверить не могу :)
        if int(get_values(path_statistic, "impossible_levels")[0]) >= 1:
            achievements.set_progress(1, 30)


if __name__ == "__main__":
    sys.exit(main())
