import pygame
import Config
import random

class Platform:
    
    def __init__(self):
        self.platforms = []
        self.generate_random_platforms()
            
    def generate_random_platforms(self):
        
        self.platforms = []
        
        num_platforms = random.randint(3, 10)
        min_distance = 100
        
        while len(self.platforms) < num_platforms:
            
            width = random.randint(80, 150)
            height = 20
            
            x = random.randint(0, Config.WIDTH - width)
            y = random.randint(Config.HEIGHT // 3, Config.HEIGHT - Config.GROUND_HEIGHT - height - 50)
            
            new_platform_rect = pygame.Rect(x, y, width, height)
            
            overlap = False # Sobreposição
            for existing_platform in self.platforms:
                if new_platform_rect.colliderect(existing_platform):
                    overlap = True
                    break
                
                if (abs(new_platform_rect.x - existing_platform.x) < min_distance or
                    abs(new_platform_rect.x + new_platform_rect.width - existing_platform.x) < min_distance or
                    abs(existing_platform.x + existing_platform.width - new_platform_rect.x) < min_distance):
                    
                    if abs(new_platform_rect.y - existing_platform.y) < existing_platform.height * 2:
                        overlap = True
                        break
            
            if not overlap:
                self.platforms.append(new_platform_rect)
            
    
    def draw(self, screen):
        
        for platform in self.platforms:
            pygame.draw.rect(screen, Config.BLACK, platform)