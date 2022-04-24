import json
import sqlite3

import requests

from .main_functions import terminate, load_image, create_sprite, get_values, extract_files, \
    add_fon, set_values, get_values_sqlite

import webbrowser
import pygame
import os


class Settings:
    """Настройки"""

    def __init__(self, screen, fps, path, user_login):
        self.email, self.password = user_login["email"], user_login["password"]
        self.path_config = os.path.join(path, "config.json")
        self.path_statistic = os.path.join(path, "statistic.json")
        self.path_achievements = os.path.join(path, "achievements.sqlite")
        self.screen, self.fps, self.path, self.size = screen, fps, path, tuple(
            map(int, (get_values(self.path_config, "screensize")[0].split("x"))))
        self.values_screensize = ["1366x768", "1920x1080"]
        self.values_screenmode = ["window", "noframe", "fullscreen"]
        self.values_fps = [30, 60, 90, 120]
        self.values_difficulty = ["easiest", "easy", "normal", "hard", "impossible"]
        self.values_theme = ["day", "night", "by_time_of_day"]
        self.value_screensize = self.values_screensize.index(
            get_values(self.path_config, "screensize")[0])
        self.value_screenmode = self.values_screenmode.index(
            get_values(self.path_config, "screenmode")[0])
        self.value_fps = self.values_fps.index(
            get_values(self.path_config, "fps")[0])
        self.value_difficulty = self.values_difficulty.index(
            get_values(self.path_config, "difficulty")[0])
        self.value_theme = self.values_theme.index(
            get_values(self.path_config, "theme")[0])

    def apply(self):
        """Действие "Применить\""""
        # with open(self.path_config, encoding="utf-8") as config_for_read:
        #     config_for_read = list(
        #         map(lambda a: a.strip("\n"), config_for_read.readlines()))
        # with open(self.path_config, "w", encoding="utf-8") as config_for_write:
        #     write = []
        #     for i in range(len(config_for_read)):
        #         if config_for_read[i].split(": ")[0] == "screensize":
        #             write.append(f"screensize: {self.values_screensize[self.value_screensize]}")
        #
        #         elif config_for_read[i].split(": ")[0] == "screenmode":
        #             write.append(f"screenmode: {self.values_screenmode[self.value_screenmode]}")
        #
        #         elif config_for_read[i].split(": ")[0] == "fps":
        #             write.append(f"fps: {self.values_fps[self.value_fps]}")
        #
        #         elif config_for_read[i].split(": ")[0] == "difficulty":
        #             write.append(f"difficulty: {self.values_difficulty[self.value_difficulty]}")
        #
        #         elif config_for_read[i].split(": ")[0] == "theme":
        #             write.append(f"theme: {self.values_theme[self.value_theme]}")
        #
        #         else:
        #             write.append(config_for_read[i])
        #
        #     config_for_write.write("\n".join(write))

        values = {
            "screensize": self.values_screensize[self.value_screensize],
            "screenmode": self.values_screenmode[self.value_screenmode],
            "fps": int(self.values_fps[self.value_fps]),
            "difficulty": self.values_difficulty[self.value_difficulty],
            "theme": self.values_theme[self.value_theme]
        }
        set_values(self.path_config, values)

        return "apply"

    def download(self):
        login_request = f"http://seabattle.aft-services.ru/{self.email}/{self.password}/api/get_data"
        try:
            statistic = json.loads(requests.get(login_request).json()["user"]["statistic"])
        except Exception:
            return -1
        s, a = statistic["statistic"], statistic["achievements"]

        stat = {}
        for i in s.keys():
            stat[i] = s[i]
        set_values(self.path_statistic, stat)

        with sqlite3.connect(self.path_achievements) as con:
            cur = con.cursor()
            for i in a.keys():
                u = "UPDATE achievements"
                if a[i]['progress'] is not None:
                    u += f"\nSET progress = {a[i]['progress']}"
                else:
                    u += f"\nSET progress = 0"

                if a[i]['date_of_completion'] is not None:
                    u += f', date_of_completion = "{a[i]["date_of_completion"]}"'
                else:
                    u += f', date_of_completion = NULL'
                u += f"\nWHERE id = {i}"
                cur.execute(u)
            con.commit()

    def load(self):
        with open(self.path_statistic) as stat:
            s = json.load(stat)
        achievements_list = get_values_sqlite(self.path_achievements, "achievements", None, "id",
                                              "progress", "date_of_completion")
        achievements_dict = {}
        for achievement in achievements_list:
            achievements_dict[achievement[0]] = {
                "progress": achievement[1],
                "date_of_completion": achievement[2]
            }

        statistic = json.dumps({
            "statistic": s,
            "achievements": achievements_dict
        }, ensure_ascii=False)

        statistic_response = {
            "email": self.email,
            "password": self.password,
            "statistic": statistic
        }

        statistic_request = "http://seabattle.aft-services.ru/api/edit_statistic"
        try:
            requests.post(statistic_request, data=statistic_response)
        except Exception:
            return -1

    def menu(self):
        """Меню настроек"""
        clock = pygame.time.Clock()
        fon = pygame.transform.scale(load_image("fon_3.png"), self.size)

        settings_sprites = pygame.sprite.Group()

        x = pygame.sprite.Sprite()
        create_sprite(x, "x.png", self.size[0] - 100, 50, settings_sprites)

        mat = pygame.sprite.Sprite()
        create_sprite(mat, f"mat_6_{self.size[1]}.png", 50, 100, settings_sprites)

        apply = pygame.sprite.Sprite()
        create_sprite(apply, "apply.png", self.size[0] - 350, self.size[1] - 150, settings_sprites)

        left_screensize = pygame.sprite.Sprite()
        create_sprite(left_screensize, "left_arrow.png", 450, 200, settings_sprites)
        right_screensize = pygame.sprite.Sprite()
        create_sprite(right_screensize, "right_arrow.png", 900, 200, settings_sprites)

        left_screenmode = pygame.sprite.Sprite()
        create_sprite(left_screenmode, "left_arrow.png", 450, 250, settings_sprites)
        right_screenmode = pygame.sprite.Sprite()
        create_sprite(right_screenmode, "right_arrow.png", 900, 250, settings_sprites)

        left_fps = pygame.sprite.Sprite()
        create_sprite(left_fps, "left_arrow.png", 450, 300, settings_sprites)
        right_fps = pygame.sprite.Sprite()
        create_sprite(right_fps, "right_arrow.png", 900, 300, settings_sprites)

        left_difficulty = pygame.sprite.Sprite()
        create_sprite(left_difficulty, "left_arrow.png", 450, 350, settings_sprites)
        right_difficulty = pygame.sprite.Sprite()
        create_sprite(right_difficulty, "right_arrow.png", 900, 350, settings_sprites)

        left_theme = pygame.sprite.Sprite()
        create_sprite(left_theme, "left_arrow.png", 450, 400, settings_sprites)
        right_theme = pygame.sprite.Sprite()
        create_sprite(right_theme, "right_arrow.png", 900, 400, settings_sprites)

        download = pygame.sprite.Sprite()
        create_sprite(download, "download.png", self.size[0] - 350, 150, settings_sprites)

        load = pygame.sprite.Sprite()
        create_sprite(load, "load.png", self.size[0] - 220, 150, settings_sprites)

        developers = pygame.sprite.Sprite()
        create_sprite(developers, "developers.png", self.size[0] - 350, self.size[1] - 250,
                      settings_sprites)

        danger_zone = pygame.sprite.Sprite()
        create_sprite(danger_zone, "danger_zone.png", 100, self.size[1] - 300, settings_sprites)

        recovery_settings = pygame.sprite.Sprite()
        create_sprite(recovery_settings, "recovery_settings.png", 225, self.size[1] - 175,
                      settings_sprites)

        new_game = pygame.sprite.Sprite()
        create_sprite(new_game, "new_game.png", 525, self.size[1] - 175,
                      settings_sprites)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if x.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            return

                        elif left_screensize.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            if self.value_screensize > 0:
                                self.value_screensize -= 1

                            else:
                                self.value_screensize = len(self.values_screensize) - 1

                        elif right_screensize.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            if self.value_screensize < len(self.values_screensize) - 1:
                                self.value_screensize += 1

                            else:
                                self.value_screensize = 0

                        elif left_screenmode.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            if self.value_screenmode > 0:
                                self.value_screenmode -= 1

                            else:
                                self.value_screenmode = len(self.values_screenmode) - 1

                        elif right_screenmode.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            if self.value_screenmode < len(self.values_screenmode) - 1:
                                self.value_screenmode += 1

                            else:
                                self.value_screenmode = 0

                        elif left_fps.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            if self.value_fps > 0:
                                self.value_fps -= 1

                            else:
                                self.value_fps = len(self.values_fps) - 1

                        elif right_fps.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            if self.value_fps < len(self.values_fps) - 1:
                                self.value_fps += 1

                            else:
                                self.value_fps = 0

                        elif left_difficulty.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            if self.value_difficulty > 0:
                                self.value_difficulty -= 1

                            else:
                                self.value_difficulty = len(self.values_difficulty) - 1

                        elif right_difficulty.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            if self.value_difficulty < len(self.values_difficulty) - 1:
                                self.value_difficulty += 1

                            else:
                                self.value_difficulty = 0

                        elif left_theme.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            if self.value_theme > 0:
                                self.value_theme -= 1

                            else:
                                self.value_theme = len(self.values_theme) - 1

                        elif right_theme.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            if self.value_theme < len(self.values_theme) - 1:
                                self.value_theme += 1

                            else:
                                self.value_theme = 0

                        elif download.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            self.download()

                        elif load.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            self.load()

                        elif developers.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            return "developers"

                        elif apply.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            return self.apply()

                    elif event.button == 3:
                        result, values = False, None
                        if recovery_settings.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            result, values = True, ["config.json"]

                        elif new_game.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            result, values = True, ["statistic.json", "achievements.sqlite"]

                        if result:
                            extract_files(os.path.join("data", "files.zip"), self.path, *values)
                            terminate()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                        return

                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                        return self.apply()

            self.screen.blit(fon, (0, 0))

            settings_sprites.draw(self.screen)

            for i in [["Настройки", (255, 255, 255), 50, 50, 50, 1],
                      [f"Версия конфигурационного файла: \
{get_values(self.path_config, 'version')[0]}",
                       (128, 128, 128), 100, 150, 25, 2],
                      ["Размер экрана: ", (255, 255, 255), 100, 200, 50, 1],
                      [self.values_screensize[self.value_screensize], (255, 255, 255), 500, 200, 50,
                       2], ["Режим экрана: ", (255, 255, 255), 100, 250, 50, 1],
                      [self.values_screenmode[self.value_screenmode], (255, 255, 255), 500, 250, 50,
                       2], ["FPS: ", (255, 255, 255), 100, 300, 50, 1],
                      [str(self.values_fps[self.value_fps]), (255, 255, 255), 500, 300, 50, 2],
                      ["Сложность: ", (255, 255, 255), 100, 350, 50, 1],
                      [self.values_difficulty[self.value_difficulty], (255, 255, 255), 500, 350, 50,
                       2], ["Тема: ", (255, 255, 255), 100, 405, 50, 1],
                      [self.values_theme[self.value_theme], (255, 255, 255), 500, 400, 50, 2]]:
                self.screen.blit(
                    pygame.font.Font(os.path.join("data", f"font_{str(i[5])}.ttf"), i[4]).render(
                        i[0], True, i[1]), (i[2], i[3]))

            pygame.display.flip()
            clock.tick(self.fps)


