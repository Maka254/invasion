import pygame 
from pygame.sprite import Sprite 

class Invader(Sprite):
    """A class to represent a single alien_invader in the fleet."""

    def __init__(self, ai_game):
        """Initialize the invader and set its startng position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the invader image and set its rect attribute.
        self.image = pygame.image.load("images/rocket.bmp")
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()

        # Start each new invader near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the invader's exact horizontal position. 
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if the invaders are at the edgeof the screen."""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True    

    def update(self):
        """Move the invader to the right."""
        self.x += (self.settings.invader_speed * self.settings.fleet_direction)
        self.rect.x = self.x    


