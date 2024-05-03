from objects.Square import Square


class Move:
    def __init__(self, start_square: Square, end_square: Square):
        self.start_square = start_square
        self.end_square = end_square

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Move):
            return False

        return (
            self.start_square == value.start_square
            and self.end_square == value.end_square
        )
