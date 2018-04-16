# -*- coding: utf-8 -*-
"""DOCSTRING."""

from enum import Enum


class UI_STATE(object):
    CREATURE = None
    NEW_ADVENTURE = None
    CURRENT_ADVENTURE = None
    INVENTORY = None
    COOK = None
    FEED = None


class ENTRY_TYPE(Enum):
    INFO = 1
    IMPORTANT = 2
    CRITICAL = 3


class UI_BUTTON(Enum):
    CREATURE = 0
    START_ADVENTURE = 1
    CURRENT_ADVENTURE = 2
    FINISH_TURN = 3
    INVENTORY = 4
    COOK = 5
    FEED = 6


class ITEM_CATEGORY(Enum):
    FOOD = 'Food'
    WEAPON = 'Weapon'
    ARMOR = 'Armor'


class ACTIVITY_TYPE(Enum):
    ADVENTURE = 'on an adventure'
    COOK = 'cooking'
    FEED = 'eating'
    FIGHTING = 'in a fight'
