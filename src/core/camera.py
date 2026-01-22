import pygame
from src import config

class Camera:
    """
    This class is responsible for camera related actions.

    Attributes:
        map_width: The width of the map.
        map_height: The height of the map.
    """
    def __init__(self, map_width, map_height):
        """
        Initialize the Camera.

        Args:
            map_width: The total width of the game map in pixels.
            map_height: The total height of the game map in pixels.
        """
        self.offset = pygame.Vector2(0, 0)
        self.offset.y = -100
        self.map_width = map_width
        self.map_height = map_height

    def follow(self, target):
        """
        Update the camera offset to center the view on a targe.

        This method calculates the ideal camera position to keep the target in the
        middle of the screen, then clamps those coordinates so the camera stops
        moving when it reaches the edge of the map.

        Args:
            target: The object to follow .
        """
        desired_x = (config.SCREEN_WIDTH // 2) - target.rect.centerx
        min_offset = -(self.map_width - config.SCREEN_WIDTH)
        self.offset.x = max(min_offset, min(0, desired_x))
        desired_y = (config.SCREEN_HEIGHT // 2) - target.rect.centery
        min_offset = -(self.map_height - config.SCREEN_HEIGHT)
        self.offset.y = max(min_offset, min(0, desired_y))
