import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
BRICK_ROWS, BRICK_COLUMNS = 5, 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Paddle
paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [5, -5]

# Bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Point System
points = 0

def reset_game():
    global paddle, ball, bricks, points, ball_speed
    paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_speed = [5, -5]
    
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick)
    
    global points
    points = 0

def draw_objects():
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.circle(screen, RED, ball.center, BALL_RADIUS)
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, brick)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Points: {points}", True, WHITE)
    screen.blit(score_text, (10, 10))

def show_game_over():
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Your score: {points}", True, WHITE)
    restart_text = font.render("Press 'R' to restart", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
    screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 150))

def main():
    reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

        keys = pygame.key.get_pressed()
        paddle.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 8

        
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        
        if ball.colliderect(paddle) and ball_speed[1] > 0:
            ball_speed[1] = -ball_speed[1]

        
        for brick in bricks:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove(brick)
                global points
                points += 1
                break

       
        if ball.top >= HEIGHT:
            show_game_over()
            pygame.display.flip()

            restart_pressed = False
            while not restart_pressed:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                            restart_pressed = True

        
        screen.fill((0, 0, 0))
        draw_objects()
        pygame.display.flip()

        
        clock.tick(60)

if __name__ == "__main__":
    main()