class About:
    """Титры"""

    def __init__(self, screen, fps, path_config):
        self.screen, self.fps, self.size, self.update, self.path_config = screen, fps, tuple(
            map(int, (get_values(
                path_config, "screensize")[0].split("x")))), pygame.USEREVENT + 1, path_config

    def menu(self):
        """Меню с информацией"""
        fon = add_fon(get_values(self.path_config, "theme")[0], self.size)

        clock = pygame.time.Clock()

        about_sprites = pygame.sprite.Group()

        x = pygame.sprite.Sprite()
        create_sprite(x, "x.png", self.size[0] - 100, 50, about_sprites)

        with open(os.path.join("data", "titles.txt"), encoding="utf-8") as titles:
            titles = titles.read().split("\n")

        mat = pygame.sprite.Sprite()
        create_sprite(mat, f"mat_6_{self.size[1]}.png", 50, 100, about_sprites)

        discord = pygame.sprite.Sprite()
        create_sprite(discord, "discord.png", 300, 150, about_sprites)

        vk = pygame.sprite.Sprite()
        create_sprite(vk, "vk.png", 375, 150, about_sprites)

        youtube = pygame.sprite.Sprite()
        create_sprite(youtube, "youtube.png", 450, 150, about_sprites)

        pygame_sprite = pygame.sprite.Sprite()
        create_sprite(pygame_sprite, "pygame.png", self.size[0] - 200, self.size[1] - 100,
                      about_sprites)

        yandex = pygame.sprite.Sprite()
        create_sprite(yandex, "yandex.png", self.size[0] - 450, self.size[1] - 100, about_sprites)

        pygame.time.set_timer(self.update, 200)
        n = 1

        aft_games = pygame.sprite.Sprite()
        create_sprite(aft_games, os.path.join("animate", f"animate_{n}.png"), 100, 150,
                      about_sprites)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                elif event.type == self.update:
                    if n >= 5:
                        pygame.time.set_timer(self.update, 0)

                    else:
                        n += 1
                        aft_games.image = load_image(os.path.join("animate", f"animate_{n}.png"))

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if x.rect.collidepoint(event.pos):
                        pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                        return

                    else:
                        link = None
                        if discord.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            link = "https://discord.gg/6BaXEbkJkw"

                        elif vk.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            link = "https://vk.com/c_aft"

                        elif youtube.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            link = "https://www.youtube.com/c/BINKO_aft"

                        elif yandex.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            link = "https://yandex.ru"

                        elif pygame_sprite.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            link = "https://www.pygame.org"

                        try:
                            webbrowser.open(link, new=0)
                        except TypeError:
                            pass

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.screen.blit(fon, (0, 0))

            about_sprites.draw(self.screen)

            c, y = 20 if self.size[1] == 768 else 30, 250
            for line in titles:
                count = 1
                for symbol in line:
                    if symbol == "#":
                        count += 1
                    else:
                        break
                text = pygame.font.Font(os.path.join("data", "font_2.ttf"), c * count).render(
                    line.lstrip("#" * (count - 1) + " "), True, (255, 255, 255))
                self.screen.blit(text, text.get_rect(center=(self.size[0] // 2, y)))
                y += c

            self.screen.blit(
                pygame.font.Font(os.path.join("data", f"font_1.ttf"), 50).render(
                    "Разработчики", True, (255, 255, 255)), (50, 50))

            pygame.display.flip()
            clock.tick(self.fps)
