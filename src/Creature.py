# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Logger import Logger
from Constants import ACTIVITY_TYPE
from Constants import BODY_PART
from Constants import STATS
from ObjectManager import ObjectManager

from activity.Adventure import Adventure
from activity.Fight import Fight

import copy


class Creature(object):
    def __init__(self, name):
        self._model = Model()
        self.logger = Logger(name)

        self.hatch(name)

    # ####################################################################### #
    #                           Getters / Setters                             #
    # ####################################################################### #

    @property
    def id(self):
        return self._model.id

    @id.setter
    def id(self, value):
        self._model.id = value

    @property
    def name(self):
        if not self.busy:
            return self._model.name
        else:
            return '{} (busy)'.format(self._model.name)

    @name.setter
    def name(self, value):
        self._model.name = value

    @property
    def hp(self):
        return self._get_stat(STATS.HP)

    @hp.setter
    def hp(self, value):
        self._set_stat(STATS.HP, value)

    @property
    def max_hp(self):
        return self._get_stat(STATS.MAX_HP)

    @max_hp.setter
    def max_hp(self, value):
        self._set_stat(STATS.MAX_HP, value)

    @property
    def strength(self):
        return self._get_stat(STATS.STRENGTH)

    @strength.setter
    def strength(self, value):
        self._set_stat(STATS.STRENGTH, value)

    @property
    def melee(self):
        return self._get_stat(STATS.MELEE)

    @melee.setter
    def melee(self, value):
        self._set_stat(STATS.MELEE, value)

    @property
    def marksmanship(self):
        return self._get_stat(STATS.MARKSMANSHIP)

    @marksmanship.setter
    def marksmanship(self, value):
        self._set_stat(STATS.MARKSMANSHIP, value)

    @property
    def evasion(self):
        return self._get_stat(STATS.EVASION)

    @evasion.setter
    def evasion(self, value):
        self._set_stat(STATS.EVASION, value)

    @property
    def armor(self):
        return self._get_stat(STATS.ARMOR)

    @armor.setter
    def armor(self, value):
        self._set_stat(STATS.ARMOR, value)

    @property
    def cooking(self):
        return self._get_stat(STATS.COOKING)

    @cooking.setter
    def cooking(self, value):
        self._set_stat(STATS.COOKING, value)

    @property
    def building(self):
        return self._get_stat(STATS.BUILDING)

    @building.setter
    def building(self, value):
        self._set_stat(STATS.BUILDING, value)

    @property
    def inventory_size(self):
        return self._get_stat(STATS.INVENTORY_SIZE)

    @inventory_size.setter
    def inventory_size(self, value):
        self._set_stat(STATS.INVENTORY_SIZE, value)

    @property
    def busy(self):
        return len(self._model.activity_stack) > 0

    @property
    def activity(self):
        if not self.busy:
            return None
        return self._model.activity_stack[-1]

    @property
    def timer(self):
        if not self.busy:
            return 0
        return self._model.activity_stack[-1].turn_count

    @property
    def inventory(self):
        return self._model.inventory

    @property
    def equipment(self):
        return self._model.equipment

    # ####################################################################### #
    #                                 Logic                                   #
    # ####################################################################### #

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

    def gain_experience(self, stat, amount):
        if stat not in self._model.stats:
            raise KeyError('Wrong stat type')
        self._model.stats[stat] += amount
        # TODO: Add log message when creature gains a new level

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

    def remove_from_inventory(self, loot):
        for item_id, quantity in loot.items():
            if item_id not in self._model.inventory:
                raise KeyError('Item {} not in inventory'.format(item_id))

            self._model.inventory[item_id] -= quantity

            if self._model.inventory[item_id] <= 0:
                del self._model.inventory[item_id]

    def hatch(self, name):
        self.name = name
        self.hp = 10
        self.max_hp = 10

        self.strength = 1.0
        self.melee = 1.0
        self.marksmanship = 1.0

        self.evasion = 1.0
        self.armor = 0.0

        self.cooking = 1.0
        self.building = 1.0

        self.inventory_size = 10

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
        data['stats'] = copy.deepcopy(self._model.stats)
        data['equipment'] = copy.deepcopy(self._model.equipment)
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
        self._model.stats = copy.deepcopy(data['stats'])
        self._model.equipment = copy.deepcopy(data['equipment'])
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


class Model(object):
    def __init__(self):
        self.id = -1
        self.name = ''

        self.stats = {}
        for stat in STATS:
            self.stats[stat] = 0.

        self.activity_stack = []

        self.equipment = {}
        for body_part in BODY_PART:
            self.equipment[body_part] = None

        self.inventory = {}
