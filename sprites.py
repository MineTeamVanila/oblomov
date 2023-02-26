from pathlib import Path
from math import copysign

import pygame
from pygame.image import load

from cards import Card, CardType
from util import random_cell, random_aim_cell, cell_distance, split_card_description
from constants import (
    WIDTH, HEIGHT, BORDER, FIELD_SIZE, CELL_SIZE,
    OBSTACLE_COUNT, MIN_AIM_DISTANCE, MIN_AIM_SPREAD, CENTRAL_CELL,
    ANIMATION_SPEED, place_to_color,
    Colors, Images, Fonts, CellType, PlayerType, DirectionType
)


class PlayersSprite(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.Surface((WIDTH, BORDER), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def draw(
            self,
            surface: pygame.Surface,
            balances: dict[PlayerType, int],
            current_player: PlayerType,
            final: bool = False,
            bad_ending: bool = False
    ) -> None:
        places = sorted(set(balances.values()), reverse=True) if final else None

        self.image.fill(Colors.empty)

        for index, (player, balance) in enumerate(balances.items()):
            name_surface = Fonts.stats.render(
                str(player),
                True,
                (
                    Colors.text_red if bad_ending else place_to_color[places.index(balance)]
                ) if final else (
                    Colors.stats_current if player == current_player else Colors.stats
                )
            )
            balance_surface = Fonts.stats.render(
                str(balance),
                True,
                (
                    Colors.text_red if bad_ending else place_to_color[places.index(balance)]
                ) if final else (
                    Colors.stats_current if player == current_player else Colors.stats
                )
            )

            player_surface = pygame.Surface((WIDTH / 4, BORDER), pygame.SRCALPHA)
            centerx = player_surface.get_rect().centerx
            player_surface.blit(name_surface, name_surface.get_rect(centerx=centerx, y=BORDER / 10))
            player_surface.blit(balance_surface, balance_surface.get_rect(centerx=centerx, y=BORDER / 2))

            self.image.blit(player_surface, (WIDTH / 4 * index, 0))

        surface.blit(self.image, self.rect)


class FieldBackground(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.Surface((WIDTH - BORDER * 2, HEIGHT - BORDER * 2))
        self.rect = self.image.get_rect(left=BORDER, top=BORDER)

        self.image.fill(Colors.field_background)


class CellSprite(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, cell_type: CellType, card_type: CardType | None) -> None:
        super().__init__()

        self.x = x  # on the field
        self.y = y  # on the field
        self.type = cell_type
        self.card_type = card_type

        self.image = load(path) if (
            path := Path(Images.images_dir, "_".join(filter(lambda s: s, [
                "cell", self.type.name.lower(), self.card_type.name.lower() if self.card_type else None
            ])) + ".png")
        ).exists() else pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(
            center=(BORDER + (self.x + 0.5) * CELL_SIZE, BORDER + (self.y + 0.5) * CELL_SIZE)
        )

        match self.type:
            case CellType.EMPTY:
                color = "#00000000"
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

        if not path.exists():
            self.image.fill(color)
            if self.card_type:
                pygame.draw.polygon(
                    self.image,
                    self.card_type.value,
                    (
                        (CELL_SIZE / 2, CELL_SIZE / 4), (CELL_SIZE * 0.75, CELL_SIZE / 2),
                        (CELL_SIZE / 2, CELL_SIZE * 0.75), (CELL_SIZE / 4, CELL_SIZE / 2)
                    )
                )


class FieldSpriteGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        # noinspection PyTypeChecker
        self.add(FieldBackground())

        self.obstacles = set()
        for _ in range(OBSTACLE_COUNT):
            self.obstacles.add(random_cell(FIELD_SIZE))

        self.oblomovka = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)

        self.shtoltz = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)
        while cell_distance(self.shtoltz, self.oblomovka) < MIN_AIM_SPREAD:
            self.shtoltz = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)

        self.olga = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)
        while cell_distance(self.olga, self.oblomovka) < MIN_AIM_SPREAD or \
                cell_distance(self.olga, self.shtoltz) < MIN_AIM_SPREAD:
            self.olga = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)

        self.tarantiev = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)
        while cell_distance(self.tarantiev, self.oblomovka) < MIN_AIM_SPREAD or \
                cell_distance(self.tarantiev, self.shtoltz) < MIN_AIM_SPREAD or \
                cell_distance(self.tarantiev, self.olga) < MIN_AIM_SPREAD:
            self.tarantiev = random_aim_cell(FIELD_SIZE, MIN_AIM_DISTANCE)

        self.obstacles = self.obstacles - {self.oblomovka, self.shtoltz, self.olga, self.tarantiev, CENTRAL_CELL}

        movement_cards = set()
        while len(movement_cards) < 4:
            if (cell := random_cell(FIELD_SIZE)) in self.obstacles or \
                    cell in (self.oblomovka, self.shtoltz, self.olga, self.tarantiev, CENTRAL_CELL):
                continue
            movement_cards.add(cell)

        economics_cards = set()
        while len(economics_cards) < 4:
            if (cell := random_cell(FIELD_SIZE)) in self.obstacles or \
                    cell in (self.oblomovka, self.shtoltz, self.olga, self.tarantiev, CENTRAL_CELL) or \
                    cell in movement_cards:
                continue
            economics_cards.add(cell)

        life_card = None
        while life_card is None:
            if (cell := random_cell(FIELD_SIZE)) in self.obstacles or \
                    cell in (self.oblomovka, self.shtoltz, self.olga, self.tarantiev, CENTRAL_CELL) or \
                    cell in movement_cards or \
                    cell in economics_cards:
                continue
            life_card = cell

        for x in range(FIELD_SIZE):
            for y in range(FIELD_SIZE):
                cell_type = CellType.EMPTY
                card_type = None
                match (x, y):
                    case coords if coords in self.obstacles:
                        cell_type = CellType.OBSTACLE
                    case self.oblomovka:
                        cell_type = CellType.OBLOMOVKA
                    case self.shtoltz:
                        cell_type = CellType.SHTOLTZ
                    case self.olga:
                        cell_type = CellType.OLGA
                    case self.tarantiev:
                        cell_type = CellType.TARANTIEV
                    case coords if coords in movement_cards:
                        card_type = CardType.MOVEMENT
                    case coords if coords in economics_cards:
                        card_type = CardType.ECONOMICS
                    case coords if coords == life_card:
                        card_type = CardType.LIFE

                # noinspection PyTypeChecker
                self.add(CellSprite(x, y, cell_type, card_type))


