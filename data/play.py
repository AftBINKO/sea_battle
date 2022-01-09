from data.main_functions import terminate, create_sprite

import pygame as pg


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

    def map_draw(self, x, y):
        font = pg.font.Font(None, self.size - 10)
        slo = list('АБВГДЕЁЖЗИ')

        for i in range(10):
            text = font.render(str(i), True, (255, 255, 255))
            self.sc.blit(text, (i * self.size + x + 15 + self.co, 3 + y))

        for i, pp in enumerate(slo):
            text = font.render(pp, True, (255, 255, 255))
            self.sc.blit(text, (x, i * self.size + y + 10 + self.co))

        for i in range(10):
            for g in range(10):
                pg.draw.rect(self.sc, (255, 255, 255), (i * self.size + x + self.co,
                                                        g * self.size + y + self.co,
                                                        self.size, self.size), 1)
        pg.draw.rect(self.sc, (255, 255, 255), (x + self.co,
                                                y + self.co,
                                                self.size * 10, self.size * 10), 4)

    def ships_draw(self):
        pass


class PlayWithBot(Board):
    # в главном файле передаётсязначение fps. Тебе стоит добавить fps в конструктор
    def __init__(self, screen, fps):
        super().__init__(screen, fps)
        self.main_1()

    def main_1(self):
        clock = pg.time.Clock()
        running = True
        while running:
            self.sc.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()

            self.map_draw(30, 30)
            pg.display.flip()

        clock.tick(self.fps)


class PlayWithFriend(Board):
    pass


class Play:
    def __init__(self, screen, fps):
        self.screen, self.fps = screen, fps

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
            menu_sprites.draw(self.screen)
            pg.display.flip()
            clock.tick(self.fps)
