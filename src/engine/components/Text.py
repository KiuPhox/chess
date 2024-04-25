from pygame.font import Font

from engine.GameObject import GameObject
from engine.components.Component import Component

from managers.UIManager import UIManager


class Text(Component):
    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self.name = "Text"
        self.text = ""
        self.font: Font = None
        self.color = (0, 0, 0)
        self.align = TextAlign.CENTER

        UIManager.register_text(self)

    def destroy(self):
        UIManager.unregister_text(self)
        return super().destroy()


class TextAlign:
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
