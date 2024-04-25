from constants.AssetPath import ImagePath

from engine.GameObject import GameObject
from engine.components.Sprite import Sprite


class Square(GameObject):
    def __init__(self, scene):
        super().__init__(scene)

        self.name = "Square"
        self.scale = (0.5, 0.5)

        self.sprite = Sprite(self)
        self.sprite.set_sprite(ImagePath.SQUARE)

        self.add_component(self.sprite)
