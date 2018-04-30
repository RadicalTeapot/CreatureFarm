# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Inventory import Inventory
from Inventory import Item
from Inventory import ArmorItem
from Inventory import FoodItem
from Inventory import WeaponItem
from Inventory import Recipe

from Adventure import Adventure
from Creature import Enemy

from Fight import Fight

from Constants import ACTIVITY_TYPE
from Constants import ENTRY_TYPE
from Constants import BODY_PART
from Constants import WEAPON_TYPE
from Constants import STATS
from Constants import FIGHT_OUTCOME

from ObjectManager import ObjectManager

from functools import partial
import json
import random


class Game(object):
    def __init__(self, window):
        self.window = window

        self.creatures = []
        self.enemies = {}
        self.adventures = []
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
            elif item_data['type'] == 'armor':
                item = ArmorItem()
                for body_part in BODY_PART:
                    if item_data['body_part'].lower() == body_part.name.lower():
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
            adventure = Adventure()
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
        creature.id = len(self.creatures)
        self.creatures.append(creature)

    def add_adventure(self, adventure):
        self.adventures.append(adventure)
        self.adventures = sorted(self.adventures, key=lambda adv: adv.title)

    def add_enemy(self, enemy):
        self.enemies[enemy.id] = enemy

    def start_adventure(self):
        creature = ObjectManager.ui._state.selected_creature
        adventure = ObjectManager.ui._state.selected_adventure

        if adventure is None:
            ObjectManager.ui.display_dialog('No adventure selected')
            return

        if creature is None or creature.busy:
            ObjectManager.ui.display_dialog('Invalid creature selection')
            return

        creature.set_activity(
            adventure,
            ACTIVITY_TYPE.ADVENTURE,
            -1,
            update_callback=partial(
                self.update_adventure, creature, adventure
            ),
            end_callback=partial(
                self.finish_adventure, creature, adventure
            )
        )
        adventure.start(creature, self.date)
        ObjectManager.ui.refresh()

    def update_adventure(self, creature, adventure):
        adventure.update(creature, self.date)

    def finish_adventure(self, creature, adventure):
        message = '{} just finished adventure {} !\n\nThey found:\n'.format(
            creature.name, adventure.title
        )
        for item_id, quantity in creature.inventory.items():
            message += '    {}: {}\n'.format(
                self.inventory.get_item(item_id).name,
                quantity
            )
        self.inventory.add_items(creature.inventory)
        creature.inventory.clear()

        ObjectManager.ui.display_dialog(message)
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

        creature.set_activity(
            recipe,
            ACTIVITY_TYPE.COOK,
            recipe.duration,
            end_callback=partial(
                self.finish_cooking, creature, recipe
            )
        )
        self.inventory.take_items(recipe.ingredients)
        ObjectManager.ui.refresh()

    def finish_cooking(self, creature, recipe):
        diff = creature.cooking - recipe.complexity

        failed = True
        rand = random.random()
        if diff == -1 and rand < 0.1:
            ObjectManager.ui.display_dialog = (
                '{} failed cooking {} and wasted the ingredients.'
            ).format(
                creature.name, recipe.name
            )
        elif (diff == 0 and rand < 0.1) or (diff == -1 and rand < .33):
            ObjectManager.ui.display_dialog = (
                '{} failed cooking {} but did not waste the ingredients.'
            ).format(
                creature.name, recipe.name
            )
            self.inventory.add_items(recipe.ingredients)
        else:
            message = '{} just finished cooking !\n\nThey used:\n'.format(
                creature.name
            )
            for item_id, quantity in recipe.ingredients.items():
                name = self.inventory.get_item(item_id).name
                message += '    {}x {}\n'.format(quantity, name)
            message += '\nAnd produced:\n'
            for item_id, quantity in recipe.results.items():
                name = self.inventory.get_item(item_id).name
                message += '    {}x {}\n'.format(quantity, name)
            ObjectManager.ui.display_dialog(message)

            self.inventory.add_items(recipe.results)
            failed = False

        xp_gain = 0.
        if diff == -1:  # One level above creature level
            xp_gain = 0.5  # 50 % xp gain
        elif diff == 0:  # Same level
            xp_gain = .2
        elif diff == 1:  # One level below creature level
            xp_gain = .1
        elif diff == 2:  # Two levels below creature level
            xp_gain = .05

        if failed:  # Get only a third of xp when failing
            xp_gain *= 0.33
        creature.gain_experience(STATS.COOKING, xp_gain)

        log_message = (
            "The recipe was too simple to improve {}'s cooking skills."
        ).format(creature.name)
        if xp_gain > 0.0:
            log_message = "{}'s cooking skills improved".format(creature.name)
            if xp_gain < .1:
                log_message += ' a bit.'
            elif xp_gain > 0.4:
                log_message += ' a lot.'
            else:
                log_message += '.'
        result = 'Successfully cooked {}'.format(recipe.name)
        if failed:
            result = 'Failed to cook {}'.format(recipe.name)

        creature.logger.add_entry(
            self.date,
            '{} ! {}'.format(result, log_message),
            ACTIVITY_TYPE.COOK,
            ENTRY_TYPE.INFO
        )

    def feed_creature(self):
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

        creature.set_activity(
            item,
            ACTIVITY_TYPE.FEED,
            1,
            end_callback=partial(
                self.finish_feeding, creature, item
            )
        )
        self.inventory.take_items({item.id: 1})
        ObjectManager.ui.refresh()

    def finish_feeding(self, creature, item):
        heal_amount = min(item.eat(), creature.max_hp - creature.hp)
        creature.hp = creature.hp + heal_amount

        ObjectManager.ui.display_dialog(
            '{} finished eating {}.\nThey healed for {} hp'.format(
                creature.name, item.name, heal_amount
            )
        )

    def equip_item(self):
        creature = ObjectManager.ui._state.selected_creature
        item = ObjectManager.ui._state.selected_item

        if item is None:
            ObjectManager.ui.display_dialog('No food selected')
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

    def start_fight(self, creature, enemy_id):
        fight = Fight(self.enemies[enemy_id])

        creature.logger.add_entry(
            self.date,
            '{} encountered {} !'.format(
                creature.name, fight.enemy.name
            ),
            ACTIVITY_TYPE.FIGHTING,
            ENTRY_TYPE.IMPORTANT
        )

        creature.set_activity(
            fight, ACTIVITY_TYPE.FIGHTING, -1,
            update_callback=partial(ObjectManager.game.update_fight, creature),
            end_callback=partial(
                ObjectManager.game.finish_fight, creature, fight
            )
        )

    def update_fight(self, creature):
        fight = creature.activity.activity
        fight.update(creature, self.date)

    def finish_fight(self, creature, fight):
        if fight.outcome == FIGHT_OUTCOME.WON:
            creature.logger.add_entry(
                self.date,
                '{} killed {} !'.format(creature.name, fight.enemy.name),
                ACTIVITY_TYPE.FIGHTING,
                ENTRY_TYPE.IMPORTANT
            )
            creature.add_to_inventory(fight.enemy.get_loot())
        elif fight.outcome == FIGHT_OUTCOME.LOST:
            creature.logger.add_entry(
                self.date,
                '{} fled from {} !'.format(
                    creature.name, fight.enemy.name
                ),
                ACTIVITY_TYPE.FIGHTING,
                ENTRY_TYPE.CRITICAL
            )
            # Stop all activities
            creature.free(free_all=True, ignore_callbacks=True)
            # Loose part of the inventory
            items = random.choice(creature.inventory.keys())
            for item_name in items:
                quantity = round(
                    random.random() * creature.inventory[item_name]
                )
                creature.remove_from_inventory({item_name: quantity})
        elif fight.outcome == FIGHT_OUTCOME.DRAW:
            creature.logger.add_entry(
                self.date,
                '{} gave up fighting {}.'.format(
                    creature.name, fight.enemy.name
                ),
                ACTIVITY_TYPE.FIGHTING,
                ENTRY_TYPE.CRITICAL
            )
            # Stop all activities
            creature.free(free_all=True, ignore_callbacks=True)

        del fight.enemy

    def draw(self):
        self.window.clear()
        ObjectManager.ui.draw()
