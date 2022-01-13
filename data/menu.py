# импортируем библиотеки
import sqlite3
import pygame
import os

from cv2 import VideoCapture  # для воспроизвдения заставки покадрово
from datetime import datetime, date

from data.main_functions import terminate, create_sprite, add_xp, format_xp, get_value


class Menu:
    def __init__(self, screen, fps, path):
        self.screen, self.fps, self.path, self.size, self.n = screen, fps, path, tuple(
            map(int, (get_value(f"{path}\config.txt", "screensize")[0].split('x')))), 0

    # функция воспроизведения заставки
    def screensaver(self):
        pygame.mixer.init()
        # воспроизводим видео, в соответствии разрешения
        cap = VideoCapture(os.path.join("data", f"screensaver{self.size[1]}.mp4"))
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
        buttons_tuple = ('Play', 'Play_With_Friend', 'Play_With_Bot', 'Settings', 'Achievements')

        clock = pygame.time.Clock()

        menu_sprites = pygame.sprite.Group()

        title = pygame.sprite.Sprite()
        create_sprite(title, "title.png", 50, 200 if self.size[1] == 768 else 300, menu_sprites)

        mat = pygame.sprite.Sprite()
        create_sprite(mat, f"mat_{self.size[1]}.png", 0,
                      self.size[1] - (200 if self.size[1] == 768 else 300), menu_sprites)

        x = 300 * self.n
        left, right = False, False

        while True:
            buttons_sprites = pygame.sprite.Group()

            if right:
                if x < (300 * self.n) - 1:
                    x += 50
                else:
                    x += 1  # корректировка
                    right = False
            if left:
                if x > (300 * self.n) + 1:
                    x -= 50
                else:
                    x -= 1
                    left = False

            buttons = pygame.sprite.Sprite()
            create_sprite(buttons, "buttons.png", self.size[0] / 2 - 125 - x,
                          self.size[1] - (200 if self.size[1] == 768 else 300), buttons_sprites)

            frame = pygame.sprite.Sprite()
            create_sprite(frame, "frame_6.png", self.size[0] / 2 - 125,
                          self.size[1] - (200 if self.size[1] == 768 else 300), buttons_sprites)

            arrows_sprites = pygame.sprite.Group()

            down_arrow = pygame.sprite.Sprite()
            create_sprite(down_arrow, "down_arrow.png", self.size[0] / 2 - 25,
                          self.size[1] - (250 if self.size[1] == 768 else 350), arrows_sprites)

            left_arrow = pygame.sprite.Sprite()
            if self.n - 1 >= 0:
                create_sprite(left_arrow, "left_arrow.png", self.size[0] / 2 - 175,
                              self.size[1] - (200 if self.size[1] == 768 else 300), arrows_sprites)

            right_arrow = pygame.sprite.Sprite()
            if self.n + 1 <= 5:
                create_sprite(right_arrow, "right_arrow.png", self.size[0] / 2 + 125,
                              self.size[1] - (200 if self.size[1] == 768 else 300), arrows_sprites)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    try:
                        if left_arrow.rect.collidepoint(event.pos):
                            x = 300 * self.n + 1
                            left = True
                            self.n -= 1
                    except AttributeError:
                        pass
                    try:
                        if right_arrow.rect.collidepoint(event.pos):
                            x = 300 * self.n - 1
                            right = True
                            self.n += 1
                    except AttributeError:
                        pass
                    if frame.rect.collidepoint(event.pos):
                        if self.n == 5:
                            terminate()
                        return buttons_tuple[self.n]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.n - 1 >= 0:
                        x = 300 * self.n + 1
                        left = True
                        self.n -= 1
                    elif event.key == pygame.K_RIGHT and self.n + 1 <= 5:
                        x = 300 * self.n - 1
                        right = True
                        self.n += 1
                    elif event.key == pygame.K_RETURN:
                        if self.n == 5:
                            terminate()
                        return buttons_tuple[self.n]

            # fon = pygame.transform.scale(load_image('fon.jpg'), self.size)
            self.screen.fill((0, 0, 0))  # self.screen.blit(fon, (0, 0))

            buttons_sprites.draw(self.screen)
            menu_sprites.draw(self.screen)
            arrows_sprites.draw(self.screen)

            text = format_xp(f"{self.path}/statistic.txt")[0].split('\n')
            y = 0
            for line in text:
                self.screen.blit(pygame.font.Font(None, 50).render(line, True, (255, 255, 255)),
                                 (0, y))
                y += 50

            pygame.display.flip()
            clock.tick(self.fps)

    def set_n(self, n):
        self.n = n

    def get_n(self):
        return self.n


