from symtable import Class

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

class ShipExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.lifetime = SHIP_EXPLOSION_LIFETIME_SECONDS
        self.radius = SHIP_EXPLOSION_RADIUS
        self.dot_positions = []
        self.dot_velocities = []
        for i in range(SHIP_EXPLOSION_LINE_COUNT):
            x_offset1 = random.uniform(-self.radius, self.radius)
            x_offset2 = random.uniform(-self.radius, self.radius)
            y_offset1 = random.uniform(-self.radius, self.radius)
            y_offset2 = random.uniform(-self.radius, self.radius)
            point_a = pygame.Vector2(x_offset1, y_offset1)
            point_b = pygame.Vector2(x_offset2, y_offset2)
            self.dot_positions.append((point_a, point_b))
            midpoint = (point_a + point_b) / 2
            velocity_a = midpoint.normalize() * SHIP_EXPLOSION_SPEED
            
            self.dot_velocities.append(velocity_a)

    def update(self, dt):
        for i, ((position_a, position_b), velocity_a) in enumerate(zip(self.dot_positions, self.dot_velocities)):
            self.dot_positions[i] = (position_a + velocity_a * dt, position_b + velocity_a * dt)
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        offset_dot_positions = []
        for position_a, position_b in self.dot_positions:
            offset_dot_positions.append((self.position + position_a, self.position + position_b))
        for offset_position_a, offset_position_b in offset_dot_positions:
            pygame.draw.line(screen, "white", offset_position_a, offset_position_b, 2)
