from constants.AssetPath import ImagePath

from constants.SortingOrder import SortingOrder

from engine.GameObject import GameObject
from engine.components.Sprite import Sprite


class SquareFrame(GameObject):
    def __init__(self, scene):
        super().__init__(scene)

        self.name = "SquareFrame"
        self.scale = (0.5, 0.5)

        sprite = Sprite(self)
        sprite.color = (100, 100, 100)
        sprite.opacity = 100
        sprite.set_sprite(ImagePath.SQUARE_FRAME)
        sprite.set_order(SortingOrder.SQUARE_FRAME)

        self.add_component(sprite)
