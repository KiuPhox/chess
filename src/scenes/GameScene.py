from constants.AssetPath import ImagePath

from engine.GameObject import GameObject
from engine.components.Sprite import Sprite

from objects.Board import Board
from scenes.Scene import Scene

from objects.Background import Background


class GameScene(Scene):
    def __init__(self, screen):
        super().__init__("GameScene", screen)

    def start(self):
        self.create_background()
        self.create_board()

    def create_background(self):
        self.bg = Background(self)

    def create_board(self):
        self.board = Board(self)
