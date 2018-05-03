# -*- coding: utf-8 -*-
"""DOCSTRING."""

from activity import Activity
from Constants import ACTIVITY_TYPE
from Constants import ENTRY_TYPE
from Constants import STATS
from ObjectManager import ObjectManager

import random


class Cook(Activity):
    def __init__(self, creature=None, recipe=None):
        super().__init__(ACTIVITY_TYPE.COOK, creature, recipe.duration)
        self.recipe = recipe

    def start(self):
        ObjectManager.game.inventory.take_items(self.recipe.ingredients)

    def end(self):
        diff = self.creature.cooking - self.recipe.complexity

        failed = True
        rand = random.random()
        if diff == -1 and rand < 0.1:
            ObjectManager.ui.display_dialog = (
                '{} failed cooking {} and wasted the ingredients.'
            ).format(
                self.creature.name, self.recipe.name
            )
        elif (diff == 0 and rand < 0.1) or (diff == -1 and rand < .33):
            ObjectManager.ui.display_dialog = (
                '{} failed cooking {} but did not waste the ingredients.'
            ).format(
                self.creature.name, self.recipe.name
            )
            self.inventory.add_items(self.recipe.ingredients)
        else:
            message = '{} just finished cooking !\n\nThey used:\n'.format(
                self.creature.name
            )
            for item_id, quantity in self.recipe.ingredients.items():
                name = self.inventory.get_item(item_id).name
                message += '    {}x {}\n'.format(quantity, name)
            message += '\nAnd produced:\n'
            for item_id, quantity in self.recipe.results.items():
                name = self.inventory.get_item(item_id).name
                message += '    {}x {}\n'.format(quantity, name)
            ObjectManager.ui.display_dialog(message)

            self.inventory.add_items(self.recipe.results)
            failed = False

        xp_gain = 0.
        if diff == -1:  # One level above creature level
            xp_gain = 0.5  # 50 % xp gain
        elif diff == 0:  # Same level
            xp_gain = .2
        elif diff == 1:  # One level below creature level
            xp_gain = .1
        elif diff == 2:  # Two levels below creature level
            xp_gain = .05

        if failed:  # Get only a third of xp when failing
            xp_gain *= 0.33
        self.creature.gain_experience(STATS.COOKING, xp_gain)

        log_message = (
            "The recipe was too simple to improve {}'s cooking skills."
        ).format(self.creature.name)
        if xp_gain > 0.0:
            log_message = "{}'s cooking skills improved".format(
                self.creature.name
            )
            if xp_gain < .1:
                log_message += ' a bit.'
            elif xp_gain > 0.4:
                log_message += ' a lot.'
            else:
                log_message += '.'
        result = 'Successfully cooked {}'.format(self.recipe.name)
        if failed:
            result = 'Failed to cook {}'.format(self.recipe.name)

        self.creature.logger.add_entry(
            self.date,
            '{} ! {}'.format(result, log_message),
            self.activity_type,
            ENTRY_TYPE.INFO
        )

    def serialize(self):
        data = super().serialize()
        data['recipe_id'] = self.recipe.id

    def deserialize(self, data):
        super().deserialize(data)
        self.recipe = ObjectManager.game.inventory.recipes[data['recipe_id']]
