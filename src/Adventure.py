# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random


class Adventure(object):
    NOT_STARTED = 0
    RUNNING = 1
    FINISHED = 2

    def __init__(self, title=''):
        self.title = title
        self.description = ''
        self.rewards = [
            Reward(1, ['food'], [[2, 5]]),
            Reward(.1, ['sword'], [[1, 1]]),
            Reward(.01, ['creaure egg'], [[1, 1]])
        ]

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

        adventure = Adventure(self.title)
        adventure.__dict__ = self.__dict__.copy()

        adventure.clock = 0
        adventure.creature.lock()
        adventure.state = self.RUNNING
        return adventure

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
                for name, qty in reward.contents.items():
                    quantity = int(
                        random.random() * (qty[1] - qty[0]) + qty[0]
                    )
                    rewards.append((name, quantity))

        if self.callback:
            self.callback(rewards)


class Reward(object):
    def __init__(self, chance, items, quantity_ranges):
        self.chance = chance
        self.contents = dict(zip(items, quantity_ranges))
