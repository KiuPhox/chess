from constants.AssetPath import ImagePath

from constants.SortingOrder import SortingOrder

from engine.GameObject import GameObject
from engine.components.Sprite import Sprite


class SquareFrame(GameObject):
    def __init__(self, scene):
        super().__init__(scene)

        self.name = "SquareFrame"

        sprite = Sprite(self)
        sprite.color = (255, 255, 255)
        sprite.opacity = 170
        sprite.set_sprite(ImagePath.SQUARE_FRAME)
        sprite.set_order(SortingOrder.SQUARE_FRAME)

        self.add_component(sprite)
