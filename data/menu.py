# импортируем библиотеки
import pygame
import csv
import os

from cv2 import VideoCapture  # для воспроизвдения заставки покадрово
from datetime import datetime

from data.main_functions import terminate, create_sprite


class Menu:
    def __init__(self, screen, fps, path):
        self.screen, self.size, self.fps = screen, screen.get_size(), fps
        with open(f"{path}\statistic.txt", encoding="utf-8") as statistic:
            self.statistic = dict(map(lambda x: tuple(x.split(': ')), [line for line in list(
                map(lambda x: x.strip('\n'), statistic.readlines())) if line != '' if
                                                                       line[0] != '#']))

    # функция воспроизведения заставки
    def screensaver(self):
        pygame.mixer.init()
        # воспроизводим видео, в соответствии разрешения
        cap = VideoCapture(os.path.join("data", f"screensaver{self.size[0]}x{self.size[1]}.mp4"))
        # т.к видео воспроизводится без звука, мы его добавим вручную
        s = pygame.mixer.Sound(os.path.join("data", "screensaver.wav"))
        running, img = cap.read()  # running — кадры остались? img — изображение
        shape = img.shape[1::-1]
        clock = pygame.time.Clock()
        s.play()  # воспроизводим звук

        while running:
            clock.tick(self.fps)
            running, img = cap.read()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            try:
                self.screen.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
            except AttributeError:
                pass
            pygame.display.update()
        s.stop()

    def menu(self):
        clock = pygame.time.Clock()

        menu_sprites = pygame.sprite.Group()

        title = pygame.sprite.Sprite()
        create_sprite(title, "title.png", 549, 50, menu_sprites)

        play = pygame.sprite.Sprite()
        create_sprite(play, "play.png", 558, 150, menu_sprites)

        with_friend = pygame.sprite.Sprite()
        create_sprite(with_friend, "withfriend.png", 558, 200, menu_sprites)

        with_bot = pygame.sprite.Sprite()
        create_sprite(with_bot, "withbot.png", 683, 200, menu_sprites)

        settings = pygame.sprite.Sprite()
        create_sprite(settings, "settings.png", 50, 250, menu_sprites)

        achievements = pygame.sprite.Sprite()
        create_sprite(achievements, "achievements.png", 50, 500, menu_sprites)

        e = pygame.sprite.Sprite()
        create_sprite(e, "exit.png", 1066, 500, menu_sprites)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play.rect.collidepoint(event.pos):
                        pass
                    elif with_friend.rect.collidepoint(event.pos):
                        pass
                    elif with_bot.rect.collidepoint(event.pos):
                        pass
                    elif settings.rect.collidepoint(event.pos):
                        return 'Settings'
                    elif achievements.rect.collidepoint(event.pos):
                        return 'Achievements'
                    elif e.rect.collidepoint(event.pos):
                        terminate()
            # fon = pygame.transform.scale(load_image('fon.jpg'), self.size)
            self.screen.fill((0, 0, 0))  # self.screen.blit(fon, (0, 0))
            menu_sprites.draw(self.screen)
            self.screen.blit(
                pygame.font.Font(None, 50).render(f"{self.statistic['EX']} EX", True,
                                                  (255, 255, 255)), (0, 0))
            pygame.display.flip()
            clock.tick(self.fps)


