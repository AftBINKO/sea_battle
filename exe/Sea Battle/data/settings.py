from data.main_functions import terminate, load_image, create_sprite, get_value, extract_files, \
    add_fon

import webbrowser
import pygame
import os


class Settings:
    def __init__(self, screen, fps, config, path):
        self.screen, self.fps, self.path, self.size, self.config = screen, fps, path, tuple(
            map(int, (get_value(f"{path}\config.txt", "screensize")[0].split('x')))), config
        self.values_screensize = ['1366x768', '1920x1080']
        self.values_screenmode = ['window', 'noframe', 'fullscreen']
        self.values_fps = ['30', '60', '90', '120']
        self.values_difficulty = ['easiest', 'easy', 'normal', 'hard', 'hardest']
        self.values_theme = ['day', 'night', 'by_time_of_day']
        self.value_screensize = self.values_screensize.index(config['screensize'])
        self.value_screenmode = self.values_screenmode.index(config['screenmode'])
        self.value_fps = self.values_fps.index(config['fps'])
        self.value_difficulty = self.values_difficulty.index(config['difficulty'])
        self.value_theme = self.values_theme.index(config['theme'])

    def apply(self):
        with open(f"{self.path}\config.txt", encoding="utf-8") as config_for_read:
            config_for_read = list(
                map(lambda a: a.strip('\n'), config_for_read.readlines()))
        with open(f"{self.path}\config.txt", 'w',
                  encoding="utf-8") as config_for_write:
            write = []
            for i in range(len(config_for_read)):
                if config_for_read[i].split(': ')[0] == 'screensize':
                    write.append(f'screensize: {self.values_screensize[self.value_screensize]}')
                elif config_for_read[i].split(': ')[0] == 'screenmode':
                    write.append(f'screenmode: {self.values_screenmode[self.value_screenmode]}')
                elif config_for_read[i].split(': ')[0] == 'fps':
                    write.append(f'fps: {self.values_fps[self.value_fps]}')
                elif config_for_read[i].split(': ')[0] == 'difficulty':
                    write.append(f'difficulty: {self.values_difficulty[self.value_difficulty]}')
                elif config_for_read[i].split(': ')[0] == 'theme':
                    write.append(f'theme: {self.values_theme[self.value_theme]}')
                else:
                    write.append(config_for_read[i])
            config_for_write.write('\n'.join(write))
        return 'apply'

    def menu(self):
        clock = pygame.time.Clock()
        fon = pygame.transform.scale(load_image('fon_3.png'), self.size)

        settings_sprites = pygame.sprite.Group()

        x = pygame.sprite.Sprite()
        create_sprite(x, 'x.png', self.size[0] - 100, 50, settings_sprites)

        mat = pygame.sprite.Sprite()
        create_sprite(mat, f'mat_6_{self.size[1]}.png', 50, 100, settings_sprites)

        apply = pygame.sprite.Sprite()
        create_sprite(apply, 'apply.png', self.size[0] - 350, self.size[1] - 150, settings_sprites)

        title = pygame.sprite.Sprite()
        create_sprite(title, 'settings_title.png', 50, 50, settings_sprites)

        left_screensize = pygame.sprite.Sprite()
        create_sprite(left_screensize, 'left_arrow.png', 450, 200, settings_sprites)
        right_screensize = pygame.sprite.Sprite()
        create_sprite(right_screensize, 'right_arrow.png', 900, 200, settings_sprites)

        left_screenmode = pygame.sprite.Sprite()
        create_sprite(left_screenmode, 'left_arrow.png', 450, 250, settings_sprites)
        right_screenmode = pygame.sprite.Sprite()
        create_sprite(right_screenmode, 'right_arrow.png', 900, 250, settings_sprites)

        left_fps = pygame.sprite.Sprite()
        create_sprite(left_fps, 'left_arrow.png', 450, 300, settings_sprites)
        right_fps = pygame.sprite.Sprite()
        create_sprite(right_fps, 'right_arrow.png', 900, 300, settings_sprites)

        left_difficulty = pygame.sprite.Sprite()
        create_sprite(left_difficulty, 'left_arrow.png', 450, 350, settings_sprites)
        right_difficulty = pygame.sprite.Sprite()
        create_sprite(right_difficulty, 'right_arrow.png', 900, 350, settings_sprites)

        left_theme = pygame.sprite.Sprite()
        create_sprite(left_theme, 'left_arrow.png', 450, 400, settings_sprites)
        right_theme = pygame.sprite.Sprite()
        create_sprite(right_theme, 'right_arrow.png', 900, 400, settings_sprites)

        developers = pygame.sprite.Sprite()
        create_sprite(developers, 'developers.png', self.size[0] - 350, self.size[1] - 250,
                      settings_sprites)

        danger_zone = pygame.sprite.Sprite()
        create_sprite(danger_zone, 'danger_zone.png', 100, self.size[1] - 300, settings_sprites)

        recovery_settings = pygame.sprite.Sprite()
        create_sprite(recovery_settings, 'recovery_settings.png', 225, self.size[1] - 175,
                      settings_sprites)

        new_game = pygame.sprite.Sprite()
        create_sprite(new_game, 'new_game.png', 525, self.size[1] - 175,
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
                        elif developers.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            return 'developers'
                        elif apply.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            return self.apply()
                    elif event.button == 3:
                        result, values = False, None
                        if recovery_settings.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            result, values = True, ['config.txt']
                        elif new_game.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            result, values = True, ['statistic.txt', 'achievements.sqlite']
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

            for i in [[f"Версия конфигурационного файла: {self.config['version']}",
                       (128, 128, 128), 100, 150, 25, 2],
                      ["Размер экрана: ", (255, 255, 255), 100, 200, 50, 1],
                      [self.values_screensize[self.value_screensize], (255, 255, 255), 500, 200, 50,
                       2], ["Режим экрана: ", (255, 255, 255), 100, 250, 50, 1],
                      [self.values_screenmode[self.value_screenmode], (255, 255, 255), 500, 250, 50,
                       2], ["FPS: ", (255, 255, 255), 100, 300, 50, 1],
                      [self.values_fps[self.value_fps], (255, 255, 255), 500, 300, 50, 2],
                      ["Сложность: ", (255, 255, 255), 100, 350, 50, 1],
                      [self.values_difficulty[self.value_difficulty], (255, 255, 255), 500, 350, 50,
                       2], ['Тема: ', (255, 255, 255), 100, 405, 50, 1],
                      [self.values_theme[self.value_theme], (255, 255, 255), 500, 400, 50, 2]]:
                self.screen.blit(
                    pygame.font.Font(os.path.join("data", f'font_{str(i[5])}.ttf'), i[4]).render(
                        i[0], True, i[1]), (i[2], i[3]))

            pygame.display.flip()
            clock.tick(self.fps)


class About:
    def __init__(self, screen, fps, path):
        self.screen, self.fps, self.size, self.update, self.path = screen, fps, tuple(map(int,
                                                                                          (get_value(
                                                                                              f"\
{path}\config.txt", "screensize")[0].split('x')))), pygame.USEREVENT + 1, path

    def menu(self):
        fon = add_fon(get_value(f"{self.path}\config.txt", 'theme')[0], self.size)

        clock = pygame.time.Clock()

        about_sprites = pygame.sprite.Group()

        x = pygame.sprite.Sprite()
        create_sprite(x, 'x.png', self.size[0] - 100, 50, about_sprites)

        with open(os.path.join("data", 'titles.txt'), encoding='utf-8') as titles:
            titles = titles.read().split('\n')

        title = pygame.sprite.Sprite()
        create_sprite(title, 'about_title.png', 50, 50, about_sprites)

        mat = pygame.sprite.Sprite()
        create_sprite(mat, f'mat_6_{self.size[1]}.png', 50, 100, about_sprites)

        discord = pygame.sprite.Sprite()
        create_sprite(discord, 'discord.png', 300, 150, about_sprites)

        vk = pygame.sprite.Sprite()
        create_sprite(vk, 'vk.png', 375, 150, about_sprites)

        youtube = pygame.sprite.Sprite()
        create_sprite(youtube, 'youtube.png', 450, 150, about_sprites)

        pygame_sprite = pygame.sprite.Sprite()
        create_sprite(pygame_sprite, 'pygame.png', self.size[0] - 200, self.size[1] - 100,
                      about_sprites)

        yandex = pygame.sprite.Sprite()
        create_sprite(yandex, 'yandex.png', self.size[0] - 450, self.size[1] - 100, about_sprites)

        pygame.time.set_timer(self.update, 200)
        n = 1

        aft_games = pygame.sprite.Sprite()
        create_sprite(aft_games, os.path.join('animate', f'animate_{n}.png'), 100, 150,
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
                        aft_games.image = load_image(os.path.join('animate', f'animate_{n}.png'))
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if x.rect.collidepoint(event.pos):
                        pygame.mixer.Sound(os.path.join("data", "click.ogg")).play()
                        return
                    else:
                        link = None
                        if discord.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            link = 'https://discord.gg/6BaXEbkJkw'
                        elif vk.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            link = 'https://vk.com/c_aft'
                        elif youtube.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            link = 'https://www.youtube.com/c/BINKO_aft'
                        elif yandex.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            link = 'https://yandex.ru'
                        elif pygame_sprite.rect.collidepoint(event.pos):
                            pygame.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                            link = 'https://www.pygame.org'
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
                    if symbol == '#':
                        count += 1
                    else:
                        break
                text = pygame.font.Font(os.path.join("data", 'font_2.ttf'), c * count).render(
                    line.lstrip('#' * (count - 1) + ' '), True, (255, 255, 255))
                self.screen.blit(text, text.get_rect(center=(self.size[0] // 2, y)))
                y += c

            pygame.display.flip()
            clock.tick(self.fps)
