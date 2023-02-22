from typing import Literal, Callable
from enum import Enum
from dataclasses import dataclass
from random import random

from constants import Colors, PlayerType


class CardType(Enum):
    MOVEMENT = Colors.card_title_movement
    ECONOMICS = Colors.card_title_economics
    LIFE = Colors.card_title_life

    # aliases
    RED = MOVEMENT
    BLUE = ECONOMICS
    WHITE = LIFE

    def __str__(self) -> str:
        return self.name


@dataclass
class Card:
    type: CardType
    rarity: Literal[1, 2, 3, 4]
    title: str
    description: str
    action: str | Callable[[dict[PlayerType, int], PlayerType], str]


# noinspection PyUnusedLocal
def blue_1(balances: dict[PlayerType, int], current_player: PlayerType) -> str:
    if (rnd := random() * 100) < 50:
        return "get_money current 5"
    if rnd < 60:
        return "get_money current 10"
    return "lose_money current 5"


cards = {
    CardType.RED: [
        Card(
            type=CardType.RED,
            rarity=1,
            title="Пирог из Обломовки",
            description="Такой вкусный пирог, что не хочется уходить отсюда!\n\n"
                        "До следующего вашего хода Обломов ходит на 1 клетку меньше",
            action="slow_others 1"
        )
    ],
    CardType.BLUE: [
        Card(
            type=CardType.BLUE,
            rarity=1,
            title="Инвестиция",
            description="Рассматриваете обломовские пироги как бренд? А вы предприниматель!\n\n"
                        "Вы получаете либо 5 монет (50%), либо 10 (10%), либо теряете 5 (40%)",
            action=blue_1
        ),
        Card(
            type=CardType.BLUE,
            rarity=4,
            title="Обломовка",
            description="Представьте, что вы - Илья Ильич! "
                        "Все, что вам нужно - закутаться в халат, лежать на диване и пить кофе.\n\n"
                        "Игрок в течение следующих 5 ходов получает 1/20 от суммы капиталов остальных игроков "
                        "(с округлением в большую сторону, минимум 3 монеты)",
            action="bonus_income"
        )
    ],
    CardType.WHITE: [
        Card(
            type=CardType.WHITE,
            rarity=1,
            title="Зарядка",
            description="На гору и обратно вместе с Обломовым!\n\nОбломов проживет на 3 хода дольше",
            action="heal 3"
        )
    ]
}

cards_for_choice: dict[CardType, list[Card]] = dict(map(
    lambda type, lst: (
        type,
        [
            duped_card
            for card in lst
            for duped_card in (card,) * ((5 - card.rarity) ** 2)
        ]  # rarity -> count: 1 -> 16, 2 -> 9, 3 -> 4, 4 -> 1
    ),
    *zip(*cards.items())
))
