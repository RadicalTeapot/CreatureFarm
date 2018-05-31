# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature

from ObjectManager import ObjectManager
from Game import Game
from ui import Ui


if __name__ == '__main__':
    object_manager = ObjectManager()
    object_manager.add_object('game', Game())
    object_manager.add_object('ui', Ui())

    ObjectManager.game.add_creature(Creature('RadicalTeapot'))

    # Add a sword and chestplate
    ObjectManager.game.inventory.add_items({
        'items.armor.chestplate': 1,
        'items.weapon.sword': 1,
        'items.utility.backpack': 1
    })

    ObjectManager.ui.run()
