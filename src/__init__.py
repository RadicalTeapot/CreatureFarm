# -*- coding: utf-8 -*-
"""DOCSTRING."""

import os
# Disable kivy reading flag args from cli
os.environ["KIVY_NO_ARGS"] = "1"

from ObjectManager import ObjectManager
from Game import Game
from ui import Ui
from Settings import Settings

import sys

if __name__ == '__main__':
    object_manager = ObjectManager()

    object_manager.add_object('game', Game())
    ObjectManager.game._model.biomass = 100

    object_manager.add_object('ui', Ui())

    save_file = None
    if len(sys.argv) > 1:
        if Settings.SAVE_FLAG in sys.argv:
            name = sys.argv[sys.argv.index(Settings.SAVE_FLAG) + 1]
            ObjectManager.game.load(os.path.join(Settings.SAVE_FOLDER, name))

    ObjectManager.ui.run()
