import pygame

from data.main_functions import terminate, create_sprite


class Board:
    pass


class PlayWithFriend(Board):
    def __init__(self, screen, fps):
        self.screen, self.size, self.fps = screen, screen.get_size(), fps


class PlayWithBot(Board):
    def __init__(self, screen, fps):
        self.screen, self.size, self.fps = screen, screen.get_size(), fps


class Play(PlayWithBot):
    def menu(self):
        clock = pygame.time.Clock()

        while True:
            menu_sprites = pygame.sprite.Group()

            x = pygame.sprite.Sprite()
            create_sprite(x, 'x.png', 1266, 50, menu_sprites)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if x.rect.collidepoint(event.pos):
                            return

                self.screen.fill((0, 0, 0))
                menu_sprites.draw(self.screen)
                pygame.display.flip()
                clock.tick(self.fps)
