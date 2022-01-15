from data.main_functions import terminate, create_sprite, load_image, get_value
import pygame as pg
import os


class Board:
    def __init__(self, screen, fps):
        self.board = [[0] * 10 for _ in range(10)]
        self.sc = screen
        self.fps = fps

        sur = pg.display.get_surface()
        self.display_width = sur.get_width()
        self.display_height = sur.get_height()

        self.co = int(self.display_width * 0.02)
        self.size = int(self.display_width * 0.035)
        self.font = pg.font.Font(None, int(self.size * 0.8))
        self.clock = pg.time.Clock()

    def map_draw(self, x, y):

        slo = list('АБВГДЕЁЖЗИ')

        for i in range(10):
            text = self.font.render(str(i), True, (255, 255, 255))
            self.sc.blit(text, (i * self.size + x + 15 + self.co, 3 + y))

        for i, pp in enumerate(slo):
            text = self.font.render(pp, True, (255, 255, 255))
            self.sc.blit(text, (x, i * self.size + y + 10 + self.co))

        for i in range(10):
            for g in range(10):
                pg.draw.rect(self.sc, (255, 255, 255), (i * self.size + x + self.co,
                                                        g * self.size + y + self.co,
                                                        self.size, self.size), 1)
        pg.draw.rect(self.sc, (255, 255, 255), (x + self.co,
                                                y + self.co,
                                                self.size * 10, self.size * 10), 4)


class Ship(pg.sprite.Sprite):
    def __init__(self, n, x, y, *op):
        super().__init__(*op)
        image = load_image('ship_' + str(n) + '.png', 1)
        print(image)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class PlayWithBot(Board):
    # в главном файле передаётсязначение fps. Тебе стоит добавить fps в конструктор
    def __init__(self, screen, fps):
        super().__init__(screen, fps)
        self.map_customization()

    def map_customization(self):
        running = True
        all_sprites = pg.sprite.Group()
        Ship(1, 0, 0, all_sprites)

        while running:
            self.sc.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()

            self.map_draw(30, 30)
            all_sprites.draw(self.sc)
            pg.display.flip()

        self.clock.tick(self.fps)


class PlayWithFriend(Board):
    pass


class Play:
    def __init__(self, screen, fps, path):
        self.screen, self.fps, self.path, self.size = screen, fps, path, tuple(
            map(int, (get_value(f"{path}\config.txt", "screensize")[0].split('x'))))

    def menu(self):
        clock = pg.time.Clock()

        menu_sprites = pg.sprite.Group()

        mat = pg.sprite.Sprite()
        create_sprite(mat, f'mat_5_{self.size[1]}.png', 0, 0, menu_sprites)

        x = pg.sprite.Sprite()
        create_sprite(x, 'x.png', self.size[0] - 100, 50, menu_sprites)

        title = pg.sprite.Sprite()
        create_sprite(title, 'play_title.png', 50, 50, menu_sprites)

        play = pg.sprite.Sprite()
        create_sprite(play, 'play.png', self.size[0] - 300, self.size[1] - 100, menu_sprites)

        q, n, mission_file = 255 if self.size[1] == 768 else 360, 0, os.path.join("data\missions",
                                                                                  "mission_" +
                                                                                  get_value(
                                                                                      os.path.join(
                                                                                          self.path,
                                                                                          'statistic\
.txt'), 'mission')[0] + ".txt")
        while True:
            self.screen.fill((0, 0, 0))

            texts, words, y, i, running = [], get_value(mission_file, "mission")[
                0].split(), q, 0, True
            while running:
                text, ln = '', 0
                while True:
                    try:
                        if ln + len(words[i]) < 57 and '\\n' not in words[i]:
                            text, ln, i = text + words[i] + ' ', ln + len(words[i]), i + 1
                        else:
                            words[i] = words[i].strip('\\n')
                            break
                    except IndexError:
                        running = False
                        break
                texts.append([text, (192, 192, 192), 55 if self.size[1] == 768 else 75, y, 25])
                y += 25
            for j in texts:
                self.screen.blit(pg.font.Font(None, j[4]).render(j[0], True, j[1]), (j[2], j[3]))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if x.rect.collidepoint(event.pos):
                            return
                        elif play.rect.collidepoint(event.pos):
                            pass
                    elif event.button == 4:
                        if n - 1 >= 0:
                            q, n = q + 25, n - 1
                    elif event.button == 5:
                        if n + 1 < len(texts) - (16 if self.size == 768 else 23):
                            q, n = q - 25, n + 1
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
                    if event.key == pg.K_UP:
                        if n - 1 >= 0:
                            q, n = q + 25, n - 1
                    elif event.key == pg.K_DOWN:
                        if n + 1 < len(texts) - (16 if self.size == 768 else 23):
                            q, n = q - 25, n + 1

            menu_sprites.draw(self.screen)

            for j in [
                [get_value(mission_file, 'name')[0], (255, 255, 255),
                 70 if self.size[1] == 768 else 80, 205 if self.size[1] == 768 else 310, 50],
                ['Награда:', (255, 255, 255), self.size[0] - 300, self.size[1] - 130, 25],
                [f"{get_value(mission_file, 'reward')[0]} XP", (255, 255, 255), self.size[0] - 215,
                 self.size[1] - 130, 25],
                ['Сложность:', (255, 255, 255), self.size[0] - 300, self.size[1] - 155, 25],
                (['Обучение', (255, 255, 255), self.size[0] - 190, self.size[1] - 155, 25],
                 ['Самый лёгкий', (66, 170, 255), self.size[0] - 190, self.size[1] - 155, 25],
                 ['Лёгкий', (0, 255, 0), self.size[0] - 190, self.size[1] - 155, 25],
                 ['Нормальный', (255, 255, 0), self.size[0] - 190, self.size[1] - 155, 25],
                 ['Сложный', (255, 165, 0), self.size[0] - 190, self.size[1] - 155, 25],
                 ['Невозможный', (255, 0, 0), self.size[0] - 190, self.size[1] - 155, 25])[
                    int(get_value(mission_file, 'difficulty')[0])]]:
                self.screen.blit(pg.font.Font(None, j[4]).render(j[0], True, j[1]),
                                 (j[2], j[3]))

            pg.display.flip()
            clock.tick(self.fps)
