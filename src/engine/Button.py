from engine.GameObject import GameObject
from engine.components.Text import Text
from engine.components.Sprite import Sprite

from managers.UIManager import UIManager

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from scenes.Scene import Scene


class Button(GameObject):
    def __init__(
        self,
        scene: "Scene",
        image: str = None,
        string: str = "",
    ) -> None:
        super().__init__(scene)

        self.sprite = None

        if image is not None:
            self.sprite = Sprite(self)
            self.sprite.set_sprite(image)
            self.add_component(self.sprite)

        self.label = Text(self)
        self.label.text = string
        self.add_component(self.label)

        self.left_down_callback = None
        self.right_down_callback = None
        self.left_down_callback = None
        self.right_down_callback = None
        self.left_up_callback = None
        self.right_up_callback = None
        self.on_enter_callback = None
        self.on_exit_callback = None

        self.touch_zone_size = (0, 0)
        self.on_mouse_enter = False
        self.interactable = True

        UIManager.register_button(self)

    def update(self):
        super().update()
        self.label.position = self.position

    def on_left_down(self) -> None:
        if self.left_down_callback is not None:
            function, args, kwargs = self.left_down_callback
            function(*args, **kwargs)

    def on_right_down(self) -> None:
        if self.right_down_callback is not None:
            function, args, kwargs = self.right_down_callback
            function(*args, **kwargs)

    def on_left_up(self) -> None:
        if self.left_up_callback is not None:
            function, args, kwargs = self.left_up_callback
            function(*args, **kwargs)

    def on_right_up(self) -> None:
        if self.right_up_callback is not None:
            function, args, kwargs = self.right_up_callback
            function(*args, **kwargs)

    def on_enter(self) -> None:
        if self.on_enter_callback is not None:
            function, args, kwargs = self.on_enter_callback
            function(*args, **kwargs)

    def on_exit(self) -> None:
        if self.on_exit_callback is not None:
            function, args, kwargs = self.on_exit_callback
            function(*args, **kwargs)

    def destroy(self):
        UIManager.unregister_button(self)
        super().destroy()

    def touch_zone(self) -> Tuple[float, float]:
        if self.sprite is None:
            return (
                self.position[0] - self.touch_zone_size[0] / 2,
                self.position[1] - self.touch_zone_size[1] / 2,
                self.position[0] + self.touch_zone_size[0] / 2,
                self.position[1] + self.touch_zone_size[1] / 2,
            )

        return (
            self.position[0] - self.sprite.width() / 2,
            self.position[1] - self.sprite.height() / 2,
            self.position[0] + self.sprite.width() / 2,
            self.position[1] + self.sprite.height() / 2,
        )
