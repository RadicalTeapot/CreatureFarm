# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Inventory import Inventory
from Inventory import Item
from Inventory import ArmorItem
from Inventory import FoodItem
from Inventory import WeaponItem
from Inventory import Recipe

from Creature import Creature
from Enemy import Enemy

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

import json


class Game(object):
    def __init__(self, window):
        self.window = window

        self.creatures = []
        self.enemies = {}
        self.adventure_templates = []
        self.inventory = Inventory()

        # Turn counter
        self.date = 0

        self._parse_data()

    def _parse_data(self):
        ids = set()
        with open("src/data/items.json", 'r') as item_data:
            ids = self._parse_items(json.loads(item_data.read()), ids)
        with open("src/data/recipes.json", 'r') as recipe_data:
            ids = self._parse_recipes(json.loads(recipe_data.read()), ids)
        with open("src/data/enemies.json", 'r') as enemy_data:
            ids = self._parse_enemies(json.loads(enemy_data.read()), ids)
        with open("src/data/adventures.json", 'r') as adventure_data:
            ids = self._parse_adventures(
                json.loads(adventure_data.read()), ids
            )

    def _parse_items(self, data, ids):
        for item_id, item_data in data.items():
            item_id = 'items.{}'.format(item_id)
            self._validate_item(item_id, item_data, ids)
            item = None
            # Food
            if item_data['type'] == 'food':
                item = FoodItem()
                item.is_raw = item_data['is_raw']
                item.nutrition_value = item_data['nutrition_value']
            # Armor
            elif item_data['type'] in ['armor', 'utility']:
                item = ArmorItem()
                for body_part in BODY_PART:
                    item_part = item_data['body_part'].lower()
                    if item_data['type'] == 'utility':
                        item.category = ITEM_CATEGORY.UTILITY
                        item_part = 'utility_' + item_part
                    if item_part == body_part.name.lower():
                        item.body_part = body_part
                        break
                for stat in item_data['modified_stats']:
                    modified_stat = [
                        s
                        for s in STATS
                        if s.name.lower() == stat['type']
                    ]
                    if modified_stat:
                        item.modified_stats[modified_stat[0]] = stat['value']
            # Weapon
            elif item_data['type'] == 'weapon':
                item = WeaponItem()
                for weapon_type in WEAPON_TYPE:
                    if weapon_type.name.lower() in item_data['flags']:
                        item.types.add(weapon_type)
                for stat in item_data['modified_stats']:
                    modified_stat = [
                        s
                        for s in STATS
                        if s.name.lower() == stat['type']
                    ]
                    if modified_stat:
                        item.modified_stats[modified_stat[0]] = stat['value']
            elif item_data['type'] == 'utility':
                # TODO: implement utility item (creature should be able to
                # equip one utility item per body part on top of their armor)
                pass
            else:
                item = Item()

            item.name = item_data['name']
            item.description = item_data['description']
            item.id = item_id

            ids.add(item_id)
            self.inventory.add_item(item)
        return ids

    def _validate_item(self, item_id, item, ids):
        for attribute in ['name', 'description']:
            if attribute not in item:
                raise KeyError('Missing {} attribute'.format(attribute))
        if item_id in ids:
            raise RuntimeError('Duplicate id')
        # TODO: check components validity as well

    def _parse_recipes(self, data, ids):
        for recipe_id, recipe_data in data.items():
            recipe_id = 'recipes.{}'.format(recipe_id)
            self._validate_recipe(recipe_id, recipe_data, ids)
            recipe = Recipe()
            recipe.game = self
            recipe.id = recipe_id
            recipe.name = recipe_data['name']
            for ingredient in recipe_data['ingredients']:
                recipe.ingredients[ingredient['item']] = ingredient['quantity']
            for result in recipe_data['results']:
                recipe.results[result['item']] = result['quantity']
            recipe.complexity = recipe_data['complexity']
            recipe.duration = recipe_data['duration']
            recipe.description = recipe_data['description']
            ids.add(recipe_id)
            self.inventory.add_recipe(recipe)
        return ids

    def _validate_recipe(self, recipe_id, recipe, ids):
        attributes = [
            "name", "ingredients", "results", "complexity",
            "duration", "description"
        ]
        for attribute in attributes:
            if attribute not in recipe:
                raise KeyError('Missing {} attribute'.format(attribute))

        for ingredient in recipe['ingredients']:
            if not self.inventory.has_item(ingredient['item']):
                raise RuntimeError(
                    'Unknown item with id {} in recipe {}'.format(
                        ingredient['item'], recipe['name']
                    )
                )
        for ingredient in recipe['results']:
            if not self.inventory.has_item(ingredient['item']):
                raise RuntimeError(
                    'Unknown item with id {} in recipe {}'.format(
                        ingredient['item'], recipe['name']
                    )
                )
        if recipe_id in ids:
            raise RuntimeError('Duplicate id')

    def _parse_adventures(self, data, ids):
        for adventure_id, adventure_data in data.items():
            adventure_id = 'adventures.{}'.format(adventure_id)
            self._validate_adventure(adventure_id, adventure_data, ids)
            adventure = AdventureTemplate()
            adventure.id = adventure_id
            adventure.title = adventure_data['title']
            adventure.description = adventure_data['description']

            for enemy in adventure_data.get('enemies', []):
                adventure.add_enemy(enemy['enemy'], enemy['chance'])

            for reward in adventure_data.get('rewards', []):
                adventure.add_reward(reward['item'], reward['chance'])

            ids.add(adventure_id)
            self.add_adventure(adventure)
        return ids

    def _validate_adventure(self, adventure_id, adventure, ids):
        attributes = [
            "title", "enemies", "rewards", "description"
        ]
        for attribute in attributes:
            if attribute not in adventure:
                raise KeyError('Missing {} attribute'.format(attribute))
        if adventure_id in ids:
            raise RuntimeError('Duplicate id')
        # TODO check rewards validity as well
        # TODO check enemies validity as well

    def _parse_enemies(self, data, ids):
        for enemy_id, enemy_data in data.items():
            enemy_id = 'enemies.{}'.format(enemy_id)
            self._validate_enemy(enemy_id, enemy_data, ids)
            enemy = Enemy()
            enemy.id = enemy_id
            enemy.name = enemy_data['name']
            enemy.description = enemy_data['description']
            enemy.max_hp = enemy_data['hp']
            enemy.hp = enemy_data['hp']
            enemy.strength = enemy_data['strength']
            enemy.armor = enemy_data['armor']
            enemy.agility = enemy_data['agility']
            for loot in enemy_data['loot']:
                enemy.loot[loot['item']] = (loot['quantity'], loot['curve'])
            ids.add(enemy_id)
            self.add_enemy(enemy)
        return ids

    def _validate_enemy(self, enemy_id, enemy, ids):
        attributes = [
            "name", "hp", "strength", "armor", "agility", "description"
        ]
        for attribute in attributes:
            if attribute not in enemy:
                raise KeyError('Missing {} attribute'.format(attribute))
        if enemy_id in ids:
            raise RuntimeError('Duplicate id')
        # TODO: check loot validity as well

    def update(self):
        for creature in self.creatures:
            creature.update()
        self.date += 1
        ObjectManager.ui.refresh()

    def add_creature(self, creature):
        # TODO: Find a better id system
        creature.id = 'creature.' + creature._model.name
        self.creatures.append(creature)

    def add_adventure(self, adventure):
        self.adventure_templates.append(adventure)
        self.adventure_templates = sorted(
            self.adventure_templates, key=lambda adv: adv.title
        )

    def add_enemy(self, enemy):
        self.enemies[enemy.id] = enemy

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
