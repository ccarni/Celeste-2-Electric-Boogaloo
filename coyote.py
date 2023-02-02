import pygame

class Coyote():
    def __init__(self, frames=4):
        self.frames = frames
        self.max_frames = frames
        self.coyoting = False

    def update_coyote(self):
        if self.frames > 0:
            self.frames -= 1
        if self.frames > 0:
            self.coyoting = True
            return True
        else:
            self.coyoting = False
    
    def reset(self):
        self.frames = self.max_frames