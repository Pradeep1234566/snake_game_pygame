import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Pygame")

clock = pygame.time.Clock()
running = True

x, y = 100, 200
speed = 5
size = 40

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: x -= speed
    if keys[pygame.K_d]: x += speed
    if keys[pygame.K_w]: y -= speed
    if keys[pygame.K_s]: y += speed

    x = max(0, min(x, WIDTH - size))
    y = max(0, min(y, HEIGHT - size))

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (0, 200, 255), (x, y, size, size))
    pygame.display.flip()

pygame.quit()
