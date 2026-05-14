import pygame
from constants import *
from game_state import Game_State
from player import draw_ship

class Hud:
    def __init__(self, game_state):
        self.game_state = game_state
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 24)

    def draw(self, screen):
        score_text = self.font.render(f"{str(self.game_state.score)}", True, "white")
        score_rect = score_text.get_rect()
        score_rect.midtop = (SCREEN_WIDTH / 2, 10)
        screen.blit(score_text, score_rect)
        for i in range(self.game_state.lives):
            x = 30 + i * 30
            y = 20
            draw_ship(screen, pygame.Vector2(x, y), 10, 180, "white")