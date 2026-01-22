import pygame
from src import config
from src.core.physics import move_and_slide


class Slime:
    """
    A basic ground-based enemy entity.

    The Slime patrols back and forth on a platform. It uses sensor logic to detect
    edges and walls, turning around to stay on safe ground.

    Attributes:
        rect: The collision hitbox.
        velocity: Current movement vector.
        direction: 1 (Right) or -1 (Left).
        current_hp: Current health points.
    """
    def __init__(self, x, y):
        """
        Initialize the Slime entity.

        Args:
            x: Starting X coordinate.
            y: Starting Y coordinate.
        """
        self.rect = pygame.Rect(x, y, 32, 32)
        self.velocity = pygame.Vector2(0, -300)
        self.speed = 40
        self.direction = 1  # 1 = Right, -1 = Left

        self.frames = []
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.is_grounded = False
        self.load_sprites("assets/graphics/enemies/Slime-0001.png", frame_count=8)
        self.image = self.frames[0]
        self.debug_floor_sensor = None
        self.debug_wall_sensor = None
        self.max_hp = 2
        self.current_hp = 2

    def load_sprites(self, path, frame_count):
        """
        Load and slice the sprite sheet into frames.

        Args:
            path: Path to the image file.
            frame_count: Number of frames in the sheet.
        """
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()

        frame_width = sheet_width // frame_count

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))

            scaled_frame = pygame.transform.scale(frame, (config.TILE_SIZE, config.TILE_SIZE))
            self.frames.append(scaled_frame)

    def update(self, dt, tiles):
        """
        Main update loop: AI decisions, physics, and animation.

        Args:
            dt: Delta time in seconds.
            tiles: List of solid tile rectangles for collision.
        """
        safe_dt = min(dt, 0.05)

        self.update_ai(tiles)
        self.velocity.x = self.speed * self.direction
        self.apply_gravity(safe_dt)
        self.rect, collisions = move_and_slide(self.rect, self.velocity, tiles, safe_dt)

        self.is_grounded = collisions['bottom']
        if self.is_grounded:
            self.velocity.y = 0

        self.animate(safe_dt)

    def update_ai(self, tiles):
        """
        Check environment sensors to steer the slime.

        Uses a floor sensor to detect ledges and a wall sensor to detect obstacles.
        If either is triggered, the direction is reversed.

        Args:
            tiles: List of collision tiles.
        """
        offset_x = 20
        check_x = self.rect.centerx + (offset_x * self.direction)  # Dynamic direction check

        floor_sensor = pygame.Rect(check_x, self.rect.bottom, 2, 2)  # Removed +2 gap to be tighter

        has_floor = False
        for tile in tiles:
            if tile.colliderect(floor_sensor):
                has_floor = True
                break

        wall_sensor_y = self.rect.centery - 5
        wall_sensor_x = self.rect.right if self.direction == 1 else self.rect.left - 4
        wall_sensor_rect = pygame.Rect(wall_sensor_x, wall_sensor_y, 4, 10)

        hits_wall = False
        for tile in tiles:
            if tile.colliderect(wall_sensor_rect):
                hits_wall = True
                break

        if hits_wall or (self.is_grounded and not has_floor):
            self.direction *= -1

    def move(self, dt):
        """
        Apply horizontal velocity based on direction.
        """
        self.velocity.x = self.speed * self.direction

    def apply_gravity(self, dt):
        """
        Apply downward acceleration.
        """
        self.velocity.y += config.GRAVITY * dt

    def animate(self, dt):
        """
        Advance the sprite animation frame.
        """
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[self.frame_index]

    def draw_health_bar(self, screen, offset):
        """
        Render the health bar above the entity.

        Args:
            screen: Main display surface.
            offset: Camera offset vector.
        """
        bar_width = 14
        bar_height = 2
        offset_y = 12
        centering_offset = (self.rect.width - bar_width) // 2

        screen_x = self.rect.x + offset.x +centering_offset
        screen_y = self.rect.y + offset.y + offset_y
        ratio = self.current_hp / self.max_hp
        fill_width = int(bar_width * ratio)

        border_rect = pygame.Rect(screen_x, screen_y, bar_width, bar_height)
        fill_rect = pygame.Rect(screen_x, screen_y, fill_width, bar_height)

        pygame.draw.rect(screen, (200, 0, 0), border_rect)
        pygame.draw.rect(screen, (0, 200, 0), fill_rect)

    def draw(self, screen, offset):
        """
        Render the Slime sprite and its ui elements.

        Args:
            screen: Main display surface.
            offset: Camera offset vector.
        """
        draw_pos = self.rect.topleft + offset

        # flip sprite if moving left
        if self.direction == 1:
            screen.blit(self.image, draw_pos)
        else:
            flipped = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped, draw_pos)
        self.draw_health_bar(screen, offset)