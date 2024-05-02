import pygame

from constants.AssetPath import FontPath, ImagePath
from constants.SortingOrder import SortingOrder

from engine.Button import Button
from engine.components.Sprite import Sprite


class Piece(Button):
    def __init__(self, scene):
        super().__init__(scene, ImagePath.WHITE_PAWN)

        self.name = "Piece"
        self.scale = (0.4, 0.4)
        self.label.font = pygame.font.Font(FontPath.TT_FORS, 20)

        self.set_type(PieceType.PAWN | PieceType.WHITE)
        self.sprite.set_order(SortingOrder.PIECE)

    def get_color(self):
        return self.type & 24

    def get_type(self):
        return self.type & 7

    def set_type(self, type: int):
        self.type = type

        color = "WHITE" if self.get_color() == PieceType.WHITE else "BLACK"
        piece_type = {
            PieceType.KING: "KING",
            PieceType.PAWN: "PAWN",
            PieceType.KNIGHT: "KNIGHT",
            PieceType.BISHOP: "BISHOP",
            PieceType.ROOK: "ROOK",
            PieceType.QUEEN: "QUEEN",
        }.get(self.get_type(), "")

        image_name = f"{color}_{piece_type}"
        self.sprite.set_sprite(ImagePath.__dict__[image_name])

    def is_team(self, piece: "Piece") -> bool:
        return self.get_color() == piece.get_color()


class PieceType:
    NONE = 0
    KING = 1
    PAWN = 2
    KNIGHT = 3
    BISHOP = 4
    ROOK = 5
    QUEEN = 6

    WHITE = 8
    BLACK = 16
