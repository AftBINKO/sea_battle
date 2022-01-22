# импортируем библиотеки
import ctypes.wintypes
import pygame
import sys
import os

from datetime import datetime

from data.main_functions import create_window, format_xp, extract_files, get_value
from data.settings import Settings, About
from data.menu import Menu, Achievements
from data.play import Play, PlayWithBot


# основная функция
def main():
    # получим путь к документам пользователя
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
    path = buf.value

    if not os.path.isdir(f"{path}\Sea Battle"):
        os.mkdir(f"{path}\Sea Battle")
        extract_files(os.path.join("data", "files.zip"), f"{path}\Sea Battle", 'config.txt',
                      'achievements.sqlite', 'statistic.txt')
    else:
        if not os.path.isfile(os.path.join(f"{path}\Sea Battle", 'config.txt')):
            extract_files(os.path.join("data", "files.zip"), f"{path}\Sea Battle", 'config.txt')
        if not os.path.isfile(os.path.join(f"{path}\Sea Battle", 'achievements.sqlite')):
            extract_files(os.path.join("data", "files.zip"), f"{path}\Sea Battle",
                          'achievements.sqlite')
        if not os.path.isfile(os.path.join(f"{path}\Sea Battle", 'statistic.txt')):
            extract_files(os.path.join("data", "files.zip"), f"{path}\Sea Battle", 'statistic.txt')

    pygame.init()  # инициализируем pygame
    screen, config, fps = create_window(f"{path}\Sea Battle")
    menu, settings, achievements = Menu(screen, fps, f"{path}\Sea Battle"), Settings(
        screen, fps, config, f"{path}\Sea Battle"), Achievements(screen, fps, f"{path}\Sea Battle")

    pygame.mouse.set_visible(False)  # погашаем мышь
    menu.screensaver()  # заставка
    pygame.mouse.set_visible(True)  # показываем мышь

    achievements.set_progress(1, 1, True)  # за вход в игру
    while True:
        x = menu.get_n()  # сохраним значение x в переменную

        level = format_xp(f"{path}\Sea Battle\statistic.txt")[1]
        for i, val in enumerate(['25', '50', '75', '100'], start=2):
            achievements.set_progress(level / int(val), i)

        # обновляем достижения, меню и настройки
        menu, settings, achievements = Menu(screen, fps, f"{path}\Sea Battle"), Settings(
            screen, fps, config, f"{path}\Sea Battle"), Achievements(screen, fps,
                                                                     f"{path}\Sea Battle")
        menu.set_n(x)  # и вставим обратно

        result = menu.menu()  # меню
        if result == 'Settings':
            while True:  # цикл был создан для того, чтобы выходить из подменю в меню настройки
                about, result_settings = About(screen, fps, f"{path}\Sea Battle"), settings.menu()
                if result_settings == 'apply':
                    screen, config, fps = create_window(f"{path}\Sea Battle")  # обновляем экран
                    break
                elif result_settings == 'developers':
                    about.menu()
                else:
                    break
        elif result == 'Achievements':
            achievements.menu()
        elif result == 'Play_With_Bot':
            d = ['easiest', 'easy', 'normal', 'hard', 'impossible'].index(
                get_value(f"{path}\Sea Battle\config.txt", 'difficulty')[
                    0]) + 1  # получаем сложность
            theme_value = get_value(f"{path}\Sea Battle\config.txt", 'theme')[0]
            PlayWithBot(screen, fps, f"{path}\Sea Battle",
                        [0, 150, 300, 600, 1200, 10000][d], d, theme_value == 'day' or (
                                theme_value == 'by_time_of_\
day' and 8 <= int(datetime.now().time().strftime('%H')) <= 18))
        elif result == 'Play':
            while True:
                play = Play(screen, fps, f"{path}\Sea Battle")
                theme_value = get_value(f"{path}\Sea Battle\config.txt", 'theme')[0]
                result_play = play.menu()
                if result_play is None:
                    m = get_value(f"{path}\Sea Battle\statistic.txt", 'mission')[0]
                    for i, val in enumerate(['2', '3', '4', '5', '6', '7', '8', '8b', '8a'],
                                            start=6):
                        if m == val:
                            achievements.set_progress(1, i)
                    break
                elif result_play != 'replay':
                    m = get_value(f"{path}\Sea Battle\statistic.txt", 'mission')[0]
                    PlayWithBot(screen, fps, f"{path}\Sea Battle", *result_play,
                                theme_value == 'day' or (
                                        theme_value == 'by_time_of_\
day' and 8 <= int(datetime.now().time().strftime('%H')) <= 18), m, 'Андрей')
                    m = get_value(f"{path}\Sea Battle\statistic.txt", 'mission')[0]
                    for i, val in enumerate(['2', '3', '4', '5', '6', '7', '8', '8b', '8a'],
                                            start=6):
                        if m == val:
                            achievements.set_progress(1, i)
                    break

        games = get_value(f"{path}\Sea Battle\statistic.txt", 'games')[0]
        for i, val in enumerate(['1', '10', '100', '1000', '10000'], start=15):
            achievements.set_progress(int(games) / int(val), i)

        victories = get_value(f"{path}\Sea Battle\statistic.txt", 'victories')[0]
        for i, val in enumerate(['1', '10', '50', '100', '1000'], start=20):
            achievements.set_progress(int(victories) / int(val), i)

        defeats = get_value(f"{path}\Sea Battle\statistic.txt", 'defeats')[0]
        for i, val in enumerate(['1', '10', '50', '100', '1000'], start=25):
            achievements.set_progress(int(defeats) / int(val), i)

        # я уверен, что это работает, но проверить не могу :)
        if int(get_value(f"{path}\Sea Battle\statistic.txt", 'impossible_levels')[0]) >= 1:
            achievements.set_progress(1, 30)


if __name__ == '__main__':
    sys.exit(main())
