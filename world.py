import pygame
import random
from background import Background
from block import Block
from spring import Spring
from spike import Spike
from sand import Sand
from ice import Ice
from level import Level
from levels.level1 import Level1 
from levels.level2 import Level2 
from levels.level3 import Level3
from levels.level4 import Level4

import os

class World():
    def __init__(self, graphics_quality):

        self.levels = [Level1(),  Level2(),  Level3(), Level4()]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        # Each tile is a square of pixels
        self.tilesize = 20
        self.graphics_quality = graphics_quality

        self.init_level()

    def next_level(self):
        if (self.current_level_index + 1 < len(self.levels)):
            self.current_level_index += 1
            self.current_level = self.levels[self.current_level_index]
            self.init_level()
        

    def init_level(self):
        self.graphics_quality = self.graphics_quality

        self.current_level.initialize_world()

        # Make all the tiles the right size
        self.cloud = pygame.transform.smoothscale(self.current_level.cloud, (self.tilesize, self.tilesize))
        self.dirt = pygame.transform.smoothscale(self.current_level.dirt, (self.tilesize, self.tilesize))
        self.grass = pygame.transform.smoothscale(self.current_level.grass, (self.tilesize, self.tilesize))
        self.spring = pygame.transform.smoothscale(self.current_level.draw_spring(), (self.tilesize, self.tilesize/2))
        self.spike = pygame.transform.smoothscale(self.current_level.draw_spike(), (self.tilesize, self.tilesize/2))
        self.sand = pygame.transform.smoothscale(self.current_level.sand, (self.tilesize, self.tilesize))
        self.ice = pygame.transform.scale(self.current_level.ice, (self.tilesize, self.tilesize))

        # Read in the level.txt file to determine the placement of blocks
        with open(self.current_level.map, 'r') as raw_level:
            self.block_grid = raw_level.read()
        self.block_grid = self.block_grid.split('\n')

        # How many blocks big the level will be
        self.level_size = (self.tilesize*len(self.block_grid[0]), self.tilesize*len(self.block_grid))

        self.objs = []
        # Make the clouds
        for i in range(int(20 * self.graphics_quality)):
            x = random.randint(0, self.level_size[0]//self.tilesize)
            y = random.randint(0, self.level_size[1]//self.tilesize//2)
            c = Background(self.cloud, x*self.tilesize, y*self.tilesize)
            c.depth = random.uniform(0.5, 1)
            self.objs.append(c)

        # Make the mountains (which look more like trees)
        for i in range(int(1000 * self.graphics_quality)):
            x = random.randint(0, self.level_size[0])
            y = random.randint(10, 2*self.level_size[1]//3)
            w = random.randint(10, 100)
            mountain = self.draw_mountain(w, self.level_size[1]-y)
            m = Background(mountain, x, y)
            m.depth = random.uniform(0.25, 0.5)
            temp_surf = pygame.Surface(mountain.get_size()).convert_alpha()
            temp_surf.fill((0,0,0,255*m.depth))
            m.image.blit(temp_surf, (0,0))
            m.image.set_colorkey((0,0,0))
            self.objs.append(m)

        moon = self.current_level.draw_moon()
        m = Background(moon, 200, 10)
        m.depth = 0.1 # This depth controls the parallax - smaller is slower
        self.objs.append(m)

        # Draw the stars
        for i in range(int(200 * self.graphics_quality)):
            star = self.draw_star()
            x = random.randint(0, self.level_size[0])
            y = random.randint(0, self.level_size[1])
            s = Background(star, x, y)
            s.depth = random.uniform(0, 0.01)
            self.objs.append(s)

        # Go through the block_grid and add the blocks to the group of blocks
        self.blocks = pygame.sprite.Group()
        for row in range(len(self.block_grid)):
            for col in range(len(self.block_grid[row])):
                if self.block_grid[row][col] == 'd':
                    d = Block(self.dirt, col*self.tilesize, row*self.tilesize)
                    self.blocks.add(d)
                if self.block_grid[row][col] == 'g':
                    g = Block(self.grass, col*self.tilesize, row*self.tilesize)
                    self.blocks.add(g)
                if self.block_grid[row][col] == 's':
                    s = Spring(self.spring, col*self.tilesize, row*self.tilesize + self.tilesize/2, 10)
                    self.blocks.add(s)
                if self.block_grid[row][col] == 'x':
                    x = Spike(self.spike, col*self.tilesize, row*self.tilesize + self.tilesize/2)
                    self.blocks.add(x)
                if self.block_grid[row][col] == 'S':
                    S = Sand(self.sand, col*self.tilesize, row*self.tilesize + self.tilesize/2)
                    self.blocks.add(S)
                if self.block_grid[row][col] == 'i':
                    i = Ice(self.ice, col*self.tilesize, row*self.tilesize)
                    self.blocks.add(i)

        # Draw the background objects so that further away objects are behind closer ones
        self.objs.sort(key=lambda x: x.depth)

    def draw_dirt(self):
        surf = pygame.Surface((5, 5))
        surf.fill((220, 220, 220))
        for i in range(surf.get_width()):
            for j in range(surf.get_width()):
                amount = [random.randint(-10, 10) for i in range(3)]
                #self.update_surrounding(surf, i, j, amount)
        return surf

    def draw_sand(self):
        surf = pygame.Surface((5, 5))
        surf.fill((237, 215, 92))
        for i in range(surf.get_width()):
            for j in range(surf.get_width()):
                amount = [random.randint(-1, 1) for i in range(3)]
                self.update_surrounding(surf, i, j, amount)
        return surf

    def draw_grass(self, dirt):
        surf = dirt.copy()
        grass_rect = pygame.Rect(0, 0, surf.get_width(), round(surf.get_width()*0.3))
        pygame.draw.rect(surf, (255, 255, 255), grass_rect)
        for i in range(surf.get_width()):
            for j in range(grass_rect.height):
                amount = [random.randint(-1, 1) for i in range(3)]
                self.update_adjacent(surf, i, j, amount)
        return surf

    def draw_cloud(self):
        surf = pygame.Surface((5, 5)).convert_alpha()
        surf.fill((255, 255, 255, 100)) # (red, green, blue, alpha)
        for i in range(surf.get_width()):
            for j in range(surf.get_width()):
                amount = [random.randint(-10, 10) for i in range(3)]
                self.update_surrounding(surf, i, j, amount)
        return surf

    def draw_mountain(self, width, height):
        surf = pygame.Surface((width, height)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        pygame.draw.polygon(surf, (250, 255, 250), [(0, surf.get_height()), (surf.get_width(), surf.get_height()), (surf.get_width()/2, 0)])
        return surf

    def draw_spring(self):
        surf = pygame.Surface((20, 10)).convert_alpha()
        surf.fill((0,0,0,0))
        #r = round(surf.get_height()/1.5) # Round the corners of the spring
        pygame.draw.rect(surf, (150, 0, 0), surf.get_rect())
        pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), width=1)
        return surf

    def draw_spring_round(self):
        surf = pygame.Surface((20, 10)).convert_alpha()
        surf.fill((0,0,0,0))
        r = round(surf.get_height()/1.5) # Round the corners of the spring
        pygame.draw.rect(surf, (255, 0, 0), surf.get_rect(), border_top_left_radius=r, border_top_right_radius=r)
        pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), border_top_left_radius=r, border_top_right_radius=r, width=1)
        return surf


    def draw_spike(self):
        surf = pygame.Surface((20, 10)).convert_alpha()
        surf.fill((0,0,0,0))
        
        w = surf.get_width()
        w3 = surf.get_width()/3
        w2 = surf.get_width()/2
        w6 = surf.get_width()/6
        pygame.draw.polygon(surf, (255, 255, 255), [(0, surf.get_height()), (w3, surf.get_height()), (w6, 0)])
        pygame.draw.polygon(surf, (255, 255, 255), [(w3, surf.get_height()), (w3*2, surf.get_height()), (w2, 0)])
        pygame.draw.polygon(surf, (255, 255, 255), [(w3*2, surf.get_height()), (w, surf.get_height()), (w - w6, 0)])
        return surf

    def draw_creature(self):
        surf = pygame.Surface((16, 36))
        pygame.draw.rect(surf, (1, 1, 1), pygame.Rect(1, 5, 14, 14), border_radius=(2))
        pygame.draw.rect(surf, (1, 1, 1), pygame.Rect(3, 15, 4, 22), border_radius=(2))
        pygame.draw.rect(surf, (1, 1, 1), pygame.Rect(9, 15, 4, 22), border_radius=(2))
        pygame.draw.rect(surf, (255, 255, 255), pygame.Rect(2, 6, 12, 12), border_radius=(2))
        pygame.draw.rect(surf, (255, 255, 255), pygame.Rect(4, 16, 2, 20), border_radius=(2))
        pygame.draw.rect(surf, (255, 255, 255), pygame.Rect(10, 16, 2, 20), border_radius=(2))
        pygame.draw.rect(surf, (1, 1, 1), pygame.Rect(3, 6, 2, 2))
        pygame.draw.rect(surf, (1, 1, 1), pygame.Rect(11, 6, 2, 2))
        pygame.draw.line(surf, (1, 1, 1),(4, 9), (11, 9))
        surf.set_colorkey((0,0,0))
        return surf

    def draw_moon(self):
        moon = pygame.Surface((100, 100)).convert_alpha()
        moon.fill((0, 0, 0, 0))
        pygame.draw.ellipse(moon, (200, 200, 200), moon.get_rect())
        for i in range(moon.get_width()):
            for j in range(moon.get_width()):
                amount = [random.randint(-10, 10)]*3 # This duplicates the number three times to ensure we don't get colors
                self.update_surrounding(moon, i, j, amount)
        return moon

    def draw_star(self):
        star = pygame.Surface((1, 1))
        star.fill((255, 255, 255))
        return star
        # what a function this one is


    # This updates the color of a pixel by amount
    def update_color(self, surf, point, amount):
        color = surf.get_at(point)
        color[0] = self.clip(color[0] + amount[0], 0, 255)
        color[1] = self.clip(color[1] + amount[1], 0, 255)
        color[2] = self.clip(color[2] + amount[2], 0, 255)
        surf.set_at(point, color)

    # This helps smooth over random noise to (hopefully) improve quality of the images
    def update_surrounding(self, surf, i, j, amount):
        self.update_color(surf, (i, j), amount)

        amount2 = [amount[i] // 1 for i in range(3)]
        right = ((i + 1) % surf.get_width(), j)
        left = ((i - 1 + surf.get_width()) % surf.get_width(), j)
        up = (i, (j - 1 + surf.get_height()) % surf.get_height())
        down = (i, (j + 1) % surf.get_height())
        self.update_color(surf, right, amount2)
        self.update_color(surf, left, amount2)
        self.update_color(surf, up, amount2)
        self.update_color(surf, down, amount2)


    # This only does horizontal updates for the grass
    def update_adjacent(self, surf, i, j, amount):
        self.update_color(surf, (i, j), amount)

        amount2 = [amount[i] // 1 for i in range(3)]
        right = ((i + 1) % surf.get_width(), j)
        left = ((i - 1 + surf.get_width()) % surf.get_width(), j)
        self.update_color(surf, right, amount2)
        self.update_color(surf, left, amount2)


    # Restricts an input number to between a lower and upper bound
    def clip(self, number, lower, upper):
        number = max(lower, number)
        number = min(upper, number)
        return number
