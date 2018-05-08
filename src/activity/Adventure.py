# -*- coding: utf-8 -*-
"""DOCSTRING."""

import random

from Constants import ACTIVITY_TYPE
from Constants import ENTRY_TYPE

from ObjectManager import ObjectManager

from activity import Activity


class AdventureTemplate(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.enemies = {}
        self.rewards = {}

    @classmethod
    def from_data(cls, id, data):
        cls.validate_data(data)

        instance = cls()
        instance.id = 'adventures.{}'.format(id)
        instance.title = data['title']
        instance.description = data['description']

        for enemy in data.get('enemies', []):
            instance.add_enemy(enemy['enemy'], enemy['chance'])

        for reward in data.get('rewards', []):
            instance.add_reward(reward['item'], reward['chance'])

        return instance

    @staticmethod
    def validate_data(data):
        attributes = [
            "title", "enemies", "rewards", "description"
        ]
        for attribute in attributes:
            if attribute not in data:
                raise KeyError('Missing {} attribute'.format(attribute))
        # TODO check rewards validity as well
        # TODO check enemies validity as well

    def add_enemy(self, enemy_id, chance):
        self.enemies[enemy_id] = chance

    def add_reward(self, item_id, chance):
        self.rewards[item_id] = chance

    def is_available(self, creature):
        return True

    def get_description(self):
        return 'Adventure description placeholder'


class Adventure(Activity):
    def __init__(self, creature=None, template=None):
        super().__init__(ACTIVITY_TYPE.ADVENTURE, creature, -1)
        self.template = template

    def start(self):
        self.creature.logger.add_entry(
            ObjectManager.game.date,
            '{} started adventure {}'.format(
                self.creature.name, self.template.title
            ),
            self.activity_type,
            ENTRY_TYPE.INFO
        )

    def update(self):
        for enemy_id, chance in self.template.enemies.items():
            if random.random() < chance:
                ObjectManager.game.start_fight(self.creature, enemy_id)
                return

        for item_id, chance in self.template.rewards.items():
            if random.random() < chance:
                self.creature.add_to_inventory({item_id: 1})

                self.creature.logger.add_entry(
                    ObjectManager.game.date,
                    '{} found one {}'.format(
                        self.creature.name,
                        ObjectManager.game.inventory.get_item(item_id).name
                    ),
                    self.activity_type,
                    ENTRY_TYPE.INFO
                )
                break

    def end(self):
        message = '{} just finished adventure {} !\n\nThey found:\n'.format(
            self.reature.name, self.template.title
        )
        for item_id, quantity in self.creature.inventory.items():
            message += '    {}: {}\n'.format(
                ObjectManager.game.inventory.get_item(item_id).name,
                quantity
            )
        self.inventory.add_items(self.creature.inventory)
        self.creature.inventory.clear()

        ObjectManager.ui.display_dialog(message)
        ObjectManager.ui.refresh()

    def serialize(self):
        data = super().serialize()
        data['template'] = None if self.template is None else self.template.id
        return data

    def deserialize(self, data):
        super().deserialize(data)
        template = [
            adventure
            for adventure in ObjectManager.game.adventures
            if adventure.id == data['template']
        ]
        if template:
            self.template = template[0]
