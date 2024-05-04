from typing import List

from constants.GameConfig import Debugger
from constants.SortingOrder import SortingOrder

from helper.BoardHelper import BoardHelper

from managers.InputManager import InputManager

from objects.Move import Move
from objects.Square import Square
from objects.BoardState import BoardState
from objects.Piece import Piece, PieceType
from objects.SquareFrame import SquareFrame
from objects.MoveGenerator import MoveGenerator

LIGHT_COLOR = (234, 236, 209)
DARK_COLOR = (120, 149, 88)
SQUARE_SIZE = 100

FEN_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# FEN_START = "r1b5/8/8/4q3/8/2Q5/8/B6R"


class Board:
    def __init__(self, scene):
        self.scene = scene
        self.selected_square = None
        self.color_to_move = PieceType.WHITE

        self.current_game_state: BoardState = BoardState(PieceType.NONE, 0)
        self.game_state_history: list[BoardState] = []

        self.create_square_frame()
        self.create_squares()
        self.create_pieces()

        self.create_move_generator()

    def create_square_frame(self) -> None:
        self.square_frame = SquareFrame(self.scene)
        self.square_frame.active = False

    def create_squares(self) -> None:
        self.squares: list[Square] = []

        for i in range(8):
            for j in range(8):
                is_light = (i + j) % 2 == 0

                square = Square(self.scene)
                square.position = (
                    SQUARE_SIZE * ((i * 8 + j) % 8 - 3.5),
                    SQUARE_SIZE * (8 - (i * 8 + j) // 8 - 4.5),
                )
                square.legal_point.position = square.position
                square.capture_circle.position = square.position

                square.sprite.color = LIGHT_COLOR if is_light else DARK_COLOR

                square.left_down_callback = (self.on_square_down, [square], {})
                square.left_up_callback = (self.on_square_up, [square], {})
                square.on_enter_callback = (self.on_square_enter, [square], {})
                square.index = len(self.squares)

                if Debugger.SHOW_BOARD_INDEXES:
                    square.label.text = str(square.index)

                self.squares.append(square)

    def create_pieces(self) -> None:
        board = self.decode_fen(FEN_START)

        for i in range(8):
            for j in range(8):
                square_index = i * 8 + j
                board_index = (7 - i) * 8 + j

                if board[board_index] == PieceType.NONE:
                    continue

                piece = Piece(self.scene)

                square = self.squares[square_index]
                square.piece = piece

                piece.position = square.position
                piece.set_type(board[board_index])

    def create_move_generator(self) -> None:
        self.mg = MoveGenerator(self)

    def update(self) -> None:
        if self.selected_square is None:
            return

        self.selected_square.piece.position = InputManager.get_mouse_position()

    def on_square_down(self, square: Square) -> None:
        if self.selected_square is not None:
            return

        piece = square.piece

        if piece is None:
            return

        if piece.get_color() != self.color_to_move:
            return

        square.piece.sprite.set_order(SortingOrder.SELECTED_PIECE)

        self.selected_square = square

        self.square_frame.active = True
        self.square_frame.position = square.position

        if Debugger.SHOW_LEGAL_MOVES:
            for s in self.squares:
                s.legal_point.active = False
                s.capture_circle.active = False

            moves = self.mg.generate_moves()
            for move in moves:
                start_square = self.squares[move.get_start_square_index()]
                target_square = self.squares[move.get_target_square_index()]

                if start_square != square:
                    continue

                if target_square.has_piece():
                    target_square.capture_circle.active = True
                else:
                    target_square.legal_point.active = True

    def on_square_up(self, square: Square) -> None:
        if self.selected_square is None:
            return

        start_square = self.selected_square
        target_square = square

        move = Move.from_square(start_square, target_square)

        valid_moves = self.mg.generate_moves()

        valid_move = next(
            (
                m
                for m in valid_moves
                if m.get_start_square_index() == move.get_start_square_index()
                and m.get_target_square_index() == move.get_target_square_index()
            ),
            None,
        )

        if not valid_move:
            valid_move = Move.from_square(start_square, start_square)

        self.make_move(valid_move)
        self.selected_square = None
        self.square_frame.active = False

        if Debugger.SHOW_LEGAL_MOVES:
            for s in self.squares:
                s.legal_point.active = False
                s.capture_circle.active = False

    def on_square_enter(self, square: Square) -> None:
        if self.selected_square is None:
            return

        self.square_frame.position = square.position

    def make_move(self, move: Move) -> None:
        start_square = self.squares[move.get_start_square_index()]
        target_square = self.squares[move.get_target_square_index()]
        move_flag = move.get_move_flag()
        is_en_passant = move_flag == Move.EN_PASSANT

        captured_piece_type = PieceType.NONE

        if is_en_passant:
            captured_piece_type = PieceType.PAWN | self.color_to_move
        elif target_square.has_piece():
            captured_piece_type = target_square.piece.get_piece_type()

        new_en_passant_file = 0

        selected_piece = start_square.piece

        # Invalid move
        if target_square == start_square:
            selected_piece.position = target_square.position
            selected_piece.sprite.set_order(SortingOrder.PIECE)
            return

        # Handle captures
        if captured_piece_type != PieceType.NONE:
            capture_square = target_square

            if is_en_passant:
                capture_square = self.squares[
                    target_square.index
                    + (-8 if self.color_to_move == PieceType.WHITE else 8)
                ]

            capture_square.piece.active = False
            capture_square.piece = None

        # Pawn has moved two forwards, mark file with en-passant flag
        if move_flag == Move.PAWN_TWO_FORWARD:
            new_en_passant_file = BoardHelper.file_index(start_square.index) + 1

        target_square.piece = selected_piece
        start_square.piece = None

        selected_piece.position = target_square.position
        selected_piece.sprite.set_order(SortingOrder.PIECE)

        self.current_game_state = BoardState(captured_piece_type, new_en_passant_file)
        self.game_state_history.append(self.current_game_state)

        self.change_turn()

    def change_turn(self) -> None:
        self.color_to_move = (
            PieceType.WHITE
            if self.color_to_move == PieceType.BLACK
            else PieceType.BLACK
        )

    def decode_fen(self, fen) -> List[PieceType]:
        board = [PieceType.NONE] * 64
        fen = fen.split(" ")[0]

        i = 0
        j = 0
        for c in fen:
            if c == "/":
                continue

            if c.isdigit():
                j += int(c)
            else:
                piece_type = {
                    "k": PieceType.KING,
                    "p": PieceType.PAWN,
                    "n": PieceType.KNIGHT,
                    "b": PieceType.BISHOP,
                    "r": PieceType.ROOK,
                    "q": PieceType.QUEEN,
                }.get(c.lower(), PieceType.NONE)

                piece_color = PieceType.WHITE if c.isupper() else PieceType.BLACK

                board[i + j] = piece_type | piece_color
                i += 1

        fen = ""

        return board
