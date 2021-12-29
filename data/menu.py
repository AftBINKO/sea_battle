# импортируем библиотеки
import sqlite3
import pygame
import os

from cv2 import VideoCapture  # для воспроизвдения заставки покадрово

from data.main_functions import terminate, create_sprite


class Menu:
    def __init__(self, screen, fps):
        self.screen, self.size, self.fps = screen, screen.get_size(), fps

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
            pygame.display.flip()
            clock.tick(self.fps)


class Achievements:
    def __init__(self, screen, fps, achievements):
        self.screen, self.fps, self.achievements = screen, fps, achievements

    def menu(self):
        clock = pygame.time.Clock()

        menu_sprites = pygame.sprite.Group()

        m = pygame.sprite.Sprite()
        create_sprite(m, 'mat_2.png', 0, 0, menu_sprites)

        x = pygame.sprite.Sprite()
        create_sprite(x, 'x.png', 1266, 50, menu_sprites)

        title = pygame.sprite.Sprite()
        create_sprite(title, 'achievements_title.png', 50, 50, menu_sprites)

        con = sqlite3.connect(os.path.join(self.achievements, "achievements.sqlite"))
        cur = con.cursor()
        achievements = cur.execute("""SELECT * FROM achievements""").fetchall()

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
                        if f + 1 < len(achievements) - 2:
                            a, f = a - 175, f + 1
                    if x.rect.collidepoint(event.pos):
                        con.close()
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if f - 1 >= 0:
                            a, f = a + 175, f - 1
                    elif event.key == pygame.K_DOWN:
                        if f + 1 < len(achievements) - 2:
                            a, f = a - 175, f + 1
            self.screen.fill((0, 0, 0))

            y, i = a, 0
            while i < len(achievements):
                achievement_sprites = pygame.sprite.Group()

                achievement = achievements[i]

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
