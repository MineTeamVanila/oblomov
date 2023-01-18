import pygame

from util import random_cell, random_aim_cell, cell_distance
from constants import (
    Colors, Fonts, CellType, PlayerType, DirectionType,
    EMPTY_COLOR,
    WIDTH, BORDER, FIELD_SIZE, CELL_SIZE, CENTRAL_CELL, OBSTACLE_COUNT, MIN_AIM_DISTANCE,
    TARGET_REACHED_REWARD
)


class Players(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.Surface((WIDTH, BORDER), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0

    def draw(self, surface: pygame.Surface, balances: dict[PlayerType, int], current_player: PlayerType) -> None:
        self.image.fill(EMPTY_COLOR)

        for index, (player, balance) in enumerate(balances.items()):
            name_surface = Fonts.stats.render(
                str(player),
                True,
                Colors.stats_current if player == current_player else Colors.stats
            )
            balance_surface = Fonts.stats.render(
                str(balance),
                True,
                Colors.stats_current if player == current_player else Colors.stats
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
        self.obstacles.discard(CENTRAL_CELL)  # field center, Oblomov starts there

        self.visited_cells = {CENTRAL_CELL}

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

    def move(
        self,
        direction: DirectionType,
        obstacles: set[tuple[int, int]]
    ) -> tuple[int, int]:  # (-1, -1) if unsuccessful
        match direction:
            case DirectionType.UP if self.y > 0 and (self.x, self.y - 1) not in obstacles:
                self.y -= 1
            case DirectionType.DOWN if self.y < (FIELD_SIZE - 1) and (self.x, self.y + 1) not in obstacles:
                self.y += 1
            case DirectionType.LEFT if self.x > 0 and (self.x - 1, self.y) not in obstacles:
                self.x -= 1
            case DirectionType.RIGHT if self.x < (FIELD_SIZE - 1) and (self.x + 1, self.y) not in obstacles:
                self.x += 1
            case _:
                return -1, -1

        self.rect.x = BORDER + self.x * CELL_SIZE
        self.rect.y = BORDER + self.y * CELL_SIZE

        return self.x, self.y


class Game:
    def __init__(self) -> None:
        self.field = Field()
        self.oblomov = Oblomov(*CENTRAL_CELL)
        self.players = Players()

        self.movements_left = self.dice()  # how many squares can player move before their move ends

        self.current_player = PlayerType.OBLOMOV
        self.balances = dict.fromkeys(PlayerType, 0)

    def next_move(self, player: PlayerType | None = None) -> None:
        self.current_player = player or tuple(PlayerType)[(tuple(PlayerType).index(self.current_player) + 1) % 4]

    def dice(self) -> int:
        return 3  # TODO

    def oblomov_movement(self, event: pygame.event) -> None:
        match event.key:
            case pygame.K_UP | pygame.K_w:
                direction = DirectionType.UP
            case pygame.K_DOWN | pygame.K_s:
                direction = DirectionType.DOWN
            case pygame.K_LEFT | pygame.K_a:
                direction = DirectionType.LEFT
            case pygame.K_RIGHT | pygame.K_d:
                direction = DirectionType.RIGHT
            case _:
                direction = DirectionType.UNKNOWN

        if (coords := self.oblomov.move(direction, self.field.obstacles)) == (-1, -1):
            return

        self.movements_left -= 1
        if self.movements_left == 0:
            self.next_move()
            self.movements_left = self.dice()

        match coords:
            case self.field.oblomovka if self.field.oblomovka not in self.field.visited_cells:
                self.balances[PlayerType.OBLOMOV] += TARGET_REACHED_REWARD
            case self.field.shtoltz if self.field.shtoltz not in self.field.visited_cells:
                self.balances[PlayerType.SHTOLTZ] += TARGET_REACHED_REWARD
            case self.field.olga if self.field.olga not in self.field.visited_cells:
                self.balances[PlayerType.OLGA] += TARGET_REACHED_REWARD
            case self.field.tarantiev if self.field.tarantiev not in self.field.visited_cells:
                self.balances[PlayerType.TARANTIEV] += TARGET_REACHED_REWARD

        self.field.visited_cells.add(coords)

    def update(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s
            ]:
                self.oblomov_movement(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill("#444444")

        self.field.draw(surface)
        self.oblomov.draw(surface)
        self.players.draw(surface, self.balances, self.current_player)
