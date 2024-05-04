from objects.Piece import PieceType


class BoardState:
    def __init__(self, captured_piece_type: PieceType, en_passant_file: int) -> None:
        self.captured_piece_type = captured_piece_type
        self.en_passant_file = en_passant_file
