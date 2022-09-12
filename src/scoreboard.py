""" record game score """
import pygame
from pygame.sprite import Sprite


class SettableShip(Sprite):
    """ left ships in game """

    def __init__(self, ai_game):
        """ initialize Ship"""
        super().__init__()

        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect

        try:
            self.image = pygame.image.load('images/ship.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, self.settings.ship_size)
            self.rect = self.image.get_rect()
        except FileNotFoundError:
            self.image = None
            self.rect = pygame.Rect(0, 0, self.settings.ship_size[0], self.settings.ship_size[1])
            print(f"load SettableShip fail")

        self.rect.top = self.screen_rect.top
        self.rect.x = self.rect.y = 0


class ScoreBoard:
    """ game score board """

    def __init__(self, ai_game):
        """ init score board """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self._create_left_ships(ai_game)

        self._prep_score()
        self._prep_high_score()
        self._prep_level()

    def _create_left_ships(self, ai_game):
        """ create left ships"""
        self.left_ships = pygame.sprite.Group()

        ship_width = SettableShip(ai_game).rect.width
        for i in range(self.settings.ship_limit):
            ship = SettableShip(ai_game)
            ship.rect.x = i * (ship_width + 10)
            self.left_ships.add(ship)

    def _prep_score(self):
        """ update score image """
        round_score = round(int(self.stats.score), -1)
        score_str = "{:,}".format(round_score)

        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.screen_rect.top

    def _prep_high_score(self):
        """ update highest score"""
        self.stats.high_score = max(self.stats.high_score, self.stats.score)
        round_score = round(int(self.stats.high_score), -1)
        score_str = "{:,}".format(round_score)

        self.high_score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = self.screen_rect.midtop

    def _prep_level(self):
        """ game level """
        level_str = str(self.stats.level)

        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.screen_rect.top
        self.level_rect.right = self.score_rect.left - 20

    def _prep_ship(self):
        """ update left ships """
        while len(self.left_ships) > self.stats.ships_left:
            self.left_ships.remove(self.left_ships.sprites()[-1])

    def prep_score(self):
        """ external prep score """
        self._prep_score()
        self._prep_high_score()
        self._prep_level()
        self._prep_ship()

    def draw_score(self):
        """ draw score board """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.left_ships.draw(self.screen)