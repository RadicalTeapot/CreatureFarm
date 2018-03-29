# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random


class Adventure(object):
    NOT_STARTED = 0
    RUNNING = 1
    FINISHED = 2

    def __init__(self, title=''):
        self.id = -1
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

    def update(self, creature):
        if random.random() < self.danger:
            creature.hit(self.difficulty)

    def finish(self):
        rewards = []
        for reward in self.rewards:
            if random.random() < reward.chance:
                for name, qty in reward.contents.items():
                    quantity = int(
                        random.random() * (qty[1] - qty[0]) + qty[0]
                    )
                    rewards.append((name, quantity))

        return rewards

    def is_available(self, creature):
        return True

    def get_description(self):
        return 'Adventure description placeholder'


class Reward(object):
    def __init__(self, chance, items, quantity_ranges):
        self.chance = chance
        self.contents = dict(zip(items, quantity_ranges))
