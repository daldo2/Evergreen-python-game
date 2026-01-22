import pygame

class UI:
    """
    Manages the User Interface (HUD) overlay.

    This class handles rendering the player's health and mana bars
    on top of the game world. It requires a reference to the Player entity
    to access current status values.
    """
    def __init__(self, player):
        """
        Initialize the UI manager.

        Args:
            player: A reference to the main player entity. Used to read
                    current_hp, max_hp, current_mp, and max_mp.
        """
        self.player = player
        self.bar_width = 100
        self.bar_height = 12
        self.hp_color = (200, 40, 40)
        self.mp_color = (40, 40, 200)
        self.bg_color = (30, 30, 30)

    def draw(self, screen):
        """
        Render the complete UI to the screen.

        Args:
            screen: The main display surface.
        """
        self.draw_bar(screen, 10, 10, self.player.current_hp, self.player.max_hp, self.hp_color)
        self.draw_bar(screen, 10, 25, self.player.current_mp, self.player.max_mp, self.mp_color)

    def draw_bar(self, screen, x, y, current, max_val, color):
        """
        Helper method to render a single statistic bar.

        Calculates the fill width based on the current/max ratio and draws
        three layers: background, colored fill, and a white border.

        Args:
            screen: The surface to draw on.
            x: X-coordinate of the bar's top-left corner.
            y: Y-coordinate of the bar's top-left corner.
            current: The current value of the stat.
            max_val: The maximum possible value of the stat.
            color: The RGB color tuple for the filled portion.
        """
        if max_val <= 0: return

        ratio = current / max_val
        fill_width = int(self.bar_width * ratio)
        bg_rect = pygame.Rect(x, y, self.bar_width, self.bar_height)
        fill_rect = pygame.Rect(x, y, fill_width, self.bar_height)

        pygame.draw.rect(screen, self.bg_color, bg_rect)
        pygame.draw.rect(screen, color, fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 1)  # White border