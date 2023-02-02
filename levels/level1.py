from level import Level
import pygame
import random

class Level1(Level):
    def __init__(self):
        self.dirt = self.draw_dirt()
        self.sand = self.draw_sand()
        self.grass = self.draw_grass(self.dirt)
        self.cloud = self.draw_cloud()
        self.map = './levels/level1.txt'
        
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


# -----------------------------------------------------------------------------

    # This updates the color of a pixel by amount
    def update_color(self, surf, point, amount):
        color = surf.get_at(point)
        color[0] = self.clip(color[0] + amount[0], 0, 255)
        color[1] = self.clip(color[1] + amount[1], 0, 255)
        color[2] = self.clip(color[2] + amount[2], 0, 255)
        surf.set_at(point, color)

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