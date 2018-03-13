# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.Panel import Panel
from ui.Elements import AttributeLabel
from ui.Elements import Button

from Settings import Settings

from collections import namedtuple
from functools import partial


class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, x, y):
        return (
            x >= self.x and y >= self.y and
            x <= self.x + self.width and
            y <= self.y + self.height
        )


class Ui(object):
    TAB_GROUPS = namedtuple('tab_groups', [
        'CREATURE',
        'ADVENTURE'
    ])(
        'creature',
        'adventure'
    )

    def __init__(self, game):
        self.game = game

        self.panels = []
        self.callbacks = dict([
            (group, None) for group in self.TAB_GROUPS
        ])

        self.build()

    def register_callback(self, button_type, method):
        if button_type not in self.TAB_GROUPS:
            raise KeyError('Wrong group type')
        self.callbacks[button_type] = method

    def callback(self, button_type):
        if callable(self.callbacks[button_type]):
            self.callbacks[button_type]()

    def build(self):
        self.left_panel = Panel(0, Settings.HEIGHT - 450, 150, 445)
        self.central_panel = Panel(150, Settings.HEIGHT - 450, 250, 445)
        self.right_panel = Panel(
            400, Settings.HEIGHT - 450, Settings.WIDTH - 400, 445
        )
        self.bottom_panel = Panel(0, 0, Settings.WIDTH, 150)

        self.panels = [
            self.left_panel,
            self.central_panel,
            self.right_panel,
            self.bottom_panel
        ]

        self.build_creature_ui()
        self.build_bottom_ui()

    def build_creature_ui(self):
        group = self.TAB_GROUPS.CREATURE

        # Left panel
        self.left_panel.add_tab(group, True, 'Creatures', 1)

        # Central panel
        tab = self.central_panel.add_tab(group, True, 'Stats', 1)
        self.central_panel.add_label(
            tab, AttributeLabel(self.game, 'hp', pre='HP:')
        )
        self.central_panel.add_label(
            tab, AttributeLabel(self.game, 'strength', pre='Strength:')
        )
        self.central_panel.add_label(
            tab, AttributeLabel(self.game, 'agility', pre='Agility:')
        )
        self.central_panel.add_label(
            tab, AttributeLabel(self.game, 'stamina', pre='Stamina:')
        )
        self.central_panel.add_label(
            tab, AttributeLabel(self.game, 'speed', pre='Speed:')
        )
        self.central_panel.add_label(
            tab, AttributeLabel(self.game, 'hunger', pre='Hunger:')
        )
        self.central_panel.add_label(
            tab, AttributeLabel(self.game, 'tired', pre='Sleep:')
        )

        # Right panel
        self.right_panel.add_tab(group, True, 'Equipment', 1)
        self.right_panel.add_tab(group, True, 'Description', 1)

    def build_bottom_ui(self):
        tab = self.bottom_panel.add_tab('bottom', True)

        creature_button = Button('(c) Creatures')
        self.bottom_panel.add_button(tab, creature_button)

        inventory_button = Button('(i) Inventory')
        self.bottom_panel.add_button(tab, inventory_button)

        cook_button = Button('(o) Cook')
        self.bottom_panel.add_button(tab, cook_button)

        build_button = Button('(b) Build')
        self.bottom_panel.add_button(tab, build_button)

        feed_button = Button('(f) Feed')
        self.bottom_panel.add_button(tab, feed_button)

        equip_button = Button('(e) Equip')
        self.bottom_panel.add_button(tab, equip_button)

        mutate_button = Button('(m) Mutate')
        self.bottom_panel.add_button(tab, mutate_button)

        adventure_button = Button('(a) Adventure')
        self.bottom_panel.add_button(tab, adventure_button)

        self.bottom_panel.set_current_group('bottom')

        # Callbacks
        creature_button.register_handler(
            partial(self.callback, self.TAB_GROUPS.CREATURE)
        )

    def show_tab_group(self, tab_group):
        if tab_group not in self.TAB_GROUPS:
            raise KeyError('Wrong tab group')

        self.left_panel.set_current_group(tab_group)
        self.central_panel.set_current_group(tab_group)
        self.right_panel.set_current_group(tab_group)

    def mouse_motion(self, x, y):
        for panel in self.panels:
            panel.mouse_motion(x, y)

    def click(self, x, y):
        for panel in self.panels:
            if panel.is_dialog and panel.click(x, y):
                return True

        for panel in self.panels:
            if not panel.is_dialog and panel.click(x, y):
                return True
        return False

    def draw(self):
        for panel in self.panels:
            panel.draw()
