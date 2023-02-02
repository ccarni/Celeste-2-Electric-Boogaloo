import pygame

class Grabber():
    def __init__(self, grace_period):
        self.grace_period = grace_period
        self.counter = 0
        self.grabbing = False
        self.holding_on = False
        self.can_grab = True

    def update_counter(self):
        self.counter -= 1

    def reset_counter(self, count = 5):
        self.counter = count
        self.can_grab = False
        self.holding_on = False