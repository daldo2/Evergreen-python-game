import pygame
from src import config

class WinScene:
    """
    Handles the Victory state of the game.

    This scene is played when the player completes the level.
    It displays a victory image and plays a victory stx.
    """
    def __init__(self):
        """
        Initialize the WinScene.

        Loads the victory background image, scales it,
        and plays the win sound effect.
        """
        path = "assets/graphics/background/win.jpg"
        raw_img = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(raw_img, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.collect_sfx = pygame.mixer.Sound("assets/sounds/sfx/win.wav")
        self.collect_sfx.set_volume(0.4)
        self.collect_sfx.play()
        self.finished = False

    def handle_input(self, event):
        """
        Process user input during the Victory screen.

        Arguments:
            event: The input event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.finished = True

    def update(self, dt):
        """
        Update scene logic.

        Args:
            Delta time.
        """
        pass
    def draw(self,screen):
        """
        Render the victory screen.

        Args:
            screen: The main display surface.
        """
        screen.blit(self.image, (0, 0))
