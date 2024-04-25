from constants.AssetPath import ImagePath

from engine.GameObject import GameObject
from engine.components.Sprite import Sprite

from scenes.Scene import Scene

from objects.Background import Background


class MenuScene(Scene):
    def __init__(self, screen):
        super().__init__("MenuScene", screen)

    def start(self):
        self.create_background()

    def create_background(self):
        self.bg = Background(self)
