# -*- coding: utf-8 -*-
"""DOCSTRING."""

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
    def __init__(self, template_id=None):
        self.template_id = template_id
        self._hp = None
        if self.template_id:
            self.hp = ObjectManager.game.enemies[self.template_id].hp

    def serialize(self):
        return {'hp': self.hp, 'template': self.template_id}

    @classmethod
    def deserialize(cls, data):
        instance = cls(data['template_id'])
        instance.hp = data['hp']

        return instance

    @property
    def name(self):
        assert self.template_id is not None
        return ObjectManager.game.enemies[self.template_id].name

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def strength(self):
        assert self.template_id is not None
        return ObjectManager.game.enemies[self.template_id].strength

    @property
    def armor(self):
        assert self.template_id is not None
        return ObjectManager.game.enemies[self.template_id].armor

    @property
    def agility(self):
        assert self.template_id is not None
        return ObjectManager.game.enemies[self.template_id].agility

    @property
    def biomass(self):
        assert self.template_id is not None
        return ObjectManager.game.enemies[self.template_id].biomass

    @property
    def knowledge(self):
        assert self.template_id is not None
        return ObjectManager.game.enemies[self.template_id].knowledge.items()
