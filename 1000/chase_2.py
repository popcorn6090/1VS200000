import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 30
PLAYER_SIZE = 30
ENEMY_SIZE = 30
POTION_SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (169, 169, 169)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()

# Set up window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft-like Game")

# Set up clock
clock = pygame.time.Clock()

# Set up player
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
original_speed = player_speed

# Set up enemies
enemy_x, enemy_y = random.randint(0, WIDTH - ENEMY_SIZE), random.randint(0, HEIGHT - ENEMY_SIZE)
enemy_speed = 3

enemy2_x, enemy2_y = random.randint(0, WIDTH - ENEMY_SIZE), random.randint(0, HEIGHT - ENEMY_SIZE)
enemy2_speed = 2  # Different speed for the second enemy

# Set up bricks
bricks = [(100, 100), (300, 200), (500, 400)]  # Bricks at specific positions

# Set up potion
potion_x, potion_y = random.randint(0, WIDTH - POTION_SIZE), random.randint(0, HEIGHT - POTION_SIZE)
potion_active = True

# Set up sounds
pygame.mixer.init()
collision_sound = pygame.mixer.Sound(r"C:\Users\USER\Desktop\Music\01. shut up.mp3"
)  # Replace with actual path
pickup_sound = pygame.mixer.Sound(r"C:\Users\USER\Desktop\Music\06. six thirty.mp3"
)  # Replace with actual path
background_music = pygame.mixer.Sound(r"C:\Users\USER\Desktop\Music\05. off the table.mp3")  # Replace with actual path

# Set up game variables
score = 0
spawn_potion_timer = 0
spawn_potion_interval = 30 * 1000  # 30 seconds in milliseconds
running = True
game_over = False
paused = False

# Start background music
background_music.play(-1)  # -1 means loop indefinitely

while running:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused  # Toggle pause state when 'P' key is pressed

    if not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            if all(player_x - player_speed != brick[0] or player_y != brick[1] for brick in bricks):
                player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
            if all(player_x + player_speed != brick[0] - BLOCK_SIZE or player_y != brick[1] for brick in bricks):
                player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            if all(player_x != brick[0] or player_y - player_speed != brick[1] for brick in bricks):
                player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - PLAYER_SIZE:
            if all(player_x != brick[0] or player_y + player_speed != brick[1] - BLOCK_SIZE for brick in bricks):
                player_y += player_speed

        # Draw bricks
        for brick in bricks:
            pygame.draw.rect(win, GREY, (brick[0], brick[1], BLOCK_SIZE, BLOCK_SIZE))

        # Draw player
        pygame.draw.rect(win, RED, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

        # Draw enemies (blue rectangles)
        pygame.draw.rect(win, BLUE, (enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE))
        pygame.draw.rect(win, BLUE, (enemy2_x, enemy2_y, ENEMY_SIZE, ENEMY_SIZE))

        # Spawn potion every 30 seconds
        spawn_potion_timer += clock.get_rawtime()
        if spawn_potion_timer >= spawn_potion_interval:
            potion_x, potion_y = random.randint(0, WIDTH - POTION_SIZE), random.randint(0, HEIGHT - POTION_SIZE)
            potion_active = True
            spawn_potion_timer = 0

        # Draw potion if active
        if potion_active:
            pygame.draw.rect(win, GREEN, (potion_x, potion_y, POTION_SIZE, POTION_SIZE))

        # Enemy chasing player
        if not game_over:
            if player_x < enemy_x:
                enemy_x -= enemy_speed
            elif player_x > enemy_x:
                enemy_x += enemy_speed
            if player_y < enemy_y:
                enemy_y -= enemy_speed
            elif player_y > enemy_y:
                enemy_y += enemy_speed

            if player_x < enemy2_x:
                enemy2_x -= enemy2_speed
            elif player_x > enemy2_x:
                enemy2_x += enemy2_speed
            if player_y < enemy2_y:
                enemy2_y -= enemy2_speed
            elif player_y > enemy2_y:
                enemy2_y += enemy2_speed

        # Collision detection with enemies
        if (player_x < enemy_x + ENEMY_SIZE and player_x + PLAYER_SIZE > enemy_x and
                player_y < enemy_y + ENEMY_SIZE and player_y + PLAYER_SIZE > enemy_y):
            game_over = True
            collision_sound.play()  # Play collision sound
            background_music.stop()  # Stop background music

        if (player_x < enemy2_x + ENEMY_SIZE and player_x + PLAYER_SIZE > enemy2_x and
                player_y < enemy2_y + ENEMY_SIZE and player_y + PLAYER_SIZE > enemy2_y):
            game_over = True
            collision_sound.play()  # Play collision sound
            background_music.stop()  # Stop background music

        # Collision detection with potion
        if (player_x < potion_x + POTION_SIZE and player_x + PLAYER_SIZE > potion_x and
                player_y < potion_y + POTION_SIZE and player_y + PLAYER_SIZE > potion_y):
            potion_active = False
            player_speed = 8  # Increase player speed after picking up potion
            background_music.stop()
            pickup_sound.play()  # Play pickup sound
            pickup_sound.stop()
            background_music.play()
            

        # Check if player escapes the enemies, increment score
        if not game_over and all(player_x != brick[0] or player_y != brick[1] for brick in bricks):
            score += 10

        # Display score
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Score: {score}", True, WHITE)
        win.blit(text, (10, 10))

        if game_over:
            font = pygame.font.SysFont(None, 40)
            text = font.render("Game Over! Press R to restart", True, WHITE)
            win.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_over = False
                score = 0  # Resetting score
                player_speed = original_speed  # Resetting player speed
                player_x, player_y = WIDTH // 2, HEIGHT // 2
                enemy_x, enemy_y = random.randint(0, WIDTH - ENEMY_SIZE), random.randint(0, HEIGHT - ENEMY_SIZE)
                enemy2_x, enemy2_y = random.randint(0, WIDTH - ENEMY_SIZE), random.randint(0, HEIGHT - ENEMY_SIZE)
                spawn_potion_timer = 0  # Resetting potion timer
                potion_active = False
                
                background_music.play(-1)  # Restart background music
                collision_sound.stop()
                pickup_sound.stop()

    # Display pause text
    if paused:
        font = pygame.font.SysFont(None, 40)
        text = font.render("Paused", True, WHITE)
        win.blit(text, (WIDTH // 2 - 70, HEIGHT // 2 - 20))
        background_music.stop()
        collision_sound.stop()
        pickup_sound.stop()

    pygame.display.update()
    clock.tick(60)

# Stop background music when exiting
background_music.stop()

pygame.quit()
