from data.main_functions import terminate, create_sprite, get_value
import pygame as pg
import os

display_width = 0
display_height = 0

all_sprites_cell = pg.sprite.Group()
all_sprites = pg.sprite.Group()

test_hover_map = False
test_hover_map_num = 0
if_yes_rect_map = []

list_pos_if_yes = []

board = [[0] * 10 for _ in range(10)]


def test_board(list_009):
    opa = []
    for tt in list_009:
        i = tt[0]
        g = tt[1]
        if i == 0 and g == 0:
            spi = list(map(lambda x: x[g:g + 2], board[i:i + 2]))
        elif g == 0:
            spi = list(map(lambda x: x[g:g + 2], board[i - 1:i + 2]))
        elif i == 0:
            spi = list(map(lambda x: x[g - 1:g + 2], board[i:i + 2]))
        else:
            spi = list(map(lambda x: x[g - 1:g + 2], board[i - 1:i + 2]))

        for h in spi:
            opa.extend(h)

    num = opa.count(1)
    if num == 0 and len(list_009) != 0:
        downloads_tic_tac(list_009)
        return True

    del list_pos_if_yes[:]
    return False


def downloads_tic_tac(list_008):
    for i in list_008:
        board[i[0]][i[1]] = 1


def flip_image(image):
    return pg.transform.rotate(image, 90)


class Board:
    def __init__(self, screen, fps):
        self.board = [[0] * 10 for _ in range(10)]
        self.sc = screen
        self.fps = fps

        self.co = int(display_width * 0.02)
        self.size = int(display_width * 0.035)
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


class Cell(pg.sprite.Sprite):
    def __init__(self, rect, size, x, y, *op):
        super().__init__(*op)
        self.pos = rect
        self.image = pg.Surface((size - 1, size - 1))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x + 1
        self.rect.y = y + 1

    def update(self, event, list_007=None, n=0):

        if n == 1 and list_007:
            global test_hover_map, test_hover_map_num, if_yes_rect_map, list_pos_if_yes
            n = 0
            for i in list_007:
                if self.rect.collidepoint(i):
                    test_hover_map_num += 1
                    list_pos_if_yes.append(self.pos)
                    if n == 0:
                        if_yes_rect_map = (self.rect.x + 5, self.rect.y + 5)

                n += 1
                if n == len(list_007):
                    break

            if test_hover_map_num == len(list_007) and test_board(list_pos_if_yes):
                test_hover_map = True
                test_hover_map_num = 0
                del list_pos_if_yes[:]

        else:
            self.image.fill((0, 0, 0))
            try:
                if list_007:
                    for i in list_007:
                        if self.rect.collidepoint(i):
                            self.image.fill((255, 0, 0))
            except AttributeError:
                pass


class Ship(pg.sprite.Sprite):
    def __init__(self, size, n, x, y, *op):
        super().__init__(*op)
        self.n = n
        self.size = size
        self.image = pg.Surface((size * n + ((n * 10) - 10), size))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.old_x = x
        self.old_y = y

        self.hover_x = 0
        self.hover_y = 0
        self.hover = False
        self.flip = False

        self.installed_map = False

    def update(self, screen, event):
        if self.installed_map:
            pass
        else:
            if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.hover = True
                self.hover_x = self.rect.x - event.pos[0]
                self.hover_y = self.rect.y - event.pos[1]

            if event.type == pg.MOUSEBUTTONUP and self.hover:

                list_008 = []
                for i in range(self.n):
                    if self.flip:
                        list_008.append((int(self.rect.x + self.size * 0.5),
                                         int(self.rect.y + self.size * 0.5 + self.size * i + i * 10)))
                    else:
                        list_008.append((int(self.rect.x + self.size * 0.5 + self.size * i + i * 10),
                                         int(self.rect.y + self.size * 0.5)))

                all_sprites_cell.update(0, list_008, 1)
                global test_hover_map, test_hover_map_num
                if test_hover_map:
                    self.installed_map = True
                    test_hover_map = False
                    test_hover_map_num = 0
                    self.rect.x = if_yes_rect_map[0]
                    self.rect.y = if_yes_rect_map[1]

                else:
                    if self.flip:
                        self.image = flip_image(self.image)
                        self.flip = False
                        x_00 = self.rect.x
                        y_00 = self.rect.y
                        self.rect = self.image.get_rect()
                        self.rect.x = x_00
                        self.rect.y = y_00

                    test_hover_map_num = 0
                    self.rect.x = self.old_x
                    self.rect.y = self.old_y

                self.hover = False

            if self.hover and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.image = flip_image(self.image)
                x_00 = self.rect.x
                y_00 = self.rect.y
                self.rect = self.image.get_rect()
                self.rect.x = x_00
                self.rect.y = y_00
                if self.flip:
                    self.flip = False
                else:
                    self.flip = True

            try:
                if self.hover:
                    self.rect.x = self.hover_x + event.pos[0]
                    self.rect.y = self.hover_y + event.pos[1]

            except AttributeError:
                pass

            if self.hover:
                list_008 = []
                for i in range(self.n):
                    if self.flip:
                        list_008.append(
                            (
                                int(self.rect.x + self.size * 0.5),
                                int(self.rect.y + self.size * 0.5 + self.size * i + i * 10)
                            )
                        )
                    else:
                        list_008.append((int(self.rect.x + self.size * 0.5 + self.size * i + i * 10),
                                        int(self.rect.y + self.size * 0.5)))

                all_sprites_cell.update(0, list_008)


