import pygame
from constants import *

class Menu:
    def __init__(self):
        self.menu_options = ["play", "leaderboard", "help", "quit"]
        self.options = self.menu_options
        self.selected_index = 0
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 24)
        self.footer_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
        self.font_title = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 48)
        self.transition_timer = 0
        
    def draw(self, screen):
        title_surface = self.font_title.render("ASTEROIDS", True, "white")
        screen.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, SCREEN_HEIGHT / 8 - title_surface.get_height() / 2))

        start_y = SCREEN_HEIGHT / 2 - (len(self.options) * 50) / 2
        for index, option in enumerate(self.options):
            y = start_y + index * 50
            if index == self.selected_index:
                text_size = self.font.size(option)
                pygame.draw.rect(screen, "white", (SCREEN_WIDTH / 2 - text_size[0] / 2 - 2, y - 5, text_size[0] + 4, 30), border_radius=5)
                text_surface = self.font.render(option.upper(), True, "black")
                screen.blit(text_surface, (SCREEN_WIDTH / 2 - text_surface.get_width() / 2 + 2, y + 2))
            else:
                text_surface = self.font.render(option.upper(), True, "white")
                screen.blit(text_surface, (SCREEN_WIDTH / 2 - text_surface.get_width() / 2, y + 2))
        
        footer_surface = self.footer_font.render("Created by Zerathane", True, "white")
        screen.blit(footer_surface, (SCREEN_WIDTH / 2 - footer_surface.get_width() / 2, SCREEN_HEIGHT - footer_surface.get_height() - 10))

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_s:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.menu_options[self.selected_index] == "play":
                        self.transition_timer = 0.5
                    else:
                        return self.menu_options[self.selected_index]
        if self.transition_timer > 0:
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                return self.menu_options[self.selected_index]