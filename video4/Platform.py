import pygame
import Config

class Platform:
    
    def __init__(self):
        self.platforms = [
            pygame.Rect(200, 450, 100, 20),
            pygame.Rect(400, 350, 120, 20),
            pygame.Rect(600, 250, 100, 20),
            pygame.Rect(100, 150, 150, 20)
        ]
    
    def draw(self, screen):
        
        for platform in self.platforms:
            pygame.draw.rect(screen, Config.BLACK, platform)