import pygame
from block import Block

# A sublcass of block as an example of how to create special objects
class Ice(Block):
    def __init__(self, image, x, y, strength=15):
        Block.__init__(self, image, x, y)
        self.strength = strength

    def collide_vertical(self, player):
        # Collide on top
        if player.rect.bottom > self.rect.top and player.v > 0:
            player.rect.bottom = self.rect.top
            player.v = 0
            player.on_ground = True

        # Collide on bottom
        if player.rect.top < self.rect.bottom and player.v < 0:
            player.rect.top = self.rect.bottom
            player.v = 0

    def do_effect(self, player, value = 0):
        player.friction = 0
        # print('slippy')

    def collide_horizontal(self, player):
        # Collide with left side
        if player.rect.right > self.rect.left and player.horizontal_dir == 'right':
            player.rect.right = self.rect.left
        # Collide with right side
        if player.rect.left < self.rect.right and player.horizontal_dir == 'left':
            player.rect.left = self.rect.right
