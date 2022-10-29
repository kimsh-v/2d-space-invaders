class Settings:
    def __init__(self):
        self.screen_width = 1600
        self.screen_height = 1000
        #self.bg_color = (255, 100, 150)

        self.ship_speed = 15
        self.ship_limit = 3

        self.bullet_speed = 6
        self.bullet_width = 70
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10
        
        self.alien_speed = 8
        self.fleet_direction = 1
        self.fleet_drop_speed = 30