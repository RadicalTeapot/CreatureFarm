# -*- coding: utf-8 -*-
"""DOCSTRING."""

import copy


class MutationTemplate:
    def __init__(self):
        self.name = ''
        self.knowledge = set()
        self.body_part = {}
        self.biomass_cost = 0.
        self.description = ''

    @classmethod
    def from_data(cls, id_, data):
        cls.validate_data(data)
        instance = cls()
        instance.id = 'recipes.{}'.format(id_)
        instance.name = data['name']
        instance.knowledge = set(data['knowledge'])
        instance.body_part = copy.deepcopy(data['body_part'])
        instance.biomass_cost = data['biomass_cost']
        instance.description = data['description']

        return instance

    @staticmethod
    def validate_data(data):
        attributes = [
            "name", "knowledge", "biomass_cost", "body_part", "description"
        ]
        for attribute in attributes:
            if attribute not in data:
                raise KeyError('Missing {} attribute'.format(attribute))
        # TODO: test data types as well

    def get_description(self):
        return self.description
