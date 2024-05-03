from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from objects.Board import Board

from objects.Move import Move
from objects.Square import Square
from objects.Piece import PieceType

DIRECTION_OFFSETS = [8, -8, -1, 1, 7, -7, 9, -9]
NUM_SQUARES_TO_EDGE = [[0] * 8 for _ in range(64)]


class MoveGenerator:
    def __init__(self, board: "Board"):
        self.board = board
        self.precomputed_move_data()

    def precomputed_move_data(self) -> None:
        for i in range(8):
            for j in range(8):
                num_north = 7 - i
                num_south = i
                num_west = j
                num_east = 7 - j

                square_index = i * 8 + j

                NUM_SQUARES_TO_EDGE[square_index] = [
                    num_north,
                    num_south,
                    num_west,
                    num_east,
                    min(num_north, num_west),
                    min(num_south, num_east),
                    min(num_north, num_east),
                    min(num_south, num_west),
                ]

        print(NUM_SQUARES_TO_EDGE[7])

    def generate_moves(self) -> List[Move]:
        moves: list[Move] = []

        for i in range(64):
            start_square = self.board.squares[i]
            piece = start_square.piece

            if piece is not None and piece.get_color() == self.board.color_to_move:
                if piece.is_sliding():
                    moves.extend(self.generate_sliding_moves(start_square))

        return moves

    def generate_sliding_moves(self, start_square: Square) -> List[Move]:
        moves: list[Move] = []
        piece = start_square.piece

        start_dir_index = 4 if piece.get_type() == PieceType.BISHOP else 0
        end_dir_index = 4 if piece.get_type() == PieceType.ROOK else 8

        for direction_index in range(start_dir_index, end_dir_index):
            for n in range(NUM_SQUARES_TO_EDGE[start_square.index][direction_index]):
                target_index = start_square.index + DIRECTION_OFFSETS[
                    direction_index
                ] * (n + 1)

                if target_index < 0 or target_index >= 64:
                    break
                target_square = self.board.squares[target_index]

                end_piece = target_square.piece

                # Blocked by friendly piece, so can't move any further in this direction
                if end_piece and piece.is_same_team(end_piece):
                    break

                moves.append(Move(start_square, target_square))

                # Can't move any further in this direction after capturing opponent's piece
                if end_piece and not piece.is_same_team(end_piece):
                    break

        return moves
