import pygame
from circleshape import CircleShape
from constants import *

class EnemyShip(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.lower_points = [
            pygame.Vector2(-1.5 * self.radius, 0),
            pygame.Vector2(1.5 * self.radius, 0),
            pygame.Vector2(1 * self.radius, (0.5 * self.radius)),
            pygame.Vector2(-1 * self.radius, (0.5 * self.radius)),
        ]
        self.middle_points = [
            pygame.Vector2(-1.55 * self.radius, (self.radius * -0.2)),
            pygame.Vector2(1.55 * self.radius, (self.radius * -0.2)),
            pygame.Vector2(1.55 * self.radius, 0),
            pygame.Vector2(-1.55 * self.radius, 0),
        ]
        self.upper_points = [
            pygame.Vector2(-1 * self.radius, (self.radius * -0.7)),
            pygame.Vector2(1 * self.radius, (self.radius * -0.7)),
            pygame.Vector2(1.5 * self.radius, (self.radius * -0.2)),
            pygame.Vector2(-1.5 * self.radius, (self.radius * -0.2)),
        ]
        self.dome_points = [
            pygame.Vector2(-0.25 * self.radius, (self.radius * -0.95)),
            pygame.Vector2(0.25 * self.radius, (self.radius * -0.95)),
            pygame.Vector2(0.80 * self.radius, (self.radius * -0.70)),
            pygame.Vector2(-0.80 * self.radius, (self.radius * -0.70)),
        ]
        

    def move(self):
        pass

    def draw(self, screen):
        lower_offset_points = []
        for point in self.lower_points:
            lower_offset_points.append(self.position + point)
        pygame.draw.polygon(screen, "white", lower_offset_points, width=LINE_WIDTH)
        middle_offset_points = []
        for point in self.middle_points:
            middle_offset_points.append(self.position + point)
        pygame.draw.polygon(screen, "white", middle_offset_points, width=LINE_WIDTH)
        upper_offset_points = []
        for point in self.upper_points:
            upper_offset_points.append(self.position + point)
        pygame.draw.polygon(screen, "white", upper_offset_points, width=LINE_WIDTH)
        dome_offset_points = []
        for point in self.dome_points:
            dome_offset_points.append(self.position + point)
        pygame.draw.polygon(screen, "white", dome_offset_points, width=LINE_WIDTH)

