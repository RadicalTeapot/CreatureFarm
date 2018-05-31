# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Constants import ACTIVITY_TYPE
from Constants import BODY_PART
from Constants import STATS
from ObjectManager import ObjectManager

from activity.Adventure import Adventure
from activity.Fight import Fight

import copy


class CreatureTemplate:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.mutations = set()

        self.stats = {}
        for stat in STATS:
            self.stats[stat] = 0.

        self.biomass = 0.
        self.knowledge = {}

    def serialize(self):
        pass

    @classmethod
    def deserialize(cls, data):
        instance = cls()
        return instance


class Creature:
    def __init__(self, template=None):
        self.template = template
        self.hp = None
        if self.template:
            self.hp = template.hp

    def _get_stat(self, stat):
        if stat not in self._model.stats:
            raise KeyError('Wrong stat type')
        value = self._model.stats[stat]
        # Add equipment stat changes to stat values
        for equiped in self._model.equipment.values():
            if equiped is None:
                continue
            # Get the modification value or 0 if it doesn't exist
            value += equiped.modified_stats.get(stat, 0.)
        return value

    def _set_stat(self, stat, value):
        if stat not in self._model.stats:
            raise KeyError('Wrong stat type')
        self._model.stats[stat] = value

    def add_to_inventory(self, loot):
        for item_id, quantity in loot.items():
            # TODO: Add message to log when inventory is full/quantity needs to
            # be adjusted
            if self.get_inventory_size_left() == 0:
                break

            if quantity > self.get_inventory_size_left():
                quantity = self.get_inventory_size_left()

            quantity += self._model.inventory.get(item_id, 0)
            self._model.inventory[item_id] = quantity

    def get_inventory_size_left(self):
        return self.inventory_size - sum([
            quantity for quantity in self._model.inventory.values()
        ])

    def hit(self, quantity):
        self.hp -= quantity

    def has_activity(self, activity):
        return activity in self._model.activity_stack

    def add_activity(self, activity):
        self._model.activity_stack.append(activity)
        activity.start()

    def update(self):
        if not self.busy:
            return

        activity = self._model.activity_stack[-1]
        activity.turn_count += 1
        if activity.duration != -1:
            if activity.duration - activity.turn_count <= 0:
                return self.free()

        activity.update()

    def free(self, free_all=False, ignore_callbacks=False):
        activities = []
        if free_all:
            activities = [
                activity
                for activity in reversed(self._model.activity_stack)
            ]
            self._model.activity_stack = []
        else:
            activities.append(self._model.activity_stack.pop())

        for activity in activities:
            if not ignore_callbacks:
                activity.end()

            del activity

    def get_description(self):
        msg = 'Creature desciption placeholder\n'
        if self.busy:
            msg += 'It has been {} for {} turns.\n'.format(
                self.activity.activity_type.value, self.timer
            )

        if self._model.inventory.items():
            msg += '\nInventory :\n'
            for item_id, quantity in self._model.inventory.items():
                name = ObjectManager.game.inventory.get_item(item_id).name
                msg += '  {}: {}\n'.format(name, quantity)
        return msg

    def serialize(self):
        data = {}
        data['id'] = self._model.id
        data['name'] = self._model.name
        data['stats'] = {}
        for stat, value in self._model.stats.items():
            data['stats'][stat.value] = value
        data['equipment'] = {}
        for body_part, item in self._model.equipment.items():
            data['equipment'][body_part.value] = item
        data['inventory'] = copy.deepcopy(self._model.inventory)
        data['activity_stack'] = [
            activity.serialize()
            for activity in self._model.activity_stack
        ]
        data['log'] = self.logger.serialize()

        return data

    def deserialize(self, data):
        self._model.id = data['id']
        self._model.name = data['name']
        self._model.stats = {}
        for stat, value in data['stats'].items():
            # HACK: Find better way to get correct stat
            for s in STATS:
                if s.value == stat:
                    self._model.stats[s] = value
        self._model.equipment = {}
        for stat, value in data['equipment'].items():
            # HACK: Find better way to get correct stat
            for s in STATS:
                if s.value == stat:
                    self._model.equipment[s] = value
        self._model.inventory = copy.deepcopy(data['inventory'])
        self._model.activity_stack = []
        for activity_data in data['activity_stack']:
            activity = None
            if activity_data['activity_type'] == ACTIVITY_TYPE.ADVENTURE:
                activity = Adventure()
            elif activity_data['activity_type'] == ACTIVITY_TYPE.FIGHT:
                activity = Fight()
            else:
                raise RuntimeError('Cannot find activity type')
            activity.deserialize(activity_data)
            self._model.activity_stack.append(activity)
        self.logger.deserialize(data['log'])
