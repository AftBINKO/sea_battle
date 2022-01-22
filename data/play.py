from data.main_functions import terminate, get_value, create_sprite, get_value, add_fon, load_image
from data.custom_map import Customization
import pygame as pg
import os
import random

display_width = 0
display_height = 0

open_cell_player = []
open_cell_bot = []

list_pos_ship_bot = []
list_pos_ship_player = []

image_popal_bot_group = pg.sprite.Group()

num = 0

n_bot = 0
n_player = 0


def test_bax(n=0):
    opa = []
    if n == 0:
        list_007 = list_pos_ship_bot
        list_008 = open_cell_player

    else:
        list_007 = list_pos_ship_player
        list_008 = open_cell_bot

    for i in list_007:
        n = 0
        for g in i:
            if g in list_008:
                n += 1

        if n == len(i):

            for g in i:
                x = g[0]
                y = g[1]
                if x - 1 != -1 and y - 1 != -1 and (x - 1, y - 1) not in list_008:
                    opa.append((x - 1, y - 1))

                if x - 1 != -1 and y + 1 != 10 and (x - 1, y + 1) not in list_008:
                    opa.append((x - 1, y + 1))

                if x - 1 != -1 and (x - 1, y) not in list_008:
                    opa.append((x - 1, y))

                if x + 1 != 10 and y - 1 != -1 and (x + 1, y - 1) not in list_008:
                    opa.append((x + 1, y - 1))

                if x + 1 != 10 and y + 1 != 10 and (x + 1, y + 1) not in list_008:
                    opa.append((x + 1, y + 1))

                if x + 1 != 10 and (x + 1, y) not in list_008:
                    opa.append((x + 1, y))

                if y - 1 != -1 and (x, y - 1) not in list_008:
                    opa.append((x, y - 1))

                if y + 1 != 10 and (x, y + 1) not in list_008:
                    opa.append((x, y + 1))

            del list_007[list_007.index(i)]
    return opa


def all_remove():
    global open_cell_player, open_cell_bot, num, list_pos_ship_bot, n_bot, n_player, list_pos_ship_player

    open_cell_player = []
    open_cell_bot = []

    list_pos_ship_bot = []
    list_pos_ship_player = []

    num = 0

    n_bot = 0
    n_player = 0

    for i in image_popal_bot_group:
        i.kill()


class Bot:
    def __init__(self, n):
        self.pos = []
        self.level = n
        self.p = [[0] * 10 for _ in range(10)]

        for x1 in range(1, 5):
            for _ in range(x1):
                vv = self.test(5 - x1)
                self.pos.append(vv)
                for tt in vv:
                    self.p[tt[1]][tt[0]] = 1

    def test(self, n):
        coords = []
        rect = (random.randint(0, 9), random.randint(0, 9))
        nap = random.randint(0, 3)
        coords.append(rect)

        x_007 = rect[0]
        y_007 = rect[1]
        if nap == 0:
            for i in range(1, n):
                coords.append((x_007 + i, y_007))

        elif nap == 1:
            for i in range(1, n):
                coords.append((x_007, y_007 + i))

        elif nap == 2:
            for i in range(1, n):
                coords.append((x_007 - i, y_007))

        elif nap == 3:
            for i in range(1, n):
                coords.append((x_007, y_007 - i))

        ref = True

        for i in coords:
            if 0 <= i[0] <= 9 and 0 <= i[1] <= 9:
                pass
            else:
                ref = False
                break

        if ref:
            opa = []
            for tt in coords:

                i = tt[1]
                g = tt[0]
                if i == 0 and g == 0:
                    spi = list(map(lambda x: x[g:g + 2], self.p[i:i + 2]))
                elif g == 0:
                    spi = list(map(lambda x: x[g:g + 2], self.p[i - 1:i + 2]))
                elif i == 0:
                    spi = list(map(lambda x: x[g - 1:g + 2], self.p[i:i + 2]))
                else:
                    spi = list(map(lambda x: x[g - 1:g + 2], self.p[i - 1:i + 2]))

                for h in spi:
                    opa.extend(h)

            if 1 not in opa:
                return coords
            else:
                return self.test(n)
        else:
            return self.test(n)

    def bir(self):
        return self.p, self.pos

    def xod_008(self):
        rect = (random.randint(0, 9), random.randint(0, 9))
        while rect in open_cell_bot:
            rect = (random.randint(0, 9), random.randint(0, 9))
        open_cell_bot.append(rect)
        return rect


