from engine.GameObject import GameObject
from managers.SceneManager import SceneManager


class Scene:
    def __init__(self, name: str, screen):
        self.name = name
        self.screen = screen
        self.game_objects: list[GameObject] = []
        self.active = False

        # Register the scene with the SceneManager
        SceneManager.register_scene(self)

    def start(self):
        pass

    def update(self):
        for game_object in self.game_objects:
            game_object.update()

    def register_game_object(self, game_object: GameObject):
        self.game_objects.append(game_object)

    def unregister_game_object(self, game_object: GameObject):
        self.game_objects.remove(game_object)
