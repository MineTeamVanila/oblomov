import pygame

from game import Game
from constants import WIDTH, HEIGHT, FPS

import ui

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("1000 нервных клеток Андрея")  # игру обломов не делал. По факту
    clock = pygame.time.Clock()

    game = Game(screen)

    done = False
    while not done:
        clock.tick(FPS)

        events = pygame.event.get()
        if any(map(lambda e: e.type == pygame.QUIT, events)):
            done = True

        game.update(events)
        game.draw(screen)

        pygame.display.flip()

    pygame.quit()
