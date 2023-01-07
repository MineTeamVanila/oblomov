from enum import Enum


class CellType(Enum):
    EMPTY = 0
    OBSTACLE = 1
    OBLOMOVKA = 2
    SHTOLTZ = 3
    OLGA = 4
    TARANTIEV = 5

    def __str__(self) -> str:
        return self.name


WIDTH = 950
HEIGHT = 950
FPS = 60

BORDER = 100
FIELD_SIZE = 15  # in cells
CELL_SIZE = (WIDTH - BORDER * 2) // FIELD_SIZE

OBSTACLE_COUNT = 30

MIN_AIM_DISTANCE = 6
