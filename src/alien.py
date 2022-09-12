""" Alien """
from pygame.sprite import Sprite
import pygame


class Alien(Sprite):
    """ Alien class """

    def __init__(self, ai_game):
        """ init Alien """
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        try:
            self.image = pygame.image.load('images/alien.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, ai_game.settings.elien_size)
            self.rect = self.image.get_rect()
        except FileNotFoundError:
            self.image = None
            self.rect = pygame.Rect(0, 0, ai_game.settings.elien_size[0], ai_game.settings.elien_size[1])
            print("Alien Can not load file: 'image/alien.png'")

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        """ update alien hrizontal distance """
        self.x += self.settings.elien_speed * self.settings.fleet_direction
        self.rect.x = int(self.x)

    def check_edges(self):
        """ elien move edge of screen """
        if self.rect.right >= self.settings.screen_width or self.rect.left <= 0:
            return True
        else:
            return False