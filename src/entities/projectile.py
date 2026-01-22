import pygame

class Projectile:
    """
        Represents a moving projectile fired by an entity.

        The projectile has two states:
        1. Flying: Moves in a straight line until it hits a wall, an enemy, or expires.
        2. Dying: Plays an impact/explosion animation before being removed.

        Attributes:
            rect: The physics hitbox.
            direction: 1 for right, -1 for left.
            is_alive: Flag to tell the main loop if this object should be removed.
            is_dying: Flag indicating the impact animation is playing.
        """

    def __init__(self, x, y, direction):
        """
        Initialize the projectile.

        Args:
            x: Starting X coordinate.
            y: Starting Y coordinate.
            direction: Direction of travel (1 for Right, -1 for Left).
        """
        self.rect = pygame.Rect(x, y + 10, 10, 10)
        self.direction = direction  # 1 (Right) or -1 (Left)
        self.speed = 400
        self.lifetime = 2.0
        self.is_alive = True
        self.is_dying = False
        self.frames_flying = []
        self.frames_dying = []
        self.load_fireball_animation("assets/graphics/abilities/fireball-001.png", 23)
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.08
        if self.frames_flying:
            self.image = self.frames_flying[0]

    def load_fireball_animation(self, path, frame_count):
        """
        Load and slice the sprite sheet, separating flying and dying frames.

        Assumes the first half of the frames are for flying and the second half
        are for the impact/explosion animation.

        Args:
            path: File path to the sprite sheet.
            frame_count: Total number of frames in the sheet.
        """
        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        frame_flying = frame_count / 2
        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (64, 32))
            if i < frame_flying:
                self.frames_flying.append(scaled_frame)
            else:
                self.frames_dying.append(scaled_frame)


    def update(self, dt, walls, enemies):
        """
        Update position, check collisions, and handle lifetime.

        If the projectile hits a wall or enemy, it stops moving and enters the
        'dying' state to play the explosion animation.

        Args:
            dt: Delta time in seconds.
            walls: List of wall rectangles to check for collisions.
            enemies: list of enemy entities to check for hits.
        """
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.is_dying = True

        if not self.is_dying:
            self.rect.x += self.speed * self.direction * dt

        for wall in walls:
            if self.rect.colliderect(wall):
                if not self.is_dying:
                    self.is_dying = True
                    self.frame_index = 0
                break

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                if not self.is_dying:
                    self.is_dying = True
                    self.frame_index = 0
                    enemy.current_hp -= 20
        self.animate(dt)

    def animate(self, dt):
        """
        Advance the animation frames.

        If dying, plays the explosion animation once and then marks is_alive as False.
        If flying, loops the flight animation.

        Args:
            dt: Delta time in seconds.
        """
        self.animation_timer += dt
        if self.is_alive and not self.is_dying:
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0

                if self.frame_index < len(self.frames_flying) - 1:
                    self.frame_index += 1
                else:
                    self.frame_index = 0
            self.image = self.frames_flying[self.frame_index]

        elif self.is_dying:
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0

                if self.frame_index < len(self.frames_dying) - 1:
                    self.frame_index += 1
                else:
                    self.is_alive = False
            self.image = self.frames_dying[self.frame_index]

    def draw(self, screen, offset):
        """
        Render the projectile relative to the camera.

        Applies a center offset because the sprite is larger than the
        physics hitbox.

        Args:
            screen: Main display surface.
            offset: Camera offset vector.
        """
        center_offset = pygame.Vector2(-24, -10)
        draw_pos = self.rect.topleft + offset + center_offset

        if self.direction == -1:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, draw_pos)
        else:
            screen.blit(self.image, draw_pos)