# импортируем библиотеки
from data.screensaver import screensaver
import pygame
import sys


# основная функция
def main():
    pygame.init()  # инициализируем pygame
    size = (1366, 768)  # размеры экрана пока оставим такими
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)  # создаём окно
    pygame.display.set_caption('Sea Battle')  # ставим заголовок
    fps = 60  # ставим количество кадров в секунду
    screensaver(screen, fps)
    pygame.quit()  # выходим из игры


if __name__ == '__main__':
    sys.exit(main())
