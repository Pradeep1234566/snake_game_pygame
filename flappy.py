import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

BIRD_SIZE = 30
bird_x = 80
bird_y = HEIGHT // 2
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3
gravity = 0.5
velocity = 0
FLAP_STRENGTH = -8
pipe_x = WIDTH
pipe_gap_y = 200  # will randomize later
pipe_x -= PIPE_SPEED
# ---------- MAIN LOOP ----------

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = FLAP_STRENGTH

    # Gravity
    velocity += gravity
    bird_y += velocity

    # Screen bounds
    if bird_y < 0:
        bird_y = 0
        velocity = 0

    if bird_y > HEIGHT - BIRD_SIZE:
        bird_y = HEIGHT - BIRD_SIZE
        velocity = 0

    # Draw
    screen.fill((135, 206, 235))

    pygame.draw.rect(
        screen,
        (255, 255, 0),
        (bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)
    )

    pygame.display.flip()
