# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui import Ui
from Inventory import Inventory

from functools import partial


class Game(object):
    def __init__(self, window):
        self.window = window

        self.creatures = []

        self.adventures = []

        self.inventory = Inventory()
        self.ui = Ui(self)

        # Callbacks
        self.ui.register_callback(
            self.ui.BUTTONS.FINISH_TURN, self.update
        )

    def get_unique_id(self):
        # HACK: This could be avoided by finding a way to store/pass pointers
        # to functions instead of values
        unique_id = 0
        ids = [creature.id for creature in self.creatures]
        ids.extend([adventure.id for adventure in self.adventures])
        ids = set(ids)
        while unique_id in ids:
            unique_id += 1
        return unique_id

    def update(self):
        for creature in self.creatures:
            creature.update()
        self.ui.refresh()

    def add_creature(self, creature):
        creature.id = self.get_unique_id()
        self.creatures.append(creature)

    def add_adventure(self, adventure):
        adventure.id = self.get_unique_id()
        self.adventures.append(adventure)

    def start_adventure(self):
        creature = self.ui._state.selected_creature
        adventure = self.ui._state.selected_adventure
        if adventure is None:
            self.ui.display_dialog('No adventure selected')
            return

        if creature is None or creature.busy:
            self.ui.display_dialog('Invalid creature selection')
            return

        creature.set_activity(
            adventure,
            adventure.duration,
            update_callback=partial(
                self.update_adventure, creature, adventure
            ),
            # TODO: use adventure id instead of the object itself
            end_callback=partial(
                self.finish_adventure, creature, adventure
            )
        )
        self.ui.refresh()

    def update_adventure(self, creature, adventure):
        adventure.update(creature)

    def finish_adventure(self, creature, adventure):
        rewards = adventure.finish()

        message = '{} just finished adventure {} !\n\nThey found:\n'.format(
            creature.name, adventure.title
        )
        for name, quantity in rewards:
            message += '    {}: {}\n'.format(name, quantity)
        self.ui.display_dialog(message)

        self.ui.refresh()

    def cook(self):
        creature = self.ui._state.selected_creature
        recipe = self.ui._state.selected_recipe

        if recipe is None:
            self.ui.display_dialog('No recipe selected')
            return

        if creature is None or creature.locked:
            self.ui.display_dialog('Invalid creature selection')
            return

        if not self.inventory.has_items(recipe.ingredients):
            self.ui.display_dialog('Ingredients not available')
            return

        self.inventory.take_items(recipe.ingredients)
        self.inventory.add_items(recipe.results)

    def draw(self):
        self.window.clear()
        self.ui.draw()
