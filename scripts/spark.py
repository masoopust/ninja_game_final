import math

import pygame

class Spark:
    def __init__(self, pos, angle, speed): # potřebujeme jen pozici, úhel a rychlost
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        
    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed      # letí po cosinu a sinu za střelou
        self.pos[1] += math.sin(self.angle) * self.speed
        
        self.speed = max(0, self.speed - 0.1)     # spark (diamant) se zmenšuje, jak zpomaluje
        return not self.speed
    
    def render(self, surf, offset=(0, 0)):
        render_points = [        # renderuje se jen v určitých bodech, které se počítají ze sinu a cosinu
            (self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[0], self.pos[1] + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle + math.pi) * self.speed * 3 - offset[1]),
            (self.pos[0] + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[0], self.pos[1] + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[1]),
        ]
        
        pygame.draw.polygon(surf, (255, 255, 255), render_points)