# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Logger import Logger
from Constants import BODY_PART
from Constants import STATS


class Creature(object):
    def __init__(self, name):
        self._model = Model()
        self._view = View()
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
        return self._model.activity is not None

    @property
    def activity(self):
        return self._model.activity

    @property
    def timer(self):
        return self._model.timer

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
        self._model.activity = activity
        self._model.activity_type = activity_type
        self._model.timer = timer
        self._model.activity_callbacks['start'] = start_callback
        self._model.activity_callbacks['update'] = update_callback
        self._model.activity_callbacks['end'] = end_callback

        if callable(self._model.activity_callbacks['start']):
            self._model.activity_callbacks['start']()

    def update(self):
        if self._model.activity is not None and self._model.timer > 0:
            self._model.timer -= 1
            if self._model.timer == 0:
                self.free()
            else:
                if callable(self._model.activity_callbacks['update']):
                    self._model.activity_callbacks['update']()

    def free(self):
        self._model.activity = None
        self._model.timer = 0

        if callable(self._model.activity_callbacks['end']):
            self._model.activity_callbacks['end']()

        self._model.activity_callbacks['start'] = None
        self._model.activity_callbacks['update'] = None
        self._model.activity_callbacks['end'] = None

    def get_description(self):
        msg = 'Creature desciption placeholder\n'
        if self.busy:
            msg += 'It is {} for {} more turns.\n'.format(
                self._model.activity_type.value, self.timer
            )
        return msg


class Model(object):
    def __init__(self):
        # TODO Use Constant stats
        self.id = -1
        self.name = ''

        self.stats = {}
        for stat in STATS:
            self.stats[stat] = 0.

        self.activity = None
        self.activity_type = ''
        self.activity_callbacks = {'start': None, 'update': None, 'end': None}
        self.timer = 0

        self.equipment = {}
        for body_part in BODY_PART:
            self.equipment[body_part] = None


class View(object):
    pass


class Enemy(object):
    def __init__(self):
        # TODO Use Constant stats
        self.name = None
        self.level = None
        self.description = None

        self._max_hp = None
        self._hp = None
        self._strength = None
        self._armor = None
        self._agility = None

    def reset(self):
        self.hp = self.max_hp

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
