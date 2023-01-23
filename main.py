import pygame

from game import Game
from constants import WIDTH, HEIGHT, FPS


if __name__ == "__main__":
    pygame.init()

    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("1000 нервных клеток Андрея")  # игру обломов не делал. По факту
    clock = pygame.time.Clock()

    game = Game(surface)

    done = False
    while not done:
        clock.tick(FPS)

        events = pygame.event.get()
        if any(e.type == pygame.QUIT for e in events):
            done = True

        game.update(events)
        game.draw()

        pygame.display.flip()

    pygame.quit()
