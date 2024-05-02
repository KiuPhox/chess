from managers.InputManager import InputManager
from objects.Piece import Piece, PieceType
from objects.Square import Square

LIGHT_COLOR = (234, 236, 209)
DARK_COLOR = (120, 149, 88)
SQUARE_SIZE = 64

FEN_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


class Cell:
    def __init__(self, square: Square, piece: Piece = None):
        self.square = square
        self.piece = piece

    def has_piece(self) -> bool:
        return self.piece is not None


class Board:
    def __init__(self, scene):
        self.scene = scene
        self.board = [PieceType.NONE] * 64
        self.cells: list[Cell] = []
        self.selected_piece = None

        self.decode_fen()

        self.create_square()
        self.create_pieces()

    def create_square(self) -> None:
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

                self.cells.append(Cell(square))

    def create_pieces(self) -> None:
        for i in range(64):
            if self.board[i] == PieceType.NONE:
                continue

            piece = Piece(self.scene)
            piece.position = self.cells[i].square.position
            piece.set_type(self.board[i])
            piece.left_click_callback = (self.on_piece_click, [piece], {})

            self.cells[i].piece = piece

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

    def update(self) -> None:
        if self.selected_piece is None:
            return

        self.selected_piece.position = InputManager.get_mouse_position()

    def on_piece_click(self, piece: Piece) -> None:
        if self.selected_piece is not None:
            return

        self.selected_piece = piece

        self.set_pieces_interactable(False)

    def on_square_click(self, square: Square) -> None:
        if self.selected_piece is None:
            return

        start_cell = self.get_cell_base_on_piece(self.selected_piece)
        end_cell = self.get_cell_base_on_square(square)

        if end_cell == start_cell:
            self.selected_piece.position = square.position
            self.selected_piece = None
            self.set_pieces_interactable(True)
            return

        if end_cell.has_piece() and end_cell.piece.is_team(self.selected_piece):
            return

        if end_cell.has_piece() and not end_cell.piece.is_team(self.selected_piece):
            end_cell.piece.active = False
            end_cell.piece = None

        start_cell.piece = None
        end_cell.piece = self.selected_piece

        self.selected_piece.position = square.position
        self.selected_piece = None
        self.set_pieces_interactable(True)

    def get_cell_base_on_piece(self, piece: Piece) -> Cell:
        return next(filter(lambda cell: cell.piece == piece, self.cells))

    def get_cell_base_on_square(self, square: Square) -> Cell:
        return next(filter(lambda cell: cell.square == square, self.cells))

    def set_pieces_interactable(self, interactable: bool) -> None:
        for cell in self.cells:
            if cell.has_piece():
                cell.piece.interactable = interactable

    def update_board(self) -> None:
        for i in range(64):
            self.board[i] = (
                self.cells[i].piece.type
                if self.cells[i].has_piece()
                else PieceType.NONE
            )
