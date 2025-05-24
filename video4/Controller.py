import pygame
from Bullet import Bullet

class Controller:
    
    def __init__(self):
        pass
    
    def update(self, player, bullets, last_shot_time):
        
        current_time = pygame.time.get_ticks()
        
        # Key press detection
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 5  # Move player left
            player.direction = "left"  # Update direction
        if keys[pygame.K_RIGHT]:
            player.x += 5  # Move player right
            player.direction = "right"  # Update direction
        if keys[pygame.K_UP]:
            player.jump()  # Make the player jump
            
        if keys[pygame.K_SPACE] and current_time - last_shot_time > 500:
            # Fire
            bullet_x = player.x + (player.width / 2)
            bullet_y = player.y + (player.height / 2)
            bullet = Bullet(bullet_x, bullet_y)
            bullet.direction = player.direction
            bullets.append(bullet)
            last_shot_time = current_time