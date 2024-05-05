from constants.AssetPath import ImagePath

from constants.SortingOrder import SortingOrder
from engine.Button import Button

from objects.Piece import PieceType


class PromotionPiece(Button):
    def __init__(self, scene, type: PieceType):
        super().__init__(scene, ImagePath.WHITE_QUEEN)

        self.name = "PromotionPiece"
        self.sprite.set_order(SortingOrder.PROMOTION_PIECE)

        self.set_type(type)

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
