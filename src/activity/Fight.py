# -*- coding: utf-8 -*-
"""DOCSTRING."""

import copy
import math
import random

from Constants import ACTIVITY_TYPE
from Constants import ENTRY_TYPE
from Constants import STATS

from activity import Activity
from Enemy import Enemy
from ObjectManager import ObjectManager


class Fight(Activity):
    def __init__(self, enemy=None, creature=None):
        super().__init__(ACTIVITY_TYPE.FIGHT, creature, -1)
        self.enemy = None
        if enemy is not None:
            self.set_enemy(enemy)

    def set_enemy(self, enemy):
        self.enemy = copy.deepcopy(enemy)

    def start(self):
        self.creature.logger.add_entry(
            ObjectManager.game.date,
            '{} encountered {} !'.format(
                self.creature.name, self.enemy.name
            ),
            self.activity_type,
            ENTRY_TYPE.IMPORTANT
        )

    def update(self):
        # TODO: Switch to a more complete fight system
        if self.turn_count > 20:
            return self.draw(self.creature)

        # Creature hitting enemy
        hit_chance = self.creature.melee - self.enemy.agility
        # This produces a curve at 0 for hit_chance = -2
        # ~1 for hit_chance = 5 and progresses nicely in between
        hit_chance = 1 - math.exp(1.0 - 1.3 ** (hit_chance + 2))

        if random.random() <= hit_chance:
            # This produces a curve at 1 for armor - strength = 0
            # ~.78 for 1, ~.34 for 5 and ~.13 for 10
            diff = max(self.enemy.armor - self.creature.strength, 0.)
            armor_absorbtion = math.exp(-(math.pow(diff, .9)) * .25)
            damages = self.creature.strength * min(
                max(armor_absorbtion, 0.), 1.
            )
            self.enemy.hp -= int(damages)
            # TODO: Fix so proper stat gets xp
            # 1% melee increase
            self.creature.gain_experience(STATS.MELEE, 0.01)

            self.creature.logger.add_entry(
                ObjectManager.game.date,
                '{} hit {} for {} damage'.format(
                    self.creature.name, self.enemy.name, int(damages)
                ),
                self.activity_type,
                ENTRY_TYPE.INFO
            )
        else:
            self.creature.logger.add_entry(
                ObjectManager.game.date,
                '{} attacks but the {} dodges'.format(
                    self.creature.name, self.enemy.name
                ),
                self.activity_type,
                ENTRY_TYPE.INFO
            )

        if self.enemy.hp <= 0:
            return self.won(self.creature)

        # Enemy hitting creature
        hit_chance = self.enemy.agility - self.creature.evasion
        hit_chance = 1 - math.exp(1.0 - 1.3 ** (hit_chance + 2))

        if random.random() <= hit_chance:
            diff = max(self.creature.armor - self.enemy.strength, 0.)
            armor_absorbtion = math.exp(-(math.pow(diff, .9)) * .25)
            damages = (
                self.enemy.strength * min(max(armor_absorbtion, 0.), 1.)
            )
            self.creature.hit(int(damages))

            # TODO: add fight counter to the date
            self.creature.logger.add_entry(
                ObjectManager.game.date,
                '{} was hit by {} for {} damage'.format(
                    self.creature.name, self.enemy.name, int(damages)
                ),
                self.activity_type,
                ENTRY_TYPE.INFO
            )
        else:
            # 1% evasion increase
            self.creature.gain_experience(STATS.EVASION, 0.01)

            self.creature.logger.add_entry(
                ObjectManager.game.date,
                'The {} attacks but {} dodges'.format(
                    self.enemy.name, self.creature.name
                ),
                self.activity_type,
                ENTRY_TYPE.INFO
            )

        if self.creature.hp <= 0:
            self.creature.hp = 0
            return self.lost(self.creature)

    def won(self, creature):
        creature.logger.add_entry(
            ObjectManager.game.date,
            '{} killed {} !'.format(self.creature.name, self.enemy.name),
            self.activity_type,
            ENTRY_TYPE.IMPORTANT
        )

        creature.add_to_inventory(self.enemy.get_loot())

        creature.free()

    def lost(self, creature):
        self.creature.logger.add_entry(
            ObjectManager.game.date,
            '{} fled from {} !'.format(
                self.creature.name, self.enemy.name
            ),
            self.activity_type,
            ENTRY_TYPE.CRITICAL
        )

        # Loose part of the inventory
        if creature.inventory:
            items = random.sample(
                creature.inventory.keys(), random.randint(
                    1, len(creature.inventory)
                )
            )
            for item_name in items:
                quantity = round(
                    random.random() * creature.inventory[item_name]
                )
            creature.remove_from_inventory({item_name: quantity})

        # Stop all activities
        creature.free(free_all=True, ignore_callbacks=True)

    def draw(self, creature):
        creature.logger.add_entry(
            ObjectManager.game.date,
            '{} gave up fighting {}.'.format(
                self.creature.name, self.enemy.name
            ),
            self.activity_type,
            ENTRY_TYPE.CRITICAL
        )
        # Stop all activities
        self.creature.free(free_all=True, ignore_callbacks=True)

    def serialize(self):
        data = super().serialize()
        data['enemy'] = self.enemy.serialize()
        return data

    def deserialize(self, data):
        super().deserialize(data)
        enemy = Enemy()
        enemy.deserialize(data['enemy'])
        self.set_enemy(enemy)
