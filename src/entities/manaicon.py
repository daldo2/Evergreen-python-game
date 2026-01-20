import pygame
from src import config

class ManaIcon:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.frames = []
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.load_sprites("assets/graphics/abilities/fireball-002.png", frame_count=5)
        self.image = self.frames[0]
        self.current_hp = 1



    def update(self, dt, tiles):
        safe_dt = min(dt, 0.05)
        self.animate(safe_dt)

    def load_sprites(self, path, frame_count):
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()
        frame_width = sheet_width // frame_count

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))

            scaled_frame = pygame.transform.scale(frame, (config.TILE_SIZE, config.TILE_SIZE))
            self.frames.append(scaled_frame)

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index += 1

            # Loop back to 0
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[self.frame_index]


    def draw(self, screen, offset):
        draw_pos = self.rect.topleft + offset
        screen.blit(self.image, draw_pos)
