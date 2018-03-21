# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui import Ui

from functools import partial


class Game(object):
    def __init__(self, window):
        self.window = window

        self.creatures = []

        self.adventures = []
        self.running_adventures = []

        self.ui = Ui(self)

        # Callbacks
        self.ui.register_callback(
            self.ui.BUTTONS.CREATURE, self.set_creature_mode
        )
        self.ui.register_callback(
            self.ui.BUTTONS.START_ADVENTURE, self.set_adventure_mode
        )
        self.ui.register_callback(
            self.ui.BUTTONS.CURRENT_ADVENTURE, self.set_current_adventure_mode
        )
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
        for adventure in self.running_adventures:
            adventure.update()
        self.ui.refresh()

    def add_creature(self, creature):
        creature.id = self.get_unique_id()
        self.creatures.append(creature)

    def set_creature_mode(self):
        self.ui.set_state(self.ui.STATE.CREATURE)

    def add_adventure(self, adventure):
        adventure.id = self.get_unique_id()
        self.adventures.append(adventure)

    def set_adventure_mode(self):
        self.ui.set_state(self.ui.STATE.NEW_ADVENTURE)

    def start_adventure(self):
        creature = self.ui._state.selected_creature
        adventure = self.ui._state.selected_adventure
        if adventure is None:
            self.ui.display_dialog('No adventure selected')
            return

        if creature is None or creature.locked:
            self.ui.display_dialog('Invalid creature selection')
            return

        adventure.assign_creature(creature)
        new_adventure = adventure.start()
        # TODO: use adventure id instead of the object itself
        new_adventure.callback = partial(
            self.finish_adventure, adventure=new_adventure
        )
        self.running_adventures.append(new_adventure)
        self.ui.refresh()

    def finish_adventure(self, rewards, adventure):
        message = '{} just finished adventure {} !\n\nThey found:\n'.format(
            adventure.creature.name, adventure.title
        )
        for name, quantity in rewards:
            message += '    {}: {}\n'.format(name, quantity)
        self.ui.display_dialog(message)
        self.running_adventures = [
            running
            for running in self.running_adventures
            if running != adventure
        ]
        self.ui.refresh()

    def set_current_adventure_mode(self):
        self.ui.set_state(self.ui.STATE.CURRENT_ADVENTURE)

    def draw(self):
        self.window.clear()
        self.ui.draw()
