# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ObjectManager import ObjectManager
from Settings import Settings


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

    def _get_excluding_mutations(self, mutation_ids):
        other_mutations = [
            ObjectManager.game.mutations[id_] for id_ in mutation_ids
        ]

        mutations = []
        for mutation in other_mutations:
            if any(exclude in self.mutation_id for exclude in mutation.exclude):
                mutations.append(mutation)
        return mutations

    def get_description(self, mutation_ids=()):
        description = [self.description]
        if ObjectManager.game.knowledge[self.mutation_id] < self.required_level:
            description.append(
                '[color={}]Required knowledge is missing.[/color]'.format(
                    Settings.RED
                )
            )

        for mutation in self._get_excluding_mutations(mutation_ids):
            description.append(
                '[color={}]Incompatible with the {} mutation.[/color]'.format(
                    Settings.RED, mutation.name
                )
            )
        return '\n'.join(description)

    def is_valid(self, mutation_ids=()):
        if ObjectManager.game.knowledge[self.mutation_id] < self.required_level:
            return False

        if self._get_excluding_mutations(mutation_ids):
            return False

        return True
