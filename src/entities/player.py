import pygame
from src import config
from src.core.physics import move_and_slide
from src.abilities.fireball import Fireball

class Player:
    """
    The main player entity controlled by the user.

    This class acts as a central state machine for the main character. It handles:
    - Physics.
    - State Management.
    - Animation switching based on current state.
    - Health/Mana stats and taking damage.
    - Input handling from the keyboard.

    Attributes:
        rect: The physics hitbox.
        velocity: Current motion vector.
        facing_right: flag for sprite orientation.
        frames: Lists containing the sliced animation frames for various states.
        fireball_ability: Instance of the Fireball class for casting spells.
    """
    def __init__(self, x, y, projectile_list):
        """
        Initialize the Player.

        Args:
            x: Starting X coordinate.
            y: Starting Y coordinate.
            projectile_list: Reference to the main game scene's projectile list.
        """
        self.rect = pygame.Rect(x, y, config.TILE_SIZE, config.TILE_SIZE * 2)
        path = "assets/graphics/player/Wizard-0001.png"
        raw_image = pygame.image.load(path).convert_alpha()
        self.idle_image = pygame.transform.scale(raw_image, (32, 64))
        self.image = pygame.image.load(path)

        self.velocity = pygame.Vector2(0, 0)
        self.speed = 200
        self.is_grounded = False
        self.facing_right = True
        self.jump_pressed = False
        self.double_jump_pressed = False
        self.is_crouching = False
        self.possible_to_stand = False
        self.is_standing = False
        self.is_casting = False
        self.is_attacking = False
        self.damage_dealt = False
        self.is_dashing = False

        self.dash_duration = 0.2
        self.dash_timer = 0
        self.dash_speed = 600
        self.dash_cooldown = 0
        self.dash_cooldown_max = 1.0

        self.double_jump_option = True
        self.fireball_option = True
        self.running = False
        self.fireball_timer = 0
        self.fireball_cooldown = 5
        self.fireball_ability = Fireball(self, projectile_list)

        self.max_hp = 30
        self.current_hp = 30
        self.max_mp = 50
        self.current_mp = 0
        self.invincible_timer = 0
        self.invincible_duration = 2.0
        self.stun_timer = 0

        self.frames_idle = []
        self.frames_run = []
        self.frames_crouch = []
        self.frames_cast = []
        self.frames_attack = []
        self.frames_breath = []

        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.08

        self.debug_attack_rect = None

        self.load_crouch_sprites("assets/graphics/player/crunching.png", 8)
        self.load_run_sprites("assets/graphics/player/running.png", 4)
        self.load_cast_sprites("assets/graphics/player/casting.png", 6)
        self.load_attack_sprites("assets/graphics/player/attacking.png", 8)
        self.load_breath_sprites("assets/graphics/player/breathing.png", 3)
        self.attack_sfx = pygame.mixer.Sound("assets/sounds/sfx/attack.wav")
        self.attack_sfx.set_volume(0.2)
        self.dash_sfx = pygame.mixer.Sound("assets/sounds/sfx/jump.wav")
        self.dash_sfx.set_volume(0.1)
        self.jump_sfx = pygame.mixer.Sound("assets/sounds/sfx/dash.wav")
        self.jump_sfx.set_volume(0.15)

        # Default image
        self.image = self.frames_crouch[0]

    def load_crouch_sprites(self, path, frame_count):
        """
        Load and slice the crouching animation sprites.

        Args:
            path: File path to the sprite sheet.
            frame_count: Number of frames to slice from the sheet.
        """
        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            # Scale to player size
            scaled_frame = pygame.transform.scale(frame, (32, 64))
            self.frames_crouch.append(scaled_frame)

    def load_breath_sprites(self, path, frame_count):
        """
        Load and slice the breathing animation sprites.
        """
        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (32, 64))
            self.frames_breath.append(scaled_frame)

    def load_run_sprites(self, path, frame_count):
        """
        Load and slice the running animation sprites.
        """
        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (32, 64))
            self.frames_run.append(scaled_frame)

    def load_attack_sprites(self, path, frame_count):
        """
            Load and slice the attacking animation sprites.
        """
        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (64, 64))
            self.frames_attack.append(scaled_frame)

    def load_cast_sprites(self, path, frame_count):
        """
        Load and slice the attacking animation sprites.
        """
        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (32, 64))
            self.frames_cast.append(scaled_frame)

    def update(self, dt, tiles):
        """
        Main update loop for the player.

        Executes the following logic in order:
        1. Updates Dash cooldowns and logic.
        2. Handles Input.
        3. Applies Gravity.
        4. Moves the entity and resolves collisions.
        5. Updates Grounded state.
        6. Updates Invincibility timers.
        7. Checks if the player can stand up.
        8. Updates Animation and Abilities.

        Args:
            dt: Delta time in seconds.
            tiles: List of solid rectangles for collision detection.
        """
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt

        if self.is_dashing:
            self.dash_timer -= dt

            if self.facing_right:
                self.velocity.x = self.dash_speed
            else:
                self.velocity.x = -self.dash_speed

            self.velocity.y = 0

            if self.dash_timer <= 0:
                self.is_dashing = False
                self.velocity.x = 0

        if not self.is_dashing and self.stun_timer <= 0:
            self.handle_input()
        elif self.stun_timer > 0:
            self.stun_timer -= dt
            self.velocity.x *= 0.95

        if not self.is_dashing:
            self.apply_gravity(dt)

        self.rect, collisions = move_and_slide(self.rect, self.velocity, tiles, dt)

        if collisions['right'] or collisions['left']:
            self.is_standing = True
            self.running = False

        if collisions['bottom']:
            self.is_grounded = True
            self.velocity.y = 0
            self.double_jump_pressed = False

        else:
            self.is_grounded = False


        if collisions['top']:
            self.velocity.y = 0

        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        self.can_stand(dt, tiles)
        self.animate(dt)
        self.fireball_ability.update(dt)

    def handle_input(self):
        """
        Process keyboard input.

        Handles Left/Right movement, Jumping (Z), Dashing (Shift),
        Crouching (Down), Melee Attack (X), and Fireball (V).
        """
        keys = pygame.key.get_pressed()
        self.velocity.x = 0

        self.running = False

        if keys[pygame.K_LSHIFT] and self.dash_cooldown <= 0 and not self.is_attacking and not self.is_casting and not self.is_crouching:
            self.start_dash()
            return

        if not self.is_casting:
            if keys[pygame.K_LEFT]:
                self.velocity.x = -self.speed
                self.facing_right = False
                self.running = True
            if keys[pygame.K_RIGHT]:
                self.velocity.x = self.speed
                self.facing_right = True
                self.running = True

        if keys[pygame.K_z]:
            if not self.jump_pressed:
                if self.is_grounded:
                    self.jump()
                elif not self.double_jump_pressed:
                    self.jump()
                    self.double_jump_pressed = True

                self.jump_pressed = True
        else:
            self.jump_pressed = False

        if keys[pygame.K_DOWN] and (self.is_grounded or self.is_crouching):
            self.is_crouching = True
            self.is_standing = False
        else:
            if self.is_crouching and self.possible_to_stand:
                self.is_crouching = False
                self.stand_up()

        if self.is_standing:

            if keys[pygame.K_v] and self.fireball_option and not self.is_casting:
                self.fireball_ability.trigger()
                self.is_casting = True
                self.frame_index = 0

            if keys[pygame.K_x] and not self.is_attacking and not self.is_casting:
                self.frame_index = 0
                self.is_attacking = True
                self.attack_sfx.play()

    def can_stand(self, dt, tiles):
        """
        Check if there is enough ceiling clearance to stand up.

        Used when the player releases the crouch button. If a tile is immediately
        above the player, they are forced to remain crouching.

        Args:
            dt: Delta time.
            tiles: List of collision tiles.
        """
        self.possible_to_stand = True
        top_rectangle = pygame.Rect(self.rect.x, self.rect.y - 32, self.rect.width, 32)
        for tile in tiles:
            if top_rectangle.colliderect(tile):
                self.possible_to_stand = False
        self.debug_attack_rect = top_rectangle

    def stand_up(self):
        """
        Restore the hitbox to full height (64px).
        """
        if self.rect.height != 64:
            self.rect = pygame.Rect(self.rect.x, self.rect.y - 32, 32, 64)

    def shrink_hitbox(self):
        """
        Reduce the hitbox height (32px) for crouching.
        """
        if self.rect.height != 32:
            self.rect = pygame.Rect(self.rect.x, self.rect.y + 32, 32, 32)

    def apply_gravity(self, dt):
        """
        Apply variable gravity.

        Gravity is stronger when falling or when the jump button is released early.

        Args:
            dt: Delta time.
        """
        current_gravity = config.GRAVITY

        if self.velocity.y > 0:
            current_gravity *= 1.3

        elif self.velocity.y < 0 and not pygame.key.get_pressed()[pygame.K_z]:
            current_gravity *= 3.0

        self.velocity.y += current_gravity * dt

    def jump(self):
        """
        Apply vertical force to jump and play sound.
        """
        self.jump_sfx.play()
        self.velocity.y = config.JUMP_FORCE

    def check_attack_hit(self, enemies):
        """
        Handle melee combat logic.

        Creates a temporary hitbox in front of the player
        at a specific frame of the attack animation. If enemies overlap, they take damage.

        Args:
            enemies: List of enemy entities to check against.
        """
        if self.is_attacking and self.frame_index == 3 and self.damage_dealt == False:
            attack_rect = None

            if self.facing_right:
                attack_rect = pygame.Rect(self.rect.right, self.rect.y + 16, 32, 32)
            else:
                attack_rect = pygame.Rect(self.rect.left - 32, self.rect.y + 16, 32, 32)


            for enemy in enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.current_hp -= 1
                    self.damage_dealt = True


                    if self.facing_right:
                        enemy.velocity.x = 400
                    else:
                        enemy.velocity.x = -400
                    enemy.velocity.y = -200

    def start_dash(self):
        """
        Initialize the dash action.
        """
        self.dash_sfx.play()
        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.dash_cooldown = self.dash_cooldown_max
        self.frame_index = 0

    def take_damage(self, amount, source_rect):
        """
        Process damage taken by the player.

        Reduces HP, sets invincibility, applies stun/knockback relative
        to the damage source.

        Args:
            amount: Amount of HP to lose.
            source_rect: The hitbox of the object causing damage.
        """
        if self.invincible_timer <= 0:
            self.current_hp -= amount
            self.invincible_timer = self.invincible_duration
            self.stun_timer = 1

            # Knock back
            self.velocity.y = -400
            if source_rect.right > self.rect.right:
                self.velocity.x = -200
            else:
                self.velocity.x = 200

    def animate(self, dt):
        """
        Update the player's sprite based on current state.

        Args:
            dt: Delta time.
        """
        self.animation_timer += dt

        if self.is_attacking:
            attack_speed = 0.035
            if self.animation_timer >= attack_speed:
                self.animation_timer = 0
                if self.frame_index < len(self.frames_attack) - 1:
                    self.frame_index += 1
                else:
                    self.is_attacking = False
                    self.damage_dealt = False
                    self.frame_index = 0
            if self.frame_index >= len(self.frames_attack):
                self.frame_index = 0
            self.image = self.frames_attack[self.frame_index]


        elif self.is_casting:
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if self.frame_index < len(self.frames_cast) - 1:
                    self.frame_index += 1
                else:
                    self.is_casting = False
                    self.frame_index = 0
            if self.frame_index >= len(self.frames_cast): self.frame_index = 0
            self.image = self.frames_cast[self.frame_index]


        elif self.is_crouching:
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                # Increment frame only if we haven't reached the end
                if self.frame_index < len(self.frames_crouch) - 1:
                    self.frame_index += 1
                else:
                    self.shrink_hitbox()
            if self.frame_index >= len(self.frames_crouch): self.frame_index = 0
            self.image = self.frames_crouch[self.frame_index]


        elif self.running:
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if self.frame_index < len(self.frames_run) - 1:
                    self.frame_index += 1
                else :
                    self.frame_index = 0
            if self.frame_index >= len(self.frames_run): self.frame_index = 0
            self.image = self.frames_run[self.frame_index]


        else:
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if self.frame_index < len(self.frames_breath) - 1:
                    self.frame_index += 1
                else:
                    self.frame_index = 0

            if self.frame_index >= len(self.frames_breath): self.frame_index = 0
            self.image = self.frames_breath[self.frame_index]
            self.is_standing = True

    def draw(self, screen, offset):
        """
        Render the player to the screen.

        Applies camera offset and flips the sprite horizontally if facing left.

        Args:
            screen: Main display surface.
            offset: Camera position vector.
        """
        draw_pos = self.rect.topleft + offset

        width_diff = self.image.get_width() - self.rect.width

        if width_diff > 0 and not self.facing_right:
            draw_pos.x -= width_diff

        if self.rect.height == 32:
            draw_pos.y -= 32
        if not self.facing_right:
            screen.blit(self.image, draw_pos)
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, draw_pos)

        if self.debug_attack_rect:
            debug_pos = self.debug_attack_rect.move(offset)