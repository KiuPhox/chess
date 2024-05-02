import pygame
from constants.AssetPath import FontPath, ImagePath

from engine.Button import Button
from engine.components.Sprite import Sprite


class Square(Button):
    def __init__(self, scene):
        super().__init__(scene, ImagePath.SQUARE)

        self.name = "Square"
        self.scale = (0.5, 0.5)
        self.label.font = pygame.font.Font(FontPath.TT_FORS, 20)
