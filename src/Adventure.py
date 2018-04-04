# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random
import math


class Adventure(object):
    NOT_STARTED = 0
    RUNNING = 1
    FINISHED = 2

    def __init__(self):
        self.id = -1
        self.title = ''
        self.description = ''
        self.rewards = []
        self.damage_range = [0, 0]
        self.damage_range_curve = 1.0

        # Length in turns
        self.duration = 10
        # Risk of damage being inflicted
        self.danger = .1

    def add_reward(self, item, quantity_range, curve, chance):
        reward = Reward()
        reward.item = item
        reward.quantity_range = quantity_range
        reward.curve = curve
        reward.chance = chance
        self.rewards.append(reward)

    def update(self, creature):
        if random.random() < self.danger:
            # TODO: Use better curve formula
            damage = math.pow(random.random(), self.damage_range_curve)
            damage *= (self.damage_range[1] - self.damage_range[0])
            damage += self.damage_range[0]
            creature.hit(damage)

    def finish(self):
        rewards = []
        for reward in self.rewards:
            if random.random() < reward.chance:
                # TODO: Use better curve formula
                quantity = math.pow(random.random(), reward.curve)
                quantity *= (
                    reward.quantity_range[1] - reward.quantity_range[0]
                )
                quantity += reward.quantity_range[0]
                rewards.append((reward.item, quantity))

        return rewards

    def is_available(self, creature):
        return True

    def get_description(self):
        return 'Adventure description placeholder'


class Reward(object):
    def __init__(self):
        self.chance = 0.0
        self.quantity_range = 0.0
        self.curve = 1.0
        self.item = -1
