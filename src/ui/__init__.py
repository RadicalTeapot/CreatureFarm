# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.Elements import Button
from ui.Elements import DescriptionLabel

from ui.Panel import Dialog
from ui.Panel import Panel

from Settings import Settings

from collections import namedtuple
from functools import partial

import pyglet


class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 0, 0)

        self.vertex_list = pyglet.graphics.vertex_list_indexed(
            4,
            [0, 1, 2, 2, 1, 3],
            ('v2i', self._build_vertices()),
            ('c3B', self._build_color())
        )

    def _build_vertices(self):
        return [
            self.x, self.y,
            self.x + self.width, self.y,
            self.x, self.y + self.height,
            self.x + self.width, self.y + self.height
        ]

    def _build_color(self):
        return [
            *self.color, *self.color, *self.color, *self.color
        ]

    def update_position(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.vertex_list.vertices = self._build_vertices()

    def update_color(self, color):
        self.color = color
        self.vertex_list.colors = self._build_color()

    def contains(self, x, y):
        return (
            x >= self.x and y >= self.y and
            x <= self.x + self.width and
            y <= self.y + self.height
        )

    def draw(self):
        self.vertex_list.draw(pyglet.gl.GL_TRIANGLES)


class UiState(object):
    def __init__(self, ui):
        self.ui = ui

    def enter(self):
        self.ui.left_panel.clear()
        self.ui.central_panel.clear()
        self.ui.right_panel.clear()

    @classmethod
    def refresh(cls, ui):
        return cls.enter()


class CreatureState(UiState):
    def __init__(self, ui):
        super().__init__(ui)
        self.selected_creature = None

    def enter(self):
        super().enter()

        if self.selected_creature is None and self.ui.game.creatures:
            self.selected_creature = self.ui.game.creatures[0]

        # Left panel
        tab = self.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in self.ui.game.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(
                partial(self.select_creature, creature)
            )
            buttons.append(button)
            button.pressed = (creature == self.selected_creature)
        self.ui.left_panel.add_buttons(tab, buttons)

        # Central panel
        self.ui.central_panel.add_tab(True, 'Stats', 1)
        self.display_creature_stats()

        # Right panel
        self.ui.right_panel.add_tab(True, 'Equipment', 1)
        self.ui.right_panel.add_tab(True, 'Description', 1)

    def select_creature(self, creature):
        self.selected_creature = creature
        self.display_creature_stats()

    def display_creature_stats(self):
        tab = self.ui.central_panel.get_tabs()[0]
        tab.clear()

        if self.selected_creature is None:
            return

        label = DescriptionLabel((
            'HP: {}\n\n'
            'Strength: {}\n\n'
            'Agility: {}\n\n'
            'Stamina: {}\n\n'
            'Speed: {}\n\n'
            'Hunger: {}\n\n'
            'Sleep: {}\n\n'
        ).format(
            self.selected_creature.hp,
            self.selected_creature.strength,
            self.selected_creature.agility,
            self.selected_creature.stamina,
            self.selected_creature.speed,
            self.selected_creature.hunger,
            self.selected_creature.tired
        ), tab.rect.width)
        tab.add_label(label)


class NewAdventureState(UiState):
    def __init__(self, ui):
        super().__init__(ui)

    def enter(self):
        super().enter()

        # Left panel
        tab = self.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in self.ui.game.creatures:
            name = creature.name
            button = Button(name)
            # button.register_handler(
            #     partial(self.ui.game.select_creature, creature)
            # )
            buttons.append(button)
            # if creature == self.selected_creature:
            #     button.pressed = True
        self.ui.left_panel.add_buttons(tab, buttons)

        # Central panel
        tab = self.ui.central_panel.add_tab(True, 'Adventures', 1)
        buttons = []
        for adventure in self.ui.game.adventures:
            count = len([
                running
                for running in self.ui.game.running_adventures
                if running.title == adventure.title
            ])
            button = Button('{} ({})'.format(adventure.title, count))
            button.register_handler(
                partial(self.ui.game.select_adventure, adventure)
            )
            buttons.append(button)
            # if adventure == self.selected_adventure:
            #     adventure.pressed = True
        self.ui.central_panel.add_buttons(tab, buttons)

        # Right panel
        tab = self.ui.right_panel.add_tab(True, 'Description', 1)
        button = Button('Start')
        button.is_tristate = False
        button.register_handler(self.ui.game.start_adventure)
        self.ui.right_panel.add_button(tab, button)


class CurrentAdventureState(UiState):
    def __init__(self, ui):
        super().__init__(ui)

    def enter(self):
        super().enter()
        # Left panel
        self.ui.left_panel.add_tab(True, 'Adventures', 1)

        # Central panel
        self.ui.central_panel.add_tab(True, 'Creatures', 1)

        # Right panel
        self.ui.right_panel.add_tab(True, 'Description', 1)


class Ui(object):
    STATE = namedtuple('state', [
        'CREATURE', 'NEW_ADVENTURE', 'CURRENT_ADVENTURE'
    ])

    BUTTONS = namedtuple('buttons', [
        'CREATURE', 'START_ADVENTURE', 'CURRENT_ADVENTURE', 'FINISH_TURN'
    ])(0, 1, 2, 3)

    def __init__(self, game):
        self.STATE.CREATURE = CreatureState(self)
        self.STATE.NEW_ADVENTURE = NewAdventureState(self)
        self.STATE.CURRENT_ADVENTURE = CurrentAdventureState(self)

        self._state = self.STATE.CREATURE

        self.game = game
        self.dialogs = []

        self.panels = []
        self.callbacks = dict([
            (button, None) for button in self.BUTTONS
        ])

        self.build()

    def register_callback(self, button_type, method):
        if button_type not in self.BUTTONS:
            raise KeyError('Wrong button type')
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

        self.refresh()
        self.build_bottom_ui()

    def refresh(self):
        self._state.enter()

    def build_bottom_ui(self):
        tab = self.bottom_panel.add_tab(True)

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

        start_adventure_button = Button('(s) Start Adventure')
        self.bottom_panel.add_button(tab, start_adventure_button)

        current_adventures_button = Button('(u) Current Adventures')
        self.bottom_panel.add_button(tab, current_adventures_button)

        finish_turn_button = Button('(t) Finish Turn')
        finish_turn_button.is_tristate = False
        self.bottom_panel.add_button(tab, finish_turn_button)

        # Callbacks
        creature_button.register_handler(
            partial(self.callback, self.BUTTONS.CREATURE)
        )
        start_adventure_button.register_handler(
            partial(self.callback, self.BUTTONS.START_ADVENTURE)
        )
        current_adventures_button.register_handler(
            partial(self.callback, self.BUTTONS.CURRENT_ADVENTURE)
        )
        finish_turn_button.register_handler(
            partial(self.callback, self.BUTTONS.FINISH_TURN)
        )

    def display_dialog(self, text):
        self.dialogs.append(Dialog(text, self.close_dialog))

    def close_dialog(self):
        self.dialogs.pop()

    def set_state(self, state):
        self._state = state
        self.refresh()

    def mouse_motion(self, x, y):
        if self.dialogs:
            return self.dialogs[-1].mouse_motion(x, y)

        for panel in self.panels:
            panel.mouse_motion(x, y)

    def click(self, x, y):
        if self.dialogs:
            return self.dialogs[-1].click(x, y)

        for panel in self.panels:
            if panel.click(x, y):
                return True
        return False

    def draw(self):
        for panel in self.panels:
            panel.draw()

        if self.dialogs:
            self.dialogs[-1].draw()
