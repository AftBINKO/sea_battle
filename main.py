# импортируем библиотеки
import ctypes.wintypes
import pygame
import sys
import os

from data.main_functions import create_window, format_xp, extract_files
from data.menu import Menu, Achievements
from data.play import Play, PlayWithFriend, PlayWithBot
from data.settings import Settings


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
    PlayWithBot(screen, fps)
    menu, settings, achievements = Menu(screen, fps, f"{path}\Sea Battle"), Settings(
        screen, fps, config, f"{path}\Sea Battle"), Achievements(screen, fps, f"{path}\Sea Battle")
    # pygame.mouse.set_visible(False)  # погашаем мышь
    # menu.screensaver()  # заставка
    # pygame.mouse.set_visible(True)  # показываем мышь
    achievements.set_progress(1, 1, True)
    while True:
        x = menu.get_n()  # сохраним значение x в переменную
        level = format_xp(f"{path}\Sea Battle\statistic.txt")[1]
        for i, val in enumerate(['25', '50', '75', '100'], start=2):
            achievements.set_progress(level / int(val), i)
        # обновляем достижения, меню и настрйки
        menu, settings, achievements = Menu(screen, fps, f"{path}\Sea Battle"), Settings(
            screen, fps, config, f"{path}\Sea Battle"), Achievements(screen, fps,
                                                                     f"{path}\Sea Battle")
        menu.set_n(x)  # и вставим обратно
        result = menu.menu()  # меню
        if result == 'Settings':
            settings.menu()
            if settings:
                screen, config, fps = create_window(f"{path}\Sea Battle")  # обновляем экран
                continue
        elif result == 'Achievements':
            achievements.menu()
        elif result == 'Play_With_Friend':
            play = PlayWithFriend(screen, fps)
        elif result == 'Play_With_Bot':
            play = PlayWithBot(screen, fps)
        elif result == 'Play':
            play = Play(screen, fps, f"{path}\Sea Battle")
            play.menu()


if __name__ == '__main__':
    sys.exit(main())
