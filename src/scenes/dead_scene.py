import pygame
from src import config

class DeadScene:
    def __init__(self):
        path = "assets/graphics/background/dead.jpg"
        raw_img = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(raw_img, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.mixer.music.stop()
        self.collect_sfx = pygame.mixer.Sound("assets/sounds/sfx/dead.wav")
        self.collect_sfx.set_volume(0.4)
        self.collect_sfx.play()
        self.finished = False

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.finished = True

    def update(self, dt):
        pass

    def draw(self,screen):
        screen.blit(self.image, (0, 0))
