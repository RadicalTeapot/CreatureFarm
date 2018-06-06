# -*- coding: utf-8 -*-
"""DOCSTRING."""

from enum import Enum

from ObjectManager import ObjectManager
from ui.screen import UiState


class MainMenuButtons(Enum):
    NEW = 0
    LOAD = 1
    SETTINGS = 2
    EXIT = 3


class MainMenu(UiState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def callback(self, action):
        if action == MainMenuButtons.NEW:
            ObjectManager.game.new_game()
        elif action == MainMenuButtons.LOAD:
            ObjectManager.game.load()
        elif action == MainMenuButtons.SETTINGS:
            ObjectManager.game.settings()
        elif ObjectManager == MainMenuButtons.EXIT:
            ObjectManager.game.exit()
