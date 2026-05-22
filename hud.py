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
        wave_text = self.font.render(f"Wave: {str(self.game_state.wave_number)}", True, "white")
        wave_rect = wave_text.get_rect()
        wave_rect.topright = (SCREEN_WIDTH - 10, 10)
        screen.blit(wave_text, wave_rect)

    def draw_game_over(self, screen):
        game_over_text = self.font.render("GAME OVER", True, "white")
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        screen.blit(game_over_text, game_over_rect)