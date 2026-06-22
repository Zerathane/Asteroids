import pygame
from constants import *

class Help():
    def __init__(self):
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)


    def draw(self, screen):
        screen.fill("black")
        title_surface = self.font.render("HELP", True, "white")
        screen.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, SCREEN_HEIGHT / 8 - title_surface.get_height() / 2))

        help_text = [
            "Controls:",
            "W: Thrust Forward",
            "A: Rotate Left",
            "D: Rotate Right",
            "E: Hyperspace",
            "Space: Shoot",
            "",
            "Objective:",
            "Destroy all asteroids",
            "Avoid collisions with asteroids and saucers",
            "",
            "Press SPACE or ESC to return to the main menu"
        ]

        start_y = SCREEN_HEIGHT / 4
        for index, line in enumerate(help_text):
            text_surface = self.font.render(line, True, "white")
            screen.blit(text_surface, (SCREEN_WIDTH / 2 - text_surface.get_width() / 2, start_y + index * 30))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return AppState.MAIN_MENU