import pygame


class GameStatsManager:
    @staticmethod
    def init(clock: pygame.time.Clock):
        GameStatsManager.clock = clock

    @staticmethod
    def get_fps() -> float:
        return GameStatsManager.clock.get_fps()
