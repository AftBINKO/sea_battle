# импортируем библиотеки
from cv2 import VideoCapture  # для воспроизвдения заставки покадрово
import pygame
import os  # для открытия файлов без ошибок


# функция воспроизведения заставки
def screensaver(screen, fps):
    pygame.mixer.init()
    size = screen.get_size()  # получаем размер экрана
    # воспроизводим видео, в соответствии разрешения
    cap = VideoCapture(os.path.join("data", f"screensaver{size[0]}x{size[1]}.mp4"))
    # т.к видео воспроизводится без звука, мы его добавим вручную
    s = pygame.mixer.Sound(os.path.join("data", "screensaver.wav"))
    running, img = cap.read()  # running — кадры остались? img — изображение
    shape = img.shape[1::-1]
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    s.play()  # воспроизводим звук

    while running:
        clock.tick(fps)
        running, img = cap.read()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        try:
            screen.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))  # заполняем
        except AttributeError:
            pass
        pygame.display.update()
    s.stop()
