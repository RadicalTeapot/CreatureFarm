# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ObjectManager import ObjectManager


class Creature:
    def __init__(self, mutation_names=[]):
        self.stats = {
            'hp': 0.,
            'agility': 0.,
            'attack': 0.,
            'held_biomass': 0.,
            'max_biomass': 0.,
            'knowledge': [],
        }
        self.mutations = []
        self.build_stats(mutation_names)

    def get_stat_modifier(self, stat):
        return sum(
            [mutation.effects.get(stat, 0.) for mutation in self.mutations]
        )

    def build_stats(self, mutation_names):
        self.mutations = [
            mutation
            for mutation in ObjectManager.game.get_mutations()
            if mutation.name in mutation_names
        ]

        size = sum([mutation.size for mutation in self.mutations])

        self.stats['hp'] = size * 10.0 + self.get_stat_modifier('hp')
        self.stats['agility'] = size * -1 + self.get_stat_modifier('agility')
        self.stats['attack'] = self.get_stat_modifier('attack')
        self.stat['max_biomass'] = size * 10.

    def hit(self, amount):
        self.stat['hp'] -= amount

    def add_biomass(self, amount):
        self.stat['held_biomass'] = max(
            self.stat['held_biomass'] + amount, self.stat['max_biomass']
        )

    def is_dead(self):
        return self.hp <= 0

    def is_full(self):
        return self.stat['held_biomass'] >= self.stat['max_biomass']

    def serialize(self):
        data = {}
        data['mutations'] = [mutation.name for mutation in self.mutations]
        data['stats'] = dict(self.stats)
        return data

    @classmethod
    def deserialize(cls, data):
        instance = cls()
        instance.build_stats(data['mutations'])
        instance.stats = dict(data['stats'])
        return instance
