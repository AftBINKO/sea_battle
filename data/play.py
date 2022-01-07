import pygame as pg


class Board:
    def __init__(self, screen):
        self.board = [[0] * 10 for _ in range(10)]
        self.sc = screen
        self.co = 30
        self.size = 40
        print()

    def map_draw(self):
        font = pg.font.Font(None, self.size)
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
    def __init__(self, screen):
        super().__init__(screen)
        self.main_1()

    def main_1(self):
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


class Play(PlayWithBot):
    pass
