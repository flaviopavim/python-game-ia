import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions and frames per second
WIDTH, HEIGHT = 800, 600
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define some color constants (RGB format)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (150, 100, 0)
YELLOW = (255, 255, 0)

# Height of the ground platform
GROUND_HEIGHT = 50

# Set up the game clock to control frame rate
clock = pygame.time.Clock()

# Adicione no início após pygame.init()
pygame.font.init()
font = pygame.font.SysFont("arial", 20)  # Você pode trocar por outra fonte

# Score inicial
score = 0

# ------------------------------
# Player class definition
# ------------------------------
class Player():
    
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = 20
        self.y = HEIGHT - GROUND_HEIGHT - self.height
        
        self.direction = "right"  # Direction the player is facing
        
        self.velocity_y = 0           # Vertical velocity for jumping and falling
        self.gravity = 0.8            # Gravity force applied each frame
        self.jump_strength = 15       # How strong the jump is
        self.on_ground = True         # Whether the player is on the ground

    def jump(self):
        # Only allow jumping if the player is currently on the ground
        if self.on_ground:
            self.velocity_y = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self):
        # Apply gravity to the player's vertical movement
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Check if the player has landed on the ground
        if self.y >= HEIGHT - GROUND_HEIGHT - self.height:
            self.y = HEIGHT - GROUND_HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True

    def update(self):
        # Update the player's position by applying gravity
        self.apply_gravity()
        
class Bullet():
    
    def __init__(self, x, y):
        self.width = 10
        self.height = 5
        self.x = x
        self.y = y
        self.speed = 10
        self.color = YELLOW
        self.direction = "right"
        
    def update(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    

# Create player and enemy instances
player = Player()
enemy = Player()
enemy.x = WIDTH - 100  # Position the enemy on the right side of the screen

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

    # Key press detection
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5  # Move player left
        player.direction = "left"  # Update direction
    if keys[pygame.K_RIGHT]:
        player.x += 5  # Move player right
        player.direction = "right"  # Update direction
    if keys[pygame.K_SPACE]:
        player.jump()  # Make the player jump
        
    if keys[pygame.K_f]:
        # Fire
        bullet_x = player.x + (player.width / 2)
        bullet_y = player.y + (player.height / 2)
        bullet = Bullet(bullet_x, bullet_y)
        bullet.direction = player.direction
        bullets.append(bullet)

    # Update player physics
    player.update()
    
    # Update bullets
    for bullet in bullets:
        bullet.update()

    # Clear the screen with a white background
    screen.fill(WHITE)

    # Draw the ground
    pygame.draw.rect(screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

    # Draw the player
    pygame.draw.rect(screen, BLUE, (player.x, player.y, player.width, player.height))

    # Draw the enemy
    pygame.draw.rect(screen, RED, (enemy.x, enemy.y, enemy.width, enemy.height))
    
    # Draw the bullets
    for bullet in bullets:
        bullet.draw(screen)
        
    # Texto
    score_text = font.render(f"Score: {score}", True, BLACK)
    
    # Desenhar na tela
    screen.blit(score_text, (10, 10))  # Draw the score at the top left corner
    

    # Update the display
    pygame.display.flip()

    # Maintain the game loop at the target FPS
    clock.tick(FPS)