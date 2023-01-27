from random import randint

import pygame

from sprites import Field, Oblomov, Players, Moves
from constants import (
    PlayerType, DirectionType,
    CENTRAL_CELL,
    TARGET_REACHED_REWARD, MAX_STEPS, TOTAL_MOVES
)


class Game:
    def __init__(self, surface: pygame.Surface) -> None:
        self.field = Field()
        self.oblomov = Oblomov(*CENTRAL_CELL)
        self.players = Players()
        self.moves = Moves()

        self.surface = surface

        self.steps_left = self.throw_dice()  # how many squares can player move before their move ends
        self.moves_left = TOTAL_MOVES
        self.game_over = False

        self.current_player = PlayerType.OBLOMOV
        self.is_oblomov_sleeping = False
        self.balances = dict.fromkeys(PlayerType, 0)

    def update(self, events: list[pygame.event.Event]) -> None:
        if self.game_over:
            return

        for event in events:
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s
            ]:
                self.oblomov_step(event)

    def draw(self) -> None:
        self.surface.fill("#444444")

        self.players.draw(self.surface, self.balances, self.current_player, self.game_over)
        self.moves.draw(self.surface, self.steps_left, self.moves_left)

        self.field.draw(self.surface)
        self.oblomov.draw(self.surface)

    def oblomov_step(self, event: pygame.event) -> None:
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

        self.steps_left -= 1
        if self.steps_left == 0:
            self.next_move()
            self.moves_left -= 1
            if self.moves_left == 0:
                self.game_over = True
            else:
                self.steps_left = self.throw_dice()

        match coords:
            case self.field.oblomovka:
                self.balances[PlayerType.OBLOMOV] += TARGET_REACHED_REWARD
                self.game_over = True
            case self.field.shtoltz:
                self.balances[PlayerType.SHTOLTZ] += TARGET_REACHED_REWARD
                self.game_over = True
            case self.field.olga:
                self.balances[PlayerType.OLGA] += TARGET_REACHED_REWARD
                self.game_over = True
            case self.field.tarantiev:
                self.balances[PlayerType.TARANTIEV] += TARGET_REACHED_REWARD
                self.game_over = True

    def next_move(self, player: PlayerType | None = None) -> None:
        self.current_player = player or tuple(PlayerType)[
            (tuple(PlayerType).index(self.current_player) + 1) % len(self.balances)
        ]

        if not player and self.current_player == PlayerType.OBLOMOV:
            self.is_oblomov_sleeping = not self.is_oblomov_sleeping
            if self.is_oblomov_sleeping:
                self.next_move()

    @staticmethod
    def throw_dice() -> int:
        return randint(1, MAX_STEPS)
