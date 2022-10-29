import pygame
class Settings:
    def __init__(self):
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h

        self.ship_speed = 15
        self.ship_limit = 3

        self.bullet_speed = 6
        self.bullet_width = 70
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10
        
        self.alien_speed = 5
        self.fleet_direction = 1
        self.fleet_drop_speed = 30