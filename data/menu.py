# импортируем библиотеки
from cv2 import VideoCapture  # для воспроизвдения заставки покадрово
from data.main_functions import terminate, load_image
import pygame
import os  # для открытия файлов без ошибок


def creator(sprite, name, x, y, group):  # функция помогает быстрее поставить sprite
    sprite.image = load_image(name)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = x
    sprite.rect.y = y
    group.add(sprite)


class Menu:
    def __init__(self, screen, fps):
        self.screen, self.size, self.fps, self.title, self.rect = screen, screen.get_size(), fps, \
                                                                  None, None

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
        # fon = pygame.transform.scale(load_image('fon.jpg'), self.size)
        self.screen.fill((0, 0, 0))  # self.screen.blit(fon, (0, 0))

        menu_sprites = pygame.sprite.Group()

        title = pygame.sprite.Sprite()
        creator(title, "title.png", 549, 50, menu_sprites)

        play = pygame.sprite.Sprite()
        creator(play, "play.png", 558, 150, menu_sprites)

        with_friend = pygame.sprite.Sprite()
        creator(with_friend, "withfriend.png", 558, 200, menu_sprites)

        with_bot = pygame.sprite.Sprite()
        creator(with_bot, "withbot.png", 683, 200, menu_sprites)

        settings = pygame.sprite.Sprite()
        creator(settings, "settings.png", 50, 250, menu_sprites)

        achievements = pygame.sprite.Sprite()
        creator(achievements, "achievements.png", 50, 500, menu_sprites)

        e = pygame.sprite.Sprite()
        creator(e, "exit.png", 1066, 500, menu_sprites)

        menu_sprites.draw(self.screen)
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
                        pass
                    elif achievements.rect.collidepoint(event.pos):
                        pass
                    elif e.rect.collidepoint(event.pos):
                        terminate()
            pygame.display.flip()
            clock.tick(self.fps)
