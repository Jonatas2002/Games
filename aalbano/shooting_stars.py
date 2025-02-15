import pygame
import math
import random

# Configurações iniciais
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
PLAYER_COLOR = (0, 255, 0)
BULLET_COLOR = (255, 255, 255)
MONSTER_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
RADIUS = min(WIDTH, HEIGHT) // 2 // 2 * 1.50
SPEED = 3
BULLET_SPEED = 5
MONSTER_SPEED = 2
MONSTER_LIFETIME = 180  # Tempo de ida e volta
ROTATION_SPEED = 5  # Velocidade do redemoinho
INITIAL_TIME = 10
EXTRA_TIME = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


# Classe do Jogador
class Player:
    def __init__(self):
        self.angle = 0  # Ângulo inicial
        self.size = 20  # Tamanho do quadrado
        self.direction = 0  # Direção do movimento
        self.bullets = []  # Lista de balas

    def update(self):
        self.angle += self.direction * SPEED  # Ajusta o ângulo de movimento
        self.update_bullets()

    def get_position(self):
        x = WIDTH // 2 + RADIUS * math.cos(math.radians(self.angle))
        y = HEIGHT // 2 + RADIUS * math.sin(math.radians(self.angle))
        return int(x), int(y)

    def shoot(self):
        x, y = self.get_position()
        self.bullets.append(Bullet(x, y, self.angle))

    def update_bullets(self):
        self.bullets = [bullet for bullet in self.bullets if bullet.update()]

    def draw(self):
        x, y = self.get_position()
        pygame.draw.rect(
            screen,
            PLAYER_COLOR,
            (x - self.size // 2, y - self.size // 2, self.size, self.size),
        )
        for bullet in self.bullets:
            bullet.draw()


# Classe da Bala
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = math.radians(angle + 180)  # Direção para o centro
        self.speed = BULLET_SPEED

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        # Se a bala atingir o centro, remover
        if math.hypot(self.x - WIDTH // 2, self.y - HEIGHT // 2) < 5:
            return False
        return True

    def draw(self):
        pygame.draw.circle(screen, BULLET_COLOR, (int(self.x), int(self.y)), 3)


# Classe do Monstro
class Monster:
    def __init__(self):
        self.angle = random.uniform(0, 360)  # Ângulo inicial aleatório
        self.distance = 0  # Começa no centro
        self.lifetime = MONSTER_LIFETIME
        self.rotation = random.choice([-1, 1]) * ROTATION_SPEED  # Direção de rotação

    def update(self):
        self.lifetime -= 1
        self.angle += self.rotation  # Faz o monstro girar
        if self.lifetime > MONSTER_LIFETIME // 2:
            self.distance += MONSTER_SPEED  # Movendo para fora
        else:
            self.distance -= MONSTER_SPEED  # Movendo para dentro
        return self.lifetime > 0

    def get_position(self):
        x = WIDTH // 2 + self.distance * math.cos(math.radians(self.angle))
        y = HEIGHT // 2 + self.distance * math.sin(math.radians(self.angle))
        return int(x), int(y)

    def draw(self):
        x, y = self.get_position()
        pygame.draw.circle(screen, MONSTER_COLOR, (x, y), 10)


player = Player()
monsters = []
score = 0
timer = INITIAL_TIME
running = True

while running:
    screen.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.direction = -1
            elif event.key == pygame.K_RIGHT:
                player.direction = 1
            elif event.key == pygame.K_SPACE:
                player.shoot()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.direction = 0

    # Spawnar monstros
    if random.random() < 0.02:
        monsters.append(Monster())

    # Atualizar balas e monstros
    player.update()
    new_monsters = []
    for monster in monsters:
        monster.update()
        if any(
            math.hypot(
                monster.get_position()[0] - bullet.x,
                monster.get_position()[1] - bullet.y,
            )
            < 10
            for bullet in player.bullets
        ):
            score += 1
            timer += random.choice([0, EXTRA_TIME])
        else:
            new_monsters.append(monster)
    monsters = new_monsters

    # Atualizar o timer
    timer -= 1 / 60
    if timer <= 0:
        running = False

    # Desenhar elementos
    for monster in monsters:
        monster.draw()
    player.draw()
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    timer_text = font.render(f"Time: {max(0, int(timer))}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (10, 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
