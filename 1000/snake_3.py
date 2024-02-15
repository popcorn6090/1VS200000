import pygame
import time
import random

pygame.init()


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)


width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')


snake_block = 10
snake_speed = 15


font = pygame.font.SysFont(None, 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_display, white, [x[0], x[1], snake_block, snake_block])

def Your_score(score):
    value = font.render("Your Score: " + str(score), True, white)
    game_display.blit(value, [0, 0])

def message(msg, color):
    mesg = font.render(msg, True, color)
    game_display.blit(mesg, [width / 6, height / 3])

def game_loop():
    game_over = False
    game_close = False
    game_pause = False

    
    x1, y1 = width / 2, height / 2

    
    x1_change, y1_change = 0, 0

    
    snake_length = 1

   
    foodx, foody = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    
    score = 0

    snake_list = []

    while not game_over:

        while game_close:
            game_display.fill(black)
            message("You lost! Press Q-Quit or C-Play Again", red)
            Your_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    game_pause = not game_pause

        if game_pause:
            continue

        
        x1 += x1_change
        y1 += y1_change

        
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

       
        if x1 == foodx and y1 == foody:
            foodx, foody = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            snake_length += 1
            score += 10

        game_display.fill(black)
        pygame.draw.rect(game_display, red, [foodx, foody, snake_block, snake_block])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)
        Your_score(score)

        pygame.display.update()

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
