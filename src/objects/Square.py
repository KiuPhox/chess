import pygame

from typing import Tuple

from constants.AssetPath import FontPath, ImagePath
from constants.SortingOrder import SortingOrder

from engine.Button import Button
from objects.Piece import Piece


class Square(Button):
    def __init__(self, scene):
        super().__init__(scene, ImagePath.SQUARE)

        self.name = "Square"
        self.scale = (0.5, 0.5)

        self.label.font = pygame.font.Font(FontPath.TT_FORS, 80)
        self.label.color = (200, 200, 200)

        self.piece: Piece = None
        self.index = 0

        self.sprite.set_order(SortingOrder.SQUARE)

    def has_piece(self) -> bool:
        return self.piece is not None

    def set_color(self, color: Tuple[int, int, int]) -> None:
        self.default_color = color
        self.sprite.color = color
