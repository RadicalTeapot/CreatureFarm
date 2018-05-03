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
    EQUIP = None


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
    EQUIP = 7


class ITEM_CATEGORY(Enum):
    FOOD = 'Food'
    WEAPON = 'Weapon'
    ARMOR = 'Armor'
    UTILITY = 'Utility'


class ACTIVITY_TYPE(Enum):
    ADVENTURE = 'on an adventure'
    COOK = 'cooking'
    FEED = 'eating'
    FIGHT = 'in a fight'


class BODY_PART(Enum):
    CHEST = 0
    HEAD = 1
    ARMS = 2
    LEGS = 3

    UTILITY_CHEST = 4
    UTILITY_HEAD = 5
    UTILITY_ARMS = 6
    UTILITY_LEGS = 7

    HAND = 8
    OFF_HAND = 9


class WEAPON_TYPE(Enum):
    ONE_HANDED = 0
    TWO_HANDED = 1
    MELEE = 2
    RANGED = 3

    SWORD = 10
    DAGGER = 11
    CLUB = 12

    BOW = 20
    CROSSBOW = 21
    GUN = 22

    SHIELD = 30


class STATS(Enum):
    HP = 0
    MAX_HP = 1

    STRENGTH = 2
    MELEE = 3
    MARKSMANSHIP = 4

    EVASION = 5
    ARMOR = 6

    COOKING = 7
    BUILDING = 8

    INVENTORY_SIZE = 9
