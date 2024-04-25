from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from scenes.Scene import Scene


class SceneManager:
    scenes: Dict[str, "Scene"] = {}
    current_scene: "Scene" = None

    @staticmethod
    def change_scene(name: str):
        if SceneManager.current_scene is not None:
            for game_object in SceneManager.current_scene.game_objects:
                game_object.destroy()

            SceneManager.current_scene.game_objects = []

        SceneManager.current_scene = SceneManager.scenes[name]
        SceneManager.current_scene.start()

    @staticmethod
    def update():
        SceneManager.current_scene.update()

    def register_scene(scene: "Scene"):
        SceneManager.scenes[scene.name] = scene
