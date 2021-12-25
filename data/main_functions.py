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
