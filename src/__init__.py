# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ObjectManager import ObjectManager
from Game import Game
from ui import Ui


if __name__ == '__main__':
    object_manager = ObjectManager()
    object_manager.add_object('game', Game())
    object_manager.add_object('ui', Ui())

    ObjectManager.ui.run()
