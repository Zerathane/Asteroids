from constants import *
from player import *

class Game_State:
    def __init__(self):
        self.score = 0
        self.lives = PLAYER_LIVES

    def add_score(self, asteroid):
        if asteroid.radius > ASTEROID_MIN_RADIUS * 2:
            self.score += SCORE_LARGE_ASTEROID
        elif asteroid.radius > ASTEROID_MIN_RADIUS:
            self.score += SCORE_MEDIUM_ASTEROID
        else:
            self.score += SCORE_SMALL_ASTEROID

    
    def lose_life(self):
        self.lives -= 1

    def is_game_over(self):
        return self.lives <= 0
    
    def reset(self):
        self.score = 0
        self.lives = PLAYER_LIVES
