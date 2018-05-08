# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature
from Enemy import EnemyTemplate

from activity.Adventure import Adventure
from activity.Adventure import AdventureTemplate
from activity.Cook import Cook
from activity.Feed import Feed
from activity.Fight import Fight

from Constants import BODY_PART
from Constants import WEAPON_TYPE
from Constants import STATS
from Constants import ITEM_CATEGORY

from ObjectManager import ObjectManager
from Settings import Settings

import json
import os


class GameModel:
    """Store data of Game."""

    genetic_material = 0
    # TODO: Convert this to per-recipe knowledge
    knowledge_points = 0

    creatures = {}
    creature_templates = {}

    mutation_templates = {}
    enemy_templates = {}
    adventure_templates = {}

    date = 0

    @classmethod
    def serialize(cls):
        """Convert data to json compatible dict."""
        raise NotImplementedError()

    @classmethod
    def deserialize(cls, data):
        """Read input data to attributes."""
        raise NotImplementedError()


class Game(object):
    def __init__(self, window):
        self.window = window

        self._parse_data()

    def _parse_data(self):
        # with open("src/data/recipes.json", 'r') as recipe_data:
        #     self._parse_recipes(json.loads(recipe_data.read()))
        with open("src/data/enemies.json", 'r') as enemy_data:
            self._parse_enemies(json.loads(enemy_data.read()))
        with open("src/data/adventures.json", 'r') as adventure_data:
            self._parse_adventures(json.loads(adventure_data.read()))

    # def _parse_recipes(self, data, ids):
    #     for recipe_id, recipe_data in data.items():
    #         recipe_id = 'recipes.{}'.format(recipe_id)
    #         self._validate_recipe(recipe_id, recipe_data, ids)
    #         recipe = Recipe()
    #         recipe.game = self
    #         recipe.id = recipe_id
    #         recipe.name = recipe_data['name']
    #         for ingredient in recipe_data['ingredients']:
    #             recipe.ingredients[ingredient['item']] = ingredient['quantity']
    #         for result in recipe_data['results']:
    #             recipe.results[result['item']] = result['quantity']
    #         recipe.complexity = recipe_data['complexity']
    #         recipe.duration = recipe_data['duration']
    #         recipe.description = recipe_data['description']
    #         ids.add(recipe_id)
    #         self.inventory.add_recipe(recipe)
    #     return ids

    # def _validate_recipe(self, recipe_id, recipe, ids):
    #     attributes = [
    #         "name", "ingredients", "results", "complexity",
    #         "duration", "description"
    #     ]
    #     for attribute in attributes:
    #         if attribute not in recipe:
    #             raise KeyError('Missing {} attribute'.format(attribute))

    #     for ingredient in recipe['ingredients']:
    #         if not self.inventory.has_item(ingredient['item']):
    #             raise RuntimeError(
    #                 'Unknown item with id {} in recipe {}'.format(
    #                     ingredient['item'], recipe['name']
    #                 )
    #             )
    #     for ingredient in recipe['results']:
    #         if not self.inventory.has_item(ingredient['item']):
    #             raise RuntimeError(
    #                 'Unknown item with id {} in recipe {}'.format(
    #                     ingredient['item'], recipe['name']
    #                 )
    #             )
    #     if recipe_id in ids:
    #         raise RuntimeError('Duplicate id')

    def _parse_adventures(self, data):
        for adventure_id, adventure_data in data.items():
            GameModel.adventure_templates[adventure_id] = (
                AdventureTemplate.from_data(adventure_id, adventure_data)
            )

    def _parse_enemies(self, data, ids):
        for enemy_id, enemy_data in data.items():
            GameModel.enemy_templates[enemy_id] = EnemyTemplate.from_data(
                enemy_id, enemy_data
            )

    def update(self):
        for creature in self.creatures:
            creature.update()
        self.date += 1
        ObjectManager.ui.refresh()

    def add_creature(self, creature):
        # TODO: Find a better id system
        creature.id = 'creature.' + creature._model.name
        self.creatures.append(creature)

    def start_adventure(self):
        creature = ObjectManager.ui._state.selected_creature
        adventure_template = ObjectManager.ui._state.selected_adventure

        if adventure_template is None:
            ObjectManager.ui.display_dialog('No adventure selected')
            return

        if creature is None or creature.busy:
            ObjectManager.ui.display_dialog('Invalid creature selection')
            return

        creature.add_activity(Adventure(creature, adventure_template))
        ObjectManager.ui.refresh()

    def start_cooking(self):
        creature = ObjectManager.ui._state.selected_creature
        recipe = ObjectManager.ui._state.selected_recipe

        if recipe is None:
            ObjectManager.ui.display_dialog('No recipe selected.')
            return

        if creature is None or creature.busy:
            ObjectManager.ui.display_dialog('Invalid creature selection.')
            return

        if creature.cooking - recipe.complexity < -1:
            ObjectManager.ui.display_dialog(
                'Cooking level too low for this recipe.'
            )
            return

        if not self.inventory.has_items(recipe.ingredients):
            ObjectManager.ui.display_dialog('Ingredients not available.')
            return

        creature.add_activity(Cook(creature, recipe))
        ObjectManager.ui.refresh()

    def start_feeding(self):
        creature = ObjectManager.ui._state.selected_creature
        item = ObjectManager.ui._state.selected_item

        if item is None:
            ObjectManager.ui.display_dialog('No food selected')
            return

        if creature is None or creature.busy:
            ObjectManager.ui.display_dialog('Invalid creature selection')
            return

        if creature.hp == creature.max_hp:
            ObjectManager.ui.display_dialog(
                '{} is already at max health'.format(creature)
            )
            return

        creature.add_activity(Feed(creature, item))
        ObjectManager.ui.refresh()

    def start_fight(self, creature, enemy_id):
        creature.add_activity(Fight(self.enemies[enemy_id], creature))

    def equip_item(self):
        creature = ObjectManager.ui._state.selected_creature
        item = ObjectManager.ui._state.selected_item

        if item is None:
            ObjectManager.ui.display_dialog('No item selected')
            return

        if creature is None or creature.busy:
            ObjectManager.ui.display_dialog('Invalid creature selection')
            return

        # TODO: Handle two handed weapons and off hand weapons
        equiped_item = creature.equipment[item.body_part]
        if equiped_item:
            equiped_item.equiped = None
        creature.equipment[item.body_part] = item
        item.equiped = creature
        ObjectManager.ui.refresh()

    def load(self, path):
        with open(path, 'r') as save_file:
            self.deserialize(json.loads(save_file.read()))

    def save(self):
        data = self.serialize()
        # print(data)
        path = os.path.normpath(os.path.join(
            os.path.abspath(Settings.SAVE_FOLDER),
            'save'
        ))
        with open(path, 'w') as save_file:
            save_file.write(json.dumps(data))

    def serialize(self):
        data = {}
        data['inventory'] = self.inventory.serialize()
        data['date'] = self.date
        data['creatures'] = [
            creature.serialize()
            for creature in self.creatures
        ]
        return data

    def deserialize(self, data):
        self.date = data['date']
        self.inventory.deserialize(data['inventory'])
        self.creatures = [
            Creature()
            for __ in data['creatures']
        ]
        for creature, creature_data in zip(self.creatures, data['creatures']):
            creature.deserialize(creature_data)

    def draw(self):
        self.window.clear()
        ObjectManager.ui.draw()