class Image_popal(pg.sprite.Sprite):
    image_popal = load_image('bot_popal.png')

    def __init__(self, rect, size, x, y, *op):
        super().__init__(*op)

        self.pos = rect
        self.size = size
        self.image = pg.transform.scale(Image_popal.image_popal, (self.size - 11, self.size - 11))
        self.rect = self.image.get_rect()
        self.rect.x = x + 6
        self.rect.y = y + 6


class Cell(pg.sprite.Sprite):
    image_popal = load_image('popal.png')
    image_ne_popal = load_image('nepopal.png')

    def __init__(self, rect, size, x, y, theme, *op):
        super().__init__(*op)
        self.color = theme
        self.pos = rect
        self.size = size
        self.image = pg.Surface((size - 1, size - 1))
        self.image.fill(theme)
        self.rect = self.image.get_rect()
        self.rect.x = x + 1
        self.rect.y = y + 1

    def update(self, board, event, n=0):
        global num, n_bot, n_player
        if n == 1:
            if self.pos == event:
                if board[event[1]][event[0]] == 1:
                    Image_popal(self.pos, self.size, self.rect.x, self.rect.y, image_popal_bot_group)
                    n_bot += 1

                else:
                    self.image = pg.transform.scale(Cell.image_ne_popal, (self.size - 1, self.size - 1))
                    num += 1

        elif n == 20:
            for hh in event:
                if self.pos == hh:
                    self.image = pg.transform.scale(Cell.image_ne_popal, (self.size - 1, self.size - 1))

        elif n == 30:
            for hh in event:
                if self.pos == hh:
                    self.image = pg.transform.scale(Cell.image_ne_popal, (self.size - 1, self.size - 1))
                    open_cell_player.append(self.pos)

        else:
            if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and\
                    self.pos not in open_cell_player:
                if board[self.pos[1]][self.pos[0]] == 1:
                    self.image = pg.transform.scale(Cell.image_popal, (self.size - 1, self.size - 1))
                    n_player += 1
                else:
                    self.image = pg.transform.scale(Cell.image_ne_popal, (self.size - 1, self.size - 1))
                    num += 1
                open_cell_player.append(self.pos)


