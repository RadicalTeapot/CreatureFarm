# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random


class Creature(object):
    def __init__(self, name):
        self._model = Model()
        self._view = View()

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
        if not self.locked:
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
    def locked(self):
        return self._model.locked

    @locked.setter
    def locked(self, value):
        self._model.locked = value

    # ####################################################################### #
    #                                 Logic                                   #
    # ####################################################################### #

    def hatch(self, name):
        self.name = name
        # TODO: get base values from Settings
        self.hp = random.randint(5, 10)
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

    def lock(self):
        self.locked = True

    def free(self):
        self.locked = False


class Model(object):
    def __init__(self):
        self.id = -1
        self.name = ''

        self.hp = 0

        self.strength = 0
        self.agility = 0
        self.stamina = 0
        self.speed = 0

        self.hunger = 0
        self.tired = 0
        self.locked = False


class View(object):
    pass
