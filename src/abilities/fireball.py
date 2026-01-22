import pygame
from src.abilities.ability import Ability
from src.entities.projectile import Projectile

class Fireball(Ability):
    """
    A specific ability that casts a projectile forward.

    Inherits from the Ability base class. It handles creating a Projectile entity
    at the correct position relative to the owner and playing a sound effect.
    """
    def __init__(self, owner, projectile_list):
        """
        Initialize the Fireball ability.

        Sets specific stats for this spell:
        - Name: "fireball"
        - Cooldown: 0.5 seconds
        - Mana Cost: 10 MP

        Args:
            owner: The entity casting the spell.
            projectile_list: A reference to the main game loop's list of projectiles,
                             used to register the new fireball so it can be updated.
        """
        super().__init__(owner, "fireball", cooldown = 0.5, mana_cost = 10)
        self.projectile_list = projectile_list
        self.shoot_sfx = pygame.mixer.Sound("assets/sounds/sfx/shoot.wav")
        self.shoot_sfx.set_volume(0.4)

    def activate(self):
        """
        Execute the fireball logic.

        This method is called automatically by the base Ability class when trigger() is successful.
        It performs the following:
        1. Calculates the spawn Y position.
        2. Plays the shooting sound effect.
        3. Determines direction and spawn X position based on which way the owner is facing.
        4. Creates a new Projectile object .
        """
        spawn_y = self.owner.rect.centery - 8
        self.shoot_sfx.play()

        if self.owner.facing_right:
            spawn_x = self.owner.rect.right
            direction = 1
        else:
            spawn_x = self.owner.rect.left - 16
            direction = -1

        new_fireball = Projectile(spawn_x, spawn_y, direction)
        self.projectile_list.append(new_fireball)