class Achievements:
    def __init__(self, screen, fps, path):
        self.screen, self.fps, self.path, self.size = screen, fps, path, tuple(
            map(int, (get_value(f"{path}\config.txt", "screensize")[0].split('x'))))
        with sqlite3.connect(os.path.join(self.path, 'achievements.sqlite')) as con:
            cur = con.cursor()

            # эти строки сортируют сначала по описанию, потом по заголовку, id, опыту, дате,
            # если имеется, сложности и наконец, по проценту выполнения
            s = sorted(sorted(sorted(
                sorted(cur.execute("""SELECT * FROM achievements""").fetchall(), key=lambda x: x[2]),
                key=lambda x: x[1]), key=lambda x: int(x[0])), key=lambda x: int(x[6]), reverse=True)
            try:
                s = sorted(s, key=lambda x: date(int(x[5].split('.')[2]), int(x[5].split('.')[1]),
                                                 int(x[5].split('.')[0])))
            except AttributeError:
                pass
            self.achievements = sorted(sorted(s, key=lambda x: int(x[3]), reverse=True),
                                       key=lambda x: float(x[4]), reverse=True)

    def menu(self):
        clock = pygame.time.Clock()

        menu_sprites = pygame.sprite.Group()

        m = pygame.sprite.Sprite()
        create_sprite(m, f'mat_2_{self.size[1]}.png', 0, 0, menu_sprites)

        x = pygame.sprite.Sprite()
        create_sprite(x, 'x.png', self.size[0] - 100, 50, menu_sprites)

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
                        if f + 1 < len(self.achievements) - (2 if self.size[1] == 768 else 5):
                            a, f = a - 175, f + 1
                    if x.rect.collidepoint(event.pos):
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if f - 1 >= 0:
                            a, f = a + 175, f - 1
                    elif event.key == pygame.K_DOWN:
                        if f + 1 < len(self.achievements) - (2 if self.size[1] == 768 else 5):
                            a, f = a - 175, f + 1
                    elif event.key == pygame.K_ESCAPE:
                        return
            self.screen.fill((0, 0, 0))

            y = a
            for i in range(len(self.achievements)):
                achievement_sprites = pygame.sprite.Group()

                achievement = self.achievements[i]

                mat = pygame.sprite.Sprite()
                create_sprite(mat, f'mat_{str(achievement[4]).split(".")[0]}_{self.size[1]}.png', 50,
                              y,
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
                          ["Прогресс", (192, 192, 192), 1000 if self.size[1] == 768 else 1100,
                           y + 10, 25],
                          [f"{int(achievement[4] * 100)}%", (255, 255, 255),
                           1000 if self.size[1] == 768 else 1100, y + 45, 50],
                          ["Награда", (192, 192, 192), 1150 if self.size[1] == 768 else 1500, y + 10,
                           25],
                          [f"{achievement[6]} XP", (255, 255, 255),
                           1150 if self.size[1] == 768 else 1500, y + 45, 50],
                          [achievement[5], (255, 255, 255), 1150 if self.size[1] == 768 else 1500,
                           y + 100, 25]]:
                    self.screen.blit(pygame.font.Font(None, j[4]).render(j[0], True, j[1]),
                                     (j[2], j[3]))

                y += 175

            menu_sprites.draw(self.screen)

            pygame.display.flip()
            clock.tick(self.fps)

    def set_progress(self, number, i, add=False):
        with sqlite3.connect(os.path.join(self.path, 'achievements.sqlite')) as con:
            cur = con.cursor()
            if float(cur.execute(f"""SELECT progress FROM achievements
WHERE id = {i}""").fetchone()[0]) != 1:
                if add:
                    pre_result = float(cur.execute(f'''SELECT progress FROM achievements
    WHERE id = {i}''').fetchone()[0]) + number
                    result = pre_result if pre_result < 1 else 1
                else:
                    result = number if number < 1 else 1
                cur.execute(f"""UPDATE achievements
SET progress = {result}
WHERE id = {i}""")
                con.commit()
                if float(cur.execute(f"""SELECT progress FROM achievements
WHERE id = {i}""").fetchone()[0]) == 1:
                    cur.execute(f"""UPDATE achievements
SET date_of_completion = '{datetime.now().date().strftime('%d.%m.%Y')}'
WHERE id = {i}""")
                    con.commit()
                    add_xp(f"{self.path}\statistic.txt", int(cur.execute(
                        f"""SELECT experience FROM achievements
WHERE id = {i}""").fetchone()[0]))
