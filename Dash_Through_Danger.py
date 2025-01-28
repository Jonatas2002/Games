import pygame
import random

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Road Rush")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Configurações do jogador
player_width, player_height = 50, 100
player_speed = 5

# Configurações dos obstáculos e bônus
obstacle_width, obstacle_height = 50, 100
bonus_width, bonus_height = 40, 40
base_obstacle_speed = 5
base_bonus_speed = 5

# Função para mostrar texto na tela
def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.Font(None, size)
    render = font.render(text, True, color)
    text_rect = render.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(render, text_rect)

# Função principal do jogo
def game():
    # Inicializar variáveis do jogo
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 20
    obstacles = [
        pygame.Rect(random.randint(0, WIDTH - obstacle_width), random.randint(-600, -100), obstacle_width, obstacle_height)
        for _ in range(3)
    ]
    bonuses = [
        pygame.Rect(random.randint(0, WIDTH - bonus_width), random.randint(-600, -100), bonus_width, bonus_height)
        for _ in range(2)
    ]
    score = 0
    lives = 3
    obstacle_speed = base_obstacle_speed
    bonus_speed = base_bonus_speed
    game_over = False
    paused = False

    # Loop principal
    while True:
        screen.fill(WHITE)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause
                    paused = not paused

                if paused and event.key == pygame.K_RETURN:  # Retomar no pause
                    paused = False

                if paused and event.key == pygame.K_q:  # Sair no pause
                    return "exit"

                if game_over and event.key == pygame.K_RETURN:  # Jogar novamente
                    return "restart"

                if game_over and event.key == pygame.K_q:  # Sair após perder
                    return "exit"

        # Controle de pausa
        if paused:
            draw_text("PAUSE", 60, BLACK, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("Pressione ENTER para continuar", 30, GRAY, WIDTH // 2, HEIGHT // 2)
            draw_text("Pressione Q para sair", 30, GRAY, WIDTH // 2, HEIGHT // 2 + 40)
            pygame.display.flip()
            clock.tick(30)
            continue

        # Controle de game over
        if game_over:
            draw_text("FIM DE JOGO", 60, BLACK, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text(f"Pontuação: {score}", 40, GRAY, WIDTH // 2, HEIGHT // 2)
            draw_text("Pressione ENTER para jogar novamente", 30, GRAY, WIDTH // 2, HEIGHT // 2 + 50)
            draw_text("Pressione Q para sair", 30, GRAY, WIDTH // 2, HEIGHT // 2 + 90)
            pygame.display.flip()
            clock.tick(30)
            continue

        # Movimentação do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Atualizar obstáculos e bônus
        for obstacle in obstacles:
            obstacle.y += obstacle_speed
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)
                obstacles.append(pygame.Rect(random.randint(0, WIDTH - obstacle_width), -obstacle_height, obstacle_width, obstacle_height))
                score += 1

        for bonus in bonuses:
            bonus.y += bonus_speed
            if bonus.y > HEIGHT:
                bonuses.remove(bonus)
                bonuses.append(pygame.Rect(random.randint(0, WIDTH - bonus_width), -bonus_height, bonus_width, bonus_height))

        # Verificar colisões
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                obstacles.remove(obstacle)
                obstacles.append(pygame.Rect(random.randint(0, WIDTH - obstacle_width), -obstacle_height, obstacle_width, obstacle_height))
                lives -= 1

        for bonus in bonuses:
            if player_rect.colliderect(bonus):
                bonuses.remove(bonus)
                bonuses.append(pygame.Rect(random.randint(0, WIDTH - bonus_width), -bonus_height, bonus_width, bonus_height))
                lives += 1

        # Acelerar jogo a cada 10 pontos
        if score > 0 and score % 10 == 0:
            obstacle_speed = base_obstacle_speed * (1 + 0.2 * (score // 10))
            bonus_speed = base_bonus_speed * (1 + 0.2 * (score // 10))

        # Verificar fim de jogo
        if lives <= 0:
            game_over = True

        # Desenhar jogador
        pygame.draw.rect(screen, BLUE, player_rect)

        # Desenhar obstáculos
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle)

        # Desenhar bônus
        for bonus in bonuses:
            pygame.draw.rect(screen, GREEN, bonus)

        # Mostrar pontuação e vidas
        draw_text(f"Pontuação: {score}", 30, BLACK, 10, 10, center=False)
        draw_text(f"Vidas: {lives}", 30, BLACK, 10, 40, center=False)

        # Atualizar tela
        pygame.display.flip()
        clock.tick(60)

# Loop principal do aplicativo
while True:
    result = game()
    if result == "exit":
        break
