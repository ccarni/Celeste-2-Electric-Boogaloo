import pygame
from block import Block

# A sublcass of block as an example of how to create special objects
class Spike(Block):
    def __init__(self, image, x, y, strength=15):
        Block.__init__(self, image, x, y)
        self.strength = strength

    def collide_vertical(self, player):
        # Collide on bottom
        if player.rect.top < self.rect.bottom and player.v < 0:
            player.rect.top = self.rect.bottom
            player.v = 0

    def collide_horizontal(self, player):
        

        #RESET
        player.rect.x = 0
        player.rect.y = 0