# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random
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
    def strength(self):
        return self._model.strength

    @strength.setter
    def strength(self, value):
        self._model.strength = value

    @property
    def agility(self):
        return self._model.agility

    @agility.setter
    def agility(self, value):
        self._model.agility = value

    @property
    def stamina(self):
        return self._model.stamina

    @stamina.setter
    def stamina(self, value):
        self._model.stamina = value

    @property
    def speed(self):
        return self._model.speed

    @speed.setter
    def speed(self, value):
        self._model.speed = value

    @property
    def hunger(self):
        return self._model.hunger

    @hunger.setter
    def hunger(self, value):
        self._model.hunger = value

    @property
    def tired(self):
        return self._model.tired

    @tired.setter
    def tired(self, value):
        self._model.tired = value

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
        # TODO: get base values from Settings
        self.hp = random.randint(5, 10)
        self.max_hp = self.hp
        self.strength = random.randint(1, 10)
        self.agility = random.randint(1, 10)
        self.stamina = random.randint(1, 10)
        self.speed = random.randint(1, 10)

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

        self.strength = 0
        self.agility = 0
        self.stamina = 0
        self.speed = 0

        self.hunger = 0
        self.tired = 0

        self.activity = None
        self.activity_type = ''
        self.activity_callbacks = {'start': None, 'update': None, 'end': None}
        self.timer = 0


class View(object):
    pass
