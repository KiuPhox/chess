class BoardHelper:
    @staticmethod
    def file_index(square_index: int) -> int:
        return square_index & 0b000111
