
import sys
from time import sleep
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
import pygame


class AlienInvasion:
    #initialize game parameters
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.dim = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen = pygame.display.set_mode(self.dim, pygame.FULLSCREEN)
        
        self.textfont = pygame.font.SysFont("chalkboard", 30)
        self.textfont1 = pygame.font.SysFont("futura", 50)
        self.textfont2 = pygame.font.SysFont("futura", 150)


        self.bg = pygame.image.load("source-code/images/pls.jpg")
        self.bg = pygame.transform.scale(self.bg, (pygame.display.Info().current_w, pygame.display.Info().current_h))


        pygame.display.set_caption ("Shawn's Alien Invasion")

        self.stats = GameStats(self)

       
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.points = 0
        self.lives = self.settings.ship_limit 
        self.level = 1

    #initialize scoreboard
    def scoreboard(self):
        
        self.score = self.textfont.render(f'Score: {self.points}' , True, (0, 255, 0))
        self.tries = self.textfont.render(f'Repairs: {self.lives}', True, (255, 255, 0))
        self.q = self.textfont.render(f'Q to quit', True, (255, 100, 0))
        self.title = self.textfont1.render(f'Space Invaders', True, (200, 150, 200))
        self.leveltest = self.textfont.render(f'Level: {self.level}', True, (255, 255, 200))
        self.screen.blit(self.score, (10, 10))
        self.screen.blit(self.tries, (10, 60))
        self.screen.blit(self.q, (10, 110))
        screen_dim = self.screen.get_rect().width
        self.screen.blit(self.title, (screen_dim // 2 - 175, 10))
        self.screen.blit(self.leveltest, (screen_dim - 175, 10))
        
    #initialize and run game
    def run_game(self):
        cap = 50
        while True:
            
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.scoreboard()
            if self.points > cap:
                self.settings.alien_speed += 4
                cap += 50
                self.level += 1

            pygame.display.update()

    #check for game events
    def _check_events(self):
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
           
    #controller logic
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:    
            self._fire_bullet()     
    
    #controller logic
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    #fire bullet sprites
    def _fire_bullet(self):
        
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    #update bullet sprites
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    #check if bullet hit an alien
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if (collisions):
            self.points += 1
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    #update alien sprites
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        self._check_aliens_bottom()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print ("SHIP HIT!!!")
            self._ship_hit()
            
    #create fleet of alien sprites
    def _create_fleet(self):
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size

        number_aliens_x = self.settings.screen_width // (2*alien_width)
        
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height))
        number_rows = available_space_y // (2*alien_height) - 1

        for row_number in range (number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number, row_number)

    #create alien sprite
    def _create_alien(self, alien_number, row_number):

        # Create an alien and place it in the row.
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        alien_width = aliens.rect.width
        aliens.x = alien_width + (1.5 *alien_width) * alien_number
        aliens.rect.x = aliens.x
        aliens.rect.y = alien_height + 2 * aliens.rect.height * row_number
        self.aliens.add(aliens)

    #check if alien sprite has reached end of screen
    def _check_fleet_edges(self):
    # Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    #fleet logic
    def _change_fleet_direction(self):
    # Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    #makes sure game persists every update
    def _update_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        #pygame.display.flip()

    #ship hit logic and update game scoreboard
    def _ship_hit(self):
        # Respond to the ship being hit by an alien
        if self.stats.ships_left >0:
        # Decrement the number of ships left
            self.stats.ships_left -= 1
            # Get rid of any remianing aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and cneter the ship
            self._create_fleet()
            self.ship.center_ship()
            self.lives -= 1
            # Pause for half a second
            self.ouch = self.textfont2.render(f'Ouch', True, (255, 0, 0))
            self.screen.blit(self.ouch, (525, 350))
            pygame.display.update()
            sleep (0.5)
        else:
            self.go = self.textfont2.render(f'Game Over', True, (255, 0, 0))
            self.screen.blit(self.go, (300, 300))
            pygame.display.update()
            sleep(5)
            self.stats.game_active = False

    #check if aliens have gone past spaceship
    def _check_aliens_bottom(self):
        # Check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

#main function to instantiate class and run game
if __name__ == '__main__':
    
    ai = AlienInvasion()
    ai.run_game()
    
    
quit()
