import pygame
import time
import Config
from Player import Player
from Controller import Controller
from Score import Score
from Platform import Platform
from Bullet import Bullet

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))

# Set up the game clock to control frame rate
clock = pygame.time.Clock()

# Create player and enemy instances
player = Player()

enemies = []
enemy_last_shot = []
for i in range(3):
    enemy = Player()
    enemy.x = Config.WIDTH - 100 - i * 100
    enemies.append(enemy)
    enemy_last_shot.append(0)

platform_handler = Platform()
controller = Controller()
score = Score()

# List to store
bullets = []

def draw_game_over(screen):
    font = pygame.font.SysFont("Arial", 72, bold=True)
    text = font.render("GAME OVER", True, Config.RED)
    text_rect = text.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))
    screen.blit(text, text_rect)

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
    
    current_time = pygame.time.get_ticks()
    
    for i, enemy in enumerate(enemies):
        if enemy.health > 0 and current_time - enemy_last_shot[i] > 3000: # 3 seconds cooldown
            bullet_x = enemy.x + (enemy.width / 2)
            bullet_y = enemy.y + (enemy.height / 2)
            bullet = Bullet(bullet_x, bullet_y)
            bullet.direction = "left"
            bullet.from_enemy = True
            bullets.append(bullet)
            enemy_last_shot[i] = current_time

    # Update player physics
    player.update(platform_handler.platforms)
    
    # Update bullets
    for bullet in bullets:
        bullet.update()
        
        if hasattr(bullet, "from_enemy") and bullet.from_enemy:
            if (player.x < bullet.x < player.x + player.width or
                player.x < bullet.x + bullet.width < player.x + player.width) and \
                (player.y < bullet.y < player.y + player.height):
                    player.health -= 10
                    bullets.remove(bullet)
                    continue
        else:
            for enemy in enemies:
                if enemy.health > 0 and \
                (enemy.x < bullet.x < enemy.x + enemy.width or
                 enemy.x < bullet.x + bullet.width < enemy.x + enemy.width) and \
                (enemy.y < bullet.y < enemy.y + enemy.height):
                    enemy.health -= 10
                    bullets.remove(bullet)
                    break
                
                    
    # Remove inactive bullets
    bullets = [b for b in bullets if 0 <= b.x <= Config.WIDTH]
    
    # Clear the screen with a white background
    screen.fill(Config.WHITE)

    # Draw the ground
    pygame.draw.rect(screen, Config.BROWN, (0, Config.HEIGHT - Config.GROUND_HEIGHT, Config.WIDTH, Config.GROUND_HEIGHT))
    
    # Draw the platform
    platform_handler.draw(screen)

    # Draw the player
    if player.health > 0:
        pygame.draw.rect(screen, Config.BLUE, (player.x, player.y, player.width, player.height))
    else:
        draw_game_over(screen)

    for enemy in enemies:
        if enemy.health > 0:
            pygame.draw.rect(screen, Config.RED, (enemy.x, enemy.y, enemy.width, enemy.height))
            
            bar_width = enemy.width
            bar_height = 5
            health_ratio = enemy.health / 100
            bar_x = enemy.x
            bar_y = enemy.y - bar_height - 2 # Position above the enemy
            
            # Draw health bar
            pygame.draw.rect(screen, Config.BLACK, (bar_x, bar_y, bar_width, bar_height))
            
            # Draw the health fill
            pygame.draw.rect(screen, Config.GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))
            
    
    # Draw the bullets
    for bullet in bullets:
        bullet.draw(screen)
    
    # Score
    score.update(screen, player)

    # Update the display
    pygame.display.flip()

    # Maintain the game loop at the target FPS
    clock.tick(Config.FPS)