from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from engine.Button import Button
    from engine.components.Text import Text


class UIManager:
    buttons: List["Button"] = []
    texts: List["Text"] = []

    @staticmethod
    def init():
        UIManager.buttons = []
        UIManager.texts = []

    @staticmethod
    def register_button(button):
        UIManager.buttons.append(button)

    @staticmethod
    def unregister_button(button):
        UIManager.buttons.remove(button)

    @staticmethod
    def register_text(text):
        UIManager.texts.append(text)

    @staticmethod
    def unregister_text(text):
        UIManager.texts.remove(text)