class Customization:
    def __init__(self, screen, fps):
        global display_width, display_height
        self.board = [[0] * 10 for _ in range(10)]
        self.sc = screen
        self.fps = fps
        self.all_sprites = pg.sprite.Group()
        sur = pg.display.get_surface()
        display_width = sur.get_width()
        display_height = sur.get_height()
        self.clock = pg.time.Clock()
        self.size = int(display_width * 0.035)
        self.co = int(display_width * 0.02)
        self.font = pg.font.Font(None, int(self.size * 0.8))

        self.map_indent_top = 50
        self.map_indent_left = 50

        self.add_cells()
        self.add_ship()
        self.map_customization()

    def map_draw(self, x, y):

        slo = list('АБВГДЕЁЖЗИ')

        for i in range(10):
            text = self.font.render(str(i), True, (255, 255, 255))
            self.sc.blit(text, (i * self.size + x + 15 + self.co, 3 + y))

        for i, pp in enumerate(slo):
            text = self.font.render(pp, True, (255, 255, 255))
            self.sc.blit(text, (x, i * self.size + y + 10 + self.co))

        for i in range(1, 10):
            pg.draw.line(self.sc, (255, 255, 255), (x + self.co + self.size * i, y + self.co),
                         (x + self.co + self.size * i, y + self.co + self.size * 10))
        for i in range(1, 10):
            pg.draw.line(self.sc, (255, 255, 255), (x + self.co, y + self.co + self.size * i),
                         (x + self.co + self.size * 10, y + self.co + self.size * i))

        pg.draw.rect(self.sc, (255, 255, 255), (x + self.co,
                                                y + self.co,
                                                self.size * 10, self.size * 10), 4)

    def map_customization(self):
        running = True

        while running:
            self.sc.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                all_sprites_cell.update(event)
                all_sprites.update(self.sc, event)

            self.map_draw(self.map_indent_left, self.map_indent_top)
            all_sprites_cell.draw(self.sc)
            all_sprites.draw(self.sc)
            self.clock.tick(self.fps)
            pg.display.flip()

    def add_ship(self):
        x = int(display_width * 0.6)
        y = int(display_height * 0.25)
        indent_bottom = 10
        indent_right = 10
        size = int(display_width * 0.035) - 10

        for i in range(1, 5):
            for g in range(i):
                Ship(size, 5 - i, x + (((size * (5 - i)) + indent_right + (((5 - i) * 10) - 10)) * g),
                     y + ((size + indent_bottom) * i), all_sprites)

    def add_cells(self):

        for i in range(10):
            for g in range(10):
                Cell((i, g), self.size, self.size * i + self.co + self.map_indent_left,
                     self.size * g + self.co + self.map_indent_top, all_sprites_cell)


class PlayWithBot:
    # в главном файле передаётсязначение fps. Тебе стоит добавить fps в конструктор
    def __init__(self, screen, fps):
        self.player = Customization(screen, fps)


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
                c = 22 if self.size[1] == 768 else 30
                texts.append([text, (192, 192, 192), 55 if self.size[1] == 768 else 75, y, c])
                y += c
            for j in texts:
                self.screen.blit(
                    pg.font.Font(os.path.join("data", 'font_2.ttf'), j[4]).render(j[0], True, j[1]),
                    (j[2], j[3]))

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
                 70 if self.size[1] == 768 else 80, 200 if self.size[1] == 768 else 300, 50, 1],
                ['Награда:', (255, 255, 255), self.size[0] - 300, self.size[1] - 130, 25, 1],
                [f"{get_value(mission_file, 'reward')[0]} XP", (255, 255, 255), self.size[0] - 215,
                 self.size[1] - 130, 25, 1],
                ['Сложность:', (255, 255, 255), self.size[0] - 300, self.size[1] - 155, 25, 1],
                (['Обучение', (255, 255, 255), self.size[0] - 190, self.size[1] - 155, 25, 1],
                 ['Самый лёгкий', (66, 170, 255), self.size[0] - 190, self.size[1] - 155, 25, 1],
                 ['Лёгкий', (0, 255, 0), self.size[0] - 190, self.size[1] - 155, 25, 1],
                 ['Нормальный', (255, 255, 0), self.size[0] - 190, self.size[1] - 155, 25, 1],
                 ['Сложный', (255, 165, 0), self.size[0] - 190, self.size[1] - 155, 25, 1],
                 ['Невозможный', (255, 0, 0), self.size[0] - 190, self.size[1] - 155, 25, 1])[
                    int(get_value(mission_file, 'difficulty')[0])]]:
                self.screen.blit(
                    pg.font.Font(os.path.join("data", f'font_{str(j[5])}.ttf'), j[4]).render(j[0],
                                                                                             True,
                                                                                             j[1]),
                    (j[2], j[3]))

            pg.display.flip()
            clock.tick(self.fps)
