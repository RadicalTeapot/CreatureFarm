# -*- coding: utf-8 -*-
"""DOCSTRING."""

from activity import Activity
from Constants import ACTIVITY_TYPE
from ObjectManager import ObjectManager


class Feed(Activity):
    def __init__(self, creature=None, item=None):
        super().__init__(ACTIVITY_TYPE.FEED, creature, 1)
        self.item = item

    def start(self):
        ObjectManager.game.inventory.take_items({self.item.id: 1})

    def end(self):
        heal_amount = min(
            self.item.eat(), self.creature.max_hp - self.creature.hp
        )
        self.creature.hp = self.creature.hp + heal_amount

        ObjectManager.ui.display_dialog(
            '{} finished eating {}.\nThey healed for {} hp'.format(
                self.creature.name, self.item.name, heal_amount
            )
        )

    def serialize(self):
        data = super().serialize()
        data['item_id'] = self.item.id

    def deserialize(self, data):
        super().deserialize(data)
        self.item = ObjectManager.game.inventory.items[data['item_id']]
