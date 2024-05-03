from typing import TYPE_CHECKING, List
import bisect

if TYPE_CHECKING:
    from engine.components.Sprite import Sprite


class SpriteManager:
    sprites: List["Sprite"] = []

    @staticmethod
    def init():
        SpriteManager.sprites = []

    @staticmethod
    def register_sprite(sprite):
        index = bisect.bisect_left(
            [sprite.order for sprite in SpriteManager.sprites], sprite.order
        )
        SpriteManager.sprites.insert(index, sprite)

    @staticmethod
    def unregister_sprite(sprite):
        SpriteManager.sprites.remove(sprite)
