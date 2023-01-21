import pygame
import random

from sprites import Field, Oblomov, Players
from constants import (
    PlayerType, DirectionType,
    CENTRAL_CELL,
    TARGET_REACHED_REWARD
)

import ui


class Game:
    def __init__(self, surface: pygame.Surface) -> None:
        self.field = Field()
        self.oblomov = Oblomov(*CENTRAL_CELL)
        self.players = Players()

        self.surface = surface

        self.movements_left = self.dice()  # how many squares can player move before their move ends

        self.current_player = PlayerType.OBLOMOV
        self.balances = dict.fromkeys(PlayerType, 0)

        

    def next_move(self, player: PlayerType | None = None) -> None:
        self.current_player = player or tuple(PlayerType)[(tuple(PlayerType).index(self.current_player) + 1) % 4]

    def dice(self) -> int:
        return ui.roll_dice(self.surface)

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
