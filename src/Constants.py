# -*- coding: utf-8 -*-
"""DOCSTRING."""

from collections import namedtuple

ACTIVITY_TYPE = namedtuple('activity_type', [
    'ADVENTURE', 'COOK', 'FEED'
])(
    'on an adventure', 'cooking', 'eating'
)

ENTRY_TYPE = namedtuple('type', [
    'INFO',
    'IMPORTANT',
    'CRITICAL'
])

UI_STATE = namedtuple('state', [
    'CREATURE', 'NEW_ADVENTURE', 'CURRENT_ADVENTURE', 'INVENTORY',
    'COOK', 'FEED'
])

UI_BUTTON = namedtuple('buttons', [
    'CREATURE', 'START_ADVENTURE', 'CURRENT_ADVENTURE', 'FINISH_TURN',
    'INVENTORY', 'COOK', 'FEED'
])(0, 1, 2, 3, 4, 5, 6)

ITEM_CATEGORY = namedtuple('category', [
    'FOOD', 'WEAPON', 'ARMOR'
])(
    'Food', 'Weapon', 'Armor'
)
