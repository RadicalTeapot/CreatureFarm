# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random


class Creature(object):
    def __init__(self, name):
        self.name = name

        self.hp = 0

        self.strength = 0
        self.agility = 0
        self.stamina = 0
        self.speed = 0

        self.hunger = 0
        self.tired = 0

        self.hatch()

    def hatch(self):
        # TODO: get base values from Settings
        self.hp = random.randint(5, 10)
        self.strength = random.randint(1, 10)
        self.agility = random.randint(1, 10)
        self.stamina = random.randint(1, 10)
        self.speed = random.randint(1, 10)

    def update(self, dt):
        self.hunger += dt
        self.tired += dt

    def eat(self, quantity):
        self.hunger -= quantity

    def sleep(self, duration):
        self.tired -= duration
