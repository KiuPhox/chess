import pygame

from engine.components.Sprite import Sprite
from engine.GameObject import GameObject

from utils.Time import Time


class AnimationSprite(Sprite):
    def __init__(
        self, gameObject: GameObject, image_path: str, frame_count=1, frame_duration=0.1
    ):
        super().__init__(gameObject)

        self.frame_count = frame_count
        self.frame_duration = frame_duration
        self.frames = [
            pygame.image.load(f"{image_path}/{i}.png") for i in range(frame_count)
        ]

        self.image = self.frames[0]
        self.current_frame = 0
        self.frame_time = 0
        self.playing = False

    def update(self):
        if self.playing:
            self.frame_time += Time.deltaTime

            if self.frame_time >= self.frame_duration:
                self.current_frame += 1
                self.frame_time = 0

                if self.current_frame >= self.frame_count:
                    self.current_frame = self.frame_count - 1
                    self.stop()

        self.image = self.frames[self.current_frame]

    def play(self, immediately=False):
        if immediately:
            self.current_frame = self.frame_count - 1
            return

        self.current_frame = 0
        self.frame_time = 0
        self.image = self.frames[self.current_frame]

        self.playing = True

    def stop(self):
        self.playing = False