class OblomovSprite(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()

        self.x = x
        self.y = y
        self.transition_x = 0
        self.transition_y = 0

        self.image = Images.oblomov
        self.rect = self.image.get_rect(
            centerx=BORDER + (self.x + 0.5) * CELL_SIZE,
            bottom=BORDER + (self.y + 1) * CELL_SIZE
        )

    def draw(self, surface: pygame.Surface) -> None:
        self.rect.left += (delta_x := copysign(ANIMATION_SPEED, self.transition_x) if self.transition_x else 0)
        self.rect.top += (delta_y := copysign(ANIMATION_SPEED, self.transition_y) if self.transition_y else 0)
        self.transition_x -= delta_x
        self.transition_y -= delta_y

        surface.blit(self.image, self.rect)

    def move(
            self,
            direction: DirectionType,
            obstacles: set[tuple[int, int]]
    ) -> tuple[int, int] | None:
        match direction:
            case DirectionType.UP if self.y > 0 and (self.x, self.y - 1) not in obstacles:
                self.y -= 1
                self.transition_y += -CELL_SIZE
            case DirectionType.DOWN if self.y < (FIELD_SIZE - 1) and (self.x, self.y + 1) not in obstacles:
                self.y += 1
                self.transition_y += CELL_SIZE
            case DirectionType.LEFT if self.x > 0 and (self.x - 1, self.y) not in obstacles:
                self.x -= 1
                self.transition_x += -CELL_SIZE
            case DirectionType.RIGHT if self.x < (FIELD_SIZE - 1) and (self.x + 1, self.y) not in obstacles:
                self.x += 1
                self.transition_x += CELL_SIZE
            case _:
                return

        return self.x, self.y


class MovesSprite(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.Surface((WIDTH, BORDER), pygame.SRCALPHA)
        self.rect = self.image.get_rect(top=HEIGHT - BORDER)
        self.base_rect = self.image.get_rect()

    def draw(self, surface: pygame.Surface, moves: int, steps: int, boost: int) -> None:
        self.image.fill(Colors.empty)

        steps_surface = Fonts.moves.render(f"Шаги: {steps}", True, Colors.moves)
        moves_surface = Fonts.moves.render(f"Ходы: {moves}", True, Colors.moves)
        if boost > 0:
            boost_surface = Fonts.moves.render(f"Шаги: {steps} + {boost}", True, Colors.moves)
        elif boost < 0:
            boost_surface = Fonts.moves.render(f"Шаги: {steps} - {abs(boost)}", True, Colors.moves_red)
        else:
            boost_surface = Fonts.moves.render("", True, Colors.moves)

        self.image.blit(boost_surface, boost_surface.get_rect(left=WIDTH / 20, centery=self.base_rect.centery))
        self.image.blit(steps_surface, steps_surface.get_rect(left=WIDTH / 20, centery=self.base_rect.centery))
        self.image.blit(moves_surface, moves_surface.get_rect(right=WIDTH - WIDTH / 20, centery=self.base_rect.centery))

        surface.blit(self.image, self.rect)


class CardSprite(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.card: Card | None = None

        self.image = pygame.Surface((WIDTH - BORDER * 2, HEIGHT - BORDER * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(left=BORDER, top=BORDER)
        self.base_rect = self.image.get_rect()

    def draw(self, surface: pygame.Surface) -> None:
        if not self.card:
            return

        self.image.fill(Colors.card_bg_fade)

        title_surface = Fonts.card_title.render(self.card.title, True, self.card.type.value)
        rarity_surface = Fonts.card_rarity.render(f"Редкость: {self.card.rarity}", True, Colors.card_rarity)

        description_surface = pygame.Surface((self.base_rect.width, self.base_rect.height * 0.5), pygame.SRCALPHA)
        description_rect = description_surface.get_rect()
        for index, string in enumerate(split_card_description(self.card.description)):
            string_surface = Fonts.card_description.render(string, True, Colors.card_description)
            description_surface.blit(
                string_surface,
                string_surface.get_rect(centerx=description_rect.centerx, top=description_rect.height / 8 * index)
            )

        self.image.blit(title_surface, title_surface.get_rect(centerx=self.base_rect.centerx))
        self.image.blit(
            rarity_surface,
            rarity_surface.get_rect(centerx=self.base_rect.centerx, bottom=self.base_rect.bottom)
        )
        self.image.blit(
            description_surface,
            description_surface.get_rect(centerx=self.base_rect.centerx, top=self.base_rect.height / 4)
        )

        surface.blit(self.image, self.rect)
