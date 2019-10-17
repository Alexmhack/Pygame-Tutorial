import pygame

from pygame.locals import (
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    QUIT
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite player")

running = True


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()


player = Player()

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(player.surf, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    pygame.display.flip()

pygame.quit()
