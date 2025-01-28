import pygame
import random

# Inicializar Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Dinossauro")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)

# Configurações do dinossauro
dino_width, dino_height = 50, 50
dino_x = 100
dino_y = HEIGHT - dino_height - 10
dino_speed = 0
jump_force = 15
gravity = 1
is_jumping = False
sprite_timer = 0  # Temporizador para animação das pernas

# Configurações dos obstáculos
obstacle_width, obstacle_height = 20, 40
obstacle_speed = 7
obstacles = [pygame.Rect(WIDTH, HEIGHT - obstacle_height - 10, obstacle_width, obstacle_height)]
min_obstacle_spacing = 300  # Distância mínima entre os obstáculos
max_obstacle_spacing = 600  # Distância máxima para gerar aleatoriamente

# Configurações do jogo
score = 0
font = pygame.font.Font(None, 36)
game_over = False

# Função para desenhar o boneco correndo
def draw_dino(x, y, frame):
    """
    Desenha um boneco simples correndo no estilo stickman.
    O movimento das pernas alterna com base no 'frame'.
    """
    # Corpo
    pygame.draw.circle(screen, BLACK, (x + 25, y + 10), 10)  # Cabeça
    pygame.draw.line(screen, BLACK, (x + 25, y + 20), (x + 25, y + 40), 5)  # Tronco
    
    # Braços
    pygame.draw.line(screen, BLACK, (x + 25, y + 25), (x + 15, y + 35), 3)  # Braço esquerdo
    pygame.draw.line(screen, BLACK, (x + 25, y + 25), (x + 35, y + 35), 3)  # Braço direito
    
    # Pernas (alternam conforme o frame)
    if frame % 20 < 10:
        pygame.draw.line(screen, BLACK, (x + 25, y + 40), (x + 15, y + 50), 3)  # Perna esquerda
        pygame.draw.line(screen, BLACK, (x + 25, y + 40), (x + 35, y + 50), 3)  # Perna direita
    else:
        pygame.draw.line(screen, BLACK, (x + 25, y + 40), (x + 35, y + 50), 3)  # Perna esquerda
        pygame.draw.line(screen, BLACK, (x + 25, y + 40), (x + 15, y + 50), 3)  # Perna direita

# Função para desenhar texto
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Função principal do jogo
def game():
    global dino_y, dino_speed, is_jumping, score, game_over, obstacle_speed, sprite_timer

    running = True

    while running:
        screen.fill(WHITE)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimento do dinossauro
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping and not game_over:
            dino_speed = -jump_force
            is_jumping = True

        # Física do dinossauro
        dino_y += dino_speed
        dino_speed += gravity

        # Evitar que o dinossauro caia abaixo do chão
        if dino_y > HEIGHT - dino_height - 10:
            dino_y = HEIGHT - dino_height - 10
            is_jumping = False

        # Atualizar obstáculos
        if not game_over:
            for obstacle in obstacles:
                obstacle.x -= obstacle_speed

            # Adicionar novos obstáculos com espaçamento aleatório (dentro do limite)
            if obstacles[-1].x < WIDTH - random.randint(min_obstacle_spacing, max_obstacle_spacing):
                new_obstacle = pygame.Rect(
                    WIDTH, HEIGHT - obstacle_height - 10, obstacle_width, obstacle_height
                )
                obstacles.append(new_obstacle)

            # Remover obstáculos fora da tela
            if obstacles[0].x < -obstacle_width:
                obstacles.pop(0)

            # Verificar colisões
            dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
            for obstacle in obstacles:
                if dino_rect.colliderect(obstacle):
                    game_over = True

            # Aumentar pontuação
            score += 1

            # Aumentar a velocidade dos obstáculos a cada 20 pontos
            if score % 200 == 0 and score > 0:
                obstacle_speed += obstacle_speed * 0.1

        # Atualizar animação do boneco
        sprite_timer += 1

        # Desenhar chão
        pygame.draw.line(screen, GRAY, (0, HEIGHT - 10), (WIDTH, HEIGHT - 10), 2)

        # Desenhar dinossauro (boneco correndo)
        draw_dino(dino_x, dino_y, sprite_timer)

        # Desenhar obstáculos
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle)

        # Exibir pontuação
        draw_text(f"Pontuação: {score // 10}", 36, BLACK, 10, 10)

        # Game Over
        if game_over:
            draw_text("GAME OVER", 72, RED, WIDTH // 2 - 150, HEIGHT // 2 - 50)
            draw_text("Pressione R para reiniciar", 36, BLACK, WIDTH // 2 - 150, HEIGHT // 2 + 20)
            if keys[pygame.K_r]:
                # Reiniciar o jogo
                reset_game()

        # Atualizar tela
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Função para reiniciar o jogo
def reset_game():
    global dino_y, dino_speed, is_jumping, score, obstacles, game_over, obstacle_speed
    dino_y = HEIGHT - dino_height - 10
    dino_speed = 0
    is_jumping = False
    score = 0
    obstacles = [pygame.Rect(WIDTH, HEIGHT - obstacle_height - 10, obstacle_width, obstacle_height)]
    game_over = False
    obstacle_speed = 7  # Resetar a velocidade inicial

# Iniciar o jogo
game()
