import pygame
from block import Block

# A sublcass of block as an example of how to create special objects
class Spring(Block):
    def __init__(self, image, x, y, strength=15):
        Block.__init__(self, image, x, y)
        self.strength = strength

    def collide_vertical(self, player):
        # Collide on bottom
        if player.rect.top < self.rect.bottom and player.v < 0:
            player.rect.top = self.rect.bottom
            player.v = 0


    def do_effect(self, player, value=0):
        player.v = -self.strength
        player.rect.bottom = self.rect.top