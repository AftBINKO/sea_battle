from data.main_functions import terminate, create_sprite, load_image
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
        self.screen, self.fps, self.path = screen, fps, path

    def menu(self):
        clock = pg.time.Clock()

        menu_sprites = pg.sprite.Group()

        mat = pg.sprite.Sprite()
        create_sprite(mat, 'mat_5.png', 0, 0, menu_sprites)

        x = pg.sprite.Sprite()
        create_sprite(x, 'x.png', 1266, 50, menu_sprites)

        title = pg.sprite.Sprite()
        create_sprite(title, 'play_title.png', 50, 50, menu_sprites)

        reward = pg.sprite.Sprite()
        create_sprite(reward, "reward.png", 1066, 518, menu_sprites)

        play = pg.sprite.Sprite()
        create_sprite(play, 'play.png', 1066, 668, menu_sprites)

        while True:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if x.rect.collidepoint(event.pos):
                        return
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return

            self.screen.fill((0, 0, 0))
            with open(os.path.join(self.path, "statistic.txt")) as statistic:
                statistic = dict(map(lambda a: tuple(a.split(': ')), [line for line in list(
                    map(lambda a: a.strip('\n'), statistic.readlines())) if line != '' if
                                                                      line[0] != '#']))
            with open(os.path.join("data\missions", f"mission_{statistic['mission']}.txt"),
                      encoding='utf-8') as mission:
                mission = dict(map(lambda a: tuple(a.split(': ')), [line for line in list(
                    map(lambda a: a.strip('\n'), mission.readlines())) if line != '' if
                                                                      line[0] != '#']))
                for j in [[mission['name'], (255, 255, 255), 70, 205, 50],
                          [mission['mission'], (192, 192, 192), 55, 255, 25]]:
                    self.screen.blit(pg.font.Font(None, j[4]).render(j[0], True, j[1]),
                                     (j[2], j[3]))
            menu_sprites.draw(self.screen)
            pg.display.flip()
            clock.tick(self.fps)
