import pygame
import sys

# Define colors
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)


class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pass  # To be implemented by subclasses


class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.color = BLUE
        self.speed = 5
        self.dx = 0
        self.dy = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.dx = 0
        self.dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dy = self.speed

    def move(self, walls):
        # Move horizontally
        self.rect.x += self.dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.dx > 0:
                    self.rect.right = wall.rect.left
                elif self.dx < 0:
                    self.rect.left = wall.rect.right

        # Move vertically
        self.rect.y += self.dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.dy > 0:
                    self.rect.bottom = wall.rect.top
                elif self.dy < 0:
                    self.rect.top = wall.rect.bottom

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Wall(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.color = GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Square Adventure")
        self.clock = pygame.time.Clock()
        self.player = Player(100, 100)
        self.walls = []
        self.load_map()
        self.running = True

    def load_map(self):
        map_layout = [
            "WWWWWWWWWWWWWWWW",
            "W              W",
            "W  WWW  WWWWW  W",
            "W  W        W   W",
            "W  W   WWW  W  W",
            "W  WW  W W  W  W",
            "W      W WWWW  W",
            "W  WWWW     W  W",
            "W      WW   W  W",
            "W      WW   W  W",
            "W      WW   W  W",
            "W      WW   W  W",
            "W      WW   W  W",
            "W      WW   W  W",
            "W      WW   W  W",
            "WWWWWWWWWWWWWWWW",
        ]

        for y, row in enumerate(map_layout):
            for x, char in enumerate(row):
                if char == "W":
                    self.walls.append(Wall(x * 50, y * 50))

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.render()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )

    def update(self):
        self.player.handle_input()
        self.player.move(self.walls)

    def render(self):
        self.screen.fill(BLACK)
        for wall in self.walls:
            wall.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
