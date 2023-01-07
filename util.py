from random import randint


def random_cell(total: int) -> tuple[int, int]:
    return randint(0, total - 1), randint(0, total - 1)


def random_aim_cell(total: int, min_distance: int) -> tuple[int, int]:
    result = random_cell(total)

    while abs(total // 2 - result[0]) < min_distance and abs(total // 2 - result[1]) < min_distance:
        result = random_cell(total)

    return result
