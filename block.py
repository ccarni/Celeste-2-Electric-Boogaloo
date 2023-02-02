import pygame
# Class for things that the player can collide with
class Block(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.copy()
        self.rect = image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.depth = 1

    def update(self, scroll = (0, 0)):
        self.rect.x = round(self.x - scroll[0])
        self.rect.y = round(self.y - scroll[1])

    def do_effect(self, player, value = 0):
        pass

    def collide_vertical(self, player):

        collided = ""
        # Collide on top
        if player.rect.bottom > self.rect.top and player.v > 0:
            player.rect.bottom = self.rect.top
            player.v = 0
            player.on_ground = True
            collided = "top"

        # Collide on bottom
        if player.rect.top < self.rect.bottom and player.v < 0:
            player.rect.top = self.rect.bottom
            player.v = 0
            collided = "bottom"
        return collided

    def collide_horizontal(self, player):
        collided = False
        # Collide with left side
        if player.rect.right > self.rect.left and player.horizontal_dir == 'right':
            player.rect.right = self.rect.left
            collided = True
        # Collide with right side
        if player.rect.left < self.rect.right and player.horizontal_dir == 'left':
            player.rect.left = self.rect.right
            collided = True
        return collided