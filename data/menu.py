# импортируем библиотеки
from cv2 import VideoCapture  # для воспроизвдения заставки покадрово
from data.main_functions import terminate, create_sprite
import pygame
import os  # для открытия файлов без ошибок


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
        # fon = pygame.transform.scale(load_image('fon.jpg'), self.size)
        self.screen.fill((0, 0, 0))  # self.screen.blit(fon, (0, 0))

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
                        return 'Settings'
                    elif achievements.rect.collidepoint(event.pos):
                        pass
                    elif e.rect.collidepoint(event.pos):
                        terminate()
            pygame.display.flip()
            clock.tick(self.fps)
