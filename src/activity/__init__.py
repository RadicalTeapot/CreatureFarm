# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ObjectManager import ObjectManager


class Activity(object):
    def __init__(self, activity_type, creature, duration):
        self.activity_type = activity_type

        self.creature = creature
        self.duration = duration
        self.turn_count = 0

    def start(self):
        pass

    def update(self):
        pass

    def end(self):
        pass

    def serialize(self):
        data = {}
        data['duration'] = self.duration
        data['turn_count'] = self.turn_count
        data['activity_type'] = self.activity_type
        data['creature_id'] = self.creature.id
        return data

    def deserialize(self, data):
        self.duration = data['duration']
        self.turn_count = data['turn_count']
        self.activity_type = data['activity_type']

        creature = [
            creature
            for creature in ObjectManager.game.creatures
            if creature.id == data['creature']
        ]
        if not creature:
            raise RuntimeError('Cannot find creature')
