import cv2
import pygame
import os


def screensaver():
    pygame.mixer.init()
    cap = cv2.VideoCapture(os.path.join("data", "aftforseabattle1366x768.mp4"))
    s = pygame.mixer.Sound(os.path.join("data", "aftforseabattle.wav"))
    running, img = cap.read()
    shape = img.shape[1::-1]
    wn = pygame.display.set_mode(shape)
    clock = pygame.time.Clock()
    s.play()

    while running:
        clock.tick(60)
        running, img = cap.read()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        try:
            wn.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
        except AttributeError:
            pass
        pygame.display.update()
    s.stop()
