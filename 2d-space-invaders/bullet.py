import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
    
    def __init__(self, ai_game):

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #self.color = self.settings.bullet_color
        self.image = pygame.image.load('2d-space-invaders/cat.png')
        self.image = pygame.transform.scale(self.image, (90, 120))
        self.rect = self.image.get_rect()
        self.cap = 12
        self.thir = 30
        
        if (self.settings.alien_speed >= self.cap):
            self.image = pygame.transform.scale(self.image, (90 + self.thir, 120 + self.thir))
            self.rect = self.image.get_rect()
        if (self.settings.alien_speed >= 16):
            self.image = pygame.transform.scale(self.image, (90 + 2 * self.thir, 120 + 2 * self.thir))
            self.rect = self.image.get_rect()
        if (self.settings.alien_speed >= 20):
            self.image = pygame.transform.scale(self.image, (90 + 3* self.thir, 120 + 3 * self.thir))
            self.rect = self.image.get_rect()
            
        
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)
        #pygame.draw.rect(self.screen, self.color, self.rect)
    