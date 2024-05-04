import pygame

from typing import Tuple

from constants.AssetPath import FontPath, ImagePath
from constants.SortingOrder import SortingOrder

from engine.Button import Button
from engine.GameObject import GameObject
from engine.components.Sprite import Sprite

from objects.Piece import Piece


class Square(Button):
    def __init__(self, scene):
        super().__init__(scene, ImagePath.SQUARE)

        self.name = "Square"
        self.scale = (0.5, 0.5)

        self.label.font = pygame.font.Font(FontPath.TT_FORS, 80)
        self.label.color = (200, 200, 200)

        self.piece: Piece = None
        self.index = 0

        self.sprite.set_order(SortingOrder.SQUARE)

        self.create_legal_point()
        self.create_capture_circle()

    def create_legal_point(self) -> None:
        self.legal_point = GameObject(self.scene)
        self.legal_point.name = "Point"
        self.legal_point.scale = (0.5, 0.5)

        point_sprite = Sprite(self.legal_point)
        point_sprite.set_sprite(ImagePath.LEGAL_POINT)
        point_sprite.set_order(SortingOrder.SQUARE_HIGHLIGHT)
        point_sprite.color = (100, 100, 100)
        point_sprite.opacity = 100

        self.legal_point.add_component(point_sprite)
        self.legal_point.active = False

    def create_capture_circle(self) -> None:
        self.capture_circle = GameObject(self.scene)
        self.capture_circle.name = "CapturePoint"
        self.capture_circle.scale = (0.5, 0.5)

        circle_sprite = Sprite(self.capture_circle)
        circle_sprite.set_sprite(ImagePath.CAPTURE_CIRCLE)
        circle_sprite.set_order(SortingOrder.SQUARE_HIGHLIGHT)
        circle_sprite.color = (100, 100, 100)
        circle_sprite.opacity = 100

        self.capture_circle.add_component(circle_sprite)
        self.capture_circle.active = False

    def has_piece(self) -> bool:
        return self.piece is not None
