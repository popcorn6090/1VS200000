import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up game window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders 2D")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Player settings
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
player_speed = 5

# Chicken settings
chicken_size = 50
chicken_x = random.randint(0, WIDTH - chicken_size)
chicken_y = 0
chicken_speed = 3

# Egg settings
egg_size = 20
egg_speed = 5

# Shot settings
shot_size = 10
shot_speed = 8
shots = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Load shooting sound
shoot_sound = pygame.mixer.Sound(r"C:\Users\USER\Downloads\shoot.mp3")

# Create clock object to control the frame rate
clock = pygame.time.Clock()

# Function to handle collisions
def is_collision(obj1, obj2):
    return obj1.colliderect(obj2)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Shoot
    if keys[pygame.K_SPACE]:
        shoot_sound.play()
        shot_x = player_x + player_size // 2 - shot_size // 2
        shot_y = player_y
        shots.append(pygame.Rect(shot_x, shot_y, shot_size, shot_size))

    # Update chicken position
    chicken_y += chicken_speed

    # Check if chicken has reached the bottom
    if chicken_y > HEIGHT:
        chicken_y = 0
        chicken_x = random.randint(0, WIDTH - chicken_size)

    # Generate eggs
    if random.choice([True, False]):
        egg_x = chicken_x
        egg_y = chicken_y
        egg_direction = 1  # Egg moves to the right
    else:
        egg_x = chicken_x + chicken_size - egg_size
        egg_y = chicken_y
        egg_direction = -1  # Egg moves to the left

    # Check for collision with player
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    chicken_rect = pygame.Rect(chicken_x, chicken_y, chicken_size, chicken_size)
    egg_rect = pygame.Rect(egg_x, egg_y, egg_size, egg_size)

    if is_collision(player_rect, egg_rect):
        print("Game Over! Your Score:", score)
        pygame.quit()
        sys.exit()

    # Check if the egg has reached the bottom
    if egg_y > HEIGHT:
        egg_y = chicken_y
        egg_x = chicken_x + chicken_size - egg_size

    # Check for collision with shots
    for shot in shots:
        if is_collision(shot, egg_rect):
            score += 10
            shots.remove(shot)
            chicken_y = 0
            chicken_x = random.randint(0, WIDTH - chicken_size)

    # Update shot positions
    shots = [pygame.Rect(shot.x, shot.y - shot_speed, shot.width, shot.height) for shot in shots]

    # Remove shots that go off-screen
    shots = [shot for shot in shots if shot.y > 0]

    # Clear the screen
    window.fill(WHITE)

    # Draw player (triangle)
    pygame.draw.polygon(window, RED, [(player_x, player_y + player_size),
                                      (player_x + player_size // 2, player_y),
                                      (player_x + player_size, player_y + player_size)])

    # Draw chicken
    pygame.draw.rect(window, WHITE, (chicken_x, chicken_y, chicken_size, chicken_size))

    # Draw eggs
    pygame.draw.rect(window, YELLOW, (egg_x, egg_y, egg_size, egg_size))

    # Draw shots
    for shot in shots:
        pygame.draw.rect(window, RED, shot)

    # Draw score
    score_text = font.render("Score: " + str(score), True, RED)
    window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
