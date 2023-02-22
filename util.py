from random import randint, choice

from cards import Card, CardType, cards_for_choice
from constants import MAX_DESCRIPTION_LINE_LENGTH


def random_cell(field_size: int) -> tuple[int, int]:
    return randint(0, field_size - 1), randint(0, field_size - 1)


def random_aim_cell(field_size: int, min_distance: int) -> tuple[int, int]:
    result = random_cell(field_size)

    while cell_distance((field_size // 2,) * 2, result) < min_distance:
        result = random_cell(field_size)

    return result


def cell_distance(cell1: tuple[int, int], cell2: tuple[int, int]) -> int:
    return max(abs(cell1[0] - cell2[0]), abs(cell1[1] - cell2[1]))


def get_card(type: CardType) -> Card:
    return choice(cards_for_choice[type])


def split_card_description(string: str) -> list[str]:
    result = []

    while len(string) > MAX_DESCRIPTION_LINE_LENGTH or "\n" in string:
        max_slice = string[:MAX_DESCRIPTION_LINE_LENGTH + 1]  # +1 in case the space/newline is the next symbol
        index = max_slice.index("\n") if "\n" in max_slice else max_slice.rindex(" ")
        result.append(string[:index])
        string = string[index + 1:]

    result.append(string)

    return result
