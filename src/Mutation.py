# -*- coding: utf-8 -*-
"""DOCSTRING."""

from collections import namedtuple

Knowledge = namedtuple('knowledge', 'type quantity')


class Mutation:
    def __init__(self):
        self.name = None
        self.knowledge = Knowledge(None, None)
        self.biomass_cost = None
        self.body_part = None
        self.description = ''

    @classmethod
    def from_data(cls, id_, data):
        cls.validate_data(data)
        instance = cls()
        instance.id = 'recipes.{}'.format(id_)
        instance.name = data['name']
        instance.knowledge.type = data['knowledge_type']
        instance.knowledge.quantity = data['knowledge_quantity']
        instance.knowledge.biomass_cost = data['biomass_cost']
        instance.knowledge.body_part = data['body_part']
        instance.description = data['description']

        return instance

    @staticmethod
    def validate_data(data):
        attributes = [
            "name", "knowledge_type", "knowledge_quantity", "biomass_cost",
            "body_part", "description"
        ]
        for attribute in attributes:
            if attribute not in data:
                raise KeyError('Missing {} attribute'.format(attribute))

    def get_description(self):
        return self.description
