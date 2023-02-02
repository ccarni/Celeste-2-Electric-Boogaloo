import pygame
from block import Block
from dash import Dash
from grabber import Grabber
from coyote import Coyote
from fake_player import Fake_Player


# The player!
class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, runner):
        pygame.sprite.Sprite.__init__(self)

        self.grabber = Grabber(5)

        self.coyote = Coyote(frames=4)

        self.runner = runner

        self.can_dash = False        

        self.speedMod = 1
        self.friction = 1


        # MOVEMENT PARAMETERS

        # Dash speed
        self.dash_speed = 0.4
        # Jump height
        self.jump_height = 7
        # Climbing ppeed
        self.climbing_speed = 1

        self.color = (255, 0, 0)
        self.color_default = (255, 0, 0)
        self.color_dash = (100, 100, 255)
        self.color_dashed = (80, 80, 245)
        self.color_grabbing = (80, 245, 80)
        self.color_holding_on = (80, 205, 80)

        self.image = image.copy()
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.depth = 1
        self.v = 0
        self.h = 0
        self.a = 1 # Acceleration due to gravity
        self.max_fall_default = 5
        self.max_fall = self.max_fall_default
        self.on_ground = False
        self.horizontal_dir = None # This is useful for determining ball-et heck
        self.vertical_dir = None # CLIMBING
        self.dasher = Dash(250, self.runner)


        # Fake player for extra ball-et heck
        self.fake_player = Fake_Player(self.image, x, y, self.runner, thickness=1)


    def update(self):
        if (self.dasher.dashing):
            self.update_color(self.color_dash)
        elif self.can_dash:
            self.update_color(self.color_default)
        elif not self.can_dash:
            self.update_color(self.color_dashed)
            

        self.coyote.update_coyote()
        
    def update_dash(self):
        if (self.dasher.dashing):
            self.dasher.update()
            
        if self.dasher.dashing:
            self.rect.x += self.h * self.runner.gamespeed
            
    def update_dash_y(self):
            
        if self.dasher.dashing:
            self.rect.y += self.v * self.runner.gamespeed



    # What would be update_x happens inline in the draw/update loop
    def update_y(self, scroll=(0, 0)):
        if not self.dasher.dashing:
            if (self.runner.counter % 2 == 0):
                self.v += self.a
            if self.v > self.max_fall:
                self.v = self.max_fall
            self.rect.y += self.v
            if self.v > 0 and self.grabber.counter <= 0:
                self.grabber.can_grab = True
        self.grabber.update_counter()

    def dash(self, dir):
        if self.can_dash:
            self.dasher.execute_dash(dir)
            self.can_dash = False

    def update_color(self, col):
        surf = pygame.Surface((10, 10))
        surf.fill(col)
        pygame.draw.rect(surf, (255, 255, 255), pygame.Rect(0, 0, 10, 10), 1)
        self.image = surf.copy()

    def update_fake_player(self, height):
        # Update fake player rect
        c_rect = self.rect
        self.fake_player.rect.x = self.rect.x - self.fake_player.thickness
        self.fake_player.rect.y = self.rect.y - self.fake_player.thickness - height * 4
        self.fake_player.rect.width = self.rect.width + self.fake_player.thickness * 2
        self.fake_player.rect.height = self.rect.height + self.fake_player.thickness * 2