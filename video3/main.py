import pygame
import time

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

# Font
pygame.font.init()
font = pygame.font.SysFont("arial", 20)  # Você pode trocar por outra fonte

# Score
score = 0
start_time = time.time()

# Shot cooldown
SHOOT_DELAY = 500  # in milliseconds
last_shot_time = 0

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
        
        self.health = 100             # Player life percentage

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
    
    current_time = pygame.time.get_ticks()
    
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
        
    if keys[pygame.K_f] and current_time - last_shot_time > SHOOT_DELAY:
        # Fire
        bullet_x = player.x + (player.width / 2)
        bullet_y = player.y + (player.height / 2)
        bullet = Bullet(bullet_x, bullet_y)
        bullet.direction = player.direction
        bullets.append(bullet)
        last_shot_time = current_time

    # Update player physics
    player.update()
    
    # Update bullets
    for bullet in bullets:
        bullet.update()
        if (enemy.x < bullet.x < enemy.x + enemy.width or
            enemy.x < bullet.x + bullet.width < enemy.x + enemy.width) and \
            (enemy.y < bullet.y < enemy.y + enemy.height):
                enemy.health -= 10
                bullets.remove(bullet)
                
                    
    # Remove inactive bullets
    bullets = [b for b in bullets if 0 <= b.x <= WIDTH]
    
    # Clear the screen with a white background
    screen.fill(WHITE)

    # Draw the ground
    pygame.draw.rect(screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

    # Draw the player
    pygame.draw.rect(screen, BLUE, (player.x, player.y, player.width, player.height))

    if enemy.health > 0:
        # Draw the enemy
        pygame.draw.rect(screen, RED, (enemy.x, enemy.y, enemy.width, enemy.height))
    else:
        pass
    
    # Draw the bullets
    for bullet in bullets:
        bullet.draw(screen)
        
    score = int(time.time() - start_time)
        
    # Texto
    score_text = font.render(f"Score: {score}", True, BLACK)
    
    # Desenhar na tela
    screen.blit(score_text, (10, 10))  # Draw the score at the top left corner
    
    # Life
    pygame.draw.rect(screen, BLACK, (10, 40, 100, 10))
    pygame.draw.rect(screen, GREEN, (10, 40, player.health, 10))
    
    # Enemy life
    pygame.draw.rect(screen, BLACK, (WIDTH - 110, 40, 100, 10))
    pygame.draw.rect(screen, GREEN, (WIDTH - 110, 40, max(enemy.health, 0), 10))
    

    # Update the display
    pygame.display.flip()

    # Maintain the game loop at the target FPS
    clock.tick(FPS)