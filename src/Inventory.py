# -*- coding: utf-8 -*-
"""DOCSTRING."""

from collections import namedtuple


class Item(object):
    CATEGORY = namedtuple('category', [
        'FOOD',
        'WEAPON',
        'ARMOR'
    ])('Food', 'Weapon', 'Armor')

    def __init__(self):
        self.name = None
        self.quantity = None
        self.category = None


class Inventory(object):
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        if item.name in self.items:
            self.items[item.name].quantity += item.quantity
            return
        self.items[item.name] = item

    def get_items(self, category=None):
        if category is None:
            return self.items.values()
        return [
            item
            for item in self.items.values()
            if item.category == category
        ]
