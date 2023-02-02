import pygame
import numpy as lmao
import random
from block import Block
from player import Player
from spring import Spring
from background import Background
from world import World
from snow import Snow

class Runner():
    def __init__(self, screen):


        self.counter_at_jump = 0

        self.jump_input = False
        self.max_jump_time = 4
        self.jump_timer = self.max_jump_time

        self.screen = screen
        self.graphics_quality = 2

        # Speedrun Time
        self.speedrun_time = 0


        self.snow = Snow(100, self.screen.get_width())

        # NOT FULL SCREEN

        self.display = pygame.display.set_mode()#flags=pygame.FULLSCREEN)

        self.world = World(self.graphics_quality)

        #OTHER INIT STUFF.  PROBABLY MAKE THIS INTO A SEPARATE CLASS PLEASE

        
        # We render everything on screen, then upscale it to display
        # this lets us get better performance at the cost of image quality
        
        self.counter = 0

        self.next_level_cooldown = 100

        p = self.draw_player()
        self.player = Player(p, 0, 0, self)


        self.gamespeed = 0.75

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.running = True
        self.true_scroll = [0, 0]
        self.scroll = [0, 0]

        self.tick = 0 # The tick that updates once every frame


        self.player.rect.y = self.world.level_size[1] - 100
        
    # You should make this cooler
    def draw_player(self):
        surf = pygame.Surface((10, 10))
        try:
            surf.fill(self.player.color)
            pygame.draw.rect(surf, (255, 255, 255), pygame.Rect(0, 0, 10, 10), 3)
        except:
            surf.fill((255, 0, 0)) # If player is not established yet
            pygame.draw.rect(surf, (255, 255, 255), pygame.Rect(0, 0, 10, 10), 3)
        return surf


    def update(self):
        self.tick = self.clock.tick(self.fps)

        if self.next_level_cooldown > 0:
            self.next_level_cooldown -= 1
        
        self.counter += 1
        right_weight = 1.2

        current_direction = [0, 0]
        
        self.speedrun_time = pygame.time.get_ticks()

        if self.jump_timer > 0:
            self.jump_timer -= 1
        if self.jump_timer <= 0:
            self.jump_input = False

        keys = pygame.key.get_pressed()

        # If friction is Zero, i.e. on ice
        if self.player.friction != 0:
            self.player.horizontal_dir = None
        
            
        self.player.vertical_dir = None
        if keys[pygame.K_LEFT]:

            self.player.horizontal_dir = 'left'
            if self.player.rect.x < 0:
                self.player.rect.x = 0
            current_direction[0] = -1
        if keys[pygame.K_RIGHT]:
            self.player.horizontal_dir = 'right'
            if self.player.rect.right-self.scroll[0] > self.screen.get_width():
                self.player.rect.right = self.screen.get_width() + self.scroll[0]

                if self.next_level_cooldown == 0:
                    self.player.rect.x = 0
                    self.player.rect.y = self.world.level_size[1] - 100
                    self.true_scroll = [0, 0]
                    self.scroll = [0, 0]
                    self.world.next_level() # NEXT LEVEL
                    self.next_level_cooldown = 100
            current_direction[0] = 1
        if keys[pygame.K_UP]:
            self.player.vertical_dir = 'up'
            current_direction[1] = -0.7
        if keys[pygame.K_DOWN]:
            self.player.vertical_dir = 'down'
            current_direction[1] = 1
        if keys[pygame.K_z]:
            self.player.grabber.grabbing = True
        else:
            self.player.grabber.grabbing = False


        #Do horizontal movement
        if not self.player.grabber.holding_on:
            if self.player.horizontal_dir == 'left':
                if not self.player.dasher.dashing:
                    self.player.rect.x -= 5 * self.gamespeed * self.player.speedMod 
            if self.player.horizontal_dir == 'right':
                if not self.player.dasher.dashing:
                    self.player.rect.x += 5 * self.gamespeed * self.player.speedMod + 1
            
        # Temporary jumping variable for jumping on walls
        jumping = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if (event.key == pygame.K_c):
                    self.jump_input = True
                    self.jump_timer = self.max_jump_time
                if event.key == pygame.K_x:
                    self.player.dash(current_direction)
                    self.player.grabber.reset_counter()
                    self.player.grabber.grabbing = False
          
        if (self.player.coyote.coyoting or self.player.grabber.holding_on):
            if (self.player.coyote.coyoting) and self.jump_input:
                self.player.v = -self.player.jump_height
                jumping = True
                self.player.grabber.reset_counter()
                self.player.grabber.grabbing = False
                self.player.friction = 1


        # Reset the player if they fall
        if self.player.rect.y > self.world.level_size[1]:
            self.player.rect.x = 0
            self.player.rect.y = 0

        # The camera magic :)
        # Every object moves based on the scroll variable
        # The scroll variable updates based on how far from the player the center of the screen is
        self.true_scroll[0] += (self.player.rect.x - self.true_scroll[0] - self.screen.get_width()/2)/20
        self.true_scroll[1] += (self.player.rect.y - self.true_scroll[1] - self.screen.get_height()/2) / 20

        # Casting to an integer when using the scroll improves the quality
        self.scroll[0] = int(self.true_scroll[0])
        self.scroll[1] = int(self.true_scroll[1])

        # Block scrolling on reaching level boundaries
        if self.scroll[0] < 0:
            self.scroll[0] = 0
        if self.scroll[0] + self.screen.get_width() > len(self.world.block_grid[0])*self.world.tilesize:
            self.scroll[0] = len(self.world.block_grid[0])*self.world.tilesize - self.screen.get_width()

        if self.scroll[1] < 0:
            self.scroll[1] = 0
        if self.scroll[1] + self.screen.get_height() > len(self.world.block_grid)*self.world.tilesize:
            self.scroll[1] = len(self.world.block_grid)*self.world.tilesize - self.screen.get_height()


        # Update block and background locations
        for obj in self.world.objs:
            obj.update(self.scroll)
        self.world.blocks.update(self.scroll)

        # Convert the player coordinates to world coordinates
        self.player.rect.x -= self.scroll[0]
        self.player.rect.y -= self.scroll[1]


        # Set max_fall to default so that it can slow
        self.player.max_fall = self.player.max_fall_default

        if jumping and self.player.grabber.holding_on:
            self.player.grabber.grabbing = False
            self.player.grabber.holding_on = False

        # Update dash before horizontal collision
        self.player.update_dash()
        

        # Check horizontal ball-et heck
        # Doing things this way avoids issues where the collision occurs on a corner of the block
        # so that there isn't confusion over whether to place the player above the block or to the side
        self.player.on_ground = False
        collides = pygame.sprite.spritecollide(self.player, self.world.blocks, dokill=False)
        collided_with_any = False
        for block in collides:
            self.player.grabber.holding_on = False
            collided = block.collide_horizontal(self.player)
            self.player.h = 0
            self.player.on_ground = True
            if collided:
                collided_with_any = True
                self.player.max_fall = int(self.player.max_fall_default / 2)
                if self.player.grabber.grabbing and self.player.grabber.can_grab:
                    self.player.grabber.holding_on = True
                else:
                    self.player.grabber.holding_on = False
                

        if ((not self.player.grabber.grabbing) and (self.player.grabber.holding_on)):
            self.player.grabber.holding_on = False
            
        if self.player.grabber.holding_on and self.player.grabber.can_grab:
            self.player.max_fall = 0
            self.player.coyote.reset()
            
            
    

        # Reset speed mod before it is changed. In case it does not change, it will be the default (1)
        self.player.speedMod = 1 * self.gamespeed

        # Update y position and check vertical ball-et heck
        self.player.update_y(self.scroll)
        self.player.update()
        self.player.update_dash_y()

        climb_height = 0
        

        if self.player.vertical_dir == 'down':
            climb_height = self.player.climbing_speed
        if self.player.vertical_dir == 'up':
            climb_height = -self.player.climbing_speed

        if self.colliding_slightly(climb_height):
            if self.player.grabber.holding_on:
                self.player.rect.y += climb_height

        collides = pygame.sprite.spritecollide(self.player, self.world.blocks, dokill=False)
        for block in collides:
            collided = block.collide_vertical(self.player)
            if collided == "top":
                self.player.coyote.reset()
            self.player.friction = 1
            block.do_effect(self.player, 0)
            self.player.h = 0
            self.player.can_dash = True
            

        # Convert the world coordinates back to player coordinates
        self.player.rect.x += self.scroll[0]
        self.player.rect.y += self.scroll[1]

    def colliding_slightly(self, height = 1):
        c_rect = self.player.fake_player.rect
        
        self.player.update_fake_player(-height)
        collides = pygame.sprite.spritecollide(self.player.fake_player, self.world.blocks, dokill=False)
        if len(collides) > 0:
            return True
        return False


    def draw(self):
        self.screen.fill((0, 0, 50))
        for obj in self.world.objs:
            self.screen.blit(obj.image, obj.rect)
        self.world.blocks.draw(self.screen)
        self.screen.blit(self.player.image, (self.player.rect.x-self.scroll[0], self.player.rect.y-self.scroll[1]))
        s = pygame.transform.scale(self.screen, self.display.get_size())
        self.display.blit(s, (0, 0))
        #snow = pygame.Surface((1, 1))
        #snow.fill((255, 255, 255))
        
        self.draw_speedrun(self.screen)

        for i in range(self.snow.snow_ammount):
            pass
            #self.snow.update(2)
            #self.screen.blit(snow, pygame.Rect(random.randint(0,self.screen.get_width()), self.snow.snows[i][1], 1, 1))
        pygame.display.update()


    def draw_speedrun(self, screen):
        millis = self.speedrun_time
        millis = int(millis)
        millis_fancy = (millis + 1000) % 1000
        seconds=(millis/1000)%60
        seconds = int(seconds)
        minutes=(millis/(1000*60))%60
        minutes = int(minutes)
        hours=(millis/(1000*60*60))%24

        millis_fancier = str(millis_fancy)
        if len(millis_fancier) == 1:
            millis_fancier = millis_fancier + "00"
        if len(millis_fancier) == 2:
            millis_fancier = millis_fancier + "0"

        time_string = "%d:%d:%d" % (minutes, seconds, int(millis_fancier))

        timer_font = pygame.font.SysFont("monospace", 30)

        surf_speedrun = timer_font.render(str(time_string), True, (255, 255, 255))

        
        big_size = self.screen.get_size()

        text_size3 = surf_speedrun.get_size()

        x3 = big_size[0] - text_size3[0] * 1.5
        y3 = 0 + text_size3[1] * 1.5

        self.screen.blit(surf_speedrun, (x3,y3))
        self.final_time = time_string