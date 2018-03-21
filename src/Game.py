# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui import Button
from ui import DescriptionLabel
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

        tab = self.ui.left_panel.get_tabs()[0]
        buttons = []
        for adventure in self.adventures:
            count = len([
                running
                for running in self.running_adventures
                if running.id == adventure.id
            ])
            if count == 0:
                continue
            button = Button('{} ({})'.format(adventure.title, count))
            button.register_handler(
                partial(self.select_current_adventure, adventure.id)
            )
            buttons.append(button)
        self.ui.left_panel.add_buttons(tab, buttons)

    def select_current_adventure(self, adventure_id):
        creatures = [
            running.creature
            for running in self.running_adventures
            if adventure_id == running.id
        ]

        tab = self.ui.central_panel.get_tabs()[0]
        tab.clear()
        buttons = []
        for creature in creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(
                partial(
                    self.select_adventure_creature,
                    adventure_id,
                    creature.id
                )
            )
            buttons.append(button)
        self.ui.central_panel.add_buttons(tab, buttons)

        tab = self.ui.right_panel.get_tabs()[0]
        tab.clear()

    def select_adventure_creature(self, adventure_id, creature_id):
        tab = self.ui.right_panel.get_tabs()[0]
        tab.clear()
        adventure = [
            adventure
            for adventure in self.running_adventures
            if adventure.id == adventure_id
        ][0]
        # TODO: Also display a log of the adventure using multiple pages
        # if necessary
        label = DescriptionLabel((
            '{} turns left'.format(adventure.duration - adventure.clock)
        ), tab.rect.width
        )
        self.ui.right_panel.add_label(tab, label)

    def draw(self):
        self.window.clear()
        self.ui.draw()
