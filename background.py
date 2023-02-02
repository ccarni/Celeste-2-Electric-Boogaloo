import pygame


# A class for things that appear exclusively in the background
# (Trees, stars, the moon)
class Background(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.copy()
        self.rect = image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.depth = 1

    def update(self, scroll):
        self.rect.x = round(self.x - scroll[0] * self.depth)
        self.rect.y = round(self.y - scroll[1] * self.depth)