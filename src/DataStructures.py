# -*- coding: utf-8 -*-
"""DOCSTRING."""

from typing import NamedTuple
from collections import OrderedDict


class Knowledge(NamedTuple):
    base_cost: float
    current_level: int


class GameModel:
    """Store data of Game."""

    def __init__(self):
        self.biomass = 0

        self.creature_groups = OrderedDict()
        self.creature_templates = OrderedDict()

        self.adventure_templates = {}
        self.enemy_templates = {}
        self.mutation_templates = {}
        self.knowledge = {}

        self.running_adventures = {}

        self.date = 0

    def serialize(self):
        data = {}

        data['biomass'] = self.biomass
        data['date'] = self.date

        data['creature_templates'] = [
            (name, template.serialize())
            for name, template in self.creature_templates.items()
        ]
        data['creature_groups'] = [
            (name, group.serialize())
            for name, group in self.creature_groups.items()
        ]

        data['running_adventures'] = [
            (name, [adventure.serialize() for adventure in adventures])
            for name, adventures in self.running_adventures.items()
        ]

        # Knowledge
        return data

    def deserialize(self, data):
        self.biomass = data['biomass']
        self.date = data['date']

        self.creature_templates = OrderedDict([
            (name, Template().deserialize(value))
            for name, value in data['creature_templates']
        ])
        self.creature_groups = OrderedDict([
            (name, Group().deserialize(value))
            for name, value in data['creature_groups']
        ])
        self.running_adventures = {
            name: [Adventure().deserialize(value) for value in values]
            for name, values in data['running_adventures']
        }
        # Knowledge


class Template:
    def __init__(self, mutations=[], cost=0):
        self.mutations = mutations
        self.cost = cost

    def serialize(self):
        return {
            'mutations': self.mutations,
            'cost': self.cost
        }

    @classmethod
    def deserialize(cls, data):
        instance = cls()
        instance.mutations = data['mutations']
        instance.cost = data['cost']
        return instance


class Group:
    def __init__(self, templates=[], cost=0):
        self.templates = templates
        self.cost = cost

    def serialize(self):
        return {
            'templates': self.templates,
            'cost': self.cost
        }

    @classmethod
    def deserialize(cls, data):
        instance = cls()
        instance.templates = data['templates']
        instance.cost = data['cost']
        return instance


class Adventure:
    def __init__(self, creatures=[], creatures_name=''):
        self.creatures = creatures
        self.creatures_name = creatures_name
        self.log = 'Placeholder log'

    def serialize(self):
        return {
            'creatures': [creature.serialize() for creature in self.creatures],
            'creatures_name': self.creatures_name,
            'log': self.log
        }

    @classmethod
    def deserialize(cls, data):
        instance = cls()
        instance.creatures = [
            Template(value) for value in data['creatures']
        ]
        instance.creatures_name = data['creatures_name']
        instance.log = data['log']
        return instance
