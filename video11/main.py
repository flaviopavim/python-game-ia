import pygame
import time
import Config
from Player import Player
from Controller import Controller
from Score import Score
from Platform import Platform
from Bullet import Bullet
import numpy as np
import os
from IA import IA

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))

# Set up the game clock to control frame rate
clock = pygame.time.Clock()

game_state = Config.GAME_STATE_PRESS_START

# Create player and enemy instances
player = Player()

NUM_ENEMIES = 5

generation = 1
best_score = 0
enemies = [] # Inimigos
enemies_ais = [] # IA de cada inimigo
enemy_last_shot = [] # Cada inimigo tem seu próprio tempo de tiro
enemy_colors = []
enemy_start_times = [] # Calcular tempo de sobrevivência
enemy_damage_dealt = {} # Dano causado por cada inimigo
enemy_damage_received = {} # Dano recebido por cada inimigo
enemy_jumps_count = {} # Contador de pulos de cada inimigo
enemy_last_jump_time = {} # Tempo do último pulo de cada inimigo

CHECKPOINT_FILE = "checkpoint.npz"

def save_checkpoint(current_generation, current_best_score, current_enemy_ais):
    
    if not current_enemy_ais:
        print("No enemy AI to save.")
        return
    
    # Extract all genomes
    all_genomes = [ia.genome for ia in current_enemy_ais]
    
    # Save fitness values
    fitness_values = [ia.fitness for ia in current_enemy_ais]
    
    genome_dict = {}
    for i, genome in enumerate(all_genomes):
        for j, layer_matrix in enumerate(genome):
            genome_dict[f'ia_{i}_layer_{j}'] = layer_matrix
            
    try:
        np.savez(
            CHECKPOINT_FILE,
            generation=np.array(current_generation),
            best_score=np.array(current_best_score),
            fitness_values=np.array(fitness_values),
            num_enemies=np.array(len(current_enemy_ais)),
            **genome_dict # Unpack the dictionary of genomes
        )
        print(f'Checkpoint saved to {CHECKPOINT_FILE}')
        
    except Exception as e:
        print(f'Error saving checkpoint: {e}')
        
def load_checkpoint():
    
    if os.path.exists(CHECKPOINT_FILE):
        try:
            data = np.load(CHECKPOINT_FILE, allow_pickle=True) #
            
            loaded_generation = data['generation'].item() # .item() to get the scalar value from the array
            loaded_best_score = data['best_score'].item()
            loaded_fitness_values = data['fitness_values']
            loaded_num_enemies = data['num_enemies'].item()
            
            loaded_ais = []
            
            for i in range(loaded_num_enemies):
                genome_parts = []
                j = 0
                while f'ia_{i}_layer_{j}' in data:
                    genome_parts.append(data[f'ia_{i}_layer_{j}'])
                    j += 1
                
                if genome_parts:
                    ia = IA(genome=genome_parts)
                    ia.fitness == loaded_fitness_values[i] if i < len(loaded_fitness_values) else 0.0
                    loaded_ais.append(ia)
                    
            print(f'Checkpoint loaded')
            return loaded_generation, loaded_best_score, loaded_ais
        except Exception as e:
            print(f'Error loading checkpoint: {e}')
            return 1, 0, []
    return 1, 0, []
        
distinct_colors = [
    (255, 165, 0), (128, 0, 128), (0, 128, 0), (0, 255, 255), (255, 0, 255),
    (124, 252, 0), (255, 20, 147), (65, 105, 225), (255, 215, 0), (0, 255, 127),
    (255, 99, 71), (100, 149, 237), (173, 255, 47), (218, 112, 214), (255, 255, 0)
] # Added more distinct colors for more enemies

def create_new_generation(ais_for_next_gen=None):
    global enemies, enemy_ais, enemy_last_shot, enemy_colors, enemy_start_times, \
           enemy_damage_dealt, enemy_damage_received, enemy_jumps_count, \
           enemy_last_jump_time, generation, NUM_ENEMIES

    # Clear previous generation data
    enemies = []
    enemy_ais = []
    enemy_last_shot = []
    enemy_colors = []
    enemy_start_times = []
    enemy_damage_dealt = {}
    enemy_damage_received = {}
    enemy_jumps_count = {}
    enemy_last_jump_time = {}
    
    current_ais = []
    if ais_for_next_gen:
        current_ais = ais_for_next_gen[:]
    else:
        current_ais = [IA() for _ in range(NUM_ENEMIES)]
        
    # Ensure we have enough AI instances
    while len(current_ais) < NUM_ENEMIES:
        current_ais.append(IA())
        
    for i in range(NUM_ENEMIES):
        enemy = Player()
        enemy.x = Config.WIDTH - 100 - (i % 5) * 80
        enemy.y = Config.HEIGHT - Config.GROUND_HEIGHT - enemy.height
        enemies.append(enemy)
        enemy_ais.append(current_ais[i])
        enemy_last_shot.append(0)
        enemy_colors.append(distinct_colors[i % len(distinct_colors)])
        enemy_start_times.append(time.time())
        enemy_damage_dealt[enemy] = 0
        enemy_damage_received[enemy] = 0
        enemy_jumps_count[enemy] = 0
        enemy_last_jump_time[enemy] = 0
    
