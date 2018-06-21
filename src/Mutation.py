# -*- coding: utf-8 -*-
"""DOCSTRING."""


class MutationTemplate:
    def __init__(self):
        self.name = ''
        self.require = set()
        self.exclude = set()
        self.size = 0.
        self.effects = {}
        self.biomass_cost = 0.
        self.description = ''

    @classmethod
    def from_data(cls, data):
        cls.validate_data(data)
        instance = cls()
        instance.name = data['name']
        instance.require = set(data['require'])
        instance.exclude = set(data['exclude'])
        instance.size = data['size']
        instance.effects.update(data['effects'])
        instance.biomass_cost = data['biomass_cost']
        instance.description = data['description']

        return instance

    @staticmethod
    def validate_data(data):
        attributes = [
            "name", "require", "exclude", "size", "effects",
            "biomass_cost", "description"
        ]
        for attribute in attributes:
            if attribute not in data:
                raise KeyError('Missing {} attribute'.format(attribute))
        # TODO: test data types as well

    def get_description(self):
        return self.description
