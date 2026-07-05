import json
import pygame
from game_state import *

class LeaderboardManager:
    def __init__(self):
        self.leaderboard_file = "leaderboard.json"
        self.leaderboard_data = self.load_leaderboard_data()
        
    def load_leaderboard_data(self):
        try:
            with open(self.leaderboard_file, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return self.create_leaderboard_file()
        
    def create_leaderboard_file(self):
        default_data = [
            {"name": "AAA", "score": 60000, "wave": 13},
            {"name": "BBB", "score": 55000, "wave": 12},
            {"name": "CCC", "score": 50000, "wave": 11},
            {"name": "DDD", "score": 45000, "wave": 10},
            {"name": "EEE", "score": 40000, "wave": 9},
            {"name": "FFF", "score": 35000, "wave": 8},
            {"name": "GGG", "score": 30000, "wave": 7},
            {"name": "HHH", "score": 25000, "wave": 6},
            {"name": "III", "score": 20000, "wave": 5},
            {"name": "JJJ", "score": 15000, "wave": 4}
        ]
        with open(self.leaderboard_file, "w") as file:
            json.dump(default_data, file)
        self.leaderboard_data = default_data
        return default_data

    def save_leaderboard_data(self):
        with open(self.leaderboard_file, "w") as file:
            json.dump(self.leaderboard_data, file)

    def update_leaderboard(self, name, score, wave):
        new_entry = {"name": name, "score": score, "wave": wave}
        self.leaderboard_data.append(new_entry)
        self.leaderboard_data.sort(key=lambda x: (x["score"], x["wave"]), reverse=True)
        self.leaderboard_data = self.leaderboard_data[:10]
        self.save_leaderboard_data()

    def qualifying_score(self, score):
        if score > min(self.leaderboard_data, key=lambda x: x["score"])["score"]:
            return True
        return False


class Leaderboard:
    def __init__(self, score, wave, leaderboard_manager):
        self.score = score
        self.wave = wave
        self.leaderboard_data = leaderboard_manager.leaderboard_data
        self.leaderboard_manager = leaderboard_manager
        if self.leaderboard_manager.qualifying_score(self.score):
            self.leaderboard_mode = "enter"
        else:
            self.leaderboard_mode = "view"
        
        self.alphabet = [chr(i).upper() for i in range(97, 123)]
        self.name = ["A", "A", "A"]
        self.current_name_slot = 0
        self.current_alphabet_index = 0
        self.highlight_timer = 0
        self.column_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 24)
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 32)
        self.character_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 48)

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

        elif self.leaderboard_mode == "enter":
            screen.fill("black")
            title_surface = self.title_font.render("NEW HIGH SCORE!", True, "white")
            screen.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, (SCREEN_HEIGHT / 8 - 30) - title_surface.get_height() / 2))

            prompt_surface = self.column_font.render("ENTER YOUR NAME", True, "white")
            screen.blit(prompt_surface, (SCREEN_WIDTH / 2 - prompt_surface.get_width() / 2, (SCREEN_HEIGHT / 4 - 20) - prompt_surface.get_height() / 2))

            for index, letter in enumerate(self.name):
                if index == self.current_name_slot:
                    if self.highlighted:
                        padding = 10
                        letter_surface = self.character_font.render(letter, True, "black")
                        pygame.draw.rect(screen, "white", (int(SCREEN_WIDTH / 2 - 100 + index * 100 - letter_surface.get_width() / 2 - padding - 2), int(SCREEN_HEIGHT / 2 - letter_surface.get_height() / 2 - padding), letter_surface.get_width() + padding * 2, letter_surface.get_height() + padding * 2))
                        screen.blit(letter_surface, (int(SCREEN_WIDTH / 2 - 100 + index * 100 - letter_surface.get_width() / 2), int(SCREEN_HEIGHT / 2 - letter_surface.get_height() / 2)))
                    else:
                        letter_surface = self.character_font.render(letter, True, "white")
                        screen.blit(letter_surface, (int(SCREEN_WIDTH / 2 - 100 + index * 100 - letter_surface.get_width() / 2), int(SCREEN_HEIGHT / 2 - letter_surface.get_height() / 2)))
                else:
                    letter_surface = self.character_font.render(letter, True, "white")
                    screen.blit(letter_surface, (int(SCREEN_WIDTH / 2 - 100 + index * 100 - letter_surface.get_width() / 2), int(SCREEN_HEIGHT / 2 - letter_surface.get_height() / 2)))

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return AppState.MAIN_MENU
                if self.leaderboard_mode == "enter":
                    if event.key == pygame.K_w:
                        self.current_alphabet_index = (self.current_alphabet_index - 1) % len(self.alphabet)
                        self.name[self.current_name_slot] = self.alphabet[self.current_alphabet_index]
                    elif event.key == pygame.K_s:
                        self.current_alphabet_index = (self.current_alphabet_index + 1) % len(self.alphabet)
                        self.name[self.current_name_slot] = self.alphabet[self.current_alphabet_index]
                    elif event.key == pygame.K_a:
                        self.current_name_slot = (self.current_name_slot - 1) % 3
                        self.current_alphabet_index = self.alphabet.index(self.name[self.current_name_slot])
                    elif event.key == pygame.K_d:
                        self.current_name_slot = (self.current_name_slot + 1) % 3
                        self.current_alphabet_index = self.alphabet.index(self.name[self.current_name_slot])
                    elif event.key == pygame.K_RETURN:
                        if self.current_name_slot < 2:
                            self.current_name_slot += 1
                            self.current_alphabet_index = 0
                        else:
                            player_name = "".join(self.name)
                            self.leaderboard_manager.update_leaderboard(player_name, self.score, self.wave)
                            self.leaderboard_data = self.leaderboard_manager.leaderboard_data
                            self.leaderboard_mode = "view"
                            return AppState.LEADERBOARD
        self.highlight_timer += dt
        if self.highlight_timer % 1 > 0.5:
            self.highlighted = True
        else:
            self.highlighted = False
            