# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui import Button
from ui import Ui
from functools import partial


class Game(object):
    def __init__(self, window):
        self.window = window

        self.creatures = []
        self.selected_creature = None

        self.adventures = []
        self.running_adventures = []
        self.selected_adventure = None

        self.ui = Ui(self)

        # Callbacks
        self.ui.register_callback(
            self.ui.BUTTONS.CREATURE, self.show_creatures
        )
        self.ui.register_callback(
            self.ui.BUTTONS.START_ADVENTURE, self.set_adventure_mode
        )
        self.ui.register_callback(
            self.ui.BUTTONS.FINISH_TURN, self.update
        )

    def update(self):
        for adventure in self.running_adventures:
            adventure.update()

    def add_creature(self, creature):
        self.creatures.append(creature)

    def show_creatures(self):
        self.ui.show_tab_group(self.ui.TAB_GROUPS.CREATURE)

        tab = self.ui.left_panel.get_tabs()[0]
        self.ui.left_panel.clear(tab)
        buttons = []
        for creature in self.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(partial(self.select_creature, creature))
            buttons.append(button)
            if creature == self.selected_creature:
                button.pressed = True
        self.ui.left_panel.add_buttons(tab, buttons)

    def select_creature(self, creature):
        self.selected_creature = creature

    @property
    def hp(self):
        if self.selected_creature:
            return self.selected_creature.hp
        return '-'

    @property
    def strength(self):
        if self.selected_creature:
            return self.selected_creature.strength
        return '-'

    @property
    def agility(self):
        if self.selected_creature:
            return self.selected_creature.agility
        return '-'

    @property
    def stamina(self):
        if self.selected_creature:
            return self.selected_creature.stamina
        return '-'

    @property
    def speed(self):
        if self.selected_creature:
            return self.selected_creature.speed
        return '-'

    @property
    def hunger(self):
        if self.selected_creature:
            return self.selected_creature.hunger
        return '-'

    @property
    def tired(self):
        if self.selected_creature:
            return self.selected_creature.tired
        return '-'

    def add_adventure(self, adventure):
        self.adventures.append(adventure)

    def set_adventure_mode(self):
        self.ui.show_tab_group(self.ui.TAB_GROUPS.START_ADVENTURE)

        tab = self.ui.left_panel.get_tabs()[0]
        self.ui.left_panel.clear(tab)
        buttons = []
        for creature in self.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(partial(self.select_creature, creature))
            buttons.append(button)
            if creature == self.selected_creature:
                button.pressed = True
        self.ui.left_panel.add_buttons(tab, buttons)

        tab = self.ui.central_panel.get_tabs()[0]
        self.ui.central_panel.clear(tab)
        buttons = []
        for adventure in self.adventures:
            count = len([
                running
                for running in self.running_adventures
                if running.title == adventure.title
            ])
            button = Button('{} ({})'.format(adventure.title, count))
            button.register_handler(partial(self.select_adventure, adventure))
            buttons.append(button)
            if adventure == self.selected_adventure:
                adventure.pressed = True
        self.ui.central_panel.add_buttons(tab, buttons)

    def select_adventure(self, adventure):
        self.selected_adventure = adventure

    def start_adventure(self):
        if self.selected_adventure is None:
            self.ui.display_dialog('No adventure selected')
            return

        if self.selected_creature is None or self.selected_creature.locked:
            self.ui.display_dialog('Invalid creature selection')
            return

        self.selected_adventure.assign_creature(self.selected_creature)
        adventure = self.selected_adventure.start()
        adventure.callback = partial(
            self.finish_adventure, adventure=adventure
        )
        self.running_adventures.append(adventure)
        self.set_adventure_mode()

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

    def draw(self):
        self.window.clear()
        self.ui.draw()
