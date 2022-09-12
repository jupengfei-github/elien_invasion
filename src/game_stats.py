""" Game Stats """


class GameStats:
    """ stat game information """

    def __init__(self, ai_game):
        """ game statics """
        self.settings = ai_game.settings
        self.high_score = 0
        self._reset_status()

    def _reset_status(self):
        """ inner reset information """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def reset_status(self):
        """ reset information """
        self._reset_status()

    def increase_score(self, number_elien):
        """ increase game score"""
        self.score += self.settings.elien_score * number_elien

    def increase_level(self):
        """ increase game level """
        self.level += 1