import pygame
import Config
from Controller import Controller
from Player import Player
from Score import Score

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))

# Set up the game clock to control frame rate
clock = pygame.time.Clock()

# Shot cooldown
last_shot_time = 0

platforms = [
    pygame.Rect(200, 450, 100, 20),
    pygame.Rect(400, 350, 120, 20),
    pygame.Rect(600, 250, 100, 20),
    pygame.Rect(100, 150, 150, 20)
]

# Create player and enemy instances
player = Player()
enemy = Player()
enemy.x = Config.WIDTH - 100  # Position the enemy on the right side of the screen

# List to store
bullets = []

# ------------------------------
# Main game loop
# ------------------------------
while True:
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    Controller().update(player, bullets, last_shot_time)

    # Update player physics
    player.update()
     
    # Update bullets
    for bullet in bullets:
        bullet.update(bullets, enemy)
                
    # Remove inactive bullets
    bullets = [b for b in bullets if 0 <= b.x <= Config.WIDTH]
    
    # Clear the screen with a white background
    screen.fill(Config.WHITE)

    # Draw the ground
    pygame.draw.rect(screen, Config.BROWN, (0, Config.HEIGHT - Config.GROUND_HEIGHT, Config.WIDTH, Config.GROUND_HEIGHT))
    
    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, Config.BLACK, platform)

    # Draw the player
    pygame.draw.rect(screen, Config.BLUE, (player.x, player.y, player.width, player.height))

    if enemy.health > 0:
        # Draw the enemy
        pygame.draw.rect(screen, Config.RED, (enemy.x, enemy.y, enemy.width, enemy.height))
    
    # Draw the bullets
    for bullet in bullets:
        bullet.draw(screen)
        
    # Draw the health bar
    Score().draw(screen, player)
    
    # Update the display
    pygame.display.flip()

    # Maintain the game loop at the target FPS
    clock.tick(Config.FPS)