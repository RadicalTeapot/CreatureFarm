# -*- coding: utf-8 -*-
"""DOCSTRING."""

from enum import Enum


# ########################################################################### #
#                                     UI                                      #
# ########################################################################### #

class UI_STATE(object):
    CREATURE = None
    NEW_ADVENTURE = None
    CURRENT_ADVENTURE = None
    INVENTORY = None
    COOK = None
    FEED = None
    EQUIP = None


class UI_BUTTON(Enum):
    CREATURE = 0
    START_ADVENTURE = 1
    CURRENT_ADVENTURE = 2
    FINISH_TURN = 3
    INVENTORY = 4
    COOK = 5
    FEED = 6
    EQUIP = 7
    LOAD = 8
    SAVE = 9


# ########################################################################### #
#                                   Logger                                    #
# ########################################################################### #

class ACTIVITY_TYPE(Enum):
    ADVENTURE = 'on an adventure'
    COOK = 'cooking'
    FEED = 'eating'
    FIGHT = 'in a fight'


class ENTRY_TYPE(Enum):
    INFO = 1
    IMPORTANT = 2
    CRITICAL = 3


# ########################################################################### #
#                              Creature / Enemy                               #
# ########################################################################### #

class STATS(Enum):
    HP = 0

    STRENGTH = 1
    MELEE = 2
    MARKSMANSHIP = 3

    EVASION = 4
    ARMOR = 5

    BIOMASS_CONTAINER_SIZE = 6