class PlayWithBot:
    def __init__(self, screen, fps, path, xp, difficulty, theme):

        all_remove()
        global display_width, display_height, list_pos_ship_bot, list_pos_ship_player
        # self.level = Level(screen, fps)  # я тебе немного помог

        if theme:
            self.t = (255, 255, 255), (0, 0, 0)
        else:
            self.t = (0, 0, 0), (255, 255, 255)

        self.board, self.ships, list_pos_ship_player = Customization(screen, fps, path, theme).bir()
        self.bot = Bot(difficulty)
        self.board_bot, list_pos_ship_bot = self.bot.bir()

        self.all_sprites_1 = pg.sprite.Group()
        self.all_sprites_2 = pg.sprite.Group()
        self.all_sprite_gg = pg.sprite.Group()

        sur = pg.display.get_surface()
        display_width = sur.get_width()
        display_height = sur.get_height()

        self.sc = screen
        self.fps = fps
        self.path = path
        self.xp = xp
        self.difficulty = difficulty
        self.clock = pg.time.Clock()
        self.size = int(display_width * 0.035)
        self.screensize = tuple(
            map(int, (get_value(f"{path}\config.txt", "screensize")[0].split('x'))))
        self.co = int(display_width * 0.02)
        self.font = pg.font.Font(os.path.join("data", f'font_2.ttf'), int(self.size * 0.5))

        self.map_indent_top = 50
        self.map_indent_left = 50

        self.add_cell()
        self.main()

    def main(self):
        running = True

        x = pg.sprite.Sprite()
        create_sprite(x, 'x' + ('_black' if self.t[0] == (255, 255, 255) else '') + '.png',
                      display_width - 75, 30, self.all_sprite_gg)

        while running:
            self.sc.fill(self.t[0])

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

                if event.type == pg.MOUSEBUTTONDOWN:
                    if x.rect.collidepoint(event.pos):
                        return

                if n_player == 20:
                    print('Ты выйграл')
                    return
                elif n_bot == 20:
                    print('Ты проиграл')
                    return

                if num % 2 == 1:
                    rect = self.bot.xod_008()
                    self.all_sprites_1.update(self.board, rect, 1)
                    self.all_sprites_1.update(self.board, test_bax(1), 20)

                else:
                    self.all_sprites_2.update(self.board_bot, event)
                    self.all_sprites_2.update(self.board, test_bax(), 30)

            self.map_draw(self.map_indent_left, self.map_indent_top)
            self.map_draw_2(self.map_indent_left + int(display_width * 0.5), self.map_indent_top)

            self.all_sprites_1.draw(self.sc)
            self.all_sprites_2.draw(self.sc)
            self.all_sprite_gg.draw(self.sc)
            self.ships.draw(self.sc)
            image_popal_bot_group.draw(self.sc)

            self.clock.tick(self.fps)
            pg.display.flip()

    def map_draw(self, x, y):

        slo = list('АБВГДЕЖЗИК')

        for i in range(10):
            text = self.font.render(str(i), True, self.t[1])
            self.sc.blit(text, (i * self.size + x + 15 + self.co, 3 + y))

        for i, pp in enumerate(slo):
            text = self.font.render(pp, True, self.t[1])
            self.sc.blit(text, (x, i * self.size + y + 10 + self.co))

        for i in range(1, 10):
            pg.draw.line(self.sc, self.t[1], (x + self.co + self.size * i, y + self.co),
                         (x + self.co + self.size * i, y + self.co + self.size * 10))
        for i in range(1, 10):
            pg.draw.line(self.sc, self.t[1], (x + self.co, y + self.co + self.size * i),
                         (x + self.co + self.size * 10, y + self.co + self.size * i))

        pg.draw.rect(self.sc, self.t[1], (x + self.co, y + self.co, self.size * 10, self.size * 10),
                     4)

        pg.draw.line(self.sc, self.t[1], (int(display_width * 0.5), 0),
                     (int(display_width * 0.5), display_height), 4)

        font = pg.font.Font(os.path.join("data", f'font_1.ttf'), self.size)

        text = font.render('Бот', True, self.t[1])
        self.sc.blit(text, (display_width // 4, 10))

        text = font.render('Компьютер', True, self.t[1])
        self.sc.blit(text, (display_width // 2 + 200, 10))

    def map_draw_2(self, x, y):

        slo = list('АБВГДЕЁЖЗИ')

        for i in range(10):
            text = self.font.render(str(i), True, self.t[1])
            self.sc.blit(text, (i * self.size + x + 15 + self.co, 3 + y))

        for i, pp in enumerate(slo):
            text = self.font.render(pp, True, self.t[1])
            self.sc.blit(text, (x, i * self.size + y + 10 + self.co))

        for i in range(1, 10):
            pg.draw.line(self.sc, self.t[1], (x + self.co + self.size * i, y + self.co),
                         (x + self.co + self.size * i, y + self.co + self.size * 10))
        for i in range(1, 10):
            pg.draw.line(self.sc, self.t[1], (x + self.co, y + self.co + self.size * i),
                         (x + self.co + self.size * 10, y + self.co + self.size * i))

        pg.draw.rect(self.sc, self.t[1], (x + self.co, y + self.co, self.size * 10, self.size * 10),
                     4)

    def add_cell(self):

        for i in range(10):
            for g in range(10):
                Cell((i, g), self.size, self.size * i + self.co + self.map_indent_left,
                     self.size * g + self.co + self.map_indent_top, self.t[0], self.all_sprites_1)

        for i in range(10):
            for g in range(10):
                Cell((i, g), self.size, self.size * i + self.co + self.map_indent_left + int(
                    display_width * 0.5), self.size * g + self.co + self.map_indent_top, self.t[0],
                     self.all_sprites_2)


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

        q, n, mission_file = 255 if self.size[1] == 768 else 360, 0, os.path.join("data\
\missions", "mission_" + get_value(os.path.join(self.path, 'statistic.txt'), 'mission')[0] + ".txt")
        mission = get_value(mission_file, "mission")[0]

        play, surrender = None, None
        if get_value(mission_file, "mode")[0] == 'normal':
            play = pg.sprite.Sprite()
            create_sprite(play, 'play.png', self.size[0] - 300, self.size[1] - 100, menu_sprites)
        elif get_value(mission_file, "mode")[0] == 'choice':
            surrender = pg.sprite.Sprite()
            create_sprite(surrender, 'surrender.png', self.size[0] - 300, self.size[1] - 100,
                          menu_sprites)

            play = pg.sprite.Sprite()
            create_sprite(play, 'play_mini.png', self.size[0] - 150, self.size[1] - 100,
                          menu_sprites)
        while True:
            self.screen.fill((0, 0, 0))

            texts, words, y, i, running = [], mission.split(), q, 0, True
            while running:
                text, ln = '', 0
                while True:
                    try:
                        if ln + len(words[i]) < 53 and '\\n' not in words[i]:
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
                            pg.mixer.Sound(os.path.join("data", "click.ogg")).play()
                            return
                        try:
                            if play.rect.collidepoint(event.pos):
                                pg.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                                return tuple(
                                    map(int, get_value(mission_file, 'reward', 'difficulty')))
                        except AttributeError:
                            pass
                        try:
                            if surrender.rect.collidepoint(event.pos):
                                pg.mixer.Sound(os.path.join("data", "enter.ogg")).play()

                                with open(f"{self.path}\statistic.txt",
                                          encoding="utf-8") as file_for_read:
                                    file_for_read = list(
                                        map(lambda a: a.strip('\n'), file_for_read.readlines()))
                                with open(f"{self.path}\statistic.txt", 'w',
                                          encoding="utf-8") as file_for_write:
                                    write = []
                                    for i in range(len(file_for_read)):
                                        if file_for_read[i].split(': ')[0] == 'mission':
                                            write.append(f"mission: 8b")
                                        else:
                                            write.append(file_for_read[i])
                                    file_for_write.write('\n'.join(write))

                                    return 'replay'
                        except AttributeError:
                            pass
                    elif event.button == 4:
                        if n - 1 >= 0:
                            q, n = q + 25, n - 1
                    elif event.button == 5:
                        if n + 1 < len(texts) - 19:
                            q, n = q - 25, n + 1
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.mixer.Sound(os.path.join("data", "click.ogg")).play()
                        return
                    elif event.key == pg.K_RETURN:
                        pg.mixer.Sound(os.path.join("data", "enter.ogg")).play()
                        return tuple(map(int, get_value(mission_file, 'reward', 'difficulty')))
                    elif event.key == pg.K_UP:
                        if n - 1 >= 0:
                            q, n = q + 25, n - 1
                    elif event.key == pg.K_DOWN:
                        if n + 1 < len(texts) - 19:
                            q, n = q - 25, n + 1

            menu_sprites.draw(self.screen)

            if get_value(mission_file, "mode")[0] != 'text':
                for j in [
                    ['Награда:', (255, 255, 255), self.size[0] - 300, self.size[1] - 130, 25, 1],
                    [f"{get_value(mission_file, 'reward')[0]} XP", (255, 255, 255),
                     self.size[0] - 215,
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
                        pg.font.Font(os.path.join("data", f'font_{str(j[5])}.ttf'), j[4]).render(
                            j[0], True, j[1]), (j[2], j[3]))

            self.screen.blit(
                pg.font.Font(os.path.join("data", 'font_1.ttf'), 50).render(
                    get_value(mission_file, 'name')[0], True, (255, 255, 255)),
                (70 if self.size[1] == 768 else 80, 200 if self.size[1] == 768 else 300))

            pg.display.flip()
            clock.tick(self.fps)


class Board:
    def __init__(self, screen, fps):
        global display_width, display_height
        self.sc = screen
        self.fps = fps

        sur = pg.display.get_surface()
        display_width = sur.get_width()
        display_height = sur.get_height()

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
