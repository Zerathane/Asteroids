from constants import *
from player import *
from asteroidfield import *
import pygame

class Game_State:
    def __init__(self):
        self.score = 0
        self.lives = PLAYER_LIVES
        self.wave_number = 1
        self.waiting = False
        self.invulnerability_timer = 0
        self.game_over_timer = 0

    def add_score(self, asteroid):
        pre_score = self.score // 10000
        if asteroid.radius > ASTEROID_MIN_RADIUS * 2:
            self.score += SCORE_LARGE_ASTEROID
        elif asteroid.radius > ASTEROID_MIN_RADIUS:
            self.score += SCORE_MEDIUM_ASTEROID
        else:
            self.score += SCORE_SMALL_ASTEROID
        post_score = self.score // 10000
        if post_score != pre_score:
            self.add_life()

    
    def lose_life(self):
        self.lives -= 1

    def is_game_over(self):
        return self.lives <= 0
    
    def reset(self):
        self.score = 0
        self.lives = PLAYER_LIVES

    def next_wave(self):
        self.wave_number += 1

    def waiting_for_respawn(self, asteroids):
        for asteroid in asteroids:
            if asteroid.position.distance_to(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)) < ASTEROID_SPAWN_DISTANCE_THRESHOLD:
                return True
        return False
       
    def add_life(self):
        self.lives += 1

    def add_saucer_score(self, saucer):
        pre_score = self.score // 10000
        if saucer.size == "large":
            self.score += SCORE_LARGE_SAUCER
        else:
            self.score += SCORE_SMALL_SAUCER
        post_score = self.score // 10000
        if post_score != pre_score:
            self.add_life()