from engine.components.Component import Component

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scenes.Scene import Scene


class GameObject:
    def __init__(self, scene: "Scene"):
        self.name = ""
        self.components: dict[str, Component] = {}
        self.active = True

        self.scene = scene
        self.scene.register_game_object(self)

        self.position = (0, 0)
        self.scale = (1, 1)

    def update(self):
        for component in self.components.values():
            component.update()

    def add_component(self, component: Component):
        if component.name in self.components:
            return

        self.components[component.name] = component

    def get_component(self, name: str):
        return self.components[name]

    def destroy(self):
        for component in self.components.values():
            component.destroy()

        self.active = False
