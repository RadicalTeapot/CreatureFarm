# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState
from ui.widget.widgets import ListEntry

from ObjectManager import ObjectManager


class AdventureModel:
    def __init__(self):
        self.adventures = {}
        self.all_creatures = {}
        self.selected_adventure = ''
        self.selected_creature = ''


class Adventure(UiState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._model = AdventureModel()

        # ################################################################### #
        #                            Ui bindings                              #
        # ################################################################### #
        self.creature_spinner.bind(
            text=lambda spinner, value: self.creature_selected(value)
        )
        self.start_button.bind(on_press=self.start_adventure)

    def __enter__(self):
        self.update_template_and_groups()
        self.update_adventures()
        self.populate_adventures_list()
        self.update_ui()
        return self

    def update_template_and_groups(self):
        # TODO Get template and group list from game and populate model dict
        # with it instead of using dummy data
        self._model.all_creatures = {
            'A': None,
            'B': None,
            'C': None,
        }

    def update_adventures(self):
        self._model.adventures = dict([
            (adventure.name, adventure)
            for adventure in ObjectManager.game.available_adventures()
        ])

    def populate_adventures_list(self):
        self.adventure_list.clear()

        for name in self._model.adventures.keys():
            entry = ListEntry.simple(name)
            entry.bind(
                on_press=lambda entry: self.adventure_selected(entry.name)
            )
            self.adventure_list.append(entry)

    def adventure_selected(self, name):
        self._model.selected_adventure = name
        self.creature_selected()
        self.update_ui()

    def creature_selected(self, name=''):
        self._model.selected_creature = name

    def update_ui(self):
        self.adventure_label.text = self._model.selected_adventure

        self.creature_spinner.values = self._model.all_creatures.keys()
        self.creature_spinner.text = self._model.selected_creature

    def start_adventure(self, button):
        print(
            f'{self._model.selected_creature} started adventure '
            f'{self._model.selected_adventure}'
        )
