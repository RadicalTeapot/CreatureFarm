# -*- coding: utf-8 -*-
"""DOCSTRING."""

import copy
from collections import OrderedDict

from Adventure import Adventure


class GameModel:
    """Store data of Game."""

    def __init__(self):
        self.biomass = 0

        self.creature_groups = OrderedDict()
        self.creature_templates = OrderedDict()

        self.adventure_templates = {}
        self.enemy_templates = {}
        self.mutation_templates = {}
        self.mutation_knowledge = {}

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
        data['mutation_knowledge'] = self.mutation_knowledge

        return data

    def deserialize(self, data):
        self.biomass = data['biomass']
        self.date = data['date']

        self.creature_templates = OrderedDict([
            (name, Template.deserialize(value))
            for name, value in data['creature_templates']
        ])
        self.creature_groups = OrderedDict([
            (name, Group.deserialize(value))
            for name, value in data['creature_groups']
        ])
        self.running_adventures = {
            name: [Adventure.deserialize(value) for value in values]
            for name, values in data['running_adventures']
        }

        self.mutation_knowledge = copy.deepcopy(data['mutation_knowledge'])


class Template:
    def __init__(self, mutations=[], size=1., cost=0):
        self.mutations = mutations
        self.cost = cost
        self.size = size

    def serialize(self):
        return {
            'mutations': self.mutations,
            'cost': self.cost,
            'size': self.size,
        }

    @classmethod
    def deserialize(cls, data):
        instance = cls()
        instance.mutations = data['mutations']
        instance.cost = data['cost']
        instance.size = data['size']
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
