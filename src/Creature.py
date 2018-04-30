# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Logger import Logger
from Constants import BODY_PART
from Constants import STATS
from ObjectManager import ObjectManager

import math
import random


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
        return self._model.activity_stack[-1].timer

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
            quantity += self._model.inventory.get(item_id, 0)
            self._model.inventory[item_id] = quantity

    def remove_from_inventory(self, loot):
        for item_id, quantity in loot.items():
            if item_id not in self._model.inventory:
                raise KeyError('Item {} not in inventory'.format(item_id))
            self._model.inventory[item_id] = max(
                self._model.inventory[item_id] - quantity, 0
            )

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

    def hit(self, quantity):
        self.hp -= quantity

    def set_activity(
        self, activity, activity_type, timer,
        start_callback=None, update_callback=None, end_callback=None
    ):
        activity = Activity(
            activity, activity_type, timer,
            start_callback, update_callback, end_callback
        )
        self._model.activity_stack.append(activity)

        if callable(activity.start):
            activity.start()

    def has_activity(self, activity):
        return activity in [
            item.activity for item in self._model.activity_stack
        ]

    def update(self):
        if not self.busy:
            return

        activity = self._model.activity_stack[-1]
        if activity.timer > 0:
            activity.timer -= 1

        if activity.timer == 0:
            self.free()
        else:
            if callable(activity.update):
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
            if not ignore_callbacks and callable(activity.end):
                activity.end()

            del activity

    def get_description(self):
        msg = 'Creature desciption placeholder\n'
        if self.busy:
            msg += 'It is {} for {} more turns.\n'.format(
                self.activity.type.value, self.timer
            )
        msg += '\nInventory :\n'
        for item_id, quantity in self._model.inventory.items():
            name = ObjectManager.game.inventory.get_item(item_id).name
            msg += '  {}: {}\n'.format(name, quantity)
        return msg


class Model(object):
    def __init__(self):
        # TODO Use Constant stats
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


class Activity(object):
    def __init__(
        self, activity, activity_type, timer,
        start_callback=None, update_callback=None, end_callback=None
    ):
        self.activity = activity
        self.type = activity_type
        self.timer = timer
        self.start = start_callback
        self.update = update_callback
        self.end = end_callback


class Enemy(object):
    def __init__(self):
        # TODO Use Constant stats
        self.name = None
        self.level = None
        self.description = None
        self.loot = {}

        self._max_hp = None
        self._hp = None
        self._strength = None
        self._armor = None
        self._agility = None

    def get_loot(self):
        rewards = {}
        for item_id, data in self.loot.items():
            # TODO: use creature stats to modify curve value
            quantity_range, curve = data
            # Remap curve for [0, 1] to [1.5, -0.5]
            curve = min(max(curve, 0.), 1.0)
            curve = (1 - curve) * 2 - 0.5
            # Sigmoid curve
            # for curve = 0.5 -> .1: .008, .5: .5, 1.: 0.998
            quantity = 1 / (1 + math.exp(-12 * (random.random() - curve)))
            # Remap quantity from [0, 1] to quantity range
            quantity *= (quantity_range[1] - quantity_range[0])
            quantity += quantity_range[0]
            quantity = round(quantity)

            if quantity > 0:
                rewards[item_id] = int(quantity)

        return rewards

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self._max_hp = value

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self._hp = value

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self._strength = value

    @property
    def armor(self):
        return self._armor

    @armor.setter
    def armor(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self._armor = value

    @property
    def agility(self):
        return self._agility

    @agility.setter
    def agility(self, value):
        if not isinstance(value, float):
            raise TypeError('Expected float, got {} instead'.format(
                type(value).__name__
            ))
        self._agility = value
