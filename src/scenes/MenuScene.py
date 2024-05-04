from constants.AssetPath import ImagePath

from engine.GameObject import GameObject
from engine.components.Sprite import Sprite

from scenes.Scene import Scene


class MenuScene(Scene):
    def __init__(self, screen):
        super().__init__("MenuScene", screen)

    def start(self):
        pass
