import pygame
from sys import exit

from engine.Screen import Screen
from managers.GameStatsManager import GameStatsManager
from utils.Time import Time

from constants.GameConfig import GameConfig, ScreenConfig
from constants.AssetPath import *

from scenes.GameScene import GameScene
from scenes.MenuScene import MenuScene

from managers.TweenManager import TweenManager
from managers.SceneManager import SceneManager
from managers.InputManager import InputManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chess")

        self.screen = Screen(ScreenConfig.WIDTH, ScreenConfig.HEIGHT)
        self.clock = pygame.time.Clock()

        pygame.display.set_icon(pygame.image.load(ImagePath.GAME_LOGO))

        self.init_game_stats_manager()
        self.init_tween_manager()
        self.init_scene_manager()

    def init_game_stats_manager(self):
        GameStatsManager.init(self.clock)

    def init_tween_manager(self):
        TweenManager.init()

    def init_scene_manager(self):
        GameScene(self.screen)
        MenuScene(self.screen)

        SceneManager.change_scene("GameScene")

    def render(self):
        SceneManager.update()
        self.screen.render()
        pygame.display.update()

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            InputManager.update()
            TweenManager.update()

            self.render()

            Time.deltaTime = self.clock.tick(GameConfig.FPS) / 1000
            Time.time = pygame.time.get_ticks() / 1000


game = Game()
game.update()
