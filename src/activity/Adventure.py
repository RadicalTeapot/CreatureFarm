# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random

from Constants import ACTIVITY_TYPE
from Constants import ENTRY_TYPE

from ObjectManager import ObjectManager


class Adventure(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.enemies = {}
        self.rewards = {}

    def add_reward(self, item_id, chance):
        self.rewards[item_id] = chance

    def add_enemy(self, enemy_id, chance):
        self.enemies[enemy_id] = chance

    def start(self, creature, date):
        creature.logger.add_entry(
            date,
            '{} started adventure {}'.format(creature.name, self.title),
            ACTIVITY_TYPE.ADVENTURE,
            ENTRY_TYPE.INFO
        )

    def update(self, creature, date):
        for enemy_id, chance in self.enemies.items():
            if random.random() < chance:
                ObjectManager.game.start_fight(creature, enemy_id)
                return

        for item_id, chance in self.rewards.items():
            if random.random() < chance:
                creature.add_to_inventory({item_id: 1})

                creature.logger.add_entry(
                    date,
                    '{} found one {}'.format(
                        creature.name,
                        ObjectManager.game.inventory.get_item(item_id).name
                    ),
                    ACTIVITY_TYPE.ADVENTURE,
                    ENTRY_TYPE.INFO
                )
                break

    def is_available(self, creature):
        return True

    def get_description(self):
        return 'Adventure description placeholder'

    def serialize(self):
        return self.id

    def deserialize(self, data):
        adventure = [
            adventure
            for adventure in ObjectManager.game.adventures
            if adventure.id == data
        ]
        if adventure:
            return adventure[0]
