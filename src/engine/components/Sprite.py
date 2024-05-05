import pygame

from constants.SortingOrder import SortingOrder

from engine.components.Component import Component
from engine.GameObject import GameObject

from managers.SpriteManager import SpriteManager


class Sprite(Component):
    def __init__(self, gameObject: GameObject):
        super().__init__(gameObject)

        self.name = "Sprite"
        self.image = None
        self.color = (255, 255, 255)
        self.order = SortingOrder.DEFAULT
        self.opacity = 255

        self.flip = (False, False)

        SpriteManager.register_sprite(self)

    def set_sprite(self, path: str):
        self.image = pygame.image.load(path)

    def set_order(self, order: int):
        self.order = order

        SpriteManager.unregister_sprite(self)
        SpriteManager.register_sprite(self)

    def width(self):
        return self.image.get_width() * self.game_object.scale[0]

    def height(self):
        return self.image.get_height() * self.game_object.scale[1]

    def destroy(self):
        SpriteManager.unregister_sprite(self)
        super().destroy()
