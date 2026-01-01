import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# -------- BIRD --------
BIRD_SIZE = 30
bird_x = 80
bird_y = HEIGHT // 2

gravity = 0.5
velocity = 0
FLAP_STRENGTH = -8

# -------- PIPES --------
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3

pipe_x = WIDTH
pipe_gap_y = random.randint(150, HEIGHT - 150)

game_over = False

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                velocity = FLAP_STRENGTH

            if game_over and event.key == pygame.K_r:
                bird_y = HEIGHT // 2
                velocity = 0
                pipe_x = WIDTH
                pipe_gap_y = random.randint(150, HEIGHT - 150)
                game_over = False

    if not game_over:
        # -------- BIRD PHYSICS --------
        velocity += gravity
        bird_y += velocity

        # -------- PIPE MOVE --------
        pipe_x -= PIPE_SPEED
        if pipe_x < -PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_gap_y = random.randint(150, HEIGHT - 150)

        # -------- COLLISION --------
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)

        top_pipe_rect = pygame.Rect(
            pipe_x, 0, PIPE_WIDTH, pipe_gap_y
        )

        bottom_pipe_rect = pygame.Rect(
            pipe_x,
            pipe_gap_y + PIPE_GAP,
            PIPE_WIDTH,
            HEIGHT - (pipe_gap_y + PIPE_GAP)
        )

        if (bird_rect.colliderect(top_pipe_rect) or
            bird_rect.colliderect(bottom_pipe_rect) or
            bird_y >= HEIGHT - BIRD_SIZE):
            game_over = True

    # -------- DRAW --------
    screen.fill((135, 206, 235))

    pygame.draw.rect(
        screen,
        (255, 255, 0),
        (bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)
    )

    pygame.draw.rect(
        screen,
        (0, 200, 0),
        (pipe_x, 0, PIPE_WIDTH, pipe_gap_y)
    )

    pygame.draw.rect(
        screen,
        (0, 200, 0),
        (pipe_x,
         pipe_gap_y + PIPE_GAP,
         PIPE_WIDTH,
         HEIGHT - (pipe_gap_y + PIPE_GAP))
    )

    if game_over:
        over_text = font.render("GAME OVER", True, (255, 80, 80))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))

        screen.blit(
            over_text,
            (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 40)
        )
        screen.blit(
            restart_text,
            (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10)
        )

    pygame.display.flip()
