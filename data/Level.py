import pygame as pg
from data.main_functions import create_sprite


class Level:
    def __init__(self, screen, fps):
        self.sc = screen
        self.fps = fps
        self.all_sprite = pg.sprite.Group()
        self.clock = pg.time.Clock()
        sur = pg.display.get_surface()
        self.display_width = sur.get_width()
        self.display_height = sur.get_height()

        self.main()

    def draw_map(self):

        font = pg.font.Font(None, 60)
        text = font.render('Выберите уровень:', True, (255, 255, 255))
        self.sc.blit(text, (self.display_width // 2 - 200, 100))

    def main(self):
        running = True
        x_x = self.display_width // 2 - 125
        y_y = 300

        x = pg.sprite.Sprite()
        create_sprite(x, 'x.png', self.display_width - 75, 30, self.all_sprite)

        lev_1 = pg.sprite.Sprite()
        create_sprite(lev_1, 'lev_1.png', x_x, y_y, self.all_sprite)

        lev_2 = pg.sprite.Sprite()
        create_sprite(lev_2, 'lev_2.png', x_x, y_y + 60, self.all_sprite)

        lev_3 = pg.sprite.Sprite()
        create_sprite(lev_3, 'lev_3.png', x_x, y_y + 60 * 2, self.all_sprite)

        lev_4 = pg.sprite.Sprite()
        create_sprite(lev_4, 'lev_4.png', x_x, y_y + 60 * 3, self.all_sprite)

        lev_5 = pg.sprite.Sprite()
        create_sprite(lev_5, 'lev_5.png', x_x, y_y + 60 * 4, self.all_sprite)

        while running:
            self.sc.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

                if event.type == pg.MOUSEBUTTONDOWN:
                    if x.rect.collidepoint(event.pos):
                        return

                    if lev_1.rect.collidepoint(event.pos):
                        return

                    if lev_2.rect.collidepoint(event.pos):
                        return

                    if lev_3.rect.collidepoint(event.pos):
                        return

                    if lev_4.rect.collidepoint(event.pos):
                        return

                    if lev_5.rect.collidepoint(event.pos):
                        return

            self.all_sprite.draw(self.sc)
            self.draw_map()

            self.clock.tick(self.fps)
            pg.display.flip()

