# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random
import math
from Constants import ACTIVITY_TYPE
from Constants import ENTRY_TYPE
from Creature import Activity
from Fight import Fight
from ObjectManager import ObjectManager

from functools import partial


class Adventure(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.duration = None
        self.enemies = []
        self.rewards = {}
        self.failed = False

    def add_reward(self, item_id, quantity_range, curve, chance):
        reward = Reward()
        reward.quantity_range = quantity_range
        reward.curve = curve
        reward.chance = chance
        self.rewards[item_id] = reward

    def add_enemy(self, enemy, chance):
        new_enemy = Enemy()
        new_enemy.enemy = enemy
        new_enemy.chance = chance
        self.enemies.append(new_enemy)

    def start(self, creature, date):
        creature.logger.add_entry(
            date,
            '{} started adventure {}'.format(creature.name, self.title),
            ACTIVITY_TYPE.ADVENTURE,
            ENTRY_TYPE.INFO
        )

    def update(self, creature, date):
        enemy = None
        for possible_enemy in self.enemies:
            if random.random() < possible_enemy.chance:
                enemy = possible_enemy
                enemy.enemy.reset()
                break
        if enemy is None:
            return

        creature.set_activity(Activity(
            Fight, ACTIVITY_TYPE.FIGHTING, -1,
            partial(ObjectManager.game.start_fight, creature, enemy),
            partial(ObjectManager.game.update_fight, creature),
            partial(ObjectManager.game.end_fight, creature)
        ))

    def finish(self, creature, date):
        rewards = {}
        if not self.failed:
            for item_id, reward in self.rewards.items():
                if random.random() < reward.chance:
                    # TODO: Use better curve formula
                    quantity = math.pow(random.random(), reward.curve)
                    quantity *= (
                        reward.quantity_range[1] - reward.quantity_range[0]
                    )
                    quantity += reward.quantity_range[0]
                    rewards[item_id] = int(quantity)

            creature.logger.add_entry(
                date,
                '{} finished adventure {}'.format(creature.name, self.title),
                ACTIVITY_TYPE.ADVENTURE,
                ENTRY_TYPE.INFO
            )
        else:
            creature.logger.add_entry(
                date,
                '{} failed adventure {}'.format(creature.name, self.title),
                ACTIVITY_TYPE.ADVENTURE,
                ENTRY_TYPE.INFO
            )

            self.failed = False

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


class Enemy(object):
    def __init__(self):
        self.enemy = -1
        self.chance = 0.0
