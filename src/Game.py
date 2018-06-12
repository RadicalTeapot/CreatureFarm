# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature

from activity.Adventure import AdventureTemplate
from Enemy import EnemyTemplate
from Mutation import MutationTemplate

from ObjectManager import ObjectManager
from Settings import Settings

import json
import os

from typing import NamedTuple
from collections import OrderedDict


class Knowledge(NamedTuple):
    base_cost: float
    current_level: int


class GameModel:
    """Store data of Game."""

    biomass = 0

    creature_groups = OrderedDict()
    creature_templates = OrderedDict()

    adventure_templates = {}
    enemy_templates = {}
    mutation_templates = {}
    knowledge = {}

    running_adventures = {}

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
        with open("data/json/adventures.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            GameModel.adventure_templates[id_] = (
                AdventureTemplate.from_data(id_, data)
            )

    def _parse_enemies(self):
        with open("data/json/enemies.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            GameModel.enemy_templates[id_] = (
                EnemyTemplate.from_data(id_, data)
            )

    def _parse_mutations(self):
        with open("data/json/mutations.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            GameModel.mutation_templates[id_] = (
                MutationTemplate.from_data(id_, data)
            )

    def _parse_knowledge(self):
        with open("data/json/knowledge.json", 'r') as json_data:
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

    def get_mutations(self):
        # TODO Check for knowledge and return only available mutation
        return GameModel.mutation_templates.values()

    def get_adventures(self):
        # TODO Return only available adventures
        return GameModel.adventure_templates.values()

    def get_running_adventures(self):
        return GameModel.running_adventures

    def get_creature_templates(self):
        return GameModel.creature_templates

    def get_creature_groups(self):
        return GameModel.creature_groups

    @property
    def biomass(self):
        return GameModel.biomass

    @biomass.setter
    def biomass(self, value):
        GameModel.biomass = value
        ObjectManager.ui.update_biomass()

    def add_running_adventure(self, name, new_adventure):
        # Adventure instances are indexed by their name
        running = GameModel.running_adventures.get(name, [])
        running.append(new_adventure)
        GameModel.running_adventures[name] = running

        count = sum([
            len(adventures)
            for adventures in GameModel.running_adventures.values()
        ])
        ObjectManager.ui.update_adventure_count(count)

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
