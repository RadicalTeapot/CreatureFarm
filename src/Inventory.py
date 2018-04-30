# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Constants import BODY_PART
from Constants import ITEM_CATEGORY


class Item(object):
    def __init__(self):
        self.id = -1
        self.name = None
        self.quantity = 0
        self.category = None
        self.description = ''

    # ####################################################################### #
    #                                  Food                                   #
    # ####################################################################### #

    def get_description(self):
        description = (
            'Name: {name}\n'
            'Quantity: {quantity}\n'
        ).format(name=self.name, quantity=self.quantity)

        return description


class FoodItem(Item):
    def __init__(self):
        super().__init__()
        self.category = ITEM_CATEGORY.FOOD
        self.is_raw = True
        self.nutrition_value = 1

    def eat(self):
        return self.nutrition_value

    def get_description(self):
        description = super().get_description()
        description += (
            '\n'
            'Raw: {raw}\n'
            'Nutrition value: {nutrition}\n'
        ).format(
            raw=self.is_raw,
            nutrition=self.nutrition_value
        )

        return description


class ArmorItem(Item):
    def __init__(self):
        super().__init__()
        self.category = ITEM_CATEGORY.ARMOR
        self.body_part = None
        self.modified_stats = {}
        self.equiped = None

    def get_description(self):
        description = super().get_description()

        equiped = ''
        if self.equiped:
            equiped = '\nEquiped to: {}\n'.format(self.equiped.name)

        stat_changes = []
        for stat, value in self.modified_stats.items():
            stat_changes.append('  {}: {}'.format(
                stat.name.title().replace('_', ' '),
                value
            ))
        stat_changes.sort()

        description += (
            '\n'
            'Body part: {}\n'
            'Stat changes:\n{}\n'
            '{}'
        ).format(
            self.body_part.name.title().replace('_', ' '),
            '\n'.join(stat_changes),
            equiped
        )

        return description


class WeaponItem(Item):
    def __init__(self):
        super().__init__()
        self.category = ITEM_CATEGORY.WEAPON
        self.body_part = BODY_PART.HAND
        self.types = set()
        self.modified_stats = {}
        self.equiped = None

    def get_description(self):
        description = super().get_description()

        equiped = ''
        if self.equiped:
            equiped = '\nEquiped to: {}\n'.format(self.equiped.name)

        stat_changes = []
        for stat, value in self.modified_stats.items():
            stat_changes.append('  {}: {}'.format(
                stat.name.title().replace('_', ' '),
                value
            ))
        stat_changes.sort()

        description += (
            '\n'
            'Types: {}\n'
            'Stat changes:\n{}\n'
            '{}'
        ).format(
            ', '.join([
                weapon_type.name.title().replace('_', ' ')
                for weapon_type in self.types
            ]),
            '\n'.join(stat_changes),
            equiped
        )

        return description


class Recipe(object):
    def __init__(self):
        self.name = None
        self.game = None
        self.ingredients = {}
        self.results = {}
        self.duration = 3
        self.complexity = 0
        self._categories = set()
        self.description = ''

    def is_available(self, creature):
        return True

    def get_description(self):
        return (
            'Ingredients :\n'
            '{ingredients}\n'
            '\n'
            'Results :\n'
            '{results}\n'
            '\n'
            'Difficulty : {complexity}\n'
            '\n'
            '{description}'
        ).format(
            ingredients='\n'.join([
                '{}x {}'.format(
                    quantity, self.game.inventory.get_item(item).name
                )
                for item, quantity in self.ingredients.items()
            ]),
            results='\n'.join([
                '{}x {}'.format(
                    quantity, self.game.inventory.get_item(item).name
                )
                for item, quantity in self.results.items()
            ]),
            complexity=self.complexity,
            description=self.description
        )


class Inventory(object):
    def __init__(self):
        self.items = {}
        self.recipes = {}

    def add_item(self, item):
        if item.id in self.items:
            self.items[item.id].quantity += item.quantity
            return
        self.items[item.id] = item

    def add_items(self, ingredients):
        for item_id, quantity in ingredients.items():
            self.items[item_id].quantity += quantity

    def take_items(self, ingredients):
        for item_id, quantity in ingredients.items():
            self.items[item_id].quantity -= quantity

    def has_item(self, item_id, quantity=0):
        return (
            item_id in self.items and
            self.items[item_id].quantity >= quantity
        )

    def has_items(self, ingredients):
        return all([
            self.has_item(item_id, quantity)
            for item_id, quantity in ingredients.items()
        ])

    def get_item(self, item_id):
        return self.items[item_id]

    def get_items(self, category=None, empty=False):
        items = []
        if category is None:
            items = [item for item in self.items.values()]
        else:
            items = [
                item
                for item in self.items.values()
                if item.category == category
            ]
        if not empty:
            items = [item for item in items if item.quantity > 0]
        return sorted(items, key=lambda item: item.name)

    def add_recipe(self, recipe):
        self.recipes[recipe.id] = recipe

    def get_recipes(self, category=None):
        if category is None:
            recipes = [recipe for recipe in self.recipes.values()]
        else:
            recipes = [
                recipe
                for recipe in self.recipes.values()
                if recipe.has_category(category)
            ]
        return sorted(
            recipes,
            key=lambda recipe: recipe.name
        )

    def get_recipe(self, recipe_id):
        return self.recipes[recipe_id]
