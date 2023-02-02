import pygame
import random

class Snow():
    def __init__(self, snow_ammount, width):
        self.snow_ammount = snow_ammount
        self.snows = []
        for i in range(snow_ammount):
            self.snows.append([random.randint(0, width), 0])

    def move_all(self, x):
        for i in range(len(self.snows) - 1):
            self.snows[i][0] += x

    def update(self, wiggle):
        for i in range(len(self.snows) - 1):
            self.snows[i][0] += random.randint(-wiggle, wiggle)