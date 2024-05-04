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

    def generate_moves(self) -> List[Move]:
        moves: list[Move] = []

        for i in range(64):
            start_square = self.board.squares[i]
            piece = start_square.piece

            if piece is not None and piece.get_color() == self.board.color_to_move:

                if piece.is_sliding():
                    moves.extend(self.generate_sliding_moves(start_square))
                if piece.get_type() == PieceType.KING:
                    moves.extend(self.generate_king_moves(start_square))
                if piece.get_type() == PieceType.KNIGHT:
                    moves.extend(self.generate_knight_moves(start_square))
                if piece.get_type() == PieceType.PAWN:
                    moves.extend(self.generate_pawn_moves(start_square))

        return moves

    def generate_king_moves(self, start_square: Square) -> List[Move]:
        moves: list[Move] = []
        piece = start_square.piece
        square_index = start_square.index

        for index in range(8):
            if NUM_SQUARES_TO_EDGE[square_index][index] == 0:
                continue

            target_index = square_index + DIRECTION_OFFSETS[index]
            target_square = self.board.squares[target_index]

            if target_square.piece is None or not piece.is_same_team(
                target_square.piece
            ):
                moves.append(Move.from_square(start_square, target_square))

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

                moves.append(Move.from_square(start_square, target_square))

                # Can't move any further in this direction after capturing opponent's piece
                if end_piece and not piece.is_same_team(end_piece):
                    break

        return moves

    def generate_knight_moves(self, start_square: Square) -> List[Move]:
        moves: list[Move] = []
        piece = start_square.piece
        square_index = start_square.index

        for index in range(4):
            if NUM_SQUARES_TO_EDGE[square_index][index] == 0:
                continue

            diagonal_indices = []
            if index == 0:
                diagonal_indices = [4, 6]
            elif index == 1:
                diagonal_indices = [5, 7]
            elif index == 2:
                diagonal_indices = [4, 7]
            else:
                diagonal_indices = [5, 6]

            for direction_index in diagonal_indices:
                direction_square_index = square_index + DIRECTION_OFFSETS[index]

                if NUM_SQUARES_TO_EDGE[direction_square_index][direction_index] == 0:
                    continue

                target_square_index = (
                    direction_square_index + DIRECTION_OFFSETS[direction_index]
                )
                target_square = self.board.squares[target_square_index]

                if target_square.piece is None or not piece.is_same_team(
                    target_square.piece
                ):
                    moves.append(Move.from_square(start_square, target_square))

        return moves

    def generate_pawn_moves(self, start_square: Square) -> List[Move]:
        moves: list[Move] = []
        piece = start_square.piece
        square_index = start_square.index

        move_direction = 1 if piece.get_color() == PieceType.WHITE else -1
        capture_directions = (
            [7, 9] if piece.get_color() == PieceType.WHITE else [-7, -9]
        )

        start_rank = 1 if piece.get_color() == PieceType.WHITE else 6
        start_rank_indices = [8 * start_rank + i for i in range(8)]

        first_move = start_rank_indices.__contains__(square_index)

        # Move single/double forward
        for index in range(2):
            target_index = square_index + 8 * move_direction * (index + 1)

            if target_index < 0 or target_index >= 64:
                break
            target_square = self.board.squares[target_index]

            if target_square.piece is not None:
                break

            if index == 0:
                moves.append(Move.from_square(start_square, target_square))
            elif first_move and index == 1:
                moves.append(
                    Move.from_square_and_flag(
                        start_square, target_square, Move.PAWN_TWO_FORWARD
                    )
                )

            if not first_move:
                break

        # Capture moves
        for direction in capture_directions:
            target_index = square_index + direction
            if target_index < 0 or target_index >= 64:
                continue
            target_square = self.board.squares[target_index]

            if target_square.piece is not None and not piece.is_same_team(
                target_square.piece
            ):
                moves.append(Move.from_square(start_square, target_square))

        # En passant
        if self.board.current_game_state.en_passant_file > 0:
            file_index = self.board.current_game_state.en_passant_file - 1
            rank_index = 4 if self.board.color_to_move == PieceType.WHITE else 3
            target_square_index = 8 * rank_index + file_index

            if (
                square_index + 1 == target_square_index
                or square_index - 1 == target_square_index
            ):
                target_square = self.board.squares[
                    target_square_index + 8 * move_direction
                ]
                moves.append(
                    Move.from_square_and_flag(
                        start_square, target_square, Move.EN_PASSANT
                    )
                )

        return moves
