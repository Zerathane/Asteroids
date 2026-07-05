import pygame
from constants import *
from game_state import *
from enemy_saucer import EnemySaucer

class SaucerManager(pygame.sprite.Sprite):
    def __init__(self, game_state, saucers, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.game_state = game_state
        self.spawn_timer = ENEMY_SAUCER_SPAWN_RATE_SECONDS
        self.saucers = saucers
        self.player = player
        

    def update(self, dt):
        if len(self.saucers) == 0:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                side = random.choice(["left", "right"])
                if side == "left":
                    spawn_x = -ENEMY_SAUCER_LARGE_RADIUS
                else:
                    spawn_x = SCREEN_WIDTH + ENEMY_SAUCER_LARGE_RADIUS
                spawn_y = random.uniform(0, SCREEN_HEIGHT)
                self.spawn_timer = ENEMY_SAUCER_SPAWN_RATE_SECONDS
                if self.game_state.wave_number <3:
                    EnemySaucer(spawn_x, spawn_y, ENEMY_SAUCER_LARGE_RADIUS, "large", side, self.player)
                else:
                    EnemySaucer(spawn_x, spawn_y, ENEMY_SAUCER_SMALL_RADIUS, "small", side, self.player)

    def reset(self):
        self.spawn_timer = ENEMY_SAUCER_SPAWN_RATE_SECONDS