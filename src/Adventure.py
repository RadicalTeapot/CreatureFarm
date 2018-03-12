# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random


class Adventure(object):
    NOT_STARTED = 0
    RUNING = 1
    FINISHED = 2

    def __init__(self):
        self.title = ''
        self.description = ''
        self.rewards = None

        # Length in turns
        self.duration = 10
        # Risk of damage being inflicted
        self.danger = .1
        # Quantity of damages to inflict
        self.difficulty = 1

        self.creature = None
        # Counter for adventure length
        self.clock = 0
        # State of the adventure
        self.state = self.NOT_STARTED
        # Callback method when adventure finishes
        self.callback = None

    def assign_creature(self, creature):
        self.creature = creature

    def start(self):
        if not self.creature:
            return

        self.clock = 0
        self.creature.lock()
        self.state = self.RUNING

    def update(self):
        self.clock += 1
        if self.clock >= self.duration:
            return self.finish()

        if random.random() < self.danger:
            self.creature.hit(self.difficulty)

    def finish(self):
        self.creature.free()
        self.state = self.FINISHED

        rewards = []
        for reward in self.rewards:
            if random.random() < reward.chance:
                for name, quantity in reward.contents.items():
                    # TODO: random to get qty and append
                    rewards.append()

        if self.callback:
            self.callback()



class Reward(object):
    def __init__(self):
        self.chance = .1
        self.contents = {'food': (2, 5)}
