from random import randint


def random_cell(total: int) -> tuple[int, int]:
    return randint(0, total - 1), randint(0, total - 1)


def random_aim_cell(total: int, min_distance: int) -> tuple[int, int]:
    result = random_cell(total)

    while cell_distance((total // 2,) * 2, result) < min_distance:
        result = random_cell(total)

    return result


def cell_distance(cell1: tuple[int, int], cell2: tuple[int, int]) -> int:
    return max(abs(cell1[0] - cell2[0]), abs(cell1[1] - cell2[1]))
