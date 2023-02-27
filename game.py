from random import randint, choice
from math import ceil

import pygame

from sprites import FieldSpriteGroup, OblomovSprite, PlayersSprite, MovesSprite, CardSprite
from cards import Card
from util import get_card
from constants import (
    CENTRAL_CELL,
    MAX_STEPS, TOTAL_MOVES,
    player_order,
    PlayerType, DirectionType, Money
)


class Game:
    def __init__(self, surface: pygame.Surface) -> None:
        self.field_sprite = FieldSpriteGroup()
        self.oblomov_sprite = OblomovSprite(*CENTRAL_CELL, player_order[0])
        self.players_sprite = PlayersSprite()
        self.moves_sprite = MovesSprite()
        self.card_sprite = CardSprite()

        self.surface = surface

        self.current_player = player_order[0]
        self.is_oblomov_sleeping = False
        self.balances = dict.fromkeys(player_order, 0)

        self.moves_left = TOTAL_MOVES
        self.boosts = dict.fromkeys(player_order, 0)
        self.steps_left = self.throw_dice()  # how many squares can player move before their move ends
        self.game_over = False
        self.bad_ending = False
        self.reward_available = True
        self.getting_bonus_income = dict.fromkeys(player_order, 0)  # how many times players would get bonus

        self.balances[PlayerType.OBLOMOV] += Money.oblomov_income  # as first move

    def update(self, events: list[pygame.event.Event]) -> None:
        if self.game_over:
            return

        for event in events:
            if self.card_sprite.card and event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self.card_sprite.card = None
                continue

            if not self.card_sprite.card and event.type == pygame.KEYDOWN and event.key in (
                pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s
            ):
                self.step(event)

    def draw(self) -> None:
        self.surface.fill("#444444")

        self.players_sprite.draw(self.surface, self.balances, self.current_player, self.game_over, self.bad_ending)
        self.moves_sprite.draw(self.surface, self.moves_left, self.steps_left, self.boosts[self.current_player])

        self.field_sprite.draw(self.surface)
        self.oblomov_sprite.draw(self.surface, self.current_player)

        self.card_sprite.draw(self.surface)

    def step(self, event: pygame.event) -> None:
        self.reward_available = True

        match event.key:
            case pygame.K_UP | pygame.K_w:
                direction = DirectionType.UP
            case pygame.K_DOWN | pygame.K_s:
                direction = DirectionType.DOWN
            case pygame.K_LEFT | pygame.K_a:
                direction = DirectionType.LEFT
            case pygame.K_RIGHT | pygame.K_d:
                direction = DirectionType.RIGHT
            case _:  # should not normally happen
                direction = DirectionType.UNKNOWN

        if not (coords := self.oblomov_sprite.move(direction, self.field_sprite.obstacles)):
            return

        if self.boosts[self.current_player] > 0:
            self.boosts[self.current_player] -= 1
        else:
            self.steps_left -= 1

        match coords:
            case self.field_sprite.oblomovka:
                self.balances[PlayerType.OBLOMOV] += Money.target_reached_reward
                self.game_over = True
            case self.field_sprite.shtoltz:
                self.balances[PlayerType.SHTOLTZ] += Money.target_reached_reward
                self.game_over = True
            case self.field_sprite.olga:
                self.balances[PlayerType.OLGA] += Money.target_reached_reward
                self.game_over = True
            case self.field_sprite.tarantiev:
                self.balances[PlayerType.TARANTIEV] += Money.target_reached_reward
                self.game_over = True

        if self.steps_left + self.boosts[self.current_player] == 0:
            self.boosts[self.current_player] = 0

            if card_type := next(spr for spr in self.field_sprite.sprites() if (spr.x, spr.y) == coords).card_type:
                card = get_card(card_type)
                self.card_sprite.card = card
                self.process_card(card)

            for player in player_order:
                if self.getting_bonus_income[player] == 0:
                    continue

                other_players = list(player_order)
                other_players.remove(player)
                self.balances[player] += max(ceil(sum(map(lambda p: self.balances[p], other_players)) / 20), 3)
                self.getting_bonus_income[player] -= 1

            self.next_move()
            self.moves_left -= 1

            if self.moves_left == 0:
                if not self.game_over:
                    self.bad_ending = True
                self.game_over = True
            else:
                self.steps_left = self.throw_dice()

    def next_move(self, player: PlayerType | None = None) -> None:
        self.current_player = player or player_order[
            (player_order.index(self.current_player) + 1) % len(player_order)
        ]

        if not player and self.current_player == PlayerType.OBLOMOV:
            self.is_oblomov_sleeping = not self.is_oblomov_sleeping
            if self.is_oblomov_sleeping:
                self.next_move()

        if self.reward_available:
            self.balances[PlayerType.OBLOMOV] += Money.oblomov_income
            match self.current_player:
                case PlayerType.SHTOLTZ:
                    self.balances[PlayerType.SHTOLTZ] += Money.shtoltz_income
                case PlayerType.OLGA:
                    self.balances[PlayerType.OLGA] += Money.olga_income
                case PlayerType.TARANTIEV:  # stealth
                    players = list(player_order)
                    players.remove(PlayerType.TARANTIEV)
                    target = choice(players)
                    self.balances[target] -= Money.tarantiev_stealth_amount[target]
                    self.balances[PlayerType.TARANTIEV] += Money.tarantiev_stealth_amount[target]
            self.reward_available = False

    def process_card(self, card: Card) -> None:
        actions = card.action if isinstance(card.action, str) else card.action(
            self.balances, self.current_player, self.is_oblomov_sleeping
        )

        for action in filter(lambda s: s, actions.split(";")):
            match tuple(map(lambda val: int(val) if val.isdigit() else val, action.strip().split())):
                case "turn", str(player):
                    self.next_move(player_order[
                        (player_order.index(PlayerType.__getitem__(player.upper())) - 1) % len(player_order)
                    ])  # -1 because self.next_move will be called again
                case ("skip",):
                    if not (self.current_player == PlayerType.TARANTIEV and self.is_oblomov_sleeping):
                        self.next_move()  # if OBLOMOV isn't next
                case "boost", "current", int(amount):
                    self.boosts[self.current_player] = amount
                case "boost", str(player), int(amount):
                    self.boosts[PlayerType.__getitem__(player.upper())] = amount
                case "slow_others", int(amount):
                    players = list(player_order)
                    players.remove(self.current_player)
                    for player in players:
                        self.boosts[player] = -amount
                case "get_money", "current", int(amount):
                    self.balances[self.current_player] += amount
                case "get_money", str(player), int(amount):
                    self.balances[PlayerType.__getitem__(player.upper())] += amount
                case "lose_money", "current", int(amount):
                    self.balances[self.current_player] -= amount
                case "lose_money", str(player), int(amount):
                    self.balances[PlayerType.__getitem__(player.upper())] -= amount
                case ("bonus_income",):
                    self.getting_bonus_income[self.current_player] = 5
                case "heal", int(amount):
                    self.moves_left += amount


    def throw_dice(self) -> int:
        return max(-self.boosts[self.current_player] + 1, randint(1, MAX_STEPS))  # at least 1 accounting negative boost
