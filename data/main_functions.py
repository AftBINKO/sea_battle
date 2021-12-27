import os
import sys
import pygame


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, c=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        raise FileNotFoundError(f'the file with the image f"{fullname}" was not found')
    image = pygame.image.load(fullname)
    return image


def create_sprite(sprite, name, x, y, group):  # функция помогает быстрее поставить sprite
    sprite.image = load_image(name)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = x
    sprite.rect.y = y
    group.add(sprite)


def create_text(screen, text, color, x, y, size, antialias=True, font=None):
    screen.blit(pygame.font.Font(font, size).render(text, antialias, color), (x, y))
