from constants.SortingOrder import SortingOrder

from managers.InputManager import InputManager
from objects.Move import Move
from objects.Piece import Piece, PieceType
from objects.Square import Square

LIGHT_COLOR = (234, 236, 209)
DARK_COLOR = (120, 149, 88)
SQUARE_SIZE = 64

FEN_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


class Board:
    def __init__(self, scene):
        self.scene = scene
        self.board = [PieceType.NONE] * 64

        self.squares: list[Square] = []
        self.selected_square = None

        self.color_to_move = PieceType.WHITE

        self.decode_fen()

        self.create_squares()
        self.create_pieces()

    def create_squares(self) -> None:
        for i in range(8):
            for j in range(8):
                is_light = (i + j) % 2 == 0

                square = Square(self.scene)
                square.position = (
                    SQUARE_SIZE * ((i * 8 + j) % 8 - 3.5),
                    SQUARE_SIZE * ((i * 8 + j) // 8 - 3.5),
                )
                square.sprite.color = LIGHT_COLOR if is_light else DARK_COLOR
                square.left_click_callback = (self.on_square_click, [square], {})

                self.squares.append(square)

    def create_pieces(self) -> None:
        for i in range(64):
            if self.board[i] == PieceType.NONE:
                continue

            piece = Piece(self.scene)
            piece.position = self.squares[i].position
            piece.set_type(self.board[i])

            self.squares[i].piece = piece

    def update(self) -> None:
        if self.selected_square is None:
            return

        self.selected_square.piece.position = InputManager.get_mouse_position()

    def on_square_click(self, square: Square) -> None:
        if self.selected_square is None:
            piece = square.piece

            if piece is None:
                return

            if piece.get_color() != self.color_to_move:
                return

            square.piece.sprite.set_order(SortingOrder.SELECTED_PIECE)
            self.selected_square = square
            return

        start_square = self.selected_square
        end_square = square

        move = Move(start_square, end_square)

        self.make_move(move)

    def make_move(self, move: Move) -> None:
        start_square = move.start_square
        end_square = move.end_square

        selected_piece = start_square.piece

        if end_square == start_square:
            selected_piece.position = end_square.position
            selected_piece.sprite.set_order(SortingOrder.PIECE)
            self.selected_square = None
            return

        if end_square.has_piece() and end_square.piece.is_team(selected_piece):
            return

        if end_square.has_piece() and not end_square.piece.is_team(selected_piece):
            end_square.piece.active = False
            end_square.piece = None

        end_square.piece = selected_piece
        start_square.piece = None

        selected_piece.position = end_square.position
        selected_piece.sprite.set_order(SortingOrder.PIECE)

        self.selected_square = None
        self.change_turn()

    def change_turn(self) -> None:
        self.color_to_move = (
            PieceType.WHITE
            if self.color_to_move == PieceType.BLACK
            else PieceType.BLACK
        )

    def decode_fen(self, fen=FEN_START) -> str:
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

                self.board[i + j] = piece_type | piece_color
                i += 1

    def encode_fen(self) -> str:
        fen = ""

        for i in range(8):
            empty = 0
            for j in range(8):
                piece = self.board[i * 8 + j]

                if piece == PieceType.NONE:
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0

                    piece_type = {
                        PieceType.KING: "k",
                        PieceType.PAWN: "p",
                        PieceType.KNIGHT: "n",
                        PieceType.BISHOP: "b",
                        PieceType.ROOK: "r",
                        PieceType.QUEEN: "q",
                    }.get(piece & 7, "")

                    piece_color = "K" if piece & PieceType.WHITE else "k"

                    fen += (
                        piece_color
                        if piece_type == ""
                        else (
                            piece_type.upper()
                            if piece & PieceType.WHITE
                            else piece_type
                        )
                    )

            if empty > 0:
                fen += str(empty)

            if i < 7:
                fen += "/"

        return fen

    def update_board(self) -> None:
        for i in range(64):
            self.board[i] = (
                self.squares[i].piece.type
                if self.squares[i].has_piece()
                else PieceType.NONE
            )
