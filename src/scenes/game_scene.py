import pygame
from src import config
from src.entities.player import Player
from src.core.level_loader import load_level
from src.core.camera import Camera
from src.entities.slime import Slime
from src.entities.frog import Frog
from src.entities.manaicon import ManaIcon
from src.core.ui import UI
import math
import random

class GameScene:
    """
    The main gameplay state where the action takes place.

    This class acts as the central controller for the game level. It manages:
    - Loading and rendering the TMX map.
    - Updating all entities.
    - Handling collisions and combat logic.
    - Managing the camera and UI overlay.
    - Checking Win/Loss conditions.

    Attributes:
        camera: Handles scrolling and centering the view on the player.
        player: The main character entity.
        enemies: A list of active enemy entities.
        projectiles: A list of active projectiles.
        ui: The Heads-Up Display for Health and Mana.
    """
    def __init__(self):
        """
        Initialize the GameScene.

        Loads resources, parses the level data
        from the TMX file, and spawns all entities at their designated positions.
        """
        bg_path = "assets/graphics/background/bg-02.png"

        raw_bg = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(raw_bg, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        music_path = "assets/sounds/music/level_theme.mp3"
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)
        self.collect_sfx = pygame.mixer.Sound("assets/sounds/sfx/pickup.wav")
        self.collect_sfx.set_volume(0.4)
        self.respawn_sfx = pygame.mixer.Sound("assets/sounds/sfx/win.wav")
        self.respawn_sfx.set_volume(0.3)
        self.respawn_sfx.play()

        data = load_level("assets/levels/level1.tmx")
        self.tmx_data = data[0]
        self.walls = data[1]
        self.hazards = data[2]
        self.visuals = data[3]
        spawn_point = data[4]
        slime_spawns = data[5]
        frog_spawns = data[6]
        mana_spawns = data[7]
        self.win_zone = data[8]
        self.has_won = False

        spawn_x, spawn_y = spawn_point
        self.projectiles = []
        self.player = Player(spawn_x, spawn_y,self.projectiles)
        self.ui = UI(self.player)
        self.char_is_dead = False
        self.enemies = []
        self.coins = []
        for pos in slime_spawns:
            self.enemies.append(Slime(pos[0], pos[1]))
        for pos in frog_spawns:
            self.enemies.append(Frog(pos[0], pos[1]))
        for pos in mana_spawns:
            self.coins.append(ManaIcon(pos[0], pos[1]))

        path = "assets/graphics/tilesets/Grass-001.png"
        self.block_img = pygame.image.load(path).convert()

        map_width = self.tmx_data.width * config.TILE_SIZE
        map_height = self.tmx_data.height * config.TILE_SIZE

        self.camera = Camera(map_width, map_height)
        self.damage_overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        border_thickness = 1000
        red_color = (255, 0, 0, 255)
        pygame.draw.rect(self.damage_overlay, red_color, (0, 0, config.SCREEN_WIDTH, border_thickness))
        pygame.draw.rect(self.damage_overlay, red_color,
                         (0, config.SCREEN_HEIGHT - border_thickness, config.SCREEN_WIDTH, border_thickness))
        pygame.draw.rect(self.damage_overlay, red_color, (0, 0, border_thickness, config.SCREEN_HEIGHT))
        pygame.draw.rect(self.damage_overlay, red_color,
                         (config.SCREEN_WIDTH - border_thickness, 0, border_thickness, config.SCREEN_HEIGHT))

    def handle_input(self, event):
        """
        Process specific input events for the scene.

        Args:
            event: The Pygame event to check.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Pauza (TODO)")

    def update(self, dt):
        """
        Update the game logic for a single frame.

        This includes:
        - Checking player life status.
        - Updating physics and movement for Player and Enemies.
        - Handling Camera movement and Screen Shake.
        - Resolving collisions.
        - Cleaning up destroyed entities.

        Args:
            dt: Delta time in seconds.
        """
        if self.player.current_hp <= 0:
            self.char_is_dead = True
            pass
        self.player.update(dt, self.walls)
        self.camera.follow(self.player)
        self.player.check_attack_hit(self.enemies)

        if self.player.stun_timer > 0:
            intensity = 1
            shake_x = 0.1 * random.randint(-intensity, intensity)
            shake_y = 0.1 * random.randint(-intensity, intensity)
            self.camera.offset.x += shake_x

        for enemy in self.enemies:
            enemy.update(dt, self.walls)

        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(10, enemy.rect)

        for mana in self.coins[:]:
            if self.player.rect.colliderect(mana.rect):
                mana.current_hp = 0
                self.player.current_mp += 30
                self.collect_sfx.play()

        if self.win_zone:
            if self.player.rect.colliderect(self.win_zone):
                self.has_won = True

        self.enemies = [e for e in self.enemies if e.current_hp > 0]
        self.coins = [e for e in self.coins if e.current_hp > 0]

        for p in self.projectiles[:]:
            p.update(dt, self.walls, self.enemies)
            if not p.is_alive:
                self.projectiles.remove(p)

        for a in self.coins[:]:
            a.update(dt, self.coins)

    def draw(self, screen):
        """
        Render the game world to the screen.

        Args:
            screen: The main display surface.
        """
        screen.blit(self.background, (0, 0))

        for image, rect in self.visuals:
            draw_pos = rect.topleft + self.camera.offset
            if -64 < draw_pos.x < config.SCREEN_WIDTH + 64 and -64 < draw_pos.y < config.SCREEN_HEIGHT + 64:
                screen.blit(image, draw_pos)

        for enemy in self.enemies:
            enemy.draw(screen, self.camera.offset)

        self.player.draw(screen, self.camera.offset)
        self.ui.draw(screen)

        for p in self.projectiles:
            p.draw(screen, self.camera.offset)

        for a in self.coins[:]:
            a.draw(screen, self.camera.offset)

        if self.player.stun_timer > 0:
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) / 2
            alpha_value = int(pulse * 50)
            self.damage_overlay.set_alpha(alpha_value)
            screen.blit(self.damage_overlay, (0, 0))