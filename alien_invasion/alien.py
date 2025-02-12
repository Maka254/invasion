import sys

import pygame
pygame.init()

from settings import Settings
from ship import Ship
from bullet import Bullet
from invader import Invader

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.invaders = pygame.sprite.Group()

        self._create_fleet()

        # Set the background color.
        self.bg_color = (255, 255, 255)

    def run_game(self):
        print("Game started")
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullet()
            self._update_invaders()
            self._update_screen()

    def _update_bullet(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_invader_collisions()

    def _check_bullet_invader_collisions(self):
        """Respond to bullet-invader collisions."""
        # Remove any bullets and invaders that have collided. 
        collisions = pygame.sprite.groupcollide(self.bullets, self.invaders, True, True)

        if not self.invaders:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet() 

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting game")
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.invaders.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _create_fleet(self):
        """Create the fleet of invaders."""
        # Create an invader and find the number of invaders in a row.
        # Spacng between each invader is equal to one invader width.
        invader = Invader(self)
        invader_width, invader_height = invader.rect.size
        available_space_x = self.settings.screen_width - (2 * invader_width)
        number_invader_x = available_space_x // (2 * invader_width)

        # Determine the number of rows of invaders that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * invader_height) - ship_height)
        number_rows = available_space_y // (2 * invader_height)

        # Create the full fleet of invaders.
        for row_number in range(number_rows):
            for invader_number in range(number_invader_x):
                self._create_invader(invader_number, row_number)

    def _create_invader(self, invader_number, row_number):
        """Create an invader and place it in the row."""
        invader = Invader(self)
        invader_width, invader_height = invader.rect.size
        invader.x = invader_width + 2 * invader_width * invader_number
        invader.rect.x = invader.x
        invader.rect.y = invader.rect.height + 2 * invader.rect.height * row_number
        self.invaders.add(invader)

    def _check_fleet_edges(self):
        """Respond appropriately if any invaders hit an edge."""
        for invader in self.invaders.sprites():
            if invader.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for invader in self.invaders.sprites():
            invader.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_invaders(self):
        """
        Check if the fleet is at an edge,
            then update the positions of all invaders in the fleet.
        """
        self._check_fleet_edges()
        self.invaders.update()   

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
