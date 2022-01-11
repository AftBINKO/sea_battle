from data.main_functions import terminate, create_sprite
import pygame
import os


class Settings:
    def __init__(self, screen, fps, config, path):
        self.screen, self.size, self.fps, self.config, self.path = screen, screen.get_size(), fps, \
                                                                   config, path
        self.values_screensize, self.values_screenmode, self.values_fps = ['1366x768', '1920x1080'
                                                                           ], ['window', 'noframe',
                                                                               'fullscreen'], [
                                                                              '30', '60', '90',
                                                                              '120']
        self.value_screensize, self.value_screenmode, self.value_fps = self.values_screensize.index(
            config['screensize']), self.values_screenmode.index(
            config['screenmode']), self.values_fps.index(config['fps'])

    def apply(self):
        with open(f"{self.path}\config.txt", encoding="utf-8") as config_for_read:
            config_for_read = list(
                map(lambda a: a.strip('\n'), config_for_read.readlines()))
        with open(f"{self.path}\config.txt", 'w',
                  encoding="utf-8") as config_for_write:
            write = []
            for i in range(len(config_for_read)):
                if config_for_read[i].split(': ')[0] == 'screensize':
                    write.append(f'screensize: \
{self.values_screensize[self.value_screensize]}')
                elif config_for_read[i].split(': ')[0] == 'screenmode':
                    write.append(f'screenmode: \
{self.values_screenmode[self.value_screenmode]}')
                elif config_for_read[i].split(': ')[0] == 'fps':
                    write.append(f'fps: \
{self.values_fps[self.value_fps]}')
                else:
                    write.append(config_for_read[i])
            config_for_write.write('\n'.join(write))
        return True

    def menu(self):
        clock = pygame.time.Clock()
        # fon = pygame.transform.scale(load_image('fon.jpg'), self.size)

        settings_sprites = pygame.sprite.Group()

        x = pygame.sprite.Sprite()
        create_sprite(x, 'x.png', self.size[0] - 100, 50, settings_sprites)

        apply = pygame.sprite.Sprite()
        create_sprite(apply, 'apply.png', self.size[0] - 300, self.size[1] - 100, settings_sprites)

        title = pygame.sprite.Sprite()
        create_sprite(title, 'settings_title.png', 50, 50, settings_sprites)

        left_screensize = pygame.sprite.Sprite()
        create_sprite(left_screensize, 'left_arrow.png', 450, 200, settings_sprites)
        right_screensize = pygame.sprite.Sprite()
        create_sprite(right_screensize, 'right_arrow.png', 800, 200, settings_sprites)

        left_screenmode = pygame.sprite.Sprite()
        create_sprite(left_screenmode, 'left_arrow.png', 450, 250, settings_sprites)
        right_screenmode = pygame.sprite.Sprite()
        create_sprite(right_screenmode, 'right_arrow.png', 800, 250, settings_sprites)

        left_fps = pygame.sprite.Sprite()
        create_sprite(left_fps, 'left_arrow.png', 450, 300, settings_sprites)
        right_fps = pygame.sprite.Sprite()
        create_sprite(right_fps, 'right_arrow.png', 800, 300, settings_sprites)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if x.rect.collidepoint(event.pos):
                        return
                    elif left_screensize.rect.collidepoint(event.pos):
                        if self.value_screensize > 0:
                            self.value_screensize -= 1
                        else:
                            self.value_screensize = len(self.values_screensize) - 1
                    elif right_screensize.rect.collidepoint(event.pos):
                        if self.value_screensize < len(self.values_screensize) - 1:
                            self.value_screensize += 1
                        else:
                            self.value_screensize = 0
                    elif left_screenmode.rect.collidepoint(event.pos):
                        if self.value_screenmode > 0:
                            self.value_screenmode -= 1
                        else:
                            self.value_screenmode = len(self.values_screenmode) - 1
                    elif right_screenmode.rect.collidepoint(event.pos):
                        if self.value_screenmode < len(self.values_screenmode) - 1:
                            self.value_screenmode += 1
                        else:
                            self.value_screenmode = 0
                    elif left_fps.rect.collidepoint(event.pos):
                        if self.value_fps > 0:
                            self.value_fps -= 1
                        else:
                            self.value_fps = len(self.values_fps) - 1
                    elif right_fps.rect.collidepoint(event.pos):
                        if self.value_fps < len(self.values_fps) - 1:
                            self.value_fps += 1
                        else:
                            self.value_fps = 0
                    elif apply.rect.collidepoint(event.pos):
                        return self.apply()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_RETURN:
                        return self.apply()
            self.screen.fill((0, 0, 0))  # self.screen.blit(fon, (0, 0))

            settings_sprites.draw(self.screen)

            for i in [[f"Версия конфигурационного файла: {self.config['version']}",
                       (128, 128, 128), 50, 155, 25],
                      ["Размер экрана: ", (255, 255, 255), 50, 205, 50],
                      [self.values_screensize[self.value_screensize], (255, 255, 255), 500, 205, 50],
                      ["Режим экрана: ", (255, 255, 255), 50, 255, 50],
                      [self.values_screenmode[self.value_screenmode], (255, 255, 255), 500, 255, 50],
                      ["FPS: ", (255, 255, 255), 50, 305, 50],
                      [self.values_fps[self.value_fps], (255, 255, 255), 500, 305, 50]]:
                self.screen.blit(pygame.font.Font(None, i[4]).render(i[0], True, i[1]), (i[2], i[3]))

            pygame.display.flip()
            clock.tick(self.fps)
