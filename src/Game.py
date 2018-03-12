# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature
from ui import Button
from ui import Ui
from functools import partial
import random


class Game(object):
    def __init__(self):
        self.creatures = []
        self.current = None

        self.food = 0
        self.ui = Ui(self)

    def add_creature(self, creature):
        self.creatures.append(creature)

    def show_creatures(self):
        tab = self.ui.left_panel.tabs[0]
        self.ui.left_panel.clear(tab)
        buttons = []
        for creature in self.creatures:
            button = Button(creature.name)
            button.register_handler(partial(self.select_creature, creature))
            buttons.append(button)
        self.ui.left_panel.add_buttons(tab, buttons)
        self.ui.left_panel.show()

    def select_creature(self, creature):
        self.current = creature

    @property
    def name(self):
        if self.current:
            return self.current.name
        return ''

    @property
    def hp(self):
        if self.current:
            return self.current.hp
        return '-'

    @property
    def strength(self):
        if self.current:
            return self.current.strength
        return '-'

    @property
    def agility(self):
        if self.current:
            return self.current.agility
        return '-'

    @property
    def stamina(self):
        if self.current:
            return self.current.stamina
        return '-'

    @property
    def speed(self):
        if self.current:
            return self.current.speed
        return '-'

    @property
    def hunger(self):
        if self.current:
            return self.current.hunger
        return '-'

    @property
    def tired(self):
        if self.current:
            return self.current.tired
        return '-'

    def do_adventure(self):
        # TODO: pick adventure here
        damages = random.randint(0, 3)
        food = random.randint(2, 5)
        egg = random.random() < .05

        return damages, food, egg

    def start_adventure(self):
        if not self.current:
            return

        damages, food, egg = self.do_adventure()
        self.current.hp -= damages
        self.current.hunger += 1
        self.current.tired += 1
        self.food += food
        if egg:
            self.creatures.append(Creature('egg'))