# Load checkpoint if it exists
initial_generation, initial_best_score, loaded_initial_ais = load_checkpoint()

generation = initial_generation
best_score = initial_best_score

if loaded_initial_ais:
    enemy_ais = loaded_initial_ais
    NUM_ENEMIES = len(loaded_initial_ais)
    
    for i, ia_instance in enumerate(enemy_ais):
        enemy = Player()
        enemy.x = Config.WIDTH - 100 - (i % 5) * 80
        enemy.y = Config.HEIGHT - Config.GROUND_HEIGHT - enemy.height
        enemies.append(enemy)
        enemy_last_shot.append(0)
        enemy_colors.append(distinct_colors[i % len(distinct_colors)])
        enemy_start_times.append(time.time())
        enemy_damage_dealt[enemy] = 0
        enemy_damage_received[enemy] = 0
        enemy_jumps_count[enemy] = 0
        enemy_last_jump_time[enemy] = 0
else:
    create_new_generation()
        
platform_handler = Platform()
platform_handler.generate_random_platforms()

controller = Controller()
score = Score()

# List to store
bullets = []

def draw_text(surface, text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size, bold=True)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)
    
def draw_game_over(screen):
    draw_text(screen, "GAME OVER", 72, Config.RED, Config.WIDTH // 2, Config.HEIGHT // 2)

def draw_press_start(screen):
    screen.fill(Config.BLUE)
    draw_text(screen, "PRESS START", 72, Config.WHITE, Config.WIDTH // 2, Config.HEIGHT // 2 - 50)
    draw_text(screen, "Press Space or Start on Gamepad", 30, Config.WHITE, Config.WIDTH // 2, Config.HEIGHT // 2 + 20)

def draw_paused(screen):
    overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    draw_text(screen, "PAUSED", 72, Config.YELLOW, Config.WIDTH // 2, Config.HEIGHT // 2 - 50)
    draw_text(screen, "Press P ou START to Resume", 30, Config.YELLOW, Config.WIDTH // 2, Config.HEIGHT // 2 + 20)

# ------------------------------
# Main game loop
# ------------------------------
while True:
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_checkpoint(generation, best_score, enemy_ais)
            pygame.quit()
            exit()
            
        game_state = controller.handle_input_events(event, game_state)
        
    if game_state == Config.GAME_STATE_PRESS_START:
        screen.fill(Config.BLUE)
        draw_press_start(screen)
        pygame.display.flip()
        clock.tick(Config.FPS)
        continue
    
    if game_state == Config.GAME_STATE_PAUSED:
        draw_paused(screen)
        pygame.display.flip()
        clock.tick(Config.FPS)
        continue
    
    current_time_ms = pygame.time.get_ticks()
    current_time_sec = time.time()    

    # Check for key presses
    controller.update(player, bullets)
    
    player.x = max(0, min(player.x, Config.WIDTH - player.width))
    player.y = max(0, player.y)
    
    bullets_info = []
    for bullet in bullets:
        bullets_info.append({
            'x': bullet.x,
            'y': bullet.y,
            'direction': bullet.direction,
            'from_enemy': bullet.from_enemy
        })
        
    platforms_info = []
    for platform_rect in platform_handler.platforms:
        platforms_info.append({
            'x': platform_rect.x,
            'y': platform_rect.y,
            'width': platform_rect.width
        })
        
    alive_enemies_count = 0
    for i, enemy in enumerate(enemies):
        if enemy.health > 0:
            alive_enemies_count += 1
            
            actions = enemy_ais[i].choose_action(player.x, player.y, enemy, bullets_info, platforms_info)
            
            if actions['move_left']:
                enemy.x -= 3
            if actions['move_right']:
                enemy.x += 3
                
            if actions['jump'] and (current_time_ms - enemy_last_jump_time.get(enemy, 0) > 1000):
                if enemy.jump():
                    enemy_jumps_count[enemy] = enemy_jumps_count.get(enemy, 0) + 1
                    enemy_last_jump_time[enemy] = current_time_ms
                    
            enemy.x = max(0, min(enemy.x, Config.WIDTH - enemy.width))
            enemy.y = max(0, enemy.y)
            
            if actions['shoot'] and current_time_ms - enemy_last_shot[i] > 1000: # 1 second cooldown
                bullet_x = enemy.x + (enemy.width / 2)
                bullet_y = enemy.y + (enemy.height / 2)
                bullet = Bullet(bullet_x, bullet_y, shooter_id=id(enemy))
                
                if player.x < enemy.x:
                    bullet.direction = "left"
                else:
                    bullet.direction = "right"
                bullet.from_enemy = True
                bullets.append(bullet)
                enemy_last_shot[i] = current_time_ms
    
    player.update(platform_handler.platforms)
    
    for enemy in enemies:
        enemy.update(platform_handler.platforms)
        
    bullets_to_remove = []
    for bullet in bullets:
        bullet.update()
        
        if not (0<=bullet.x <= Config.WIDTH):
            bullets_to_remove.append(bullet)
            continue
        
        if hasattr(bullet, "from_enemy") and bullet.from_enemy:
            if player.rect.colliderect(pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)):
                player.health -= 10
                if bullet.shooter_id in enemies:
                    for enemy_instance in enemies:
                        if id(enemy_instance) == bullet.shooter_id:
                            enemy_damage_dealt[enemy_instance] = enemy_damage_dealt.get(enemy_instance, 0) + 10
                            break
                bullets_to_remove.append(bullet)
        else:
            for i, enemy in enumerate(enemies):
                if enemy.health > 0 and \
                    pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height).colliderect(enemy.rect):
                        enemy.health -= 25
                        bullets_to_remove.append(bullet)
                        enemy_damage_received[enemy] = enemy_damage_received.get(enemy, 0) + 10
                        break
                    
    bullets = [b for b in bullets if b not in bullets_to_remove]
    
    player_won_round = False
    if alive_enemies_count == 0:
        player_won_round = True
        
    if player.health <= 0 or alive_enemies_count == 0:
        current_player_score = int(time.time() - score.start_time)
        if current_player_score > best_score:
            best_score = current_player_score
            
        for i, enemy_instance in enumerate(enemies):
            time_survived = current_time_sec - enemy_start_times[i]
            damage_dealt = enemy_damage_dealt.get(enemy_instance, 0)
            damage_received = enemy_damage_received.get(enemy_instance, 0)
            jumps_count = enemy_jumps_count.get(enemy_instance, 0)
            
            enemy_ais[i].calculate_fitness(
                time_survived,
                damage_dealt,
                damage_received,
                jumps_count
            )
        
        evolved_ais = IA.evolve_population(enemy_ais, NUM_ENEMIES)

        save_checkpoint(generation, best_score, evolved_ais)
        
        player = Player()  # Reset player
        score = Score()  # Reset score
        generation += 1
        create_new_generation(evolved_ais)
        platform_handler.generate_random_platforms()  # Reset platforms
        bullets = []
        game_state = Config.GAME_STATE_PRESS_START
    
    screen.fill(Config.BACKGROUND_COLOR)
    
    pygame.draw.rect(screen, Config.BROWN, (0, Config.HEIGHT - Config.GROUND_HEIGHT, Config.WIDTH, Config.GROUND_HEIGHT))
    
    platform_handler.draw(screen)
    
    if player.health > 0:
        pygame.draw.rect(screen, Config.BLUE, (player.x, player.y, player.width, player.height))
    else:
        draw_game_over(screen)
        game_state = Config.GAME_STATE_GAME_OVER
        
    for i, enemy in enumerate(enemies):
        if enemy.health > 0:
            pygame.draw.rect(screen, enemy_colors[i], (enemy.x, enemy.y, enemy.width, enemy.height))
            
            bar_width = enemy.width
            bar_height = 5
            health_ratio = enemy.health / 100
            bar_x = enemy.x
            bar_y = enemy.y - bar_height - 2
            
            pygame.draw.rect(screen, Config.BLACK, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, Config.GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))
            
    for bullet in bullets:
        bullet.draw(screen)
    
    score.update(screen, player)
    
    font = pygame.font.SysFont("Arial", 20)
    generation_text = font.render(f"Generation: {generation}", True, Config.BLACK)
    screen.blit(generation_text, (10, 60))
    
    best_score_text = font.render(f"Best Score: {best_score}", True, Config.BLACK)
    screen.blit(best_score_text, (10, 80))
    
    alive_enemies_text = font.render(f"Alive Enemies: {alive_enemies_count}", True, Config.BLACK)
    screen.blit(alive_enemies_text, (10, 100))
    
    # Update the display
    pygame.display.flip()

    # Maintain the game loop at the target FPS
    clock.tick(Config.FPS)