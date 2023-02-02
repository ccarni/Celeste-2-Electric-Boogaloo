import pygame
import random
import runner
from block import Block
from runner import Runner

pygame.init()



screen = pygame.Surface((320, 180))
runner = Runner(screen)

while runner.running:
    runner.update()
    runner.draw()
