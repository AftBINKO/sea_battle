from data.main_functions import terminate, create_sprite, create_text
import pygame
import os


class Settings:
    def __init__(self, screen, fps, config):
        self.screen, self.size, self.fps, self.config = screen, screen.get_size(), fps, config

    def menu(self):
        clock = pygame.time.Clock()
        # fon = pygame.transform.scale(load_image('fon.jpg'), self.size)
        self.screen.fill((0, 0, 0))  # self.screen.blit(fon, (0, 0))

        settings_sprites = pygame.sprite.Group()

        x = pygame.sprite.Sprite()
        create_sprite(x, 'x.png', 1266, 50, settings_sprites)

        title = pygame.sprite.Sprite()
        create_sprite(title, 'settings_title.png', 50, 50, settings_sprites)

        left_screensize = pygame.sprite.Sprite()
        create_sprite(left_screensize, 'left_arrow.png', 450, 205, settings_sprites)
        right_screensize = pygame.sprite.Sprite()
        create_sprite(right_screensize, 'right_arrow.png', 800, 205, settings_sprites)

        left_screenmode = pygame.sprite.Sprite()
        create_sprite(left_screenmode, 'left_arrow.png', 450, 250, settings_sprites)
        right_screenmode = pygame.sprite.Sprite()
        create_sprite(right_screenmode, 'right_arrow.png', 800, 250, settings_sprites)

        left_fps = pygame.sprite.Sprite()
        create_sprite(left_fps, 'left_arrow.png', 450, 300, settings_sprites)
        right_fps = pygame.sprite.Sprite()
        create_sprite(right_fps, 'right_arrow.png', 800, 300, settings_sprites)

        for i in [[self.screen, f"Версия конфигурационного файла: {self.config['version']}",
                   (128, 128, 128), 50, 150, 25],
                  [self.screen, "Размер экрана: ", (255, 255, 255), 50, 200, 50],
                  [self.screen, self.config['screensize'], (255, 255, 255), 500, 200, 50],
                  [self.screen, "Режим экрана: ", (255, 255, 255), 50, 250, 50],
                  [self.screen, self.config['screenmode'], (255, 255, 255), 500, 250, 50],
                  [self.screen, "FPS: ", (255, 255, 255), 50, 300, 50],
                  [self.screen, self.config['fps'], (255, 255, 255), 500, 300, 50]]:
            create_text(*i)

        settings_sprites.draw(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if x.rect.collidepoint(event.pos):
                        return
            pygame.display.flip()
            clock.tick(self.fps)
