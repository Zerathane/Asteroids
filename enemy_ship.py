import pygame
from circleshape import CircleShape

class EnemyShip(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def move(self):
        pass

    def draw(self, screen):
        lower_top_left = self.position + pygame.Vector2(-1.5 * self.radius, 0)
        lower_top_right = self.position + pygame.Vector2(1.5 * self.radius, 0)
        lower_bottom_right = self.position + pygame.Vector2(1 * self.radius, (0.5 * self.radius))
        lower_bottom_left = self.position + pygame.Vector2(-1 * self.radius, (0.5 * self.radius))
        pygame.draw.polygon(screen, "white", [lower_top_left, lower_top_right, lower_bottom_right, lower_bottom_left], 2)
        middle_top_left = self.position + pygame.Vector2(-1.55 * self.radius, (self.radius * -0.2))
        middle_top_right = self.position + pygame.Vector2(1.55 * self.radius, (self.radius * -0.2))
        middle_bottom_left = self.position + pygame.Vector2(-1.55 * self.radius, 0)
        middle_bottom_right = self.position + pygame.Vector2(1.55 * self.radius, 0)
        pygame.draw.polygon(screen, "white", [middle_top_left, middle_top_right, middle_bottom_right, middle_bottom_left], 2)
        upper_top_left = self.position + pygame.Vector2(-1 * self.radius, (self.radius * -0.7))
        upper_top_right = self.position + pygame.Vector2(1 * self.radius, (self.radius * -0.7))
        upper_bottom_right = self.position + pygame.Vector2(1.5 * self.radius, (self.radius * -0.2))
        upper_bottom_left = self.position + pygame.Vector2(-1.5 * self.radius, (self.radius * -0.2))
        pygame.draw.polygon(screen, "white", [upper_top_left, upper_top_right, upper_bottom_right, upper_bottom_left], 2)
        dome_top_left = self.position + pygame.Vector2(-0.25 * self.radius, (self.radius * -0.95))
        dome_top_right = self.position + pygame.Vector2(0.25 * self.radius, (self.radius * -0.95))
        dome_bottom_right = self.position + pygame.Vector2(0.80 * self.radius, (self.radius * -0.70))
        dome_bottom_left = self.position + pygame.Vector2(-0.80 * self.radius, (self.radius * -0.70))
        pygame.draw.polygon(screen, "white", [dome_top_left, dome_top_right, dome_bottom_right, dome_bottom_left], 2)
        
        