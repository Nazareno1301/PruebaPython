import pygame
import sys
import random

pygame.init()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

COLOR_NAMES = {
    WHITE: "Blanco",
    GREEN: "Verde",
    BLUE: "Azul"
}

# Pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mi Juego Pygame")

# Jugador
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
player_speed = 5
player_color = WHITE

# Enemigos
enemy_size = 30
enemy_speed = 3
enemies = []

# Vidas
lives = 3

# Fuente
font = pygame.font.Font(None, 36)

# seleccionar personaje
def select_character():
    global player_color

    colors = [WHITE, GREEN, BLUE]  
    selected_index = 0

    selection_menu = True

    while selection_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for i, _ in enumerate(colors):
                    rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + i * 40 - 50, 100, 40)
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected_index = i
                        player_color = colors[selected_index]
                        selection_menu = False
                        game(player_color)

        screen.fill(BLACK)

        # opciones de selección de personaje
        color_options_text = [font.render(COLOR_NAMES[colors[i]], True, colors[i]) for i in range(len(colors))]
        for i, text in enumerate(color_options_text):
            rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + i * 40 - 50, 100, 40)
            pygame.draw.rect(screen, RED if i == selected_index else BLACK, rect, 2)
            screen.blit(text, rect)

        pygame.display.flip()

# colisiones con enemigos
def handle_collisions():
    global player_x, player_y, player_size, enemies, lives

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            lives -= 1
            print(f"Perdiste una vida. Vidas restantes: {lives}")
            enemies.remove(enemy)

# Función principal
def game(selected_color):
    global player_x, player_y, enemies, enemy_speed, lives, player_color

    # Color del jugador
    player_color = selected_color

    clock = pygame.time.Clock()

    while True:
        if lives <= 0:
            game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        handle_input(keys)

        screen.fill(BLACK)

        draw_player()

        move_and_draw_enemies()

        handle_collisions()

        create_new_enemies()

        draw_lives_panel()

        pygame.display.flip()
        clock.tick(60)

# Game Over
def game_over():
    global lives

    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    lives_text = font.render(f"Vidas restantes: {lives}", True, WHITE)
    retry_text = font.render("Presiona Enter para volver al menú", True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    lives_rect = lives_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(lives_text, lives_rect)
    screen.blit(retry_text, retry_rect)

    pygame.display.flip()

    wait_for_enter()

    lives = 3
    main_menu()

# Enter
def wait_for_enter():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# nuevo enemigo
def create_enemy():
    global WIDTH, enemy_size, enemies

    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = 0
    enemies.append([enemy_x, enemy_y])

# menú
def main_menu():
    global player_color
    player_color = WHITE
    while True:
        option, selected_color = show_menu()

        if option == "start":
            game(player_color)
        elif option == "select_character":
            player_color = selected_color

# mostrar el menú
def show_menu():
    global start_rect, select_character_rect
    menu = True
    selected_option = None
    selected_color = None

    start_rect = None
    select_character_rect = None

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if start_rect.collidepoint(mouse_x, mouse_y):
                    selected_option = "start"
                    menu = False
                elif select_character_rect.collidepoint(mouse_x, mouse_y):
                    selected_option = "select_character"
                    selected_color = select_character()
                    menu = False

        screen.fill(BLACK)

        # opciones del menú
        start_text = font.render("Iniciar Juego", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))

        pygame.draw.rect(screen, RED, start_rect, 2)
        screen.blit(start_text, start_rect)

        # opción de selección de personaje
        select_character_text = font.render("Seleccionar Personaje", True, WHITE)
        select_character_rect = select_character_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

        pygame.draw.rect(screen, RED, select_character_rect, 2)
        screen.blit(select_character_text, select_character_rect)

        pygame.display.flip()

    return selected_option, selected_color

# entrada del jugador
def handle_input(keys):
    global player_x, player_speed, WIDTH, player_size
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

# Dibujar al jugador
def draw_player():
    global screen, player_x, player_y, player_size, player_color
    pygame.draw.rect(screen, player_color, [player_x, player_y, player_size, player_size])

# mover y dibujar enemigos
def move_and_draw_enemies():
    global enemies, enemy_speed, screen, enemy_size, WHITE
    for enemy in enemies:
        enemy[1] += enemy_speed
        pygame.draw.rect(screen, WHITE, [enemy[0], enemy[1], enemy_size, enemy_size])

# crear nuevos enemigos
def create_new_enemies():
    global enemies, WIDTH, enemy_size
    if random.randint(0, 100) < 5:
        create_enemy()

# panel de vidas
def draw_lives_panel():
    global screen, font, WHITE, lives
    lives_text = font.render(f"Vidas: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))

if __name__ == "__main__":
    main_menu()
