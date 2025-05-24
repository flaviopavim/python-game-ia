import pygame
import Config

class Bullet():
    
    def __init__(self, x, y):
        self.width = 10
        self.height = 5
        self.x = x
        self.y = y
        self.speed = 10
        self.color = Config.YELLOW
        self.direction = "right"
        
    def update(self, bullets, enemy):
        # Update bullets
        for bullet in bullets:
            if self.direction == "right":
                self.x += self.speed
            elif self.direction == "left":
                self.x -= self.speed
            if (enemy.x < bullet.x < enemy.x + enemy.width or
                enemy.x < bullet.x + bullet.width < enemy.x + enemy.width) and \
                (enemy.y < bullet.y < enemy.y + enemy.height):
                    enemy.health -= 10
                    bullets.remove(bullet)        
            
    
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))