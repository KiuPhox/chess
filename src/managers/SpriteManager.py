from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from engine.components.Sprite import Sprite


class SpriteManager:
    sprites: List["Sprite"] = []

    @staticmethod
    def init():
        SpriteManager.sprites = []

    @staticmethod
    def register_sprite(sprite):
        SpriteManager.sprites.append(sprite)
        SpriteManager.sort()

    @staticmethod
    def unregister_sprite(sprite):
        SpriteManager.sprites.remove(sprite)
        SpriteManager.sort()

    @staticmethod
    def sort():
        SpriteManager.sprites.sort(key=lambda x: x.order)
