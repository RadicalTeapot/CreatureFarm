# -*- coding: utf-8 -*-
"""DOCSTRING."""

import math
import random
import copy

from ObjectManager import ObjectManager


class EnemyTemplate:
    def __init__(self):
        self.id = None
        self.name = None
        self.level = None
        self.description = None
        self.knowledge = {}
        self.biomass = None

        self.hp = None
        self.strength = None
        self.armor = None
        self.agility = None

    @classmethod
    def from_data(cls, id_, data):
        cls.validate_data(data)
        instance = cls()
        instance.id = 'enemies.{}'.format(id_)
        instance.name = data['name']
        instance.description = data['description']
        instance.hp = data['hp']
        instance.strength = data['strength']
        instance.armor = data['armor']
        instance.agility = data['agility']
        instance.knowledge = copy.deepcopy(data['knowledge'])
        instance.biomass = data['biomass']

        return instance

    @staticmethod
    def validate_data(data):
        attributes = [
            "name", "hp", "strength", "armor", "agility", "description",
            "knowledge", "biomass"
        ]
        for attribute in attributes:
            if attribute not in data:
                raise KeyError('Missing {} attribute'.format(attribute))


class Enemy:
    def __init__(self, template=None):
        self.template = None
        self.hp = None
        if self.template:
            self.hp = template.hp

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
        return {'hp': self.hp, 'template': self.template.id}

    @classmethod
    def deserialize(cls, data):
        instance = cls.from_template(
            ObjectManager.game.enemy_templates.data['template']
        )
        instance.hp = data['hp']

        return instance

    @property
    def hp(self):
        return self.hp

    @hp.setter
    def hp(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self.hp = value

    @property
    def strength(self):
        assert self.template is not None
        return self.template.strength

    @property
    def armor(self):
        assert self.template is not None
        return self.template.armor

    @property
    def agility(self):
        assert self.template is not None
        return self.template.agility
