import pygame
from Bullet import Bullet

# Toggle to select input mode: True = Xbox controller, False = Keyboard
USE_GAMEPAD = True

class Controller:
    def __init__(self):
        self.last_shot_time = 0  # Timestamp of the last bullet shot
        self.joystick = None     # Reference to the connected joystick

        if USE_GAMEPAD:
            pygame.joystick.init()
            if pygame.joystick.get_count() > 0:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                print(f"Gamepad detected: {self.joystick.get_name()}")
            else:
                print("No gamepad detected. Falling back to keyboard.")
                self.joystick = None

    def update(self, player, bullets):
        current_time = pygame.time.get_ticks()

        if USE_GAMEPAD and self.joystick:
            # Get the value of the horizontal axis (left analog stick)
            axis_x = self.joystick.get_axis(0)  # -1 (left) to 1 (right)

            # Move player based on analog stick direction
            if axis_x < -0.2:
                player.x -= 5
                player.direction = "left"
            elif axis_x > 0.2:
                player.x += 5
                player.direction = "right"

            # Jump when pressing button A (usually button index 0)
            if self.joystick.get_button(0):
                player.jump()

            # Shoot when pressing button X (usually button index 2)
            if self.joystick.get_button(2) and current_time - self.last_shot_time > 500:
                bullet_x = player.x + (player.width / 2)
                bullet_y = player.y + (player.height / 2)
                bullet = Bullet(bullet_x, bullet_y)
                bullet.direction = player.direction
                bullets.append(bullet)
                self.last_shot_time = current_time

        else:
            # ----------------------------
            # FALLBACK TO KEYBOARD CONTROL
            # ----------------------------
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                player.x -= 5
                player.direction = "left"

            if keys[pygame.K_RIGHT]:
                player.x += 5
                player.direction = "right"

            if keys[pygame.K_SPACE]:
                player.jump()

            if keys[pygame.K_f] and current_time - self.last_shot_time > 500:
                bullet_x = player.x + (player.width / 2)
                bullet_y = player.y + (player.height / 2)
                bullet = Bullet(bullet_x, bullet_y)
                bullet.direction = player.direction
                bullets.append(bullet)
                self.last_shot_time = current_time
