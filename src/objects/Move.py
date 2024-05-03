from objects.Square import Square


class Move:
    def __init__(self, start_square: Square, end_square: Square):
        self.start_square = start_square
        self.target_square = end_square

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Move):
            return False

        return (
            self.start_square == value.start_square
            and self.target_square == value.target_square
        )
