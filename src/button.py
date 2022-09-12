""" play button """
import pygame


class Button:
    """ button """

    def __init__(self, ai_game, msg):
        """ init button """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.width, self.height = (200, 50)
        self.color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """ generate msg image """
        self.msg_image = self.font.render(msg, True, self.text_color, self.color)
        self.image_rect = self.msg_image.get_rect()
        self.image_rect.center = self.rect.center

    def draw_button(self):
        """ draw text """
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.msg_image, self.image_rect)