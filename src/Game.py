# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui import Ui
from Inventory import Inventory
from Inventory import Item
from Inventory import Recipe
from Adventure import Adventure
from Adventure import Reward
import Creature

from functools import partial
import json


class Game(object):
    def __init__(self, window):
        self.window = window

        self.creatures = []

        self.adventures = []

        self.inventory = Inventory()
        self.ui = Ui(self)

        # Callbacks
        self.ui.register_callback(
            self.ui.BUTTONS.FINISH_TURN, self.update
        )

        self._parse_data()

    def _parse_data(self):
        ids = []
        with open("src/data/items.json", 'r') as item_data:
            ids = self._parse_items(json.loads(item_data.read()), ids)
        with open("src/data/recipes.json", 'r') as recipe_data:
            ids = self._parse_recipes(json.loads(recipe_data.read()), ids)
        with open("src/data/adventures.json", 'r') as adventure_data:
            ids = self._parse_adventures(
                json.loads(adventure_data.read()), ids
            )

    def _parse_items(self, data, ids):
        for item_data in data.values():
            self._validate_item(item_data, ids)
            item = Item(item_data['id'])
            item.name = item_data['name']
            item.description = item_data['description']

            for component in item_data.get('components', []):
                if component['type'] == 'food':
                    item.add_food_component(
                        component['is_raw'], component['nutrition_value']
                    )
                elif component['type'] == 'armor':
                    pass
                elif component['type'] == 'weapon':
                    pass

            ids.append(item_data['id'])
            self.inventory.add_item(item)
        return ids

    def _validate_item(self, item, ids):
        for attribute in ['id', 'name', 'description']:
            if attribute not in item:
                raise KeyError('Missing {} attribute'.format(attribute))
        if item['id'] in ids:
            raise RuntimeError('Duplicate id')
        # TODO: check components validity as well

    def _parse_recipes(self, data, ids):
        for recipe_data in data.values():
            self._validate_recipe(recipe_data, ids)
            recipe = Recipe()
            recipe.id = recipe_data['id']
            recipe.name = recipe_data['name']
            recipe.ingredients = recipe_data['ingredients']
            recipe.results = recipe_data['results']
            recipe.complexity = recipe_data['complexity']
            recipe.duration = recipe_data['duration']
            recipe.description = recipe_data['description']
            self.inventory.add_recipe(recipe)
            ids.append(recipe_data['id'])
        return ids

    def _validate_recipe(self, recipe, ids):
        attributes = [
            "id", "name", "ingredients", "results", "complexity",
            "duration", "description"
        ]
        for attribute in attributes:
            if attribute not in recipe:
                raise KeyError('Missing {} attribute'.format(attribute))
        if recipe['id'] in ids:
            raise RuntimeError('Duplicate id')

    def _parse_adventures(self, data, ids):
        for adventure_data in data.values():
            self._validate_adventure(adventure_data, ids)
            adventure = Adventure()
            adventure.id = adventure_data['id']
            adventure.title = adventure_data['title']
            adventure.description = adventure_data['description']
            adventure.duration = adventure_data['duration']
            adventure.damage_range = adventure_data['damage_range']
            adventure.damage_range_curve = adventure_data['damage_range_curve']
            adventure.danger = adventure_data['danger']
            for reward in adventure_data.get('rewards', []):
                adventure.add_reward(
                    reward['item'], reward['quantity_range'], reward['curve'],
                    reward['chance']
                )
            self.add_adventure(adventure)
            ids.append(adventure_data['id'])
        return ids

    def _validate_adventure(self, adventure, ids):
        attributes = [
            "id", "title", "duration", "danger", "damage_range",
            "damage_range_curve", "rewards", "description"
        ]
        for attribute in attributes:
            if attribute not in adventure:
                raise KeyError('Missing {} attribute'.format(attribute))
        if adventure['id'] in ids:
            raise RuntimeError('Duplicate id')
        # TODO check rewards validity as well

    def get_unique_id(self):
        # HACK: This could be avoided by finding a way to store/pass pointers
        # to functions instead of values
        unique_id = 0
        ids = [creature.id for creature in self.creatures]
        ids.extend([adventure.id for adventure in self.adventures])
        ids = set(ids)
        while unique_id in ids:
            unique_id += 1
        return unique_id

    def update(self):
        for creature in self.creatures:
            creature.update()
        self.ui.refresh()

    def add_creature(self, creature):
        creature.id = self.get_unique_id()
        self.creatures.append(creature)

    def add_adventure(self, adventure):
        adventure.id = self.get_unique_id()
        self.adventures.append(adventure)

    def start_adventure(self):
        creature = self.ui._state.selected_creature
        adventure = self.ui._state.selected_adventure

        if adventure is None:
            self.ui.display_dialog('No adventure selected')
            return

        if creature is None or creature.busy:
            self.ui.display_dialog('Invalid creature selection')
            return

        creature.set_activity(
            adventure,
            Creature.ACTIVITY_TYPE.ADVENTURE,
            adventure.duration,
            update_callback=partial(
                self.update_adventure, creature, adventure
            ),
            end_callback=partial(
                self.finish_adventure, creature, adventure
            )
        )
        self.ui.refresh()

    def update_adventure(self, creature, adventure):
        adventure.update(creature)

    def finish_adventure(self, creature, adventure):
        rewards = adventure.finish()

        message = '{} just finished adventure {} !\n\nThey found:\n'.format(
            creature.name, adventure.title
        )
        for name, quantity in rewards:
            message += '    {}: {}\n'.format(name, quantity)
        self.ui.display_dialog(message)

        self.ui.refresh()

    def start_cooking(self):
        creature = self.ui._state.selected_creature
        recipe = self.ui._state.selected_recipe

        if recipe is None:
            self.ui.display_dialog('No recipe selected')
            return

        if creature is None or creature.busy:
            self.ui.display_dialog('Invalid creature selection')
            return

        if not self.inventory.has_items(recipe.ingredients):
            self.ui.display_dialog('Ingredients not available')
            return

        creature.set_activity(
            recipe,
            Creature.ACTIVITY_TYPE.COOK,
            recipe.duration,
            end_callback=partial(
                self.finish_cooking, creature, recipe
            )
        )
        self.inventory.take_items(recipe.ingredients)
        self.ui.refresh()

    def finish_cooking(self, creature, recipe):
        self.inventory.add_items(recipe.results)

        message = '{} just finished cooking !\n\nThey used:\n'.format(
            creature.name
        )

        for item_id, quantity in recipe.ingredients:
            name = self.inventory.get_item(item_id).name
            message += '    {}x {}\n'.format(quantity, name)
        message += '\nAnd produced:\n'
        for item_id, quantity in recipe.results:
            name = self.inventory.get_item(item_id).name
            message += '    {}x {}\n'.format(quantity, name)
        self.ui.display_dialog(message)

    def draw(self):
        self.window.clear()
        self.ui.draw()
