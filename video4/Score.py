import pygame
import time
import Config

# Font
pygame.font.init()
font = pygame.font.SysFont("arial", 20)  # Você pode trocar por outra fonte

# Score
score = 0
start_time = time.time()

class Score:
    
    def __init__(self):
        pass
    
    
    def draw(self, screen, player):
        score = int(time.time() - start_time)
        
        # Texto
        score_text = font.render(f"Score: {score}", True, Config.BLACK)
        
        # Desenhar na tela
        screen.blit(score_text, (10, 10))  # Draw the score at the top left corner
        
        # Life
        pygame.draw.rect(screen, Config.BLACK, (10, 40, 100, 10))
        pygame.draw.rect(screen, Config.GREEN, (10, 40, player.health, 10))