from enum import Enum
from pathlib import Path

from pygame.font import Font
from pygame import Color


class Colors:
    wrong = Color("#0000ff")

    background = Color("#444444")

    empty_cell = Color("#888888")

    stats = Color("#888888")
    stats_current = Color("#dddddd")


class Fonts:
    assets_dir = Path("assets")
    images_dir = Path(assets_dir, "images")
    fonts_dir = Path(assets_dir, "fonts")

    stats = Font(Path(fonts_dir, "inter.ttf"), 32)


class CellType(Enum):
    EMPTY = 0
    OBSTACLE = 1
    OBLOMOVKA = 2
    SHTOLTZ = 3
    OLGA = 4
    TARANTIEV = 5

    def __str__(self) -> str:
        return self.name


class PlayerType(Enum):
    OBLOMOV = "Обломов"
    SHTOLTZ = "Штольц"
    OLGA = "Ольга"
    TARANTIEV = "Тарантьев"

    def __str__(self) -> str:
        return self.value


WIDTH = 950
HEIGHT = 950
FPS = 60

BORDER = 100
FIELD_SIZE = 15  # in cells
CELL_SIZE = (WIDTH - BORDER * 2) // FIELD_SIZE

OBSTACLE_COUNT = 30

MIN_AIM_DISTANCE = 6

EMPTY_COLOR = Color("#00000000")
