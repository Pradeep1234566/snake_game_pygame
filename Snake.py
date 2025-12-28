import pygame
import sys
import random

pygame.init()
font = pygame.font.SysFont(None, 36)

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
speed = 10
game_over = False   

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)
food = (
    random.randrange(0, WIDTH, CELL_SIZE),
    random.randrange(0, HEIGHT, CELL_SIZE)
)
score = 0

while True:
    clock.tick(speed)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

    # -------- UPDATE --------
    if not game_over:
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Wall collision
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            game_over = True

        # Self collision
        elif new_head in snake:
            game_over = True

        else:
            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                speed += 1
                food = (
                    random.randrange(0, WIDTH, CELL_SIZE),
                    random.randrange(0, HEIGHT, CELL_SIZE)
                )
            else:
                snake.pop()

    # -------- DRAW --------
    screen.fill((30, 30, 30))

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

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = font.render(
            "Game Over! Press R to Restart | Q to Quit",
            True,
            (255, 0, 0)
        )
        screen.blit(
            over_text,
            (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2)
        )

    pygame.display.flip()

    # -------- WAIT FOR RESTART --------
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    snake = [(100, 100), (80, 100), (60, 100)]
                    direction = (CELL_SIZE, 0)
                    food = (
                        random.randrange(0, WIDTH, CELL_SIZE),
                        random.randrange(0, HEIGHT, CELL_SIZE)
                    )
                    score = 0
                    speed = 10
                    game_over = False
