import pygame
import sys
import random


pygame.init()

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

snake = [(100, 100), (80, 100), (60, 100)] # Initial snake segments
direction = (CELL_SIZE, 0)
food = (
    random.randrange(0, WIDTH, CELL_SIZE),
    random.randrange(0, HEIGHT, CELL_SIZE)
)


while True:
    clock.tick(10) # helps to control the frame rate

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE): # Prevent reversing direction
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    # -------- UPDATE --------
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    snake.insert(0, new_head)
    if new_head == food:
        food = (
            random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE)
        )
    else:
        snake.pop()

    # -------- DRAW --------
    screen.fill((30, 30, 30)) # 

    for block in snake:
        pygame.draw.rect(
            screen,
            (0, 200, 0),
            (block[0], block[1], CELL_SIZE, CELL_SIZE)
        )

    pygame.draw.rect(
    screen,
    (200, 0, 0),
    (food[0], food[1], CELL_SIZE, CELL_SIZE)
)

    pygame.display.flip()
    
