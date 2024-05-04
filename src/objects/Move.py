from objects.Square import Square


class Move:

    NONE = 0b0000
    EN_PASSANT = 0b0001
    CASTLE = 0b0010
    PAWN_TWO_FORWARD = 0b0011

    PROMOTE_TO_QUEEN = 0b0100
    PROMOTE_TO_KNIGHT = 0b0101
    PROMOTE_TO_ROOK = 0b0110
    PROMOTE_TO_BISHOP = 0b0111

    START_SQUARE_MASK = 0b0000000000111111
    TARGET_SQUARE_MASK = 0b0000111111000000
    FLAG_MASK = 0b1111000000000000

    def __init__(self, move_value: int) -> None:
        self.move_value = move_value

    @classmethod
    def from_square(cls, start_square: Square, target_square: Square) -> "Move":
        move_value = start_square.index | target_square.index << 6
        return cls(move_value)

    @classmethod
    def from_square_and_flag(
        cls, start_square: Square, target_square: Square, flag: int
    ) -> "Move":
        move_value = start_square.index | target_square.index << 6 | flag << 12
        return cls(move_value)

    @classmethod
    def null_move(cls) -> "Move":
        return cls(0)

    def get_start_square_index(self) -> int:
        return self.move_value & Move.START_SQUARE_MASK

    def get_target_square_index(self) -> int:
        return (self.move_value & Move.TARGET_SQUARE_MASK) >> 6

    def get_move_flag(self) -> int:
        return self.move_value >> 12

    def is_promotion(self) -> bool:
        return self.get_move_flag() >= Move.PROMOTE_TO_QUEEN

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Move):
            return False

        return self.move_value == value.move_value
