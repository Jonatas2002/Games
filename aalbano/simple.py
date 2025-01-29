import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Simple Pygame Init")
dt = 0

font = pygame.font.Font(None, 36)
text_color = (0, 0, 0)

player_radius = 40
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
velocity_y = 0  # Velocidade vertical da bola
gravity = 800  # Intensidade da gravidade (pixels por segundo ao quadrado)

sky_blue = (167, 213, 255)

dragging = False

# Main game loop
while running:
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            distance = pygame.math.Vector2(
                mouse_x - player_pos.x, mouse_y - player_pos.y
            ).length()
            if distance < player_radius:
                dragging = True

        if event.type == pygame.MOUSEMOTION and dragging:
            player_pos.x, player_pos.y = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    if not dragging:
        velocity_y += gravity * dt  # Acelera a queda
        player_pos.y += velocity_y * dt  # Move a bola para baixo

    # Collision with bottom of the screen
    if player_pos.y + player_radius > screen.get_height():
        player_pos.y = screen.get_height() - player_radius
        velocity_y = 0  # Para a velocidade ao tocar o chão

    # Fill the screen with a color (RGB)
    screen.fill(sky_blue)

    # RENDER YOUR GAME HERE
    pygame.draw.circle(screen, "red", player_pos, player_radius)

    velocity_text = font.render(f"Velocidade: {int(velocity_y)} px/s", True, text_color)

    text_x = screen.get_width() - velocity_text.get_width() - 20
    text_y = 20
    screen.blit(velocity_text, (text_x, text_y))

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()
