# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ObjectManager import ObjectManager


class Creature:
    def __init__(self, template_name, mutation_names):
        self.template_name = template_name
        self.mutation_names = mutation_names

        self.stats = {
            'hp': 0.,
            'agility': 0.,
            'attack': 0.,
            'held_biomass': 0.,
            'max_biomass': 0.,
            'knowledge': [],
            'size': 0.,
        }
        self.build_stats(mutation_names)

    def get_stat_modifier(self, stat):
        return sum(
            [mutation.effects.get(stat, 0.) for mutation in self.mutations]
        )

    def build_stats(self, mutation_names):
        game_mutations = ObjectManager.game.get_mutations()
        mutations = [game_mutations[name] for name in self.mutation_names]
        self.stats['size'] = sum([mutation.size for mutation in mutations])
        self.stats['hp'] = (
            self.stats['size'] * 10.0 + self.get_stat_modifier('hp')
        )
        self.stats['agility'] = (
            self.stats['size'] * -1 + self.get_stat_modifier('agility')
        )
        self.stats['attack'] = self.get_stat_modifier('attack')
        self.stats['max_biomass'] = self.stats['size'] * 10.

    def hit(self, amount):
        self.stats['hp'] -= amount

    def add_biomass(self, amount):
        self.stats['held_biomass'] = max(
            self.stats['held_biomass'] + amount, self.stats['max_biomass']
        )

    def is_dead(self):
        return self.hp <= 0

    def is_full(self):
        return self.stats['held_biomass'] >= self.stats['max_biomass']

    def serialize(self):
        data = {}
        data['template_name'] = self.name
        data['mutation_names'] = self.mutation_names
        data['stats'] = dict(self.stats)
        return data

    @classmethod
    def deserialize(cls, data):
        instance = cls('', [])
        instance.template_name = data['template_name']
        instance.mutation_names = data['mutation_names']
        instance.stats = dict(data['stats'])
        return instance
