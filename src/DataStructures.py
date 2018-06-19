# -*- coding: utf-8 -*-
"""DOCSTRING."""

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


class Template:
    def __init__(self, mutations=[], cost=0):
        self.mutations = mutations
        self.cost = cost

    def serialize(self):
        return {
            'mutations': self.mutations,
            'cost': self.cost
        }

    def deserialize(self, data):
        self.mutations = data['mutations']
        self.cost = data['cost']


class Group:
    def __init__(self, templates=[], cost=0):
        self.templates = templates
        self.cost = 0

    def serialize(self):
        return {
            'templates': self.templates,
            'cost': self.cost
        }

    def deserialize(self, data):
        self.template = data['templates']
        self.cost = data['cost']


class Adventure:
    def __init__(self, creatures=[], creatures_name=''):
        self.creatures = creatures
        self.creatures_name = creatures_name
        self.log = 'Placeholder log'

    def serialize(self):
        return {
            'creatures': [template.serialize() for template in self.creatures],
            'creature_names': self.creature_names,
            'log': self.log
        }

    def deserialize(self, data):
        self.creatures = [
            Template(value) for value in data['creatures']
        ]
        self.creature_names = data['creature_names']
        self.log = data['log']
