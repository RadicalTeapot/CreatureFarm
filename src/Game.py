# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature

from activity.Adventure import AdventureTemplate
from Enemy import EnemyTemplate
from Mutation import MutationTemplate

from activity.Adventure import Adventure
from activity.Cook import Cook
from activity.Feed import Feed
from activity.Fight import Fight

from ObjectManager import ObjectManager
from Settings import Settings

import json
import os

from collections import namedtuple

Knowledge = namedtuple('Knowledge', 'base_cost current_level')


class GameModel:
    """Store data of Game."""

    genetic_material = 0

    creatures = {}
    creature_templates = {}

    adventure_templates = {}
    enemy_templates = {}
    mutation_templates = {}
    knowledge = {}

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
    def __init__(self):
        self._parse_adventures()
        self._parse_enemies()
        self._parse_mutations()
        self._parse_knowledge()

    def _parse_adventures(self):
        with open("src/data/adventures.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            GameModel.adventure_templates[id_] = (
                AdventureTemplate.from_data(id_, data)
            )

    def _parse_enemies(self):
        with open("src/data/enemies.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            GameModel.enemy_templates[id_] = (
                EnemyTemplate.from_data(id_, data)
            )

    def _parse_mutations(self):
        with open("src/data/mutations.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            GameModel.mutation_templates[id_] = (
                MutationTemplate.from_data(id_, data)
            )

    def _parse_knowledge(self):
        with open("src/data/knowledge.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            GameModel.knowledge[id_] = Knowledge(data, 0.)

    def update(self):
        for creature in self.creatures:
            creature.update()
        self.date += 1
        ObjectManager.ui.refresh()

    def has_knowledge(self, knowledge_id):
        if knowledge_id not in self.knowledge:
            raise KeyError('Knowledge {} not found'.format(knowledge_id))
        return (
            self.knowledge[knowledge_id].current_level >=
            self.knowledge[knowledge_id].base_cost
        )

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
