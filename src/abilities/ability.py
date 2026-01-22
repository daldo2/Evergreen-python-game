class Ability:
    """
        Class representing throwable abilities.

        This class handles the core logic shared by all skills, including:
        - Cooldown management
        - Resource checking (Mana/MP costs).
        - Triggering the effect.

        Attributes:
            owner: The entity that possesses this ability.
            name: The display name of the ability.
            cooldown: The waiting time required between uses.
            mana_cost: The amount of Mana required to cast the ability.
            current_cooldown: The remaining time until the ability is ready.
        """
    def __init__(self, owner, name, cooldown = 1.0, mana_cost = 10):
        """
        Initializes a new Ability instance.

        Args:
            owner: The entity that owns this skill.
            name: A unique identifier for the skill.
            cooldown: Time in seconds before reuse. Defaults to 1.0.
            mana_cost: Mana required to cast. Defaults to 10.
        """
        self.owner = owner
        self.name = name
        self.cooldown = cooldown
        self.mana_cost = mana_cost
        self.current_cooldown = 0

    def update(self, dt):
        """
        Updates the cooldown timer.

        This method must be called every frame in the game loop

        Args:
            dt: Delta time
        """
        if self.current_cooldown > 0:
            self.current_cooldown -= dt

    def can_cast(self):
        """
        Check if the ability is ready to be used.

        Returns True if the ability can be cast, False otherwise.
        """
        if self.current_cooldown > 0:
            return False

        if self.owner.current_mp < self.mana_cost:
            return False

        return True

    def trigger(self):
        """
        Attempts to activate the ability.

        If can_cast() returns True, this method will:
        - Deduct the mana cost from the owner.
        - Reset the cooldown timer.
        - Call the activate() method to perform the skill effect.
        """
        if self.can_cast():
            self.owner.current_mp -= self.mana_cost
            self.current_cooldown = self.cooldown
            self.activate()

    def activate(self):
        """
        Activate the ability

        Takes nothing and returns nothing.
        """
        pass