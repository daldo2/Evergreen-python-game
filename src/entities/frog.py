import pygame
from src import config
from src.core.physics import move_and_slide

class Frog:
    """
    A simple enemy entity.

    The Frog moves horizontally, applies gravity, and uses sensor logic to
    detect walls or edges of platforms. If it encounters an obstacle or a drop,
    it reverses direction.
    """
    def __init__(self, x, y):
        """
        Initialize the Frog entity.

        Args:
            x: The starting X coordinate.
            y: The starting Y coordinate.
        """
        self.rect = pygame.Rect(x, y, 32, 32)
        self.velocity = pygame.Vector2(0, 300)
        self.speed = 40
        self.direction = 1  # 1 = Right, -1 = Left

        self.frames = []
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.is_grounded = False
        self.load_sprites("assets/graphics/enemies/Frog001.png", frame_count=3)
        self.image = self.frames[0]
        self.debug_floor_sensor = None
        self.debug_wall_sensor = None
        self.max_hp = 3
        self.current_hp = 3

    def load_sprites(self, path, frame_count):
        """
        Load and slice a sprite sheet into individual animation frames.

        Args:
            path: Path to the sprite sheet image file.
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
        Main update loop for the entity.

        Handles AI decision-making, physics movement,
        and animation updates.

        Args:
            dt: Delta time.
            tiles: List of collidable tiles in the level.
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
        Performs environment sensing to steer the enemy.

        Uses invisible rectangles to check:
        1. Floor Sensor
        2. Wall Sensor
        If the path is blocked or safe ground ends, the Frog reverses direction.

        Args:
            tiles: List of collidable tiles.
        """
        offset_x = 20
        check_x = self.rect.centerx + (offset_x * self.direction)
        floor_sensor = pygame.Rect(check_x, self.rect.bottom, 4, 4)

        has_floor = False
        for tile in tiles:
            if tile.colliderect(floor_sensor):
                has_floor = True
                break

        # Wall Sensor
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
        Updates the horizontal velocity based on current direction.
        """
        self.velocity.x = self.speed * self.direction

    def apply_gravity(self, dt):
        """
        Applies gravitational acceleration to the vertical velocity.
        """
        self.velocity.y += config.GRAVITY * dt

    def animate(self, dt):
        """
        Advances the animation frame based on the timer.

        Args:
            dt: Delta time.
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
        Renders a small health bar above the enemy.

        Args:
            screen : The game surface.
            offset: The camera offset.
        """
        bar_width = 14
        bar_height = 2
        offset_y = 5
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
        Renders the Frog sprite and health bar to the screen.

        Args:
            screen: The game surface.
            offset: The camera offset.
        """
        draw_pos = self.rect.topleft + offset

        # Flip sprite if moving left
        if self.direction == 1:
            screen.blit(self.image, draw_pos)
        else:
            flipped = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped, draw_pos)
        self.draw_health_bar(screen, offset)