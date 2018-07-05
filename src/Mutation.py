# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ObjectManager import ObjectManager


class MutationTemplate:
    def __init__(self):
        self.mutation_id = ''
        self.name = ''
        self.required_level = 0.
        self.exclude = set()
        self.size = 0.
        self.effects = {}
        self.biomass_cost = 0.
        self.description = ''

    @classmethod
    def from_data(cls, mutation_id, data):
        cls.validate_data(data)
        instance = cls()
        instance.mutation_id = mutation_id
        instance.name = data['name']
        instance.required_level = data['required_level']
        instance.exclude = set(data['exclude'])
        instance.size = data['size']
        instance.effects.update(data['effects'])
        instance.biomass_cost = data['biomass_cost']
        instance.description = data['description']

        return instance

    @staticmethod
    def validate_data(data):
        attributes = [
            "name", "required_level", "exclude", "size", "effects",
            "biomass_cost", "description"
        ]
        for attribute in attributes:
            if attribute not in data:
                raise KeyError('Missing {} attribute'.format(attribute))
        # TODO: test data types as well

    def get_description(self):
        # TODO Add validity info to description (green for valid,
        # red for invalid) i.e. cannot select quadruped because of
        # selected crawl or cannot select biped because too little knowledge
        return self.description

    def is_valid(self, mutation_ids=()):
        if ObjectManager.game.knowledge[self.mutation_id] < self.required_level:
            return False

        other_mutations = [
            ObjectManager.game.mutations[id_] for id_ in mutation_ids
        ]
        for mutation in other_mutations:
            if any(exclude in self.mutation_id for exclude in mutation.exclude):
                return False

        return True
