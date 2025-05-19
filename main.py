import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (150, 100, 0)

GROUND_HEIGHT = 50

clock = pygame.time.Clock()

class Player():
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = 20
        self.y = HEIGHT - GROUND_HEIGHT - self.height
        
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_strength = 15
        self.on_ground = True
        
    def jump(self):
        if self.on_ground:
            self.velocity_y = -self.jump_strength
            self.on_ground = False
            
    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # Verifica se o jogador atingiu o chão
        if self.y >= HEIGHT - GROUND_HEIGHT - self.height:
            self.y = HEIGHT - GROUND_HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True
        
            
    def update(self):
        self.apply_gravity()
        
class Enemy():
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = WIDTH - 100
        self.y = HEIGHT - GROUND_HEIGHT - self.height

player = Player()
enemy = Enemy()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # Teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE]:
        player.jump()
        
    # Atualiza o jogador
    player.update()
    
    screen.fill(WHITE)
    
    # Chão
    pygame.draw.rect(screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    
    # Player
    pygame.draw.rect(screen, BLUE, (player.x, player.y, player.width, player.height))
    
    # Enemy
    pygame.draw.rect(screen, RED, (enemy.x, enemy.y, enemy.width, enemy.height))
    
    pygame.display.flip()
    clock.tick(FPS)