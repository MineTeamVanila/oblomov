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

MAX_DESCRIPTION_LINE_LENGTH = 40


class Colors:
    empty = Color("#00000000")

    wrong = Color("#0000ff")

    background = Color("#444444")

    text_white = Color("#dddddd")
    text_bright_white = Color("#f0f0f0")
    text_gray = Color("#888888")
    text_red = Color("#fc2847")  # Скарлет
    text_blue = Color("#1fcecb")  # Яиц странствующего дрозда

    empty_cell = Color("#888888")

    stats = text_gray
    stats_current = text_white

    moves = text_white
    moves_red = text_red

    card_title_movement = text_red
    card_title_economics = text_blue
    card_title_life = text_bright_white
    card_description = text_white
    card_rarity = text_white

    gold = Color("#ffd700")
    silver = Color("#c0c0c0")
    bronze = Color("#cd7f32")

    card_bg_fade = Color("#000000aa")


class Images:
    images_dir = Path("assets", "images")

    oblomov = load(Path(images_dir, "oblomov.png"))


class Fonts:
    fonts_dir = Path("assets", "fonts")

    stats = Font(Path(fonts_dir, "inter.ttf"), 32)
    moves = Font(Path(fonts_dir, "inter.ttf"), 48)

    card_title = Font(Path(fonts_dir, "inter.ttf"), 56)
    card_description = Font(Path(fonts_dir, "inter.ttf"), 24)
    card_rarity = Font(Path(fonts_dir, "inter.ttf"), 32)


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


class Money:
    target_reached_reward = 50

    oblomov_income = 1
    shtoltz_income = 3
    olga_income = 2
    tarantiev_stealth_amount = {
        PlayerType.OBLOMOV: 4,
        PlayerType.SHTOLTZ: 0,
        PlayerType.OLGA: 2
    }


place_to_color = [
    Colors.gold,
    Colors.silver,
    Colors.bronze,
    Colors.stats
]

player_order = (
    PlayerType.OBLOMOV,
    PlayerType.SHTOLTZ,
    PlayerType.OLGA,
    PlayerType.TARANTIEV
)
