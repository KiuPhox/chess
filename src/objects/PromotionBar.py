from typing import TYPE_CHECKING

from constants.AssetPath import ImagePath
from constants.SortingOrder import SortingOrder

from engine.Button import Button
from engine.GameObject import GameObject
from engine.components.Sprite import Sprite

if TYPE_CHECKING:
    from objects.Board import Board

from objects.Move import Move
from objects.Square import Square
from objects.Piece import PieceType
from objects.PromotionPiece import PromotionPiece


class PromotionBar(GameObject):
    def __init__(self, scene, board: "Board" = None):
        super().__init__(scene)

        self.name = "PromotionBar"
        self.position = (0, 0)
        self.scale = (1, 1)

        self.board = board
        self.move: Move = None

        self.sprite = Sprite(self)
        self.sprite.set_sprite(ImagePath.PROMOTION_BAR)
        self.sprite.set_order(SortingOrder.PROMOTION_BAR)
        self.add_component(self.sprite)

        self.create_promotion_pieces()
        self.create_close_button()

    def create_promotion_pieces(self):
        self.queen = PromotionPiece(self.scene, PieceType.QUEEN | PieceType.WHITE)
        self.knight = PromotionPiece(self.scene, PieceType.KNIGHT | PieceType.WHITE)
        self.rook = PromotionPiece(self.scene, PieceType.ROOK | PieceType.WHITE)
        self.bishop = PromotionPiece(self.scene, PieceType.BISHOP | PieceType.WHITE)

        self.queen.left_up_callback = (self.on_promotion_piece_click, [self.queen], {})
        self.knight.left_up_callback = (
            self.on_promotion_piece_click,
            [self.knight],
            {},
        )
        self.rook.left_up_callback = (self.on_promotion_piece_click, [self.rook], {})
        self.bishop.left_up_callback = (
            self.on_promotion_piece_click,
            [self.bishop],
            {},
        )

    def create_close_button(self):
        self.close_button = Button(self.scene, ImagePath.CLOSE_ICON)
        self.close_button.name = "CloseButton"

        self.close_button.sprite.set_order(SortingOrder.PROMOTION_PIECE)
        self.close_button.sprite.color = (139, 137, 135)

        self.close_button.left_up_callback = (self.on_close_button_click, [], {})

    def set_position_from_square(self, square: Square):
        direction = 1 if self.board.color_to_move == PieceType.WHITE else -1

        self.sprite.flip = (
            False,
            False if self.board.color_to_move == PieceType.WHITE else True,
        )

        self.position = (square.position[0] + 25, -150 * direction)
        self.queen.position = square.position
        self.knight.position = (
            square.position[0],
            square.position[1] + 100 * direction,
        )
        self.rook.position = (square.position[0], square.position[1] + 200 * direction)
        self.bishop.position = (
            square.position[0],
            square.position[1] + 300 * direction,
        )
        self.close_button.position = (
            square.position[0],
            square.position[1] + 375 * direction,
        )

    def set_active(self, active: bool):
        self.active = active
        self.queen.active = active
        self.knight.active = active
        self.rook.active = active
        self.bishop.active = active
        self.close_button.active = active

        if active:
            color_type = (
                PieceType.WHITE
                if self.board.color_to_move == PieceType.WHITE
                else PieceType.BLACK
            )

            self.queen.set_type(PieceType.QUEEN | color_type)
            self.knight.set_type(PieceType.KNIGHT | color_type)
            self.rook.set_type(PieceType.ROOK | color_type)
            self.bishop.set_type(PieceType.BISHOP | color_type)

    def open(self, move: Move):
        self.move = move
        self.set_position_from_square(
            self.board.squares[move.get_target_square_index()]
        )
        self.set_active(True)

    def on_promotion_piece_click(self, piece: PromotionPiece):
        start_square = self.board.squares[self.move.get_start_square_index()]
        target_square = self.board.squares[self.move.get_target_square_index()]
        promotion_flag = {
            self.queen: Move.PROMOTE_TO_QUEEN,
            self.knight: Move.PROMOTE_TO_KNIGHT,
            self.rook: Move.PROMOTE_TO_ROOK,
            self.bishop: Move.PROMOTE_TO_BISHOP,
        }.get(piece)

        move = Move.from_square_and_flag(start_square, target_square, promotion_flag)

        self.board.make_move(move)

        self.set_active(False)

    def on_close_button_click(self):
        self.set_active(False)

        start_square = self.board.squares[self.move.get_start_square_index()]
        move = Move.from_square(start_square, start_square)

        self.board.make_move(move)
