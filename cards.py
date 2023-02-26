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

def blue_2(balances: dict[PlayerType, int], current_player: PlayerType) -> str:
    if (rnd := random() * 100) < 50:
        return "get_money current "
    return "lose_money current 10"

cards = {
    CardType.RED: [
        Card(
            type=CardType.RED,
            rarity=1,
            title="Пирог из Обломовки",
            description="Такой вкусный пирог, что не хочется уходить отсюда!\n\n"
                        "До следующего вашего хода Обломов ходит на 1 клетку меньше",
            action="slow_others 1"
        ),
        Card(
            type=CardType.RED,
            rarity=1,
            title="Луч надежды",
            description="Обломов изменился?\n\n"
                        "В следующий ваш ход Обломов ходит на 1 клетку больше",
            action="boost current 1"
        ),
        Card(
            type=CardType.RED,
            rarity=2,
            title="Расцвет любви",
            description="Обломов влюбляется в Ольгу.\n\n"
                        "В следующий ход игрока [Ольга] Обломов ходит на 2 клетки больше",
            action="boost olga 2"
        ),
        Card(
            type=CardType.RED,
            rarity=2,
            title="Старый друг",
            description="Обломов решает покушать суп со Штольцем.\n\n"
                        "В следующий ход игрока [Штольц] Обломов ходит на 2 клетки больше",
            action="boost shtoltz 2"
        ),
        Card(
            type=CardType.RED,
            rarity=2,
            title="Вымогательство",
            description="Тарантьев облапошил Обломова.\n\n"
                        "В следующий ход игрока [Тарантьев] Обломов ходит на 2 клетки больше",
            action="boost tarantiev 2"
        ),
        Card(
            type=CardType.RED,
            rarity=2,
            title="Призрак пирога",
            description="Обломов очень сильно захотел пирогов из Обломовки...\n\n"
                        "В следующий ход игрока [Обломов] Обломов ходит на 4 клетки больше",
            action="boost oblomov 2"
        ),
        Card(
            type=CardType.RED,
            rarity=3,
            title="Бьется сердце!",
            description="Обломов собирает волю в кулак и решает действовать.\n\n"
                        "Следующий ход становится ходом игрока [Обломов]",
            action="turn oblomov"
        ),
        Card(
            type=CardType.RED,
            rarity=3,
            title="Послеобеденный сон",
            description="Что-то спать захотелась… *зевает*\n\n"
                        "До следующего вашего хода Обломов ходит на 3 клетки меньше.",
            action="slow_others"
        ),
        Card(
            type=CardType.RED,
            rarity=4,
            title="Договор Тарантьева",
            description="Не стоит такое подписывать\n\n"
                        "Следующий игрок пропускает ход (кроме игрока [Обломов])",
            action="skip"
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
            rarity=1,
            title="Схема обмана",
            description="Вам в руки попали записки Тарантьева. Возможно удача благоволит вам...\n\n"
                        "Вы пытаетесь украсть деньги у следующего игрока."
                        "С вероятностью 50% вы преуспеваете и получаете 1/10 его сумму(или 2 монеты, если у игрока нет таких средств)."
                        "В случае провала вы теряете 10 монет. Если следующий игрок - [Штольц], вы теряете 10 монет.",
            action=blue_2
        ),
        Card(
            type=CardType.BLUE,
            rarity=2,
            title="Доход",
            description="Конечно не 5 тысяч в месяц, но тоже ничего...\n\n"
                        "Вы получаете 5 монет",
            action="get_money 5"
        ),
        Card(
            type=CardType.BLUE,
            rarity=2,
            title="Щедрая душа",
            description="Подарите улыбки людям!\n\n"
                        "Игрок с самым высоким балансом передает 10 монет(или половину своего состояния, если у него меньше 20 монет) игроку с самым маленьким балансом",
            action=blue_3
        ),
        Card(
            type=CardType.BLUE,
            rarity=3,
            title="Пора встать с дивана",
            description="Пока Илья Ильич встает, жизнь вовсю несется. Кому же повезет поймать удачу за хвост?\n\n"
                        "Каждый игрок бросает кубик дважды."
                        "Тот, кто выкинет наибольшую сумму, получает 10 монет и забирает 1/10 от баланса каждого игрока",
            action=blya_pizda_sochuvstvuyu
        ),
        Card(
            type=CardType.BLUE,
            rarity=3,
            title="Игра стоит свеч?",
            description="Вам в руки попали секретные методы ведения бизнеса Штольца…\n\n"
                        "Игрок получает 20 монет."
                        "Если следующий игрок - [Тарантьев], то игрок передает ему 10 монет, если [Штольц] - оба игрока получают 5 дополнительных монет, если [Ольга] - то игрок передает 5 монет игроку [Обломов]."
                        "Если следующий игрок - [Обломов], то игрок ничего никому не передает.",
            action=zdelat_legche
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
        ),
        Card(
            type=CardType.WHITE,
            rarity=2,
            title="Зарядка",
            description="Правильный, вкусный и сбалансированный обед.\n\nОбломов проживет на 5 ходов дольше",
            action="heal 5"
        ),
        Card(
            type=CardType.WHITE,
            rarity=2,
            title="Панацея",
            description="Говорят, исцеляет все болезни\n\nОбломов проживет на 15 ходов дольше",
            action="heal 15"
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
