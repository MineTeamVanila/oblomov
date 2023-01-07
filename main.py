import pygame

from objects import Field, Oblomov
from constants import WIDTH, HEIGHT, FPS, FIELD_SIZE


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра в манипуляцию Обломовым")  # игру обломов не делал. По факту
clock = pygame.time.Clock()


field = Field()
oblomov = Oblomov(FIELD_SIZE // 2, FIELD_SIZE // 2)  # field center


done = False
while not done:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        oblomov.update(event, field)


    screen.fill("#444444")
    field.draw(screen)
    oblomov.draw(screen)


    pygame.display.flip()

pygame.quit()
