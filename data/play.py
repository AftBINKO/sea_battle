from data.main_functions import terminate, create_sprite

import pygame as pg


class Board:
    def __init__(self, screen):
        self.board = [[0] * 10 for _ in range(10)]
        self.sc = screen
        self.co = 30
        self.size = 40
        print()

    def map_draw(self):
        font = pg.font.Font(None, self.size // 2 + 10)
        slo = list('АБВГДЕЁЖЗИ')

        for i in range(10):
            text = font.render(str(i), True, (255, 255, 255))
            self.sc.blit(text, (i * self.size + self.co + 15, 3))

        for i, pp in enumerate(slo):
            print(i, pp)
            text = font.render(pp, True, (255, 255, 255))
            self.sc.blit(text, (0, i * self.size + self.co + 15))

        for i in range(10):
            for g in range(10):
                pg.draw.rect(self.sc, (255, 255, 255), (i * self.size + self.co,
                                                        g * self.size + self.co,
                                                        self.size, self.size), 2)


class PlayWithBot(Board):
    # в главном файле передаётсязначение fps. Тебе стоит добавить fps в конструктор
    def __init__(self, screen):
        super().__init__(screen)
        self.main()

    def main(self):
        running = True
        while running:
            self.sc.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.map_draw()
            pg.display.flip()


class PlayWithFriend(Board):
    pass


class Play:
    def __init__(self, screen, fps):
        self.screen, self.fps = screen, fps

    def menu(self):
        clock = pg.time.Clock()

        while True:
            menu_sprites = pg.sprite.Group()

            x = pg.sprite.Sprite()
            create_sprite(x, 'x.png', 1266, 50, menu_sprites)

            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        terminate()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if x.rect.collidepoint(event.pos):
                            return

                self.screen.fill((0, 0, 0))
                menu_sprites.draw(self.screen)
                pg.display.flip()
                clock.tick(self.fps)
