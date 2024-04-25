from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.GameObject import GameObject


class Component:
    def __init__(self, game_object: "GameObject"):
        self.name = ""
        self.game_object = game_object

    def update(self):
        pass

    def destroy(self):
        pass
