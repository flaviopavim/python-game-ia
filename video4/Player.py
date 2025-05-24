import Config

# ------------------------------
# Player class definition
# ------------------------------
class Player():
    
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = 20
        self.y = Config.HEIGHT - Config.GROUND_HEIGHT - self.height
        
        self.direction = "right"  # Direction the player is facing
        
        self.velocity_y = 0           # Vertical velocity for jumping and falling
        self.gravity = 0.8            # Gravity force applied each frame
        self.jump_strength = 15       # How strong the jump is
        self.on_ground = True         # Whether the player is on the ground
        
        self.health = 100             # Player life percentage

    def jump(self):
        # Only allow jumping if the player is currently on the ground
        if self.on_ground:
            self.velocity_y = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self):
        # Apply gravity to the player's vertical movement
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Check if the player has landed on the ground
        if self.y >= Config.HEIGHT - Config.GROUND_HEIGHT - self.height:
            self.y = Config.HEIGHT - Config.GROUND_HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True

    def update(self):
        # Update the player's position by applying gravity
        self.apply_gravity()