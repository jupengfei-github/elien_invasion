""" Alien Invasion Game """

import pygame
import sys
import time
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """ manager game resouece and behavior """

    def __init__(self):
        """ initialzie game resouce """
        self.settings = Settings()
        pygame.init()

        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_width()
            self.settings.screen_height = self.screen.get_height()
            self.screen_rect = self.screen.get_rect()
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
            self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.button = Button(self, "Play")
        self.score = ScoreBoard(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
        """ create aliens """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - 2*alien_width
        available_space_x = min(available_space_x, self.settings.screen_width//2)
        number_alien_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - 3*alien_height - ship_height
        available_space_y = min(available_space_y, self.settings.screen_height//2) # 1/2 space

        number_alien_y = available_space_y // (2 * alien_height)

        for alien_row in range(number_alien_x):
            for alien_line in range(number_alien_y):
                self._create_alien(alien_width, alien_height, alien_row, alien_line)

    def _create_alien (self, alien_width, alien_height, row_number, line_number):
        new_alien = Alien(self)

        new_alien.x = 2 * alien_width * row_number + alien_width
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = 2 * alien_height * line_number + alien_height
        self.aliens.add(new_alien)

    def _check_events(self):
        """ dealwith user click event """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_events_down(event)
            elif event.type == pygame.KEYUP:
                self._check_events_up(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_events(event)

    def _check_mouse_events(self, event):
        """ check mouse events """
        mouse_pos = pygame.mouse.get_pos()
        button_click = self.button.rect.collidepoint(mouse_pos)
        if button_click and not self.settings.game_active:
            self.settings.game_active = True

            self.stats.reset_status()
            self._restart_once_game()
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)

    def _check_events_down(self, event):
        """ check down events """
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _fire_bullet(self):
        """ fire ship bullet """
        if len(self.bullets) < self.settings.bullets_allowed:
            bullet = Bullet(self)
            self.bullets.add(bullet)
        else:
            print(f"reach max bullet. don't fire bullet")

    def _check_events_up(self, event):
        """ check up events """
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = False

    def _update_screen(self):
        """ update screen display """
        self.screen.fill(self.settings.bg_color)

        if not self.settings.game_active:
            self.button.draw_button()

    def _update_ship (self):
        """ update ship """
        self.ship.update()
        self.ship.blitme()

    def _update_bullet(self):
        """ update bullet """
        self.bullets.update()
        self._check_bullet_elien_collision()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_bullet_elien_collision(self):
        """ bullet hit elien """
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for elien in collisions.values():
                self.stats.increase_score(len(elien))

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.increase_level()
            self.settings.fleet_direction = 1

    def _check_elien_edge(self):
        """ check elien edge"""
        fleet_drop = False
        for elien in self.aliens.sprites():
            if elien.check_edges():
                self.settings.fleet_direction *= -1
                fleet_drop = True
                break

        if fleet_drop:
            for elien in self.aliens.sprites():
                elien.rect.y += self.settings.fleet_drop_speed

    def _check_eliens_bottom(self):
        """ elien move bottmon """
        for elien in self.aliens.sprites():
            if elien.rect.bottom >= self.screen_rect.bottom:
                return True

        return False

    def _update_alien(self):
        """ update alien move """
        if pygame.sprite.spritecollideany(self.ship, self.aliens) or self._check_eliens_bottom():
            self._ship_hit()

        self._check_elien_edge()
        self.aliens.update()
        self.aliens.draw(self.screen)

    def _restart_once_game(self):
        """ replay game """
        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()
        self.settings.fleet_direction = 1

        pygame.event.clear()

    def _ship_hit(self):
        """ ship hit  """
        self.stats.ships_left -= 1
        if self.stats.ships_left > 0:
            time.sleep(1)
            self._restart_once_game()
        else:
            self.settings.game_active = False
            pygame.mouse.set_visible(True)
            time.sleep(1)

    def _update_score(self):
        """ update score """
        self.score.prep_score()
        self.score.draw_score()

    def run_game(self):
        """ play game """
        while True:
            self._check_events()

            self._update_screen()
            if self.settings.game_active:
                self._update_ship()
                self._update_bullet()
                self._update_alien()
                self._update_score()

            pygame.display.flip()


# main entrance
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
