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
        self._categories = set()
        self._components = []

    def has_category(self, category):
        return category in self._categories

    # ####################################################################### #
    #                                  Food                                   #
    # ####################################################################### #

    def add_food_component(self, is_raw=True, nutrition_level=1):
        self._categories.add(self.CATEGORY.FOOD)
        component = FoodComponent(self)
        component.is_raw = is_raw
        component.nutrition_level = nutrition_level
        self._components.append(component)

    def cook(self):
        if self.CATEGORY.FOOD in self._categories:
            components = [
                component
                for component in self._components
                if isinstance(component, FoodComponent)
            ]
            for component in components:
                return component.cook()

    def eat(self):
        if self.CATEGORY.FOOD in self._categories:
            components = [
                component
                for component in self._components
                if isinstance(component, FoodComponent)
            ]
            for component in components:
                return component.eat()

    def get_description(self):
        description = (
            'Name: {name}\n'
            'Quantity: {quantity}\n'
        ).format(name=self.name, quantity=self.quantity)

        if self.CATEGORY.FOOD in self._categories:
            components = [
                component
                for component in self._components
                if isinstance(component, FoodComponent)
            ]
            for component in components:
                description += (
                    '\n'
                    'Raw: {raw}\n'
                    'Nutrition value: {nutrition}\n'
                ).format(
                    raw=component.is_raw,
                    nutrition=component.nutrition_level
                )

        return description


class FoodComponent(object):
    def __init__(self, item):
        self.item = item
        self.is_raw = True
        self.nutrition_level = 1

    def eat(self):
        return self.nutrition_level

    def cook(self):
        if not self.is_raw:
            return False
        return True


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
            if item.has_category(category)
        ]