class Achievements:
    def __init__(self, screen, fps, path):
        self.screen, self.fps, self.path = screen, fps, path
        with open(os.path.join(path, 'achievements.csv'), encoding='utf8') as file:
            self.achievements = list(
                map(lambda q: [int(q[0]), q[1], q[2], int(q[3]), float(q[4]), q[5], int(q[6]), q[7]],
                    list(csv.reader(file, delimiter=';', quotechar='"'))[1:]))

    def menu(self):
        clock = pygame.time.Clock()

        menu_sprites = pygame.sprite.Group()

        m = pygame.sprite.Sprite()
        create_sprite(m, 'mat_2.png', 0, 0, menu_sprites)

        x = pygame.sprite.Sprite()
        create_sprite(x, 'x.png', 1266, 50, menu_sprites)

        title = pygame.sprite.Sprite()
        create_sprite(title, 'achievements_title.png', 50, 50, menu_sprites)

        a, f = 150, 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if f - 1 >= 0:
                            a, f = a + 175, f - 1
                    elif event.button == 5:
                        if f + 1 < len(self.achievements) - 2:
                            a, f = a - 175, f + 1
                    if x.rect.collidepoint(event.pos):
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if f - 1 >= 0:
                            a, f = a + 175, f - 1
                    elif event.key == pygame.K_DOWN:
                        if f + 1 < len(self.achievements) - 2:
                            a, f = a - 175, f + 1
            self.screen.fill((0, 0, 0))

            y, i = a, 0
            while i < len(self.achievements):
                achievement_sprites = pygame.sprite.Group()

                achievement = self.achievements[i]

                mat = pygame.sprite.Sprite()
                create_sprite(mat, f'mat_{str(achievement[4]).split(".")[0]}.png', 50, y,
                              achievement_sprites)

                frame = pygame.sprite.Sprite()
                create_sprite(frame, f'frame_{achievement[3]}.png', 145, y + 25,
                              achievement_sprites)

                try:
                    image = pygame.sprite.Sprite()
                    create_sprite(image, achievement[7], 150, y + 30, achievement_sprites)
                except TypeError:
                    pass

                achievement_sprites.draw(self.screen)

                for j in [[str(i + 1), (255, 255, 255), 75, y + 25, 75],
                          [achievement[1], (255, 255, 255), 400, y + 25, 75],
                          [achievement[2], (192, 192, 192), 400, y + 100, 25],
                          ["Прогресс", (192, 192, 192), 900, y + 10, 25],
                          [f"{int(achievement[4] * 100)}%", (255, 255, 255), 900, y + 45, 50],
                          ["Награда", (192, 192, 192), 1100, y + 10, 25],
                          [f"{achievement[6]} EX", (255, 255, 255), 1100, y + 45, 50]]:
                    self.screen.blit(pygame.font.Font(None, j[4]).render(j[0], True, j[1]),
                                     (j[2], j[3]))

                y, i = y + 175, i + 1

            menu_sprites.draw(self.screen)

            pygame.display.flip()
            clock.tick(self.fps)

    def add_progress(self, number, i):
        with open(os.path.join(self.path, 'achievements.csv'), encoding='utf8') as file:
            self.achievements = list(
                map(lambda q: [int(q[0]), q[1], q[2], int(q[3]), float(q[4]), q[5], int(q[6]), q[7]],
                    list(csv.reader(file, delimiter=';', quotechar='"'))[1:]))
        i = list(map(lambda x: x[0], self.achievements)).index(i)
        if self.achievements[i][5] == '':
            self.achievements[i][4] += number
            if self.achievements[i][4] == 1.0:
                self.achievements[i][5] = datetime.now().date().strftime('%d.%m.%Y')
                with open(f"{self.path}\statistic.txt", encoding="utf-8") as statistic_for_read:
                    statistic_for_read = list(
                        map(lambda a: a.strip('\n'), statistic_for_read.readlines()))
                with open(f"{self.path}\statistic.txt", 'w',
                          encoding="utf-8") as statistic_for_write:
                    write = []
                    for j in range(len(statistic_for_read)):
                        if statistic_for_read[j].split(': ')[0] == 'EX':
                            n = str(
                                int(statistic_for_read[j].split(': ')[1]) + self.achievements[i][6])
                            write.append(
                                f"EX: {n}")
                        else:
                            write.append(statistic_for_read[j])
                    statistic_for_write.write('\n'.join(write))
            with open(os.path.join(self.path, 'achievements.csv'), 'w', encoding='utf-8') as file:
                write = [
                    'id;name;description;difficulty;progress;date_of_completion;experience;image\n']
                for i in self.achievements:
                    write.append(';'.join(list(map(str, i))))
                write = ''.join(write)
                file.write(write)
