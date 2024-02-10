import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600  # You can change the initial window size here
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("2-Player Race Game")

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Player 1 (Arrow keys)
player1_x = width // 4
player1_y = height // 2
player1_speed = 5

# Player 2 (WASD keys)
player2_x = width * 3 // 4
player2_y = height // 2
player2_speed = 5

# Obstacles
obstacle_width = 20
obstacle_height = 20
obstacle_speed = 5
obstacle_frequency = 25
obstacles = []

# Score
score_player1 = 0
score_player2 = 0
font = pygame.font.SysFont(None, 36)

# Game state
game_over = False
winner = None

# Game loop
clock = pygame.time.Clock()

def reset_game():
    global game_over, winner, obstacles, score_player1, score_player2
    game_over = False
    winner = None
    obstacles = []
    score_player1 = 0
    score_player2 = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    if not game_over:
        # Move players
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player1_y > player1_speed:
            player1_y -= player1_speed
        if keys[pygame.K_DOWN] and player1_y < height - 50:
            player1_y += player1_speed
        if keys[pygame.K_LEFT] and player1_x > player1_speed:
            player1_x -= player1_speed
        if keys[pygame.K_RIGHT] and player1_x < width // 2 - 50:
            player1_x += player1_speed

        if keys[pygame.K_w] and player2_y > player2_speed:
            player2_y -= player2_speed
        if keys[pygame.K_s] and player2_y < height - 50:
            player2_y += player2_speed
        if keys[pygame.K_a] and player2_x > width // 2:
            player2_x -= player2_speed
        if keys[pygame.K_d] and player2_x < width - 50:
            player2_x += player2_speed

        # Move obstacles
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            if obstacle[1] > height:  # Reset obstacle when it goes beyond the screen
                obstacle[1] = -obstacle_height
                obstacle[0] = random.randint(0, width - obstacle_width)

        # Spawn obstacles
        if random.randint(1, obstacle_frequency) == 1:
            spawn_direction = random.choice(["top", "left", "right"])
            if spawn_direction == "top":
                obstacles.append([random.randint(0, width - obstacle_width), -obstacle_height])
            elif spawn_direction == "left":
                obstacles.append([-obstacle_width, random.randint(0, height - obstacle_height)])
            elif spawn_direction == "right":
                obstacles.append([width, random.randint(0, height - obstacle_height)])

        # Check for collisions
        player1_rect = pygame.Rect(player1_x, player1_y, 20, 20)
        player2_rect = pygame.Rect(player2_x - 20, player2_y, 20, 20)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
            if player1_rect.colliderect(obstacle_rect):
                game_over = True
                winner = "Player 2"
            elif player2_rect.colliderect(obstacle_rect):
                game_over = True
                winner = "Player 1"

    # Draw everything
    screen.fill(white)

    pygame.draw.rect(screen, green, [player1_x, player1_y, 20, 20])
    pygame.draw.rect(screen, blue, [player2_x - 20, player2_y, 20, 20])

    for obstacle in obstacles:
        pygame.draw.rect(screen, red, [obstacle[0], obstacle[1], obstacle_width, obstacle_height])

    score_text = font.render(f"Player 1: {score_player1} | Player 2: {score_player2}", True, red)
    screen.blit(score_text, (width // 2 - 150, 10))

    if game_over:
        winner_text = font.render(f"Game Over! {winner} wins!", True, red)
        screen.blit(winner_text, (width // 2 - 120, height // 2 - 30))
        reset_text = font.render("Press 'R' to play again", True, yellow)
        screen.blit(reset_text, (width // 2 - 120, height // 2 + 10))

    pygame.display.flip()

    # Check for reset input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and game_over:
        reset_game()

    # Set the frame rate
    clock.tick(30)
