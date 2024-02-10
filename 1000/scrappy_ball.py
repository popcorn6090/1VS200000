import pygame
import cv2
import numpy as np
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
BIRD_SIZE = 50
PIPE_WIDTH = 50
PIPE_HEIGHT = 300
GRAVITY = 0.5
JUMP_HEIGHT = 10

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create the game window
screen = pygame.display.set_mode((800, 600))  # Default size
pygame.display.set_caption("Flappy Bird Clone")

# Load bird video
cap = cv2.VideoCapture(r"C:\Users\USER\Desktop\eg\r.mp4")

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Resize the video frame to match the bird size
resized_bird = cv2.resize(cap.read()[1], (BIRD_SIZE, BIRD_SIZE))

# Release the video capture object
cap.release()

# Convert the image to RGB format
bird_video = cv2.cvtColor(resized_bird, cv2.COLOR_BGR2RGB)

# Convert the video frame to Pygame surface
bird_surface = pygame.surfarray.make_surface(bird_video)

# Initialize bird variables
bird_x = screen.get_width() // 4
bird_y = screen.get_height() // 2
bird_velocity = 0

# Create pipes
pipes = []

def create_pipe():
    gap_y = random.randint(50, screen.get_height() - 150)
    pipe_upper = pygame.Rect(screen.get_width(), 0, PIPE_WIDTH, gap_y)
    pipe_lower = pygame.Rect(screen.get_width(), gap_y + 100, PIPE_WIDTH, screen.get_height() - gap_y - 100)
    return pipe_upper, pipe_lower

# Game state
game_over = False

# Fullscreen flag
fullscreen = False

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                bird_velocity = -JUMP_HEIGHT
            elif game_over and event.key == pygame.K_r:
                # Restart the game
                bird_x = screen.get_width() // 4
                bird_y = screen.get_height() // 2
                bird_velocity = 0
                pipes = []
                game_over = False
            elif event.key == pygame.K_f:
                # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800, 600))

    if not game_over:
        # Update bird position
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Generate pipes
        if len(pipes) == 0 or pipes[-1][0].x < screen.get_width() - 200:
            pipes.append(create_pipe())

        # Update pipes position
        for pipe_pair in pipes:
            for pipe in pipe_pair:
                pipe.x -= 5

        # Remove off-screen pipes
        pipes = [pipe_pair for pipe_pair in pipes if pipe_pair[0].x > -PIPE_WIDTH]

        # Check collision with pipes
        for pipe_pair in pipes:
            if pipe_pair[0].colliderect((bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)) or \
               pipe_pair[1].colliderect((bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)) or \
               bird_y < 0 or bird_y > screen.get_height() - BIRD_SIZE:
                game_over = True

        # Clear the screen
        screen.fill(WHITE)

        # Draw bird
        screen.blit(bird_surface, (bird_x, bird_y))

        # Draw pipes
        for pipe_pair in pipes:
            pygame.draw.rect(screen, BLUE, pipe_pair[0])
            pygame.draw.rect(screen, BLUE, pipe_pair[1])
    else:
        # Game over screen
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over. Press R to restart", True, BLUE)
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)
