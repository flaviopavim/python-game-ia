import pygame
import time
import Config
from Player import Player
from Controller import Controller
from Score import Score
from Platform import Platform

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))

# Set up the game clock to control frame rate
clock = pygame.time.Clock()

# Create player and enemy instances
player = Player()
enemy = Player()
enemy.x = Config.WIDTH - 100  # Position the enemy on the right side of the screen

platform_handler = Platform()
controller = Controller()
score = Score()

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

    # Check for key presses
    controller.update(player, bullets)

    # Update player physics
    player.update(platform_handler.platforms)
    
    # Update bullets
    for bullet in bullets:
        bullet.update()
        if (enemy.x < bullet.x < enemy.x + enemy.width or
            enemy.x < bullet.x + bullet.width < enemy.x + enemy.width) and \
            (enemy.y < bullet.y < enemy.y + enemy.height):
                enemy.health -= 10
                bullets.remove(bullet)
                
                    
    # Remove inactive bullets
    bullets = [b for b in bullets if 0 <= b.x <= Config.WIDTH]
    
    # Clear the screen with a white background
    screen.fill(Config.WHITE)

    # Draw the ground
    pygame.draw.rect(screen, Config.BROWN, (0, Config.HEIGHT - Config.GROUND_HEIGHT, Config.WIDTH, Config.GROUND_HEIGHT))
    
    # Draw the platform
    platform_handler.draw(screen)

    # Draw the player
    pygame.draw.rect(screen, Config.BLUE, (player.x, player.y, player.width, player.height))

    if enemy.health > 0:
        # Draw the enemy
        pygame.draw.rect(screen, Config.RED, (enemy.x, enemy.y, enemy.width, enemy.height))
    else:
        pass
    
    # Draw the bullets
    for bullet in bullets:
        bullet.draw(screen)
    
    # Score
    score.update(screen, player)

    # Update the display
    pygame.display.flip()

    # Maintain the game loop at the target FPS
    clock.tick(Config.FPS)