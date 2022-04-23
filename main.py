# v1.1.1
import ctypes.wintypes
import sys

import requests
import pygame
import os

from datetime import datetime

try:
    from .data.main_functions import create_window, format_xp, extract_files, get_values, \
        set_statistic, get_values_sqlite
    from .data.exceptions import NotAuthorizedError, NotLicensedError, AuthorizationError, \
        NoLauncherRunError
    from .data.achievements import Achievements, Titles
    from .data.menu import Menu, Statistic, Instruction
    from .data.settings import Settings, About
    from .data.play import Play, PlayWithBot
except ImportError:
    from data.main_functions import create_window, format_xp, extract_files, get_values, \
        set_statistic, get_values_sqlite
    from data.exceptions import NotAuthorizedError, NotLicensedError, AuthorizationError, \
        NoLauncherRunError
    from data.achievements import Achievements, Titles
    from data.menu import Menu, Statistic, Instruction
    from data.settings import Settings, About
    from data.play import Play, PlayWithBot


def main(user_data: dict):
    """Запуск игры"""
    # проверим лицензию
    try:
        user_login = user_data["user_login"]
        if user_login is None:
            raise NotAuthorizedError

        login_request = "http://127.0.0.1:5000/" + \
                        f"{user_login['email']}/{user_login['password']}/api/get_data"
        response = requests.get(login_request)
        if not response.json()["user"]["is_activated"]:
            raise NotLicensedError("Купите игру, чтобы играть")
    except NotAuthorizedError as error:
        raise NotAuthorizedError(error)
    except NotLicensedError as error:
        raise NotLicensedError(error)
    except Exception as error:
        raise AuthorizationError(f'Ошибка авторизации: {error.__class__.__name__} "{error}"')

    # получим путь к документам пользователя
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
    path = buf.value

    """Основные переменные"""
    path, archive, cfg, ach, stat = os.path.join(path, "Sea Battle"), os.path.join(
        "data", "files.zip"), "config.json", "achievements.sqlite", "statistic.json"
    path_config, path_achievements, path_statistic = os.path.join(path, cfg), os.path.join(
        path, ach), os.path.join(path, stat)

    if not os.path.isdir(path):
        os.mkdir(path)
        extract_files(archive, path, a=True)
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

    menu, settings, achievements = Menu(screen, fps, path, None), Settings(
        screen, fps, path, user_login), Achievements(screen, fps, path)

    pygame.mouse.set_visible(False)  # погашаем мышь
    menu.screensaver()  # заставка
    pygame.mouse.set_visible(True)  # показываем мышь

    # переменная push означает, получено ли достижение сейчас, чтобы уведомить об этом игрока
    push = achievements.set_progress(1, 1, True)  # достижение за вход в игру

    while True:
        x = menu.get_n()  # сохраним значение x в переменную

        # обновляем достижения, меню и настройки
        menu, settings, achievements = Menu(screen, fps, path, push), Settings(
            screen, fps, path, user_login), Achievements(screen, fps, path)
        push = None  # обнулили
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
            while True:
                titles, result_achievements = Titles(screen, fps, path), achievements.menu()
                if result_achievements is None:
                    break
                elif result_achievements == "titles":
                    while True:
                        if titles.menu() is None:
                            break

        elif result == "Statistic":
            statistic = Statistic(screen, fps, path)
            statistic.menu()

        elif result == "Instruction":
            instruction = Instruction(screen, fps, path)
            instruction.menu()

        elif result == "Play_With_Bot":
            d = ["easiest", "easy", "normal", "hard", "impossible"].index(
                get_values(path_config, "difficulty")[0]) + 1  # получаем сложность
            theme_value = get_values(path_config, "theme")[0]
            PlayWithBot(screen, fps, path, [0, 150, 300, 600, 1200, 10000][d], d,
                        theme_value == "day" or (theme_value == "by_time_of_day" and 8 <= int(
                            datetime.now().time().strftime("%H")) <= 18))

        elif result == "Farm":
            d = ["easiest", "easy", "normal", "hard", "impossible"].index(
                get_values(path_config, "difficulty")[0]) + 1  # получаем сложность
            theme_value = get_values(path_config, "theme")[0]
            PlayWithBot(screen, fps, path, "Farm", d,
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

        elif result == "Titles":
            titles = Titles(screen, fps, path)
            while True:
                if titles.menu() is None:
                    break

        """Установка прогресса для достижений"""
        m = get_values(path_statistic, "mission")[0]
        for i, val in enumerate(["2", "3", "4", "5", "6", "7", "8", "8b", "8a"], start=6):
            if m == val:
                a = achievements.set_progress(1, i)
                if push is None:
                    push = a

        level = format_xp(path_statistic)[1]
        for i, val in enumerate(["25", "50", "75", "100"], start=2):
            a = achievements.set_progress(level / int(val), i)
            if push is None:
                push = a

        games = get_values(path_statistic, "games")[0]
        for i, val in enumerate(["1", "10", "100", "1000", "10000"], start=15):
            a = achievements.set_progress(int(games) / int(val), i)
            if push is None:
                push = a

        victories = get_values(path_statistic, "victories")[0]
        for i, val in enumerate(["1", "10", "50", "100", "1000"], start=20):
            a = achievements.set_progress(int(victories) / int(val), i)
            if push is None:
                push = a

        defeats = get_values(path_statistic, "defeats")[0]
        for i, val in enumerate(["1", "10", "50", "100", "1000"], start=25):
            a = achievements.set_progress(int(defeats) / int(val), i)
            if push is None:
                push = a

        # я уверен, что это работает, но проверить не могу :)
        if int(get_values(path_statistic, "impossible_levels")[0]) >= 1:
            a = achievements.set_progress(1, 30)
            if push is None:
                push = a

        set_statistic(path_statistic, len(get_values_sqlite(
            path_achievements, "achievements", "progress = 1", "id")),
                      key="completed_achievements", add=False)


if __name__ == "__main__":
    # raise NoLauncherRunError("Запустите игру через лаунчер")
    sys.exit(main({
    "config_version": "1.0",
    "user_login": {
        "email": "chuyanov2006@gmail.com",
        "password": "churoma2006"
    },
    "user_data": {
        "biography": "Всемогущий, Великий и Превосходный создатель!",
        "nickname": "AftBINKO"
    }
}))
