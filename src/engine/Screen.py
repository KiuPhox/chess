import pygame

from managers.InputManager import InputManager
from managers.SpriteManager import SpriteManager
from managers.UIManager import UIManager

from engine.components.Text import TextAlign


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

    def render(self):
        self.handle_input()
        self.render_sprites()
        self.render_texts()

    def handle_input(self):
        mouse_position = InputManager.get_mouse_position()

        mouse_position = (
            mouse_position[0] - self.width / 2,
            mouse_position[1] - self.height / 2,
        )

        for button in UIManager.buttons:
            if not button.interactable:
                continue

            touch_zone = button.touch_zone()

            if (
                mouse_position[0] >= touch_zone[0]
                and mouse_position[1] >= touch_zone[1]
                and mouse_position[0] <= touch_zone[2]
                and mouse_position[1] <= touch_zone[3]
            ):
                if not button.on_mouse_enter:
                    button.on_enter()
                    button.on_mouse_enter = True

                if InputManager.get_mouse_down(0):
                    button.on_left_click()
                    return
                elif InputManager.get_mouse_down(2):
                    button.on_right_click()
                    return

            elif button.on_mouse_enter:
                button.on_exit()
                button.on_mouse_enter = False

    def render_sprites(self):
        for sprite in SpriteManager.sprites:
            game_object = sprite.game_object

            if not game_object.active:
                continue

            size = (sprite.width(), sprite.height())

            scaled_image = pygame.transform.scale(sprite.image, size)
            scaled_image.fill(sprite.color, special_flags=pygame.BLEND_RGB_MULT)

            position = (
                game_object.position[0] - sprite.width() / 2 + self.width / 2,
                game_object.position[1] - sprite.height() / 2 + self.height / 2,
            )

            self.screen.blit(scaled_image, position)

    def render_texts(self):
        for text in UIManager.texts:
            game_object = text.game_object

            if not game_object.active:
                continue

            text_surface = text.font.render(text.text, True, text.color)
            text_size = text_surface.get_size()
            size = (
                game_object.scale[0] * text_size[0],
                game_object.scale[1] * text_size[1],
            )

            scaled_text = pygame.transform.scale(text_surface, size)

            if text.align == TextAlign.LEFT:
                offset = (0, -size[1] / 2)
            elif text.align == TextAlign.CENTER:
                offset = (-size[0] / 2, -size[1] / 2)
            elif text.align == TextAlign.RIGHT:
                offset = (-size[0], -size[1] / 2)

            position = (
                game_object.position[0] + offset[0] + self.width / 2,
                game_object.position[1] + offset[1] + self.height / 2,
            )

            self.screen.blit(scaled_text, position)
