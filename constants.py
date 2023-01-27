from enum import Enum
from pathlib import Path

from pygame import Color
from pygame.image import load
from pygame.font import Font, init as init_font

init_font()


WIDTH = 800
HEIGHT = 800
FPS = 60

BORDER = 100
FIELD_SIZE = 15  # in cells
CELL_SIZE = (WIDTH - BORDER * 2) // FIELD_SIZE
CENTRAL_CELL = (FIELD_SIZE // 2, FIELD_SIZE // 2)

OBSTACLE_COUNT = 30
MIN_AIM_DISTANCE = 6  # from Oblomov and from other aims
MIN_AIM_SPREAD = 5  # between each other

ANIMATION_SPEED = 4

MAX_STEPS = 6
TOTAL_MOVES = 99

TARGET_REACHED_REWARD = 50


class Colors:
    empty = Color("#00000000")

    wrong = Color("#0000ff")

    background = Color("#444444")

    empty_cell = Color("#888888")

    stats = Color("#888888")
    stats_current = Color("#dddddd")

    moves = Color("#dddddd")

    gold = Color("#ffd700")
    silver = Color("#c0c0c0")
    bronze = Color("#cd7f32")


class Images:
    images_dir = Path("assets", "images")

    oblomov = load(Path(images_dir, "oblomov.png"))


class Fonts:
    fonts_dir = Path("assets", "fonts")

    stats = Font(Path(fonts_dir, "inter.ttf"), 32)
    moves = Font(Path(fonts_dir, "inter.ttf"), 48)


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


class DirectionType(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    UNKNOWN = 0  # should not occur

    def __str__(self) -> str:
        return self.name


place_to_color = [
    Colors.gold,
    Colors.silver,
    Colors.bronze,
    Colors.stats
]
