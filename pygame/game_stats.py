class GameStats:
    def __init__ (self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = True
        self.aliens_destroyed = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit