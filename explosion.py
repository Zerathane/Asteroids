import pygame
from circleshape import *
from constants import *
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.lifetime = EXPLOSION_LIFETIME_SECONDS
        self.dot_positions = []
        self.dot_velocities = []
        for i in range(EXPLOSION_DOT_COUNT):
            x_offset = random.uniform(-self.radius, self.radius)
            y_offset = random.uniform(-self.radius, self.radius)
            self.dot_positions.append(pygame.Vector2(x_offset, y_offset))
            velocity = pygame.Vector2(x_offset, y_offset).normalize() * EXPLOSION_DOT_SPEED
            self.dot_velocities.append(velocity)

    def update(self, dt):
        for i, (position, velocity) in enumerate(zip(self.dot_positions, self.dot_velocities)):
            self.dot_positions[i] += velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        offset_dot_positions = []
        for dot_position in self.dot_positions:
            offset_dot_positions.append(self.position + dot_position)
        for offset_dot_position in offset_dot_positions:
            pygame.draw.circle(screen, "white", offset_dot_position, 1)
        