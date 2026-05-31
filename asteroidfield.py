from turtle import position

import pygame
import random
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.player = player

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
       pass

    def spawn_wave(self, wave_number):
        for _ in range(wave_number):
            edge = random.choice(self.edges)
            speed = random.randint(50, 110)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-45, 45))
            while True:
                position = edge[1](random.uniform(0, 1))
                if position.distance_to(self.player.position) > ASTEROID_SPAWN_DISTANCE_THRESHOLD:
                    break
            self.spawn(ASTEROID_MAX_RADIUS, position, velocity)
