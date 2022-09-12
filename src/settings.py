""" Game Settings """


class Settings:
    """ Gemae Settings """

    def __init__(self):
        """ initialize game settings property """
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (150, 150, 150)

        self.ship_speed = 1
        self.ship_size = (40, 40)
        self.ship_limit = 3

        self.fullscreen = False
        self.game_active = False

        self.elien_size = (40, 40)
        self.elien_speed = 0.4
        self.fleet_drop_speed = 40
        self.fleet_direction = 1

        # bullet
        self.bullet_speed = 3.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.elien_score = 50

    def initialize_dynamic_settings(self):
        """ reset dynamic settings """
        self.ship_speed = 1
        self.elien_speed = 0.4
        self.bullet_speed = 3.5

        self.fleet_direction = 1
        self.elien_score = 50

    def increase_speed(self):
        """ increase ship/elien/bullet speed """
        self.ship_speed *= self.speedup_scale
        self.elien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.elien_score *= self.score_scale
