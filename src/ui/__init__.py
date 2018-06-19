# -*- coding: utf-8 -*-
"""DOCSTRING."""

from enum import Enum

from .screen.main_menu import MainMenu
from .screen.template_editor import TemplateEditor
from .screen.group_manager import GroupManager
from .screen.adventure import Adventure
from .screen.current_adventure import CurrentAdventure
from .widget.dialog import EscapeMenu

from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.factory import Factory
from kivy.uix.widget import Widget

from kivy.app import App

from ObjectManager import ObjectManager


class State(Enum):
    MAIN_MENU = 0
    TEMPLATE_EDITOR = 1
    GROUP_MANAGER = 2
    ADVENTURE = 3
    CURRENT_ADVENTURE = 4


class Ui(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_widget = UiWidget()

        self._states = {
            State.MAIN_MENU: MainMenu(),
            State.TEMPLATE_EDITOR: TemplateEditor(),
            State.GROUP_MANAGER: GroupManager(),
            State.ADVENTURE: Adventure(),
            State.CURRENT_ADVENTURE: CurrentAdventure(),
        }

        self.set_state(State.TEMPLATE_EDITOR)

    def build(self):
        return self.main_widget

    @property
    def state(self):
        return self._state

    def set_state(self, state_type):
        if not isinstance(state_type, State):
            raise TypeError('Expected State, got {} instead'.format(
                type(state_type).__name__
            ))
        with self._states[state_type] as state:
            self.main_widget.layout.clear_widgets()
            if not state.hide_top_bar:
                self.main_widget.layout.add_widget(self.main_widget.top_bar)
            self.main_widget.layout.add_widget(state)

    def open_template_editor(self):
        self.set_state(State.TEMPLATE_EDITOR)

    def open_group_manager(self):
        self.set_state(State.GROUP_MANAGER)

    def open_adventure(self):
        self.set_state(State.ADVENTURE)

    def open_current_adventure(self):
        self.set_state(State.CURRENT_ADVENTURE)

    def update_biomass(self):
        self.main_widget.update_biomass()

    def open_escape_menu(self):
        self.main_widget.escape_menu.open()

    def update_adventure_count(self, count):
        self.main_widget.update_adventure_count(count)


class UiWidget(Widget):
    layout = ObjectProperty()
    dialog = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('data/kv/main.kv')
        Builder.apply_rules(self, 'ui')

        self.top_bar = Factory.TopBar()
        self.escape_menu = EscapeMenu()

    def update_biomass(self):
        self.top_bar.biomass = str(ObjectManager.game.biomass)

    def update_adventure_count(self, count):
        self.top_bar.running_adventures = str(count)
