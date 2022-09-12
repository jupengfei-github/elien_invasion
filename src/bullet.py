""" ship bullet """
from pygame.sprite import Sprite
import pygame


class Bullet(Sprite):
    """ bullet """

    def __init__(self, ai_game):
        """ init function """
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y_postion = float(self.rect.y)

    def update (self):
        """ update bullet position """
        self.y_postion -= self.settings.bullet_speed
        self.rect.y = int(self.y_postion)

    def draw_bullet (self):
        """ draw bullet """
        pygame.draw.rect(self.screen, self.color, self.rect)