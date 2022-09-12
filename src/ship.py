""" space ship """
import pygame


class Ship:
    """ packing ship """

    def __init__(self, ai_game):
        """ init shape property """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        try:
            self.image = pygame.image.load('images/ship.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, self.settings.ship_size)
            self.rect = self.image.get_rect()
        except FileNotFoundError:
            self.image = None
            self.rect = pygame.Rect(0, 0, self.settings.ship_size[0], self.settings.ship_size[1])
            print("pygame load 'images/ship.png' fail")

        self.center_ship()

    def update (self):
        """ update ship position """
        if self.move_right:
            self.x_position += self.settings.ship_speed

        if self.move_left:
            self.x_position -= self.settings.ship_speed

        # move range
        self.x_position = max(0, min(self.x_position, self.screen_rect.right - self.rect.width))
        self.rect.x = int(self.x_position)

    def center_ship(self):
        """ center ship """
        self.rect.midbottom = self.screen_rect.midbottom
        self.move_left  = False
        self.move_right = False
        self.x_position = float(self.rect.x)

    def blitme(self):
        """ draw ship """
        if self.image:
            self.screen.blit(self.image, self.rect)
        else:
            print("image blit becauseof None")
