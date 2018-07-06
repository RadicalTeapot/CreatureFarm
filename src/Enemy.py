# -*- coding: utf-8 -*-
"""DOCSTRING."""


class EnemyTemplate:
    def __init__(self):
        self.id = None
        self.name = None
        self.mutation_ids = []
        self.size = 1.0
        self.description = None

    @classmethod
    def from_data(cls, id_, data):
        cls.validate_data(data)
        instance = cls()
        instance.id = 'enemies.{}'.format(id_)
        instance.name = data['name']
        instance.mutation_ids = data['mutations']
        instance.size = data['size']
        instance.description = data['description']

        return instance

    @staticmethod
    def validate_data(data):
        attributes = ["name", "description", "mutations", "size"]
        for attribute in attributes:
            if attribute not in data:
                raise KeyError('Missing {} attribute'.format(attribute))
