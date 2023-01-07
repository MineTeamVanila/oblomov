import pygame

from util import random_cell, random_aim_cell
from constants import CellType, BORDER, FIELD_SIZE, CELL_SIZE, OBSTACLE_COUNT, MIN_AIM_DISTANCE


class FieldCell(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, type: CellType) -> None:
        super().__init__()

        self.x = x
        self.y = y
        self.type = type

        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()

        self.rect.x = BORDER + self.x * CELL_SIZE
        self.rect.y = BORDER + self.y * CELL_SIZE

        match self.type:
            case CellType.EMPTY:
                color = "#888888"
            case CellType.OBSTACLE:
                color = "#222222"
            case CellType.OBLOMOVKA:
                color = "#009900"  # мусульманский зеленый
            case CellType.SHTOLTZ:
                color = "#6600ff"  # персидский синий
            case CellType.OLGA:
                color = "#fbec5d"  # кукурузный
            case CellType.TARANTIEV:
                color = "#ff4f00"  # сигнальный оранжевый
            case _:  # should not be the case
                color = "#0000ff"

        self.image.fill(color)


class Field(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        self.obstacles = set()
        for _ in range(OBSTACLE_COUNT):
            self.obstacles.add(random_cell(FIELD_SIZE))

        self.oblomovka = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)

        self.shtoltz = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)
        while self.shtoltz == self.oblomovka:
            self.shtoltz = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)

        self.olga = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)
        while self.olga == self.oblomovka or self.olga == self.shtoltz:
            self.olga = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)

        self.tarantiev = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)
        while self.tarantiev == self.oblomovka or self.tarantiev == self.shtoltz or self.tarantiev == self.olga:
            self.tarantiev = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)

        self.obstacles.discard(self.oblomovka)
        self.obstacles.discard(self.shtoltz)
        self.obstacles.discard(self.olga)
        self.obstacles.discard(self.tarantiev)
        self.obstacles.discard((FIELD_SIZE // 2, FIELD_SIZE // 2))  # field center, Oblomov starts there

        for x in range(FIELD_SIZE):
            for y in range(FIELD_SIZE):
                type = CellType.EMPTY
                match (x, y):
                    case coords if coords in self.obstacles:
                        type = CellType.OBSTACLE
                    case self.oblomovka:
                        type = CellType.OBLOMOVKA
                    case self.shtoltz:
                        type = CellType.SHTOLTZ
                    case self.olga:
                        type = CellType.OLGA
                    case self.tarantiev:
                        type = CellType.TARANTIEV

                # noinspection PyTypeChecker
                self.add(FieldCell(x, y, type))



class Oblomov(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()

        self.x = x
        self.y = y

        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.rect.x = BORDER + self.x * CELL_SIZE
        self.rect.y = BORDER + self.y * CELL_SIZE

        pygame.draw.circle(self.image, "#1faee9", (CELL_SIZE / 2, CELL_SIZE / 2), CELL_SIZE / 3)  # цвет твиттера

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def update(self, event: pygame.event.Event, field: Field):
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT if self.x > 0 and (self.x - 1, self.y) not in field.obstacles:
                    self.x -= 1
                case pygame.K_RIGHT if self.x < (FIELD_SIZE - 1) and (self.x + 1, self.y) not in field.obstacles:
                    self.x += 1
                case pygame.K_UP if self.y > 0 and (self.x, self.y - 1) not in field.obstacles:
                    self.y -= 1
                case pygame.K_DOWN if self.y < (FIELD_SIZE - 1) and (self.x, self.y + 1) not in field.obstacles:
                    self.y += 1

            self.rect.x = BORDER + self.x * CELL_SIZE
            self.rect.y = BORDER + self.y * CELL_SIZE
