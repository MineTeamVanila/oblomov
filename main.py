import pygame
pygame.init()

from objects import Field, Oblomov, Players
from constants import WIDTH, HEIGHT, FPS, FIELD_SIZE


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бюджет игры: 1000 нервных клеток Андрея")  # игру обломов не делал. По факту
clock = pygame.time.Clock()


field = Field()
oblomov = Oblomov(FIELD_SIZE // 2, FIELD_SIZE // 2)  # field center
players = Players()


done = False
while not done:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        oblomov.move(event, field)


    screen.fill("#444444")

    field.draw(screen)
    oblomov.draw(screen)
    players.draw(screen)


    pygame.display.flip()

pygame.quit()
