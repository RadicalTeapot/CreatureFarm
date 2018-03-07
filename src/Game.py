# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random
from Creature import Creature


class Game(object):
    def __init__(self):
        self.creatures = []
        self.current = None

        self.food = 0

    def add_creature(self, creature):
        self.creatures.append(creature)

    def show_creatures(self, panel):
        panel.show()

    def do_adventure(self):
        # TODO: pick adventure here
        damages = random.randint(0, 3)
        food = random.randint(2, 5)
        egg = random.random() < .05

        return damages, food, egg

    def start_adventure(self):
        if not self.current:
            self.pick_creature()

        damages, food, egg = self.do_adventure()
        self.current.hp -= damages
        self.current.hunger += 1
        self.current.tired += 1
        self.food += food
        if egg:
            self.creatures.append(Creature())
