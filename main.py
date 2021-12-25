# импортируем библиотеки
from data.menu import Menu
import pygame
import sys


# основная функция
def main():
    pygame.init()  # инициализируем pygame
    size = (1366, 768)  # размеры экрана пока оставим такими
    screen = pygame.display.set_mode(size)  # создаём окно
    pygame.display.set_caption('Sea Battle')  # ставим заголовок
    fps = 60  # ставим количество кадров в секунду
    menu = Menu(screen, fps)
    # pygame.mouse.set_visible(False)  # погашаем мышь
    # menu.screensaver()  # заставка
    # pygame.mouse.set_visible(True)  # показываем мышь
    menu.menu()  # меню
    pygame.quit()  # выходим из игры


if __name__ == '__main__':
    sys.exit(main())
