import pygame


class InputManager:
    currentMouseState = [False, False, False]
    previousMouseState = [False, False, False]

    @staticmethod
    def update():
        InputManager.previousMouseState = InputManager.currentMouseState
        InputManager.currentMouseState = pygame.mouse.get_pressed()

    @staticmethod
    def get_mouse(input: int):
        return InputManager.currentMouseState[input]

    @staticmethod
    def get_mouse_down(input: int):
        return (
            InputManager.currentMouseState[input]
            and not InputManager.previousMouseState[input]
        )

    @staticmethod
    def get_mouse_up(input: int):
        return (
            not InputManager.currentMouseState[input]
            and InputManager.previousMouseState[input]
        )

    @staticmethod
    def get_mouse_position():
        return pygame.mouse.get_pos()
