from typing import Literal, Callable
from enum import Enum
from dataclasses import dataclass

from constants import PlayerType


class CardType(Enum):
    MOVEMENT = 1
    ECONOMICS = 2
    LIFE = 3

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
    name: str
    description: str
    action: str | Callable[[dict[PlayerType, int], PlayerType], str]


cards = {
    CardType.RED: [

    ],
    CardType.BLUE: [

    ],
    CardType.WHITE: [

    ]
}
