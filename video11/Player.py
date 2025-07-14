import pygame
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
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.health = 100             # Player life percentage

    def jump(self):
        # Only allow jumping if the player is currently on the ground
        if self.on_ground:
            self.velocity_y = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self, platforms):
        # Apply gravity to the player's vertical movement
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        self.on_ground = False
        
        # Collision detection with platforms
        if self.velocity_y > 0:
            for platform_rect in platforms:
                if self.rect.colliderect(platform_rect):
                    if (self.rect.bottom - self.velocity_y) <= platform_rect.top + 1:
                        if self.rect.bottom >= platform_rect.top:
                            self.rect.bottom = platform_rect.top
                            self.velocity_y = 0
                            self.on_ground = True
                            break
        
        # ground collision detection
        if not self.on_ground:
            if self.rect.bottom>= Config.HEIGHT - Config.GROUND_HEIGHT:
                self.rect.bottom  = Config.HEIGHT - Config.GROUND_HEIGHT
                self.velocity_y = 0
                self.on_ground = True

    def update(self, platforms):
        
        # Update the player's rectangle position
        self.rect.x = self.x
        
        # Update the player's position by applying gravity
        self.apply_gravity(platforms)
        
        self.y = self.rect.y