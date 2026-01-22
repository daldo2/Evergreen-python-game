import pygame
from src import config

class MenuScene:
    """
    Represents the Main Menu state of the game.

    This scene displays a static image and waits for the player
    to press the Spacebar to start the game.

    Attributes:
        image: The scaled background image surface.
        finished: Flag indicating if the menu is done or not done
    """
    def __init__(self):
        """
        Initialize the menu scene.

        Loads the background image from assets, optimizes it with convert(),
        and scales it to match the screen resolution defined in config.
        """
        path = "assets/graphics/background/welcome.png"
        raw_img = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(raw_img, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.finished = False

    def handle_input(self, event):
        """
        Process input events.

        Checks if the Spacebar is pressed. If so, sets the 'finished' flag
        to True, signaling the main loop to switch states.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.finished = True

    def update(self, dt):
        """
        Update scene logic.

        Currently empty because the menu is static.

        Args:
            dt: Delta time in seconds.
        """
        pass

    def draw(self,screen):
        """
        Render the menu to the display.

        Args:
            screen: The main game surface.
        """
        screen.blit(self.image, (0, 0))
