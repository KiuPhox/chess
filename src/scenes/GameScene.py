from objects.Board import Board
from scenes.Scene import Scene


class GameScene(Scene):
    def __init__(self, screen):
        super().__init__("GameScene", screen)

    def start(self):
        self.create_board()

    def create_board(self):
        self.board = Board(self)

    def update(self):
        self.board.update()
        return super().update()
