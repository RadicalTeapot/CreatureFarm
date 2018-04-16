# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random
import math
from Constants import ACTIVITY_TYPE
from Constants import ENTRY_TYPE


class Adventure(object):
    NOT_STARTED = 0
    RUNNING = 1
    FINISHED = 2

    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.duration = None
        self.enemies = []
        self.rewards = []

    def add_reward(self, item, quantity_range, curve, chance):
        reward = Reward()
        reward.item = item
        reward.quantity_range = quantity_range
        reward.curve = curve
        reward.chance = chance
        self.rewards.append(reward)

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

        creature.logger.add_entry(
            date,
            '{} encountered {} !'.format(
                creature.name, enemy.enemy.name
            ),
            ACTIVITY_TYPE.FIGHTING,
            ENTRY_TYPE.IMPORTANT
        )

        counter = 0
        while True:
            if enemy.enemy.hp <= 0:
                # TODO: add fight counter to the date
                creature.logger.add_entry(
                    date,
                    '{} killed {} !'.format(creature.name, enemy.enemy.name),
                    ACTIVITY_TYPE.FIGHTING,
                    ENTRY_TYPE.IMPORTANT
                )
                break
            if creature.hp <= 0:
                # TODO: add fight counter to the date
                creature.logger.add_entry(
                    date,
                    '{} was killed by {} !'.format(
                        creature.name, enemy.enemy.name
                    ),
                    ACTIVITY_TYPE.FIGHTING,
                    ENTRY_TYPE.CRITICAL
                )
                break
            if counter >= 50:
                # HACK: This avoids an infinite loop, find a more elegant
                # system
                break
            counter += 1

            # TODO: Switch to a more complete fight system

            # Creature hitting enemy
            hit_chance = creature.melee - enemy.enemy.agility
            # This produces a curve is at 0 for hit_chance = -2
            # ~1 for hit_chance = 5 and progresses nicely in between
            hit_chance = 1 - math.exp(1.0 - 1.3 ** (hit_chance + 2))

            if random.random() <= hit_chance:
                # TODO: improve formula
                damages = creature.strength * (1. - enemy.enemy.armor)
                enemy.enemy.hp -= damages
                creature.melee += 0.01  # 1% skill increase

                # TODO: add fight counter to the date
                creature.logger.add_entry(
                    date,
                    '{} hit {} for {} damage'.format(
                        creature.name, enemy.enemy.name, damages
                    ),
                    ACTIVITY_TYPE.FIGHTING,
                    ENTRY_TYPE.INFO
                )

            # Enemy hitting creature
            hit_chance = enemy.enemy.agility - creature.evasion
            hit_chance = 1 - math.exp(1.0 - 1.3 ** (hit_chance + 2))

            if random.random() <= hit_chance:
                # TODO: improve formula
                damages = enemy.enemy.strength * (1. - creature.armor)
                creature.hit(damages)

                # TODO: add fight counter to the date
                creature.logger.add_entry(
                    date,
                    '{} was hit by {} for {} damage'.format(
                        creature.name, enemy.enemy.name, damages
                    ),
                    ACTIVITY_TYPE.FIGHTING,
                    ENTRY_TYPE.INFO
                )
            else:
                creature.evasion += 0.01  # 1% evasion increase

    def finish(self, creature, date):
        rewards = []
        for reward in self.rewards:
            if random.random() < reward.chance:
                # TODO: Use better curve formula
                quantity = math.pow(random.random(), reward.curve)
                quantity *= (
                    reward.quantity_range[1] - reward.quantity_range[0]
                )
                quantity += reward.quantity_range[0]
                rewards.append((reward.item, int(quantity)))

        creature.logger.add_entry(
            date,
            '{} finished adventure {}'.format(creature.name, self.title),
            ACTIVITY_TYPE.ADVENTURE,
            ENTRY_TYPE.INFO
        )

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


class Enemy(object):
    def __init__(self):
        self.enemy = -1
        self.chance = 0.0
