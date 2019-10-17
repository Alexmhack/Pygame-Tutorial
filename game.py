import pygame

from pygame.locals import (
    # K_UP,
    # K_DOWN,
    # K_LEFT,
    # K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

# initialize pygame library
pygame.init()

# constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

while running:
    for event in pygame.event.get():
        # if the event type is a key press
        if event.type == KEYDOWN:
            # user has clicked the escape button, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # user closed the window, stop the loop
        if event.type == QUIT:
            running = False

    surf = pygame.Surface((50, 50))
    surf.fill((0, 0, 0))

    rect = surf.get_rect()

    screen.fill((255, 255, 255))
    screen.blit(surf, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    pygame.display.flip()

pygame.quit()
