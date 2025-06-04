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
        self.from_enemy = False
        
    def update(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))