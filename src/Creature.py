# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Logger import Logger


class Creature(object):
    def __init__(self, name):
        self._model = Model()
        self._view = View()
        self.logger = Logger()

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
        return self._model.hp

    @hp.setter
    def hp(self, value):
        self._model.hp = value

    @property
    def max_hp(self):
        return self._model.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self._model.max_hp = value

    @property
    def melee(self):
        return self._model.melee

    @melee.setter
    def melee(self, value):
        self._model.melee = value

    @property
    def marksmanship(self):
        return self._model.marksmanship

    @marksmanship.setter
    def marksmanship(self, value):
        self._model.marksmanship = value

    @property
    def cooking(self):
        return self._model.cooking

    @cooking.setter
    def cooking(self, value):
        self._model.cooking = value

    @property
    def building(self):
        return self._model.building

    @building.setter
    def building(self, value):
        self._model.building = value

    @property
    def busy(self):
        return self._model.activity is not None

    @property
    def activity(self):
        return self._model.activity

    @property
    def timer(self):
        return self._model.timer

    # ####################################################################### #
    #                                 Logic                                   #
    # ####################################################################### #

    def hatch(self, name):
        self.name = name
        self.hp = 10
        self.max_hp = self.hp
        self.melee = 1.0
        self.marksmanship = 1.0
        self.cooking = 1.0
        self.building = 1.0

    def eat(self, quantity):
        self.hunger -= quantity

    def sleep(self, duration):
        self.tired -= duration

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
                self._model.activity_type, self.timer
            )
        return msg


class Model(object):
    def __init__(self):
        self.id = -1
        self.name = ''

        self.max_hp = 0
        self.hp = 0

        self.melee = 0
        self.marksmanship = 0
        self.cooking = 0
        self.building = 0

        self.activity = None
        self.activity_type = ''
        self.activity_callbacks = {'start': None, 'update': None, 'end': None}
        self.timer = 0


class View(object):
    pass
