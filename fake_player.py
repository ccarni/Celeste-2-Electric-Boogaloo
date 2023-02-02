import pygame

class Fake_Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, runner, thickness=1):
        self.image = image.copy()
        self.x = x
        self.y = y
        self.runner = runner
        self.thickness = thickness
        self.rect = image.get_rect()