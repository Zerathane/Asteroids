

import pygame
from game_state import *


class LeaderboardManager:
    pass




class Leaderboard:
    def __init__(self, game_state, leaderboard_data):
        self.score = game_state.score
        self.leaderboard_data = leaderboard_data
        if self.score > min(leaderboard_data, key=lambda x: x["score"])["score"]:
            self.leaderboard_mode = "enter"
        else:
            self.leaderboard_mode = "view"
        self.alphabet = [chr(i).upper() for i in range(97, 123)]
        self.name = ["A", "A", "A"]
        self.current_name_slot = 0
        self.current_alphabet_index = 0
        self.column_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 24)
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 32)

    def draw(self, screen):
        screen.fill("black")
        if self.leaderboard_mode == "view":
            screen.fill("black")
            title_surface = self.title_font.render("LEADERBOARD", True, "white")
            screen.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, (SCREEN_HEIGHT / 8 - 30) - title_surface.get_height() / 2))

            column_titles = ["Rank", "Name", "Score", "Wave"]
            start_x = SCREEN_WIDTH / 2 - 225
            column_x_offsets = [0, 150, 300, 450]
            for index, title in enumerate(column_titles):
                text_surface = self.column_font.render(title, True, "white")
                screen.blit(text_surface, (start_x + column_x_offsets[index] - text_surface.get_width() / 2, (SCREEN_HEIGHT / 4 - 20) - text_surface.get_height() / 2))

            for index, entry in enumerate(self.leaderboard_data):
                rank_surface = self.column_font.render(str(index + 1), True, "white")
                name_surface = self.column_font.render(entry["name"], True, "white")
                score_surface = self.column_font.render(str(entry["score"]), True, "white")
                wave_surface = self.column_font.render(str(entry["wave"]), True, "white")

                surfaces = [rank_surface, name_surface, score_surface, wave_surface]
                for column_x_offset, surface in zip(column_x_offsets, surfaces):
                    screen.blit(surface, (start_x + column_x_offset - surface.get_width() / 2, (SCREEN_HEIGHT / 4 -15) + (index + 1) * 50 - surface.get_height() / 2))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return AppState.MAIN_MENU
                

        
        