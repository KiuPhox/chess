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
        self.cells = []

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
                self.cells.append(Cell(square))

    def create_pieces(self) -> None:
        for i in range(64):
            if self.board[i] == PieceType.NONE:
                continue

            piece = Piece(self.scene)
            piece.position = self.cells[i].square.position
            piece.set_type(self.board[i])

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


class Cell:
    def __init__(self, square: Square, piece: Piece = None):
        self.square = square
        self.piece = piece
