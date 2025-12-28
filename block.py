import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Apples")

clock = pygame.time.Clock()

# ---------- AUDIO ----------
pygame.mixer.music.load("bg.mp3")
pygame.mixer.music.set_volume(0.4)

miss_sound = pygame.mixer.Sound("miss.mp3")
miss_sound.set_volume(0.7)

# ---------- CONSTANTS ----------
PLAYER_SIZE = 40
player_y = HEIGHT - 60
player_speed = 10

ENEMY_SIZE = 40
MAX_ENEMY_SPEED = 15

# ---------- GAME STATE ----------
in_menu = True

def reset_game():
    return {
        "score": 0,
        "misses": 0,
        "player_x": WIDTH // 2 - PLAYER_SIZE // 2,
        "enemy_x": random.randint(0, WIDTH - ENEMY_SIZE),
        "enemy_y": -ENEMY_SIZE,
        "enemy_speed": 5,
        "last_speed_increase_score": 0,
        "game_over": False
    }

state = reset_game()

# Start menu music
pygame.mixer.music.play(-1)

# ---------- MAIN LOOP ----------
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # ----- MENU INPUT -----
            if in_menu and event.key == pygame.K_RETURN:
                in_menu = False
                pygame.mixer.music.stop()
                state = reset_game()

            # ----- GAME OVER INPUT -----
            elif not in_menu and state["game_over"]:
                if event.key == pygame.K_r:
                    in_menu = True
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    # ---------- MENU SCENE ----------
    if in_menu:
        screen.fill((30, 30, 30))

        title = big_font.render("CATCH THE APPLES", True, (0, 255, 0))
        start_text = font.render("Press ENTER to Start", True, (200, 200, 200))

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50)
        )
        screen.blit(
            start_text,
            (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 10)
        )

        pygame.display.flip()
        continue

    # ---------- GAMEPLAY ----------
    if not state["game_over"]:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            state["player_x"] -= player_speed
        if keys[pygame.K_RIGHT]:
            state["player_x"] += player_speed

        state["player_x"] = max(
            0, min(state["player_x"], WIDTH - PLAYER_SIZE)
        )

        # Enemy movement
        state["enemy_y"] += state["enemy_speed"]

        if state["enemy_y"] > HEIGHT:
            state["misses"] += 1
            miss_sound.play()
            state["enemy_y"] = -ENEMY_SIZE
            state["enemy_x"] = random.randint(0, WIDTH - ENEMY_SIZE)

        # Collision
        player_rect = pygame.Rect(
            state["player_x"], player_y, PLAYER_SIZE, PLAYER_SIZE
        )
        enemy_rect = pygame.Rect(
            state["enemy_x"], state["enemy_y"], ENEMY_SIZE, ENEMY_SIZE
        )

        if player_rect.colliderect(enemy_rect):
            state["score"] += 1
            state["enemy_y"] = -ENEMY_SIZE
            state["enemy_x"] = random.randint(0, WIDTH - ENEMY_SIZE)

        # Difficulty scaling
        if state["score"] - state["last_speed_increase_score"] >= 5:
            state["enemy_speed"] = min(
                state["enemy_speed"] + 1, MAX_ENEMY_SPEED
            )
            state["last_speed_increase_score"] = state["score"]

        # Game over condition
        if state["misses"] >= 3:
            state["game_over"] = True

    # ---------- DRAW ----------
    screen.fill((30, 30, 30))

    pygame.draw.rect(
        screen,
        (0, 200, 255),
        (state["player_x"], player_y, PLAYER_SIZE, PLAYER_SIZE)
    )

    pygame.draw.rect(
        screen,
        (255, 60, 60),
        (state["enemy_x"], state["enemy_y"], ENEMY_SIZE, ENEMY_SIZE)
    )

    score_text = font.render(
        f"Score: {state['score']}", True, (255, 255, 255)
    )
    miss_text = font.render(
        f"Misses: {state['misses']}/3", True, (255, 180, 180)
    )

    screen.blit(score_text, (10, 10))
    screen.blit(miss_text, (10, 40))

    if state["game_over"]:
        over_text = big_font.render("GAME OVER", True, (255, 80, 80))
        restart_text = font.render(
            "Press R to Restart | Q to Quit", True, (200, 200, 200)
        )

        screen.blit(
            over_text,
            (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 40)
        )
        screen.blit(
            restart_text,
            (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20)
        )

    pygame.display.flip()
