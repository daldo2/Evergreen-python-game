import pygame
from src import config

class DeadScene:
    """
    Scene representing the game over state.

    This class handles the display of the death screen, plays death sfx, stops the bacground music,
    and waits for input to restart.
    """
    def __init__(self):
        """
        Initialize the DeadScene.
        Loads the bacground image, stops the background, and plays death sfx.
        """
        path = "assets/graphics/background/dead.jpg"
        raw_img = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(raw_img, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.mixer.music.stop()
        self.collect_sfx = pygame.mixer.Sound("assets/sounds/sfx/dead.wav")
        self.collect_sfx.set_volume(0.4)
        self.collect_sfx.play()
        self.finished = False

    def handle_input(self, event):
        """
        Handles input from the user.

        Takes event to process.
        If space is pressed the self.finished is set to True, signaling to switch back to game
        scene.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.finished = True

    def update(self, dt):
        """
        Updates the scene logic.

        Takes dt as args, and returns nothing.
        """
        pass

    def draw(self,screen):
        """
        Renders the scene to the screen.

        Takes screen as args.
        """
        screen.blit(self.image, (0, 0))
