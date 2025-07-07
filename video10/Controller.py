import pygame
from Bullet import Bullet
import Config

USE_GAMEPAD = True # False to use keyboard controls

class Controller:
    
    def __init__(self):
        self.last_shot_time = 0
        self.joystick = None
        self.start_button_pressed = False
        self.p_key_pressed = False
        
        if USE_GAMEPAD:
            pygame.joystick.init()
            if pygame.joystick.get_count() > 0:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                print(f"Gamepad detected: {self.joystick.get_name()}")
            else:
                print("No gamepad detected. Using keyboard controls.")
                self.joystick = None
                
    def handle_input_events(self, event, game_state):
        
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_SPACE:
                if game_state == Config.GAME_STATE_PRESS_START:
                    game_state = Config.GAME_STATE_PLAYING
                    
            if event.key == pygame.K_p:
                if not self.p_key_pressed:
                    if game_state == Config.GAME_STATE_PLAYING:
                        game_state = Config.GAME_STATE_PAUSED
                    elif game_state == Config.GAME_STATE_PAUSED:
                        game_state = Config.GAME_STATE_PLAYING
                    self.p_key_pressed = True
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                self.p_key_pressed = False
                
        if USE_GAMEPAD and self.joystick:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == Config.JOY_BUTTON_START:
                    if not self.start_button_pressed:
                        if game_state == Config.GAME_STATE_PRESS_START:
                            game_state = Config.GAME_STATE_PLAYING
                        elif game_state == Config.GAME_STATE_PLAYING:
                            game_state = Config.GAME_STATE_PAUSED
                        elif game_state == Config.GAME_STATE_PAUSED:
                            game_state = Config.GAME_STATE_PLAYING
                        self.start_button_pressed = True
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == Config.JOY_BUTTON_START:
                    self.start_button_pressed = False
                    
        return game_state
    
    def update(self, player, bullets):
        
        current_time = pygame.time.get_ticks()
        
        if USE_GAMEPAD and self.joystick:
            axis_x = self.joystick.get_axis(0)  # Left stick horizontal axis
            
            if axis_x < -0.2:
                player.x -= 5
                player.direction = "left"
            elif axis_x > 0.2:
                player.x += 5
                player.direction = "right"
                
            if self.joystick.get_button(0):  # Assuming button 0 is the jump button
                player.jump()  # Make the player jump
                
            if self.joystick.get_button(2) and current_time - self.last_shot_time > 500:
                bullet_x = player.x + (player.width / 2)
                bullet_y = player.y + (player.height / 2)
                bullet = Bullet(bullet_x, bullet_y)
                bullet.direction = player.direction
                bullets.append(bullet)
                self.last_shot_time = current_time
                
        else:
            
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
                
            if keys[pygame.K_f] and current_time - self.last_shot_time > 500:
                # Fire
                bullet_x = player.x + (player.width / 2)
                bullet_y = player.y + (player.height / 2)
                bullet = Bullet(bullet_x, bullet_y)
                bullet.direction = player.direction
                bullets.append(bullet)
                self.last_shot_time = current_time