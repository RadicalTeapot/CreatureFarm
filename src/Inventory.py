# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Constants import ITEM_CATEGORY


class Item(object):
    def __init__(self, item_id):
        self.id = item_id
        self.name = None
        self.quantity = 0
        self._categories = set()
        self._components = []
        self.description = ''

    def has_category(self, category):
        return category in self._categories

    # ####################################################################### #
    #                                  Food                                   #
    # ####################################################################### #

    def add_food_component(self, is_raw=True, nutrition_value=1):
        self._categories.add(ITEM_CATEGORY.FOOD)
        component = FoodComponent(self)
        component.is_raw = is_raw
        component.nutrition_value = nutrition_value
        self._components.append(component)

    def cook(self):
        if ITEM_CATEGORY.FOOD in self._categories:
            components = [
                component
                for component in self._components
                if isinstance(component, FoodComponent)
            ]
            for component in components:
                return component.cook()

    def eat(self):
        if ITEM_CATEGORY.FOOD in self._categories:
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

        if ITEM_CATEGORY.FOOD in self._categories:
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
                    nutrition=component.nutrition_value
                )

        description += '\n{}'.format(self.description)
        return description


class FoodComponent(object):
    def __init__(self, item):
        self.item = item
        self.is_raw = True
        self.nutrition_value = 1

    def eat(self):
        return self.nutrition_value

    def cook(self):
        if not self.is_raw:
            return False
        return True


class Recipe(object):
    def __init__(self):
        self.name = None
        self.ingredients = []
        self.results = []
        self.duration = 3
        self._categories = set()
        self.description = ''

    def is_available(self, creature):
        return True

    def get_description(self):
        return self.description


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
        for item_id, quantity in ingredients:
            self.items[item_id].quantity += quantity

    def take_items(self, ingredients):
        for item_id, quantity in ingredients:
            self.items[item_id].quantity -= quantity

    def has_items(self, ingredients):
        return all([
            item_id in self.items and self.items[item_id].quantity >= quantity
            for item_id, quantity in ingredients
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
                if item.has_category(category)
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
