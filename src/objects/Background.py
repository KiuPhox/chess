from constants.AssetPath import ImagePath

from engine.GameObject import GameObject
from engine.components.Sprite import Sprite


class Background(GameObject):
    def __init__(self, scene):
        super().__init__(scene)

        self.name = "Background"
        self.scale = (10, 6)

        self.sprite = Sprite(self)
        self.sprite.color = (48, 46, 43)
        self.sprite.set_sprite(ImagePath.SQUARE)

        self.add_component(self.sprite)
