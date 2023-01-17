import pygame

from util import random_cell, random_aim_cell, cell_distance
from constants import (
    Colors, Fonts, CellType, PlayerType,
    WIDTH, BORDER, FIELD_SIZE, CELL_SIZE, OBSTACLE_COUNT, MIN_AIM_DISTANCE, EMPTY_COLOR
)


class Players(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.current = PlayerType.OBLOMOV
        self.balances = dict.fromkeys(PlayerType, 0)

        self.image = pygame.Surface((WIDTH, BORDER), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0

    def draw(self, surface: pygame.Surface) -> None:
        self.image.fill(EMPTY_COLOR)

        for index, (player, balance) in enumerate(self.balances.items()):
            name_surface = Fonts.stats.render(
                str(player),
                True,
                Colors.stats_current if player == self.current else Colors.stats
            )
            balance_surface = Fonts.stats.render(
                str(balance),
                True,
                Colors.stats_current if player == self.current else Colors.stats
            )

            player_surface = pygame.Surface((WIDTH / 4, BORDER), pygame.SRCALPHA)
            player_surface.blit(
                name_surface,
                name_surface.get_rect(centerx=player_surface.get_rect().centerx, y=BORDER * 1/10),
            )
            player_surface.blit(
                balance_surface,
                balance_surface.get_rect(centerx=player_surface.get_rect().centerx, y=BORDER * 1/2),
            )

            self.image.blit(player_surface, (WIDTH / 4 * index, 0))

        surface.blit(self.image, (0, 0))

    def next_move(self, player: PlayerType | None = None) -> None:
        self.current = player or tuple(PlayerType)[(tuple(PlayerType).index(self.current) + 1) % 4]


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
        while cell_distance(self.shtoltz, self.oblomovka) < 5:
            self.shtoltz = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)

        self.olga = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)
        while cell_distance(self.olga, self.oblomovka) < 5 or cell_distance(self.olga, self.shtoltz) < 5:
            self.olga = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)

        self.tarantiev = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)
        while cell_distance(self.tarantiev, self.oblomovka) < 5 or \
                cell_distance(self.tarantiev, self.shtoltz) < 5 or \
                cell_distance(self.tarantiev, self.olga) < 5:
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

    def move(self, event: pygame.event.Event, field: Field) -> None:
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT | pygame.K_a if self.x > 0 and (self.x - 1, self.y) not in field.obstacles:
                    self.x -= 1
                case pygame.K_RIGHT | pygame.K_d \
                        if self.x < (FIELD_SIZE - 1) and (self.x + 1, self.y) not in field.obstacles:
                    self.x += 1
                case pygame.K_UP | pygame.K_w if self.y > 0 and (self.x, self.y - 1) not in field.obstacles:
                    self.y -= 1
                case pygame.K_DOWN | pygame.K_s \
                        if self.y < (FIELD_SIZE - 1) and (self.x, self.y + 1) not in field.obstacles:
                    self.y += 1

            self.rect.x = BORDER + self.x * CELL_SIZE
            self.rect.y = BORDER + self.y * CELL_SIZE
