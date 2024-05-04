import pygame

from constants.AssetPath import FontPath
from constants.GameConfig import ScreenConfig, Debugger

from managers.UIManager import UIManager
from managers.InputManager import InputManager
from managers.SpriteManager import SpriteManager
from managers.GameStatsManager import GameStatsManager

from engine.GameObject import GameObject
from engine.components.Text import Text, TextAlign


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

        self.create_game_stats()

    def create_game_stats(self):
        self.fps = pygame.font.Font(FontPath.TT_FORS, 20)

    def render(self):
        self.handle_input()
        self.render_sprites()
        self.render_texts()
        self.render_stats()

    def handle_input(self):
        mouse_position = InputManager.get_mouse_position()

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
                    button.on_left_down()
                    return
                elif InputManager.get_mouse_up(0):
                    button.on_left_up()
                    return
                elif InputManager.get_mouse_down(2):
                    button.on_right_down()
                    return
                elif InputManager.get_mouse_up(2):
                    button.on_right_up()
                    return

            elif button.on_mouse_enter:
                button.on_exit()
                button.on_mouse_enter = False

    def render_sprites(self):
        self.screen.fill(ScreenConfig.COLOR)

        for sprite in SpriteManager.sprites:
            game_object = sprite.game_object

            if not game_object.active:
                continue

            size = (sprite.width(), sprite.height())

            scaled_image = pygame.transform.scale(sprite.image, size)
            scaled_image.fill(sprite.color, special_flags=pygame.BLEND_RGB_MULT)
            scaled_image.set_alpha(sprite.opacity)

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

    def render_stats(self):
        if not Debugger.SHOW_GAME_STATS:
            return

        fps = GameStatsManager.get_fps()
        fps_text = self.fps.render(f"FPS: {int(fps)}", True, (255, 255, 255))

        self.screen.blit(fps_text, (10, 10))
