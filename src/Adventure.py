# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random

from ObjectManager import ObjectManager
from Creature import Creature
from Logger import Logger


class AdventureTemplate:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.enemies = {}
        self.biomass_pool = 0.
        self.biomass_regen_speed = 0.

    @classmethod
    def from_data(cls, data):
        cls.validate_data(data)

        instance = cls()
        instance.name = data['name']
        instance.description = data['description']

        for enemy in data.get('enemies', []):
            instance.add_enemy(enemy['enemy'], enemy['chance'])

        instance.biomass_pool = data['biomass_pool']
        instance.biomass_regen_speed = data['biomass_regen_speed']

        return instance

    @staticmethod
    def validate_data(data):
        attributes = [
            "name", "enemies", "biomass_pool",
            "biomass_regen_speed", "description"
        ]
        for attribute in attributes:
            if attribute not in data:
                raise KeyError('Missing {} attribute'.format(attribute))
        # TODO check enemies validity as well

    def add_enemy(self, enemy_id, chance):
        self.enemies[enemy_id] = chance

    def add_reward(self, item_id, chance):
        self.rewards[item_id] = chance

    def is_available(self, creature):
        return True

    def get_description(self):
        return 'Adventure description placeholder'


class Adventure:
    def __init__(self, creatures, group_name, template_name):
        self.template_name = template_name
        self.creatures = creatures
        self.group_name = group_name
        # TODO Pass a unique name to the logger identifying this adventure
        # template_name + group_name is not enough as the player
        # may send the same creature/group to the same adventure multiple
        # times
        self.log = Logger(f'{self.template_name}_{self.group_name}')

    def start(self):
        self.logger.add_entry(
            ObjectManager.game.date,
            '{} started adventure {}'.format(
                self.group_name, self.template_name
            ),
            'adventure',
            'info'
        )

    def update(self):
        template = ObjectManager.game.get_adventures[self.template_name]

        for enemy_id, chance in template.enemies.items():
            if random.random() < chance:
                ObjectManager.game.fight(self.creatures, enemy_id)
                return

        # Take from adventure and add it to creatures container

        # TODO Check if all creatures dead -> stop adventure
        # TODO Check if all creature biomass containers full -> stop adventure

    def end(self):
        pass

    def serialize(self):
        data = {}
        data['template_name'] = self.template_name
        data['creatures'] = [
            creature.serialize() for creature in self.creatures
        ]
        data['group_name'] = self.group_name
        data['log'] = self.log.serialize()

        return data

    @classmethod
    def deserialize(cls, data):
        instance = cls([], '', '')
        instance.template_name = data['template_name']
        instance.group_name = data['group_name']
        instance.creatures = [
            Creature.deserialize(creature_data)
            for creature_data in data['creatures']
        ]
        instance.logger = Logger.deserialize(data.['log'])
        return instance
