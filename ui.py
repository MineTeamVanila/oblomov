import pygame
from random import randint as rnd

from constants import (
    Colors, Fonts, CellType, PlayerType, DirectionType,
    EMPTY_COLOR,
    WIDTH, BORDER, FIELD_SIZE, CELL_SIZE, CENTRAL_CELL, OBSTACLE_COUNT, MIN_AIM_DISTANCE
)

dice = 0

def roll_dice(surface):
    dice = rnd(1, 6)
    
    dice_font = Fonts.stats.render(
        str(dice),
        True,
        Colors.stats
    )

    player_surface = pygame.Surface((WIDTH / 4, BORDER), pygame.SRCALPHA)

    player_surface.blit(
        dice_font,
        dice_font.get_rect(centerx=player_surface.get_rect().centerx, y=BORDER * 1/2),
    )

    surface.blit(player_surface, (0, 0))
    return dice