import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Interface")

# Load background image
background_image = pygame.image.load("background.jpg")  # Replace "background.jpg" with your image file
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.Font(None, 36)

# Game names and scripts
games = {
    1: {"name": "Snake 2.0", "script": "snake_3.py"},
    2: {"name": "Catch Me if you Can", "script": "chase_2.py"},
    3: {"name": "Chicken Invaders", "script": "chick_invade.py"},
    4: {"name": "Hell Stones", "script": "race_2.py"},
    5: {"name": "Scrappy Bird", "script": "scrappy_ball.py"},
     6: {"name": "Break Bricks", "script": "break_bricks.py"},
}

# Selected game number
selected_game = None

# Calculate the vertical starting point for game buttons
game_button_height = 50
game_button_padding = 10
game_buttons_start_y = (HEIGHT - len(games) * (game_button_height + game_button_padding)) // 2

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                game_number = int(chr(event.key))
                if game_number in games:
                    selected_game = game_number
                    game_script = games[game_number]["script"]
                    try:
                        subprocess.run(["python", game_script], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Error running {game_script}: {e}")
                        pygame.quit()
                        sys.exit()

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Display game buttons with rounded edges
    for i, (number, game_info) in enumerate(games.items()):
        button_rect = pygame.Rect(10, game_buttons_start_y + i * (game_button_height + game_button_padding),
                                  WIDTH - 20, game_button_height)
        pygame.draw.rect(screen, GRAY, button_rect, border_radius=10)
        text = font.render(f"{number}. {game_info['name']}", True, BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    # Display selected game
    if selected_game:
        text = font.render(f"Selected Game: {games[selected_game]['name']}", True, WHITE)
        screen.blit(text, (10, 220))

    text = font.render("Press 1-6 to play a game (ESC to quit)", True, WHITE)
    screen.blit(text, (250, 50))
    text = font.render("Fun Awaits You", True, WHITE)
    screen.blit(text, (320, 70))
    text = font.render("I recommend everything, and oh they are very addictive", True, WHITE)
    screen.blit(text, (200, 90))

    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
