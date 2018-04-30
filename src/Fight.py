# -*- coding: utf-8 -*-
"""DOCSTRING."""

import copy
import math
import random

from Constants import ACTIVITY_TYPE
from Constants import ENTRY_TYPE
from Constants import STATS
from Constants import FIGHT_OUTCOME


class Fight(object):
    def __init__(self, enemy):
        self.enemy = copy.deepcopy(enemy)
        self.turn_count = 0
        self.outcome = None

    def update(self, creature, date):
        # TODO: Switch to a more complete fight system
        self.turn_count += 1
        if self.turn_count > 20:
            return self.draw(creature)

        # Creature hitting enemy
        hit_chance = creature.melee - self.enemy.agility
        # This produces a curve at 0 for hit_chance = -2
        # ~1 for hit_chance = 5 and progresses nicely in between
        hit_chance = 1 - math.exp(1.0 - 1.3 ** (hit_chance + 2))

        if random.random() <= hit_chance:
            # This produces a curve at 1 for armor - strength = 0
            # ~.78 for 1, ~.34 for 5 and ~.13 for 10
            diff = max(self.enemy.armor - creature.strength, 0.)
            armor_absorbtion = math.exp(-(math.pow(diff, .9)) * .25)
            damages = creature.strength * min(max(armor_absorbtion, 0.), 1.)
            self.enemy.hp -= int(damages)
            # TODO: Fix so proper stat gets xp
            # 1% melee increase
            creature.gain_experience(STATS.MELEE, 0.01)

            creature.logger.add_entry(
                date,
                '{} hit {} for {} damage'.format(
                    creature.name, self.enemy.name, int(damages)
                ),
                ACTIVITY_TYPE.FIGHTING,
                ENTRY_TYPE.INFO
            )
        else:
            creature.logger.add_entry(
                date,
                '{} attacks but the {} dodges'.format(
                    creature.name, self.enemy.name
                ),
                ACTIVITY_TYPE.FIGHTING,
                ENTRY_TYPE.INFO
            )

        if self.enemy.hp <= 0:
            return self.won(creature)

        # Enemy hitting creature
        hit_chance = self.enemy.agility - creature.evasion
        hit_chance = 1 - math.exp(1.0 - 1.3 ** (hit_chance + 2))

        if random.random() <= hit_chance:
            diff = max(creature.armor - self.enemy.strength, 0.)
            armor_absorbtion = math.exp(-(math.pow(diff, .9)) * .25)
            damages = (
                self.enemy.strength * min(max(armor_absorbtion, 0.), 1.)
            )
            creature.hit(int(damages))

            # TODO: add fight counter to the date
            creature.logger.add_entry(
                date,
                '{} was hit by {} for {} damage'.format(
                    creature.name, self.enemy.name, int(damages)
                ),
                ACTIVITY_TYPE.FIGHTING,
                ENTRY_TYPE.INFO
            )
        else:
            # 1% evasion increase
            creature.gain_experience(STATS.EVASION, 0.01)

            creature.logger.add_entry(
                date,
                'The {} attacks but {} dodges'.format(
                    self.enemy.name, creature.name
                ),
                ACTIVITY_TYPE.FIGHTING,
                ENTRY_TYPE.INFO
            )

        if creature.hp <= 0:
            return self.lost(creature)

    def won(self, creature):
        self.outcome = FIGHT_OUTCOME.WON
        creature.free()

    def lost(self, creature):
        self.outcome = FIGHT_OUTCOME.LOST
        creature.free()

    def draw(self, creature):
        self.outcome = FIGHT_OUTCOME.DRAW
        # TODO: Also stop adventuring
        creature.free()
