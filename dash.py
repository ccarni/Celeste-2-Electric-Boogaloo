import pygame
import time

class Dash():
    def __init__(self, dashtime, runner):
        self.dashtime = dashtime
        self.dashcount = 0
        self.runner = runner

        self.direction = [0, 0]

        self.dashing = False

    def execute_dash(self, dir):
        self.dashcount = self.dashtime
        self.dashing = True
        self.direction = dir

    def update(self):
        dt = self.runner.tick

        if (self.dashcount <= 0):
            self.dashing = False
            self.runner.player.h = 0
        else:
            self.dashcount -= dt
            self.runner.player.h = self.direction[0] * self.runner.player.dash_speed * dt * self.runner.gamespeed
            self.runner.player.v = self.direction[1] * self.runner.player.dash_speed * dt * self.runner.gamespeed
        
        