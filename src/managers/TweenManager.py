from engine.GameObject import GameObject
from managers.EaseManager import Ease, EaseManager
from utils.Time import Time

from typing import Tuple


class Tween:
    def __init__(
        self, game_object: GameObject, scale: Tuple[float, float], duration: float
    ) -> None:
        self.game_object = game_object
        self.ease = Ease.LINEAR
        self.duration = duration

        self.start_scale = self.game_object.scale
        self.end_scale = scale

        self.start_time = Time.time

        self.on_complete_callback = None

        TweenManager.tweens.append(self)

    def set_ease(self, ease: Ease):
        self.ease = ease

    def on_complete(self, callback):
        self.on_complete_callback = callback

    def update(self):
        elapsed = Time.time - self.start_time
        t = min(elapsed / self.duration, 1)

        xScale = self.start_scale[0] + EaseManager.ease_func(self.ease, t) * (
            self.end_scale[0] - self.start_scale[0]
        )

        yScale = self.start_scale[1] + EaseManager.ease_func(self.ease, t) * (
            self.end_scale[1] - self.start_scale[1]
        )

        self.game_object.scale = (xScale, yScale)

        if t == 1:
            if self.on_complete_callback:
                self.on_complete_callback()
            self.destroy()

    def destroy(self):
        TweenManager.tweens.remove(self)


class TweenManager:
    tweens: Tween = []

    @staticmethod
    def init():
        TweenManager.tweens = []

    @staticmethod
    def update():
        for tween in TweenManager.tweens:
            tween.update()
