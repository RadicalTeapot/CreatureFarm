# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random

from ObjectManager import ObjectManager
from Creature import Creature
from Enemy import Enemy
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

        self.update = self.update_regular
        self.enemies = []
        self._in_fight = False

    def start(self):
        self.logger.add_entry(
            ObjectManager.game.date,
            '{} started adventure {}'.format(
                self.group_name, self.template_name
            ),
            'adventure',
            'info'
        )

    def update_regular(self):
        template = ObjectManager.game.get_adventures[self.template_name]

        for enemy_id, chance in template.enemies.items():
            if random.random() < chance:
                self.enemies.append(Enemy(enemy_id))
        if self.enemies:
            self.in_fight = True
            return

        # Extract some biomass from the adventure pool
        size = sum(creature.stats['size'] for creature in self.creatures)
        # Use the group size to get the amount of biomass extracted
        extracted_biomass = min(size * .1, template.biomass_pool)
        total_biomass = extracted_biomass
        # Fill each creature in order
        for creature in self.creatures:
            if not creature.is_full():
                extracted_biomass -= creature.add_biomass(extracted_biomass)
        # Remove the extracted biomass from the adventure pool
        template.biomass_pool -= (total_biomass - extracted_biomass)

        if all(creature.is_full() for creature in self.creatures):
            return ObjectManager.game.end_adventure(self)

    @property
    def in_fight(self):
        return self._in_fight

    @in_fight.setter
    def in_fight(self, value):
        if not isinstance(value, bool):
            raise TypeError('Expected bool, got {} instead'.format(
                type(value).__name__
            ))
        self._in_fight = value

        self.update = (
            self.update_regular
            if self._in_fight
            else self.update_fight
        )

    def update_fight(self):
        if all(creature.is_dead() for creature in self.creatures):
            return ObjectManager.game.end_adventure(self)

        # TODO Improve fight system
        for enemy in self.enemies:
            # Get live creatures
            creatures = [
                creature
                for creature in self.creatures
                if not creature.is_dead()
            ]
            attack = sum(creature.stat['attack'] for creature in creatures)

            enemy.hp -= attack
            if enemy.hp <= 0:
                # TODO Add knowledge of dead enemy to creatures
                continue

            creature = random.choice(creatures)
            creature.stat['hp'] -= creature.strength
        # Clear dead enemies from the list
        self.enemies = [enemy for enemy in self.enemies if enemy.hp > 0]

        if not self.enemies:
            self.in_fight = False

    def serialize(self):
        data = {}
        data['template_name'] = self.template_name
        data['creatures'] = [
            creature.serialize() for creature in self.creatures
        ]
        data['group_name'] = self.group_name
        data['log'] = self.log.serialize()
        data['in_fight'] = self.in_fight
        # TODO Serialize enemies
        data['enemies'] = []

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
        instance.logger = Logger.deserialize(data['log'])
        instance.in_fight = data['in_fight']
        return instance
