# -*- coding: utf-8 -*-
"""DOCSTRING."""

import math
import random
import copy


class EnemyTemplate:
    def __init__(self):
        # TODO Use Constant stats
        self.name = None
        self.level = None
        self.description = None
        self.loot = {}

        self.max_hp = None
        self.hp = None
        self.strength = None
        self.armor = None
        self.agility = None

    @classmethod
    def from_data(cls, id, data):
        cls.validate_data(data)
        instance = cls()
        instance.id = 'enemies.{}'.format(id)
        instance.name = data['name']
        instance.description = data['description']
        instance.max_hp = data['hp']
        instance.hp = data['hp']
        instance.strength = data['strength']
        instance.armor = data['armor']
        instance.agility = data['agility']
        for loot in data['loot']:
            instance.loot[loot['item']] = (loot['quantity'], loot['curve'])

        return instance

    @staticmethod
    def validate_data(data):
        attributes = [
            "name", "hp", "strength", "armor", "agility", "description"
        ]
        for attribute in attributes:
            if attribute not in data:
                raise KeyError('Missing {} attribute'.format(attribute))
        # TODO: Check loot validity as well


class Enemy(object):
    def __init__(self):
        # TODO Use Constant stats
        self.name = None
        self.level = None
        self.description = None
        self.loot = {}

        self._max_hp = None
        self._hp = None
        self._strength = None
        self._armor = None
        self._agility = None

    def get_loot(self):
        rewards = {}
        for item_id, data in self.loot.items():
            # TODO: use creature stats to modify curve value
            quantity_range, curve = data
            # Remap curve for [0, 1] to [1.5, -0.5]
            curve = min(max(curve, 0.), 1.0)
            curve = (1 - curve) * 2 - 0.5
            # Sigmoid curve
            # for curve = 0.5 -> .1: .008, .5: .5, 1.: 0.998
            quantity = 1 / (1 + math.exp(-12 * (random.random() - curve)))
            # Remap quantity from [0, 1] to quantity range
            quantity *= (quantity_range[1] - quantity_range[0])
            quantity += quantity_range[0]
            quantity = round(quantity)

            if quantity > 0:
                rewards[item_id] = int(quantity)

        return rewards

    def serialize(self):
        data = {}
        data['name'] = self.name
        data['level'] = self.level
        data['desciption'] = self.description
        data['loot'] = copy.deepcopy(self.loot)
        data['max_hp'] = self._max_hp
        data['hp'] = self._hp
        data['strength'] = self._strength
        data['armor'] = self._armor
        data['agility'] = self._agility

        return data

    def deserialize(self, data):
        self.name = data['name']
        self.level = data['level']
        self.description = data['description']
        self.loot = copy.deepcopy(data['loot'])
        self._max_hp = data['max_hp']
        self._hp = data['hp']
        self._strength = data['strength']
        self._armor = data['armor']
        self._agility = data['agility']

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self._max_hp = value

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self._hp = value

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self._strength = value

    @property
    def armor(self):
        return self._armor

    @armor.setter
    def armor(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self._armor = value

    @property
    def agility(self):
        return self._agility

    @agility.setter
    def agility(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self._agility = value
